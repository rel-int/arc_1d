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
modal run --detach modal_run.py::main --name batched-l4 --machine l4 --args "--batched --device=cuda"
modal run modal_run.py::fetch --name default-cpu16   # results/default-cpu16/ back on disk
```

One image from `uv.lock` for every machine, the dataset baked in. Without
`--batched`, `--device cuda` makes the pool spawn its workers rather than
fork them, since CUDA does not survive a fork.

**Batch on a GPU.** Each candidate is a model of a few hundred parameters
fitted on three grids of at most 93 cells, so fitted one task at a time a GPU
spends its time launching tiny kernels, and is slower than the CPU. `--batched`
fits one candidate on every task at once instead: its parameters stacked
along a task axis, the forward pass vmapped over tasks padded to one length,
one Adam over the stack, which is one Adam per task. Padding is exact
(`tests/test_batch.py`): every box producing a `Grid` puts background back
outside the grid and `reflect` reverses the grid cells alone.

| run | machine | top-1, iterations 0/1/2 | wake, iterations 0/1/2 | total |
|---|---|---|---|---|
| default, per task | Modal, 4 cores | 76 / 88 / 98 | 422 / 948 / 1,000 s | 2,380 s |
| default, per task | Modal, 16 cores | 76 / 88 / 98 | 135 / 298 / 316 s | 761 s |
| default, per task | Modal, L4 | 76 / – / – | 1,580 s / – / – | preempted |
| default, `--batched` | Modal, 4 cores | 77 / 90 / 91 | 151 / 357 / 346 s | 862 s |
| default, `--batched` | Modal, **L4** | 76 / 91 / 96 | 61 / 130 / 143 s | **342 s** |
| 901 tasks, size 5, per task | 4 cores, agent sandbox | 538 / 571 / 571 | 8,667 / 10,141 / 11,037 s | 8.3 h |
| 901 tasks, size 5, `--batched` | Modal, **L4** | 538 / 569 / 575 | 473 / 559 / 621 s | **27.6 min** |
| 901 tasks, size 5, `--batched` | Modal, **A100** | 538 / 567 / 571 | 345 / 370 / 402 s | **18.6 min** |

The batched L4 is 7× the 4 cores on the default and 18× on the 901 tasks;
the A100 27×. The more tasks a batch carries, the more the GPU wins.

**Iteration 0 is the only one to compare exactly.** Every run starts from the
same library and agrees there, within a task. After it, the runs drift apart
by a few tasks: Adam divides a gradient by its own magnitude, so where the
true gradient of a parameter is zero, rounding of order 1e-12 becomes a step
of order 1e-6, which the parameter code's thresholds then turn into whole
bits, and the learned boxes inherit the medoid of those weights. Two machines
running the same per-task code already differ on 8 of 180 best terms at
iteration 0 (`pr-cpu16` against the committed `default`, which predates early
stopping, reproduced with `--stop-bits -1`). So top-1 counts at iterations 1
and 2 carry a noise of about ±4 of 180, which is the size of the gaps the
library is being judged on.

## Restarts, leave-one-out, and does the library help?

`--restarts R` fits each candidate from R starts, restart 0 at the prior and
the others perturbed from it by noise seeded by `(seed, iteration, term)`;
each task keeps the start of least DL. `--select loo` fits each of the `keep`
candidates of least DL once more per training pair, on the other two, and
re-ranks them by how many held-out pairs they predict, ties by DL. Both need
`--batched`. `python -m dc.compare` puts groups of seeds side by side.

All 901 tasks, size ≤ 5 by quotas `3:57,4:50,5:43`, 4 restarts, leave-one-out
over the 10 kept, seeds 0/1/2, one L4 each; the **library** adds two boxes per
iteration, the **control** (`--new-boxes 0`) has the same candidate budget and
re-estimates its grammar but learns no box:

| run | iteration | top-1 (leave-one-out) | top-1 (least DL) | any of the 10 kept | fit train exactly | mean DL |
|---|---|---|---|---|---|---|
| reference: 1 start, least DL | 0 / 2 | – | 538 / 571 | – | 629 / 665 | 76.4 / 76.9 |
| library | 0 | 662.7 ± 3.1 | 639.3 ± 8.5 | 764.7 ± 4.7 | 794.0 ± 4.4 | 65.4 |
| library | 1 | 667.7 ± 17.0 | 645.0 ± 19.2 | 768.3 ± 2.1 | 784.7 ± 7.6 | 65.2 |
| library | 2 | **682.3 ± 13.3** | 664.7 ± 18.1 | 771.0 ± 6.6 | 790.0 ± 4.4 | 61.1 |
| control | 1 | 668.3 ± 11.7 | 647.3 ± 13.3 | 768.7 ± 2.9 | 780.0 ± 6.6 | 66.1 |
| control | 2 | **677.0 ± 10.6** | 651.7 ± 12.5 | 768.0 ± 1.0 | 789.3 ± 4.2 | 64.5 |

- **Restarts are the big win**: with one start, 629 tasks fit their training
  pairs; with four, 794. Top-1 by least DL goes from 538 to 639 at iteration 0.
- **Leave-one-out adds 23 more** (639 → 663) at no search cost, but the kept
  candidates contain a right answer on ~765 tasks: selection still loses ~100.
- **The library does not beat the control on the test pairs**: 682 ± 13 against
  677 ± 11 at iteration 2, per seed 0, +18 and −2. It does compress (mean
  DL 61.1 against 64.5), and iteration 0, where the two runs are the same,
  agrees within a task.
- **Seeds matter after iteration 0**: ± 3 at iteration 0 but ± 11–19 after,
  since the re-estimated grammar picks the next iteration's 150 candidates
  from what the last one solved. Judging any change on one seed is not enough.

Each run took 1.6–1.9 h on an L4: four starts plus the leave-one-out fits cost
about 4× the single-start run.
