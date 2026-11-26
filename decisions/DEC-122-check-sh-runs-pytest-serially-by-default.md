---
id: DEC-122
title: check.sh runs pytest serially by default; parallel runs only when CHECK_WORKERS asks (amends DEC-121)
status: accepted
area: [workflow, infra]
created: 2026-11-26
from: [DIS-069]
related: [DEC-121, DEC-120, DEC-119]
superseded_by:
---
# DEC-122: check.sh runs pytest serially by default

## Context

[DEC-121](DEC-121-check-sh-runs-pytest-with-3-workers.md) (check.sh runs pytest with 3 workers)
fixed 3 pytest-xdist workers, measured on machine01 (15 GB memory) in
[TASK-300](../../backlog/tasks/task-300%20-%20Measure-parallel-tests-with-pytest-xdist-and-adopt-them-in-check.sh-only-if-at-least-30-faster-and-3-runs-in-a-row-pass-DEC-120.md)
(parallel test measurement). The user pointed out that a fixed count does not fit other
machines, and that the full suite runs seldom since
[DEC-119](DEC-119-check-sh-skips-pytest-on-unchanged-code.md) (check.sh skips pytest on
unchanged code), so the saving does not pay for the risk.

## Decision

1. `scripts/check.sh` runs pytest **serially by default** (`CHECK_WORKERS` unset means 1). This
   replaces DEC-121 point 1 (3 workers by default).
2. The parallel code stays: `CHECK_WORKERS=<n>` with n above 1 runs pytest on n workers, each
   worker's math threads capped at 1, and prints the count. The memory bound of DEC-121 point 2
   (keep at least half the memory free) guides the n a member picks.
3. pytest-xdist stays pinned in `requirements-dev.txt` (DEC-121 point 3), so the opt-in works.

## Consequences

- check.sh times go back to serial: about 78 s for the fast set and 144 s for the full suite on
  machine01 (TASK-300 means, n = 3), except when the DEC-119 skip applies.
- A later DEC can pick a default per machine (e.g. from its memory) if parallel runs are wanted
  again.
