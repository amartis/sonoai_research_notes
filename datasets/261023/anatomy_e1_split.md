# Epic 1 split feasibility report on 261023: test set per tolerance, anatomy candidates

[TASK-167 (epic 1 split feasibility report)](../../../backlog/tasks/task-167%20-%20Epic-1-split-feasibility-report-on-261023-run-the-TASK-166-report-on-the-anatomy-candidate-table-at-tolerances-1-2-3-and-5-points-dataset-record-for-the-user-to-set-tolerances-and-minimum-counts-DEC-071.md), [DEC-071 (parameterised split method)](../../decisions/DEC-071-epic1-splitting-parameterised-split-method.md), [DIS-034 (epic 1 splitting)](../../discussions/DIS-034-epic1-splitting.md), [TASK-166 (split method and report mode)](../../../backlog/tasks/task-166%20-%20Parameterised-split-method-test-by-datasource-groups-with-every-classs-positive-rate-balanced-val-by-image-stratified-by-positive-pattern-feasibility-report-sonoai-data-command-synthetic-tests-DEC-071.md), [TASK-164 (candidate table)](../../../backlog/tasks/task-164%20-%20Epic-1-anatomy-candidate-table-on-261023_plain-run-the-TASK-163-builder-at-224-px-dataset-record-with-counts-per-flag-organ-state-and-datasource-group-polygon-overlap-and-in-crop-area-DEC-069.md), [anatomy_e1_candidates.md](anatomy_e1_candidates.md), [TASK-168 (freeze, waits for the tolerances)](../../../backlog/tasks/task-168%20-%20Freeze-the-epic-1-sample-file-on-261023-with-the-users-tolerances-and-minimum-counts-split-state-columns-enc1-copy-dataset-record-with-counts-per-split-and-class-DEC-071-DEC-070.md). Aggregates only: no images, file names, folder names or identifiers; datasource groups are given as counts.

**Status: descriptive feasibility counts for the user; sets no rule.** The user sets the tolerances and the minimum counts in a later consult session ([DEC-071](../../decisions/DEC-071-epic1-splitting-parameterised-split-method.md) item 9). Made on 2026-11-18 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)). Not reviewed. Reporting checklists (CLAIM, STARD): not applicable (no model; a split is searched and described, none is frozen). 95% CIs are Wilson intervals on the samples of a split; samples of one datasource group are not independent, so they are too narrow.

## Summary

1. **A test set exists at all four tolerances (1, 2, 3 and 5 points, the same for every class)**, with the minimum counts left null (counted as 0; the user has not set them yet). Each set passes every check (shares in range, gaps within the tolerance).
2. **Best set, taken here as the one at the tightest tolerance with a test set, 1 point** (see Assumptions): 15 of the 56 datasource groups in test, 1,814 of 20,011 candidate samples (9.07%); train 15,190 (75.91%), val 3,007 (15.03%). The largest gap is liver, +0.92 points (0.92 of the 1-point tolerance).
3. **The gap in positive rate hides a larger gap among labelled samples.** The rate is taken over all samples, unknown included (DIS-034 point 2). In the 1-point set the unknown share in test is above that of train + val for kidney (30.3% against 22.0%) and gallbladder (42.1% against 23.9%), and the positive share among labelled samples differs by +8.1 points for kidney and +3.1 for gallbladder (Table 3).
4. **Limits seen** (observations; section "Where the gap or the counts limit the choice"): kidney and gallbladder unknown shares in test; 183 to 268 gallbladder positives in test; 244 kidney negatives in the 5-point test; 6 groups only in the 3-point test; a search that is random, not exhaustive.

## Method

**Table read** (plain style via `sonoai.paths.dataset_dir`, [DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md); approved with TASK-167): `derived/anatomy_e1_candidates_v1_261023_plain_df.pkl` of `261023_plain` (29,233 rows, of which 20,011 candidates; only candidates are split). **Written: nothing** (the report mode writes no table; no other table was read; [DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md)).

Command (runs in about 7 s; changes nothing):

```bash
sonoai-data split report 261023_plain --spec configs/data/splits/anatomy_e1.yaml --tolerances 0.01,0.02,0.03,0.05
```

| Item | Value |
|---|---|
| Split spec | `configs/data/splits/anatomy_e1.yaml`, name `anatomy_e1_samples`, version 1 |
| Code and spec commit | `f860eeb62283448377ac97bdccd477e03698023b` (master when the report was run; the TASK-166 code and the spec are in it; this task changed no code or spec) |
| Candidate table sha256 | `1448ca703ed84d2839539f242c550bb7259d701d4dbbde37b3b23daf5323eb0d` (equal to the sha256 in [anatomy_e1_candidates.md](anatomy_e1_candidates.md)) |
| Samples, images, groups | 20,011 candidate samples, 19,515 distinct images, 56 datasource groups |
| Shares (target; range) | train 0.75 (0.70-0.85); val 0.15 (0.15-0.23); test 0.10 (0.08-0.13) |
| Classes | state_liver, state_kidney, state_stomach, state_gallbladder; positive = `positive`, negative = `negative`, any other state is unknown |
| Tolerance | 1, 2, 3 and 5 points, the same for every class, one run each |
| Minimum counts | null in the spec, counted as 0 by the report (16 values) |
| Test search | 56 groups are above `exhaustive_max` 16, so a seeded random greedy search (20,000 tries, seed 0); of the fitting sets, the one closest to the 10% target share, then with the smallest largest gap |
| Val | by image (hash), stratified by positive pattern, `merge_size` 20, seed 0; 15.03% of samples at every tolerance |

