---
id: DIS-048
title: A representative confusion matrix per run and epoch for the Epic 1 label-set targets
status: open
created: 2026-11-24
outcomes: []
related: [DEC-076, DEC-066, DEC-068, DEC-070, DEC-045, DEC-006, DEC-080]
---
# DIS-048: A representative confusion matrix for the Epic 1 label-set targets

## Question

The user wants confusion matrices of the [TASK-197](../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md)
(Epic 1 runs R1 to R6 on RunPod) runs, per epoch, to get a feel for what the models confuse.
Two things make a plain confusion matrix ill-defined here: some pixels have no single true class
(the label set holds background and the unknown organs), and in many samples an organ has no
ground-truth pixels (closed negative or unknown). Few matrices per run and epoch are wanted; more
are accepted only if unavoidable.

## Facts checked

- Target ([DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md) rule 3): each
  pixel has a **label set** S. Inside one positive organ's polygon S = {that organ}; inside two or
  more overlapping polygons S = those organs; outside every polygon S = {background} plus the
  organs unknown in that sample; [target fill](../../docs/glossary/global-glossary.md) outside the
  crop is {background} ([DEC-068](../decisions/DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md));
  ignore pixels (255) count nowhere. The prediction is one class (argmax of 5).
- What the runs keep ([DEC-076](../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md) rule 6.1):
  per sample, per epoch, per split, only 5 numbers per organ: presence state, predicted pixels P,
  polygon pixels G, overlap P∩G, input area. Not the joint counts (which class the missed pixels
  went to, or where the spilled predictions landed). So a full confusion matrix **cannot be built
  from the existing records**; it needs a new per-sample record.
- Checkpoints: the four fetched seed-0 run folders (R1, R4, R5, R6) hold `best.pt` only
  (checked by listing `checkpoints/`). Per-epoch matrices for these runs can therefore not be
  recovered later; only the selected epoch can be re-evaluated. R2 and R3 are not on machine01.
- Size of the problem (R4 seed 0, records of the first epoch; states do not depend on the epoch):

| Split | Samples | With ≥ 1 unknown organ | Positive: liver / kidney / stomach / gallbladder | Median polygon share of the input area, where positive |
|---|---|---|---|---|
| val | 3,007 | 983 (33%) | 2,288 / 1,486 / 539 / 316 | 11.3% / 6.6% / 1.8% / 2.5% |
| test | 2,168 | 503 (23%) | 1,617 / 1,063 / 367 / 268 | 15.0% / 10.7% / 2.5% / 2.2% |

Table 1. How common unknown organs and small organs are, R4 seed 0 evaluation records (aggregates
of the per-sample records; the states come from the targets). A third of val samples have
pixels with no single true class; liver polygons are about 5 times larger than gallbladder ones.

- Re-evaluating one checkpoint on val and test on machine01's CPU: about 9 to 16 min per run
  (derived from the TASK-197 note "11 reads of val and test take 1.7 to 2.9 h"; not measured).

## Reasoning

1. **Rows are kinds of label set, not classes.** A pixel has a true class only when its label
   set has one member. So the rows are: background only; liver; kidney; stomach; gallbladder;
   two or more organs (overlapping polygons); and **background or unknown organ** (outside the
   polygons, in a sample with an unknown organ). Columns are the 5 predicted classes. "VOID" is
   not used for the last row: it is a global term with another meaning ([DEC-043](../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md), the
   `lseg_cirrhosis_v4` organ layer).
2. **Average over samples, as W1 does.** A pixel-pooled matrix (sum all pixels, then normalise)
   is dominated by the liver and by large crops (Table 1); DEC-076 rule 3 rejected pixel pooling
   for selection for the same reason. A sample-mean matrix tells the same story as W1 and W2.
3. **Empty rows drop out per row ("zero area").** Normalise each row within each sample, then
   average row r only over the samples where row r has at least one pixel. A closed-negative or
   unknown organ adds nothing to its own row in that sample (no zero, no NaN). Each row then sums
   to 1, and its n (samples) is printed beside it. The diagonal of an organ row is then the mean
   share of the polygon that the model found (mean recall over positives).
4. **False positives need the second view.** In a row-normalised view, phantom predictions are a
   tiny share of the large background rows and look like 0. The column-normalised view (where do
   the pixels predicted as c lie?) shows them directly. In that view the "background or unknown
   organ" pixels split cleanly for each column c: c known absent or positive there (an error,
   the pixels W2 counts) versus c unknown there (not scored). Two views of the same counts.
5. **Epochs are curves, not 30 heatmaps.** Full matrices at the selected epoch; over epochs,
   curves of a few quantities. The existing records already give, per epoch and organ, the margins
   of the matrix: mean recall (P∩G / G), mean spill (share of predicted c outside c's polygon,
   1 − P∩G / P) and phantom rate (1 − W2). Which class takes the missed or spilled pixels needs
   the new record, so its per-epoch curves exist only for runs trained after the record is added.
6. **Test only at the selected epoch.** Per-epoch test matrices invite an informal choice on
   test ([DEC-045](../decisions/DEC-045-per-sample-confusion-matrices-in-runs.md) rule 3).

```
Recall view (rows sum to 1)            pred: bg    liver kidney stomach gb     n
  background only                           .97    .01   .01    .01    .00   2,990
  liver                                     .06    .92   .01    .01    .00   2,288
  kidney                                    ...                                1,486
  stomach / gallbladder / two or more organs ...
  ---------------------------------------------------------------
  background or unknown organ               .80    .05   .03    .10    .02     983
                                       (each organ cell also gives the part where that organ
                                        is known absent: an error)
```

Figure 1. Layout of the recall view (made-up numbers, layout only). The precision view has the
same rows and columns, normalised per column, with the last row split per column into "c known
absent" (error) and "c unknown" (not scored).

## Options considered

- **A: one recall-view matrix per run** at the selected epoch. Fewest figures; phantom
  predictions are nearly invisible.
- **B (recommended): recall view and precision view per run** at the selected epoch, val and
  test, plus margin curves over epochs on val. One figure per split (two panels) and one curve
  figure per run.
- **C: full matrices at every epoch** (30 per run and split). Only possible for runs trained
  with the new record; too many to read.
- Weighting: **sample-mean** (recommended, as W1) or **pixel-pooled** (better when the question
  is "where do most pixels go", e.g. for loss weighting).
- Data: **re-evaluate `best.pt`** of the six seed-0 runs on machine01 (no retraining; same code
  for all six) and **add the record to the trainer** so that the seed 1 and 2 runs of the best
  recipe get per-epoch matrices (recommended), or re-run seed 0 (cost of six RunPod runs).

## Conclusion

Pending the user's answers (see open questions).

## Open questions

1. Views: B (recall and precision views, plus margin curves)?
2. Weighting: sample-mean?
3. Data: re-evaluate `best.pt` of the six seed-0 runs on machine01, and add the record to the
   trainer before the seed 1 and 2 runs (which would then wait for that method task)?
