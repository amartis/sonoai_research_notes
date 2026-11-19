# Epic 1 split on 261023: feasibility report (TASK-167) and frozen sample file (TASK-168), anatomy eligible samples

[TASK-167 (epic 1 split feasibility report)](../../../backlog/tasks/task-167%20-%20Epic-1-split-feasibility-report-on-261023-run-the-TASK-166-report-on-the-anatomy-candidate-table-at-tolerances-1-2-3-and-5-points-dataset-record-for-the-user-to-set-tolerances-and-minimum-counts-DEC-071.md), [DEC-071 (parameterised split method)](../../decisions/DEC-071-epic1-splitting-parameterised-split-method.md), [DIS-034 (epic 1 splitting)](../../discussions/DIS-034-epic1-splitting.md), [TASK-166 (split method and report mode)](../../../backlog/tasks/task-166%20-%20Parameterised-split-method-test-by-datasource-groups-with-every-classs-positive-rate-balanced-val-by-image-stratified-by-positive-pattern-feasibility-report-sonoai-data-command-synthetic-tests-DEC-071.md), [TASK-164 (table of eligible samples)](../../../backlog/tasks/task-164%20-%20Epic-1-anatomy-candidate-table-on-261023_plain-run-the-TASK-163-builder-at-224-px-dataset-record-with-counts-per-flag-organ-state-and-datasource-group-polygon-overlap-and-in-crop-area-DEC-069.md), [anatomy_e1_candidates.md](anatomy_e1_candidates.md), [TASK-168 (freeze, waits for the tolerances)](../../../backlog/tasks/task-168%20-%20Freeze-the-epic-1-sample-file-on-261023-with-the-users-tolerances-and-minimum-counts-split-state-columns-enc1-copy-dataset-record-with-counts-per-split-and-class-DEC-071-DEC-070.md). Aggregates only: no images, file names, folder names or identifiers; datasource groups are given as counts.

**Status: the sections up to "Next step" are the TASK-167 feasibility report (descriptive, sets no rule); the section "Frozen split (TASK-168)" at the end records the sample file frozen with the user's values ([DEC-075](../../decisions/DEC-075-epic1-split-values-tolerance-and-minimum-counts.md)).** In the report sections the gap tolerances and the minimum counts were still open: the user set them afterwards in a consult session ([DEC-071](../../decisions/DEC-071-epic1-splitting-parameterised-split-method.md) item 9; [DEC-075](../../decisions/DEC-075-epic1-split-values-tolerance-and-minimum-counts.md)), and the frozen section uses those values. Made on 2026-11-18 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)). Not reviewed. Reporting checklists (CLAIM, the Checklist for Artificial Intelligence in Medical Imaging, and STARD, the Standards for Reporting of Diagnostic Accuracy): not applicable (no model; the report sections search and describe a split, the frozen section records one).

**Terms used.** *Point* = percentage point. *CI* = confidence interval; the 95% CIs here are Wilson intervals on the samples of a split, and samples of one datasource group are not independent, so they are too narrow. *Datasource group* = datasources joined because an image occurs under both; the unit of the test split. *Eligible sample* = a sample of the [table of eligible samples](anatomy_e1_candidates.md) that passes the exclusion flags (its `candidate` column is true). *Positive rate* = positives over all samples of a split, unknown included ([DIS-034](../../discussions/DIS-034-epic1-splitting.md) point 2). *Positive-rate gap* (short form "gap") = positive rate of test minus that of train + val (val: minus train), in points. *Gap tolerance* (short form "tolerance") = the largest allowed absolute gap. *Unknown* = the state of the organ is neither positive nor negative. *Organ* = one of the four balanced state columns (liver, kidney, stomach, gallbladder). Terms of the section "Frozen split (TASK-168)": *sample file* = the table that lists every eligible sample with its `split` (train, val or test) and the four state columns. *Freeze* = the command `sonoai-data split freeze`: it searches the split once, then writes the sample file and its enc1 copy, and writes nothing when no split meets the spec. *Enc1 copy* = the encrypted copy of the sample file in the `261023_enc1` store. *sha256* = a 64-character fingerprint of a file's bytes; equal fingerprints mean equal files. *Labeled sample* (for one organ) = a sample whose state for the organ is positive or negative (not unknown); it is not a sample that has a labeling. *Positive share* (among labeled samples) = positives over positives + negatives; it is not the positive rate, which is over all samples with unknown included.

