import json
import os
import re

import pytest

from ldt.bohm import Tree, Undefined
from ldt.dsl2d import SPACE, bg, blobs, objs

ARC = os.environ.get("ARC_AGI_ROOT", "/home/user/ARC-AGI")


def P(text: str) -> Tree:
    """A tree from its printed form, e.g. ``map_objs(x1, x0)``."""
    tokens = re.findall(r"\w+|[(),]", text)

    def go(i):
        head, args, i = tokens[i], [], i + 1
        if i < len(tokens) and tokens[i] == "(":
            while tokens[i] != ")":
                arg, i = go(i + 1)
                args.append(arg)
            i += 1
        return Tree(head, tuple(args)), i
    tree, i = go(0)
    assert i == len(tokens)
    return tree


def fn(name):
    return SPACE.prims[name].fn


G = ((1, 2),
     (3, 4))
H = ((0, 0, 0, 0, 0),
     (0, 3, 3, 0, 0),
     (0, 3, 0, 0, 5),
     (0, 0, 0, 0, 5))
O3 = (1, 1, ((3, 3), (3, -1)))
O5 = (2, 4, ((5, ), (5, )))
W = ((0, 0, 0, 0, 0),
     (3, 0, 0, 0, 5),
     (0, 0, 0, 0, 0))


def test_background_and_objects():
    assert bg(((1, 2), (2, 1))) == 1
    assert bg(((1, 1), (1, 0))) == 0
    assert objs(H) == (O3, O5) and blobs(H) == (O3, O5)
    two = ((1, 2, 0, 0),
           (2, 0, 0, 0),
           (0, 0, 0, 0))
    assert objs(two) == ((0, 0, ((1, ), )), (0, 0, ((-1, 2), (2, -1))))
    assert blobs(two) == ((0, 0, ((1, 2), (2, -1))), )


def test_rotations_and_flips():
    assert fn("rot90")(G) == ((3, 1), (4, 2))
    assert fn("rot180")(G) == ((4, 3), (2, 1))
    assert fn("rot270")(G) == ((2, 4), (1, 3))
    assert fn("flip_h")(G) == ((2, 1), (4, 3))
    assert fn("flip_v")(G) == ((3, 4), (1, 2))
    assert fn("transpose")(G) == ((1, 3), (2, 4))


def test_scale_tile_concat():
    assert fn("upscale")(2, ((1, 2), )) == ((1, 1, 2, 2), (1, 1, 2, 2))
    assert fn("downscale")(2, ((1, 2, 3), (4, 5, 6), (7, 8, 9))) == (
        (1, 3), (7, 9))
    assert fn("tile")(2, 3, ((1, 2), )) == ((1, 2, 1, 2, 1, 2), ) * 2
    assert fn("hconcat")(G, G) == ((1, 2, 1, 2), (3, 4, 3, 4))
    assert fn("vconcat")(G, ((5, 6), )) == ((1, 2), (3, 4), (5, 6))
    for name, args in [("upscale", (0, G)), ("upscale", (16, G)),
                       ("downscale", (0, G)), ("tile", (1, 0, G)),
                       ("hconcat", (G, ((1, ), ))),
                       ("vconcat", (G, ((1, ), )))]:
        with pytest.raises(Undefined):
            fn(name)(*args)


def test_overlay_replace():
    assert fn("overlay")(((1, 1), (1, 1)), ((0, 2), (0, 0))) == (
        (1, 2), (1, 1))
    assert fn("replace")(1, 5, G) == ((5, 2), (3, 4))
    with pytest.raises(Undefined):
        fn("overlay")(G, ((1, 2), ))