Rates are positives over all samples of the split. Gap = rate of the split minus the rate of its reference (test: train + val; val: train), in percentage points; the check is the gap against the tolerance.

## Results

Table 1. Does a test set exist? One run per tolerance (same tolerance for every class), minimum counts 0, n = 20,011 candidate samples in 56 datasource groups. Groups in train + val = 56 minus groups in test. "Largest gap, share of tolerance" = the largest absolute gap over the four classes, divided by the tolerance.

| Tolerance, points | Test set exists | Datasource groups in test | Datasource groups in train + val | Test samples (share) | Largest gap, share of tolerance | Checks |
|---|---|---|---|---|---|---|
| 1 | yes | 15 | 41 | 1,814 (9.07%) | 0.922 | all passed |
| 2 | yes | 11 | 45 | 2,168 (10.83%) | 0.859 | all passed |
| 3 | yes | 6 | 50 | 2,007 (10.03%) | 0.798 | all passed |
| 5 | yes | 16 | 40 | 1,999 (9.99%) | 0.847 | all passed |

Table 2. Best set (1-point tolerance): per class and split, samples, positives, negatives, unknown (a state that is neither), positive rate with 95% Wilson CI, and gap in points (test against train + val, val against train). Test n = 1,814 samples in 15 groups; train + val n = 18,197 in 41 groups; train n = 15,190; val n = 3,007 (by image, inside the 41 groups). Every row meets the checks.

| Class | Split | Samples | Positives | Negatives | Unknown | Positive rate, % (95% CI) | Gap, points |
|---|---|---|---|---|---|---|---|
| liver | train | 15,190 | 11,513 | 3,230 | 447 | 75.79 (75.11-76.47) | - |
| liver | val | 3,007 | 2,283 | 644 | 80 | 75.92 (74.36-77.42) | +0.13 |
| liver | test | 1,814 | 1,392 | 407 | 15 | 76.74 (74.74-78.62) | +0.92 |
| kidney | train | 15,190 | 7,498 | 4,346 | 3,346 | 49.36 (48.57-50.16) | - |
| kidney | val | 3,007 | 1,488 | 857 | 662 | 49.48 (47.70-51.27) | +0.12 |
| kidney | test | 1,814 | 903 | 361 | 550 | 49.78 (47.48-52.08) | +0.40 |
| stomach | train | 15,190 | 2,684 | 8,387 | 4,119 | 17.67 (17.07-18.28) | - |
| stomach | val | 3,007 | 535 | 1,645 | 827 | 17.79 (16.47-19.20) | +0.12 |
| stomach | test | 1,814 | 333 | 921 | 560 | 18.36 (16.64-20.20) | +0.67 |
| gallbladder | train | 15,190 | 1,658 | 9,896 | 3,636 | 10.92 (10.43-11.42) | - |
| gallbladder | val | 3,007 | 326 | 1,965 | 716 | 10.84 (9.78-12.00) | -0.07 |
| gallbladder | test | 1,814 | 183 | 867 | 764 | 10.09 (8.79-11.56) | -0.81 |

Table 3. Best set (1-point tolerance): the same classes read among labelled samples only (positive and negative, unknown left out), test against train + val. Not a check of the method; shown because the unknown share differs between test and train + val. Positive share among labelled samples, % (95% Wilson CI for test); n = labelled samples.

| Class | Test: labelled n | Test: positive share, % (95% CI) | Train + val: labelled n | Train + val: positive share, % | Difference, points | Unknown share, % (test; train + val) |
|---|---|---|---|---|---|---|
| liver | 1,799 | 77.4 (75.4-79.3) | 17,670 | 78.1 | -0.7 | 0.8; 2.9 |
| kidney | 1,264 | 71.4 (68.9-73.9) | 14,189 | 63.3 | +8.1 | 30.3; 22.0 |
| stomach | 1,254 | 26.6 (24.2-29.1) | 13,251 | 24.3 | +2.3 | 30.9; 27.2 |
| gallbladder | 1,050 | 17.4 (15.3-19.8) | 13,845 | 14.3 | +3.1 | 42.1; 23.9 |

