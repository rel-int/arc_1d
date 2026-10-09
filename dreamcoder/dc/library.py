"""
Wire types and the base library of typed boxes.

Two types of wire, both lists of shapes in the sense of ``discopy.neural``:

- ``GRID`` is ``Dims(Dim(10))``: a 1D grid as one distribution over the ten
  colours per cell, a tensor ``(batch, length, 10)``;
- ``FEAT`` is ``Dims(Dim(6, 10))``: six colour-valued features per cell, a
  tensor ``(batch, length, 6, 10)``, e.g. "the colour of my left neighbour" or
  "my colour, if my object has length one".

Every learned map acts on the colour axis through :func:`equivariant`, a
10x10 matrix with five parameters that commutes with every permutation of the
nine foreground colours, plus an absolute part that is free to name colours.
1D-ARC needs both: in most families the test pair uses a colour no training
pair shows, so a per-colour weight cannot generalise, while the recolouring
families paint fixed colours.

A box of the library is an :class:`Entry`: a primitive, whose module is built
by a class below, or an abstraction, whose module is the compiled diagram of
its body loaded with the weights it was learned with.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import torch
from torch import nn
from torch.nn.functional import pad, softmax

from discopy.neural.network import Dim, Dims

from dc.data import COLOURS

CHANNELS = 6
GRID, FEAT = Dims(Dim(COLOURS)), Dims(Dim(CHANNELS, COLOURS))
TYPES = {"Grid": GRID, "Feat": FEAT}
TAU = 10.0  # inverse temperature turning colour scores into a distribution
IDENTITY = (1., 0., 0., 1., 0.)  # bg->bg, bg->fg, fg->bg, fg->same fg, fg->other fg
ZERO = (0., 0., 0., 0., 0.)


def equivariant(theta: torch.Tensor) -> torch.Tensor:
    """
    The 10x10 matrices commuting with permutations of the foreground colours
    1..9, from ``theta = (bg->bg, bg->fg, fg->bg, fg->same, fg->other)``,
    batched over the leading dimensions of ``theta``.
    """
    bb, bf, fb, same, other = theta.unbind(-1)
    eye = torch.eye(COLOURS - 1)
    fg = other[..., None, None] + (same - other)[..., None, None] * eye
    top = torch.cat([bb[..., None, None], bf[..., None, None].expand(
        *bf.shape, 1, COLOURS - 1)], -1)
    bottom = torch.cat([fb[..., None, None].expand(*fb.shape, COLOURS - 1, 1), fg], -1)
    return torch.cat([top, bottom], -2)


def background_like(grid: torch.Tensor, length: int) -> torch.Tensor:
    """``length`` cells of background, batched like ``grid``."""
    cells = torch.zeros(grid.shape[0], length, COLOURS)
    cells[..., 0] = 1
    return cells


def shift_taps(grid: torch.Tensor, reach: int) -> torch.Tensor:
    """``(batch, length, 2 * reach + 1, 10)``: the cell at offset -reach..reach, background outside."""
    edge = background_like(grid, reach)
    padded = torch.cat([edge, grid, edge], 1)
    return torch.stack([padded[:, reach + o:reach + o + grid.shape[1]]
                        for o in range(-reach, reach + 1)], 2)


def foreground_mass(x: torch.Tensor) -> torch.Tensor:
    return x[..., 1:].sum(-1)


class Cells:
    """
    Which cells of a padded batch are grid: ``mask`` is ``(batch, length)``,
    set by :func:`dc.wake.wake_batch` while it fits tasks of different
    lengths together, ``None`` otherwise. Outside a grid is background, so
    every box producing a ``Grid`` puts background back in the padding, which
    is what ``shift``, ``local`` and ``scan`` read beyond the edge of an
    unpadded grid, and ``reflect`` reverses the grid cells alone.
    """
    mask: torch.Tensor | None = None


CELLS = Cells()


def confine(grid: torch.Tensor) -> torch.Tensor:
    """Background outside the grid cells of a padded batch."""
    if CELLS.mask is None:
        return grid
    return torch.where(CELLS.mask[..., None], grid, background_like(grid, grid.shape[1]))


class Recolour(nn.Module):
    """``Grid -> Grid``, per cell: an equivariant colour map plus an absolute one."""
    def __init__(self):
        super().__init__()
        self.theta = nn.Parameter(torch.tensor(IDENTITY))
        self.absolute = nn.Parameter(torch.zeros(COLOURS, COLOURS))
        self.bias = nn.Parameter(torch.zeros(COLOURS))

    def forward(self, grid):
        return confine(softmax(TAU * (grid @ (equivariant(self.theta) + self.absolute) + self.bias), -1))


class Shift(nn.Module):
    """``Grid -> Grid``, a translation: a convolution with a softmax over offsets -3..3, shared by all colours."""
    REACH = 3

    def __init__(self):
        super().__init__()
        self.offsets = nn.Parameter(torch.zeros(2 * self.REACH + 1))

    def forward(self, grid):
        # output cell t reads input cell t - o with weight softmax(offsets)[o]
        taps = shift_taps(grid, self.REACH).flip(2)
        return confine(torch.einsum("blod,o->bld", taps, softmax(self.offsets, 0)))


class Reflect(nn.Module):
    """``Grid -> Grid``, reversal of the grid, no parameters."""
    def forward(self, grid):
        if CELLS.mask is None:
            return grid.flip(1)
        position = torch.arange(grid.shape[1]).expand(grid.shape[:2])
        length = CELLS.mask.sum(1, keepdim=True)
        source = torch.where(CELLS.mask, length - 1 - position, position)
        return confine(grid.gather(1, source[..., None].expand(-1, -1, COLOURS)))


class Local(nn.Module):
    """``Grid -> Feat``, the neighbourhood: each channel a learned combination of the cells at offsets -3..3."""
    def __init__(self):
        super().__init__()
        taps = torch.zeros(CHANNELS, 2 * Shift.REACH + 1)
        for channel, offset in enumerate([-1, 1, -2, 2, -3, 3]):
            taps[channel, offset + Shift.REACH] = 1
        self.taps = nn.Parameter(taps)

    def forward(self, grid):
        return torch.einsum("blod,ko->blkd", shift_taps(grid, Shift.REACH), self.taps)


class Mix(nn.Module):
    """A learned mixing of the channels of a fixed feature extractor, the identity at first."""
    def __init__(self):
        super().__init__()
        self.mix = nn.Parameter(torch.eye(CHANNELS))

    def forward(self, grid):
        return torch.einsum("blkd,jk->bljd", self.features(grid), self.mix)


class Scan(Mix):
    """
    ``Grid -> Feat``, what lies left and right: the colour of the nearest
    foreground cell strictly on the left ``L`` and on the right ``R``, then
    ``L`` if there is foreground on the right, ``R`` if there is some on the
    left, ``L`` if an odd number of foreground cells lie on the left and ``R``
    if an odd number lie on the right.
    """
    @staticmethod
    def nearest(grid, fg):
        batch, length, _ = grid.shape
        position = torch.arange(length).expand(batch, length)
        last = torch.where(fg, position, -1).cummax(1).values
        before = torch.cat([torch.full((batch, 1), -1), last[:, :-1]], 1)
        found = before >= 0
        colours = grid.gather(1, before.clamp(min=0)[..., None].expand(-1, -1, COLOURS))
        colours = torch.where(found[..., None], colours, background_like(grid, length))
        count = torch.cat([torch.zeros(batch, 1), fg.float().cumsum(1)[:, :-1]], 1)
        return colours, found, count % 2 == 1

    def features(self, grid):
        fg = grid.argmax(-1) > 0
        left, found_left, odd_left = self.nearest(grid, fg)
        right, found_right, odd_right = (x.flip(1) for x in self.nearest(grid.flip(1), fg.flip(1)))
        keep = lambda x, mask: x * mask[..., None]
        return torch.stack([left, right, keep(left, found_right), keep(right, found_left),
                            keep(left, odd_left), keep(right, odd_right)], 2)


class Segment(Mix):
    """
    ``Grid -> Feat``, objects: maximal runs of one foreground colour. Each
    channel is the colour of the cell when its object has some property --
    length one, two, three, odd, the largest of the grid, and being one of
    its two end cells -- and nothing otherwise.
    """
    def features(self, grid):
        colour = grid.argmax(-1)
        batch, length = colour.shape
        fg = colour > 0
        previous = torch.cat([torch.full((batch, 1), -1), colour[:, :-1]], 1)
        following = torch.cat([colour[:, 1:], torch.full((batch, 1), -1)], 1)
        start, end = fg & (colour != previous), fg & (colour != following)
        run = start.long().cumsum(1) * fg
        size = torch.zeros(batch, length + 1).scatter_add(1, run, fg.float())
        size[:, 0] = 0
        cell_size = size.gather(1, run) * fg
        largest = cell_size == size.max(1, keepdim=True).values
        flags = [cell_size == 1, cell_size == 2, cell_size == 3,
                 cell_size % 2 == 1, largest, start | end]
        return torch.stack([grid * (f & fg)[..., None] for f in flags], 2)


class Paint(nn.Module):
    """
    ``Grid @ Feat -> Grid``, per cell: the colour scores of the cell and of
    each feature channel through an equivariant map each, plus absolute
    colours read from how much foreground each carries.
    """
    def __init__(self):
        super().__init__()
        self.theta = nn.Parameter(torch.tensor(IDENTITY))
        self.channels = nn.Parameter(torch.tensor([ZERO] * CHANNELS))
        self.absolute = nn.Parameter(torch.zeros(CHANNELS + 1, COLOURS))
        self.bias = nn.Parameter(torch.zeros(COLOURS))

    def forward(self, grid, feat):
        scores = grid @ equivariant(self.theta) + torch.einsum(
            "blkd,kde->ble", feat, equivariant(self.channels))
        mass = torch.cat([foreground_mass(grid)[..., None], foreground_mass(feat)], -1)
        return confine(softmax(TAU * (scores + mass @ self.absolute + self.bias), -1))


PRIMITIVES = {
    "recolour": (Recolour, ("Grid",), "Grid"),
    "shift": (Shift, ("Grid",), "Grid"),
    "reflect": (Reflect, ("Grid",), "Grid"),
    "local": (Local, ("Grid",), "Feat"),
    "scan": (Scan, ("Grid",), "Feat"),
    "segment": (Segment, ("Grid",), "Feat"),
    "paint": (Paint, ("Grid", "Feat"), "Grid"),
}
IDEMPOTENT = {"recolour", "reflect"}  # f(f(x)) is f(x) or x: never enumerated


@dataclass
class Entry:
    """
    A box of the library. A primitive names its module class; an
    abstraction carries its ``body``, a term over earlier entries, and the
    trained ``weights`` of that body, keyed by parameter name.
    """
    name: str
    dom: tuple[str, ...]
    cod: str
    body: object = None
    weights: dict = field(default_factory=dict)
    iteration: int = 0

    @property
    def is_primitive(self) -> bool:
        return self.body is None

    def signature(self) -> str:
        return f"{self.name} : {' @ '.join(self.dom)} -> {self.cod}"


@dataclass
class Library:
    """The entries by name, with their weight in the prior over terms."""
    entries: dict[str, Entry]
    weights: dict[str, float]

    @classmethod
    def base(cls) -> Library:
        entries = {name: Entry(name, dom, cod) for name, (_, dom, cod) in PRIMITIVES.items()}
        return cls(entries, {name: 1. for name in entries})

    def __getitem__(self, name: str) -> Entry:
        return self.entries[name]

    def __len__(self):
        return len(self.entries)

    def producing(self, cod: str) -> list[Entry]:
        return [e for e in self.entries.values() if e.cod == cod]
