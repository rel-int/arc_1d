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
`Space.compile` wherever it is defined (`tests/test_discopy.py`). It is call by value, so it raises on
an undefined `ite` branch that `Space.compile` never takes.

## Running it

```shell
REARC=/path/to/re-arc ARC_AGI_ROOT=/path/to/ARC-AGI uv run --extra dev --extra discopy pytest
modal run modal_app.py::generate --name d1 --shards 200 --per-shard 500
modal run --detach modal_app.py::train --name r1 --data d1 --gpu H100 --steps 20000
modal run modal_app.py::evaluate --run r1 --prune 1 --evaluate '{"free": 0.5}'
modal run modal_app.py::enumerate_arc --budget 1000000
```

Without `REARC` and `ARC_AGI_ROOT` the tests that read re-arc and ARC-AGI skip. The evaluation splits of ARC-AGI-1 and ARC-AGI-2 are sealed (`ldt/arc.py`); each read is logged in
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
no outcome. Its 19,321 restarts were counted before `join` learnt to tell 1D objects from grids,
which prunes a little more (91 against 87 of 223 sampled partial `ite` trees).

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

### arc-dsl: straight-line programs, re-arc supervision

The ceiling above was the hand-written DSL. The second round takes Hodel's arc-dsl as the signature
(160 functions, 28 constants) and writes programs as its solvers are written: straight-line
statements `x_i = f(a, ...)` with atomic arguments, i.e. Böhm trees with sharing (`ldt/straight.py`).
Positions are 32 statements × (head + 4 arguments); the structure is a star (the program's length is
shared, each statement independent given it), so the projection is exact arc consistency on it,
checked against brute force. There is no typing projection: arc-dsl's annotations are too loose to be
sound, so typing is left to the network and to execution.

Supervision is re-arc (`ldt/rearc.py`): its 1,000 generated examples per ARC-AGI-1 training task,
each kept by re-arc only if the task's verifier reproduces it, with the verifier — a straight-line
arc-dsl program, parsed from source, canonicalised — as the target. 295 of the 400 fit 32 statements
in this round; 298 do since the canonical form writes a repeated statement once.
Each draw is a verifier task or, with probability one half, a one-edit mutant of a verifier run on
that task's inputs: a program near the ARC distribution that no training task uses. Most mutants are
undefined and the draw starts again, so about one task in ten is a mutant. r4b's data (d4) was drawn
with probability 0.7 and before mutants giving the verifier's own outputs were dropped: 177 of the
400 tasks of its first shard are mutants, 112 of them giving the verifier's outputs.

The control is the **library**: every one of the 295 verifiers run as it is. A solution the LDT finds
and the library does not is a program no training task gives. These are the round's numbers: the
current code builds 298 verifiers, which solve 297 of ARC-AGI-1 training (3ac3eb23, 57aa92db and
c8cbb738 join); the evaluation columns were read with the round's code, and a rerun would be a new
read.

| method | held-out re-arc (128) | ARC-AGI-1 training (400) | ARC-AGI-1 evaluation (400) | ARC-AGI-2 evaluation (120) |
|---|---:|---:|---:|---:|
| untrained Scott-domain search, 5,120 calls per task | — | 0 | — | — |
| library: 295 verifiers as they are | — | 294 | **21** | **0** |
| LDT r4b (20k steps, ~1.2 h on one H100), 32 chains × 160 rounds | 108 | 54 | **11** | **0** |

Of the LDT's eleven on ARC-AGI-1 evaluation, eight are training verifiers it reproduced (the library
finds those too) and **three are programs no verifier is**, on tasks the library does not solve:

- `0c786b71`: `vmirror`, `hconcat`, `hmirror`, `vconcat`, `hmirror` — a five-statement composition;
- `d4b1c2b1`: `upscale(I, numcolors(I))`;
- `ea959feb`: the verifier of `484b58aa` with one argument of `objects` changed (`F` to `T`), the
  edit its mutant tasks train.

That is a small number and the clearest result of the round: learned deduction over programs
composes and edits beyond the programs it was trained on, while the library is pure recall. Two
gaps stand out. On ARC-AGI-1 training the LDT finds 54 against the library's 294: it learned
re-arc's distribution of each task better than the original instances (84% on held-out re-arc
tasks), and building a 15-statement program field by field rarely survives every choice. And
ARC-AGI-2 stays at 0 for every method, the library included: none of its tasks is a re-arc
transformation or one edit away from one.

The validation set is 128 held-out tasks of r4b's data, re-arc examples of the same 295 verifiers of
which about one in six is a one-edit mutant no verifier gives, so it measures recall within
re-arc's distribution, not generalisation; the evaluation splits are the claim. Each of the four
evaluation numbers is one read, logged in `EVALUATION.md` before it ran.

## Open

- **The hybrid's second half.** Abstract evaluation maps program states to output-lattice states (the
  first half, above); the other direction is a transductive head that predicts the test output as the
  paper's grid lattice and ranks partial programs whose abstract test output is disjoint from it (a
  learned state can rank but not prune soundly). Deferred: the next round starts from TRM (USER,
  2026-10-23).
- **Canonical-order retraining.** Data made since the second review has canonical targets; r4b was
  trained before, against one statement order.
- **Longer programs.** 102 of re-arc's 400 verifiers exceed 32 statements (105 in this round).