**Precision.** Rates, gaps, CIs and shares of samples are given with 2 decimals, as the report prints them, because the gaps are compared with tolerances as small as 1 point. A share of a tolerance is given in whole percent.

## Summary

1. **A test set exists at all four gap tolerances (1, 2, 3 and 5 points, the same for every organ)**, with the minimum counts left null (counted as 0; the user has not set them yet). Each set passes every check (shares in range, gaps within the tolerance).
2. **The 1-point test set** (shown in full because it is at the tightest tolerance; see "Assumptions"): 15 of the 56 datasource groups in test, 1,814 of 20,011 eligible samples (9.07%); train 15,190 (75.91%), val 3,007 (15.03%). The largest gap is liver, +0.92 points (92% of the 1-point tolerance).
3. **The gap in positive rate hides a larger difference among labeled samples.** The rate is taken over all samples, unknown included. In the 1-point test set the unknown share in test is above that of train + val for kidney (30.32% against 22.03%) and gallbladder (42.12% against 23.92%), and the positive share among labeled samples is higher in test by 8.11 points for kidney and 3.10 for gallbladder (Table 3).
4. **Limits seen** (observations; section "Where the gap or the counts limit the choice"): kidney and gallbladder unknown shares in test; 183 to 268 gallbladder positives in test; 244 kidney negatives in the 5-point test set; 6 groups only in the 3-point test set; a search that is random, not exhaustive.

## Method

**Table read** (plain style via `sonoai.paths.dataset_dir`, [DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md); approved with TASK-167): `derived/anatomy_e1_candidates_v1_261023_plain_df.pkl` of `261023_plain` (the table of eligible samples, as named by TASK-164; 29,233 rows, of which 20,011 eligible; only eligible samples are split). **Written: nothing** (the report mode writes no table; no other table was read; [DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md)).

Command (changes nothing; prints only):

```bash
sonoai-data split report 261023_plain --spec configs/data/splits/anatomy_e1.yaml --tolerances 0.01,0.02,0.03,0.05
```

| Item | Value |
|---|---|
| Split spec | `configs/data/splits/anatomy_e1.yaml`, name `anatomy_e1_samples`, version 1 |
| Code and spec commit | `f860eeb62283448377ac97bdccd477e03698023b` (master when the report was run; the TASK-166 code and the spec are in it; this task changed no code or spec) |
| Table of eligible samples, sha256 | `1448ca703ed84d2839539f242c550bb7259d701d4dbbde37b3b23daf5323eb0d` (equal to the sha256 in [anatomy_e1_candidates.md](anatomy_e1_candidates.md)) |
| Samples, images, groups | 20,011 eligible samples, 19,515 distinct images, 56 datasource groups |
| Shares (target; range) | train 0.75 (0.70-0.85); val 0.15 (0.15-0.23); test 0.10 (0.08-0.13) |
| Balanced state columns (spec key `classes`) | `state_liver`, `state_kidney`, `state_stomach`, `state_gallbladder`; positive = `positive`, negative = `negative`, any other state is unknown |
| Gap tolerance | 1, 2, 3 and 5 points, the same for every organ, one run each |
| Minimum counts | null in the spec, counted as 0 by the report (16 values) |
| Test search | 56 groups are above `exhaustive_max` 16, so a seeded random greedy search (20,000 tries, seed 0); of the fitting sets, the one closest to the 10% target share, then with the smallest largest gap ([DEC-071](../../decisions/DEC-071-epic1-splitting-parameterised-split-method.md) item 3) |
| Val | by image hash, drawn per stratum (images with the same set of positive organs; strata with fewer than `merge_size` 20 images are merged), seed 0; 15.03% of samples at every tolerance |

## Results

