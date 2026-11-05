---
id: DIS-019
title: A hepatic-cirrhosis training task - organ layer as ground truth only, filtered sample set, datasource-held-out test, per-sample matrices
status: concluded
created: 2026-11-05
outcomes: [DEC-043, DEC-044, DEC-045]
related: [DEC-004, DEC-006, DEC-033, DEC-034, DEC-035, DEC-036, DEC-041, DEC-042, DIS-012]
---
# DIS-019: A hepatic-cirrhosis training task

## Question

The user wants a training task that diagnoses hepatic cirrhosis, with:

- ground truth (GT) in two layers: an organ layer (background, upper-abdomen organs, VOID
  where the organ outline is uncertain) and a cirrhosis layer; the prediction has the
  cirrhosis layer only;
- one sample per crop, even when the crop was labelled in several projects;
- only normal-quality images with a clear liver and a clear cirrhosis status, filtered by
  rules and by Qwen3-VL-8B-Instruct, without dropping good images; the final list fixed in
  a file;
- three splits: test held out by datasource, train/val random, similar cirrhosis share;
- per epoch, a confusion matrix per sample (train, val and test), DSC and IoU of the
  cirrhosis layer, the share of predicted cirrhosis inside the GT liver, and an accuracy
  from a per-sample DSC threshold.

Why now: no liver-disease task has been trained yet (milestone m-1), and the existing
`lseg_cirrhosis_v3` ([DEC-006](../decisions/DEC-006-losses-optim-tracking.md), [DEC-034](../decisions/DEC-034-organ-layer-from-organ-polygons-only.md)) predicts both layers and has a liver-only organ layer.

## What the configs show

- 4 labeling projects of 261023 offer the `hepatic_cirrhosis` polygon
  (`configs/data/label_projects.yaml`). 2 offer the full upper-abdomen organ list; 2 offer
  no organ at all. Crops of the latter have an organ outline only if the same crop was also
  outlined in another project, so merging one crop across projects matters.
- `taskcrops_df.id` is one row per labeling task, so one crop can appear as several rows.
- The quality and exclusion rule for train/val/test is open in [TASK-062](../../backlog/tasks/task-062%20-%20Decide-the-rule-for-leaving-out-quality-and-case-exclusion-crops-from-train-val-test-DIS-012.md) (Parked).

## Options considered

- **VOID rule.** (A) VOID = area whose organ status is unknown: outside drawn organs when
  none of the sample's projects offered the full organ list, rare organ labels, and
  disease polygon area outside the liver polygon. (B) A band of a few pixels along every
  organ outline. (C) Both. Chosen: A. Two projects outline no organs, so their
  background is not "no organ"; an edge band adds noise to a layer used only for measuring.
- **Per-sample matrices.** DEC-006 keeps only aggregates in runs, no sample identifiers.
  (A) Amend it: per-sample matrices keyed by the sample's number in the fixed sample file.
  (B) Per-sample DSC and IoU only. Chosen: A.
- **Eligibility.** (A) Strict: liver polygon required; positive = a cirrhosis polygon;
  negative = looked at in a project that offered cirrhosis and drawn by none; ambiguous
  cases out. (B) Liver evidence as in v3. Chosen: A; the liver measure needs a liver
  outline on every sample.
- Defaults set by Claude and not objected to: task name, organ class list, sample identity
  by image hash and crop box, quality-filter acceptance (at most 2% of known-good crops
  flagged), split targets and balance tolerance, accuracy rule for negatives. All are
  recorded in the DECs below.
- Said once to the user: a random train/val split puts the same datasources, and perhaps
  the same patients, in both; validation scores will be optimistic and checkpoint choice
  leans with them. Only the test score is unbiased. The user's choice stands.

## Conclusion

- [DEC-043](../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md): the task `lseg_cirrhosis_v4`: GT organ + cirrhosis layers, prediction cirrhosis
  only, VOID rule, strict eligibility, measures and accuracy.
- [DEC-044](../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md): the sample set: one sample per image and crop box, rule and Qwen3-VL
  quality filter, fixed sample file, the three splits.
- [DEC-045](../decisions/DEC-045-per-sample-confusion-matrices-in-runs.md): per-sample confusion matrices in runs each epoch (amends DEC-006).
- Board tasks: see the task list in the DECs' consequences (created 2026-11-05).

## Open questions

- If the strict rule leaves too few positives or a test split cannot meet the size and
  balance targets, the data task reports the counts and stops; the user decides.
- Precirrhosis ([DEC-033](../decisions/DEC-033-precirrhosis-as-middle-grade-of-cirrhosis-task.md), proposed) is out of this task; its version becomes the next free
  one after `_v4`.
