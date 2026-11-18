---
id: DEC-071
title: Epic 1 point 3 - splitting - one parameterised split method (test by datasource group, val at random by image, every class's positive rate balanced); epic 1 uses it after a feasibility report
status: accepted
area: [datasets, training]
created: 2026-11-18
from: [DIS-034]
related: [DEC-065, DEC-044, DEC-066, DEC-069, DEC-070, DEC-053, DEC-024]
superseded_by:
---
# DEC-071: Epic 1 point 3 - a parameterised split method

## Context

[DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md) (mission: upper-abdomen
anatomy segmentation) point 3 asks for the test and val units, sizes and class coverage.
[DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) (cirrhosis split) rules
8–11 balance one class and have their limits in code. Epic 1 has four classes (liver, kidney,
stomach, gallbladder, [DEC-066](DEC-066-epic1-model-task-label-set-softmax.md)), each with a
`strict_v1` state per sample ([DEC-070](DEC-070-anatomy-label-set-task-states-in-sample-file.md)).
Options and reasons: [DIS-034](../discussions/DIS-034-epic1-splitting.md).

Terms: a **datasource group** is a set of datasources that share an image (DEC-044 rule 2). A
sample's **positive rate** for a class, in a split, is the number of samples positive for that
class divided by all samples of the split.

## Decision

### The method (general; every value below is a parameter)

1. **Principles kept from DEC-044.** Seeded and reproducible. Test is whole datasource groups;
   no group is in test and in train or val. Val is drawn at random from the rest, whole images
   at a time (all crops of one image hash in one split). If no split meets the rules, the
   method stops and reports the closest options; the user decides.
2. **A split spec** (one YAML file per use, versioned) holds: the test unit column (default
   datasource group), the val unit column (default image hash), target share and allowed range
   per split (default train 75% [70–85%], val 15% [15–23%], test 10% [8–13%]), the class columns
   with their positive and negative values (a sample with neither is unknown for that class),
   the tolerance per class, the minimum positives and minimum negatives per class in test and in
   val, the rare-pattern merge size, the search settings (exhaustive limit, tries) and the seed.
3. **Test.** Among sets of whole test units whose sample share is in the test range, every
   class's test positive rate is within its tolerance of the rate in the rest (train + val), and
   every class has at least its minimum positives and negatives in test: the set closest to the
   target share, then the smallest largest gap (gap divided by tolerance), then the lowest unit
   ids. Every subset is tried when the units are few; otherwise seeded random greedy fills
   (DEC-044 search).
4. **Val.** Each val unit (image) has a **positive pattern**: the set of classes positive on any
   of its samples. Units are stratified by pattern; patterns with fewer units than the merge
   size are merged into one stratum. Per stratum, units in seeded random order go to val until
   val holds the target share. Then each class's val positive rate must be within its tolerance
   of train's, with the minimum counts; otherwise the method stops and reports.
5. **Feasibility report.** Without writing anything, the method reports for a list of
   tolerances whether a test set exists and, for the best one, per class and split: samples,
   positives, negatives, unknown, positive rate (95% Wilson CI) and gap. Aggregates only.
6. **Output.** A sample file under `derived/` with a new versioned name
   ([DEC-053](DEC-053-table-naming-and-preservation.md)), one row per sample with its split and
   the columns the task needs; its attrs hold the split spec and its sha256. An enc1 copy for
   the GPU box ([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).
7. **Code.** A new module with the method and a `sonoai-data` command (report and freeze),
   tested on synthetic data. The DEC-044 code (`src/sonoai/data/sample_sets.py`) is not changed,
   so the frozen cirrhosis v4 sample file still checks against it.

### Use in epic 1

8. **Input:** the point-2 candidate table of 261023
   ([DEC-069](DEC-069-epic1-data-preparation.md)). Classes: `state_liver`, `state_kidney`,
   `state_stomach`, `state_gallbladder`, positive value `positive`, negative value `negative`.
   Default shares and ranges of item 2.
9. **Tolerances and minimum counts are set by the user after the feasibility report** on the
   real candidates (DIS-034 point 4). Then the sample file is frozen with the `state_*` columns
   (DEC-070 rule 2) and a dataset record gives counts per split and class.

## Consequences

- Validation shares datasources with train, so val scores are optimistic (as in DEC-044);
  generalisation is judged by DEC-065 criterion W3 on test.
- Later projects write a new split spec; a code change is needed only for a new kind of rule.
- Board: [TASK-166](../../backlog/tasks/task-166%20-%20Parameterised-split-method-test-by-datasource-groups-with-every-classs-positive-rate-balanced-val-by-image-stratified-by-positive-pattern-feasibility-report-sonoai-data-command-synthetic-tests-DEC-071.md) (split method and `sonoai-data` command, method);
  [TASK-167](../../backlog/tasks/task-167%20-%20Epic-1-split-feasibility-report-on-261023-run-the-TASK-166-report-on-the-anatomy-candidate-table-at-tolerances-1-2-3-and-5-points-dataset-record-for-the-user-to-set-tolerances-and-minimum-counts-DEC-071.md) (feasibility report on 261023, data, after TASK-166 and [TASK-164](../../backlog/tasks/task-164%20-%20Epic-1-anatomy-candidate-table-on-261023_plain-run-the-TASK-163-builder-at-224-px-dataset-record-with-counts-per-flag-organ-state-and-datasource-group-polygon-overlap-and-in-crop-area-DEC-069.md), the
  candidate table on 261023); [TASK-168](../../backlog/tasks/task-168%20-%20Freeze-the-epic-1-sample-file-on-261023-with-the-users-tolerances-and-minimum-counts-split-state-columns-enc1-copy-dataset-record-with-counts-per-split-and-class-DEC-071-DEC-070.md) (freeze of the epic 1 sample file, data, Parked
  `needs-decision` until the user sets the tolerances and minimum counts).
