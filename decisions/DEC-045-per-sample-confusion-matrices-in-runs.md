---
id: DEC-045
title: Runs store a confusion matrix per sample for train, val and test at every evaluation, keyed by the sample number of the fixed sample file
status: accepted
area: [training, data-security]
created: 2026-11-05
from: [DIS-019]
related: [DEC-006, DEC-043, DEC-044]
superseded_by:
---
# DEC-045: Per-sample confusion matrices in runs

## Context

[DIS-019](../discussions/DIS-019-cirrhosis-training-task.md). The user wants, for every
epoch, the confusion matrix of each train, val and test sample.
[DEC-006](DEC-006-losses-optim-tracking.md) records only aggregates in runs: "never images,
per-sample predictions or sample identifiers".

## Decision

Amends DEC-006 (result tracking):

1. A task may ask for **per-sample matrices**. At each evaluation the run then stores, for
   each sample of each evaluated split, its integer joint pixel matrix
   ([DEC-043](DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md) rule 6), in
   `eval/<split>_e<NNN>_samples.json` (or `.jsonl`).
2. Samples are keyed **only by their sample number** in the fixed sample file
   ([DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md)), never by a file
   name, path, image hash, `taskcrops_df` id or datasource. The number maps back to an image
   only on machine01, through the sample file.
3. Train, val and test are evaluated every epoch (train without augmentation). Selection
   uses val only; test is recorded and never used for a choice.
4. The rest of DEC-006 stands: no images and no predicted masks in runs.

## Consequences

- Accuracy at any DSC threshold, per-sample DSC, IoU and liver share can be recomputed for
  any past run without inference.
- Size: 24 GT rows (12 organ classes incl. VOID x 2 cirrhosis classes) x 2 columns of
  integers per sample; a few MB per evaluation for tens of thousands of samples.
- An evaluation pass over train each epoch costs time: train is about 5 times val, so
  about 5 val passes; a recipe may set the train evaluation to every N epochs.
- Work: a `method` task (evaluation, run records, loop).
