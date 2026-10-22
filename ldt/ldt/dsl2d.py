"""
A typed signature for two-dimensional ARC grids.

Base types: ``G`` a grid (a tuple of rows of colours, at most 30 by 30), ``O``
an object (the row and column of its top-left corner and its patch, ``-1`` off
the object, which may stretch outside the grid), ``N`` a small number, ``C`` a
colour, ``B`` a boolean, ``D`` a direction. Programs have type ``G -> G``.

The background of a grid is its most common colour, the smaller on ties.
Objects are the 8-connected components of non-background cells of one colour,
blobs those of any colour, both ordered by the top-left corner of their
bounding box, then colour. A grid is rebuilt from objects by painting them in
order on a blank grid of the same shape; background cells of an object leave
the grid as it is, cells outside the grid are clipped.

Example
-------
>>> from ldt.bohm import Tree
>>> x0, x1 = Tree("x0"), Tree("x1")
>>> fall = Tree("map_objs", (Tree("move", (Tree("down"), Tree("n1"), x1)), x0))
>>> SPACE.compile(fall)(((0, 3, 0), (0, 0, 0), (0, 0, 0)))
((0, 0, 0), (0, 3, 0), (0, 0, 0))
"""

from __future__ import annotations

from functools import lru_cache
from itertools import chain

from ldt.bohm import Primitive, Space, Ty, Undefined

Grid = tuple[tuple[int, ...], ...]
Obj = tuple[int, int, tuple[tuple[int, ...], ...]]

MAX = 30
DIRECTIONS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


def check_grid(g: Grid) -> Grid:
    if not g or not g[0] or len(g) > MAX or len(g[0]) > MAX:
        raise Undefined("empty or oversized grid")
    return g


def check_obj(o: Obj) -> Obj:
    if not o[2] or not o[2][0]:
        raise Undefined("empty object")
    return o


def rows(flat: list[int], w: int) -> Grid:
    return tuple(tuple(flat[i:i + w]) for i in range(0, len(flat), w))


@lru_cache(maxsize=4096)
def histogram(g: Grid) -> tuple[int, ...]:
    flat = tuple(chain.from_iterable(g))
    return tuple(flat.count(c) for c in range(10))


def bg(g: Grid) -> int:
    counts = histogram(g)
    return 0 if counts[0] else counts.index(max(counts))


def least(g: Grid) -> int:
    counts = histogram(g)
    return min((n, c) for c, n in enumerate(counts) if n)[1]


@lru_cache(maxsize=64)
def neighbours(h: int, w: int, diagonal: bool = True) -> tuple:
    steps = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
             if (dy or dx) and (diagonal or not dy or not dx)]
    return tuple(
        tuple((y + dy) * w + x + dx for dy, dx in steps
              if 0 <= y + dy < h and 0 <= x + dx < w)
        for y in range(h) for x in range(w))


@lru_cache(maxsize=1 << 14)
def colour(patch) -> int:
    counts = [sum(row.count(c) for row in patch) for c in range(10)]
    return counts.index(max(counts))


def size(o: Obj) -> int:
    return sum(len(row) - row.count(-1) for row in o[2])


def cells(o: Obj) -> list[tuple[int, int, int]]:
    r0, c0, patch = o
    return [(r0 + i, c0 + j, v) for i, row in enumerate(patch)
            for j, v in enumerate(row) if v >= 0]


def from_cells(cs) -> Obj:
    r0, r1 = min(r for r, _, _ in cs), max(r for r, _, _ in cs)
    c0, c1 = min(c for _, c, _ in cs), max(c for _, c, _ in cs)
    patch = [[-1] * (c1 - c0 + 1) for _ in range(r1 - r0 + 1)]
    for r, c, v in cs:
        patch[r - r0][c - c0] = v
    return r0, c0, tuple(map(tuple, patch))


