"""
arc-dsl as a :class:`ldt.straight.StraightSpace`, and tasks from re-arc.

re-arc (Hodel, 2024, https://github.com/michaelhodel/re-arc) gives, for each of
the 400 ARC-AGI-1 training tasks, a generator, a verifier and 1,000 generated
examples, each kept only if the verifier reproduces it. The verifiers are
straight-line programs over arc-dsl's 160 functions and 28 constants, which
:func:`programs` reads from ``verifiers.py`` without running it. ``dsl.py`` is
the semantics. Both are found at ``REARC`` (default ``/data/re-arc``).

:class:`Generator` draws few-shot tasks two ways. A verifier task samples
demonstrations and a test pair of one re-arc task, its verifier the solution.
A mutant task edits one field of a verifier — a head for another function of
its arity, a constant for another, a function value for another of its arity,
a reference for another in scope — runs it on that task's inputs, and keeps it
when it is defined, moves something and does not send every input to one
output: a program near the ARC distribution that no task of it uses.
"""

from __future__ import annotations

import ast
import importlib.util
import inspect
import json
import os
import random
import zipfile
from functools import lru_cache

from ldt.bohm import Undefined
from ldt.data import Task
from ldt.straight import Program, Statement, StraightSpace, is_reference

REARC = os.environ.get("REARC", "/data/re-arc")


def is_grid(value) -> bool:
    if not isinstance(value, tuple) or not 1 <= len(value) <= 30:
        return False
    width = len(value[0]) if isinstance(value[0], tuple) else 0
    return 1 <= width <= 30 and all(
        isinstance(row, tuple) and len(row) == width
        and all(type(c) is int and 0 <= c <= 9 for c in row)  # not bool
        for row in value)


@lru_cache(None)
def dsl(root: str = REARC):
    spec = importlib.util.spec_from_file_location(
        "rearc_dsl", os.path.join(root, "dsl.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    functions = {name: f for name, f in vars(module).items()
                 if inspect.isfunction(f) and f.__module__ == "rearc_dsl"}
    constants = {name: v for name, v in vars(module).items()
                 if name.isupper() and isinstance(v, (bool, int, tuple))}
    return functions, constants


@lru_cache(None)
def space(root: str = REARC, statements: int = 32) -> StraightSpace:
    functions, constants = dsl(root)
    return StraightSpace(functions, constants, statements, 4, is_grid)


def parse(function: ast.FunctionDef) -> Program:
    """A verifier's body as a program: ``x = f(a, ...)`` with atomic
    arguments, then ``return`` of the last name assigned."""
    names, out = {}, []
    for st in function.body:
        if isinstance(st, ast.Return):
            break
        call = st.value
        rename = lambda n: names.get(n, n)  # noqa: E731
        out.append(Statement(rename(call.func.id),
                             tuple(rename(a.id) for a in call.args)))
        names[st.targets[0].id] = f"x{len(out)}"
    return Program(out)


@lru_cache(None)
def programs(root: str = REARC, statements: int = 32) -> dict[str, Program]:
    """Every verifier that fits ``statements`` once its dead code is gone."""
    sp = space(root, statements)
    with open(os.path.join(root, "verifiers.py")) as f:
        tree = ast.parse(f.read())
    out = {}
    for function in tree.body:
        if isinstance(function, ast.FunctionDef):
            program = sp.canonical(parse(function))
            if len(program) <= statements and sp.check(program):
                out[function.name[len("verify_"):]] = program
    return out


class Examples:
    """re-arc's generated examples, read from its zip on demand."""

    def __init__(self, root: str = REARC):
        self.zip = zipfile.ZipFile(os.path.join(root, "re_arc.zip"))

    @lru_cache(None)
    def __call__(self, task: str) -> list:
        data = json.loads(self.zip.read(f"re_arc/tasks/{task}.json"))
        grid = lambda g: tuple(tuple(r) for r in g)  # noqa: E731
        return [(grid(e["input"]), grid(e["output"])) for e in data
                if is_grid(grid(e["input"])) and is_grid(grid(e["output"]))]


class Generator:
    """
    Parameters:
        root : Where re-arc is.
        statements : The largest number of statements.
        mutants : The share of mutant tasks.
        demos : The range of the number of demonstrations.
        exclude : Task ids never drawn.
    """

    def __init__(self, root: str = REARC, statements: int = 32,
                 mutants: float = 0.5, demos=(3, 4), exclude=()):
        self.space = space(root, statements)
        self.programs = {k: v for k, v in programs(root, statements).items()
                         if k not in set(exclude)}
        self.ids = sorted(self.programs)
        self.examples = Examples(root)
        self.mutants, self.demos = mutants, demos
        sp = self.space
        self.by_arity = {}
        for name, k in sp.function_arity.items():
            self.by_arity.setdefault(k, []).append(name)
        self.constant_names = sorted(sp.constants)

    def task(self, rng: random.Random, tries: int = 50) -> Task | None:
        for _ in range(tries):
            name = rng.choice(self.ids)
            examples = self.examples(name)
            n = rng.randint(*self.demos)
            if len(examples) < n + 1:
                continue
            pairs = rng.sample(examples, n + 1)
            program = self.programs[name]
            family = f"rearc:{name}"
            if rng.random() < self.mutants:
                program = self.mutate(rng, program)
                f = self.space.compile(program)
                try:
                    outputs = [f(x) for x, _ in pairs]
                except Undefined:
                    continue
                if all(x == y for (x, _), y in zip(pairs, outputs))\
                        or len(set(outputs)) == 1:
                    continue
                pairs = [(x, y) for (x, _), y in zip(pairs, outputs)]
                program = self.space.canonical(program)
                family = f"mutant:{name}"
            return Task(family, pairs[:n], pairs[n:],
                        [self.space.encode(program)], family=family)
        return None

    def mutate(self, rng: random.Random, program: Program) -> Program:
        """One field of one statement replaced by another of its kind."""
        i = rng.randrange(len(program))
        s = program[i]
        fields = [0] * (s.head in self.space.functions) + list(
            range(1, len(s.args) + 1))
        j = rng.choice(fields) if fields else 0
        old = s.head if j == 0 else s.args[j - 1]
        new = old
        sp = self.space
        if j == 0 or old in sp.functions:
            arity = sp.function_arity[old]
            new = rng.choice(self.by_arity[arity])
        elif old in sp.constants:
            new = rng.choice(self.constant_names)
        elif old == "I" or is_reference(old):
            new = rng.choice(["I"] + [f"x{k + 1}" for k in range(i)])
        if j == 0:
            s = Statement(new, s.args)
        else:
            s = Statement(s.head, s.args[:j - 1] + (new, ) + s.args[j:])
        return Program(program[:i] + (s, ) + program[i + 1:])
