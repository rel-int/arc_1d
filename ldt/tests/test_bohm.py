import random
from collections import Counter

import numpy as np
import pytest

from ldt.bohm import Tree, Ty
from ldt.dsl1d import SPACE
from ldt.synth import Sampler

x0, x1, x2 = Tree("x0"), Tree("x1"), Tree("x2")


def T(head, *args):
    return Tree(head, args)


MIRROR = T("map_segs", T("ite", T("size_eq", Tree("n1"), x1), x1, T(
    "reflect", T("pick", T("size_eq", Tree("n1"), x2), x0), x1)), x0)


def test_parse():
    assert str(Ty.parse("(O -> B) -> G -> O")) == "(O -> B) -> G -> O"
    assert Ty.parse("N -> O -> O").args == (Ty((), "N"), Ty((), "O"))


def test_encode_decode():
    labels = SPACE.encode(MIRROR)
    assert SPACE.decode(labels) == MIRROR
    assert SPACE.check(MIRROR)
    assert SPACE.check(T("map_segs", x1, x0))  # the identity on objects
    assert not SPACE.check(T("map_segs", T("shift", Tree("n1"), x2), x0))


def test_semantics():
    f = SPACE.compile(MIRROR)
    assert f((0, 0, 2, 2, 0, 9, 0, 0, 0, 0)) == (0, 0, 0, 0, 0, 9, 0, 2, 2, 0)


def test_propagate_fixes_a_tree():
    cand = SPACE.singleton(SPACE.encode(MIRROR))
    assert (SPACE.propagate(cand) == cand).all()


def test_propagate_is_exact():
    """The projection keeps exactly the labels used by some typed tree: it
    keeps every label of every enumerated tree, and at the root and its
    children every label it keeps is used by one of size at most 7."""
    top = SPACE.propagate(SPACE.top())
    used = np.zeros_like(top)
    for s in range(1, 8):
        for t in SPACE.trees(s):
            used[np.arange(SPACE.n_positions), SPACE.encode(t)] = True
    assert (used <= top).all()
    assert (used[:1 + SPACE.arity] == top[:1 + SPACE.arity]).all()


def test_propagate_kills_untypable():
    cand = SPACE.propagate(SPACE.top())
    cand[0] = False
    cand[0, SPACE.index["map_segs"]] = True
    cand[1] = False
    cand[1, SPACE.index["max_size"]] = True  # N where O -> O is expected
    assert not SPACE.propagate(cand).any()


@pytest.mark.parametrize("size", [3, 5, 7])
def test_sampler_counts_match_enumeration(size):
    sampler = Sampler(SPACE)
    trees = list(SPACE.trees(size))
    assert len(trees) == sampler.count(SPACE.root, (), size, SPACE.depth)
    assert all(SPACE.check(t) and t.size == size for t in trees)
    rng = random.Random(size)
    assert sampler.sample(rng, size) in set(trees)


def test_sampler_is_uniform():
    sampler, trees = Sampler(SPACE), set(SPACE.trees(5))
    rng = random.Random(0)
    draws = Counter(sampler.sample(rng, 5) for _ in range(50 * len(trees)))
    assert set(draws) == trees
    assert max(draws.values()) < 3 * min(draws.values())
