---
id: DEC-120
title: Parallel tests with pytest-xdist are measured first and adopted in check.sh only if at least 30% faster and 3 parallel runs in a row pass
status: accepted
area: [workflow, infra]
created: 2026-11-26
from: [DIS-069]
related: [DEC-084, DEC-119, DEC-020]
superseded_by:
---
# DEC-120: Parallel tests measured before adoption

## Context

machine01 has 6 cores; pytest runs on one. pytest-xdist (runs tests across several worker
processes) is not installed, and its saving here is not measured. Tests that share files or
ports can fail at random in parallel, and torch in several processes can be slower unless
each process's math threads are capped
([DIS-069](../discussions/DIS-069-faster-check-sh-and-test-runs.md), faster check.sh).

## Decision

1. One infra task installs pytest-xdist, pinned in `requirements-dev.txt`.
2. It times the full suite and the fast set **3 times each**, serial and with 6 workers,
   with each worker's math threads capped at 1 (e.g. `OMP_NUM_THREADS=1`), and reports
   each time and the mean.
3. `scripts/check.sh` adopts parallel runs only if the parallel mean is **at least 30%
   below** the serial mean for the full suite, and **3 parallel full runs in a row pass**.
   Otherwise it changes nothing in check.sh, removes the pin, and reports the numbers.

## Consequences

- A test that fails only in parallel is fixed or marked to run serially by that task, or
  the adoption stops.
- The bar (30%, 3 runs) can be changed by a later DEC once the numbers are in.