Table 1. Does a test set exist? One run per gap tolerance (the same for every organ), minimum counts 0, n = 20,011 eligible samples in 56 datasource groups. Groups in train + val = 56 minus groups in test. "Largest gap, share of tolerance" = the largest absolute gap over the four organs divided by the tolerance, in percent. "Checks" = the report's checks on the set: every split share in its range, every gap within the tolerance, minimum counts met (0 here).

| Gap tolerance, points | Test set exists | Datasource groups in test | Datasource groups in train + val | Test samples (share of 20,011) | Largest gap, share of tolerance, % | Checks |
|---|---|---|---|---|---|---|
| 1 | yes | 15 | 41 | 1,814 (9.07%) | 92 | all passed |
| 2 | yes | 11 | 45 | 2,168 (10.83%) | 86 | all passed |
| 3 | yes | 6 | 50 | 2,007 (10.03%) | 80 | all passed |
| 5 | yes | 16 | 40 | 1,999 (9.99%) | 85 | all passed |

Table 2. The 1-point test set: per organ and split, samples, positives, negatives, unknown, positive rate with 95% Wilson CI, and gap in points (test against train + val, val against train). Test n = 1,814 samples in 15 datasource groups; train + val n = 18,197 in 41 groups; train n = 15,190; val n = 3,007 (by image, inside the 41 groups). Every row meets the checks.

| Organ | Split | Samples | Positives | Negatives | Unknown | Positive rate, % (95% CI) | Gap, points |
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

Table 3. The 1-point test set: the same organs read among labeled samples only (positive and negative; unknown left out), test against train + val. Not a check of the method; shown because the unknown share differs between test and train + val. n = labeled samples; positive share among labeled samples, % (95% Wilson CI for test). The differences are descriptive and carry no CI (samples of one datasource group are not independent, see "Terms used").

| Organ | Test: labeled n | Test: positive share among labeled, % (95% CI) | Train + val: labeled n | Train + val: positive share among labeled, % | Difference in positive share among labeled samples, points | Unknown share, % (test; train + val) |
|---|---|---|---|---|---|---|
| liver | 1,799 | 77.38 (75.39-79.25) | 17,670 | 78.08 | -0.70 | 0.83; 2.90 |
| kidney | 1,264 | 71.44 (68.89-73.86) | 14,189 | 63.33 | +8.11 | 30.32; 22.03 |
| stomach | 1,254 | 26.56 (24.19-29.07) | 13,251 | 24.29 | +2.26 | 30.87; 27.18 |
| gallbladder | 1,050 | 17.43 (15.25-19.84) | 13,845 | 14.33 | +3.10 | 42.12; 23.92 |

Table 4. The 2-, 3- and 5-point test sets and their val sets, per organ: samples, positives, negatives, unknown, positive rate with 95% Wilson CI, and gap in points (test against train + val, val against train). From the same run as Tables 1-3. 2-point: test n = 2,168 samples in 11 datasource groups, val n = 3,007. 3-point: test n = 2,007 in 6 groups, val n = 3,008. 5-point: test n = 1,999 in 16 groups, val n = 3,008. Train rows are not repeated; every row meets the checks.

