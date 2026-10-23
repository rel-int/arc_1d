# TODO

> I want to make a breakthrough in neurosymbolic AI by merging deep learning and domain theory with discopy i.e. adapt the lattice deduction transformer with the Scott domain of Bohm trees as lattice. Generate some synthetic data to train and use ARC AGI as a benchmark (the 1D version first then the public challenges 1 and 2).
> You should have access to modal GPUs for compute, let's say with a $100 budget to begin with and we can increase it depending on how promising the results are.

USER's answers in the session (2026-10-22): programs first then the hybrid with the output lattice; code in `rel-int/arc_1d` under `ldt/`; a hand-written typed DSL; straight through to ARC-AGI-1/2 within the $100.

- [x] typed Böhm-tree space: heap addresses, labels, the typing automaton and its exact projection (`ldt/bohm.py`)
- [x] 1D signature covering the 18 families of 1D-ARC (`ldt/dsl1d.py`), ceiling 901/901 by construction
- [x] synthetic tasks: uniform-by-size programs, Occam shrinking, one-edit alpha sets (`ldt/synth.py`)
- [x] discopy-next `closed` as reference semantics (`ldt/discopy_bridge.py`), 400/400 round trips
- [x] model, on-policy trainer, verified solver, enumeration control
- [x] 98k synthetic tasks on Modal; pilot (3k steps, 15 min H100): 388/901 pass@2 vs enumeration 451/460/502 at 10^4/10^5/10^6
- [x] full run (20k steps); kill-free chains; untrained control: r1 514/901
- [x] 1D-ARC: LDT vs enumeration vs untrained search, per family, search cost; LDT-then-enumeration 564
- [x] abstract evaluation of partial trees (`ldt/abstract.py`), sound on every cut of 150 random programs
- [x] hybrid, first half: prune with abstract evaluation at inference, measured (sound, no gain in 1D)
- [ ] hybrid, second half: a transductive output-lattice head whose state prunes programs
- [x] 2D DSL, synthetic data (one-edit and exact α), ARC-AGI-1 and ARC-AGI-2 public evaluation:
  enumeration 7/400 and 0/120, LDT 3/400 and 0/120, each one logged read
- [ ] README with results; delete this file
