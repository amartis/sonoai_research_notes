---
id: DEC-121
title: check.sh runs pytest with 3 workers, keeping at least half of machine01's memory free (amends DEC-120)
status: accepted
area: [workflow, infra]
created: 2026-11-26
from: [DIS-069]
related: [DEC-120, DEC-119, DEC-084]
superseded_by:
---
# DEC-121: check.sh runs pytest with 3 workers

## Context

[DEC-120](DEC-120-parallel-tests-measured-before-adoption.md) (parallel tests measured before
adoption) asked for timings with 6 workers before `scripts/check.sh` runs tests in parallel.
[TASK-300](../../backlog/tasks/task-300%20-%20Measure-parallel-tests-with-pytest-xdist-and-adopt-them-in-check.sh-only-if-at-least-30-faster-and-3-runs-in-a-row-pass-DEC-120.md)
(parallel test measurement) measured on machine01 (6 cores, 15 GB memory), n = 3 runs each,
math threads capped at 1 per worker, with other sessions running at the same time:

| Setup | Full suite mean | Fast set mean | Full runs passed | Peak memory, full suite |
| --- | --- | --- | --- | --- |
| Serial | 143.6 s | 77.6 s | 3 of 3 | not measured |
| 6 workers | 72.5 s (50% lower) | 27.4 s (65% lower) | 2 of 3 | one worker killed out of memory at 2.5 GB |
| 3 workers | 65.2 s (55% lower) | 34.5 s (56% lower) | 3 of 3 | 6.1 GB total, 3.1 GB largest process |

*Table: pytest-xdist timings for TASK-300 on machine01, n = 3 runs per cell; no confidence
interval for n = 3. Run times and notes are on TASK-300.*

The user asked to leave room for other work: at least 50% of the memory free while tests run.

## Decision

1. `scripts/check.sh` runs pytest with **3 workers** (pytest-xdist, `-n 3`), each worker's math
   threads capped at 1, and prints the worker count. This replaces the 6 workers of DEC-120
   point 2 for the adopted setting.
2. **Memory bound:** a test run keeps at least half of machine01's memory free (peak at most
   about 7.5 GB). The worker count is not raised unless a new measurement shows that bound holds.
3. pytest-xdist is pinned in `requirements-dev.txt` and installed in the default venv ([DEC-020](DEC-020-default-venv-matches-gpu-box.md)).
4. DEC-120 point 3 (adopt only if at least 30% faster and 3 parallel full runs in a row pass) is
   met for 3 workers and stays the bar for any later change of the worker count.

## Consequences

- The full suite drops from about 2.5 minutes to about 1 minute on machine01; the fast set from
  about 78 s to about 35 s.
- A test that fails only in parallel is fixed or marked to run serially, as DEC-120 says.
- Another machine with less memory may need fewer workers; the count is one setting in
  `scripts/check.sh`.
