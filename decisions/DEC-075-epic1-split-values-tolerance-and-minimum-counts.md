---
id: DEC-075
title: Epic 1 split values - 2-point gap tolerance for every organ, at least 200 positives and 300 negatives per organ in test and val, positive rate over all samples kept
status: accepted
area: [datasets, training]
created: 2026-11-18
from: [DIS-034]
related: [DEC-071, DEC-065, DEC-070, DEC-053]
superseded_by:
---
# DEC-075: Epic 1 split values

## Context

[DEC-071](DEC-071-epic1-splitting-parameterised-split-method.md) (parameterised split method)
item 9 leaves the gap tolerances and the minimum counts of epic 1 to the user, after a
feasibility report. The report is
[anatomy_e1_split.md](../datasets/261023/anatomy_e1_split.md) ([TASK-167](../../backlog/tasks/task-167%20-%20Epic-1-split-feasibility-report-on-261023-run-the-TASK-166-report-on-the-anatomy-candidate-table-at-tolerances-1-2-3-and-5-points-dataset-record-for-the-user-to-set-tolerances-and-minimum-counts-DEC-071.md), 261023, 20,011
eligible samples in 56 datasource groups; minimum counts 0 there). Discussion: follow-up of
[DIS-034](../discussions/DIS-034-epic1-splitting.md) (epic 1 splitting), 2026-11-18.

Terms as in the report: *gap* = positive rate of test minus that of train + val (val: minus
train), in percentage points; *tolerance* = the largest allowed absolute gap.

## Decision

1. **Gap tolerance: 2 points (0.02) for every organ** (liver, kidney, stomach, gallbladder).
2. **Minimum counts per organ: 200 positives and 300 negatives in test, and the same in val.**
3. **The balanced rate stays the positive rate over all samples** (DIS-034 point 2); no second
   rule on the positive share among labeled samples.
4. These values go into a new version (2) of `configs/data/splits/anatomy_e1.yaml`; the other
   values (shares, merge size 20, search, seed 0) stay. Then the freeze runs
   ([TASK-168](../../backlog/tasks/task-168%20-%20Freeze-the-epic-1-sample-file-on-261023-with-the-users-tolerances-and-minimum-counts-split-state-columns-enc1-copy-dataset-record-with-counts-per-split-and-class-DEC-071-DEC-070.md)). If no set fits, the freeze writes nothing and
   reports; the user decides again.

## Reasons

- **Tolerance 2 points.** In the report, the 2-point test set is the only one that meets the
  minimum counts of item 2 with margin (smallest: 268 gallbladder positives, 543 liver
  negatives in test), with 11 datasource groups, 10.83% of samples (target 10%) and every gap
  at most 1.72 points. The 1-point set had 183 gallbladder positives; the 3-point set had 6
  groups; the 5-point set had 244 kidney negatives and a +4.23-point stomach gap. The freeze
  searches again with the minimums, so its set may differ from the reported one.
- **Minimum counts.** W1 of [DEC-065](DEC-065-mission-upper-abdomen-anatomy-segmentation.md)
  is measured on positives and W2 on closed negatives. Analyst's arithmetic (normal
  approximation, not a run): a 95% CI on a W2 share of 0.90 is about ±3.4 points with 300
  negatives, about ±4.2 with 200; too narrow, since samples of one datasource group are not
  independent.
- **One rate.** The unknown share differs between test and train + val (1-point set: kidney
  30.32% against 22.03%), so the positive share among labeled samples differs by about 3 to
  18 points across the reported sets (analyst's arithmetic from the report's tables). W1 and W2
  are each computed on one state only, so this mix changes their counts and CI widths, not
  their values; item 2 covers the counts. A second rule would need new code and a new report.

## Alternatives

- 1-point tolerance: more test groups (15) and tighter balance; would win if source diversity
  in test mattered more than counts.
- Also balancing the positive share among labeled samples: would win if a metric pooled over
  states were reported, or test had to resemble train in label coverage.

## Consequences

- The dataset record of the freeze notes the unknown-share difference between test and
  train + val as a known limit.
- Reversal before training: a new spec version and a new freeze (minutes). After training: a
  new sample file and new runs.