| Gap tolerance, points | Organ | Split | Samples | Positives | Negatives | Unknown | Positive rate, % (95% CI) | Gap, points |
|---|---|---|---|---|---|---|---|---|
| 2 | liver | test | 2,168 | 1,617 | 543 | 8 | 74.58 (72.71-76.37) | -1.47 |
| 2 | liver | val | 3,007 | 2,288 | 630 | 89 | 76.09 (74.53-77.58) | +0.04 |
| 2 | kidney | test | 2,168 | 1,063 | 718 | 387 | 49.03 (46.93-51.14) | -0.43 |
| 2 | kidney | val | 3,007 | 1,486 | 836 | 685 | 49.42 (47.63-51.20) | -0.06 |
| 2 | stomach | test | 2,168 | 367 | 1,512 | 289 | 16.93 (15.41-18.56) | -0.92 |
| 2 | stomach | val | 3,007 | 539 | 1,617 | 851 | 17.92 (16.60-19.34) | +0.09 |
| 2 | gallbladder | test | 2,168 | 268 | 1,495 | 405 | 12.36 (11.04-13.81) | +1.72 |
| 2 | gallbladder | val | 3,007 | 316 | 1,916 | 775 | 10.51 (9.46-11.66) | -0.16 |
| 3 | liver | test | 2,007 | 1,502 | 497 | 8 | 74.84 (72.89-76.69) | -1.18 |
| 3 | liver | val | 3,008 | 2,286 | 651 | 71 | 76.00 (74.44-77.49) | -0.02 |
| 3 | kidney | test | 2,007 | 1,017 | 658 | 332 | 50.67 (48.49-52.86) | +1.39 |
| 3 | kidney | val | 3,008 | 1,479 | 825 | 704 | 49.17 (47.38-50.96) | -0.13 |
| 3 | stomach | test | 2,007 | 313 | 1,334 | 360 | 15.60 (14.07-17.25) | -2.40 |
| 3 | stomach | val | 3,008 | 543 | 1,631 | 834 | 18.05 (16.72-19.47) | +0.07 |
| 3 | gallbladder | test | 2,007 | 203 | 1,321 | 483 | 10.11 (8.87-11.51) | -0.79 |
| 3 | gallbladder | val | 3,008 | 328 | 1,921 | 759 | 10.90 (9.84-12.07) | -0.01 |
| 5 | liver | test | 1,999 | 1,495 | 490 | 14 | 74.79 (72.84-76.64) | -1.23 |
| 5 | liver | val | 3,008 | 2,285 | 628 | 95 | 75.96 (74.40-77.46) | -0.07 |
| 5 | kidney | test | 1,999 | 984 | 244 | 771 | 49.22 (47.04-51.42) | -0.21 |
| 5 | kidney | val | 3,008 | 1,485 | 876 | 647 | 49.37 (47.58-51.15) | -0.09 |
| 5 | stomach | test | 1,999 | 431 | 859 | 709 | 21.56 (19.81-23.42) | +4.23 |
| 5 | stomach | val | 3,008 | 523 | 1,647 | 838 | 17.39 (16.07-18.78) | +0.07 |
| 5 | gallbladder | test | 1,999 | 201 | 821 | 977 | 10.06 (8.81-11.45) | -0.86 |
| 5 | gallbladder | val | 3,008 | 327 | 1,961 | 720 | 10.87 (9.81-12.03) | -0.05 |

## Where the gap or the counts limit the choice

Observations only; no rule, gap tolerance or minimum is proposed here (the user sets them).

1. **Gaps are inside every tolerance, but the 1-point test set uses 92% of its tolerance** (liver, +0.92 points). Gap tolerances were tried only at 1, 2, 3 and 5 points; whether a set fits below 1 point was not run.
2. **The set chosen at a tolerance is the one closest to the 10% test share, not the one with the smallest gaps.** So the gaps above are not the smallest gaps that exist at that tolerance. In the 5-point test set the stomach gap is +4.23 points (85% of the tolerance), in the 3-point test set the stomach gap is -2.40 (80%), and in the 2-point test set the gallbladder gap is +1.72 (86%) and the liver gap is -1.47.
3. **Unknown states differ between test and the rest for kidney and gallbladder.** In the 1-point test set the gallbladder unknown share is 42.12% in test against 23.92% in train + val, and the kidney share 30.32% against 22.03%; the positive rate over all samples differs by less than 1 point (Table 2), while the positive share among labeled samples is higher in test by 3.10 points (gallbladder) and 8.11 points (kidney) (Table 3; descriptive, no CI). The gap, as defined, does not see this.
4. **Test counts per organ are smallest for the gallbladder and, in the 5-point test set, the kidney.** Test gallbladder positives: 183 (1 point), 268 (2), 203 (3), 201 (5); the 1-point CI is 8.79-11.56%, a width of 2.77 points. Test kidney negatives: 361 (1 point), 718 (2), 658 (3), 244 (5). Test liver negatives: 407, 543, 497, 490. Val counts are larger (Tables 2 and 4: gallbladder positives 316-328, kidney negatives 825-876, over the four sets).
5. **The number of datasource groups in test falls from 15 to 6 between 1 and 3 points, and is 16 at 5 points.** Fewer groups mean fewer sources in test (the 3-point test set has 6 groups and 10.03% of the samples).
6. **The search is random, not exhaustive** (56 groups, above 16): a set that fits may exist where none was found, and a different seed or more tries can pick another set at the same tolerance. The largest datasource group holds 2,723 samples (13.61% of the eligible samples), above the 13% upper test share, so it cannot be in test.
7. **The minimum counts were 0.** The test counts above are what the search found; none of them was required.

