import random

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from ldt.dsl1d import SPACE  # noqa: E402
from ldt.lattice import Typing, alpha, consistent, is_total, pin  # noqa: E402
from ldt.synth import Generator  # noqa: E402


def test_typing_matches_numpy():
    typing = Typing(SPACE)
    rng = np.random.default_rng(0)
    top = SPACE.propagate(SPACE.top())
    xs = []
    for p in [0.02, 0.1, 0.3] * 8:
        kill = rng.random(top.shape) < p
        kill[:, 0] = False
        xs.append(top & ~kill)
    out = typing(torch.from_numpy(np.stack(xs))).numpy()
    ref = np.stack([SPACE.propagate(x) for x in xs])
    assert (out == ref).all() and ref[:, 0].any(-1).sum() > 10


def test_alpha_and_pinning_reach_a_solution():
    typing = Typing(SPACE)
    g = Generator(SPACE)
    tasks = [g.task(random.Random(seed)) for seed in range(4)]
    Y = torch.zeros(4, 4, SPACE.n_positions, dtype=torch.long)
    valid = torch.zeros(4, 4, dtype=torch.bool)
    for i, t in enumerate(tasks):
        for k, s in enumerate(t.solutions[:4]):
            Y[i, k] = torch.from_numpy(SPACE.encode(s))
            valid[i, k] = True
    x = typing.top[None].expand(4, -1, -1).clone()
    target, none = alpha(x, Y, valid)
    assert not none.any() and (target <= x).all()
    gen = torch.Generator().manual_seed(0)
    for _ in range(100):
        target, _ = alpha(x, Y, valid)
        logits = torch.where(target, 0.0, float("-inf"))
        x = typing(pin(x, logits, typing.parent, 1.0, gen))
    assert is_total(x).all() and consistent(x, Y, valid).any(1).all()
