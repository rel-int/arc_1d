"""
Modal entry points: synthetic data on CPUs, training and evaluation on a GPU.

Everything lands on the volume ``ldt-arc``; results come back as return values
because ``modal volume get`` is blocked from the agents' sandbox.

    modal run modal_app.py::generate --name d1 --shards 200 --per-shard 500
    modal run --detach modal_app.py::train --name r1 --data d1 --gpu H100
    modal run modal_app.py::evaluate --run r1 --bench 1darc --prune 1
    modal run modal_app.py::fetch --path runs/r1/log.jsonl

``--dsl 2d`` selects the two-dimensional signature, ``--bench`` one of
``1darc``, ``arc1-training``, ``arc1-evaluation``, ``arc2-evaluation``; an
evaluation split needs ``--unseal`` naming the claim (see ``EVALUATION.md``).
"""

from __future__ import annotations

import json
import os
import pickle
import time

import modal

COMMIT = "1e74dc4cb4c58d8160e1fbd0ba638eb745f37147"
ARC1 = "399030444e0ab0cc8b4e199870fb20b863846f34"
ARC2 = "f3283f727488ad98fe575ea6a5ac981e4a188e49"
# https://github.com/michaelhodel/re-arc (MIT)
REARC = "e5b7f1d06362a76f9d3b8c25154ff1fafca897ce"

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git")
    .pip_install("numpy>=2.0", "torch==2.14.1")
    .run_commands(
        "git clone https://github.com/khalil-research/1D-ARC /data/1D-ARC",
        f"cd /data/1D-ARC && git checkout {COMMIT}",
        "git clone https://github.com/fchollet/ARC-AGI /data/ARC-AGI",
        f"cd /data/ARC-AGI && git checkout {ARC1}",
        "git clone https://github.com/arcprize/ARC-AGI-2 /data/ARC-AGI-2",
        f"cd /data/ARC-AGI-2 && git checkout {ARC2}",
        "git clone https://github.com/michaelhodel/re-arc /data/re-arc",
        f"cd /data/re-arc && git checkout {REARC}")
    .add_local_python_source("ldt")
)
# a second deployment (LDT_APP) runs new code while older calls finish
app = modal.App(os.environ.get("LDT_APP", "ldt-arc"), image=image)
volume = modal.Volume.from_name("ldt-arc", create_if_missing=True)
VOL = "/vol"


def signature(dsl: str):
    """The space of a signature and its input sampler."""
    if dsl == "1d":
        from ldt.dsl1d import SPACE
        return SPACE, None
    if dsl == "rearc":
        from ldt import rearc
        return rearc.space(), None
    if dsl != "2d":
        raise ValueError(f"unknown dsl {dsl!r}: 1d, 2d or rearc")
    from ldt.dsl2d import SPACE
    from ldt import synth2d
    return SPACE, (synth2d.random_style, synth2d.random_grid)


def benchmark(bench: str, unseal: str = ""):
    """The tasks of a benchmark; an evaluation split only with ``unseal``,
    the claim it scores, and never ARC-AGI-1's evaluation tasks inside
    ARC-AGI-2's training split."""
    from ldt.data import load_1darc
    from ldt import arc
    if bench == "1darc":
        return load_1darc("/data/1D-ARC")
    root = {"arc1": "/data/ARC-AGI", "arc2": "/data/ARC-AGI-2"}[bench[:4]]
    exclude = arc.sealed_ids("/data/ARC-AGI")\
        if bench == "arc2-training" else ()
    return arc.load(root, bench.split("-", 1)[1], claim=unseal,
                    exclude=set(exclude))


@app.function(cpu=1.0, memory=4096, timeout=3 * 3600, volumes={VOL: volume})
def generate_shard(name: str, seed: int, n: int, sizes=(2, 20),
                   dsl: str = "1d", exact: int = 0, mutants: float = 0.5):
    import random
    from ldt.synth import Generator
    from ldt.data import Task
    SPACE, inputs = signature(dsl)
    rng = random.Random(seed)
    if dsl == "rearc":
        from ldt.rearc import Generator as Rearc
        g = Rearc(mutants=mutants)
    else:
        g = Generator(SPACE, sizes=tuple(sizes), inputs=inputs, exact=exact)
    tasks, t0 = [], time.time()
    while len(tasks) < n:
        task = g.task(rng)
        if task is None:
            continue
        if dsl == "rearc":  # already a ldt.data.Task, solutions encoded
            task.name = f"{seed}-{len(tasks)}"
            tasks.append(task)
            continue
        tasks.append(Task(f"{seed}-{len(tasks)}", task.train, task.test,
                          [SPACE.encode(y) for y in task.solutions],
                          family=str(task.program)))
    os.makedirs(f"{VOL}/data/{name}", exist_ok=True)
    with open(f"{VOL}/data/{name}/shard-{seed:05d}.pkl", "wb") as f:
        pickle.dump(tasks, f)
    volume.commit()
    return {"seed": seed, "n": n, "sec": round(time.time() - t0, 1)}