## Assumptions and what was not checked

- **Which test set is shown in full.** DEC-071 and the report do not define a "best" test set across tolerances. By the order of DEC-071 item 3 (closest to the target share first), the 5-point test set (9.99%) is closest to 10%, not the 1-point one (9.07%). The 1-point test set is shown in full (Tables 2 and 3) because it is at the tightest tolerance, not by that rule; Table 4 gives the other three. The user chooses.
- Nothing written to disk: the report mode prints only. The printed output also lists the test group ids; they are not copied here.
- Not run: tolerances below 1 point or per-organ tolerances, other seeds, more tries, any minimum count other than 0.

## Frozen split (TASK-168)

**Superseded by version 3 (TASK-179, section "Sample file version 3")**: same split, two more columns. The plain file of version 2 is in `derived/obsolete/`; its enc1 copy stays in the store. The counts in this section and the next tables are those of both versions.

Frozen on 2026-11-18 with [DEC-075 (epic 1 split values)](../../decisions/DEC-075-epic1-split-values-tolerance-and-minimum-counts.md): 2-point gap tolerance for every organ, at least 200 positives and 300 negatives per organ in test and in val, positive rate over all samples. Task: [TASK-168 (freeze)](../../../backlog/tasks/task-168%20-%20Freeze-the-epic-1-sample-file-on-261023-with-the-users-tolerances-and-minimum-counts-split-state-columns-enc1-copy-dataset-record-with-counts-per-split-and-class-DEC-071-DEC-070.md). Aggregates only; groups are given as counts. The freeze command was run by the user (the agent has no access to the data passphrase); the agent computed the sha256 and re-checked the written file.

Command (writes a new file and its enc1 copy; changes no existing table, [DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md)):

```bash
sonoai-data split freeze 261023_plain --spec configs/data/splits/anatomy_e1.yaml
```

Table 5. The frozen sample file and how it was made: name pattern, fingerprints, spec version, seed, size and code. n = 20,011 samples. The two sha256 values equal the ones the freeze printed.

| Item | Value |
|---|---|
| Sample file, name pattern | `derived/anatomy_e1_samples_v2_261023_plain_df.pkl` in `261023_plain`; encrypted copy at the same path in the `261023_enc1` store |
| Sample file sha256 | `db2f2429152c889de31d520c55b14d518ca7ebc5220f70df3a2a302ff35f8ab9` (computed on the written file; equal to the sha256 the freeze printed) |
| Split spec | `configs/data/splits/anatomy_e1.yaml`, version 2, name `anatomy_e1_samples`; sha256 `2d7674332de464bbb95e6d93ca5730cf43fe5fb775652ce00717e6b01be7aec7` (equal to the freeze output and to the `spec_sha256` stored in the file) |
| Seed | 0 (random greedy test search, 20,000 tries; 56 groups are above `exhaustive_max` 16) |
| Input | table of eligible samples, sha256 `1448ca703ed84d2839539f242c550bb7259d701d4dbbde37b3b23daf5323eb0d` (equal to the sha256 stored in the file and in [anatomy_e1_candidates.md](anatomy_e1_candidates.md)) |
| Rows and columns | 20,011 samples (all unique sample numbers), 19,515 distinct images; 12 columns: the sample number, image hash, crop box (4), datasource group, the four `state_*` columns ([DEC-070](../../decisions/DEC-070-anatomy-label-set-task-states-in-sample-file.md) rule 2) and `split` |
| Code | `sonoai.data.splitting` (TASK-166); this task changed no code or spec |
| Enc1 copy | the manifest and one new blob of the store were written at the same second as the plain file; the blob is 32 bytes larger than the plain file (the enc1 overhead). Not decrypted or compared by the agent (no passphrase); the freeze printed that it wrote the copy |

