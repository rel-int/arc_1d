import random

from ldt.abstract import TOP, Abstract, compatible, transformers_1d
from ldt.bohm import Tree, Undefined
from ldt.dsl1d import SPACE
from ldt.synth import Sampler, random_grid, random_style, run


def cuts(tree):
    """Every partial tree with one subtree replaced by Omega (``None``)."""
    yield None
    for j, arg in enumerate(tree.args):
        for cut in cuts(arg):
            yield Tree(tree.head, tree.args[:j] + (cut, ) + tree.args[j + 1:])


def test_abstract_evaluation_is_sound_and_informative():
    """The abstract output of a partial tree admits the output of every
    completion, so a sound conflict never rejects the program it came from."""
    abstract, sampler, rng = Abstract(SPACE, transformers_1d()), \
        Sampler(SPACE), random.Random(0)
    informative = 0
    for _ in range(150):
        program = sampler.sample(rng, rng.randint(2, 14))
        f, style = SPACE.compile(program), random_style(rng)
        pairs = [(x, run(f, x)) for x in
                 (random_grid(rng, style) for _ in range(3))]
        if any(y is None for _, y in pairs):
            continue
        for cut in cuts(program):
            assert not abstract.conflict(cut, pairs)
            g = abstract.compile(cut)
            for x, y in pairs:
                try:
                    value = g(x)
                except Undefined:
                    continue
                assert compatible(value, y)
                informative += value is not TOP
    assert informative > 500


def test_abstract_evaluation_prunes():
    """Recolouring with an unknown colour keeps every object in place, so it
    cannot explain an object that moved, whatever the colour turns out to be."""
    abstract = Abstract(SPACE, transformers_1d())
    recolour = Tree("map_segs", (Tree("recolor", (None, Tree("x1"))),
                                 Tree("x0")))
    assert abstract.conflict(recolour, [((0, 3, 0, 0), (0, 0, 3, 0))])
    assert not abstract.conflict(recolour, [((0, 3, 0, 0), (0, 7, 0, 0))])
