# Epic 3 split on 261023: frozen sample file by whole datasource groups (TASK-279)

[TASK-279 (epic 3 split on 261023)](../../../backlog/tasks/task-279%20-%20Epic-3-split-on-261023-build-the-table-of-samples-to-split-run-the-feasibility-report-freeze-the-sample-file-with-the-DEC-108-limits-and-its-enc1-copy-dataset-record-per-split-and-class-DEC-108.md), [DEC-108 (epic 3 split: test 15% and validation 15% by whole datasource groups)](../../decisions/DEC-108-epic3-split-test-and-validation-by-whole-groups.md), [DEC-103 (epic 3 negatives and contested labels)](../../decisions/DEC-103-epic3-negatives-and-contested-labels.md), [DIS-063 (epic 3 split discussion)](../../discussions/DIS-063-epic3-split-by-datasource-groups.md). Aggregates only: no images, file names, folder names, datasource ids or table rows. Counts of 1 to 4 are shown as "<5"; a rate or share over fewer than 5 samples is shown as "-".

**Status: frozen on 2026-11-26 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md), plain style for local research). Not reviewed.** The table of samples to split and the feasibility report were made by this task (the data agent); the freeze (`sonoai-data split freeze`) was run by the user, because it needs the data passphrase for the enc1 copy. Reporting checklists (CLAIM, STARD): not applicable (no model; a split is made and described).

**Terms used.** *Datasource group* = datasources joined because an image occurs under both; the unit of test and validation here. *Sample* = one crop of the sample-label index v2. *Positive, negative, unknown* = the state of a class under strict_v1 (the presence policy that counts only certain labels) on index v2; a contested pair (a labeling task gives the label and another answers closed or open, [DEC-103](../../decisions/DEC-103-epic3-negatives-and-contested-labels.md) rule 4) is unknown. *Positive rate* = positives over all samples of the split, unknown included; the 95% CI is a Wilson interval on samples, too narrow because samples of one group are not independent. *Cirrhosis negatives* = samples where hepatoma is negative and cirrhosis is positive (a balanced class, DEC-103 rule 3; in Table 1 its "negatives" column is hepatoma negative with cirrhosis negative). *Four parts of the negatives* = DEC-103 rule 2: cirrhosis, other diffuse disease, none, not known. *Largest group's share* = positives of the group with most positives over the positives of the split. *Sample file* = the table listing every sample with its `split`. *Enc1 copy* = the encrypted copy of the sample file in the `261023_enc1` store.

## Summary

1. **The freeze passed every check of the spec** ([DEC-108](../../decisions/DEC-108-epic3-split-test-and-validation-by-whole-groups.md) rules 2 to 4): 16,176 samples in 55 datasource groups; train 11,329 (70.04%) in 30 groups, validation 2,426 (15.00%) in 14 groups, test 2,421 (14.97%) in 11 groups. No group and no image is in two splits (checked on the sample file).
2. **Test equals the candidate of [DIS-063](../../discussions/DIS-063-epic3-split-by-datasource-groups.md) Table 1 (15% test row) in every count** (257, 79, 33, 83 and 105 positives). Validation by whole groups has 14 groups, not the 6 of the DIS-063 simulation.
3. **Thin spots (observations):** validation hepatoma 193 positives from fewer than 5 groups (largest 68%); validation hemangioma 22 and cyst 19 positives, cyst with a largest group at 89.5%; test hemangioma and cyst positives each from fewer than 5 groups (largest 89.9% and 81.8%); ascites has fewer than 5 positives in validation (not balanced, [DEC-100](../../decisions/DEC-100-epic3-mission-spot-liver-diseases.md) rule 2).
4. **The contested samples** (303 in the table, in fewer than 5 groups) are 112 in train, none in validation and 191 in test.
5. **DEC-108 says 57 datasource groups; the data has 55.** The same 16,176 samples hold 55 groups (builder, report and sample file). DIS-063's own Table 2 sums to 55 (11 + 6 + 38 groups), so "57" in DIS-063 text and DEC-108 rule 1 looks like a slip; I did not change either record.

## Method

**Tables** (plain style through `sonoai.paths.dataset_dir`, [DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md), approved for this task on 2026-11-25): read `images/taskcrops_df.pkl`, `derived/sample_label_index_v2_df.pkl`, `derived/sample_label_presence_strictv1_indexv2_df.pkl`, and the sample file for the numbers below. Written, all new ([DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md), a written table is not changed): `derived/spot_e3_candidates_v1_261023_plain_df.pkl` (and `.xlsx`), the table of samples to split; `derived/spot_e3_samples_v1_261023_plain_df.pkl`, the sample file (24 columns, 16,176 rows), and its enc1 copy at the same path in the `261023_enc1` store (checked by size and time only, not decrypted: file names in the store are encrypted, so I saw that its manifest and one new file of about the size of the plain file were written at the freeze).

Commands (the first writes only the new table; the report writes nothing; the freeze wrote the sample file and its enc1 copy):

