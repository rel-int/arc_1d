"""
Böhm trees of a simply-typed signature, laid out on a fixed address space.

A program is the Böhm tree of a closed term of a root type over a signature of
typed primitives: each node, of type ``A1 -> ... -> An -> b``, binds ``n`` new
variables and applies a head (a primitive or a variable in scope, numbered by de
Bruijn level) to the trees of its arguments. The node's type fixes its binders,
so a node is labelled by its head alone.

Trees live on the complete ``arity``-ary tree of ``depth`` levels in heap order:
position ``a`` has children ``arity * a + 1 + j``. The abstract domain of the
lattice deduction transformer is ``positions -> P(labels)`` where the labels are
the heads plus ``ABSENT`` for an address the tree does not reach. A partial Böhm
tree (``None`` for an unknown subtree, i.e. Omega) is the abstract element with a
singleton at each defined node and every label at each unknown one.

Well-typed trees are the language of a top-down tree automaton whose states are
``(type, context)``; :meth:`Space.propagate` intersects a candidate state with it
exactly, by arc consistency on the tree, see Freuder, *A sufficient condition for
backtrack-free search* (1982).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator

import numpy as np

ABSENT = "·"


def _any_matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Boolean matrix product: ``out[i, k] = any_j a[i, j] & b[j, k]``."""
    return (a.astype(np.int32) @ b.astype(np.int32)) > 0


class Undefined(Exception):
    """A primitive applied outside its domain, e.g. ``pick`` finding nothing."""


@dataclass(frozen=True)
class Ty:
    """The type ``args[0] -> ... -> args[-1] -> base``."""
    args: tuple[Ty, ...]
    base: str

    def __str__(self):
        if not self.args:
            return self.base
        return " -> ".join(
            f"({a})" if a.args else str(a) for a in self.args) + " -> " + self.base

    @staticmethod
    def parse(text: str) -> Ty:
        """
        >>> print(Ty.parse("(O -> O) -> G -> G"))
        (O -> O) -> G -> G
        """
        tokens = re.findall(r"->|\(|\)|\w+", text)

        def arrow(i):
            left, i = atom(i)
            if i < len(tokens) and tokens[i] == "->":
                right, i = arrow(i + 1)
                return Ty((left, ) + right.args, right.base), i
            return left, i

        def atom(i):
            if tokens[i] == "(":
                result, i = arrow(i + 1)
                return result, i + 1
            return Ty((), tokens[i]), i + 1

        result, i = arrow(0)
        assert i == len(tokens), text
        return result


@dataclass(frozen=True)
class Primitive:
    """A typed constant with its semantics, curried into ``fn(*args)``."""
    name: str
    type: Ty
    fn: Any
    lazy: bool = False  # receives its arguments as thunks, e.g. ``ite``

    @property
    def arity(self):
        return len(self.type.args)


@dataclass(frozen=True)
class Tree:
    """A Böhm tree node: a head applied to argument trees."""
    head: str
    args: tuple[Tree, ...] = ()

    def __str__(self):
        if not self.args:
            return self.head
        return f"{self.head}(" + ", ".join(map(str, self.args)) + ")"

    @property
    def size(self) -> int:
        return 1 + sum(arg.size for arg in self.args)


def is_variable(head: str) -> bool:
    return head[0] == "x" and head[1:].isdigit()


@dataclass(frozen=True)
class State:
    """A state of the typing automaton: the node's type and the types in scope."""
    type: Ty | None  # None for an absent node
    context: tuple[Ty, ...]


