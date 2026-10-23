import itertools
import os

import numpy as np
import pytest

from ldt.bohm import Undefined
from ldt.straight import Program, Statement, StraightSpace


def tiny():
    functions = {"neg": lambda a: -a, "add": lambda a, b: a + b,
                 "lbind": lambda f, a: (lambda b: f(a, b))}
    return StraightSpace(functions, {"ONE": 1}, statements=2, arity=2)


def valid(space):
    """Every structurally valid program of the space, by brute force."""
    names = space.vocab[1:]

    # statements one at a time: every head and argument tuple that checks
    def statements(i):
        for head in names:
            for k in range(1, space.arity + 1):
                for args in itertools.product(names, repeat=k):
                    yield Statement(head, args)
    programs = [()]
    for i in range(space.statements):
        programs += [p + (s, ) for p in programs if len(p) == i
                     for s in statements(i)]
    return [Program(p) for p in programs if p and space.check(Program(p))]


def test_propagate_is_exact():
    space = tiny()
    programs = valid(space)
    labels = np.stack([space.encode(p) for p in programs])
    rng = np.random.default_rng(0)
    top = space.top()
    for _ in range(40):
        cand = top & (rng.random(top.shape) > rng.choice([0.2, 0.5, 0.8]))
        inside = [np.take_along_axis(cand, row[:, None], 1).all()
                  for row in labels]
        expected = np.zeros_like(cand)
        for row in labels[inside]:
            expected[np.arange(len(row)), row] = True
        assert (space.propagate(cand) == expected).all()


def test_typing_matches_propagate():
    torch = pytest.importorskip("torch")
    space = tiny()
    rng = np.random.default_rng(1)
    top = space.top()
    xs = np.stack([top & (rng.random(top.shape) > p)
                   for p in [0.2, 0.5, 0.8] * 10])
    out = space.typing()(torch.from_numpy(xs)).numpy()
    assert (out == np.stack([space.propagate(x) for x in xs])).all()


def test_semantics_sharing_and_dead_code():
    space = tiny()
    program = Program([Statement("lbind", ("add", "ONE")),
                       Statement("x1", ("I", ))])
    assert space.check(program) and space.compile(program)(41) == 42
    assert space.decode(space.encode(program)) == program
    with pytest.raises(Undefined):
        space.compile(Program([Statement("neg", ("add", ))]))(1)
    dead = Program([Statement("neg", ("I", )), Statement("add", ("I", "I"))])
    assert space.dead_code(dead) == Program([Statement("add", ("I", "I"))])


REARC = os.environ.get("REARC", "/tmp/claude-0/survey/re-arc")


@pytest.mark.skipif(not os.path.exists(REARC), reason="re-arc not found")
def test_rearc_verifiers_are_programs_of_the_space():
    from ldt import rearc
    space = rearc.space(REARC)
    programs = rearc.programs(REARC)
    examples = rearc.Examples(REARC)
    assert len(programs) > 250
    for name in sorted(programs)[::15]:
        program = programs[name]
        labels = space.encode(program)
        assert space.decode(labels) == program
        cand = space.singleton(labels)
        assert (space.propagate(cand) == cand).all()
        x, y = examples(name)[0]
        assert space.compile(program)(x) == y
