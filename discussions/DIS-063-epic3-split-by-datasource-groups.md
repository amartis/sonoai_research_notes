---
id: DIS-063
title: Epic 3 point 7 - the split by datasource groups (test and validation by whole groups, size and limits)
status: concluded
created: 2026-11-25
outcomes: [DEC-108]
related: [DIS-034, DIS-056, DIS-058, DEC-044, DEC-071, DEC-075, DEC-100, DEC-103, EXP-003]
---
# DIS-063: Epic 3 point 7 - the split by datasource groups

## Question

[TASK-270](../../backlog/tasks/task-270%20-%20Decide-epic-3-point-7-one-datasource-group-split-for-every-policy-with-enough-cirrhosis-negatives-in-test-DIS-056.md) (decide the epic 3 split) takes up point 7 (split) of the handoff in
[DIS-056](DIS-056-epic3-spot-liver-disease-mission.md) (the epic 3 mission discussion): one split,
made once, for every presence policy ([DEC-100](../decisions/DEC-100-epic3-mission-spot-liver-diseases.md),
the epic 3 mission, rule 3). To settle: how large the test set is, how validation is drawn, and
which limits the split must meet. The sample-label index v2 (the index of [TASK-264](../../backlog/tasks/task-264%20-%20Build-the-261023-sample-label-index-v2-labeling-group-skip-and-the-strict_v1-and-loose_v1-presence-tables-on-it-dataset-record-with-counts-per-class-and-state-against-v1-DEC-101.md), record
[sample_label_index_v2.md](../datasets/261023/sample_label_index_v2.md)) is built.

## Facts checked

Counts from three tables of 261023_plain that the user approved for this session: the taskcrops
table (datasource group of each sample), the strict_v1 presence table on index v2 (the truth for
validation and test, DEC-100 rule 3) and index v2 itself (the contested pairs of projects 35 and 36,
which are not in the presence table). Read only, in memory, aggregates only, nothing written.

**The samples to split.** A sample with a known state (positive or negative) for at least one of
the four spot classes (`hepatoma`, `hemangioma`, `hepatic_cyst`, `hepatic_stone`): 16,176 samples
in 57 datasource groups. Positives: hepatoma 1,417 (18 groups), hemangioma 204 (13), cyst 116
(12), stone 298 (38), ascites 122 (10). Cirrhosis negatives (a hepatoma negative with cirrhosis
positive, the part with its own bar in [DEC-103](../decisions/DEC-103-epic3-negatives-and-contested-labels.md),
epic 3 negatives and contested labels, rule 3): 470 in 26 groups. The largest group holds 19% of
the samples, the five largest 45%; 19 groups have fewer than 50 samples. The largest group of
hepatoma positives holds 35% of them; the three largest hold 55%.

**How the candidate splits were made.** The split method of Epic 1
([DEC-071](../decisions/DEC-071-epic1-splitting-parameterised-split-method.md), the parameterised
split method; `sonoai.data.splitting`) run in memory on these samples, seed 0, 20,000 random tries.
Classes balanced: the four spot classes and the cirrhosis negatives. A freeze can find another set.

