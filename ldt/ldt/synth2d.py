"""
Random two-dimensional inputs for synthetic ARC tasks.

A style fixes what a task's inputs share: the size range, the background, the
palette and the kind of objects (rectangles, random 8-connected shapes, single
pixels, lines, noise, a separator line splitting the grid in two). Each input
draws its own objects in that style.
"""

from __future__ import annotations

import random


def random_style(rng: random.Random) -> dict:
    small = rng.random() < 0.6
    h = rng.randint(3, 12) if small else rng.randint(10, 30)
    w = h if rng.random() < 0.5 else (
        rng.randint(3, 12) if small else rng.randint(10, 30))
    return {
        "height": (max(2, h - rng.choice([0, 0, 2])), h),
        "width": (max(2, w - rng.choice([0, 0, 2])), w),
        "background": 0 if rng.random() < 0.8 else rng.randint(1, 9),
        "palette": rng.sample(range(1, 10), rng.choice([1, 1, 2, 2, 3, 4, 6])),
        "objects": (1, rng.choice([1, 2, 3, 4, 6, 10])),
        "kinds": rng.sample(["rect", "shape", "pixel", "line", "hollow"],
                            rng.choice([1, 1, 2, 3])),
        "size": rng.choice([1, 2, 3, 4, 6]),
        "noise": rng.choice([0, 0, 0, 0.05]),
        "separator": rng.random() < 0.1,
    }


def random_grid(rng: random.Random, style: dict):
    h, w = rng.randint(*style["height"]), rng.randint(*style["width"])
    bg = style["background"]
    palette = [c for c in style["palette"] if c != bg] or [1 + bg % 9]
    grid = [[bg] * w for _ in range(h)]
    for _ in range(rng.randint(*style["objects"])):
        colour = rng.choice(palette)
        kind = rng.choice(style["kinds"])
        s = style["size"]
        oh, ow = rng.randint(1, min(h, s + 1)), rng.randint(1, min(w, s + 1))
        r, c = rng.randrange(h - oh + 1), rng.randrange(w - ow + 1)
        if kind == "pixel":
            grid[r][c] = colour
        elif kind == "line":
            if rng.random() < 0.5:
                for cc in range(c, min(w, c + rng.randint(2, w))):
                    grid[r][cc] = colour
            else:
                for rr in range(r, min(h, r + rng.randint(2, h))):
                    grid[rr][c] = colour
        elif kind == "rect":
            for rr in range(r, r + oh):
                for cc in range(c, c + ow):
                    grid[rr][cc] = colour
        elif kind == "hollow":
            for rr in range(r, r + oh):
                for cc in range(c, c + ow):
                    if rr in (r, r + oh - 1) or cc in (c, c + ow - 1):
                        grid[rr][cc] = colour
        else:  # a random 8-connected shape grown from one cell
            cells = {(r, c)}
            for _ in range(rng.randint(1, oh * ow)):
                rr, cc = rng.choice(sorted(cells))
                rr += rng.choice([-1, 0, 1])
                cc += rng.choice([-1, 0, 1])
                if 0 <= rr < h and 0 <= cc < w:
                    cells.add((rr, cc))
            for rr, cc in cells:
                grid[rr][cc] = colour
    if style["noise"]:
        for rr in range(h):
            for cc in range(w):
                if rng.random() < style["noise"]:
                    grid[rr][cc] = rng.choice(palette)
    if style["separator"] and h >= 3 and w >= 3:
        colour = rng.choice([c for c in range(10) if c != bg])
        if rng.random() < 0.5 and w % 2:
            for rr in range(h):
                grid[rr][w // 2] = colour
        elif h % 2:
            grid[h // 2] = [colour] * w
    return tuple(tuple(row) for row in grid)
