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
