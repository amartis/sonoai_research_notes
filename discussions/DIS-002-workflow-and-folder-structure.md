---
id: DIS-002
title: Workflow and folder structure review
status: concluded
created: 2026-10-27
outcomes: [DEC-008, DEC-009, DEC-010]
related: [DEC-003, DEC-007]
---
# DIS-002: Workflow and folder structure review

## Question

After the board (Backlog.md), [DEC-007](../decisions/DEC-007-session-branches-no-worktrees.md) and the first dataset tools landed,
the repo was reviewed with the user (2026-10-27): does the folder layout
still match what is there, is the process light enough for one person
working with agents, and can a run be traced back to the task it serves?

## Findings

1. **README layout is stale.** It lists `labeling/`, `serving/`, `viz/`
   (each only an empty `__init__.py`, imported by nothing) and misses
   `backlog/`, `docs/`, `configs/scraping/`, `configs/data/label_projects.yaml`.
2. **Dataset tools are six loose scripts** in `scripts/`
   (`make_plain_dataset.py`, `check_plain_dataset.py`, `make_enc_dataset.py`,
   `check_enc_dataset.py`, `remove_from_enc_dataset.py`, `label_summary.py`).
   Their logic is not importable, has no tests, and the checkers count
   failures in a global.
3. **Notebooks have no convention.** `notebooks/data_prep/T7-*.ipynb` are the
   user's own working notebooks; nothing says which notebooks agents may edit
   or where task notebooks go.
4. **Base branch.** The repo has no remote; the app proposes `main`, but the
   branch is `master`.
5. **Training config.** `configs/experiments/*.yaml` is what `train.py`
   reads today; [DEC-003](../decisions/DEC-003-trainrecipe-files-structure.md) recipes/plans are designed but not implemented.
6. **Process weight.** Every task passes through Triage, even small obvious
   ones; checks are not tiered (the hook runs no lint, and there is no single
   pre-merge check).
7. **Docs.** The workflow rules sit in `CLAUDE.md` next to the hard rules,
   which makes the hard rules harder to see.
8. **Runs and tasks.** A run's `meta.json` records the commit, not the task
   it was made for; EXP records have to reconstruct this.
9. `research_notes/tasks/` is retired (Backlog.md replaced TSK records) but
   still exists.

## Options considered

- **Worktrees for parallel sessions.** Raised again and dropped: DEC-007
  stands (one checkout, one branch per session).
- **Dataset tools**: keep scripts / move the logic into `src/sonoai/data/`
  behind one CLI. The CLI wins: testable with synthetic data, one entry point.
- **Checks**: full suite on every commit (slow) / tiered by cost. The user
  wants it time-efficient: no slow tests on small commits.

## Conclusion

Agreed with the user on 2026-10-27:

- [DEC-008](../decisions/DEC-008-repo-layout.md): repo layout (dataset CLI `sonoai-data`, no empty packages,
  `notebooks/human/` vs task notebooks, base branch stays `master`,
  experiments YAML is interim until DEC-003 is implemented).
- [DEC-009](../decisions/DEC-009-light-process-and-checks.md): lighter process (small obvious tasks go straight to To Do) and
  checks tiered by cost (`ruff` on staged files in the hook, `scripts/check.sh`
  before merging); workflow docs move to `docs/workflow.md`.
- [DEC-010](../decisions/DEC-010-runs-record-task.md): runs record the board task (`--task TASK-NNN`).
- Board: [TASK-002](../../backlog/archive/tasks/task-002%20-%20README-layout-fix-and-empty-package-removal.md) (README, empty packages), [TASK-003](../../backlog/archive/tasks/task-003%20-%20sonoai-data-CLI-for-the-dataset-tools.md) (`sonoai-data`),
  [TASK-004](../../backlog/archive/tasks/task-004%20-%20Notebooks-layout-human-and-per-scope-task-notebooks.md) (notebooks), [TASK-005](../../backlog/archive/tasks/task-005%20-%20Training-runs-record-the-board-task-task.md) (`--task`), [TASK-006](../../backlog/archive/tasks/task-006%20-%20Tiered-checks-ruff-in-pre-commit-scripts-check.sh.md) (checks), [TASK-007](../../backlog/archive/tasks/task-007%20-%20Workflow-docs-and-lighter-process.md)
  (workflow docs, notes cleanup), [TASK-008](../../backlog/tasks/task-008%20-%20Proper-labeling-documentation.md) (labeling documentation, Triage),
  [TASK-009](../../backlog/tasks/task-009%20-%20Implement-DEC-003-training-recipes-and-plans.md) (DEC-003 recipes/plans, after TASK-008).
- `research_notes/tasks/` is removed.

## Open questions

- What "proper" labeling documentation must cover (TASK-008, waits on the
  user); `configs/data/label_projects.yaml` and `label_taxonomy.yaml` exist.
