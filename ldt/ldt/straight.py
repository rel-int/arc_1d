"""
Straight-line programs over a DSL of Python functions: Böhm trees with sharing.

A program is a sequence of statements ``x_i = f(a_1, ..., a_k)``. The head
``f`` is a function of the DSL, or an earlier ``x_j`` holding one (built by a
combinator such as ``lbind`` or ``compose``); each argument is the input ``I``,
an earlier ``x_j``, a function of the DSL passed as a value, or a constant. The
last statement is the output. Naming every intermediate value is what keeps
programs that share subterms small: arc-dsl's solvers and re-arc's verifiers
are written this way.

Positions are the fields of ``statements`` rows, a head and ``arity`` argument
slots each; labels are ``ABSENT``, ``I``, the references, the functions and the
constants. A partial program is a candidate set per field, and the order is
inclusion, as for :mod:`ldt.bohm`. The structure of the domain is a star: the
program's length is shared by every statement, and given it each statement is
independent (a present statement's head fixes which of its arguments exist,
references only point back). :meth:`StraightSpace.propagate` is arc
consistency on that star, so it projects onto the structurally valid programs
exactly. The DSL's types are not used: they are loose enough in arc-dsl that a
typing projection would not be sound, and checking is left to execution.
"""

from __future__ import annotations

import inspect
import signal
import threading
from contextlib import contextmanager
from dataclasses import dataclass

import numpy as np
import torch

from ldt.bohm import ABSENT, Undefined


@dataclass(frozen=True)
class Statement:
    head: str
    args: tuple[str, ...]


class Program(tuple):
    """A tuple of statements, the last one the output."""

    @property
    def size(self) -> int:
        return len(self)

    def __str__(self):
        return "; ".join(f"x{i + 1} = {s.head}({', '.join(s.args)})"
                         for i, s in enumerate(self))


def is_reference(label: str) -> bool:
    return label[0] == "x" and label[1:].isdigit()


class TimeLimit(Exception):
    pass


@contextmanager
def time_limit(seconds: float | None):
    """Raise :class:`TimeLimit` in the block after ``seconds``, where a timer
    signal can be delivered (the main thread); no limit elsewhere."""
    if not seconds or threading.current_thread() is not threading.main_thread():
        yield
        return

    def handler(signum, frame):
        raise TimeLimit(f"over {seconds} s")
    previous = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


