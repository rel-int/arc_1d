"""
Abstract evaluation of partial Böhm trees: the link from the program lattice
to the output lattice.

A partial tree has ``None`` (Omega) where a subtree is unknown. Evaluation is
Scott-continuous, so a partial tree denotes a partial output that every
completion refines: here an output grid is abstracted cell by cell as the set
of colours it may take (the paper's grid powerset lattice), a bitmask per cell.
If a demonstration's output is outside that set, no completion of the tree is
consistent: a sound conflict, found before the tree is total. On the test input
the same evaluation gives the output-lattice state the program state implies.

Abstract values are :data:`TOP` (anything), concrete values, or the refined
forms :class:`Cells` (a grid of colour masks) and :class:`Shape` (an object
whose start or colours are partly unknown). A primitive with no abstract
transformer returns :data:`TOP` as soon as one argument is not concrete, which
is sound and coarse; :data:`TRANSFORMERS` refines the ones that matter.
"""

from __future__ import annotations

from dataclasses import dataclass

from ldt.bohm import Space, Tree, Undefined, is_variable

ALL = (1 << 10) - 1  # every colour


class Unknown:
    """Abstract values refuse to be read as booleans, so that a concrete
    primitive never silently treats an unknown condition as true."""

    def __bool__(self):
        raise TypeError("an abstract value has no truth value")


class Top(Unknown):
    def __repr__(self):
        return "TOP"


TOP = Top()


@dataclass(frozen=True)
class Cells(Unknown):
    """A grid of colour masks."""
    masks: tuple[int, ...]


@dataclass(frozen=True)
class Shape(Unknown):
    """An object with a possibly unknown start and per-cell colour masks."""
    start: int | None
    masks: tuple[int, ...]


def concrete(v) -> bool:
    return not isinstance(v, Unknown)


def mask_of(c: int) -> int:
    return 1 << c


def shape(o) -> Shape:
    return o if isinstance(o, Shape) else Shape(o[0], tuple(map(mask_of, o[1])))


def join(a, b):
    if concrete(a) and concrete(b) and a == b:
        return a
    if isinstance(a, Top) or isinstance(b, Top):
        return TOP
    if isinstance(a, Cells) or isinstance(b, Cells) or isinstance(a, tuple)\
            and a and isinstance(a[0], int) and isinstance(b, tuple)\
            and b and isinstance(b[0], int):
        ma, mb = cells(a), cells(b)
        if ma is None or mb is None or len(ma.masks) != len(mb.masks):
            return TOP
        return Cells(tuple(x | y for x, y in zip(ma.masks, mb.masks)))
    try:
        sa, sb = shape(a), shape(b)
    except (TypeError, IndexError):
        return TOP
    if len(sa.masks) != len(sb.masks):
        return TOP
    return Shape(sa.start if sa.start == sb.start else None,
                 tuple(x | y for x, y in zip(sa.masks, sb.masks)))


def cells(g) -> Cells | None:
    if isinstance(g, Cells):
        return g
    if isinstance(g, tuple) and all(isinstance(c, int) for c in g):
        return Cells(tuple(map(mask_of, g)))
    return None


def paint(n: int, objs) -> Cells | tuple:
    """Paint abstract objects left to right, as :func:`ldt.dsl1d.paint`."""
    out = [mask_of(0)] * n
    for o in objs:
        if isinstance(o, Top):
            return Cells((ALL, ) * n)
        s = shape(o)
        transparent = [m & 1 for m in s.masks]
        colours = [m & ~1 for m in s.masks]
        if s.start is None:
            union = 0
            for c in colours:
                union |= c
            out = [m | union for m in out]
            continue
        for k, (c, t) in enumerate(zip(colours, transparent)):
            x = s.start + k
            if 0 <= x < n and c:
                out[x] = c | (out[x] if t else 0)
    if all(m & (m - 1) == 0 for m in out):
        return tuple(m.bit_length() - 1 for m in out)
    return Cells(tuple(out))


def compatible(value, expected) -> bool:
    """Whether some completion may produce ``expected``."""
    if isinstance(value, Top):
        return True
    if isinstance(value, Cells):
        return len(value.masks) == len(expected) and all(
            m >> c & 1 for m, c in zip(value.masks, expected))
    return value == expected


# ----------------------------------------------------- abstract transformers

