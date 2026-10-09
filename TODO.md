> yes let's go

(USER, 2026-10-09, approving levers 1 + 2 of the scaling brainstorm on this PR: random restarts as a
second vmap axis with real seeds, leave-one-out selection, then the 3-seed matched-compute comparison
of the learned library against the base library on all 901 tasks.)

- [WIP] @session_01Y854etDnNVah3TKrmmmSg9-2026-10-09 11:00 `--restarts R`: each candidate fitted from R starts, restart 0 at the prior and the others
      perturbed from it by noise seeded by `(seed, iteration, term)`; the best by DL is the candidate's fit
- [ ] `--select loo`: re-rank the `keep` candidates of least DL by how many training pairs they predict
      when fitted on the other two, ties by DL; the summary reports top-1 under both selectors
- [ ] tests for both
- [ ] `modal_run.py` resumes from its checkpoints after a preemption
- [ ] runs: library (2 new boxes per iteration) vs control (`--new-boxes 0`), seeds 0/1/2, all 901 tasks,
      size ≤ 5, on GPUs; mean ± sd per iteration
- [ ] README and PR description