@app.function(cpu=0.25, timeout=6 * 3600)
def generate_all(name: str, shards: int, per_shard: int, start: int = 0,
                 dsl: str = "1d", max_size: int = 20, exact: int = 0,
                 mutants: float = 0.5):
    """Every shard of a dataset, from inside Modal, so that no local client
    has to outlive the generation."""
    args = [(name, start + s, per_shard, (2, max_size), dsl, exact, mutants)
            for s in range(shards)]
    secs = [r["sec"] for r in generate_shard.starmap(args)]
    return {"shards": len(secs), "tasks": shards * per_shard,
            "mean_sec": sum(secs) / len(secs)}


@app.local_entrypoint()
def generate(name: str = "d1", shards: int = 8, per_shard: int = 100,
             start: int = 0, dsl: str = "1d", max_size: int = 20,
             exact: int = 0):
    print(json.dumps(generate_all.remote(name, shards, per_shard, start, dsl,
                                         max_size, exact)))


def load_shards(name: str, limit: int | None = None):
    import glob
    tasks = []
    for path in sorted(glob.glob(f"{VOL}/data/{name}/shard-*.pkl")):
        with open(path, "rb") as f:
            tasks.extend(pickle.load(f))
        if limit and len(tasks) >= limit:
            break
    return tasks