**Re-check on the written file.** This is the freeze re-check: the agent repeated every check of the spec (shares, groups, gaps, minimum counts) on the file read back from disk, not on the freeze's memory.

Table 6. The freeze re-check: each check of the spec, with the result on the written file. n = 20,011 samples (train 14,836, val 3,007, test 2,168); shares and their ranges are percentages of samples.

| Check | Result |
|---|---|
| Share of samples in range | train 74.14% (range 70-85%), val 15.03% (range 15-23%), test 10.83% (range 8-13%): met |
| Datasource groups in test also in train or val | 0 (test and train 0, test and val 0): met |
| Images in more than one split | 0 (train and val 0, test and the rest 0): met |
| Every organ's gap within 2 points | largest absolute gap 1.72 (gallbladder, 86% of the tolerance): met (Table 7) |
| Minimum counts, test | smallest positives 268 (gallbladder; minimum 200), smallest negatives 543 (liver; minimum 300): met |
| Minimum counts, val | smallest positives 316 (gallbladder; minimum 200), smallest negatives 630 (liver; minimum 300): met |
| Same result as the in-memory run before the freeze | yes (every count equal) |

Table 7. The frozen split, per organ and split: samples, positives, negatives, unknown, positive rate over all samples with 95% Wilson CI, and gap in points (test against train + val, val against train). n = 20,011 samples: train 14,836, val 3,007, test 2,168. Samples of one datasource group are not independent, so the CIs are too narrow. Percentages with 2 decimals, as in Tables 2 and 4.

| Organ | Split | Samples | Positives | Negatives | Unknown | Positive rate, % (95% CI) | Gap, points |
|---|---|---|---|---|---|---|---|
| liver | train | 14,836 | 11,283 | 3,108 | 445 | 76.05 (75.36-76.73) | - |
| liver | val | 3,007 | 2,288 | 630 | 89 | 76.09 (74.53-77.58) | +0.04 |
| liver | test | 2,168 | 1,617 | 543 | 8 | 74.58 (72.71-76.37) | -1.47 |
| kidney | train | 14,836 | 7,340 | 4,010 | 3,486 | 49.47 (48.67-50.28) | - |
| kidney | val | 3,007 | 1,486 | 836 | 685 | 49.42 (47.63-51.20) | -0.06 |
| kidney | test | 2,168 | 1,063 | 718 | 387 | 49.03 (46.93-51.14) | -0.43 |
| stomach | train | 14,836 | 2,646 | 7,824 | 4,366 | 17.83 (17.23-18.46) | - |
| stomach | val | 3,007 | 539 | 1,617 | 851 | 17.92 (16.60-19.34) | +0.09 |
| stomach | test | 2,168 | 367 | 1,512 | 289 | 16.93 (15.41-18.56) | -0.92 |
| gallbladder | train | 14,836 | 1,583 | 9,317 | 3,936 | 10.67 (10.18-11.18) | - |
| gallbladder | val | 3,007 | 316 | 1,916 | 775 | 10.51 (9.46-11.66) | -0.16 |
| gallbladder | test | 2,168 | 268 | 1,495 | 405 | 12.36 (11.04-13.81) | +1.72 |

Table 8. Datasource groups per split, of 56. Test is by group; val is by image hash inside the groups, so a group can be in both train and val. Counts of groups.

| Split | Datasource groups | Samples |
|---|---|---|
| train | 45 | 14,836 |
| val | 43 | 3,007 |
| test | 11 | 2,168 |
| in test and (train or val) | 0 | - |

