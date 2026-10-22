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


def load(root: str, split: str) -> list[Task]:
    if split == SEALED and not os.environ.get(UNSEAL):
        raise RuntimeError(
            f"{root}/data/{split} is sealed: set {UNSEAL} to the claim it "
            "scores and log the read in EVALUATION.md")
    tasks = []
    for path in sorted(glob.glob(os.path.join(root, "data", split, "*.json"))):
        with open(path) as f:
            data = json.load(f)
        pairs = [[(grid(p["input"]), grid(p["output"])) for p in data[k]]
                 for k in ("train", "test")]
        tasks.append(Task(os.path.basename(path)[:-5], *pairs))
    return tasks
