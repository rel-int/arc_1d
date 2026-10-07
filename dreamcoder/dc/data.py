"""Loading 1D-ARC (Xu et al. 2023) and encoding grids as one-hot tensors."""

from __future__ import annotations

import json
import random
import subprocess
from dataclasses import dataclass
from pathlib import Path

import torch

COLOURS = 10
REPO = "https://github.com/khalil-research/1D-ARC.git"
COMMIT = "1e74dc4cb4c58d8160e1fbd0ba638eb745f37147"


@dataclass(frozen=True)
class Task:
    """A 1D-ARC task: its family, name, training pairs and the held-out test pair."""
    family: str
    name: str
    train: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]
    test: tuple[tuple[int, ...], tuple[int, ...]]

    @property
    def length(self) -> int:
        return len(self.test[0])


def fetch(root: Path) -> Path:
    """Clone 1D-ARC at a pinned commit into ``root`` unless it is there already."""
    target = root / "1D-ARC"
    if not (target / "dataset").exists():
        root.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "-q", REPO, str(target)], check=True)
        subprocess.run(["git", "-C", str(target), "checkout", "-q", COMMIT], check=True)
    return target / "dataset"


def load(root: Path, per_family: int | None = None, seed: int = 0) -> list[Task]:
    """Every task of every family, or ``per_family`` of each drawn with ``seed``."""
    tasks = []
    for family_dir in sorted(fetch(root).iterdir()):
        files = sorted(family_dir.glob("*.json"), key=lambda f: int(f.stem.split("_")[-1]))
        if per_family is not None:
            files = sorted(random.Random(f"{seed}/{family_dir.name}").sample(files, per_family))
        for file in files:
            raw = json.loads(file.read_text())
            pair = lambda p: (tuple(p["input"][0]), tuple(p["output"][0]))
            tasks.append(Task(
                family=family_dir.name.removeprefix("1d_"), name=file.stem,
                train=tuple(map(pair, raw["train"])), test=pair(raw["test"][0])))
    return tasks


def onehot(grids) -> torch.Tensor:
    """A batch of equal-length grids as a ``(batch, length, COLOURS)`` tensor."""
    return torch.nn.functional.one_hot(torch.tensor(grids), COLOURS).float()


def show(grid) -> str:
    return "".join("." if c == 0 else str(c) for c in grid)
