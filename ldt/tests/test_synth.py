import random

from ldt.dsl1d import SPACE
from ldt.synth import Generator, run


def test_tasks_are_consistent_and_minimal():
    g = Generator(SPACE, sizes=(2, 12))
    rng = random.Random(0)
    for _ in range(10):
        task = g.task(rng)
        f = SPACE.compile(task.program)
        assert all(run(f, x) == y for x, y in task.train + task.test)
        for s in task.solutions:
            assert g.consistent(s, task.train)
            assert s.size <= task.program.size
        assert all(v.size >= task.program.size
                   or not g.consistent(v, task.train)
                   for v in g.variants(task.program))


def test_exact_solution_sets_are_every_minimal_program():
    g = Generator(SPACE, sizes=(2, 6), exact=6)
    rng = random.Random(1)
    for _ in range(6):
        task = g.task(rng)
        size = task.program.size
        smaller = [t for s in range(1, size) for t in SPACE.trees(s)]
        assert not any(g.consistent(t, task.train) for t in smaller)
        same = [t for t in SPACE.trees(size) if g.consistent(t, task.train)]
        assert task.solutions == same[:g.max_solutions]
