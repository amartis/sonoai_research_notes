---
id: DIS-021
title: Training progress and TensorBoard on the GPU box
status: concluded
created: 2026-11-10
outcomes: [DEC-048]
related: [DEC-006, DEC-024, DEC-045]
---
# DIS-021: Training progress and TensorBoard on the GPU box

## Question

The user ran a training on the GPU box (`gpu train`) and asked four things:

1. After each epoch the output stops while the evaluation runs: no progress is shown.
2. The batch progress bar prints a new line for each batch. Is `\r` used properly?
3. Can the run evaluate the test split every epoch (when configured)?
4. What shows a run's progress in TensorBoard or another friendly view, and can it be
   opened on the GPU box without copying the run to machine01?

## Findings (from the code, 2026-11-10)

- The batch bar is `EpochProgress` in `src/sonoai/tracking/display.py` (tqdm, which redraws
  with `\r`). The epoch evaluation (`loop.fit` step 4, `sonoai.evaluation.evaluate`) has no
  progress output. It evaluates train (the whole training set), val and test one after the
  other, so the silent pause is long.
- `gpu train` runs the command in tmux and pipes its output through `tee` into `train.log`.
  Likely cause of one line per batch (**unverified**): the tqdm line is about 100 characters,
  wider than the ssh / Windows console, so each `\r` redraw starts on a wrapped row.
- Test is already evaluated at every evaluation when the test split has samples
  ([DEC-045](../decisions/DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3); the epoch table prints a `test:` line.
- Every run already writes TensorBoard event files to `<run>/tb/` (`TensorBoardView`, per
  [DEC-006](../decisions/DEC-006-losses-optim-tracking.md)): train loss and learning rate per step, each split's measures, and confusion
  matrix figures. Nothing starts a TensorBoard server.

## Options considered

- Progress in the log file: plain newline-ended lines every ~10 s when output is not a
  terminal, or a tqdm bar capped at 79 characters.
- Test cadence: a recipe option `test_eval_every` (default 1), or no change.
- TensorBoard: a repo script that starts the server on the GPU box and an ssh tunnel to
  machine01, or browsing only from Windows on machine02.

## Conclusion

1. Eval progress: a progress bar per evaluated split (decided by Claude: low stakes, inside
   the topic). Board task (method).
2. `\r` / line-per-batch: **skipped** by the user ("not important").
3. Test cadence: **no change**; DEC-045 already evaluates test every epoch.
4. TensorBoard through an ssh tunnel: [DEC-048](../decisions/DEC-048-tensorboard-on-the-gpu-box-through-an-ssh-tunnel.md). Board task (infra).

## Open questions

- If the line-per-batch output becomes a problem, check the wrap cause first (narrow the
  bar, or plain lines when output is not a terminal).
