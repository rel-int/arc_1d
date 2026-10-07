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
