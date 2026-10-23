# Lattice deduction over the Scott domain of Böhm trees

The Lattice Deduction Transformer ([arXiv 2605.08605](https://arxiv.org/abs/2605.08605)) solves a
puzzle by descending a lattice of partial information, `positions → P(labels)`: a recurrent
transformer kills the labels it deduces impossible, a search pins one position when deduction stalls,
and training runs that same loop on-policy against the paper's α, the labels used by the solutions
still consistent with the state. Its own limitations section reports that a direct port to ARC, over
output grids, plateaus at about 36% because the conflict head becomes unreliable, and suggests
"a different abstract domain entirely: one over the programs that produce solutions".

This directory is that domain. A solution is a **program**: the Böhm tree of a closed, simply-typed
λ-term `G → G` over a signature of grid primitives.

## The construction

**Positions and labels.** A Böhm tree in η-long β-normal form is a head (a primitive, or a bound
variable by de Bruijn level) applied to the trees of its arguments; the node's type fixes its binders,
so a node is its head alone. Trees live on the complete `arity`-ary tree of `depth` levels in heap order
(`ldt/bohm.py`): 364 addresses for depth 6 and arity 3, each labelled by a head or `·` (no node).

**The lattice.** A state is a candidate set of heads per address, ordered by inclusion. Partial Böhm
trees — `Ω` for an unknown subtree — ordered by Ω-refinement form a Scott domain, and they sit in the
lattice as the states with a singleton at each defined node and every label below each `Ω`. LDT's
branching step "pin one position" is then exactly forcing one argument of a lazy Böhm tree
(`closed.BohmTree.__getitem__` in discopy-next), restricted to the frontier of the decided part
(`ldt.lattice.frontier`); the learned kills are the states in between.

**Three deduction operators, one learned.**

1. *Types, exact.* η-long normal forms of a type are a regular tree language: a top-down automaton
   whose states are `(type, context)`. Arc consistency on the tree (one bottom-up and one top-down
   pass, `Space.propagate`, batched on the GPU in `ldt.lattice.Typing`) intersects a state with it and
   projects back exactly, `α(γ(a) ∩ WellTyped)`, after every kill and every pin.
2. *Semantics, learned.* The transformer reads the state and the demonstrations and emits a kill logit
   per label and a conflict logit, trained with the paper's loss against α over the programs
   consistent with the demonstrations. Programs make that set huge (`shift(n0, o)` is `o`), so the
   generator cuts it by Occam's razor: the program is shrunk to a locally minimal one, and α runs over
   it and its no-larger one-edit variants (`ldt/synth.py`).
3. *Verification, exact.* A total tree is run on the demonstrations; only a consistent program is ever
   an answer. Soundness never rests on the network, which is where the output-lattice port failed.
   Before a tree is total, **abstract evaluation** (`ldt/abstract.py`) runs the partial tree with each
   `Ω` as the top of the output lattice — sets of colours per cell — and restarts a chain whose
   demonstration outputs fall outside, a sound conflict found early. Evaluation is Scott-continuous, so
   this is the link between the program lattice and the paper's output lattice.

**Reference semantics.** `ldt/discopy_bridge.py` maps every tree to a `discopy.closed` term with the
signature as free variables, reduces it with `closed.LeftmostOutermost` and reads the `BohmTree` back;
evaluation by `closed.Functor` into `python.Function` agrees with the fast interpreter of
`Space.compile` (`tests/test_discopy.py`).

## Running it

```shell
uv run pytest                                   # discopy tests need the [discopy] extra
modal run modal_app.py::generate --name d1 --shards 200 --per-shard 500
modal run --detach modal_app.py::train --name r1 --data d1 --gpu H100 --steps 20000
modal run modal_app.py::evaluate --run r1 --prune 1 --evaluate '{"free": 0.5}'
modal run modal_app.py::enumerate_arc --budget 1000000
```

The evaluation splits of ARC-AGI-1 and ARC-AGI-2 are sealed (`ldt/arc.py`); each read is logged in
`EVALUATION.md`.

## Results

1D-ARC (Xu et al., 2023): 901 tasks in 18 families, 3 demonstrations and 1 test each, pass@2. The 1D
signature (`ldt/dsl1d.py`, 25 primitives and 16 constants) was written after reading one example per
family, so its ceiling is 901/901 by construction: what is measured is search, not coverage.

| method | pass@2 | cost |
|---|---:|---|
| enumeration by size, 10⁴ programs per task | 451 | 0.08 CPU core-hours |
| enumeration by size, 10⁵ | 460 | 0.9 |
| enumeration by size, 10⁶ | 502 | 9 |
| untrained Scott-domain search: no kill, uniform pins, ≤ 3,200 calls per task | 266 | 44 s on one H100 |
| LDT pilot, 3k steps (15 min on one H100), ≤ 3,200 model calls per task | 388 | ~$1 + 11 min |
| the same model, half the chains kill-free | 482 | 8 min |
| the same, with abstract pruning (19,321 chains restarted early) | 482 | 9 min |
| **LDT r1, 20k steps (1.5 h on one H100, ~$6), half the chains kill-free** | **514** | 7.4 min, 222 calls to the first program |

Per family, r1 against enumeration at 10⁶ programs: equal on the eleven families both nearly
saturate; ahead on `recolor_oe` (50 against 0: the program, 11 nodes with a parity test, is beyond
10⁶ programs in size order), `scale_dp` (6 against 4) and `recolor_cmp` (3 against 0); behind on
`mirror` (0 against 41), whose program nests a second binder (`pick`'s predicate inside
`map_segs`'s), and `move_2p_dp` (4 against 5). Neither solves `pcopy_*` or `recolor_cnt`, whose
programs have 10 to 19 nodes.

The two searches fail differently: 452 tasks are solved by both, 62 by the LDT alone and 50 by
enumeration alone. The fixed policy "the LDT, then enumeration at 10⁶ when the LDT finds no program"
solves **564**. For scale, the DreamCoder of arc_1d#2 reaches 677–682 with learned boxes and 842 with
three hand-written ones, and GPT-4 on object representations 755 (Xu et al.): neither search here
reaches the 10–19-node programs that `pcopy_*` and `recolor_cnt` need.

Kill-free chains are what an unsound kill needs: the pilot learned to kill the right shift constant
in `move_2p`/`move_3p` (12 and 10 of 50), and with half its chains only ordering pins they come back
to 47 and 48. Abstract pruning is sound but, with the 1D transformers as coarse as they are, changes
no outcome.

### ARC-AGI

The 2D signature (`ldt/dsl2d.py`, 75 primitives over grids, objects, numbers, colours, booleans and
directions) was written against ARC-AGI-1 training. pass@2, two attempts per test input:

| method | ARC-AGI-1 training (400) | ARC-AGI-1 evaluation (400) | ARC-AGI-2 evaluation (120) |
|---|---:|---:|---:|
| enumeration by size, 2×10⁴ programs per task (sizes ≤ 4) | 36 | **7** | **0** |
| enumeration by size, 10⁵ (sizes ≤ 5) | 46 | — | — |
| untrained Scott-domain search, 3,200 calls per task | 7 | — | — |
| LDT r2d (one-edit α, 12k steps) | 21 | — | — |
| LDT r2d3 (exact α, 20k steps, ~$8), 3,200 calls per task | 25–27 | **3** | **0** |

Each evaluation number is one read, logged in `EVALUATION.md` before it ran. The LDT's three
ARC-AGI-1 evaluation tasks (`connect`, `upscale(n2)`, `symmetrize`) are among enumeration's seven.

Two things limit 2D, and the second is the one to fix first. The signature reaches about 10% of
ARC-AGI-1 training and 2% of its evaluation even by exhaustive search, so the ceiling is the DSL. And
the 2D model learns slowly: its kills stay unsound on about half the training steps, where 1D's fall
to a fifth. Part of that was the α target: in 2D most programs have equivalent rewrites
(`rot90 ∘ flip_h = rot180 ∘ transpose`), and α over one-edit variants labels them wrong. Exact α
(every minimal consistent program up to size 5) took validation from 4 to 6–8 of 128 held-out tasks
and halved the calls to a first program, but did not close the gap to enumeration.