Table 9. Known limit ([DEC-075](../../decisions/DEC-075-epic1-split-values-tolerance-and-minimum-counts.md) Consequences): the unknown share per organ differs between test and train + val, and so does the positive share among labeled samples. Test n = 2,168; train + val n = 17,843. Unknown share in %; positive share among labeled samples in % (95% Wilson CI for test; train + val without CI); difference in points. The differences are descriptive and carry no CI (see the note under Table 7).

| Organ | Unknown share, test, % | Unknown share, train + val, % | Test: labeled n | Test: positive share among labeled, % (95% CI) | Train + val: labeled n | Train + val: positive share among labeled, % | Difference, points |
|---|---|---|---|---|---|---|---|
| liver | 0.37 | 2.99 | 2,160 | 74.86 (72.99-76.65) | 17,309 | 78.40 | -3.54 |
| kidney | 17.85 | 23.38 | 1,781 | 59.69 (57.39-61.94) | 13,672 | 64.56 | -4.87 |
| stomach | 13.33 | 29.24 | 1,879 | 19.53 (17.80-21.39) | 12,626 | 25.23 | -5.69 |
| gallbladder | 18.68 | 26.40 | 1,763 | 15.20 (13.60-16.95) | 13,132 | 14.46 | +0.74 |

**Known limit.** The positive rate over all samples is balanced within 2 points, but the unknown share in test is lower than in train + val for every organ (by 2.62 points for liver, 5.53 for kidney, 15.91 for stomach, 7.72 for gallbladder). Among labeled samples the positive share is therefore lower in test than in train + val for liver, kidney and stomach (by 3.54 to 5.69 points) and about the same for gallbladder (+0.74). Two of the mission's checks ([DEC-065](../../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md)) each read one state: W1, how well the organ is outlined, is measured on test samples where the organ is positive; W2, no phantom organs, is measured on test samples where the organ is a closed negative (a negative state that carries a closure: the label set of the sample is closed for that organ; [DIS-034](../../discussions/DIS-034-epic1-splitting.md) point 2). So the unknown-share difference changes their counts and CI widths, not their definition; a metric pooled over states would see the difference. This is the consequence DEC-075 accepted (one rate over all samples). Not checked: why the unknown share differs (for example, which datasources carry which states).

**Not checked.** Whether the enc1 copy decrypts to the same bytes (no passphrase for the agent); the check is the user's `sonoai-data` run that printed the copy as written. Reporting checklists (CLAIM, STARD): not applicable (no model).

## Sample file version 3 (TASK-179)

[TASK-179 (sample file v3 on 261023)](../../../backlog/tasks/task-179%20-%20Epic-1-sample-file-v3-on-261023-build-candidate-table-v2-sample-taskcrops_ids-re-freeze-with-split-spec-v3-check-the-split-equals-v2-for-every-sample-move-v1-candidates-and-v2-samples-to-derived-obsolete-TASK-173-DEC-071.md) froze the split again so that the sample file has the two columns the training sample reader needs: `sample` and `taskcrops_ids` ([TASK-173 (sample reader columns)](../../../backlog/tasks/task-173%20-%20Epic-1-sample-file-readable-by-the-sample-reader-sample-and-taskcrops_ids-columns-found-in-TASK-166.md)). The freeze used candidate table version 2 ([anatomy_e1_candidates.md](anatomy_e1_candidates.md)), spec version 3 and the same seed, tolerances and minimum counts as version 2 ([DEC-075](../../decisions/DEC-075-epic1-split-values-tolerance-and-minimum-counts.md)). **Every sample is in the same split as in sample file version 2, so every count in this record (Tables 6 to 9, the known limit) is those of version 2 and is not repeated.** The freeze command was run by the user (the agent has no access to the data passphrase); the agent computed the sha256 and ran the checks on the written file.

Command (writes a new file and its enc1 copy; changes no existing table, [DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md)):

```bash
sonoai-data split freeze 261023_plain --spec configs/data/splits/anatomy_e1.yaml
```

Table 10. Sample file version 3 and version 2: name pattern, fingerprints, spec version, seed, size and location. n = 20,011 samples in both. The sha256 values of version 3 are computed on the written file and equal the ones the user reported from the freeze.

