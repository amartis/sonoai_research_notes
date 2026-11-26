---
id: DEC-119
title: check.sh skips pytest when the code files are unchanged since its last passing run of the same or a stronger mode (amends DEC-084)
status: accepted
area: [workflow]
created: 2026-11-26
from: [DIS-069]
related: [DEC-084, DEC-009, DEC-118]
superseded_by:
---
# DEC-119: check.sh skips pytest on unchanged code

## Context

`scripts/check.sh` chooses fast or full tests from the branch diff against master
([DEC-084](DEC-084-light-check-sh-slow-marker-auto-full-run.md), light check.sh with automatic full run), so it reruns tests that cannot give a
new answer: after text-only commits, and on text-only branches (74 s fast set, 135 s full
suite on machine01, [DIS-069](../discussions/DIS-069-faster-check-sh-and-test-runs.md)).
The user wants this logic in the script, not in instructions that agents interpret.

## Decision

1. After a run where every step passed, `scripts/check.sh` stores a **code fingerprint**
   and the mode it ran (fast or full) in an untracked file inside the worktree's git folder
   (`git rev-parse --git-dir`). The fingerprint covers the contents of every file, tracked
   or untracked (not ignored), under `src/`, `tests/`, `scripts/`, `configs/`, plus
   `pyproject.toml` and `requirements*.txt`. The file holds hashes and the mode only, no
   data, and is never committed.
2. On the next run, pytest is **skipped** when the fingerprint is the same and the stored
   mode is at least the mode this run needs (full covers fast). The script prints why, e.g.
   `== pytest skipped: code unchanged since the passing full run`.
3. ruff, the duplicate-ID and glossary checks and the notes index check **run every time**.
   `--full` always runs the full suite. A failed run stores nothing and removes an old file.
4. **Amends DEC-084** point 4: the mode rule is unchanged; this adds the skip in front of it.

## Consequences

- Merging master into a branch changes the fingerprint when master brought code, so the
  tests run again; a text-only commit or rerun costs seconds.
- A change outside the listed paths that a test reads (e.g. a test fixture elsewhere) is
  not seen; `--full` is there when in doubt, and the list can grow.
- Each worktree has its own git folder, so the stored file is per worktree.