def _train(name, data, model_json, train_json, validation, eval_json,
           dsl="1d", benches="1darc", unseal=""):
    import torch
    from dataclasses import asdict
    from ldt.model import Config
    from ldt.train import TrainConfig, train as run_train
    from ldt.solve import solve, score
    SPACE, _ = signature(dsl)
    if dsl != "1d" and "1darc" in benches.split(","):
        raise ValueError(f"1darc is a 1D benchmark: pass --benches for {dsl}")
    out = f"{VOL}/runs/{name}"
    os.makedirs(out, exist_ok=True)
    volume.reload()
    tasks = load_shards(data)
    if dsl == "rearc":  # shards made before is_grid refused boolean cells
        from ldt.rearc import is_grid
        before = len(tasks)
        tasks = [t for t in tasks if all(
            is_grid(g) for pair in t.train + t.test for g in pair)]
        print(json.dumps({"dropped": before - len(tasks)}), flush=True)
    held = tasks[len(tasks) - validation:]
    tasks = tasks[:len(tasks) - validation]
    config = Config(**{"grid": "1d" if dsl == "1d" else "2d"}
                    | json.loads(model_json))
    tc = TrainConfig(**json.loads(train_json))
    logf = open(f"{out}/log.jsonl", "a")

    def log(msg):
        print(json.dumps(msg), flush=True)
        logf.write(json.dumps(msg) + "\n")
        logf.flush()

    log({"tasks": len(tasks), "held": len(held), "model": asdict(config),
         "train": asdict(tc), "gpu": torch.cuda.get_device_name()})

    def save(state):
        torch.save(state, f"{out}/model.pt")
        volume.commit()

    def validate(model, typing):
        if not held:
            return {}
        model.eval()
        sub = held[:128]
        res = solve(SPACE, typing, model, sub, chains=16, rounds=80, slots=32,
                    enough=1, augment=False)
        model.train()
        return score(sub, res) | {"mean_first_call": _mean(
            [r.first_call for r in res if r.first_call])}

    state = None
    if os.path.exists(f"{out}/model.pt"):  # a preempted or repeated run
        state = torch.load(f"{out}/model.pt", map_location="cuda")
    if state is not None and state["step"] >= tc.steps:
        from ldt.model import LDT
        log({"finished": state["step"]})
        typing = SPACE.typing().to("cuda")
        model = LDT(SPACE.n_positions, len(SPACE.vocab), config).to("cuda")
        model.load_state_dict(state["model"])
    else:
        model, typing = run_train(
            SPACE, tasks, config, tc, device="cuda", log=log,
            checkpoint=(500, save), resume=state,
            validate=(max(1000, tc.steps // 5), validate))
    model.eval()
    report = {"validation": validate(model, typing)}
    for bench in filter(None, benches.split(",")):
        report[bench] = run_benchmark(SPACE, typing, model, bench, eval_json,
                                      unseal, f"{out}/{bench}")
    log({"report": report})
    volume.commit()
    return report


def run_benchmark(space, typing, model, bench, eval_json, unseal, path,
                  prune=False):
    from ldt.solve import solve, score
    from ldt.abstract import Abstract, transformers_1d
    tasks = benchmark(bench, unseal)
    ev = json.loads(eval_json)
    # the refined transformers read 1D objects; 2D falls back to TOP
    transformers = transformers_1d() if bench == "1darc" else {}
    pruner = Abstract(space, transformers) if prune else None
    t0 = time.time()
    res = solve(space, typing, model, tasks, prune=pruner, **ev)
    out = score(tasks, res) | {"sec": round(time.time() - t0)}
    if bench == "1darc":
        out["families"] = families(tasks, res)
    out["first_call"] = _mean([r.first_call for r in res if r.first_call])
    out["calls"] = sum(r.calls for r in res)
    out["pruned"] = sum(r.pruned for r in res)
    with open(f"{path}.pkl", "wb") as f:
        pickle.dump([(r.name, {str(k): v for k, v in r.programs.items()},
                      r.attempts, r.first_call, r.calls) for r in res], f)
    return out


@app.function(gpu="H100", cpu=4.0, memory=16384, timeout=12 * 3600,
              volumes={VOL: volume})
def evaluate_remote(run: str, bench: str, eval_json: str, unseal: str = "",
                    prune: bool = False, uniform: bool = False,
                    dsl: str = "1d", tag: str = ""):
    """A trained run (or, with ``uniform``, the untrained control: no kill,
    uniform pins) on a benchmark."""
    import torch
    from ldt.model import LDT, Config
    SPACE, _ = signature(dsl)
    typing = SPACE.typing().to("cuda")
    model = None
    if not uniform:
        volume.reload()
        state = torch.load(f"{VOL}/runs/{run}/model.pt", map_location="cuda")
        model = LDT(SPACE.n_positions, len(SPACE.vocab),
                    Config(**state["config"])).to("cuda")
        model.load_state_dict(state["model"])
        model.eval()
    out = f"{VOL}/runs/{run}"
    os.makedirs(out, exist_ok=True)
    report = run_benchmark(SPACE, typing, model, bench, eval_json, unseal,
                           f"{out}/{bench}{tag}", prune)
    # one file per run, bench and tag, since concurrent appends from
    # containers overwrite: calls that run at once need distinct tags
    with open(f"{out}/eval-{bench}{tag}.json", "w") as f:
        json.dump({"bench": bench, "tag": tag, "prune": prune,
                   "uniform": uniform, "eval": json.loads(eval_json),
                   "report": report}, f)
    volume.commit()
    return report


@app.local_entrypoint()
def evaluate(run: str, bench: str = "1darc", unseal: str = "",
             prune: int = 0, uniform: int = 0, dsl: str = "1d", tag: str = "",
             evaluate: str = '{"chains": 32, "rounds": 100, "slots": 32}'):
    print(json.dumps(evaluate_remote.remote(
        run, bench, evaluate, unseal, bool(prune), bool(uniform), dsl, tag)))


def _mean(xs):
    return round(sum(xs) / len(xs), 1) if xs else None


def families(tasks, results):
    from ldt.solve import correct
    out = {}
    for t, r in zip(tasks, results):
        top1, pass2, _ = correct(t, r.attempts)
        row = out.setdefault(t.family, [0, 0, 0])
        row[0] += 1
        row[1] += top1
        row[2] += pass2
    return out


GPU = dict(cpu=4.0, memory=16384, timeout=24 * 3600, volumes={VOL: volume})


@app.function(gpu="L4", **GPU)
def train_l4(*args):
    return _train(*args)


@app.function(gpu="A10G", **GPU)
def train_a10g(*args):
    return _train(*args)


@app.function(gpu="A100", **GPU)
def train_a100(*args):
    return _train(*args)


@app.function(gpu="H100", **GPU)
def train_h100(*args):
    return _train(*args)


@app.local_entrypoint()
def train(name: str = "r0", data: str = "d1", gpu: str = "L4",
          model: str = "{}", steps: int = 1000, batch: int = 256,
          extra: str = "{}", validation: int = 512,
          evaluate: str = '{"chains": 32, "rounds": 100, "slots": 32}',
          dsl: str = "1d", benches: str = "1darc", unseal: str = ""):
    train_json = json.dumps({"steps": steps, "batch": batch}
                            | json.loads(extra))
    fn = globals()[f"train_{gpu.lower()}"]
    print(json.dumps(fn.remote(name, data, model, train_json, validation,
                               evaluate, dsl, benches, unseal)))


@app.function(volumes={VOL: volume}, timeout=600)
def read(path: str):
    """The bytes of a file on the volume, in chunks of 1 MiB: larger return
    values and volume downloads are blocked from the sandbox."""
    volume.reload()
    with open(f"{VOL}/{path}", "rb") as f:
        while chunk := f.read(1 << 20):
            yield chunk


@app.local_entrypoint()
def fetch(path: str, out: str = ""):
    data = b"".join(read.remote_gen(path))
    if out:
        with open(out, "wb") as f:
            f.write(data)
    else:
        print(data.decode())


@app.function(cpu=1.0, memory=4096, timeout=8 * 3600)
def enumerate_chunk(budget: int, start: int, stop: int, bench: str = "1darc",
                    dsl: str = "1d", unseal: str = ""):
    from ldt.enumerate import library, search
    from ldt.solve import correct
    SPACE, _ = signature(dsl)
    if dsl == "rearc":  # no enumeration of 160 untyped functions: a library
        from ldt.rearc import programs
        known = list(programs().values())
    out = []
    for task in benchmark(bench, unseal)[start:stop]:
        t0 = time.time()
        r = library(SPACE, task, known) if dsl == "rearc"\
            else search(SPACE, task, budget)
        top1, pass2, credit = correct(task, r.attempts)
        out.append({"name": task.name, "family": task.family,
                    "first": r.first_call, "found": len(r.programs),
                    "tried": r.calls, "sec": round(time.time() - t0, 2),
                    "top1": top1, "pass2": pass2, "credit": credit,
                    "program": str(next(iter(r.programs), ""))})
    return out


@app.function(cpu=0.25, timeout=12 * 3600, volumes={VOL: volume})
def enumerate_all(budget: int, bench: str = "1darc", dsl: str = "1d",
                  unseal: str = "", chunk: int = 10, name: str = ""):
    """The enumeration control on a benchmark, its rows saved on the volume
    as ``enum/<name>.json``."""
    n = len(benchmark(bench, unseal))
    args = [(budget, s, s + chunk, bench, dsl, unseal)
            for s in range(0, n, chunk)]
    rows = [r for rs in enumerate_chunk.starmap(args) for r in rs]
    summary = {"bench": bench, "dsl": dsl, "budget": budget,
               "tasks": len(rows), "top1": sum(r["top1"] for r in rows),
               "pass2": sum(r["pass2"] for r in rows),
               "pass2_outputs": round(sum(r["credit"] for r in rows), 2),
               "found": sum(r["found"] > 0 for r in rows)}
    os.makedirs(f"{VOL}/enum", exist_ok=True)
    with open(f"{VOL}/enum/{name or bench + '-' + str(budget)}.json",
              "w") as f:
        json.dump({"summary": summary, "rows": rows}, f)
    volume.commit()
    return summary


@app.local_entrypoint()
def enumerate_arc(budget: int = 100000, bench: str = "1darc",
                  dsl: str = "1d", unseal: str = ""):
    """The enumeration control on a benchmark."""
    print(json.dumps(enumerate_all.remote(budget, bench, dsl, unseal)))


@app.function(cpu=1.0, timeout=300)
def probe():
    """Whether the time limit on programs holds in a container, as it must
    before a sealed read: it needs the main thread."""
    import threading
    from ldt.bohm import Undefined
    from ldt.straight import Program, Statement, StraightSpace
    space = StraightSpace({"spin": lambda a: [a for _ in iter(int, 1)]}, {},
                          statements=1, arity=1, seconds=0.5)
    start = time.time()
    try:
        space.compile(Program([Statement("spin", ("I", ))]))(1)
    except Undefined:
        pass
    return {"main_thread":
            threading.current_thread() is threading.main_thread(),
            "stopped_after": round(time.time() - start, 2)}
