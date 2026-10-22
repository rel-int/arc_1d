"""
Modal entry points: synthetic data on CPUs, training and evaluation on a GPU.

Everything lands on the volume ``ldt-arc``; results come back as return values
because ``modal volume get`` is blocked from the agents' sandbox.

    modal run modal_app.py::generate --name d1 --shards 200 --per-shard 500
    modal run --detach modal_app.py::train --name r1 --data d1 --gpu L4
    modal run modal_app.py::fetch --path runs/r1/log.jsonl
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
    .add_local_python_source("ldt")
)
app = modal.App("ldt-arc", image=image)
volume = modal.Volume.from_name("ldt-arc", create_if_missing=True)
VOL = "/vol"


@app.function(cpu=1.0, memory=2048, timeout=3600, volumes={VOL: volume})
def generate_shard(name: str, seed: int, n: int, sizes=(2, 20)):
    import random
    from ldt.dsl1d import SPACE
    from ldt.synth import Generator
    from ldt.data import Task
    rng = random.Random(seed)
    g = Generator(SPACE, sizes=tuple(sizes))
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
             start: int = 0):
    args = [(name, start + s, per_shard) for s in range(shards)]
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


def _train(name, data, model_json, train_json, validation, eval_json):
    import torch
    from dataclasses import asdict
    from ldt.dsl1d import SPACE
    from ldt.model import Config
    from ldt.train import TrainConfig, train as run_train
    from ldt.data import load_1darc
    from ldt.solve import solve, score
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
    ev = json.loads(eval_json)
    model.eval()
    report = {"validation": validate(model, typing)}
    arc = load_1darc("/data/1D-ARC")
    t0 = time.time()
    res = solve(SPACE, typing, model, arc, **ev)
    report["1darc"] = score(arc, res) | {"sec": round(time.time() - t0)}
    report["1darc_families"] = families(arc, res)
    report["1darc_first_call"] = _mean([r.first_call for r in res
                                        if r.first_call])
    with open(f"{out}/predictions.pkl", "wb") as f:
        pickle.dump([(r.name, {str(k): v for k, v in r.programs.items()},
                      r.attempts, r.first_call, r.calls) for r in res], f)
    log({"report": report})
    volume.commit()
    return report


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
          evaluate: str = '{"chains": 32, "rounds": 100, "slots": 32}'):
    train_json = json.dumps({"steps": steps, "batch": batch}
                            | json.loads(extra))
    fn = globals()[f"train_{gpu.lower()}"]
    print(json.dumps(fn.remote(name, data, model, train_json, validation,
                               evaluate)))


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
