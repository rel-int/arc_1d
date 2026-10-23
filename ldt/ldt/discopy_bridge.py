"""
The bridge to ``discopy.closed`` (rel-int/discopy-next), the reference semantics.

A :class:`ldt.bohm.Tree` becomes a ``closed`` term whose free variables are the
signature; ``closed.LeftmostOutermost`` reduces it back to a ``closed.BohmTree``
whose heads index the signature followed by the bound variables, so that
:func:`from_bohm` reads our tree back. ``closed.Functor`` into
``python.Function`` evaluates it. The fast interpreter of
:meth:`ldt.bohm.Space.compile` is tested against both.

Example
-------
>>> from ldt.bohm import Tree
>>> from ldt.dsl1d import SPACE, PYTHON_TYPES
>>> tree = Tree("map_segs", (Tree("shift", (Tree("n1"), Tree("x1"))), Tree("x0")))
>>> bridge = Bridge(SPACE, PYTHON_TYPES)
>>> assert bridge.from_bohm(bridge.reduce(bridge.to_term(tree))) == tree
>>> bridge.evaluate(tree)((0, 3, 3, 0, 0))
(0, 0, 3, 3, 0)
"""

from __future__ import annotations

from discopy import closed
from discopy.python import Function

from ldt.bohm import Space, Tree, Ty, is_variable


def curry(fn, n):
    if n <= 1:
        return fn
    return lambda a: curry(lambda *rest: fn(a, *rest), n - 1)


class Bridge:
    """
    Parameters:
        space : The signature and its address space.
        python_types : The Python type of each base type, for the functor.
    """
    def __init__(self, space: Space, python_types: dict[str, type]):
        self.space = space
        self.base = {}
        self.signature = tuple(
            closed.Variable(p.name, self.ty(p.type)) for p in space.primitives)
        self.functor = closed.Functor(
            ob_map={t: python_types[name] for name, t in self.base.items()},
            ar_map={}, cod=Function)

    def ty(self, t: Ty) -> closed.Ty:
        if t.base not in self.base:
            self.base[t.base] = closed.Ty(t.base)
        result = self.base[t.base]
        for arg in reversed(t.args):
            result = self.ty(arg) >> result
        return result

    def to_term(self, tree: Tree, ty: Ty | None = None, scope=()):
        """The ``closed`` term of a tree, its bound variables named ``x`` and
        their de Bruijn level, so that no two variables in scope are equal."""
        ty = self.space.root if ty is None else ty
        if not ty.args:
            return self._body(tree, scope)
        first, rest = ty.args[0], Ty(ty.args[1:], ty.base)
        var = closed.Variable(f"x{len(scope)}", self.ty(first))
        body = self.to_term(tree, rest, scope + (var, ))
        return var.cod.abstraction_factory(var, body)

    def _body(self, tree, scope):
        if is_variable(tree.head):
            head = scope[int(tree.head[1:])]
            arg_types = self._variable_type(tree, scope)
        else:
            prim = self.space.prims[tree.head]
            head = self.signature[self.space.primitives.index(prim)]
            arg_types = prim.type.args
        for arg, t in zip(tree.args, arg_types):
            head = head(self.to_term(arg, t, scope))
        return head

    def _variable_type(self, tree, scope):
        assert not tree.args, "variables of higher type are not used yet"
        return ()

    def reduce(self, term) -> closed.BohmTree:
        return closed.LeftmostOutermost(None)(term, self.signature)

    def from_bohm(self, node: closed.BohmTree, depth: int = 0) -> Tree:
        """Our tree of a ``closed.BohmTree`` in the context of the signature."""
        n = len(self.signature)
        if node.head < n:
            head = self.signature[node.head].name
        else:
            head = f"x{node.head - n}"
        return Tree(head, tuple(self.from_bohm(node[i])
                                for i in range(len(node.spine))))

    def evaluate(self, tree: Tree):
        """The program as a Python function, by ``closed.Functor``."""
        bohm = self.reduce(self.to_term(tree))
        term = bohm.to_term(len(self.signature))
        impls = [curry(_strict(p), p.arity) if p.arity else p.fn
                 for p in self.space.primitives]
        return term.eval(self.functor, list(self.signature))(*impls)


def _strict(prim):
    """The primitive on values: ``python.Function`` evaluates every argument
    first, so ``ite`` is strict here, unlike :meth:`ldt.bohm.Space.compile`."""
    if prim.lazy:
        return lambda *args: prim.fn(*[(lambda a=a: a) for a in args])
    return prim.fn
