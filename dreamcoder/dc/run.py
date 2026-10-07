"""
The wake/abstract loop on 1D-ARC, writing ``results/<name>/report.md``.

    uv run python -m dc.run            # default: ~10 tasks per family, 3 iterations
    uv run python -m dc.run --quick    # smoke test: a few minutes
"""

from __future__ import annotations

import argparse
import json
import platform
import random
import time
from collections import defaultdict
from dataclasses import asdict
from multiprocessing import get_context
from pathlib import Path

import torch

from dc import data
from dc.abstract import abstract
from dc.library import Library
from dc.semantics import TraceFree
from dc.terms import to_diagram
from dc.wake import Config, candidates, wake

QUICK = dict(per_family=2, iterations=2, max_candidates=30, steps=60)


def parse():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--quick", action="store_true", help=f"smoke test, i.e. {QUICK}")
    parser.add_argument("--per-family", type=int, default=10, help="tasks per family, 0 for all 50")
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--new-boxes", type=int, default=2, help="library entries added per iteration")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--out", type=Path, default=None)
    for name, value in asdict(Config()).items():
        parser.add_argument(f"--{name.replace('_', '-')}", type=type(value), default=value)
    args = parser.parse_args()
    if args.quick:
        for name, value in QUICK.items():
            setattr(args, name, value)
    args.out = args.out or Path("results") / ("quick" if args.quick else "default")
    return args


def run_task(job):
    task, terms, library, config, iteration = job
    return task.name, wake(task, terms, library, TraceFree(), config, iteration)


def main():
    args = parse()
    config = Config(**{k: getattr(args, k) for k in asdict(Config())})
    random.seed(config.seed)
    torch.manual_seed(config.seed)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "config.json").write_text(json.dumps(
        {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()}
        | {"torch": torch.__version__, "python": platform.python_version()}, indent=2))
    tasks = data.load(args.data, args.per_family or None, config.seed)
    by_name = {t.name: t for t in tasks}
    library = Library.base()
    history, best = [], {}
    with get_context("fork").Pool(args.workers) as pool:
        for iteration in range(args.iterations):
            start = time.time()
            terms = candidates(library, config)
            jobs = [(t, terms, library, config, iteration) for t in tasks]
            results = dict(pool.imap_unordered(run_task, jobs))
            best = {name: solutions[0] for name, solutions in results.items()}
            record = summarise(iteration, tasks, results, library, len(terms))
            added = abstract(library, best, args.new_boxes, iteration) \
                if iteration < args.iterations - 1 else []
            record["new_boxes"] = [(e.signature(), str(e.body), len(e.weights)) for e in added]
            record["seconds"] = time.time() - start
            history.append(record)
            print(f"iteration {iteration}: top-1 {record['top1']}/{len(tasks)}, "
                  f"train-solved {record['train']}, mean DL {record['mean_dl']:.1f}, "
                  f"library {record['library']}, {record['seconds']:.0f}s, new {record['new_boxes']}",
                  flush=True)
            (args.out / "history.json").write_text(json.dumps(history, indent=2))
    write_report(args, config, tasks, by_name, history, best, results, library)


def summarise(iteration, tasks, results, library, n_candidates):
    family = defaultdict(lambda: [0, 0])
    top1 = top3 = train = 0
    for task in tasks:
        solutions = results[task.name]
        hit = solutions[0].test_prediction == task.test[1]
        top1 += hit
        top3 += any(s.test_prediction == task.test[1] for s in solutions)
        train += solutions[0].train_exact
        family[task.family][0] += hit
        family[task.family][1] += 1
    dls = [results[t.name][0].dl for t in tasks]
    return dict(iteration=iteration, top1=top1, top3=top3, train=train, tasks=len(tasks),
                library=len(library), candidates=n_candidates, mean_dl=sum(dls) / len(dls),
                family=dict(sorted(family.items())),
                solutions={t.name: [str(s.term), round(s.dl, 1), s.test_prediction == t.test[1]]
                           for t in tasks for s in results[t.name][:1]})


