"""
The semantics of diagrams: a functor from the free category on the library
into PyTorch modules.

The search only ever calls :meth:`Semantics.model` on a term and gets back a
:class:`Model`, a ``torch.nn.Module`` from grids to grids that knows its
parameter cost. :class:`TraceFree` is the one implementation: a
``discopy.neural.network.Functor`` sending each box of the symbolic diagram
to a box carrying a fresh module for its entry, the copies and discards
being those of the target, then ``discopy.neural.torch.Module`` compiling the
image to a function on tensors. A neural geometry of interaction, i.e.
``Int(NN)`` with the trace as a fixpoint, is another :class:`Semantics` with
the same ``model``; nothing in ``dc.wake`` or ``dc.abstract`` changes.
"""

from __future__ import annotations

from typing import Protocol

import torch
from torch import nn

from discopy.neural import network
from discopy.neural.torch import Module

from dc.library import PRIMITIVES, Library
from dc.terms import Term, to_diagram


class Model(nn.Module):
    """
    A term compiled to a module from ``(batch, length, 10)`` grids to grids.
    ``slots`` maps the path of each node to its module, ``prior`` each
    parameter to the value it started from, i.e. the mean of its code.
    """
    def __init__(self, term: Term, slots: dict[str, nn.Module], compiled: nn.Module):
        super().__init__()
        self.term, self.compiled = term, compiled
        self.slots = slots  # the same modules as ``compiled``'s, not registered twice
        self.prior = {name: p.detach().clone() for name, p in self.slot_parameters()}

    def forward(self, grid):
        return self.compiled(grid)

    def slot_parameters(self):
        for path, module in self.slots.items():
            for name, p in module.named_parameters():
                yield f"{path}.{name}", p

    def deviations(self):
        return [p - self.prior[name] for name, p in self.slot_parameters()]

    def param_bits(self, delta: float) -> torch.Tensor:
        """
        The parameter cost: each parameter coded as its deviation from its
        prior value, quantised to ``delta``, at ``log2(1 + |d| / delta)``
        bits. An unchanged parameter is free; a library entry reused as
        learned is free; a large change costs logarithmically in its size.
        """
        total = torch.zeros(())
        for d in self.deviations():
            total = total + torch.log2(1 + d.abs() / delta).sum()
        return total

    def shrink(self, step: float):
        """Soft-threshold every deviation from the prior by ``step``, the proximal step of an L1 penalty."""
        with torch.no_grad():
            for name, p in self.slot_parameters():
                d = p - self.prior[name]
                p.copy_(self.prior[name] + d.sign() * (d.abs() - step).clamp(min=0))

    def snap(self, delta: float):
        """Round deviations below half a quantum back to the prior, as the code would."""
        with torch.no_grad():
            for name, p in self.slot_parameters():
                small = (p - self.prior[name]).abs() < delta / 2
                p[small] = self.prior[name][small]


class Semantics(Protocol):
    def model(self, term: Term, library: Library) -> Model: ...


class TraceFree:
    """Feedforward networks: the functor into PyTorch modules of ``discopy.neural.torch``."""

    def module(self, entry_name: str, library: Library) -> nn.Module:
        """A fresh module for one box, at its prior: initial weights, or the learned ones of an abstraction."""
        entry = library[entry_name]
        if entry.is_primitive:
            return PRIMITIVES[entry_name][0]()
        model = self.model(entry.body, library)
        with torch.no_grad():
            for name, p in model.slot_parameters():
                p.copy_(entry.weights[name])
        model.prior = {name: p.detach().clone() for name, p in model.slot_parameters()}
        return model

    def compile(self, diagram: network.Network, library: Library) -> tuple[Module, dict]:
        """
        The image of a symbolic diagram, whose boxes carry a :class:`dc.terms.Slot`,
        under the functor sending each box to a box with a fresh module for its
        entry, and every copy, discard and swap to itself; compiled to a
        ``torch.nn.Module``. Also returns the module of each slot by path.
        """
        slots = {}

        def ar_map(box):
            slot = box.module
            slots[slot.path] = self.module(slot.entry, library)
            return network.Box(box.name, box.dom, box.cod, module=slots[slot.path])

        functor = network.Functor(ob_map=lambda x: x, ar_map=ar_map)
        return Module(functor(diagram)), slots

    def model(self, term: Term, library: Library) -> Model:
        compiled, slots = self.compile(to_diagram(term, library), library)
        return Model(term, slots, compiled)


def nll_bits(output: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """The code length in bits of the target colours under the predicted distributions."""
    p = output.gather(-1, target[..., None]).squeeze(-1).clamp(min=1e-9)
    return -torch.log2(p).sum()

