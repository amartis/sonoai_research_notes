---
id: DEC-108
title: Epic 3 split - test 15% and validation 15% by whole datasource groups, training the rest; 3-point tolerance and minimum counts per class; one split for every presence policy
status: accepted
area: [datasets, training]
created: 2026-11-25
from: [DIS-063]
related: [DEC-044, DEC-053, DEC-071, DEC-075, DEC-100, DEC-103]
superseded_by:
---
# DEC-108: Epic 3 split by whole datasource groups

## Context

Point 7 (split) of the epic 3 handoff in [DIS-056](../discussions/DIS-056-epic3-spot-liver-disease-mission.md) (the epic 3 mission discussion). The counts, the
candidate splits and the explanation the user asked for are in
[DIS-063](../discussions/DIS-063-epic3-split-by-datasource-groups.md) (the epic 3 split discussion).
[DEC-100](DEC-100-epic3-mission-spot-liver-diseases.md) (the epic 3 mission) rule 3 asks one split,
made once, for every presence policy, with strict_v1 on index v2 as the truth of validation and test.
The split method of Epic 1 ([DEC-071](DEC-071-epic1-splitting-parameterised-split-method.md), the
parameterised split method) draws test by whole datasource groups but validation by image.

## Decision

1. **Samples to split.** The samples of 261023 with a known state (positive or negative) under
   strict_v1 on index v2 for at least one of the four spot classes (`hepatoma`, `hemangioma`,
   `hepatic_cyst`, `hepatic_stone`): 16,176 samples in 57 datasource groups at the time of
   DIS-063. One split for strict_v1 and loose_v1 (and posrich_v1); only the training labels differ.
2. **Whole groups for test and validation.** Test is whole datasource groups, target 15% of the
   samples (range 13% to 18%). Validation is also whole datasource groups, target 15% (range 12% to
   20%), chosen from the groups not in test by the same rules as test. Training is the rest (about
   70%). No group is in two splits. This adds an option to the DEC-071 method; Epic 1 keeps
   validation by image.
3. **Limits.** Balanced classes: the four spot classes and the cirrhosis negatives (a hepatoma
   negative with cirrhosis positive, against a hepatoma negative with cirrhosis negative;
   [DEC-103](DEC-103-epic3-negatives-and-contested-labels.md), epic 3 negatives and contested
   labels, rule 3). Tolerance 3 points for each (positive rate over all samples, unknown included, as
   in DEC-071); it binds for hepatoma and stone, and the minimum counts bind for the rarer classes.
   Minimum positives in test: hepatoma 250, hemangioma 40, cyst 22, stone 60, cirrhosis negatives
   80. In validation: hepatoma 100, hemangioma 15, cyst 8, stone 25, cirrhosis negatives 40. No
   minimum negatives (each class has thousands). Ascites is not balanced (DEC-100 rule 2).
4. **Search and stop.** As DEC-071: seeded (seed 0), every subset when the groups are few, else
   20,000 random tries; among the sets that fit, the one closest to the target share, then the
   smallest largest gap. If no set fits, nothing is written and the closest options are reported;
   the user decides.
5. **Output.** A sample file under `derived/` with a new versioned name
   ([DEC-053](DEC-053-table-naming-and-preservation.md), table naming and preservation) and its enc1
   copy, as DEC-071 item 6 (output); its dataset record gives, per split and class, samples,
   positives, negatives, groups with a positive, the largest group's share, the four parts of the
   negatives of DEC-103 rule 2, and the contested samples per split.
6. **Validation scores are given with their interval over groups.** Because validation rests on a
   few groups (2 or 3 for hepatoma in DIS-063), every validation score of epic 3 is reported with a
   95% interval from a bootstrap over datasource groups, as in [EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md) (the cirrhosis runs).

## Consequences

- Validation estimates the score on unseen sources, as test does; its scores are noisier than with
  validation by image.
- At 15% test, hemangioma and cyst test positives come from 2 to 5 groups (DIS-063 Table 2); their
  results stay without a bar (DEC-100 rule 4).
- Code: [TASK-278](../../backlog/tasks/task-278%20-%20Split-method-validation-by-whole-test-units-as-a-spec-option-and-the-epic-3-table-of-samples-to-split-with-its-sonoai-data-command-synthetic-tests-DEC-108.md) (method) adds whole-group validation to `sonoai.data.splitting` (synthetic tests;
  Epic 1 unchanged) and builds the epic 3 table of samples to split; then [TASK-279](../../backlog/tasks/task-279%20-%20Epic-3-split-on-261023-build-the-table-of-samples-to-split-run-the-feasibility-report-freeze-the-sample-file-with-the-DEC-108-limits-and-its-enc1-copy-dataset-record-per-split-and-class-DEC-108.md) (data) builds it,
  runs the report, freezes the sample file and writes the record.
- Reversal: before training, a new spec version and a new freeze; after training, new runs.