| Item | Version 2 (TASK-168) | Version 3 (TASK-179) |
|---|---|---|
| Sample file, name pattern | `derived/anatomy_e1_samples_v2_261023_plain_df.pkl` | `derived/anatomy_e1_samples_v3_261023_plain_df.pkl` in `261023_plain`; encrypted copy at the same path in the `261023_enc1` store |
| Sample file sha256 | `db2f2429152c889de31d520c55b14d518ca7ebc5220f70df3a2a302ff35f8ab9` | `fdf85557fa5c825f0c85f1b71522476bb73c82b2c88fa33889b56dd07000fa32` |
| Split spec | `configs/data/splits/anatomy_e1.yaml`, version 2, sha256 `2d7674332de464bbb95e6d93ca5730cf43fe5fb775652ce00717e6b01be7aec7` | the same file, version 3, sha256 `8477795f63eef27f2b56c4b4841367546e74a7a50bce2ba75038bc1eafed90a4` (equal to the `spec_sha256` stored in the file) |
| Seed | 0 | 0 (random greedy test search, 20,000 tries; 56 groups are above `exhaustive_max` 16) |
| Input | candidate table version 1, sha256 `1448ca703ed84d2839539f242c550bb7259d701d4dbbde37b3b23daf5323eb0d` | candidate table version 2, sha256 `41a6ccdc2088890a6b52ac1f67935fc11eca01d780900275501fa6aaabd80f64` (equal to the `input_sha256` stored in the file) |
| Columns | 12 | 14: the 12 of version 2 plus `sample` and `taskcrops_ids` (`sample`, `taskcrops_ids`, `sample_no`, image hash, crop box (4), datasource group, the four `state_*` columns, `split`) |
| Location | `derived/obsolete/` in `261023_plain` (moved on 2026-11-19, sha256 unchanged); **the encrypted copy of version 2 stays in the `261023_enc1` store, untouched** | `derived/` in `261023_plain` and in the enc1 store |

What changed in the split spec between version 2 and version 3: the input name (candidate table version 2), and the columns `sample` and `taskcrops_ids` added to the columns copied into the sample file. No share, tolerance, minimum count, seed or search setting changed.

Table 11. The checks on sample file version 3, run on the file read back from disk. n = 20,011 samples.

| Check | Result |
|---|---|
| Spec checks again (shares, datasource groups, images, gaps, minimum counts; the same function as the freeze) | 0 failures; train 74.14%, val 15.03%, test 10.83% of samples |
| Split of each sample against sample file version 2, joined on `sample_no` | 20,011 matched, 0 only in one of the files; **0 samples differ** |
| Samples per split against version 2 | equal: train 14,836, val 3,007, test 2,168 |
| Test datasource groups against version 2 | the same list of 11 groups |
| The 12 columns of version 2 | equal to version 2, row for row (all columns except `split`, which is checked above) |
| `sample` equals `sample_no` | 20,011 of 20,011 rows; sample numbers unique |
| `check_sample_file` of the sample reader (`sonoai.training.samples`) | accepts the file |
| `taskcrops_ids` against `build_samples` on `taskcrops_df` | 0 of 20,011 samples differ; none empty |

**Not checked.** Whether the enc1 copy of version 3 decrypts to the same bytes (no passphrase for the agent); the user's `sonoai-data` run printed the copy as written. Reporting checklists (CLAIM, STARD): not applicable (no model).

## Next step

The user set the gap tolerances and the minimum counts ([DEC-075](../../decisions/DEC-075-epic1-split-values-tolerance-and-minimum-counts.md)); the spec (version 2) and the freeze ([TASK-168](../../../backlog/tasks/task-168%20-%20Freeze-the-epic-1-sample-file-on-261023-with-the-users-tolerances-and-minimum-counts-split-state-columns-enc1-copy-dataset-record-with-counts-per-split-and-class-DEC-071-DEC-070.md)) is done (section "Frozen split"). The sample file was frozen again as version 3 with the two reader columns and the same split (section "Sample file version 3 (TASK-179)"). Next: training uses sample file version 3.
