---
id: DIS-049
title: Epic 1 - low test W2 liver of R1 and R4 - suspected liver-negative label errors, spleen confusion checked, audit and blinded re-read
status: concluded
created: 2026-11-24
outcomes: []
related: [DEC-076, DEC-077, DEC-080, DEC-071, DEC-075, DEC-059, DEC-052, DEC-053, DIS-028]
---
# DIS-049: Epic 1 - low test W2 liver of R1 and R4

## Question

The user found the test W2 liver of R1 (`transunet`, ImageNet-21k weights) and R4 (DINOv3
ConvNeXt-B with an MLP head), the first two seed-0 runs of [TASK-197](../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md) (epic 1 runs on RunPod), not
satisfactory. Both models did badly on the same kind of sample: liver labelled absent. The user
suspected the labels and asked for theory to analyse this, then whether the models mistake
the spleen for liver. W2 is the "no phantom organs" score: per organ, the share of samples
labelled absent (closed negative, `strict_v1`) where the model predicts 0 pixels of it
([DEC-076](../decisions/DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md) Table 1).

## Facts checked

Full numbers, CIs and methods: the journal note
[2026-11-24-liver-negative-label-check-claude.md](../journal/2026/2026-11-24-liver-negative-label-check-claude.md).
Exploratory; one seed per recipe; aggregates only.

- W2 liver, val against test: R1 0.860 against 0.527, R4 0.929 against 0.584 (n = 630 val and
  543 test liver negatives; checkpoints selected on val, R1 epoch 30, R4 epoch 15).
- Shared failures beyond chance: 184 test samples failed in both models against 107.0 expected if
  independent; Cohen's κ 0.573 (95% CI 0.446-0.655, cluster bootstrap over datasource groups).
- 540 of 543 test liver negatives are kidney views (kidney positive, stomach and gallbladder
  absent). The false liver is small: median 0.016 (R1) and 0.030 (R4) of the input area.
- Val shares datasource groups with train and failed on 0.071-0.140 of liver negatives; test holds
  out groups and failed on 0.416-0.473, high in every test group with 12 or more such samples.
- Spleen: 538 of 543 test liver negatives also have the spleen labelled absent. Where a spleen is
  drawn (val 143, train 723), both models failed less often than where it is absent. Test sources
  draw a spleen on 5 of 2,168 samples, train + val on 877 of 17,843.

## Options considered

Analyst's reading, given once: a shared failure has three possible causes (label wrong, hard image,
test sources that differ), and the run records cannot separate them. Spleen confusion, as
labelled, does not explain the test failures. A kidney view with both liver and spleen labelled
absent is unusual in general ultrasound anatomy (the analyst's understanding, not verified), so
"absent" in those projects may mean "not labelled". Only a look at the images decides it.

Methods offered (links in the journal note): error consistency (κ between the two models' errors;
done), the kinds of label noise (random, class-dependent, input-dependent), confident learning
(needs per-sample probabilities the records do not hold), and area under the margin (training
dynamics; the per-sample train records every 5 epochs exist).

Table 1. The analyst's proposals, the user's choice (2026-11-24, "ok" to the defaults) and when the
alternative would win.

| # | Question | Recommendation (default) | Chosen | Alternative, and when it would win |
|---|---|---|---|---|
| 1 | Next analysis without images | a liver-negative audit task: failure per datasource group and spleen state, and a training-dynamics count from the saved train records | **accepted** ([TASK-232](../../backlog/tasks/task-232%20-%20Liver-negative-audit-of-the-TASK-197-runs-R1-and-R4-failure-rate-per-datasource-group-and-spleen-state-on-val-and-test-and-a-training-dynamics-count-of-train-liver-negatives-fit-late-or-never-aggregate-dataset-record-DIS-049.md)) | skip it and go straight to the re-read, if the user already suspects one labelling project |
| 2 | Decide the cause | a blinded re-read by the user in Label Studio: 40 test liver negatives both models failed on and 40 both passed, mixed, no model output; per image liver visible, spleen visible, kidney side | **accepted** ([TASK-233](../../backlog/tasks/task-233%20-%20Blinded-re-read-of-test-liver-negatives-in-Label-Studio-40-both-fail-and-40-both-pass-samples-of-R1-and-R4-no-model-output-liver-visible-spleen-visible-kidney-side-dataset-record-DIS-049.md)) | none offered; it is the only check that looks at the images |
| 3 | The other epic 1 runs | keep running R2, R3, R5 and R6 unchanged; the EXP record carries the W2 liver caveat | **accepted** (caveat sent to the TASK-197 session) | pause, if the re-read were expected to change the labels before the other runs end |

Said once by the analyst and kept: test labels must not be changed only where the models failed,
which would raise the test score by construction. The re-read changes no label. A relabel rule, if
one comes, is a new DEC and applies to all splits.

Also made at the user's request (not board work): a paginated gallery notebook of R1 and R4 liver
predictions per sample category (`notebooks/quick/epic1-task197-liver-negative-gallery.ipynb`,
machine01 scratch, not committed). It shows model output, so it is not for the blinded re-read.

## Conclusion

No decision record: the work is analysis and a re-read that change no rule, label or split. Board
tasks, both `data`, milestone m-1, To Do:

- TASK-232: liver-negative audit of the TASK-197 runs R1 and R4 (failure per datasource group and
  spleen state; training-dynamics count); aggregate dataset record.
- TASK-233: blinded re-read of test liver negatives in Label Studio; new derived table of the
  answers; dataset record.

TASK-197 (epic 1 runs on RunPod) keeps running. The caveat for its EXP record was sent to the
session working on TASK-197, because that task file had that session's uncommitted edits.

## Open questions

- After TASK-233: if liver is often visible in "liver absent" kidney views, what relabel or
  presence-policy rule follows (a new DEC; it would apply to all splits, and touches labels and
  metrics).
- Whether the W2 bar for liver should be read with the 1% area floor (DEC-076 rule 2 keeps floors
  as information only until a DEC sets one after the values are seen).
