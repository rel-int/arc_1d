import pytest

torch = pytest.importorskip("torch")

from ldt.bohm import Tree  # noqa: E402
from ldt.data import Task, permute  # noqa: E402
from ldt.dsl2d import SPACE  # noqa: E402
from ldt.lattice import Typing  # noqa: E402
from ldt.train import Pool, TrainConfig, verify  # noqa: E402


def test_pool_keeps_the_program_a_solution_of_what_it_shows():
    """``least`` breaks ties by colour index, so swapping two tied colours
    changes which one ``replace(least(x0), c5, x0)`` recolours: the pool must
    not show the model demonstrations its program does not solve."""
    program = Tree("replace", (Tree("least", (Tree("x0"), )), Tree("c5"),
                               Tree("x0")))
    f = SPACE.compile(program)
    x = ((0, 0, 0), (0, 1, 0), (0, 0, 2))
    task = Task("tie", [(x, f(x))], [(x, f(x))], [SPACE.encode(program)])
    pool = Pool(SPACE, Typing(SPACE), [task], TrainConfig(batch=64), "cpu")
    for i in range(64):
        labels = pool.Y[i, 0].numpy()
        assert verify(SPACE, labels, pool.train[i])
        assert pool.train[i] == permute(task.train, pool.perm[i])
    assert any(p == list(range(10)) for p in pool.perm)
