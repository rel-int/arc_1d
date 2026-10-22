# Reads of sealed splits

The ARC-AGI-1 and ARC-AGI-2 `evaluation` splits are read only to score a published claim
(USER's ruling for the earlier ARC work, 2026-09-03). Each read is one line, written before the
numbers are looked at. 1D-ARC is the benchmark of the one-dimensional phase: it is never trained or
selected on; the signature in `ldt/dsl1d.py` was written after reading one example per family,
which is said wherever its numbers are.

| date | split | claim scored | by |
|---|---|---|---|
