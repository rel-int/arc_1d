from dc.data import onehot, show
from dc.library import Pivot, Reverse, Slide
from dc.select import select
from dc.terms import X
from dc.wake import Solution


def apply(box, *grids):
    """The box on grids written as ``show`` writes them, one batch of equal lengths."""
    cells = onehot([[".123456789".index(c) for c in grid] for grid in grids])
    return [show(row) for row in box(cells).argmax(-1).tolist()]


def test_reverse_reverses_each_object_in_place():
    assert apply(Reverse(), "..4888..12.", "...........") == ["..8884..21.", "..........."]


def test_pivot_reflects_about_the_first_smallest_object():
    assert apply(Pivot(), "3333.9.......", "..55..9......") == [".....9.3333..", "......9..55.."]


def test_pivot_drops_what_lands_outside_the_grid():
    assert apply(Pivot(), "..9.4444") == ["4.9....."]


def test_slide_moves_each_side_until_it_touches_the_anchor():
    assert apply(Slide(), "33.44...9...11.") == ["...33.44911...."]
    assert apply(Slide(), "....8......") == ["....8......"]


def candidate(prediction, dl, loo):
    return Solution(X, dl, 0., 0., True, {}, prediction, loo)


def test_votes_pool_the_candidates_that_agree():
    a, b, c = candidate((1,), 10., 3), candidate((2,), 11., 2), candidate((2,), 12., 2)
    assert select([a, b, c], "dl")[0] is a and select([a, b, c], "loo")[0] is a
    assert select([a, b, c], "vote_loo")[0] is b  # 3 + 3 against 4
    assert select([a, b, c], "bma")[0] is a  # 2^-10 against 2^-11 + 2^-12