| Test share (val by image) | Test groups | Hepatoma test positives (groups; largest group's share) | Hemangioma | Cyst | Stone | Cirrhosis negatives | Hepatoma train positives |
|---|---:|---|---:|---:|---:|---:|---:|
| 10% | 11 | 159 (4; 83%) | 23 | 12 | 37 | 77 | 1,047 |
| 15%, with the limits of DEC-108 | 11 | 257 (7; 50%) | 79 | 33 | 83 | 105 | 953 |
| 20% | 16 | 331 (6; 40%) | 92 | 37 | 90 | 124 | 881 |

Table 1. Candidate test sets at three sizes, validation drawn by image as in Epic 1. Counts are
test positives unless the column says otherwise.

Wilson 95% intervals for a measured 0.80 (analyst's arithmetic): 159 positives 0.73 to 0.86, 257
about 0.75 to 0.85, 331 0.75 to 0.84; for the cirrhosis bar, 77 negatives 0.69 to 0.88, 124 0.72
to 0.86. Samples of one group are not independent, so these are too narrow.

**Validation by whole groups** (the method cannot do it yet; simulated by choosing the val groups
with the same search among the groups not in test), 15% test and 15% val, with the limits of
DEC-108, three seeds:

| Seed | Groups test / val / train | Hepatoma val positives (groups; largest share) | Hemangioma val | Cyst val | Test hepatoma (groups) | Test hemangioma (groups) | Test cyst (groups) |
|---|---|---|---|---|---|---|---|
| 0 | 11 / 6 / 38 | 193 (2; 68%) | 26 | 17 (1 group) | 257 (7) | 79 (2) | 33 (2) |
| 1 | 17 / 6 / 32 | 197 (3; 67%) | 22 | 17 (1 group) | 251 (5) | 79 (2) | 33 (2) |
| 2 | 16 / 9 / 30 | 208 (3; 63%) | 22 | 17 (1 group) | 264 (6) | 81 (3) | 38 (5) |

Table 2. Whole-group validation at 15% test. Val by image at the same test share gives hepatoma 207
val positives from many groups, hemangioma 24, cyst 15.

- **Contested samples** (304 samples of projects 35 and 36, DEC-103 rule 4) lie in 4 groups of
  684, 558, 501 and 496 samples. In the candidate sets one or two of these groups fall in test
  (99 to 191 contested samples there), so the separate table of DEC-103 rule 5 can be made.
- **Why validation by image is optimistic.** The cirrhosis split drew val by image
  ([DEC-044](../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md), the cirrhosis
  sample set, which already warned that val shares datasources and maybe patients with train); the
  model scored 0.696 DSC on val and 0.047 on test
  ([EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md),
  the cirrhosis runs). Probably not the only cause: that test had 64 positives in 4 groups.

## Options considered

| # | Question | Analyst's recommendation | Chosen by the user (2026-11-25) |
|---|---|---|---|
| 1 | Test size | 20% (hepatoma 331 positives from 6 groups) | **15%** |
| 2 | How validation is drawn | Whole datasource groups, like test | **Whole groups**, after an explanation with examples (below) |
| 3 | Limits | 3-point tolerance; minimum test and val positives as in DEC-108 rule 3 | **As recommended** |

Table 3. The three questions as put and answered.

Point 2 (how validation is drawn) was explained to the user before the choice: validation makes
four decisions for epic 3 (the epoch kept, the image-level threshold, the check that val minus test
is at most 0.10, and which policy and recipe wins), each as if its score were the score on unseen
sources. A datasource group shares device, protocol, screen marks, labelers and probably patients,
so val by image measures sources the model has seen, and val by whole groups measures unseen ones,
as test does. The cost: whole-group val rests on 2 or 3 groups for hepatoma and 1 for cyst (Table 2),
so it is noisier. Examples given: a threshold that meets the bar on val by image and misses it on
new groups; an epoch choice that keeps rising on val by image while the model memorises sources;
EXP-003.

Not chosen:
1. 20% test (more test groups and narrower intervals; 16% fewer hepatoma positives to train on) and
   10% test (as Epic 1; hepatoma test nearly one group's result).
2. Two validation sets: a small by-image set for the epoch choice and a whole-group set for the
   threshold, the gap check and the comparisons (wins if 2 or 3 groups make the epoch choice too
   random); validation by image as Epic 1 (no code; steady but optimistic).
3. Setting the limits after a feasibility report of the real run, as in Epic 1.

## Conclusion

Accepted by the user on 2026-11-25: [DEC-108](../decisions/DEC-108-epic3-split-test-and-validation-by-whole-groups.md)
(epic 3 split). Board: [TASK-278](../../backlog/tasks/task-278%20-%20Split-method-validation-by-whole-test-units-as-a-spec-option-and-the-epic-3-table-of-samples-to-split-with-its-sonoai-data-command-synthetic-tests-DEC-108.md) (method: validation by whole groups in the split method, and the
epic 3 table of samples to split); then [TASK-279](../../backlog/tasks/task-279%20-%20Epic-3-split-on-261023-build-the-table-of-samples-to-split-run-the-feasibility-report-freeze-the-sample-file-with-the-DEC-108-limits-and-its-enc1-copy-dataset-record-per-split-and-class-DEC-108.md) (data: builds that table, runs the report, freezes
the sample file and writes its dataset record).

Said once by the analyst: at 15% test, hemangioma test positives come from 2 or 3 groups; a 20% test
would have had 4.

## Open questions

- Whether the input size of point 12 (input size) of DIS-056 drops small samples: that would remove
  samples inside each split, not move groups.
