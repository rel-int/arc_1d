"""
The unlearned control: enumerate the programs in order of size, verify each
on the demonstrations, rank the answers like :mod:`ldt.solve` does.

This is the same Scott domain searched with no deduction but types: every
eta-long normal form of size one, then two, and so on, each run on the
demonstrations until ``budget`` programs have been tried.
"""

from __future__ import annotations

import time

from ldt.bohm import Space
from ldt.data import Task
from ldt.solve import Result, rank
from ldt.synth import run


def search(space: Space, task: Task, budget: int, enough: int = 4,
           max_size: int = 40) -> Result:
    result = Result(task.name)
    sizes, tried = {}, 0
    train = task.train
    for size in range(1, max_size + 1):
        for tree in space.trees(size):
            tried += 1
            f = space.compile(tree)
            if all(run(f, x) == y for x, y in train):
                result.programs[tree] = tuple(run(f, x) for x, _ in task.test)
                sizes[tree] = size
                if result.first_call is None:
                    result.first_call = tried
            if tried >= budget or len(result.programs) >= enough:
                break
        if tried >= budget or len(result.programs) >= enough:
            break
    result.calls = tried
    result.attempts = rank(result, sizes)
    return result


def search_all(space: Space, tasks: list[Task], budget: int, **kwargs):
    t0 = time.time()
    results = [search(space, t, budget, **kwargs) for t in tasks]
    return results, time.time() - t0