@lru_cache(maxsize=4096)
def components(g: Grid, by_colour: bool) -> tuple[Obj, ...]:
    h, w = len(g), len(g[0])
    flat, b = tuple(chain.from_iterable(g)), bg(g)
    adjacent = neighbours(h, w)
    seen = bytearray(len(flat))
    found = []
    for i, v in enumerate(flat):
        if v == b or seen[i]:
            continue
        seen[i], stack, members = 1, [i], []
        while stack:
            j = stack.pop()
            members.append(j)
            for k in adjacent[j]:
                if not seen[k]:
                    u = flat[k]
                    if u != b and (u == v or not by_colour):
                        seen[k] = 1
                        stack.append(k)
        found.append(from_cells([(j // w, j % w, flat[j]) for j in members]))
    found.sort(key=lambda o: (o[0], o[1], colour(o[2])))
    return tuple(found)


def objs(g: Grid) -> tuple[Obj, ...]:
    return components(g, True)


def blobs(g: Grid) -> tuple[Obj, ...]:
    return components(g, False)


@lru_cache(maxsize=4096)
def max_size(g: Grid) -> int:
    return max((size(o) for o in objs(g)), default=0)


def paint_into(canvas: list[list[int]], o: Obj):
    r0, c0, patch = check_obj(o)
    h, w = len(canvas), len(canvas[0])
    for i, prow in enumerate(patch):
        r = r0 + i
        if 0 <= r < h:
            crow = canvas[r]
            for j, v in enumerate(prow):
                if v >= 0 and 0 <= c0 + j < w:
                    crow[c0 + j] = v


def canvas(g: Grid, objects) -> Grid:
    out = [[bg(g)] * len(g[0]) for _ in g]
    for o in objects:
        paint_into(out, o)
    return tuple(map(tuple, out))


def paint(o: Obj, g: Grid) -> Grid:
    out = list(map(list, g))
    paint_into(out, o)
    return tuple(map(tuple, out))


def crop(o: Obj) -> Grid:
    patch = check_obj(o)[2]
    return check_grid(tuple(tuple(v if v >= 0 else 0 for v in row)
                            for row in patch))


def trim(g: Grid) -> Grid:
    b = bg(g)
    ys = [i for i, row in enumerate(g) if any(v != b for v in row)]
    if not ys:
        raise Undefined("nothing to trim to")
    xs = [j for j, col in enumerate(zip(*g)) if any(v != b for v in col)]
    return tuple(row[xs[0]:xs[-1] + 1] for row in g[ys[0]:ys[-1] + 1])


def upscale(n: int, g: Grid) -> Grid:
    if n < 1 or len(g) * n > MAX or len(g[0]) * n > MAX:
        raise Undefined("upscale out of range")
    out = []
    for row in g:
        out += [tuple(v for v in row for _ in range(n))] * n
    return tuple(out)


def downscale(n: int, g: Grid) -> Grid:
    if n < 1:
        raise Undefined("downscale by zero")
    return tuple(row[::n] for row in g[::n])


def tile(n: int, m: int, g: Grid) -> Grid:
    if n < 1 or m < 1 or len(g) * n > MAX or len(g[0]) * m > MAX:
        raise Undefined("tile out of range")
    return tuple(row * m for row in g) * n


def hconcat(a: Grid, b: Grid) -> Grid:
    if len(a) != len(b) or len(a[0]) + len(b[0]) > MAX:
        raise Undefined("hconcat of different heights")
    return tuple(x + y for x, y in zip(a, b))


def vconcat(a: Grid, b: Grid) -> Grid:
    if len(a[0]) != len(b[0]) or len(a) + len(b) > MAX:
        raise Undefined("vconcat of different widths")
    return a + b


def same_shape(a: Grid, b: Grid):
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise Undefined("shape mismatch")


def overlay(a: Grid, b: Grid) -> Grid:
    same_shape(a, b)
    k = bg(b)
    return tuple(tuple(y if y != k else x for x, y in zip(ra, rb))
                 for ra, rb in zip(a, b))


def replace(c: int, d: int, g: Grid) -> Grid:
    return tuple(tuple(d if v == c else v for v in row) for row in g)


@lru_cache(maxsize=4096)
def enclosed(g: Grid) -> tuple[int, ...]:
    """The background cells not 4-connected to the border by background."""
    h, w = len(g), len(g[0])
    flat, b = tuple(chain.from_iterable(g)), bg(g)
    adjacent = neighbours(h, w, False)
    seen = bytearray(len(flat))
    stack = [i for i, v in enumerate(flat) if v == b and (
        i < w or i >= (h - 1) * w or i % w in (0, w - 1))]
    for i in stack:
        seen[i] = 1
    while stack:
        for k in adjacent[stack.pop()]:
            if not seen[k] and flat[k] == b:
                seen[k] = 1
                stack.append(k)
    return tuple(i for i, v in enumerate(flat) if v == b and not seen[i])


def fill_enclosed(c: int, g: Grid) -> Grid:
    holes = enclosed(g)
    if not holes:
        return g
    flat = list(chain.from_iterable(g))
    for i in holes:
        flat[i] = c
    return rows(flat, len(g[0]))


def connect_lines(lines, b: int):
    for line in lines:
        out = list(line)
        marks = [(j, v) for j, v in enumerate(line) if v != b]
        for (i, u), (j, v) in zip(marks, marks[1:]):
            if u == v and j > i + 1:
                out[i + 1:j] = [u] * (j - i - 1)
        yield out


def connect(g: Grid) -> Grid:
    """Rows first, then columns: a vertical line crosses a horizontal one."""
    b = bg(g)
    out = list(connect_lines(g, b))
    for j, col in enumerate(connect_lines(zip(*g), b)):
        for i, v in enumerate(col):
            if v != b:
                out[i][j] = v
    return tuple(map(tuple, out))


def halve(g: Grid, keep_first: bool, vertical: bool) -> Grid:
    if vertical:
        k = len(g) // 2
        return check_grid(g[:k] if keep_first else g[len(g) - k:])
    k = len(g[0]) // 2
    return check_grid(tuple(row[:k] if keep_first else row[len(row) - k:]
                            for row in g))


def cellwise(op):
    """A cell is on when it is not 0: the halves of a logic task often hold
    more ink than background, so their most common colour is no guide."""
    def fn(c: int, a: Grid, b: Grid) -> Grid:
        same_shape(a, b)
        return tuple(tuple(c if op(x != 0, y != 0) else 0
                           for x, y in zip(ra, rb)) for ra, rb in zip(a, b))
    return fn


@lru_cache(maxsize=1024)
def symmetrize(g: Grid) -> Grid:
    """
    The mask is the colour found in every asymmetric pair of cells of the
    most mirror symmetries among flip_h, flip_v and rot180, the least common
    on ties. Each mask cell takes the value of its image under the first of
    those symmetries that holds outside the mask and is not the mask there.
    """
    images = (tuple(row[::-1] for row in g), g[::-1],
              tuple(row[::-1] for row in g[::-1]))
    shared = []
    for image in images:
        common = None
        for ra, rb in zip(g, image):
            if ra == rb:
                continue
            for v, u in zip(ra, rb):
                if v != u:
                    common = {u, v} if common is None else common & {u, v}
            if common == set():
                break
        shared.append(common or set())
    candidates = set().union(*shared)
    if not candidates:
        return g
    counts = histogram(g)
    m = min(candidates, key=lambda c: (
        -sum(c in s for s in shared), counts[c], c))
    usable = [image for image, s in zip(images, shared) if m in s]
    out = list(map(list, g))
    for i, row in enumerate(g):
        for j, v in enumerate(row):
            if v != m:
                continue
            for image in usable:
                if image[i][j] != m:
                    out[i][j] = image[i][j]
                    break
    return tuple(map(tuple, out))


def move(d: str, n: int, o: Obj) -> Obj:
    dr, dc = DIRECTIONS[d]
    return o[0] + n * dr, o[1] + n * dc, o[2]


def obstacle(g: Grid, own: set):
    h, w, b = len(g), len(g[0]), bg(g)
    return lambda r, c: not (0 <= r < h and 0 <= c < w)\
        or (g[r][c] != b and (r, c) not in own)


def slide(d: str, g: Grid, o: Obj) -> Obj:
    dr, dc = DIRECTIONS[d]
    points = [(r, c) for r, c, _ in cells(o)]
    blocked = obstacle(g, set(points))
    k = 0
    while k < MAX and not any(blocked(r + (k + 1) * dr, c + (k + 1) * dc)
                              for r, c in points):
        k += 1
    return o[0] + k * dr, o[1] + k * dc, o[2]


def extend(d: str, g: Grid, o: Obj) -> Obj:
    """Each cell last in its line along ``d`` casts a ray of its colour until
    the next cell is off the grid or a cell of ``g`` not in the object."""
    dr, dc = DIRECTIONS[d]
    cs = cells(o)
    blocked = obstacle(g, {(r, c) for r, c, _ in cs})
    ends = {}
    for r, c, v in cs:
        key, depth = (c, r * dr) if dr else (r, c * dc)
        if key not in ends or depth > ends[key][0]:
            ends[key] = depth, r, c, v
    rays = []
    for _, r, c, v in ends.values():
        while not blocked(r + dr, c + dc):
            r, c = r + dr, c + dc
            rays.append((r, c, v))
    return from_cells(cs + rays) if rays else o


def recolor(c: int, o: Obj) -> Obj:
    return o[0], o[1], tuple(tuple(c if v >= 0 else -1 for v in row)
                             for row in o[2])


def border(c: int, o: Obj) -> Obj:
    patch = list(map(list, check_obj(o)[2]))
    h, w = len(patch), len(patch[0])
    for i in range(h):
        patch[i][0] = patch[i][w - 1] = c
    patch[0] = patch[h - 1] = [c] * w
    return o[0], o[1], tuple(map(tuple, patch))


def fill_box(c: int, o: Obj) -> Obj:
    return o[0], o[1], tuple(tuple(v if v >= 0 else c for v in row)
                             for row in o[2])


def ite(b, x, y):
    return x() if b() else y()


def pick(p, g: Grid) -> Obj:
    for o in objs(g):
        if p(o):
            return o
    raise Undefined("pick found nothing")


def largest(g: Grid) -> Obj:
    if not objs(g):
        raise Undefined("no object")
    return max(objs(g), key=size)


def smallest(g: Grid) -> Obj:
    if not objs(g):
        raise Undefined("no object")
    return min(objs(g), key=size)


def touches_border(g: Grid, o: Obj) -> bool:
    h, w = len(g), len(g[0])
    r0, c0, patch = o
    if r0 > 0 and c0 > 0 and r0 + len(patch) < h and c0 + len(patch[0]) < w:
        return False
    return any(r in (0, h - 1) or c in (0, w - 1) for r, c, _ in cells(o))


def _sig(name, ty, fn, lazy=False):
    return Primitive(name, Ty.parse(ty), fn, lazy)


PRIMITIVES = [
    _sig("rot90", "G -> G", lambda g: tuple(zip(*g[::-1]))),
    _sig("rot180", "G -> G", lambda g: tuple(row[::-1] for row in g[::-1])),
    _sig("rot270", "G -> G", lambda g: tuple(zip(*g))[::-1]),
    _sig("flip_h", "G -> G", lambda g: tuple(row[::-1] for row in g)),
    _sig("flip_v", "G -> G", lambda g: g[::-1]),
    _sig("transpose", "G -> G", lambda g: tuple(zip(*g))),
    _sig("upscale", "N -> G -> G", upscale),
    _sig("downscale", "N -> G -> G", downscale),
    _sig("tile", "N -> N -> G -> G", tile),
    _sig("hconcat", "G -> G -> G", hconcat),
    _sig("vconcat", "G -> G -> G", vconcat),
    _sig("overlay", "G -> G -> G", overlay),
    _sig("replace", "C -> C -> G -> G", replace),
    _sig("map_objs", "(O -> O) -> G -> G",
         lambda f, g: canvas(g, (f(o) for o in objs(g)))),
    _sig("map_blobs", "(O -> O) -> G -> G",
         lambda f, g: canvas(g, (f(o) for o in blobs(g)))),
    _sig("keep_objs", "(O -> B) -> G -> G",
         lambda p, g: canvas(g, (o for o in objs(g) if p(o)))),
    _sig("paint", "O -> G -> G", paint),
    _sig("crop", "O -> G", crop),
    _sig("trim", "G -> G", trim),
    _sig("fill_enclosed", "C -> G -> G", fill_enclosed),
    _sig("connect", "G -> G", connect),
    _sig("left_half", "G -> G", lambda g: halve(g, True, False)),
    _sig("right_half", "G -> G", lambda g: halve(g, False, False)),
    _sig("top_half", "G -> G", lambda g: halve(g, True, True)),
    _sig("bottom_half", "G -> G", lambda g: halve(g, False, True)),
    _sig("cell_and", "C -> G -> G -> G", cellwise(lambda p, q: p and q)),
    _sig("cell_or", "C -> G -> G -> G", cellwise(lambda p, q: p or q)),
    _sig("cell_xor", "C -> G -> G -> G", cellwise(lambda p, q: p != q)),
    _sig("cell_nor", "C -> G -> G -> G", cellwise(lambda p, q: not (p or q))),
    _sig("symmetrize", "G -> G", symmetrize),
    _sig("move", "D -> N -> O -> O", move),
    _sig("slide", "D -> G -> O -> O", slide),
    _sig("extend", "D -> G -> O -> O", extend),
    _sig("recolor", "C -> O -> O", recolor),
    _sig("flip_obj_h", "O -> O",
         lambda o: (o[0], o[1], tuple(row[::-1] for row in o[2]))),
    _sig("flip_obj_v", "O -> O", lambda o: (o[0], o[1], o[2][::-1])),
    _sig("border", "C -> O -> O", border),
    _sig("fill_box", "C -> O -> O", fill_box),
    _sig("ite", "B -> O -> O -> O", ite, lazy=True),
    _sig("pick", "(O -> B) -> G -> O", pick),
    _sig("largest", "G -> O", largest),
    _sig("smallest", "G -> O", smallest),
    _sig("size_eq", "N -> O -> B", lambda n, o: size(o) == n),
    _sig("size_gt", "N -> O -> B", lambda n, o: size(o) > n),
    _sig("colour_eq", "C -> O -> B", lambda c, o: colour(o[2]) == c),
    _sig("touches_border", "G -> O -> B", touches_border),
    _sig("is_largest", "G -> O -> B", lambda g, o: size(o) == max_size(g)),
    _sig("not_", "B -> B", lambda b: not b),
    _sig("size", "O -> N", size),
    _sig("count", "G -> N", lambda g: len(objs(g))),
    _sig("height", "G -> N", len),
    _sig("width", "G -> N", lambda g: len(g[0])),
    _sig("colour", "O -> C", lambda o: colour(o[2])),
    _sig("most", "G -> C", bg),
    _sig("least", "G -> C", least),
] + [_sig(f"n{k}", "N", k) for k in range(6)]\
  + [_sig(f"c{k}", "C", k) for k in range(10)]\
  + [_sig(d, "D", d) for d in DIRECTIONS]

PYTHON_TYPES = {"G": tuple, "O": tuple, "N": int, "C": int, "B": bool,
                "D": str}

SPACE = Space(PRIMITIVES, Ty.parse("G -> G"), depth=6, arity=3, max_vars=3)
