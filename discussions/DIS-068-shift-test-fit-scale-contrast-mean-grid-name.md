---
id: DIS-068
title: Brightness shift test of fit-scale runs - contrast mean and grid name
status: concluded
created: 2026-11-26
outcomes: [DEC-116]
related: [DEC-079, DEC-080, DEC-109]
---
# DIS-068: Brightness shift test of fit-scale runs

## Question

[TASK-285](../../backlog/tasks/task-285%20-%20Brightness-shift-test-with-fit-scale-reads-level-change-and-input-normalisation-on-the-crop-pixels-only-padding-kept-at-image-0-DEC-109-rule-5.md)
(brightness shift test with fit-scale reads), filed by
[TASK-282](../../backlog/tasks/task-282%20-%20Fit-scale-resize-mode-in-the-sample-reader-aspect-kept-longer-side-fills-the-input-centred-padding-with-image-0-and-the-target-fill-stretch-stays-the-default-synthetic-tests-DEC-109.md)
(fit-scale resize mode in the sample reader). In a fit-scale run the crop is fitted into the
512 x 512 input and the rest is padding at image 0
([DEC-109](../decisions/DEC-109-epic3-input-512-no-minimum-side-two-resize-modes.md), epic 3
input 512 and two resize modes, rule 3). Rule 5 of DEC-109 says the shift tests use the run's resize
mode. The shift test (`scripts/eval_shift.py`) applies its level and the input normalisation to the
whole image, so an offset or contrast level lifts the padding off 0, and the padding enters the
statistics. Two points needed the user:

1. For the contrast levels of grid `bright_grid_v1` (c = 0.6 and 1.5,
   [DEC-079](../decisions/DEC-079-epic1-brightness-robustness-augmentation-percentile-norm-shift-test.md),
   epic 1 brightness robustness, rule 3), which pixels give the mean grey value the contrast turns
   around: the crop's pixels only, or the whole input with the padding?
2. Keep the grid name `bright_grid_v1`, or a new name, since DEC-079 says a changed grid is a new name?

The percentile normalisation part was not open: the reader's own unaugmented read already uses only
the crop's pixels (TASK-282), and the shift test must equal it.

## Options considered

Point 1, the contrast mean:

- **Crop pixels only.** A scanner contrast change acts on the ultrasound image; the padding is a
  resize artefact. In a stretch run the whole input is the crop, so stretch and fit runs get the
  same change, and the stretch-against-fit comparison of DEC-109 stays fair. The padding at 0 would
  pull a whole-input mean down, more for wide or tall crops.
- **Whole input, padding included.** The same as the training augmentations `us_mild_v2` and
  `us_bright_v1` in fit mode (accepted by the user on TASK-282). Wins only if the test should copy
  the training augmentation exactly.

Point 2, the grid name:

- **Keep `bright_grid_v1`.** The grid already says each level changes the pixels of the crop;
  stretch runs give the same numbers as before, so a new name would split identical results.
  The note `shift.json` records the run's resize mode.
- **New name `bright_grid_v2`.** A strict reading of "a changed grid is a new name".

## Conclusion

The user, 2026-11-26: crop pixels only, and keep `bright_grid_v1`. Recorded as
[DEC-116](../decisions/DEC-116-shift-test-fit-scale-levels-on-crop-pixels-grid-name-kept.md)
(shift test on fit-scale runs). TASK-285 carries it (method, To Do).

## Open questions

None. Cost to reverse is low: no fit-run shift results exist yet, and a change means re-running
the shift test only, no retraining.
