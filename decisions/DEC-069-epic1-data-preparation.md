---
id: DEC-069
title: Epic 1 point 2 - data preparation - candidates with a first-set state, no quality skip, no first-set positive without polygon, shorter side at least 224 px; input 224 x 224
status: accepted
area: [datasets, training]
created: 2026-11-18
from: [DIS-033]
related: [DEC-065, DEC-066, DEC-068, DEC-044, DEC-053]
superseded_by:
---
# DEC-069: Epic 1 point 2 - data preparation

## Context

[DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md) (mission: upper-abdomen
anatomy segmentation) leaves to point 2 which samples enter, the minimum crop size, quality
skips, positives without a polygon, and the input size.
[DEC-066](DEC-066-epic1-model-task-label-set-softmax.md) (label-set softmax) fixes the first
set: liver, kidney, stomach, gallbladder. Options and the user's two count notebooks:
[DIS-033](../discussions/DIS-033-epic1-data-preparation.md).

## Decision

1. **Universe.** Every sample of the sample-label index v1 of 261023
   (`derived/sample_label_index_v1_df.pkl`), with the states of the `strict_v1` presence table
   (`derived/sample_label_presence_strictv1_df.pkl`).
2. **A sample is a candidate when none of these holds** (G+Q+C+S):

   | Flag | The sample is excluded when |
   |---|---|
   | G | no first-set organ is positive or negative under `strict_v1` |
   | Q | the sample has a quality-skip fact item (`n_quality > 0` in the index) |
   | C | a first-set organ is positive without a polygon (`has_polygon` false) |
   | S | the shorter side of the crop box is below **224 px** (pixels of the source image) |

   Table 1. Exclusion flags; a sample with any flag is out.
3. **Same filters for every split.** Train, val and test are cut from the candidates. The
   DEC-065 bar therefore covers crops with a shorter side of at least 224 px, without quality
   skips.
4. **Input.** 224 x 224; the crop is stretched to it (aspect not kept), as the reader does now
   (`src/sonoai/training/samples.py`). Outside the crop the image is 0 and the target is
   background (`us_mild_v2`, [DEC-068](DEC-068-us-mild-v2-zero-image-and-background-outside-the-crop.md)).
5. **Positives without a polygon** do not enter (flag C). DEC-066 rule 3b stays in the code,
   so a later version can let them in.
6. **DEC-066 assumptions kept.** A positive organ's polygons cover all of it in the crop
   (rule 3); first-set polygons overlap rarely (rule 8). The candidate build measures the
   overlap; a rule is added only if the counts call for it, in a new DEC.
7. **Candidate table first, sample file after point 3.** A versioned candidate table goes
   under `derived/` ([DEC-053](DEC-053-table-naming-and-preservation.md)) with a dataset record
   of aggregate counts: per flag and combination; per organ and state; lost share per
   datasource group; share of positive organ pairs whose polygon overlaps another first-set
   positive polygon; positives by polygon area inside the crop. The sample file with its split
   and its enc1 copy for the GPU box follow point 3 (splitting).

Departure from the DEC-065 starting lean (Table 3, row 2: "choice-only positives give no mask
loss"): they are excluded instead (the user's choice; simpler, and they are where the rule 3
assumption is weakest).

## Consequences

- Board: [TASK-163](../../backlog/tasks/task-163%20-%20Epic-1-anatomy-candidate-builder-GQCS-exclusion-flags-at-a-224-px-minimum-side-counts-per-flag-organ-state-and-datasource-group-first-set-polygon-overlap-and-in-crop-polygon-area-report-sonoai-data-command-synthetic-tests-DEC-069.md) (candidate builder and `sonoai-data` command, method), [TASK-164](../../backlog/tasks/task-164%20-%20Epic-1-anatomy-candidate-table-on-261023_plain-run-the-TASK-163-builder-at-224-px-dataset-record-with-counts-per-flag-organ-state-and-datasource-group-polygon-overlap-and-in-crop-area-DEC-069.md) (candidate
  table and dataset record on 261023, data, depends on TASK-163); [TASK-159](../../backlog/tasks/task-159%20-%20Anatomy-label-set-task-definition-a-registered-task-for-background-liver-kidney-stomach-and-gallbladder-whose-target-is-the-DEC-066-bitmask-built-by-label_set_target-from-each-samples-strict_v1-states-and-polygons.md) (anatomy label-set
  task kind, method) moves from Triage to To Do.
- Point 3 (splitting) starts from the TASK-164 counts.
- The minimum crop side is tied to the input size: a change of input size in point 5 or 6 does
  not change the minimum without a new DEC.