class StraightSpace:
    """
    Parameters:
        functions : The DSL's functions by name.
        constants : The DSL's constants by name.
        statements : The largest number of statements.
        arity : The largest number of arguments.
        check_output : Whether a value is a valid output, e.g. a grid.
        seconds : The time a program may take on one input, beyond which it
            is undefined: a short program can build a 27,000 x 27,000 canvas.
    """

    def __init__(self, functions: dict, constants: dict, statements: int = 32,
                 arity: int = 4, check_output=None, seconds: float = 1.0):
        self.functions, self.constants = functions, constants
        self.seconds = seconds
        self.statements, self.arity = statements, arity
        self.check_output = check_output or (lambda value: True)
        self.vocab = [ABSENT, "I"] + [
            f"x{i + 1}" for i in range(statements)] + sorted(functions)\
            + sorted(constants)
        self.index = {v: i for i, v in enumerate(self.vocab)}
        self.fields = arity + 1
        self.n_positions = statements * self.fields
        V = len(self.vocab)
        self.function_arity = {
            name: len(inspect.signature(f).parameters)
            for name, f in functions.items()}
        assert max(self.function_arity.values()) <= arity
        # arities a head allows, as a mask over 0..arity (0: the head is absent)
        self.head_arities = np.zeros((V, arity + 1), dtype=bool)
        self.head_arities[0, 0] = True
        for name, k in self.function_arity.items():
            self.head_arities[self.index[name], k] = True
        for i in range(statements):
            self.head_arities[self.index[f"x{i + 1}"], 1:4] = True
        self._top = self._build_top()

    # ------------------------------------------------------------------ space

    def position(self, i: int, j: int) -> int:
        return i * self.fields + j

    def _build_top(self) -> np.ndarray:
        V, N = len(self.vocab), self.statements
        top = np.zeros((N, self.fields, V), dtype=bool)
        functions = [self.index[f] for f in self.functions]
        constants = [self.index[c] for c in self.constants]
        for i in range(N):
            earlier = [self.index[f"x{k + 1}"] for k in range(i)]
            top[i, 0, [0] + functions + earlier] = True
            top[i, 1:, [0, 1] + functions + constants + earlier] = True
        top[0, 0, 0] = False  # a program has a statement
        return top.reshape(N * self.fields, V)

    def top(self) -> np.ndarray:
        return self.propagate(self._top.copy())

    def propagate(self, cand: np.ndarray) -> np.ndarray:
        """The exact projection onto structurally valid programs: empty
        everywhere iff none is left."""
        N, F = self.statements, self.fields
        x = cand.reshape(N, F, -1) & self._top.reshape(N, F, -1)
        present_arg = x[:, 1:, 1:].any(-1)  # (N, A): a non-absent label
        absent_arg = x[:, 1:, 0]
        # pattern k: arguments 1..k present, k+1..A absent
        A = self.arity
        pattern = np.ones((N, A + 1), dtype=bool)
        for k in range(A + 1):
            pattern[:, k] = present_arg[:, :k].all(-1) & absent_arg[:, k:].all(-1)
        heads = x[:, 0]  # (N, V)
        allowed = (heads.astype(np.int32) @ self.head_arities) > 0
        feasible = allowed & pattern  # (N, A + 1)
        can_absent = feasible[:, 0]
        can_present = feasible[:, 1:].any(-1)
        lengths = np.array([
            can_present[:L].all() and can_absent[L:].all()
            for L in range(N + 1)])
        lengths[0] = False
        if not lengths.any():
            return np.zeros_like(cand)
        present_ok = np.array([lengths[i + 1:].any() for i in range(N)])
        absent_ok = np.array([lengths[:i + 1].any() for i in range(N)])
        feasible[:, 0] &= absent_ok
        feasible[:, 1:] &= present_ok[:, None]
        out = x.copy()
        out[:, 0] &= (self.head_arities[None] & feasible[:, None]).any(-1)
        for j in range(1, A + 1):
            out[:, j, 1:] &= feasible[:, j:].any(-1)[:, None]
            out[:, j, 0] &= feasible[:, :j].any(-1)
        return out.reshape(N * F, -1)

    def typing(self) -> StraightTyping:
        return StraightTyping(self)

    # --------------------------------------------------------------- encoding

    def encode(self, program: Program) -> np.ndarray:
        labels = np.zeros((self.statements, self.fields), dtype=np.int64)
        if len(program) > self.statements:
            raise ValueError(f"{len(program)} statements do not fit")
        for i, s in enumerate(program):
            labels[i, 0] = self.index[s.head]
            for j, a in enumerate(s.args):
                labels[i, j + 1] = self.index[a]
        return labels.reshape(-1)

    def decode(self, labels: np.ndarray) -> Program | None:
        labels = np.asarray(labels).reshape(self.statements, self.fields)
        out = []
        for row in labels:
            if row[0] == 0:
                break
            args = tuple(self.vocab[a] for a in row[1:] if a != 0)
            out.append(Statement(self.vocab[row[0]], args))
        return Program(out) if out else None

    def singleton(self, labels: np.ndarray) -> np.ndarray:
        cand = np.zeros((self.n_positions, len(self.vocab)), dtype=bool)
        cand[np.arange(self.n_positions), labels] = True
        return cand

    def check(self, program: Program) -> bool:
        """Whether the program is structurally valid."""
        if not program or len(program) > self.statements:
            return False
        for i, s in enumerate(program):
            scope = {f"x{k + 1}" for k in range(i)}
            if s.head in self.functions:
                if len(s.args) != self.function_arity[s.head]:
                    return False
            elif s.head not in scope or not 1 <= len(s.args) <= 3:
                return False
            for a in s.args:
                if not (a == "I" or a in scope or a in self.functions
                        or a in self.constants):
                    return False
        return True

    # -------------------------------------------------------------- semantics

    def compile(self, program: Program):
        """The program as a function; any exception of the DSL, or an output
        that is not valid, is :class:`Undefined`."""
        functions, constants = self.functions, self.constants
        steps = []
        for s in program:
            steps.append((s.head, s.args))

        def value(env, name):
            if name in env:
                return env[name]
            if name in functions:
                return functions[name]
            return constants[name]

        def run(x):
            env = {"I": x}
            try:
                with time_limit(self.seconds):
                    for i, (head, args) in enumerate(steps):
                        f = env[head] if head in env else functions[head]
                        env[f"x{i + 1}"] = f(*[value(env, a) for a in args])
                out = env[f"x{len(steps)}"]
            except Exception as e:  # TimeLimit and MemoryError included
                raise Undefined(str(e)) from e
            if not self.check_output(out):
                raise Undefined("not a valid output")
            return out
        return run

    def dead_code(self, program: Program) -> Program:
        """The program without the statements its output does not use."""
        used, n = {len(program) - 1}, len(program)
        for i in reversed(range(n)):
            if i in used:
                s = program[i]
                for name in (s.head, ) + s.args:
                    if is_reference(name):
                        used.add(int(name[1:]) - 1)
        keep = sorted(used)
        rename = {f"x{k + 1}": f"x{r + 1}" for r, k in enumerate(keep)}
        return Program(Statement(rename.get(program[k].head, program[k].head),
                                 tuple(rename.get(a, a) for a in program[k].args))
                       for k in keep)


    def canonical(self, program: Program) -> Program:
        """One representative of the programs equal up to dead code, repeated
        statements and the order of independent statements: the used
        statements, each written once, in the topological order that puts
        first the smallest statement written with the representative's own
        names, the output last."""
        program = self.dead_code(program)
        n = len(program)
        deps = [{int(a[1:]) - 1 for a in (s.head, ) + s.args
                 if is_reference(a)} for s in program]
        placed, rename, out = set(), {}, []
        while len(placed) < n:
            ready = [i for i in range(n) if i not in placed
                     and deps[i] <= placed and (i == n - 1 or len(out) < n - 1)]
            if len(ready) > 1:
                ready = [i for i in ready if i != n - 1]

            def written(i):
                s = program[i]
                return (rename.get(s.head, s.head),
                        tuple(rename.get(a, a) for a in s.args))
            head, args = min(map(written, ready))
            out.append(Statement(head, args))
            for i in ready:
                if written(i) == (head, args):
                    placed.add(i)
                    rename[f"x{i + 1}"] = f"x{len(out)}"
        return Program(out)


