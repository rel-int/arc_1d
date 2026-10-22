# TODO

> I want to make a breakthrough in neurosymbolic AI by merging deep learning and domain theory with discopy i.e. adapt the lattice deduction transformer with the Scott domain of Bohm trees as lattice. Generate some synthetic data to train and use ARC AGI as a benchmark (the 1D version first then the public challenges 1 and 2).
> You should have access to modal GPUs for compute, let's say with a $100 budget to begin with and we can increase it depending on how promising the results are.

USER's answers in the session (2026-10-22): programs first then the hybrid with the output lattice; code in `rel-int/arc_1d` under `ldt/`; a hand-written typed DSL; straight through to ARC-AGI-1/2 within the $100.

- [x] typed Böhm-tree space: heap addresses, labels, the typing automaton and its exact projection (`ldt/bohm.py`)
- [x] 1D signature covering the 18 families of 1D-ARC (`ldt/dsl1d.py`), ceiling 901/901 by construction
- [x] synthetic tasks: uniform-by-size programs, Occam shrinking, one-edit alpha sets (`ldt/synth.py`)
- [x] discopy-next `closed` as reference semantics (`ldt/discopy_bridge.py`), 400/400 round trips
- [x] model, on-policy trainer, verified solver, enumeration control
- [ ] 100k synthetic tasks on Modal, a pilot run, then the full run
- [ ] 1D-ARC: LDT vs enumeration vs untrained search, per family, search cost
- [ ] hybrid: abstract evaluation of partial programs links the program and output lattices
- [ ] 2D DSL, synthetic data, ARC-AGI-1 and ARC-AGI-2 public evaluation (pass@2)
- [ ] README with results; delete this file
