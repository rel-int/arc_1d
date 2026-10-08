# A diagrammatic DreamCoder on 1D-ARC

A feasibility run: can a wake/abstract loop over string diagrams, with no LLM
anywhere, solve 1D-ARC tasks and grow a useful library?

- **Programs** are DisCoPy string diagrams `Grid -> Grid` over a library of
  typed boxes, each box a small PyTorch module (`dc/library.py`).
- **Semantics** is a functor from the free Markov category on the library
  into PyTorch modules: `discopy.neural.network.Functor` puts a fresh module
  in every box, `discopy.neural.torch.Module` compiles the image
  (`dc/semantics.py`). It sits behind `Semantics.model(term, library)`, which
  is all the search calls.
- **Wake** enumerates type-correct terms up to a size bound in order of their
  prior, fits each one's weights on the task's training pairs, and scores it
  by description length = structure + parameters + training data, in bits
  (`dc/wake.py`).
- **Abstract** mines the subdiagrams shared by the best solutions and adds the
  top few as new boxes, carrying their trained weights (`dc/abstract.py`).

The test pair of every task is held out: it is only ever predicted.

## Run

```shell
uv sync
uv run python -m dc.run --quick   # smoke test: 36 tasks, 2 iterations, ~1.5 min on 4 cores
uv run python -m dc.run           # default: 180 tasks, 3 iterations, see the PR for timing
uv run pytest                     # type-checking and the functor on hand-built diagrams
```

The data is cloned on first run from
[khalil-research/1D-ARC](https://github.com/khalil-research/1D-ARC) at a
pinned commit into `data/`. Results go to `results/<quick|default>/`:
`report.md`, `history.json`, `config.json` and the drawn diagrams. Every
option of `dc.wake.Config` is a flag, e.g. `--per-family 0` for all 901 tasks,
`--iterations 5`, `--workers 8`.

`discopy.neural` is not on DisCoPy's `main` yet: `pyproject.toml` pins the
head of [discopy#743](https://github.com/discopy/discopy/pull/743) (`Network`
and its PyTorch compile), stacked on #736 and #701.

## Run on Modal

```shell
pip install "modal[api-proxy-support]"   # the extra is what a sandbox behind a proxy needs
modal run --detach modal_run.py::main --name default-cpu16 --machine cpu16 --args "--workers=16"
modal run --detach modal_run.py::main --name default-l4 --machine l4 --args "--workers=4 --device=cuda"
modal run modal_run.py::fetch --name default-cpu16   # results/default-cpu16/ back on disk
```

One image from `uv.lock` for every machine, the dataset baked in. `--device cuda`
makes the pool spawn its workers rather than fork them, since CUDA does not
survive a fork.

**Use CPUs, not a GPU.** Each candidate is a model of a few hundred parameters
fitted on three grids of at most 93 cells, so every step is a handful of tiny
kernels and a GPU spends its time launching them. The default run, 180 tasks:

| run | machine | top-1, iterations 0/1/2 | wall-clock |
|---|---|---|---|
| `default` (committed, before early stopping) | 4 cores, agent sandbox | 81 / 99 / 101 | 2,994 s |
| `pr-cpu16` (`--stop-bits -1`, the same code) | Modal, 16 cores | 79 / 101 / 103 | 849 s |
| `default-cpu4` (head) | Modal, 4 cores | 76 / 88 / 98 | 2,380 s (422 / 948 / 1,000) |
| `default-cpu16` (head) | Modal, 16 cores | 76 / 88 / 98 | 761 s (135 / 298 / 316) |
| `default-l4` (head) | Modal, L4 + 4 cores | 76 / – / – | iteration 0 alone 1,580 s |

The L4 finds what 4 cores find, task for task, 3.7× slower (3.0× on
`--quick`); it was preempted in iteration 1 and stopped there. Cores scale
nearly linearly, 3.1× from 4 to 16. Results are not bit-reproducible across
machines: with the committed code on another CPU, 8 of 180 best terms already
differ at iteration 0, and the top-1 counts land within two tasks.
