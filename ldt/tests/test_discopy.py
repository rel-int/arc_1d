import random

import pytest

pytest.importorskip("discopy")

from ldt.bohm import Undefined  # noqa: E402
from ldt.discopy_bridge import Bridge  # noqa: E402
from ldt.dsl1d import PYTHON_TYPES, SPACE  # noqa: E402
from ldt.synth import Sampler, random_grid, random_style, run  # noqa: E402


def test_bohm_trees_and_semantics_agree_with_discopy():
    bridge, sampler, rng = Bridge(SPACE, PYTHON_TYPES), Sampler(SPACE), \
        random.Random(0)
    for _ in range(100):
        tree = sampler.sample(rng, rng.randint(2, 16))
        assert bridge.from_bohm(bridge.reduce(bridge.to_term(tree))) == tree
        f, g = SPACE.compile(tree), bridge.evaluate(tree)
        x = random_grid(rng, random_style(rng))
        try:
            expected = g(x)
        except (Undefined, IndexError, ValueError):
            expected = None
        # call by value: the bridge may raise where compile is lazy
        assert run(f, x) == expected or expected is None