@dataclass
class Space:
    """
    The address space, the label vocabulary and the typing automaton.

    Parameters:
        primitives : The signature.
        root : The type of the programs, e.g. ``G -> G``.
        depth : The number of levels of the address space.
        arity : The maximum number of arguments of a head.
        max_vars : The number of variable labels ``x0, x1, ...``.
    """
    primitives: list[Primitive]
    root: Ty
    depth: int = 6
    arity: int = 3
    max_vars: int = 4
    vocab: list[str] = field(init=False)

    def __post_init__(self):
        self.prims = {p.name: p for p in self.primitives}
        assert max(p.arity for p in self.primitives) <= self.arity
        self.vocab = [ABSENT] + [f"x{i}" for i in range(self.max_vars)] + [
            p.name for p in self.primitives]
        self.index = {v: i for i, v in enumerate(self.vocab)}
        self.n_positions = sum(self.arity ** d for d in range(self.depth))
        self.position_depth = np.concatenate([
            np.full(self.arity ** d, d) for d in range(self.depth)])
        self._build_automaton()

    # ------------------------------------------------------------------ space

    def child(self, position: int, j: int) -> int:
        return self.arity * position + 1 + j

    def levels(self) -> list[range]:
        start, out = 0, []
        for d in range(self.depth):
            out.append(range(start, start + self.arity ** d))
            start += self.arity ** d
        return out

    # -------------------------------------------------------------- automaton

    def head_type(self, head: str, context: tuple[Ty, ...]) -> Ty | None:
        if is_variable(head):
            i = int(head[1:])
            return context[i] if i < len(context) else None
        return self.prims[head].type

    def _build_automaton(self):
        absent = State(None, ())
        states, todo = [absent], [State(self.root, ())]
        index = {absent: 0}
        edges = [(0, self.index[ABSENT], (0, ) * self.arity)]
        while todo:
            state = todo.pop()
            if state in index:
                continue
            index[state] = q = len(states)
            states.append(state)
            scope = state.context + state.type.args
            for head in self.vocab[1:]:
                ty = self.head_type(head, scope)
                if ty is None or ty.base != state.type.base:
                    continue
                if any(len(scope) + len(a.args) > self.max_vars
                       for a in ty.args):
                    continue  # its argument would bind an unnameable variable
                children = tuple(State(a, scope) for a in ty.args)
                todo.extend(c for c in children if c not in index)
                edges.append((q, self.index[head], children))
        # resolve child states now that every state has an index
        self.states = states
        self.state_index = index
        self.edge_state = np.array([e[0] for e in edges])
        self.edge_label = np.array([e[1] for e in edges])
        self.edge_child = np.zeros((len(edges), self.arity), dtype=np.int64)
        for k, (_, _, children) in enumerate(edges):
            for j, c in enumerate(children):
                self.edge_child[k, j] = c if isinstance(c, int) else index[c]
        self.n_states, self.n_edges = len(states), len(edges)
        self.root_state = index[State(self.root, ())]
        V, E, Q = len(self.vocab), self.n_edges, self.n_states
        self.edge_label_matrix = np.zeros((E, V), dtype=bool)
        self.edge_label_matrix[np.arange(E), self.edge_label] = True
        self.edge_state_matrix = np.zeros((E, Q), dtype=bool)
        self.edge_state_matrix[np.arange(E), self.edge_state] = True
        self.edge_child_matrix = np.zeros((self.arity, E, Q), dtype=bool)
        for j in range(self.arity):
            self.edge_child_matrix[j, np.arange(E), self.edge_child[:, j]] = True

    # ------------------------------------------------------------ propagation

    def top(self) -> np.ndarray:
        """The top element: every label at every position, before typing."""
        return np.ones((self.n_positions, len(self.vocab)), dtype=bool)

    def typing(self):
        """The projection as a module on the device, see
        :class:`ldt.lattice.Typing`."""
        from ldt.lattice import Typing
        return Typing(self)

    def propagate(self, cand: np.ndarray) -> np.ndarray:
        """
        The exact projection onto each position of the well-typed trees within
        ``cand``, i.e. ``alpha(gamma(cand) & WellTyped)``. Empty everywhere iff
        no well-typed tree is left (the bottom element).
        """
        P, Q = self.n_positions, self.n_states
        label_of_edge = cand[:, self.edge_label]  # [P, E]
        support = np.zeros((P, self.n_edges), dtype=bool)
        alive = np.zeros((P, Q), dtype=bool)  # some supported edge from state q
        levels = self.levels()
        for d in reversed(range(self.depth)):
            idx = np.array(levels[d])
            ok = label_of_edge[idx].copy()
            for j in range(self.arity):
                if d == self.depth - 1:
                    child_alive = np.zeros((len(idx), Q), dtype=bool)
                    child_alive[:, 0] = True  # beyond the space only absent
                else:
                    child_alive = alive[self.arity * idx + 1 + j]
                ok &= child_alive[:, self.edge_child[:, j]]
            support[idx] = ok
            alive[idx] = _any_matmul(ok, self.edge_state_matrix)
        reach = np.zeros((P, Q), dtype=bool)
        reach[0, self.root_state] = True
        out = np.zeros_like(cand)
        for d in range(self.depth):
            idx = np.array(levels[d])
            active = support[idx] & reach[idx][:, self.edge_state]
            out[idx] = _any_matmul(active, self.edge_label_matrix)
            if d + 1 < self.depth:
                for j in range(self.arity):
                    reach[self.arity * idx + 1 + j] = _any_matmul(
                        active, self.edge_child_matrix[j])
        if not out[0].any():
            out[:] = False
        return out

    # --------------------------------------------------------------- encoding

    def encode(self, tree: Tree) -> np.ndarray:
        """The labels of a total tree, one per position."""
        labels = np.zeros(self.n_positions, dtype=np.int64)

        def go(node, a):
            if a >= self.n_positions:
                raise ValueError(f"{tree} does not fit depth {self.depth}")
            labels[a] = self.index[node.head]
            for j, arg in enumerate(node.args):
                go(arg, self.child(a, j))
        go(tree, 0)
        return labels

    def decode(self, labels: np.ndarray, a: int = 0) -> Tree | None:
        """The tree of a label vector, ``None`` where a label is absent."""
        head = self.vocab[labels[a]]
        if head == ABSENT:
            return None
        n = self._arity_of(labels, a)
        return Tree(head, tuple(
            self.decode(labels, self.child(a, j)) for j in range(n)))

    def _arity_of(self, labels, a):
        n = 0
        while n < self.arity and self.child(a, n) < self.n_positions\
                and labels[self.child(a, n)] != 0:
            n += 1
        return n

    def singleton(self, labels: np.ndarray) -> np.ndarray:
        cand = np.zeros((self.n_positions, len(self.vocab)), dtype=bool)
        cand[np.arange(self.n_positions), labels] = True
        return cand

    # ----------------------------------------------------------------- typing

    def check(self, tree: Tree, ty: Ty | None = None,
              context: tuple[Ty, ...] = ()) -> bool:
        """Whether ``tree`` is an eta-long normal form of type ``ty``."""
        ty = self.root if ty is None else ty
        scope = context + ty.args
        head_ty = self.head_type(tree.head, scope)
        if head_ty is None or head_ty.base != ty.base\
                or len(head_ty.args) != len(tree.args):
            return False
        return all(self.check(arg, a, scope)
                   for arg, a in zip(tree.args, head_ty.args))

    # -------------------------------------------------------------- semantics

    def compile(self, tree: Tree, ty: Ty | None = None) -> Callable:
        """
        The semantics of a closed tree of type ``ty`` as a Python function.
        Raises :class:`Undefined` when a primitive is applied outside its domain.
        """
        ty = self.root if ty is None else ty
        return self._compile(tree, ty, ())([])

    def _compile(self, tree, ty, context):
        """A function from an environment (a list) to the node's value."""
        scope = context + ty.args
        n_bound, depth = len(ty.args), len(context)
        body = self._compile_body(tree, scope)
        if not n_bound:
            return body

        def closure(env):
            return lambda *xs: body(env[:depth] + list(xs))
        return closure

    def _compile_body(self, tree, scope):
        head = tree.head
        if is_variable(head):
            i = int(head[1:])
            if not tree.args:
                return lambda env: env[i]
            args = [self._compile(a, t, scope)
                    for a, t in zip(tree.args, scope[i].args)]
            return lambda env: env[i](*[a(env) for a in args])
        prim = self.prims[head]
        if not prim.arity:
            value = prim.fn
            return lambda env: value
        args = [self._compile(a, t, scope)
                for a, t in zip(tree.args, prim.type.args)]
        fn = prim.fn
        if prim.lazy:
            return lambda env: fn(*[(lambda a=a: a(env)) for a in args])
        if len(args) == 1:
            a0, = args
            return lambda env: fn(a0(env))
        if len(args) == 2:
            a0, a1 = args
            return lambda env: fn(a0(env), a1(env))
        return lambda env: fn(*[a(env) for a in args])

    # ------------------------------------------------------------ enumeration

    def trees(self, size: int, ty: Ty | None = None,
              context: tuple[Ty, ...] = (), depth: int | None = None
              ) -> Iterator[Tree]:
        """Every eta-long normal form of exactly ``size`` nodes that fits."""
        ty = self.root if ty is None else ty
        depth = self.depth if depth is None else depth
        if size < 1 or depth < 1:
            return
        scope = context + ty.args
        for head in self.vocab[1:]:
            head_ty = self.head_type(head, scope)
            if head_ty is None or head_ty.base != ty.base:
                continue
            if not head_ty.args:
                if size == 1:
                    yield Tree(head)
                continue
            for args in self._spines(size - 1, head_ty.args, scope, depth - 1):
                yield Tree(head, args)

    def _spines(self, size, types, scope, depth):
        if not types:
            if size == 0:
                yield ()
            return
        first, rest = types[0], types[1:]
        for k in range(1, size - len(rest) + 1):
            for t in self.trees(k, first, scope, depth):
                for ts in self._spines(size - k, rest, scope, depth):
                    yield (t, ) + ts