def grid_rows(task, prediction):
    rows = [f"| train {i} | `{data.show(a)}` | `{data.show(b)}` |" for i, (a, b) in enumerate(task.train)]
    rows.append(f"| **test** | `{data.show(task.test[0])}` | `{data.show(task.test[1])}` |")
    rows.append(f"| predicted | | `{data.show(prediction)}` |")
    return ["| pair | input | output |", "|---|---|---|", *rows]


def write_report(args, config, tasks, by_name, history, best, results, library):
    figures = args.out / "figures"
    figures.mkdir(exist_ok=True)
    families = sorted({t.family for t in tasks})
    lines = [
        "# Diagrammatic DreamCoder on 1D-ARC: results", "",
        f"Tasks: {len(tasks)} ({args.per_family or 50} per family, drawn with seed {config.seed}), "
        f"fitted on their 3 training pairs only, scored on the held-out test pair by exact match. "
        f"Config: `{args.out / 'config.json'}`.", "",
        "## Per iteration", "",
        "| iteration | top-1 test | top-3 test | train fit exactly | mean DL (bits) | library | candidates | wall-clock |",
        "|---|---|---|---|---|---|---|---|"]
    for r in history:
        n = r["tasks"]
        lines.append(f"| {r['iteration']} | {r['top1']}/{n} ({r['top1'] / n:.0%}) | {r['top3']}/{n} "
                     f"| {r['train']}/{n} | {r['mean_dl']:.1f} | {r['library']} | {r['candidates']} "
                     f"| {r['seconds']:.0f}s |")
    lines += ["", "Top-1 is the prediction of the least-DL candidate; top-3 counts a hit "
              "among the three kept. Mean DL is over the best candidate of every task.", "",
              "## Per family (top-1 test exact match)", "",
              "| family | " + " | ".join(f"it {r['iteration']}" for r in history) + " |",
              "|---|" + "---|" * len(history)]
    for family in families:
        lines.append(f"| {family} | " + " | ".join(
            "{}/{}".format(*r["family"][family]) for r in history) + " |")
    lines += ["", "## Library growth", ""]
    for r in history:
        for signature, body, n_weights in r["new_boxes"]:
            lines.append(f"- after iteration {r['iteration']}: `{signature}` := `{body}` "
                         f"({n_weights} trained weight tensors inherited)")
    if not any(r["new_boxes"] for r in history):
        lines.append("- no fragment had support in two tasks")
    for entry in library.entries.values():
        if not entry.is_primitive:
            path = figures / f"box-{entry.name}.png"
            to_diagram(entry.body, library).draw(path=str(path), figsize=(4, 3))
            lines += ["", f"`{entry.name}`'s body:", "", f"![{entry.name}](figures/{path.name})"]
    lines += ["", "## Examples from the last iteration", ""]
    last = history[-1]["solutions"]
    solved = [n for n in sorted(last) if last[n][2]]
    failed = [n for n in sorted(last) if not last[n][2]]
    pick = random.Random(config.seed)
    for kind, names in (("Solved", solved), ("Failed", failed)):
        chosen = sorted(pick.sample(names, min(3, len(names))),
                        key=lambda n: by_name[n].family)
        for name in chosen:
            solution = results[name][0]
            path = figures / f"{name}.png"
            to_diagram(solution.term, library).draw(path=str(path), figsize=(5, 4))
            lines += [f"### {kind}: `{name}`", "",
                      f"`{solution.term}`, DL {solution.dl:.1f} = {solution.structure:.1f} structure "
                      f"+ {solution.params:.1f} parameters + {solution.data:.1f} data bits, "
                      f"{'fits' if solution.train_exact else 'does not fit'} its training pairs exactly.", "",
                      f"![{name}](figures/{path.name})", "",
                      *grid_rows(by_name[name], solution.test_prediction), ""]
    lines += ["## All best solutions, last iteration", "", "| task | term | DL | test |", "|---|---|---|---|"]
    for name in sorted(last):
        term, dl, hit = last[name]
        lines.append(f"| {name} | `{term}` | {dl} | {'✓' if hit else '✗'} |")
    (args.out / "report.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out / 'report.md'}")


if __name__ == "__main__":
    main()
