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
