"""
Synthetic tasks: a random program, random inputs, and the programs equivalent
to it on the demonstrations.

Programs are drawn uniformly among the eta-long normal forms of a size drawn
uniformly from a range, by the counting recursion of
:class:`ldt.bohm.Space` — a prior with no weights tuned to any benchmark. A task
keeps the program when it is defined on every input, moves something, and does
not send every input to the same output.

Programs are where the alpha operator matters most: most programs consistent
with the demonstrations are bloated copies of a smaller one (``shift(n0, o)``,
``recolor(c, recolor(c', o))``), so the concrete domain is cut by Occam's razor.
A sampled program is first shrunk, one edit at a time, to a locally minimal
program consistent with the demonstrations; its size is the task's size, drawn
uniformly by rejection. The solution set ``Y`` that supervises the alpha
operator is that program plus every one-edit variant of it that is consistent
with the demonstrations and no larger: each subtree replaced by each tree of at
most ``bank_size`` nodes of the same automaton state.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from functools import lru_cache

import numpy as np

from ldt.bohm import Space, Tree, Ty, Undefined


class Sampler:
    """Uniform sampling of normal forms of a given size, by counting."""

    def __init__(self, space: Space):
        self.space = space

    def heads(self, ty: Ty, scope: tuple[Ty, ...]):
        for head in self.space.vocab[1:]:
            head_ty = self.space.head_type(head, scope)
            if head_ty is None or head_ty.base != ty.base:
                continue
            if any(len(scope) + len(a.args) > self.space.max_vars
                   for a in head_ty.args):
                continue
            yield head, head_ty

    @lru_cache(None)
    def count(self, ty: Ty, context: tuple[Ty, ...], size: int, depth: int):
        if size < 1 or depth < 1:
            return 0
        scope = context + ty.args
        total = 0
        for _, head_ty in self.heads(ty, scope):
            if not head_ty.args:
                total += size == 1
            else:
                total += self.spines(head_ty.args, scope, size - 1, depth - 1)
        return total

    @lru_cache(None)
    def spines(self, types, scope, size, depth):
        if not types:
            return int(size == 0)
        return sum(
            self.count(types[0], scope, k, depth)
            * self.spines(types[1:], scope, size - k, depth)
            for k in range(1, size - len(types) + 2))

    def sample(self, rng: random.Random, size: int, ty: Ty | None = None,
               context: tuple[Ty, ...] = (), depth: int | None = None) -> Tree:
        ty = self.space.root if ty is None else ty
        depth = self.space.depth if depth is None else depth
        total = self.count(ty, context, size, depth)
        if not total:
            raise ValueError(f"no tree of size {size}")
        r = rng.randrange(total)
        scope = context + ty.args
        for head, head_ty in self.heads(ty, scope):
            if not head_ty.args:
                k = int(size == 1)
                if r < k:
                    return Tree(head)
                r -= k
                continue
            k = self.spines(head_ty.args, scope, size - 1, depth - 1)
            if r < k:
                return Tree(head, self._spine(
                    rng, head_ty.args, scope, size - 1, depth - 1))
            r -= k
        raise AssertionError

    def _spine(self, rng, types, scope, size, depth):
        if not types:
            return ()
        weights = [self.count(types[0], scope, k, depth)
                   * self.spines(types[1:], scope, size - k, depth)
                   for k in range(1, size - len(types) + 2)]
        k = 1 + rng.choices(range(len(weights)), weights)[0]
        return (self.sample(rng, k, types[0], scope, depth), ) + self._spine(
            rng, types[1:], scope, size - k, depth)


# ------------------------------------------------------------------ inputs

def random_grid(rng: random.Random, style: dict) -> tuple[int, ...]:
    """A one-dimensional grid of objects on a background, drawn in a style
    shared by every input of a task."""
    n = rng.randint(*style["length"])
    grid = [0] * n
    x = rng.randint(0, 3)
    for _ in range(rng.randint(*style["objects"])):
        size = rng.randint(*style["size"])
        if rng.random() < style["pixel"]:
            size = 1
        if x + size > n:
            break
        colour = rng.choice(style["palette"])
        for k in range(size):
            c = colour
            if size > 2 and rng.random() < style["noise"]:
                c = rng.choice(range(1, 10))
            grid[x + k] = c
        x += size + rng.randint(style["gap"], style["gap"] + 6)
    return tuple(grid)


def random_style(rng: random.Random) -> dict:
    lo = rng.randint(8, 24)
    palette = rng.sample(range(1, 10), rng.choice([1, 1, 2, 2, 3, 5]))
    long = rng.random() < 0.15
    return {
        "length": (rng.randint(40, 80), 96) if long else
                  (lo, lo + rng.choice([0, 0, 4, 12])),
        "objects": (1, rng.choice([2, 4, 8, 12] if long else [1, 2, 3, 4, 6])),
        "size": (1, rng.choice([2, 4, 6, 10, 16])),
        "pixel": rng.choice([0, 0.2, 0.5]),
        "noise": rng.choice([0, 0, 0, 0.15]),
        "palette": palette,
        "gap": rng.choice([0, 1, 1, 2]),
    }


# ------------------------------------------------------------------- tasks

@dataclass
class Task:
    program: Tree
    train: list[tuple[tuple, tuple]]
    test: list[tuple[tuple, tuple]]
    solutions: list[Tree]


def run(f, x):
    try:
        return f(x)
    except (Undefined, IndexError, ValueError, RecursionError):
        return None


class Generator:
    """
    Parameters:
        space : The signature and its address space.
        sizes : The range of program sizes, drawn uniformly.
        demos : The range of the number of training demonstrations.
        bank_size : The largest replacement tree in a one-edit variant.
        max_solutions : The cap K on the solution set.
        inputs : ``(style, grid)``: draws a style shared by a task's inputs,
            and an input in that style; one-dimensional grids by default.
        exact : The largest program size for which the solution set is
            exact: every program of the minimal size consistent with the
            demonstrations, found by enumerating every program up to that
            size, which also replaces a locally minimal program by a
            globally minimal one.
    """

    def __init__(self, space: Space, sizes=(2, 20), demos=(3, 4),
                 bank_size=3, max_solutions=32, inputs=None, exact=0):
        self.space, self.sizes, self.demos = space, sizes, demos
        self.inputs = inputs or (random_style, random_grid)
        self.exact = exact
        self._small = None
        self.sampler = Sampler(space)
        self.bank_size, self.max_solutions = bank_size, max_solutions
        self.sizes_available = [
            s for s in range(sizes[0], sizes[1] + 1)
            if self.sampler.count(space.root, (), s, space.depth)]
        self._banks = {}

    def bank(self, ty, context, depth):
        key = ty, context, depth
        if key not in self._banks:
            self._banks[key] = [
                t for s in range(1, self.bank_size + 1)
                for t in self.space.trees(s, ty, context, depth)]
        return self._banks[key]

    def task(self, rng: random.Random, tries: int = 200) -> Task | None:
        """A task whose minimal program has a size drawn uniformly."""
        target = rng.choice(self.sizes_available)
        for _ in range(tries):
            task = self._task(rng, rng.randint(target, self.sizes[1]))
            if task is not None and task.program.size == target:
                return task
        return None

    def _task(self, rng: random.Random, size: int, tries: int = 50):
        for _ in range(tries):
            program = self.sampler.sample(rng, size)
            f = self.space.compile(program)
            make_style, make_grid = self.inputs
            style = make_style(rng)
            n_train = rng.randint(*self.demos)
            pairs = []
            for _ in range(4 * (n_train + 1)):
                x = make_grid(rng, style)
                y = run(f, x)
                if y is not None and any(x):
                    pairs.append((x, y))
                if len(pairs) == n_train + 1:
                    break
            if len(pairs) < n_train + 1:
                continue
            if all(x == y for x, y in pairs):
                continue
            if len({y for _, y in pairs}) == 1 and len({x for x, _ in pairs}) > 1:
                continue
            if not any(any(y) for _, y in pairs):
                continue
            train, test = pairs[:n_train], pairs[n_train:]
            program = self.shrink(program, train)
            solutions = None
            if program.size <= self.exact:
                solutions = self.minimal(train, program.size)
                program = solutions[0]
            if all(run(self.space.compile(program), x) == y for x, y in test)\
                    and any(x != y for x, y in test):
                return Task(program, train, test, solutions
                            or self.solutions(program, train))
        return None

    def minimal(self, train, size: int) -> list[Tree]:
        """Every program of the smallest size consistent with ``train``, up
        to ``max_solutions``, given that one of size ``size`` is."""
        if self._small is None:
            self._small = [(t, self.space.compile(t))
                           for s in range(1, self.exact + 1)
                           for t in self.space.trees(s)]
        found = []
        for tree, f in self._small:
            if tree.size > size or found and tree.size > found[0].size:
                break
            if all(run(f, x) == y for x, y in train):
                found.append(tree)
                if len(found) == self.max_solutions:
                    break
        return found

    def consistent(self, tree: Tree, train) -> bool:
        f = self.space.compile(tree)
        return all(run(f, x) == y for x, y in train)

    def shrink(self, program: Tree, train) -> Tree:
        """A locally minimal program consistent with ``train``: no one-edit
        variant of it is smaller and consistent."""
        while True:
            for variant in self.variants(program):
                if variant.size < program.size\
                        and self.consistent(variant, train):
                    program = variant
                    break
            else:
                return program

    def solutions(self, program: Tree, train) -> list[Tree]:
        """The program and its one-edit variants, no larger, consistent with
        ``train``."""
        found, seen = [program], {program}
        for variant in self.variants(program):
            if variant in seen or variant.size > program.size:
                continue
            seen.add(variant)
            f = self.space.compile(variant)
            if all(run(f, x) == y for x, y in train):
                found.append(variant)
                if len(found) == self.max_solutions:
                    break
        return found

    def variants(self, tree, ty=None, context=(), depth=None):
        """Every tree differing from ``tree`` in exactly one subtree."""
        ty = self.space.root if ty is None else ty
        depth = self.space.depth if depth is None else depth
        for other in self.bank(ty, context, depth):
            if other != tree:
                yield other
        yield from self.hoists(tree, ty, context, ty, context)
        scope = context + ty.args
        head_ty = self.space.head_type(tree.head, scope)
        for j, (arg, arg_ty) in enumerate(zip(tree.args, head_ty.args)):
            for v in self.variants(arg, arg_ty, scope, depth - 1):
                yield Tree(tree.head, tree.args[:j] + (v, ) + tree.args[j + 1:])


    def hoists(self, tree, ty, context, target_ty, target_context):
        """The proper subtrees of ``tree`` that can replace the node of type
        ``target_ty`` in ``target_context``: those whose body has the same base
        type in the same scope, so that their variables keep their levels."""
        scope = context + ty.args
        target_scope = target_context + target_ty.args
        head_ty = self.space.head_type(tree.head, scope)
        for arg, arg_ty in zip(tree.args, head_ty.args):
            if arg_ty.base == target_ty.base\
                    and scope + arg_ty.args == target_scope:
                yield arg
            yield from self.hoists(arg, arg_ty, scope, target_ty, target_context)


def to_arrays(space: Space, task: Task, max_solutions: int) -> dict:
    """The task as arrays: demos padded with -1, solutions as label vectors."""
    labels = np.zeros((max_solutions, space.n_positions), dtype=np.int16)
    for k, t in enumerate(task.solutions[:max_solutions]):
        labels[k] = space.encode(t)
    return {
        "train": task.train, "test": task.test,
        "solutions": labels, "n_solutions": min(len(task.solutions),
                                                max_solutions),
    }