```bash
sonoai-data spot-e3-candidates 261023_plain
sonoai-data split report 261023_plain --spec configs/data/splits/spot_e3.yaml
sonoai-data split freeze 261023_plain --spec configs/data/splits/spot_e3.yaml
```

| Item | Value |
|---|---|
| Code commit | `16551e4683ee42e709029545eba34c1dfb7ed5eb` (master when run; builder and split method are in it, from [TASK-278](../../../backlog/tasks/task-278%20-%20Split-method-validation-by-whole-test-units-as-a-spec-option-and-the-epic-3-table-of-samples-to-split-with-its-sonoai-data-command-synthetic-tests-DEC-108.md) (split method and table of samples to split)) |
| Builder config | `configs/data/spot_e3.yaml`, version 1 (index v2, policy strict_v1) |
| Split spec | `configs/data/splits/spot_e3.yaml`, name `spot_e3_samples`, version 1 |
| Spec sha256 | `564b9c242b7755f77d420d83c0842908e3714e17eeb6508a39bcf87c8a35446e` (checked equal to the spec file in the worktree) |
| Table of samples to split, sha256 | `3df7ef021d7b581cbb58728451c8f1393e4f4c7e98d63211a5edcc7096d3c066` |
| Sample file, sha256 | `5744cb68dc9c5d8ee3729123be7397d5642f2e923d2895b8d2edfce1a8dd1ec8` (checked equal to the file in `derived/`) |
| Search | 55 groups are above `exhaustive_max` 16: seeded random greedy fill, 20,000 tries, seed 0, test first, then validation from the other groups ([DEC-108](../../decisions/DEC-108-epic3-split-test-and-validation-by-whole-groups.md) rule 4) |
| Tolerance and minimums | 3 points for each of five balanced classes; minimum positives in test (hepatoma 250, hemangioma 40, cyst 22, stone 60, cirrhosis negatives 80) and validation (100, 15, 8, 25, 40) |

## Results

Table 1. Samples, states, positive rate and group concentration per split and class. n = 16,176 samples in 55 groups; train 30 groups, validation 14, test 11. "Groups with a positive" = datasource groups holding at least one positive of the class in that split.

| Class | Split | Samples | Positives | Negatives | Unknown | Positive rate, % (95% CI) | Groups with a positive | Largest group's share of the positives, % |
|---|---|---|---|---|---|---|---|---|
| hepatoma | train | 11,329 | 967 | 10,139 | 223 | 8.54 (8.04-9.06) | 9 | 52.0 |
| hepatoma | val | 2,426 | 193 | 2,162 | 71 | 7.96 (6.94-9.10) | <5 | 68.4 |
| hepatoma | test | 2,421 | 257 | 2,005 | 159 | 10.62 (9.45-11.91) | 7 | 49.8 |
| hemangioma | train | 11,329 | 103 | 11,092 | 134 | 0.91 (0.75-1.10) | 9 | 53.4 |
| hemangioma | val | 2,426 | 22 | 2,333 | 71 | 0.91 (0.60-1.37) | <5 | 72.7 |
| hemangioma | test | 2,421 | 79 | 2,275 | 67 | 3.26 (2.63-4.05) | <5 | 89.9 |
| hepatic cyst | train | 11,329 | 64 | 11,133 | 132 | 0.56 (0.44-0.72) | 8 | 54.7 |
| hepatic cyst | val | 2,426 | 19 | 2,336 | 71 | 0.78 (0.50-1.22) | <5 | 89.5 |
| hepatic cyst | test | 2,421 | 33 | 2,361 | 27 | 1.36 (0.97-1.91) | <5 | 81.8 |
| hepatic stone | train | 11,329 | 184 | 11,101 | 44 | 1.62 (1.41-1.87) | 20 | 26.1 |
| hepatic stone | val | 2,426 | 31 | 2,371 | 24 | 1.28 (0.90-1.81) | 8 | 29.0 |
| hepatic stone | test | 2,421 | 83 | 2,304 | 34 | 3.43 (2.77-4.23) | 10 | 43.4 |
| ascites (not balanced) | train | 11,329 | 89 | 9,303 | 1,937 | 0.79 (0.64-0.97) | 5 | 60.7 |
| ascites (not balanced) | val | 2,426 | <5 | 636 | 1,788 | - | <5 | - |
| ascites (not balanced) | test | 2,421 | 31 | 2,043 | 347 | 1.28 (0.90-1.81) | <5 | 87.1 |
| cirrhosis negatives | train | 11,329 | 305 | 9,698 | 1,326 | 2.69 (2.41-3.01) | 14 | 30.8 |
| cirrhosis negatives | val | 2,426 | 60 | 2,101 | 265 | 2.47 (1.93-3.17) | <5 | 60.0 |
| cirrhosis negatives | test | 2,421 | 105 | 1,810 | 506 | 4.34 (3.60-5.22) | 8 | 34.3 |

Every balanced class passed its checks in the report: gaps in positive rate are within 3 points (test against train plus validation: hemangioma +2.35, hepatoma +2.18, stone +1.87, cirrhosis negatives +1.68, cyst +0.76; validation against train within 0.58) and the minimum positives are met. The test positive rate is above that of train for every class, within the tolerance.

