---
id: DIS-033
title: Epic 1 point 2 - data preparation - which samples enter, minimum crop size, input size, and what the candidate build measures
status: concluded
created: 2026-11-18
outcomes: [DEC-069]
related: [DEC-065, DEC-066, DEC-068, DEC-044, DEC-053]
---
# DIS-033: Epic 1 point 2 - data preparation

## Question

Point 2 of [DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md)
(mission: upper-abdomen anatomy segmentation), Table 3: which samples enter, the minimum crop
size, quality skips, positives without a polygon, and the input size. Point 1 is settled by
[DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md) (label-set softmax; first
set liver, kidney, stomach, gallbladder).

## Options considered

**1. Which samples enter.** The user counted, in a local notebook
(`notebooks/quick/strictv1-epic1-sample-exclusions.ipynb`, outputs not committed), the samples
of the sample-label index v1 left after four exclusion flags, alone and in every combination:

| Flag | A sample is excluded when |
|---|---|
| G (gate) | no first-set organ is positive or negative under `strict_v1` |
| Q (quality) | the sample has a quality-skip fact item (`n_quality > 0` in the sample-label index v1) |
| C (choice only) | a first-set organ is positive without a polygon (`has_polygon` false) |
| S (size) | the shorter side of the crop box is below the minimum |

Table 1. The four exclusion flags of the user's notebook.

- **Chosen: G+Q+C+S** (exclude on any flag). The user's reading: about 30% of the samples are
  lost, about the same as G alone, so Q, C and S mostly hit samples G already drops. The analyst
  did not see the notebook outputs (they are not saved) and noted that its combination tables
  used a placeholder minimum of 64 px; the user kept the choice without a recount. The candidate
  build task (below) reports the exact counts at 224 px.
- C departs from the DEC-065 starting lean ("choice-only positives give no mask loss"):
  DEC-066 rule 3b could train on such samples, with the organ allowed outside the other
  polygons. Excluding them is simpler, and these are the samples where the DEC-066 assumption
  "a positive organ's polygons cover all of it" is weakest.
- Alternative: G alone, with Q, C and S handled by the target and loss. Would win if C or S
  removed many positives of gallbladder or stomach.

**2. Minimum crop size.** The user's notebook `notebooks/quick/epic1-min-crop-size.ipynb`
(outputs not committed) shows the shorter-side distribution of the candidate crops and the drop
per candidate minimum, overall and per organ and state.

- **Chosen: 224 px** shorter side, equal to the input size, so no crop is upsampled.
- The cirrhosis sample set used 128 px ([DEC-044](../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md)
  rule 5, chosen 2026-11-05). 128 px would keep more small crops, upsampled at most 1.75 times.
- Risk named by the analyst: small crops may come from a few datasource groups; if 224 px
  removes most of a group, point 3 (splitting) has fewer groups to hold out. The candidate
  build task reports the share of each group that is lost.

**3. Further point-2 questions** (raised by the analyst; the user took the default of each):

| # | Question | Agreed |
|---|---|---|
| a | Input size and resize rule | 224 x 224; the crop is stretched to it (aspect not kept), as the reader does now |
| b | Do the filters apply to every split? | Yes: train, val and test use the same filters |
| c | DEC-066 rule 3 assumption (polygons cover the whole organ) and rule 8 (overlap rare, not measured) | Keep the assumption; the candidate build measures the overlap of first-set positive polygons |
| d | Positives with almost no polygon area inside the crop | No rule now; the candidate build reports how many there are |
| e | Sample file and order of work | Build the candidate table and its counts now; fix the sample file with its split after point 3; the GPU box needs an enc1 copy then |

Table 2. Point-2 questions beyond the four flags, with what was agreed.

## Conclusion

[DEC-069](../decisions/DEC-069-epic1-data-preparation.md): candidate samples are those with
none of G, Q, C, S (minimum shorter side 224 px), the same filters for every split, input
224 x 224 by stretching. Board: [TASK-163](../../backlog/tasks/task-163%20-%20Epic-1-anatomy-candidate-builder-GQCS-exclusion-flags-at-a-224-px-minimum-side-counts-per-flag-organ-state-and-datasource-group-first-set-polygon-overlap-and-in-crop-polygon-area-report-sonoai-data-command-synthetic-tests-DEC-069.md) (candidate builder, method), [TASK-164](../../backlog/tasks/task-164%20-%20Epic-1-anatomy-candidate-table-on-261023_plain-run-the-TASK-163-builder-at-224-px-dataset-record-with-counts-per-flag-organ-state-and-datasource-group-polygon-overlap-and-in-crop-area-DEC-069.md) (candidate table
and dataset record on 261023, data); [TASK-159](../../backlog/tasks/task-159%20-%20Anatomy-label-set-task-definition-a-registered-task-for-background-liver-kidney-stomach-and-gallbladder-whose-target-is-the-DEC-066-bitmask-built-by-label_set_target-from-each-samples-strict_v1-states-and-polygons.md)
(anatomy label-set task kind, method) leaves Triage.

## Open questions

- The sample file with its split column, and its enc1 copy for the GPU box: point 3
  (splitting).
- Whether the overlap or tiny-area counts call for a new rule: decided after TASK-164 reports
  them.
