> go for selection, ensemble the kept candidates, add the building blocks for familes with zero

(USER, 2026-10-12, on this PR. "Families with zero" are those at 0/50 in #1's runs, still the three
lowest after restarts: mirror 4, flip 4, move_dp 5 of 50.)

- [WIP] @session_01Y854etDnNVah3TKrmmmSg9-2026-10-12 09:00 `dc/select.py`: selectors over the kept
      candidates — least DL, leave-one-out, and votes over their test predictions: by `2^-DL`
      (model averaging under the MDL prior), by leave-one-out hits, and by both
- [ ] offline: every selector on the six runs' checkpoints, chosen on even tasks, reported on odd
- [ ] `reverse` (each object reversed in place), `pivot` (reflection about the first smallest
      object), `slide` (each side moved until it touches it): parameter-free, exact under padding
- [ ] tests for the three boxes and the selectors
- [ ] runs: new boxes + the chosen selector, library and control, seeds 0/1/2, all 901 tasks
- [ ] README and PR description
