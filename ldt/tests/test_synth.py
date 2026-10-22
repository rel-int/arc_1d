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