Table 2. The four parts of the negatives ([DEC-103](../../decisions/DEC-103-epic3-negatives-and-contested-labels.md) rule 2) per split, for the negatives of each spot class and for the samples negative for all four. "Negatives" = row total (the four parts add up to it).

| Negatives of | Split | Negatives | Cirrhosis | Other diffuse disease | None | Not known |
|---|---|---|---|---|---|---|
| hepatoma | train | 10,139 | 305 | 6,020 | 3,546 | 268 |
| hepatoma | val | 2,162 | 60 | 1,689 | 387 | 26 |
| hepatoma | test | 2,005 | 105 | 990 | 671 | 239 |
| hemangioma | train | 11,092 | 937 | 6,246 | 3,542 | 367 |
| hemangioma | val | 2,333 | 175 | 1,745 | 387 | 26 |
| hemangioma | test | 2,275 | 181 | 1,054 | 672 | 368 |
| hepatic cyst | train | 11,133 | 956 | 6,265 | 3,544 | 368 |
| hepatic cyst | val | 2,336 | 185 | 1,738 | 387 | 26 |
| hepatic cyst | test | 2,361 | 180 | 1,107 | 672 | 402 |
| hepatic stone | train | 11,101 | 961 | 6,216 | 3,506 | 418 |
| hepatic stone | val | 2,371 | 184 | 1,743 | 365 | 79 |
| hepatic stone | test | 2,304 | 181 | 1,087 | 647 | 389 |
| all four | train | 9,821 | 266 | 5,813 | 3,501 | 241 |
| all four | val | 2,070 | 47 | 1,643 | 365 | 15 |
| all four | test | 1,765 | 105 | 843 | 646 | 171 |

Table 3. Contested samples per split and class (reason `conflict`, DEC-103 rule 4; their state is unknown, so they are not in the positives or negatives of Table 1). Fewer than 5 groups hold them: two in train and two in test.

| Split | Samples | Hepatoma | Hemangioma | Hepatic cyst | Hepatic stone | Samples contested for at least one class | Groups holding them |
|---|---|---|---|---|---|---|---|
| train | 11,329 | 104 | 10 | 7 | 0 | 112 | <5 |
| val | 2,426 | 0 | 0 | 0 | 0 | 0 | 0 |
| test | 2,421 | 148 | 55 | 17 | 0 | 191 | <5 |

### Against DIS-063

Table 4. The frozen split against the candidate sets of [DIS-063](../../discussions/DIS-063-epic3-split-by-datasource-groups.md). Its Table 1 is the test set at 15% with validation by image; its Table 2 is whole-group validation simulated with seed 0 (validation taken from the groups outside test with the same search). "-" = DIS-063 gives no value.

| Quantity | DIS-063 Table 1 (15% test, limits of DEC-108) | DIS-063 Table 2 (seed 0) | Frozen split |
|---|---|---|---|
| Groups test / val / train | 11 / - / - | 11 / 6 / 38 | 11 / 14 / 30 |
| Test hepatoma positives (groups; largest share) | 257 (7; 50%) | 257 (7) | 257 (7; 49.8%) |
| Test hemangioma positives | 79 | 79 (2 groups) | 79 (fewer than 5 groups) |
| Test cyst positives | 33 | 33 (2 groups) | 33 (fewer than 5 groups) |
| Test stone positives | 83 | - | 83 |
| Test cirrhosis negatives | 105 | - | 105 |
| Hepatoma val positives (groups; largest share) | by image: 207 | 193 (2; 68%) | 193 (fewer than 5; 68.4%) |
| Hemangioma val positives | by image: 24 | 26 | 22 |
| Cyst val positives | by image: 15 | 17 (1 group) | 19 (fewer than 5 groups; 89.5%) |
| Hepatoma train positives | 953 (val by image) | - | 967 |
| Contested samples | 304 in 4 groups | - | 303 in the table (fewer than 5 groups): 112 train, 0 val, 191 test |

The test set is the same as the DIS-063 candidate at 15%. The validation set differs from the simulation (14 groups, not 6); the reason is not checked (the simulation was a separate run). Its hepatoma positives (193, 68% in the largest group) equal Table 2's; hemangioma (22) and cyst (19) differ by 4 and 2. The contested count differs by 1: DIS-063 counted 304, the builder finds 303 in the table (1 contested sample is outside it, as the builder report says).

## Limits

- Validation rests on few groups (fewer than 5 for hepatoma, hemangioma, cyst and cirrhosis negatives), so validation scores carry the bootstrap interval over groups of DEC-108 rule 6. Hemangioma and cyst test results stay without a bar (DEC-100 rule 4, DEC-108 consequences).
- The 95% CIs in Table 1 treat samples as independent and are too narrow.
- The enc1 copy was not opened: its existence is shown by size and time only.

## Next step

Training can read the sample file. To change any value, bump `version` in the spec for a new file ([DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md)); the user decides.
