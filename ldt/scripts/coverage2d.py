"""
How much of ARC-AGI-1 training the 2D signature reaches by enumeration alone.

Every task of the training split is searched with :func:`ldt.enumerate.search`:
the programs of :data:`ldt.dsl2d.SPACE` in order of size, each run on the
demonstrations, until ``budget`` programs have been tried or four consistent
ones found. A task is *consistent* when some program reproduces every training
pair, *solved* when the right test outputs (every test pair) are among the two
answers ranked by :func:`ldt.solve.rank`. The first consistent program is the
smallest, since the enumeration goes by size.

    python -m scripts.coverage2d --budget 20000 --workers 4 \\
        --out /tmp/claude-0/results/coverage2d-20000.json
"""

from __future__ import annotations

import argparse
import json
import os
import time
from collections import Counter
from multiprocessing import Pool

from ldt.arc import load, sealed_ids
from ldt.bohm import Tree, is_variable
from ldt.dsl2d import SPACE
from ldt.enumerate import search
from ldt.solve import correct

TASKS = []
ROOT = "/home/user/ARC-AGI"


def heads(tree: Tree):
    yield tree.head
    for arg in tree.args:
        yield from heads(arg)


def init(root: str, arc1: str):
    exclude = sealed_ids(arc1) if os.path.abspath(root) != os.path.abspath(
        arc1) else set()
    TASKS.extend(load(root, "training", exclude=exclude))


def run(args) -> dict:
    i, budget = args
    task = TASKS[i]
    t0 = time.process_time()
    try:
        result = search(SPACE, task, budget)
    except Exception as e:
        return {"name": task.name, "error": f"{type(e).__name__}: {e}"}
    seconds = time.process_time() - t0
    top1, pass2, _ = correct(task, result.attempts)
    first = next(iter(result.programs), None)
    return {
        "name": task.name,
        "consistent": first is not None,
        "top1": top1,
        "pass2": pass2,
        "program": None if first is None else str(first),
        "size": None if first is None else first.size,
        "heads": [] if first is None else [
            h for h in heads(first) if not is_variable(h)],
        "first_call": result.first_call,
        "programs": len(result.programs),
        "calls": result.calls,
        "seconds": round(seconds, 3),
    }


def report(rows: list[dict], budget: int, wall: float) -> dict:
    ok = [r for r in rows if "error" not in r]
    found = [r for r in ok if r["consistent"]]
    calls, cpu = sum(r["calls"] for r in ok), sum(r["seconds"] for r in ok)
    return {
        "split": f"{os.path.basename(os.path.abspath(ROOT))} training",
        "budget": budget,
        "tasks": len(rows),
        "consistent": len(found),
        "top1": sum(r["top1"] for r in ok),
        "pass2": sum(r["pass2"] for r in ok),
        "consistent_by_size": dict(sorted(Counter(
            r["size"] for r in found).items())),
        "pass2_by_size": dict(sorted(Counter(
            r["size"] for r in found if r["pass2"]).items())),
        "heads_in_first_program": dict(Counter(
            h for r in found for h in set(r["heads"])).most_common()),
        "programs_tried": calls,
        "cpu_seconds": round(cpu, 1),
        "wall_seconds": round(wall, 1),
        "programs_per_cpu_second": round(calls / max(cpu, 1e-9)),
        "errors": [r for r in rows if "error" in r],
        "per_task": sorted(rows, key=lambda r: r["name"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--budget", type=int, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--root", default="/home/user/ARC-AGI")
    parser.add_argument("--arc1", default="/home/user/ARC-AGI",
                        help="ARC-AGI-1, whose evaluation ids stay sealed "
                             "inside any other root's training split")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    global ROOT
    ROOT = args.root
    init(args.root, args.arc1)
    n = len(TASKS)
    t0 = time.time()
    with Pool(args.workers, init, (args.root, args.arc1)) as pool:
        rows = []
        for row in pool.imap_unordered(
                run, [(i, args.budget) for i in range(n)], chunksize=1):
            rows.append(row)
            if len(rows) % 50 == 0:
                found = sum(r.get("consistent", 0) for r in rows)
                print(f"{len(rows)}/{n} tasks, {found} consistent, "
                      f"{time.time() - t0:.0f}s", flush=True)
    out = report(rows, args.budget, time.time() - t0)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("per_task", "errors")}, indent=1))
    print(f"{len(out['errors'])} errors, report in {args.out}")


if __name__ == "__main__":
    main()
