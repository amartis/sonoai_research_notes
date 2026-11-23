---
id: DEC-084
title: A light scripts/check.sh - slow tests marked and run in full only when model or training code changes; passing tests leave no temp files (amends DEC-009)
status: accepted
area: [workflow]
created: 2026-11-23
from: [DIS-043]
related: [DEC-009, DEC-028, DEC-032]
superseded_by:
---
# DEC-084: A light scripts/check.sh with an automatic full run

## Context

`scripts/check.sh` runs before every merge to `master` ([DEC-009](DEC-009-light-process-and-checks.md)), often in several
worktrees at once ([DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)). The full pytest takes about 190 s on machine01, and the
trainer tests left about 2.6 GB of checkpoints per run in pytest's temp folders, enough to
fill the 9.5 GB `/tmp` after three runs ([DIS-043](../discussions/DIS-043-light-check-sh-and-pytest-temp-space.md)). The user wants `check.sh` light, while
it still works as the QA gate.

## Decision

1. **Passing tests leave no temp files.** `pyproject.toml` sets
   `tmp_path_retention_policy = "failed"`: pytest deletes a passing test's `tmp_path` at
   teardown and keeps failing tests' folders for debugging.
2. **Tests write no checkpoints they do not check.** A test that only checks weights or
   metrics stops checkpoint writes inside the test (for example by monkeypatching
   `torch.save`), not through a test-only option in `src/`. Resume, `best.pt` and
   `last.pt` stay covered by the tests that check them.
3. **A `slow` marker.** Tests that take 1 s or more on machine01 get `@pytest.mark.slow`
   (the marker is registered in `pyproject.toml`, with `--strict-markers`), so that the
   default run takes under about 60 s on machine01.
4. **`scripts/check.sh` runs the fast tests by default** (`-m "not slow"`) and **the full
   suite** when:
   - `--full` is given, or
   - the branch diff against `master` (`git diff --name-only master...HEAD` plus uncommitted
     changes) touches code that a slow test covers: `src/sonoai/models/`,
     `src/sonoai/training/`, any other `src/sonoai/<area>/` that a test file with slow tests
     imports (`check.sh` reads this from the test files' `sonoai` imports, so there is no
     list to keep up to date), `scripts/train.py`, `pyproject.toml`, `requirements*.txt`,
     or a test file that holds a slow test.

   It prints which mode it ran and why. ruff and the notes index check run in both modes.
5. **Amends DEC-009**: the check.sh bullet now reads as above; the Definition of Done stays
   "scripts/check.sh passes".

## Consequences

- A docs, board or tooling branch runs the fast set only; a branch that changes code a slow
  test covers pays for the full run, as before.
- A change that breaks a slow test only through an import the trigger does not see (a
  dynamic import, or code reached through another area) is caught at the next full run.
  `--full` is there when in doubt.
- New slow tests must be marked; a reviewer checks this on test changes.
