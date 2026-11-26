---
id: DEC-118
title: Test runs while working and in review - own test files while working, check.sh once on the final code, reviewers rerun only after a later code commit
status: accepted
area: [workflow]
created: 2026-11-26
from: [DIS-069]
related: [DEC-009, DEC-032, DEC-084, DEC-119]
superseded_by:
---
# DEC-118: Test runs while working and in review

## Context

In TASK-286 (epic 3 scoring for seg_spot_v1) the whole suite (135 s on machine01) ran
several times: by the writer after a commit that changed only text, by the code reviewer
on code the writer had already tested, and by the lead
([DIS-069](../discussions/DIS-069-faster-check-sh-and-test-runs.md), faster check.sh).

## Decision

1. **Writer agents, while working:** run only the test files for the code they change, plus
   `ruff check` on those files.
2. **Writer agents, at the end:** run `scripts/check.sh` once on the final code and report
   its result with the commit it ran on. Rerun it only after a later commit that changes
   code (`src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml`, `requirements*.txt`).
3. **Code reviewers:** run `ruff check` and the task's own test files; run
   `scripts/check.sh` only when the branch has a code commit after the writer's reported
   run, or the writer reported none.
4. **The lead:** runs `scripts/check.sh` once before the merge question when master has
   moved since the writer's run (after merging master into the branch).

The rule is in `docs/workflow.md` (Checks, "Test runs while working and in review"); the
method, data, infra and reviewer agent definitions and the lead skill point to it.

## Consequences

- The Definition of Done stays "scripts/check.sh passes" (DEC-084).
- Once [DEC-119](DEC-119-check-sh-skips-pytest-on-unchanged-code.md) (check.sh skips
  pytest on unchanged code) is in the script, points 2 to 4 shrink to "run
  `scripts/check.sh`; the script decides": TASK-299 cuts the text to that.