def test_objects_to_grid():
    down = fn("map_objs")(lambda o: fn("move")("down", 1, o), H)
    assert down == ((0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0),
                    (0, 3, 3, 0, 0),
                    (0, 3, 0, 0, 5))
    assert fn("map_blobs")(lambda o: o, H) == H
    assert fn("keep_objs")(lambda o: o[2][0][0] == 5, H) == (
        (0, ) * 5, (0, ) * 5, (0, 0, 0, 0, 5), (0, 0, 0, 0, 5))
    assert fn("paint")((0, 0, ((7, -1), )), H) == ((7, 0, 0, 0, 0), ) + H[1:]
    assert fn("crop")(O3) == ((3, 3), (3, 0))
    assert fn("trim")(H) == ((3, 3, 0, 0), (3, 0, 0, 5), (0, 0, 0, 5))
    with pytest.raises(Undefined):
        fn("trim")(((4, 4), ))


def test_fill_enclosed_and_connect():
    ring = ((0, 0, 0, 0, 0),
            (0, 1, 1, 1, 0),
            (0, 1, 0, 1, 0),
            (0, 1, 1, 1, 0),
            (0, 0, 0, 0, 0))
    filled = fn("fill_enclosed")(4, ring)
    assert filled == ring[:2] + ((0, 1, 4, 1, 0), ) + ring[3:]
    lines = ((2, 0, 0, 2, 0),
             (0, 0, 0, 0, 0),
             (3, 0, 0, 0, 0),
             (0, 0, 0, 0, 0),
             (3, 0, 1, 0, 0))
    assert fn("connect")(lines) == ((2, 2, 2, 2, 0),
                                    (0, 0, 0, 0, 0),
                                    (3, 0, 0, 0, 0),
                                    (3, 0, 0, 0, 0),
                                    (3, 0, 1, 0, 0))
    cross = ((0, 1, 0), (2, 0, 2), (0, 1, 0))
    assert fn("connect")(cross)[1] == (2, 1, 2)


def test_halves_and_cells():
    s = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    assert fn("left_half")(s) == ((1, ), (4, ), (7, ))
    assert fn("right_half")(s) == ((3, ), (6, ), (9, ))
    assert fn("top_half")(s) == ((1, 2, 3), )
    assert fn("bottom_half")(s) == ((7, 8, 9), )
    with pytest.raises(Undefined):
        fn("left_half")(((1, ), ))
    a, b = ((1, 0), (1, 0)), ((1, 1), (0, 0))
    assert fn("cell_and")(7, a, b) == ((7, 0), (0, 0))
    assert fn("cell_or")(7, a, b) == ((7, 7), (7, 0))
    assert fn("cell_xor")(7, a, b) == ((0, 7), (7, 0))
    assert fn("cell_nor")(7, a, b) == ((0, 0), (0, 7))
    with pytest.raises(Undefined):
        fn("cell_and")(7, a, ((1, ), ))


def test_symmetrize():
    masked = ((1, 2, 2, 1),
              (3, 4, 9, 3),
              (3, 4, 4, 3),
              (1, 2, 2, 1))
    assert fn("symmetrize")(masked)[1] == (3, 4, 4, 3)
    assert fn("symmetrize")(G) == G


def test_object_to_object():
    assert fn("move")("right", 2, O3) == (1, 3, O3[2])
    o = objs(W)[0]
    assert fn("slide")("right", W, o) == (1, 3, ((3, ), ))
    assert fn("slide")("up", W, o) == (0, 0, ((3, ), ))
    assert fn("slide")("left", W, o) == o
    assert fn("extend")("right", W, o) == (1, 0, ((3, 3, 3, 3), ))
    assert fn("extend")("down", H, O3) == (1, 1, ((3, 3), ) * 3)
    assert fn("recolor")(7, O3) == (1, 1, ((7, 7), (7, -1)))
    assert fn("flip_obj_h")(O3) == (1, 1, ((3, 3), (-1, 3)))
    assert fn("flip_obj_v")(O3) == (1, 1, ((3, -1), (3, 3)))
    assert fn("border")(7, (0, 0, ((3, ) * 3, ) * 3)) == (
        0, 0, ((7, 7, 7), (7, 3, 7), (7, 7, 7)))
    assert fn("fill_box")(7, O3) == (1, 1, ((3, 3), (3, 7)))
    assert fn("ite")(lambda: True, lambda: O3, lambda: 1 / 0) == O3


