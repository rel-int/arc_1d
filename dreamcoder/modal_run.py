"""
The default run on Modal, on CPU or GPU, from the same image and lock.

    modal run --detach modal_run.py --name batched-l4 --machine l4 --args "--batched --device cuda"
    modal run --detach modal_run.py --name cpu-4 --machine cpu4
    modal run modal_run.py::fetch --name gpu-l4     # results/<name>/ back on disk

Each run writes ``results/<name>/`` to the ``arc-1d-dreamcoder`` volume, and
``fetch`` returns it as a tarball without the checkpoints, since neither
``modal volume get`` nor a large return value, which Modal hands over as a
download, is reachable from every sandbox.
"""

from __future__ import annotations

import io
import shlex
import subprocess
import tarfile
import time
from pathlib import Path

import modal

HERE = Path(__file__).parent
VOLUME = modal.Volume.from_name("arc-1d-dreamcoder", create_if_missing=True)
image = (
    modal.Image.debian_slim(python_version="3.13")
    .apt_install("git")
    .uv_sync(str(HERE), frozen=True)
    .add_local_dir(HERE / "dc", "/root/dreamcoder/dc", copy=True)
    .workdir("/root/dreamcoder")
    .run_commands("python -c 'from pathlib import Path; from dc import data; data.fetch(Path(\"data\"))'")
)
app = modal.App("arc-1d-dreamcoder", image=image)


def run(name: str, args: str) -> dict:
    out = Path("/results") / name
    command = ["python", "-m", "dc.run", "--out", str(out), "--resume", *shlex.split(args)]
    start = time.time()
    with open(Path("/results") / f"{name}.log", "a") as log:
        subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
    seconds = time.time() - start
    (out / "wall.txt").write_text(f"{seconds:.1f}\n")
    VOLUME.commit()
    return dict(name=name, seconds=seconds)


@app.function(volumes={"/results": VOLUME}, cpu=4, timeout=6 * 3600)
def cpu4(name: str, args: str) -> dict:
    return run(name, args)


@app.function(volumes={"/results": VOLUME}, cpu=16, timeout=6 * 3600)
def cpu16(name: str, args: str) -> dict:
    return run(name, args)


@app.function(volumes={"/results": VOLUME}, gpu="L4", cpu=4, timeout=6 * 3600)
def l4(name: str, args: str) -> dict:
    subprocess.run(["nvidia-smi", "-L"])
    return run(name, args)


@app.function(volumes={"/results": VOLUME}, gpu="A100", cpu=4, timeout=6 * 3600)
def a100(name: str, args: str) -> dict:
    subprocess.run(["nvidia-smi", "-L"])
    return run(name, args)


@app.function(volumes={"/results": VOLUME})
def fetch_remote(name: str) -> bytes:
    VOLUME.reload()
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for path in (Path("/results") / name, Path("/results") / f"{name}.log"):
            if path.exists():
                tar.add(path, arcname=path.name, filter=lambda info: None if info.name.endswith(".pkl") else info)
    return buffer.getvalue()


@app.function(volumes={"/results": VOLUME}, timeout=3600)
def selection_remote(names: list[str]) -> dict:
    """
    Every selector on the kept candidates of each run's last iteration, read
    from its checkpoint: test pairs hit, over all tasks, the even-numbered
    ones and the odd-numbered ones, so a selector chosen on one half can be
    reported on the other.
    """
    import pickle
    from dc import data
    from dc.select import SELECTORS, select
    tasks = {t.name: t for t in data.load(Path("data"))}
    half = lambda name: "even" if int(name.rsplit("_", 1)[1]) % 2 == 0 else "odd"
    found = {}
    for name in names:
        _, _, _, results = pickle.loads((Path("/results") / name / "checkpoint.pkl").read_bytes())
        hits = {rule: {"all": 0, "even": 0, "odd": 0} for rule in (*SELECTORS, "kept")}
        for task_name, solutions in results.items():
            answer = tasks[task_name].test[1]
            for rule in SELECTORS:
                hit = select(solutions, rule)[0].test_prediction == answer
                hits[rule]["all"] += hit
                hits[rule][half(task_name)] += hit
            hit = any(s.test_prediction == answer for s in solutions)
            hits["kept"]["all"] += hit
            hits["kept"][half(task_name)] += hit
        found[name] = hits
    return found


@app.local_entrypoint()
def selection(names: str):
    """``--names lib-s0,ctl-s0``: a table of every selector on each run."""
    found = selection_remote.remote(names.split(","))
    rules = list(next(iter(found.values())))
    print("| run | " + " | ".join(rules) + " |")
    print("|---|" + "---|" * len(rules))
    for name, hits in found.items():
        cells = [f"{h['all']} ({h['even']} + {h['odd']})" for h in hits.values()]
        print(f"| {name} | " + " | ".join(cells) + " |")


@app.local_entrypoint()
def main(name: str, machine: str = "cpu4", args: str = ""):
    function = {"cpu4": cpu4, "cpu16": cpu16, "l4": l4, "a100": a100}[machine]
    print(function.remote(name, args))


@app.local_entrypoint()
def fetch(name: str, target: str = ""):
    target = Path(target) if target else HERE / "results"
    with tarfile.open(fileobj=io.BytesIO(fetch_remote.remote(name)), mode="r:gz") as tar:
        tar.extractall(target, filter="data")
    print(f"fetched results/{name}")
