# Reads of sealed splits

The ARC-AGI-1 and ARC-AGI-2 `evaluation` splits are read only to score a published claim
(USER's ruling for the earlier ARC work, 2026-09-03). Each read is one line, written before the
numbers are looked at. 1D-ARC is the benchmark of the one-dimensional phase: it is never trained or
selected on; the signature in `ldt/dsl1d.py` was written after reading one example per family,
which is said wherever its numbers are.

| date | split | claim scored | by |
|---|---|---|---|
| 2026-10-23 | ARC-AGI-1 evaluation | enumeration of `dsl2d` at 2×10⁴ programs per task, pass@2 (arc_1d#3 results table) | toumix-agents |
| 2026-10-23 | ARC-AGI-1 evaluation | LDT r2d3 (exact α, 20k steps), 32 chains × 100 rounds, half kill-free, pass@2; chosen on ARC-AGI-1 training (25 vs 21 for r2d) | toumix-agents |
| 2026-10-23 | ARC-AGI-2 evaluation | enumeration of `dsl2d` at 2×10⁴ programs per task, pass@2 | toumix-agents |
| 2026-10-23 | ARC-AGI-2 evaluation | LDT r2d3, the same settings, pass@2 | toumix-agents |

Results and one correction, 2026-10-23. ARC-AGI-1 evaluation: enumeration 7/400, LDT r2d3 3/400.
ARC-AGI-2 evaluation: both reads scored 114 tasks, not 120: the exclusion of ARC-AGI-1's evaluation ids,
meant for ARC-AGI-2's training split, also dropped the 6 evaluation tasks the two benchmarks share
(fixed in `benchmark`). Those 6 are identical to ARC-AGI-1 evaluation tasks, whose read already
scored them: neither method solves any. Both methods are 0/120 on ARC-AGI-2 evaluation, with no
further read.
| 2026-10-23 | ARC-AGI-1 evaluation | library control: re-arc's 295 verifiers that fit 32 statements, each run as it is, pass@2 (arc_1d#3, arc-dsl round) | toumix-agents |
| 2026-10-23 | ARC-AGI-1 evaluation | LDT r4b (straight-line arc-dsl, re-arc data, 20k steps), 32 chains × 160 rounds, half kill-free, no colour augmentation, 1 s per program run, pass@2 | toumix-agents |
| 2026-10-23 | ARC-AGI-2 evaluation | library control, as above | toumix-agents |
| 2026-10-23 | ARC-AGI-2 evaluation | LDT r4b, as above | toumix-agents |