def test_selectors_and_features():
    assert fn("pick")(lambda o: fn("size")(o) == 2, H) == O5
    assert fn("largest")(H) == O3 and fn("smallest")(H) == O5
    for name, args in [("pick", (lambda o: False, H)),
                       ("largest", (((0, ), ), )),
                       ("smallest", (((0, ), ), ))]:
        with pytest.raises(Undefined):
            fn(name)(*args)
    assert fn("size_eq")(3, O3) and not fn("size_gt")(3, O3)
    assert fn("colour_eq")(3, O3) and not fn("colour_eq")(5, O3)
    assert fn("touches_border")(H, O5) and not fn("touches_border")(H, O3)
    assert fn("is_largest")(H, O3) and not fn("is_largest")(H, O5)
    assert fn("not_")(True) is False
    assert (fn("size")(O3), fn("count")(H)) == (3, 2)
    assert (fn("height")(H), fn("width")(H)) == (4, 5)
    assert fn("colour")((0, 0, ((1, 2, 2), ))) == 2
    assert (fn("most")(H), fn("least")(H)) == (0, 5)
    assert (fn("n3"), fn("c7"), fn("up")) == (3, 7, "up")


def test_check():
    assert SPACE.check(P("x0"))
    assert SPACE.check(P("map_objs(x1, x0)"))
    assert SPACE.check(P("keep_objs(not_(touches_border(x0, x1)), x0)"))
    assert SPACE.check(P("map_objs(ite(is_largest(x0, x1), recolor(c1, x1), "
                         "x1), x0)"))
    assert not SPACE.check(P("map_objs(move(up, n1, x2), x0)"))
    assert not SPACE.check(P("crop(x0)"))
    assert not SPACE.check(P("upscale(c2, x0)"))
    assert not SPACE.check(P("rot90(x0, x0)"))


SOLUTIONS = {
    "3c9b0459": "rot180(x0)",
    "c59eb873": "upscale(n2, x0)",
    "00d62c1b": "fill_enclosed(c4, x0)",
    "0520fde7": "cell_and(c2, left_half(x0), right_half(x0))",
    "1f85a75f": "crop(largest(x0))",
    "6e82a1ae": "map_objs(ite(size_eq(n4, x1), recolor(c1, x1), ite(size_eq("
                "n3, x1), recolor(c2, x1), recolor(c3, x1))), x0)",
    "dbc1a6ce": "overlay(replace(c1, c8, connect(x0)), x0)",
    "d037b0a7": "map_objs(extend(down, x0, x1), x0)",
    "b8825c91": "symmetrize(x0)",
    "a79310a0": "map_objs(recolor(c2, move(down, n1, x1)), x0)",
}


@pytest.mark.parametrize("name", SOLUTIONS)
def test_encode_decode_propagate(name):
    tree = P(SOLUTIONS[name])
    assert SPACE.check(tree)
    labels = SPACE.encode(tree)
    assert SPACE.decode(labels) == tree
    cand = SPACE.singleton(labels)
    assert (SPACE.propagate(cand) == cand).all()


@pytest.mark.parametrize("name", SOLUTIONS)
def test_solves_arc_training_task(name):
    path = os.path.join(ARC, "data", "training", f"{name}.json")
    if not os.path.exists(path):
        pytest.skip(f"no ARC-AGI-1 training split at {ARC}")
    with open(path) as f:
        data = json.load(f)
    f = SPACE.compile(P(SOLUTIONS[name]))
    for pair in data["train"] + data["test"]:
        x, y = (tuple(map(tuple, pair[k])) for k in ("input", "output"))
        assert f(x) == y


def test_only_undefined_escapes():
    grids = [G, H, W, ((0, ), ), ((1, ) * 30, ) * 30]
    for size in range(1, 4):
        for tree in SPACE.trees(size):
            f = SPACE.compile(tree)
            for g in grids:
                try:
                    out = f(g)
                except Undefined:
                    continue
                assert 0 < len(out) <= 30 and 0 < len(out[0]) <= 30
                assert all(len(row) == len(out[0]) for row in out)