class StraightTyping(torch.nn.Module):
    """:meth:`StraightSpace.propagate` batched on the device, with the
    interface of :class:`ldt.lattice.Typing`: ``top``, ``parent`` (a head's
    parent is the previous statement's head, an argument's is its statement's
    head) and ``forward``."""

    def __init__(self, space: StraightSpace):
        super().__init__()
        self.space = space
        N, F = space.statements, space.fields
        self.register_buffer("mask", torch.from_numpy(space._top))
        self.register_buffer("head_arities",
                             torch.from_numpy(space.head_arities).float())
        parent = []
        for i in range(N):
            parent.append(-1 if i == 0 else (i - 1) * F)
            parent.extend([i * F] * (F - 1))
        self.register_buffer("parent", torch.tensor(parent))
        self.register_buffer("top", torch.from_numpy(space.top()))

    @torch.no_grad()
    def forward(self, cand: torch.Tensor) -> torch.Tensor:
        sp = self.space
        B, N, F, A = cand.shape[0], sp.statements, sp.fields, sp.arity
        x = (cand & self.mask).reshape(B, N, F, -1)
        present_arg = x[:, :, 1:, 1:].any(-1)
        absent_arg = x[:, :, 1:, 0]
        pattern = torch.stack([
            present_arg[:, :, :k].all(-1) & absent_arg[:, :, k:].all(-1)
            for k in range(A + 1)], -1)  # (B, N, A + 1)
        allowed = (x[:, :, 0].float() @ self.head_arities) > 0
        feasible = allowed & pattern
        can_absent = feasible[..., 0]
        can_present = feasible[..., 1:].any(-1)
        # lengths[L]: statements < L present, >= L absent
        prefix = torch.cat([torch.ones(B, 1, dtype=torch.bool,
                                       device=cand.device),
                            can_present.cumprod(-1).bool()], -1)
        suffix = torch.cat([can_absent.flip(-1).cumprod(-1).bool().flip(-1),
                            torch.ones(B, 1, dtype=torch.bool,
                                       device=cand.device)], -1)
        lengths = prefix & suffix
        lengths[:, 0] = False
        # present_ok[i]: some feasible L > i; absent_ok[i]: some L <= i
        present_ok = lengths.flip(-1).cumsum(-1).flip(-1)[:, 1:] > 0
        absent_ok = lengths.cumsum(-1)[:, :N] > 0
        feasible = feasible.clone()
        feasible[..., 0] &= absent_ok
        feasible[..., 1:] &= present_ok[..., None]
        out = x.clone()
        out[:, :, 0] &= ((self.head_arities[None, None] > 0)
                         & feasible[:, :, None]).any(-1)
        for j in range(1, A + 1):
            out[:, :, j, 1:] &= feasible[..., j:].any(-1)[..., None]
            out[:, :, j, 0] &= feasible[..., :j].any(-1)
        out = out.reshape(B, N * F, -1)
        out[~lengths.any(-1)] = False
        return out
