"""
Tasks as tensors, and the benchmarks.

A task is a list of training pairs and a list of test pairs of one-dimensional
grids (tuples of colours). On the device a batch of tasks is

- ``inputs``, ``outputs``: (batch, pairs, length) colour codes, the training
  pairs first, then the test input with a ``MASK``ed output, ``PAD`` beyond;
- ``Y``: (batch, K, positions) the labels of the solution set, ``valid`` its
  rows; empty for a benchmark task.

Colour permutations fixing the background are the augmentation: they act on
the grids and on the colour constants of the programs alike.
"""

from __future__ import annotations

import glob
import json
import os
import random
from dataclasses import dataclass, field

import numpy as np
import torch

from ldt.bohm import Space
from ldt.model import MASK, PAD

ONE_D_ARC = "https://github.com/khalil-research/1D-ARC"
ONE_D_ARC_COMMIT = "1e74dc4cb4c58d8160e1fbd0ba638eb745f37147"


@dataclass
class Task:
    name: str
    train: list
    test: list
    solutions: list = field(default_factory=list)  # label vectors
    family: str = ""


def load_1darc(root: str) -> list[Task]:
    """The 901 tasks of 1D-ARC (Xu et al., 2023) in ``root/dataset``."""
    tasks = []
    for path in sorted(glob.glob(os.path.join(root, "dataset", "*", "*.json"))):
        family = os.path.basename(os.path.dirname(path))[3:]
        with open(path) as f:
            data = json.load(f)
        pairs = [[(tuple(p["input"][0]), tuple(p["output"][0]))
                  for p in data[k]] for k in ("train", "test")]
        tasks.append(Task(os.path.basename(path)[:-5], *pairs, family=family))
    return tasks


def colour_permutation(rng: random.Random) -> list[int]:
    perm = list(range(1, 10))
    rng.shuffle(perm)
    return [0] + perm


def label_permutation(space: Space, perm: list[int]) -> np.ndarray:
    """The action of a colour permutation on the labels ``c0, ..., c9``."""
    table = np.arange(len(space.vocab))
    for k in range(10):
        name = f"c{k}"
        if name in space.index:
            table[space.index[name]] = space.index[f"c{perm[k]}"]
    return table


def encode(tasks: list[Task], space: Space, max_solutions: int, length: int,
           pairs: int, perms: list[list[int]] | None = None):
    """A batch of tasks as tensors (on the CPU)."""
    B = len(tasks)
    inputs = np.full((B, pairs, length), PAD, dtype=np.int64)
    outputs = np.full((B, pairs, length), PAD, dtype=np.int64)
    Y = np.zeros((B, max_solutions, space.n_positions), dtype=np.int64)
    valid = np.zeros((B, max_solutions), dtype=bool)
    for b, task in enumerate(tasks):
        perm = np.arange(10) if perms is None else np.asarray(perms[b])
        demos = task.train[:pairs - 1]
        for i, (x, y) in enumerate(demos):
            inputs[b, i, :len(x)] = perm[list(x)]
            outputs[b, i, :len(y)] = perm[list(y)]
        x = task.test[0][0]
        inputs[b, len(demos), :len(x)] = perm[list(x)]
        outputs[b, len(demos), :len(x)] = MASK
        table = label_permutation(space, list(perm))
        for k, labels in enumerate(task.solutions[:max_solutions]):
            Y[b, k] = table[labels]
            valid[b, k] = True
    return (torch.from_numpy(inputs), torch.from_numpy(outputs),
            torch.from_numpy(Y), torch.from_numpy(valid))
