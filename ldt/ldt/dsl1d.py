"""
A typed signature for one-dimensional ARC grids.

Base types: ``G`` a grid (a tuple of colours, 0 the background), ``O`` an object
(its first cell and its colours, which may stretch outside the grid), ``N`` a
small number, ``C`` a colour, ``B`` a boolean. Programs have type ``G -> G``.

Segments are maximal runs of one non-background colour, blobs maximal runs of
non-background cells. A grid is rebuilt from objects by painting them, left to
right, on a blank grid of the same length; background cells of an object leave
the grid as it is, cells outside the grid are clipped.

Example
-------
>>> from ldt.bohm import Tree
>>> x0, x1 = Tree("x0"), Tree("x1")
>>> move_2 = Tree("map_segs", (Tree("shift", (Tree("n2"), x1)), x0))
>>> SPACE.compile(move_2)((0, 3, 3, 0, 0, 5, 0, 0))
(0, 0, 0, 3, 3, 0, 0, 5)
"""

from __future__ import annotations

from collections import Counter

from ldt.bohm import Primitive, Space, Ty, Undefined

Grid = tuple[int, ...]
Obj = tuple[int, tuple[int, ...]]


def segments(g: Grid) -> list[Obj]:
    out, i, n = [], 0, len(g)
    while i < n:
        c = g[i]
        if not c:
            i += 1
            continue
        j = i
        while j < n and g[j] == c:
            j += 1
        out.append((i, (c, ) * (j - i)))
        i = j
    return out


def blobs(g: Grid) -> list[Obj]:
    out, i, n = [], 0, len(g)
    while i < n:
        if not g[i]:
            i += 1
            continue
        j = i
        while j < n and g[j]:
            j += 1
        out.append((i, tuple(g[i:j])))
        i = j
    return out


def paint(n: int, objs) -> Grid:
    out = [0] * n
    for start, cells in objs:
        for k, c in enumerate(cells):
            x = start + k
            if c and 0 <= x < n:
                out[x] = c
    return tuple(out)


def check_obj(o: Obj) -> Obj:
    if not o[1]:
        raise Undefined("empty object")
    return o


def gap_right(g: Grid, o: Obj) -> int:
    """The number of background cells between ``o`` and the next cell of ``g``,
    or to the border when there is none."""
    end = o[0] + len(o[1]) - 1
    x = max(end + 1, 0)
    while x < len(g) and not g[x]:
        x += 1
    return x - end - 1


def majority(cells) -> int:
    return Counter(c for c in cells if c).most_common(1)[0][0]


def fill_pairs(g: Grid) -> Grid:
    out = list(g)
    for c in sorted(set(g) - {0}):
        xs = [i for i, v in enumerate(g) if v == c]
        for a, b in zip(xs[0::2], xs[1::2]):
            out[a:b + 1] = [c] * (b + 1 - a)
    return tuple(out)


def pick(p, g: Grid) -> Obj:
    for o in segments(g):
        if p(o):
            return o
    raise Undefined("pick found nothing")


def hollow(o: Obj) -> Obj:
    cells = o[1]
    if len(cells) < 3:
        return o
    return o[0], (cells[0], ) + (0, ) * (len(cells) - 2) + (cells[-1], )


def grow(n: int, o: Obj) -> Obj:
    cells = o[1]
    return o[0] - n, (cells[0], ) * n + cells + (cells[-1], ) * n


def reflect(p: Obj, o: Obj) -> Obj:
    twice_centre = 2 * p[0] + len(p[1]) - 1
    return twice_centre - (o[0] + len(o[1]) - 1), o[1][::-1]


def ite(b, x, y):
    return x() if b() else y()


def max_size(g: Grid) -> int:
    return max((len(o[1]) for o in segments(g)), default=0)


def _sig(name, ty, fn, lazy=False):
    return Primitive(name, Ty.parse(ty), fn, lazy)


PRIMITIVES = [
    # grid to grid
    _sig("map_segs", "(O -> O) -> G -> G",
         lambda f, g: paint(len(g), (check_obj(f(o)) for o in segments(g)))),
    _sig("map_blobs", "(O -> O) -> G -> G",
         lambda f, g: paint(len(g), (check_obj(f(o)) for o in blobs(g)))),
    _sig("keep_segs", "(O -> B) -> G -> G",
         lambda p, g: paint(len(g), (o for o in segments(g) if p(o)))),
    _sig("fill_pairs", "G -> G", fill_pairs),
    _sig("reverse_grid", "G -> G", lambda g: g[::-1]),
    # object to object
    _sig("shift", "N -> O -> O", lambda n, o: (o[0] + n, o[1])),
    _sig("shift_l", "N -> O -> O", lambda n, o: (o[0] - n, o[1])),
    _sig("recolor", "C -> O -> O", lambda c, o: (o[0], (c, ) * len(o[1]))),
    _sig("reverse_obj", "O -> O", lambda o: (o[0], o[1][::-1])),
    _sig("hollow", "O -> O", hollow),
    _sig("majority", "O -> O",
         lambda o: (o[0], (majority(o[1]), ) * len(o[1]))),
    _sig("grow", "N -> O -> O", grow),
    _sig("slide", "G -> O -> O", lambda g, o: (o[0] + gap_right(g, o), o[1])),
    _sig("stretch", "G -> O -> O",
         lambda g, o: (o[0], o[1] + (o[1][-1], ) * gap_right(g, o))),
    _sig("reflect", "O -> O -> O", reflect),
    _sig("ite", "B -> O -> O -> O", ite, lazy=True),
    _sig("pick", "(O -> B) -> G -> O", pick),
    # predicates
    _sig("size_eq", "N -> O -> B", lambda n, o: len(o[1]) == n),
    _sig("size_gt", "N -> O -> B", lambda n, o: len(o[1]) > n),
    _sig("odd", "O -> B", lambda o: len(o[1]) % 2 == 1),
    _sig("not_", "B -> B", lambda b: not b),
    _sig("colour_eq", "C -> O -> B", lambda c, o: majority(o[1]) == c),
    # numbers and colours
    _sig("max_size", "G -> N", max_size),
    _sig("size", "O -> N", lambda o: len(o[1])),
    _sig("colour", "O -> C", lambda o: majority(o[1])),
] + [_sig(f"n{k}", "N", k) for k in range(6)]\
  + [_sig(f"c{k}", "C", k) for k in range(10)]

PYTHON_TYPES = {"G": tuple, "O": tuple, "N": int, "C": int, "B": bool}

SPACE = Space(PRIMITIVES, Ty.parse("G -> G"), depth=6, arity=3, max_vars=3)
