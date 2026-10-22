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

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git")
    .pip_install("numpy>=2.0", "torch==2.14.1")
    .run_commands(
        "git clone https://github.com/khalil-research/1D-ARC /data/1D-ARC",
        f"cd /data/1D-ARC && git checkout {COMMIT}")
    .add_local_dir("/home/user/ARC-AGI/data", "/data/ARC-AGI/data")
    .add_local_dir("/home/user/ARC-AGI-2/data", "/data/ARC-AGI-2/data")
    .add_local_python_source("ldt")
)
app = modal.App("ldt-arc", image=image)
volume = modal.Volume.from_name("ldt-arc", create_if_missing=True)
VOL = "/vol"


def signature(dsl: str):
    """The space of a signature and its input sampler."""
    if dsl == "1d":
        from ldt.dsl1d import SPACE
        return SPACE, None
    from ldt.dsl2d import SPACE
    from ldt import synth2d
    return SPACE, (synth2d.random_style, synth2d.random_grid)


def benchmark(bench: str, unseal: str = ""):
    from ldt.data import load_1darc
    from ldt import arc
    if unseal:
        os.environ[arc.UNSEAL] = unseal
    if bench == "1darc":
        return load_1darc("/data/1D-ARC")
    root = {"arc1": "/data/ARC-AGI", "arc2": "/data/ARC-AGI-2"}[bench[:4]]
    return arc.load(root, bench.split("-", 1)[1])


@app.function(cpu=1.0, memory=2048, timeout=3600, volumes={VOL: volume})
def generate_shard(name: str, seed: int, n: int, sizes=(2, 20),
                   dsl: str = "1d"):
    import random
    from ldt.synth import Generator
    from ldt.data import Task
    SPACE, inputs = signature(dsl)
    rng = random.Random(seed)
    g = Generator(SPACE, sizes=tuple(sizes), inputs=inputs)
    tasks, t0 = [], time.time()
    while len(tasks) < n:
        task = g.task(rng)
        if task is None:
            continue
        tasks.append(Task(f"{seed}-{len(tasks)}", task.train, task.test,
                          [SPACE.encode(y) for y in task.solutions],
                          family=str(task.program)))
    os.makedirs(f"{VOL}/data/{name}", exist_ok=True)
    with open(f"{VOL}/data/{name}/shard-{seed:05d}.pkl", "wb") as f:
        pickle.dump(tasks, f)
    volume.commit()
    return {"seed": seed, "n": n, "sec": round(time.time() - t0, 1)}


@app.local_entrypoint()
def generate(name: str = "d1", shards: int = 8, per_shard: int = 100,
             start: int = 0, dsl: str = "1d", max_size: int = 20):
    args = [(name, start + s, per_shard, (2, max_size), dsl)
            for s in range(shards)]
    secs = [r["sec"] for r in generate_shard.starmap(args)]
    print(json.dumps({"shards": len(secs), "tasks": shards * per_shard,
                      "mean_sec": sum(secs) / len(secs)}))


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
    out = f"{VOL}/runs/{name}"
    os.makedirs(out, exist_ok=True)
    tasks = load_shards(data)
    held = tasks[-validation:]
    tasks = tasks[:-validation]
    config = Config(**json.loads(model_json))
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
        model.eval()
        sub = held[:128]
        res = solve(SPACE, typing, model, sub, chains=16, rounds=40, slots=32,
                    enough=1, augment=False)
        model.train()
        return score(sub, res) | {"mean_first_call": _mean(
            [r.first_call for r in res if r.first_call])}

    resume = None
    if os.path.exists(f"{out}/model.pt"):  # a preempted run of this name
        state = torch.load(f"{out}/model.pt", map_location="cuda")
        if "optimizer" in state and state["step"] < tc.steps:
            resume = state
    model, typing = run_train(SPACE, tasks, config, tc, device="cuda",
                              log=log, checkpoint=(500, save),
                              validate=(max(1000, tc.steps // 5), validate),
                              resume=resume)
    save({"model": model.state_dict(), "config": asdict(config),
          "train": asdict(tc), "step": tc.steps})
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
    pruner = Abstract(space, transformers_1d()) if prune else None
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
    from ldt.lattice import Typing
    from ldt.model import LDT, Config
    SPACE, _ = signature(dsl)
    typing = Typing(SPACE).to("cuda")
    model = None
    if not uniform:
        state = torch.load(f"{VOL}/runs/{run}/model.pt", map_location="cuda")
        model = LDT(SPACE.n_positions, len(SPACE.vocab),
                    Config(**state["config"])).to("cuda")
        model.load_state_dict(state["model"])
        model.eval()
    out = f"{VOL}/runs/{run}"
    os.makedirs(out, exist_ok=True)
    report = run_benchmark(SPACE, typing, model, bench, eval_json, unseal,
                           f"{out}/{bench}{tag}", prune)
    with open(f"{out}/eval.jsonl", "a") as f:
        f.write(json.dumps({"bench": bench, "tag": tag, "prune": prune,
                            "uniform": uniform, "eval": json.loads(eval_json),
                            "report": report}) + "\n")
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
    out = {}
    for t, r in zip(tasks, results):
        truth = tuple(y for _, y in t.test)
        row = out.setdefault(t.family, [0, 0, 0])
        row[0] += 1
        row[1] += bool(r.attempts) and r.attempts[0] == truth
        row[2] += truth in r.attempts[:2]
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


@app.function(cpu=1.0, memory=2048, timeout=8 * 3600)
def enumerate_chunk(budget: int, start: int, stop: int):
    from ldt.dsl1d import SPACE
    from ldt.data import load_1darc
    from ldt.enumerate import search
    out = []
    for task in load_1darc("/data/1D-ARC")[start:stop]:
        t0 = time.time()
        r = search(SPACE, task, budget)
        truth = tuple(y for _, y in task.test)
        out.append({"name": task.name, "family": task.family,
                    "first": r.first_call, "found": len(r.programs),
                    "tried": r.calls, "sec": round(time.time() - t0, 2),
                    "top1": bool(r.attempts) and r.attempts[0] == truth,
                    "pass2": truth in r.attempts[:2],
                    "program": str(next(iter(r.programs), ""))})
    return out


@app.local_entrypoint()
def enumerate_arc(budget: int = 100000, chunk: int = 10, out: str = ""):
    """The enumeration control on all 901 tasks of 1D-ARC."""
    args = [(budget, s, s + chunk) for s in range(0, 901, chunk)]
    rows = [r for rs in enumerate_chunk.starmap(args) for r in rs]
    summary = {"budget": budget, "tasks": len(rows),
               "top1": sum(r["top1"] for r in rows),
               "pass2": sum(r["pass2"] for r in rows),
               "found": sum(r["found"] > 0 for r in rows)}
    print(json.dumps(summary))
    if out:
        with open(out, "w") as f:
            json.dump({"summary": summary, "rows": rows}, f)
