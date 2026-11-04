---
id: DEC-010
title: Training runs record the board task they serve
status: accepted
area: [training]
created: 2026-10-27
from: [DIS-002]
related: [DEC-006]
superseded_by:
---
# DEC-010: Training runs record the board task they serve

## Context

A run's `meta.json` records the git commit but not which board task it was
made for, so EXP records have to reconstruct that link by hand.

## Decision

- `scripts/train.py --task TASK-NNN` (or `task:` in the experiment YAML; the
  flag wins) stores `task` in the run's `meta.json`.
- It is optional: smoke and debug runs may leave it out.
- EXP records list the names of the runs they draw on.

## Consequences

- Runs can be grouped by task; `git log --grep TASK-NNN` finds the code.
- `sonoai.tracking.Run` takes an optional task and writes it to `meta.json`.
