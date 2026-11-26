---
id: DIS-069
title: Faster check.sh and test runs for agents
status: concluded
created: 2026-11-26
outcomes: [DEC-118, DEC-119, DEC-120]
related: [DEC-009, DEC-084, DEC-032]
---
# DIS-069: Faster check.sh and test runs for agents

## Question

How should `scripts/check.sh` (the check before every merge into master, [DEC-009](../decisions/DEC-009-light-process-and-checks.md) light
process and checks) and the agents stop spending time on test runs that cannot give a new
answer? Raised by the user on 2026-11-26 after [TASK-286](../../backlog/tasks/task-286%20-%20Epic-3-evaluation-for-seg_spot_v1-top-50-image-score-pixel-scores-with-the-stone-counted-for-its-mass-per-sample-record-validation-AUC-and-Dice-measures-synthetic-tests-DEC-112.md) (epic 3 scoring for seg_spot_v1):
its writer, its code reviewer and the lead each ran the whole test suite, including after
commits that changed only text.

Measured on machine01 on 2026-11-26 (one run each, no CI):

| Run | Tests | Time |
| --- | --- | --- |
| full suite (`pytest -q`) | 2169 passed, 2 skipped | 135 s |
| fast set (`-m "not slow"`), text-only branch | 2128 passed, 81 deselected | 74 s |
| the two TASK-286 test files alone | 92 passed | 2.5 s |

*Table 1. Test-run times on machine01, 2026-11-26, one run each. [DEC-084](../decisions/DEC-084-light-check-sh-slow-marker-auto-full-run.md) (light check.sh
with automatic full run) aimed for a fast set under about 60 s.*

Why the time was lost: DEC-084 chooses the mode from the whole branch diff against master,
so once a branch changes covered code, every later run is a full run, also after text-only
commits; and a text-only branch still runs the 74 s fast set.

## Options considered

- **Rules for agents only** (when writers, reviewers and the lead run what): quick to
  apply, but agents must interpret them.
- **check.sh skips pytest by a stored fingerprint of the code files** after a passing run:
  the logic sits in the script, so no agent has to judge "text only". Needs a small
  untracked file in the worktree's git folder.
- **check.sh skips pytest when the branch changes only text against master**: simpler, but
  a docs branch is then never tested on top of a master that another merge may have broken.
- **Parallel tests (pytest-xdist)**: saving not measured; tests that share files or ports
  can fail at random; torch in 6 processes can be slower unless threads are capped.

## Conclusion

The user chose:

- [DEC-118](../decisions/DEC-118-test-runs-while-working-and-in-review.md): writers run
  only their own test files while working and `scripts/check.sh` once on the final code;
  reviewers rerun it only after a later code commit (written into docs/workflow.md, the
  agent definitions and the lead skill).
- [DEC-119](../decisions/DEC-119-check-sh-skips-pytest-on-unchanged-code.md): the skip goes
  into the script itself, by the stored fingerprint, "as far as the logic in the script,
  instead of natural language the agent should interpret" (the user's words).
- [DEC-120](../decisions/DEC-120-parallel-tests-measured-before-adoption.md): parallel
  tests are measured first and adopted only past a set bar.

Board: [TASK-299](../../backlog/tasks/task-299%20-%20check.sh-skips-pytest-when-the-code-files-are-unchanged-since-its-last-passing-run-of-the-same-or-a-stronger-mode-DEC-119.md) (check.sh pytest skip, DEC-119) and [TASK-300](../../backlog/tasks/task-300%20-%20Measure-parallel-tests-with-pytest-xdist-and-adopt-them-in-check.sh-only-if-at-least-30-faster-and-3-runs-in-a-row-pass-DEC-120.md) (parallel test measurement,
DEC-120), the second after the first, because both change `scripts/check.sh`. [TASK-230](../../backlog/tasks/task-230%20-%20check.sh-mode-choice-read-multi-line-sonoai-imports-and-ignore-slow-marker-mentions-in-comments-make-the-torch.save-stub-in-the-DINOv3-fit-test-accept-file-objects.md)
(check.sh mode-choice fixes) stays in Triage.

## Open questions

- None now. TASK-300's numbers decide whether parallel runs are adopted.
