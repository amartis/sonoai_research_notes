---
id: DEC-116
title: Brightness shift test on fit-scale runs - levels and normalisation on the crop pixels only, padding kept at 0, grid name bright_grid_v1 kept
status: accepted
area: [training]
created: 2026-11-26
from: [DIS-068]
related: [DEC-079, DEC-080, DEC-109]
superseded_by:
---
# DEC-116: Brightness shift test on fit-scale runs

## Context

[DIS-068](../discussions/DIS-068-shift-test-fit-scale-contrast-mean-grid-name.md) (brightness
shift test of fit-scale runs). In a fit-scale run
([DEC-109](../decisions/DEC-109-epic3-input-512-no-minimum-side-two-resize-modes.md), epic 3
input 512 and two resize modes, rule 3) part of the input is padding at image 0. Rule 5 of DEC-109
says the shift tests use the run's resize mode. The grid `bright_grid_v1`
([DEC-079](DEC-079-epic1-brightness-robustness-augmentation-percentile-norm-shift-test.md), epic 1
brightness robustness, rule 3) was written when every input was all crop.

## Decision

Accepted by the user on 2026-11-26.

1. **Levels act on the crop's pixels only.** In a fit-scale run, each level of the brightness shift
   test (gain, offset, gamma, contrast) changes only the pixels of the crop; the padding stays image 0.
   The contrast mean is `mean(grey(x))` over the crop's pixels only, not over the padding.
   In a stretch run the crop is the whole input, so nothing changes there.
2. **Normalisation on the crop's pixels only**, as in the reader's own unaugmented read
   ([TASK-282](../../backlog/tasks/task-282%20-%20Fit-scale-resize-mode-in-the-sample-reader-aspect-kept-longer-side-fills-the-input-centred-padding-with-image-0-and-the-target-fill-stretch-stays-the-default-synthetic-tests-DEC-109.md),
   fit-scale resize mode): the statistics of `Data.normalize` read only the crop's pixels, and the
   padding is 0 after it. So the unchanged read of the shift test equals the trainer's evaluation
   (DEC-079 rule 3; order of steps by
   [DEC-080](DEC-080-epic1-optimisation-strategy.md), epic 1 optimisation, rule 3.3).
3. **The grid name stays `bright_grid_v1`.** Its text says "the mean over the crop's pixels"; the
   note `shift.json` records the run's resize mode.
4. The training augmentations `us_mild_v2` and `us_bright_v1` are not changed: in fit mode their
   contrast mean and depth gain curve still cover the padding (accepted by the user on TASK-282).

## Consequences

- [TASK-285](../../backlog/tasks/task-285%20-%20Brightness-shift-test-with-fit-scale-reads-level-change-and-input-normalisation-on-the-crop-pixels-only-padding-kept-at-image-0-DEC-109-rule-5.md)
  (brightness shift test with fit-scale reads) implements rules 1 to 3 in `scripts/eval_shift.py`,
  with tests on synthetic data.
- Shift results of existing stretch runs stay valid; no re-run.
- A change of this decision means re-running the shift test only, no retraining.
