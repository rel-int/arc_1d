"""
Runs side by side, each a group of seeds, as mean ± sd per iteration.

    uv run python -m dc.compare library='results/lib-s*' control='results/ctl-s*'
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

COLUMNS = {"top1": "top-1 (selected)", "top1_dl": "top-1 (least DL)", "kept": "any kept",
           "train": "fit train exactly", "mean_dl": "mean DL", "seconds": "seconds"}


def histories(pattern: str) -> list[list[dict]]:
    return [json.loads((d / "history.json").read_text()) for d in sorted(Path().glob(pattern))
            if (d / "history.json").exists()]


def spread(values: list[float | None]) -> str:
    if None in values:
        return "–"
    sd = statistics.stdev(values) if len(values) > 1 else 0.
    return f"{statistics.mean(values):.1f} ± {sd:.1f}"


def table(groups: dict[str, list[list[dict]]]) -> str:
    lines = ["| run | seeds | iteration | " + " | ".join(COLUMNS.values()) + " |",
             "|---|---|---|" + "---|" * len(COLUMNS)]
    for name, runs in groups.items():
        for i in range(min(len(h) for h in runs)):
            cells = [spread([h[i].get(k) for h in runs]) for k in COLUMNS]
            lines.append(f"| {name} | {len(runs)} | {i} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    groups = dict(arg.split("=", 1) for arg in sys.argv[1:])
    print(table({name: histories(pattern) for name, pattern in groups.items()}))


if __name__ == "__main__":
    main()
