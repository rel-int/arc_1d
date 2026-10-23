"""
ARC-AGI-1 and ARC-AGI-2 tasks, with the evaluation splits sealed.

``load(root, "training")`` reads a split of either benchmark's ``data/``
directory. The evaluation split is read only to score a published claim, as
USER ruled for the earlier ARC work (2026-09-03): ``load`` refuses it unless
``LDT_UNSEAL`` names the claim, and every read is appended to
``EVALUATION.md`` by whoever unseals it. A task with several test inputs is
one task: solved when every test output is right.
"""

from __future__ import annotations

import glob
import json
import os

from ldt.data import Task

SEALED = "evaluation"
UNSEAL = "LDT_UNSEAL"


def grid(rows) -> tuple:
    return tuple(tuple(r) for r in rows)


def sealed_ids(root: str) -> set[str]:
    """The task ids of a benchmark's evaluation split, from the file names
    alone: ARC-AGI-2's training split holds most of ARC-AGI-1's evaluation."""
    return {name[:-5] for name in os.listdir(os.path.join(root, "data", SEALED))
            if name.endswith(".json")}


def load(root: str, split: str, claim: str = "",
         exclude: set[str] = frozenset()) -> list[Task]:
    """The tasks of a split, without those in ``exclude``; the evaluation
    split only with a ``claim`` (or ``LDT_UNSEAL``) naming what it scores."""
    split = os.path.basename(os.path.normpath(split))
    if split == SEALED and not (claim or os.environ.get(UNSEAL)):
        raise RuntimeError(
            f"{root}/data/{split} is sealed: name the claim it scores and "
            "log the read in EVALUATION.md")
    tasks = []
    for path in sorted(glob.glob(os.path.join(root, "data", split, "*.json"))):
        name = os.path.basename(path)[:-5]
        if name in exclude:
            continue
        with open(path) as f:
            data = json.load(f)
        pairs = [[(grid(p["input"]), grid(p["output"])) for p in data[k]]
                 for k in ("train", "test")]
        tasks.append(Task(name, *pairs))
    return tasks