Table 4. The other three sets (2, 3 and 5 points): per class, the test set's samples, positives, negatives, unknown, positive rate (95% Wilson CI) and gap against train + val. Test n and groups as in Table 1; the val gaps are within 0.16 points at every tolerance (largest: gallbladder, -0.16 at 2 points). Train and val rows are not repeated.

| Tolerance, points | Class | Test samples | Positives | Negatives | Unknown | Positive rate, % (95% CI) | Gap, points |
|---|---|---|---|---|---|---|---|
| 2 | liver | 2,168 | 1,617 | 543 | 8 | 74.58 (72.71-76.37) | -1.47 |
| 2 | kidney | 2,168 | 1,063 | 718 | 387 | 49.03 (46.93-51.14) | -0.43 |
| 2 | stomach | 2,168 | 367 | 1,512 | 289 | 16.93 (15.41-18.56) | -0.92 |
| 2 | gallbladder | 2,168 | 268 | 1,495 | 405 | 12.36 (11.04-13.81) | +1.72 |
| 3 | liver | 2,007 | 1,502 | 497 | 8 | 74.84 (72.89-76.69) | -1.18 |
| 3 | kidney | 2,007 | 1,017 | 658 | 332 | 50.67 (48.49-52.86) | +1.39 |
| 3 | stomach | 2,007 | 313 | 1,334 | 360 | 15.60 (14.07-17.25) | -2.40 |
| 3 | gallbladder | 2,007 | 203 | 1,321 | 483 | 10.11 (8.87-11.51) | -0.79 |
| 5 | liver | 1,999 | 1,495 | 490 | 14 | 74.79 (72.84-76.64) | -1.23 |
| 5 | kidney | 1,999 | 984 | 244 | 771 | 49.22 (47.04-51.42) | -0.21 |
| 5 | stomach | 1,999 | 431 | 859 | 709 | 21.56 (19.81-23.42) | +4.23 |
| 5 | gallbladder | 1,999 | 201 | 821 | 977 | 10.06 (8.81-11.45) | -0.86 |

## Where the gap or the counts limit the choice

Observations only; no rule, tolerance or minimum is proposed here (the user sets them).

1. **Gaps are inside every tolerance, but the 1-point set uses 92% of its tolerance** (liver, +0.92 points). The tolerances were tried only at 1, 2, 3 and 5 points; whether a set fits below 1 point was not run.
2. **The set chosen is the one closest to the 10% test share, not the one with the smallest gaps.** So the gaps above are not the smallest gaps that exist at that tolerance. At 5 points the stomach gap is +4.23 points (85% of the tolerance), at 3 points the stomach gap is -2.40 (80%), at 2 points the gallbladder gap is +1.72 (86%) and the liver gap is -1.47.
3. **Unknown states differ between test and the rest for kidney and gallbladder.** In the 1-point set the gallbladder unknown share is 42.1% in test against 23.9% in train + val, and the kidney share 30.3% against 22.0%; the rate over all samples is within 1 point while the positive share among labelled samples differs by +3.1 (gallbladder) and +8.1 (kidney) points (Table 3). The gap rule, as written, does not see this.
4. **Test counts per class are smallest for the gallbladder and, at some tolerances, the kidney.** Test gallbladder positives: 183 (1 point), 268 (2), 203 (3), 201 (5); the 1-point CI is 8.79-11.56%, a width of 2.8 points. Test kidney negatives: 361 (1 point), 718 (2), 658 (3), 244 (5). Test liver negatives: 407, 543, 497, 490. Val counts are larger (gallbladder positives 316-328, kidney negatives 825-876, over the four sets).
5. **The number of datasource groups in test falls from 15 to 6 between 1 and 3 points, and is 16 at 5 points.** Fewer groups mean fewer sources in test (a 6-group test set holds 10.03% of the samples).
6. **The search is random, not exhaustive** (56 groups above 16): a set that fits may exist where none was found, and a different seed or more tries can pick another set at the same tolerance. The largest group holds 2,723 samples (13.6% of the candidates), above the 13% upper test share, so it cannot be in test.
7. **The minimum counts were 0.** The test counts above are what the search found; none of them was required.

## Assumptions and what was not checked

- **"Best set" is read as the set at the tightest tolerance that has a test set (1 point).** DEC-071 and the report do not define "best across tolerances"; every tolerance has a set, and Table 4 gives the other three.
- Nothing written to disk: the report mode prints only. The printed output also lists the test group ids; they are not copied here.
- Not run: tolerances below 1 point or per-class tolerances, other seeds, more tries, any minimum count other than 0.

## Next step

The user sets the tolerances and the minimum counts in a consult session; then the spec (a new version) and the freeze ([TASK-168](../../../backlog/tasks/task-168%20-%20Freeze-the-epic-1-sample-file-on-261023-with-the-users-tolerances-and-minimum-counts-split-state-columns-enc1-copy-dataset-record-with-counts-per-split-and-class-DEC-071-DEC-070.md)) follow.
