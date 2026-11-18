---
id: DEC-070
title: Anatomy label-set task seg_anatomy_v2 - organ states come from sample-file columns; evaluation refuses label-set tasks until point 4
status: accepted
area: [training]
created: 2026-11-18
from: []
related: [DEC-066, DEC-069, DEC-065, DEC-068, DEC-044]
superseded_by:
---
# DEC-070: Anatomy label-set task seg_anatomy_v2 - organ states in the sample file

## Context

[DEC-066](DEC-066-epic1-model-task-label-set-softmax.md) (label-set softmax) fixes the classes
and the target of the epic 1 anatomy model: per pixel a label set, built from each first-set
organ's `strict_v1` state and its polygons. [DEC-069](DEC-069-epic1-data-preparation.md)
(data preparation) fixes which samples enter. Two things were left open for the task kind
([TASK-159](../../backlog/tasks/task-159%20-%20Anatomy-label-set-task-definition-a-registered-task-for-background-liver-kidney-stomach-and-gallbladder-whose-target-is-the-DEC-066-bitmask-built-by-label_set_target-from-each-samples-strict_v1-states-and-polygons.md)):

1. The training reader (`src/sonoai/training/samples.py`) reads only the `labels/` tables. The
   organ states live in a `derived/` presence table, so they had no way into the target.
2. The segmentation trainer evaluates with class-id confusion matrices
   (`src/sonoai/evaluation/evaluate.py`). A label-set (bitmask) target there gives wrong
   numbers. The proper score (DEC-066 rule 6) belongs to point 4 (metrics), not yet decided.

Options were discussed in a consult session (no DIS record; the choice was small):

| Question | Chosen | Alternative | When the alternative would win |
|---|---|---|---|
| Where the organ states come from at train time | Columns of the sample file | The reader also reads the `strict_v1` presence table and joins by image and crop box | Many sample files share one presence table and should not be rebuilt |
| Evaluation before point 4 | Refuse a label-set task with a clear error | Evaluate by the loss only | A sanity run is wanted before point 4 is settled |

Table 1. The two open questions of the task kind, with the user's choice and the best alternative.

## Decision

1. **Task `seg_anatomy_v2`.** Classes background, liver, kidney, stomach, gallbladder (DEC-066
   rule 1 order); flat type `seg`, one softmax; `ignore_index` 255; target fill 1, the label set
   {background} ([DEC-068](DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md)).
   Same subject as `seg_anatomy_v1`, new version because classes and target form changed.
2. **Organ states come from the sample file.** Columns `state_liver`, `state_kidney`,
   `state_stomach`, `state_gallbladder`, each `positive`, `negative` or `unknown` (unknown where
   the pair has no `strict_v1` row). The candidate table of DEC-069 rule 7 carries them; the
   sample-file builder of point 3 (splitting) copies them; the reader gives them to the target.
3. **Every sample of the sample file is eligible.** Which samples enter is the builder's job
   (DEC-069). Positive-without-polygon flags are all false, because DEC-069 flag C excludes such
   samples; DEC-066 rule 3b stays in the target builder for a later version (DEC-069 rule 5).
4. **Evaluation refuses a label-set task** with a message naming point 4 (metrics), until a
   point-4 task adds the DEC-066 rule 6 score.

Reasons for rule 2: the run record already keeps the sample file's sha256, so it then pins the
targets too; the GPU box needs no second enc1 copy; the B-mode detector task `det_bmode_v1`
already reads its targets from its sample file.

## Consequences

- Board: TASK-159 (task kind `seg_anatomy_v2`, method) is rewritten to this record;
  [TASK-163](../../backlog/tasks/task-163%20-%20Epic-1-anatomy-candidate-builder-GQCS-exclusion-flags-at-a-224-px-minimum-side-counts-per-flag-organ-state-and-datasource-group-first-set-polygon-overlap-and-in-crop-polygon-area-report-sonoai-data-command-synthetic-tests-DEC-069.md) (candidate builder) adds the four `state_*` columns to the candidate table.
- Point 3: its sample-file builder copies the `state_*` columns.
- Point 4: its metrics task replaces the refusal of rule 4.
