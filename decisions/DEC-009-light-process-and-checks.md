---
id: DEC-009
title: Lighter task process and checks tiered by cost
status: accepted
created: 2026-10-27
from: [DIS-002]
related: [DEC-007]
superseded_by:
---
# DEC-009: Lighter task process and checks tiered by cost

## Context

One person drives the project with agents. Sending every task through
Triage and running the full test suite on every commit costs time without
catching more. The user wants the checks time-efficient: no slow tests on
small commits.

## Decision

- **Triage only when needed.** Small, obvious `method`, `infra` and `coord`
  tasks may go straight to To Do with a `--ref` to the DIS they came from.
  Triage is for tasks an agent found on its own, or that are unclear.
- **Checks tiered by cost.**
  - Pre-commit hook (every commit, seconds): the existing guards (data and
    binary files, notebook outputs) plus `ruff check` on the staged `.py`
    files only. When ruff is missing it warns and skips.
  - `scripts/check.sh` (once before merging to `master`, not on every commit):
    `ruff check src tests scripts`, `pytest -q`, and
    `python research_notes/tools/build_index.py --check` (skipped when
    `research_notes/` is absent).
  - The board's Definition of Done is "scripts/check.sh passes".
- **Docs.** The workflow (records, board, git and [DEC-007](DEC-007-session-branches-no-worktrees.md), checks, notebooks)
  moves to `docs/workflow.md`, imported into `CLAUDE.md` with
  `@docs/workflow.md`. The hard rules (patient data, no worktrees, NOTOUCH,
  `submit1` naming) stay in `CLAUDE.md` itself.

## Consequences

- Commits stay fast; the full suite runs once per branch.
- Small tasks start without waiting for triage.
- `CLAUDE.md` is short and the hard rules stand out.
