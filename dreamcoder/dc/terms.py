"""
Terms over the library, their prior and their string diagrams.

A candidate program is a term in one variable ``x : Grid``: a tree whose
nodes are library entries applied to arguments of their ``dom`` types and
whose leaves are ``x``. A term is type-correct by construction, since
:func:`enumerate_terms` only ever fills an argument of type ``T`` with a term
of type ``T``. Its string diagram, :func:`to_diagram`, is
``Network.from_callable`` on the term read as a Python function: every use
of ``x`` beyond the first is a copy, every node a box.

Each box of the diagram carries a :class:`Slot` as its data: which entry it
is and where in the term it sits. The slot is what the semantics functor
replaces by a module, so two occurrences of one entry get two modules, and
what abstraction reads to find the trained weights of a subterm.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import cache

from discopy.neural.network import Box, Network

from dc.library import GRID, IDEMPOTENT, TYPES, Library

LEAF = 0.5  # prior probability that a Grid-typed node is the variable x


@dataclass(frozen=True)
class Term:
    head: str  # an entry name, or "x"
    args: tuple[Term, ...] = ()

    def __str__(self):
        return self.head if not self.args else f"{self.head}({', '.join(map(str, self.args))})"

    @property
    def size(self) -> int:
        """The number of boxes, i.e. of nodes that are not ``x``."""
        return (self.head != "x") + sum(a.size for a in self.args)

    @classmethod
    def parse(cls, text: str) -> Term:
        """The term printed as ``text``, e.g. ``Term.parse("paint(x, scan(x))")``."""
        term, rest = cls.read(text.replace(" ", ""))
        assert not rest, f"trailing {rest!r}"
        return term

    @classmethod
    def read(cls, text: str) -> tuple[Term, str]:
        head = text[:min((text.find(c) for c in "(,)" if c in text), default=len(text))]
        rest, args = text[len(head):], []
        if rest.startswith("("):
            rest = rest[1:]
            while True:
                arg, rest = cls.read(rest)
                args.append(arg)
                rest, done = rest[1:], rest[0] == ")"
                if done:
                    break
        return cls(head, tuple(args)), rest

    def subterms(self, path: str = "r"):
        """Every node with its path: ``r`` for the root, ``r_i`` for its ``i``-th argument, etc."""
        yield path, self
        for i, arg in enumerate(self.args):
            yield from arg.subterms(f"{path}_{i}")


X = Term("x")


@dataclass(frozen=True)
class Slot:
    """Where a box sits in its term: the entry and the path of its node."""
    entry: str
    path: str


def enumerate_terms(library: Library, max_size: int) -> list[Term]:
    """Every ``Grid``-typed term with at most ``max_size`` boxes, pruning ``f(f(x))`` for idempotent ``f``."""

    @cache
    def terms(cod: str, size: int) -> tuple[Term, ...]:
        found = [X] if cod == "Grid" and size == 0 else []
        for entry in library.producing(cod) if size > 0 else []:
            for args in arguments(entry.dom, size - 1):
                if entry.name in IDEMPOTENT and args[0].head == entry.name:
                    continue
                found.append(Term(entry.name, args))
        return tuple(found)

    @cache
    def arguments(dom: tuple[str, ...], size: int) -> tuple[tuple[Term, ...], ...]:
        if not dom:
            return ((),) if size == 0 else ()
        return tuple((first, *rest) for k in range(size + 1)
                     for first in terms(dom[0], k) for rest in arguments(dom[1:], size - k))

    return [t for size in range(1, max_size + 1) for t in terms("Grid", size)]


def structure_bits(term: Term, library: Library) -> float:
    """
    ``-log2`` of the probability of the term under a probabilistic grammar:
    a ``Grid`` node is ``x`` with probability ``LEAF``, otherwise an entry
    producing its type with probability proportional to the entry's weight.
    The weights are the box frequencies the abstraction step re-estimates.
    """
    cod = "Grid" if term.head == "x" else library[term.head].cod
    if term.head == "x":
        return -math.log2(LEAF)
    total = sum(library.weights[e.name] for e in library.producing(cod))
    p = library.weights[term.head] / total * ((1 - LEAF) if cod == "Grid" else 1)
    return -math.log2(p) + sum(structure_bits(a, library) for a in term.args)


def to_diagram(term: Term, library: Library) -> Network:
    """The string diagram ``Grid -> Grid`` of a term, its boxes carrying a :class:`Slot`."""

    def box(path: str, node: Term) -> Box:
        entry = library[node.head]
        dom = Network.ob().tensor(*(TYPES[t] for t in entry.dom))
        return Box(node.head, dom, TYPES[entry.cod], module=Slot(node.head, path))

    def evaluate(node: Term, path: str, x):
        if node.head == "x":
            return x
        args = [evaluate(a, f"{path}_{i}", x) for i, a in enumerate(node.args)]
        return box(path, node)(*args)

    return Network.from_callable(GRID, TYPES[library[term.head].cod])(
        lambda x: evaluate(term, "r", x))
