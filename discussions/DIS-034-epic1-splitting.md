---
id: DIS-034
title: Epic 1 point 3 - splitting - keep the DEC-044 principles, balance every class's positive rate, one parameterised split method for later projects
status: concluded
created: 2026-11-18
outcomes: [DEC-071, DEC-075]
related: [DEC-065, DEC-044, DEC-069, DEC-070, DEC-053, DIS-030]
---
# DIS-034: Epic 1 point 3 - splitting

## Question

Point 3 of [DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md)
(mission: upper-abdomen anatomy segmentation), Table 3: test and val units, sizes, class
coverage per split. The starting lean was "test and val both held out by datasource group",
because in the cirrhosis model the random val ([DEC-044](../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 10) could not show the test failure
(val DSC 0.696, test DSC 0.047, [EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md)).
The first set is liver, kidney, stomach, gallbladder
([DEC-066](../decisions/DEC-066-epic1-model-task-label-set-softmax.md)); each sample has a
`strict_v1` state per organ: positive, negative or unknown
([DEC-070](../decisions/DEC-070-anatomy-label-set-task-states-in-sample-file.md)).

The user also asked for one split method that later projects reuse by changing parameter
values only.

## Options considered

**1. Val unit.**

- **Chosen (the user): the DEC-044 principles.** Test held out by datasource group, val at
  random from the remaining groups. The user's reason: with val also held out by group, val
  and test are the same kind of split and there is no intrinsic difference between them.
- Analyst's view, said once: the difference would be in use (val selects the checkpoint, test
  is used once), and a random val cannot show a drop on new datasources during model
  selection. Under the user's choice, criterion W3 of DEC-065 (val DSC minus test DSC ≤ 0.10)
  is the measure of generalisation, seen only after training.

**2. Which positive rate is balanced.** Per class, a sample is positive, closed negative or
unknown.

- **Chosen: positives over all samples of the split**, plus a minimum count of positives and
  of closed negatives per class in test (W1 needs positives, W2 needs closed negatives).
- Alternative: positives over known samples (positive or negative). Would win if unknown
  shares differ a lot between datasources and only the balance the loss sees mattered.
- Both rates at once: strictest, may leave no feasible test set with about 50 groups.

**3. How val is balanced over several classes.**

- **Chosen: positive-pattern strata.** Each image is stratified by which classes are positive
  on it (up to 16 patterns for 4 classes); rare patterns are merged; then each class's rate is
  checked.
- Alternative: iterative stratification for multi-label data (Sechidis, Tsoumakas and Vlahavas
  2011; citation unverified). Would win with many classes (more than about 8), where patterns
  become too sparse.
- No stratification, check only: simplest; may fail the check for rare classes.

**4. When the tolerance and the minimum counts are set.**

- **Chosen: after a feasibility report.** The code takes them as parameters; a data task
  first reports, on the point-2 candidate table, the best achievable per-class gap and counts
  at several tolerances; the user picks; then the sample file is frozen.
- Alternative: fix now at 2 percentage points for every class (DEC-044 rule 9). Loose for rare
  classes (a 10% rate may then be 8–12%).

**5. Where the code lives** (analyst's call, reversible). A new module with a YAML spec per
split; the DEC-044 code in `src/sonoai/data/sample_sets.py` stays as is, so the frozen
cirrhosis v4 sample file still checks against it.

## Conclusion

[DEC-071](../decisions/DEC-071-epic1-splitting-parameterised-split-method.md): the
parameterised split method and its use for epic 1. Board: [TASK-166](../../backlog/tasks/task-166%20-%20Parameterised-split-method-test-by-datasource-groups-with-every-classs-positive-rate-balanced-val-by-image-stratified-by-positive-pattern-feasibility-report-sonoai-data-command-synthetic-tests-DEC-071.md) (split method, method),
[TASK-167](../../backlog/tasks/task-167%20-%20Epic-1-split-feasibility-report-on-261023-run-the-TASK-166-report-on-the-anatomy-candidate-table-at-tolerances-1-2-3-and-5-points-dataset-record-for-the-user-to-set-tolerances-and-minimum-counts-DEC-071.md) (feasibility report on 261023, data), [TASK-168](../../backlog/tasks/task-168%20-%20Freeze-the-epic-1-sample-file-on-261023-with-the-users-tolerances-and-minimum-counts-split-state-columns-enc1-copy-dataset-record-with-counts-per-split-and-class-DEC-071-DEC-070.md) (freeze of the epic 1 sample file, data,
Parked until the user sets the tolerances); links in DEC-071 Consequences.

## Follow-up 2026-11-18: values after the feasibility report

After the TASK-167 report ([anatomy_e1_split.md](../datasets/261023/anatomy_e1_split.md)) the
user chose, on the analyst's recommendation: a 2-point tolerance for every organ; at least 200
positives and 300 negatives per organ in test and val; and to keep point 2 (positive rate over
all samples) although the unknown share differs between test and train + val, because W1 and W2
are computed on one state each. Record: [DEC-075](../decisions/DEC-075-epic1-split-values-tolerance-and-minimum-counts.md).

## Open questions

- ~~Tolerance per class and the minimum test counts~~: set in DEC-075.
- Whether the cirrhosis and B-mode detector sample builders move to the new method: not now;
  a later task if wanted.
