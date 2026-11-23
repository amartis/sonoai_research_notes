---
id: DIS-043
title: A light scripts/check.sh that still guards QA, and pytest temp space
status: concluded
created: 2026-11-23
outcomes: [DEC-084]
related: [DEC-009, DEC-028, DEC-032]
---
# DIS-043: A light scripts/check.sh that still guards QA, and pytest temp space

## Question

On 2026-11-20 `/tmp` (a 9.5 GB tmpfs on machine01) filled after a few `scripts/check.sh`
runs ([TASK-220](../../backlog/tasks/task-220%20-%20Trainer-tests-leave-several-GB-of-checkpoints-in-the-pytest-temp-folder-smaller-models-or-cleanup-so-scripts-check.sh-does-not-fill-tmp.md)), and the user paused `check.sh`. How do we stop the tests from filling
`/tmp`, and make `check.sh`, which every task runs before merging, light while it still works
as the QA gate?

Measured on machine01 on 2026-11-23 (synthetic tests only):

- The four trainer and model test files leave 2.6 GB per run: 2.1 GB from the frozen-then-warm
  fit test (the real DINOv3 ConvNeXt encoder: two runs, each with a best and a last
  checkpoint with optimiser state), 0.6 GB from the two FCOS-R50 detection runs, and almost
  none from the segmentation tests (a tiny conv model). pytest keeps the last 3 base temp
  folders: 3 x 2.6 GB is about 7.8 GB, close to the 7.6 GB found.
- The full suite takes 190 s (1631 tests on 2 CPUs) and peaks at about 3.5 GB of RAM.
  About 17 tests on real backbones (TransUNet-R50, DINOv3, FCOS-R50, Swin) take about half
  of the time.

## Options considered

Temp space:

- **A: `tmp_path_retention_policy = "failed"`** in `pyproject.toml`. pytest 8.3.5 deletes a
  passing test's `tmp_path` at teardown and keeps only failing tests' folders. One line.
  With A alone, a run still peaks at about 2.1 GB during the DINOv3 test, so 4 worktrees
  checking at once could need about 8.4 GB.
- **B: the DINOv3 frozen-then-warm test writes no checkpoints** (it checks encoder weights
  only), by monkeypatching `torch.save` in that test. With A, a run peaks at about 0.3 GB.
  The other way, a `save_checkpoints=False` option in `fit()`, changes the training loop
  for tests only.
- **C: a conftest fixture that deletes run folders**: the same as A, with more code.
- **D: a tiny FCOS for the detection tests**: saves only about 0.3 GB more and tests less of
  the real model.

Light check:

- **E: a `slow` marker with an automatic full run.** Heavy tests get `@pytest.mark.slow`.
  `check.sh` skips them by default, and runs everything when the branch diff against
  `master` touches model or training code or a slow test, or when `--full` is given. A
  model or training change cannot skip its own tests.
- **F: the same marker with `--full` run by hand**: simpler, easy to forget.
- **G: pytest-testmon** (only the tests that changed code reaches): the most selective, but a
  new dependency, a coverage database in each worktree, and it misses the dynamic imports of
  the model registry and `scripts/train.py`.

## Conclusion

The user chose A + B (monkeypatch in the test) and E, with a default run under about 60 s on
machine01: [DEC-084](../decisions/DEC-084-light-check-sh-slow-marker-auto-full-run.md). Board: TASK-220 (`method`).

## Open questions

- Once TASK-220 is merged, the pause on `check.sh` can be lifted (the user's call).