def _map(objects):
    def transformer(f, g):
        if not concrete(g):
            return TOP
        return paint(len(g), [f(o) for o in objects(g)])
    return transformer


def _keep(f, g):
    from ldt.dsl1d import segments
    if not concrete(g):
        return TOP
    kept = []
    for o in segments(g):
        b = f(o)
        if b is True:
            kept.append(o)
        elif b is not False:
            kept.append(Shape(o[0], tuple(mask_of(c) | 1 for c in o[1])))
    return paint(len(g), kept)


def _shift(sign):
    def transformer(n, o):
        if isinstance(o, Top):
            return TOP
        s = shape(o)
        if not concrete(n) or s.start is None:
            return Shape(None, s.masks)
        return Shape(s.start + sign * n, s.masks)
    return transformer


def _recolor(c, o):
    if isinstance(o, Top):
        return TOP
    s = shape(o)
    m = mask_of(c) if concrete(c) else ALL
    return Shape(s.start, (m, ) * len(s.masks))


def _ite(b, x, y):
    b = b()
    if b is True:
        return x()
    if b is False:
        return y()
    branches = []
    for branch in (x, y):
        try:
            branches.append(branch())
        except Undefined:
            pass  # a completion may still take the other branch
    if not branches:
        raise Undefined("both branches undefined")
    return branches[0] if len(branches) == 1 else join(*branches)


def transformers_1d():
    from ldt.dsl1d import blobs, segments
    return {
        "map_segs": _map(segments), "map_blobs": _map(blobs),
        "keep_segs": _keep, "shift": _shift(1), "shift_l": _shift(-1),
        "recolor": _recolor, "ite": _ite,
    }


# ------------------------------------------------------------- evaluation

class Abstract:
    """Abstract evaluation of partial trees over a :class:`Space`."""

    def __init__(self, space: Space, transformers: dict):
        self.space, self.transformers = space, transformers

    def compile(self, tree: Tree | None):
        return self._compile(tree, self.space.root, ())([])

    def _compile(self, tree, ty, context):
        scope = context + ty.args
        depth = len(context)
        body = self._body(tree, scope)
        if not ty.args:
            return body

        def closure(env):
            return lambda *xs: body(env[:depth] + list(xs))
        return closure

    def _body(self, tree, scope):
        if tree is None:
            return lambda env: TOP
        head = tree.head
        if is_variable(head):
            i = int(head[1:])
            return lambda env: env[i]
        prim = self.space.prims[head]
        if not prim.arity:
            return lambda env: prim.fn
        args = [self._compile(a, t, scope)
                for a, t in zip(tree.args, prim.type.args)]
        abstract = self.transformers.get(head)

        def apply(env):
            if prim.lazy:
                thunks = [(lambda a=a: a(env)) for a in args]
                if abstract is not None:
                    return abstract(*thunks)
                values = [t() for t in thunks]
            else:
                values = [a(env) for a in args]
            if all(concrete(v) or callable(v) for v in values):
                try:
                    return prim.fn(*values) if not prim.lazy else prim.fn(
                        *[(lambda v=v: v) for v in values])
                except Undefined:
                    raise
                except TypeError:
                    pass  # a callable that returns abstract values
            if abstract is not None:
                return abstract(*values)
            return TOP
        return apply

    def conflict(self, tree: Tree | None, train) -> bool:
        """Whether no completion of ``tree`` is consistent with ``train``."""
        f = self.compile(tree)
        for x, y in train:
            try:
                if not compatible(f(x), y):
                    return True
            except (Undefined, IndexError, ValueError, TypeError,
                    RecursionError):
                if tree is not None and _total(tree):
                    return True
        return False


def _total(tree: Tree) -> bool:
    return all(a is not None and _total(a) for a in tree.args)


def partial_tree(space: Space, x) -> Tree | None:
    """The decided part of a state, Omega below the first undecided address:
    ``x`` is (positions, labels), boolean."""
    count = x.sum(-1)

    def build(a, ty, context):
        if count[a] != 1:
            return None
        head = space.vocab[int(x[a].argmax())]
        scope = context + ty.args
        head_ty = space.head_type(head, scope)
        if head_ty is None:
            return None
        return Tree(head, tuple(
            build(space.child(a, j), t, scope) if space.child(a, j)
            < space.n_positions else None
            for j, t in enumerate(head_ty.args)))
    return build(0, space.root, ())
