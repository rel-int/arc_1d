#!/bin/bash
# (Re)start the 901-task size-5 run, resuming from its checkpoints.
cd "$(dirname "$0")"
setsid uv run python -m dc.run --per-family 0 --max-size 5 --quotas 3:57,4:50,5:43 \
    --out results/full-size5 --resume >> results/full-size5.log 2>&1 &
