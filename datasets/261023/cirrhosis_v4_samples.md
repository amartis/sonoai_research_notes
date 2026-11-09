# Cirrhosis v4 sample file and train/val/test split on 261023_plain

[TASK-097](../../../backlog/tasks/task-097%20-%20Re-freeze-the-cirrhosis-v4-sample-file-under-the-DEC-047-cases-dataset-record-with-one-count-per-case-code-per-group-and-per-split.md), [DEC-047](../../decisions/DEC-047-cirrhosis-v4-cases-per-project-group-and-liver-fallback.md), [DEC-044](../../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md), [DEC-046](../../decisions/DEC-046-cirrhosis-v4-drops-the-qwen3-vl-quality-step.md), [DEC-043](../../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md). Aggregates only; no images, file names or identifiers. Counts and a fixed split, no model. Reporting checklists (CLAIM, STARD): not applicable. 95% CIs are Wilson intervals on the sample (samples of one datasource are not independent, so they are too narrow).

Made on 2026-11-09 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)) with `sonoai-data sample-set freeze 261023_plain --min-side 128 --no-verdicts --seed 97 --name cirrhosis_v4_dec047_samples` (code at master cc8756c: DEC-047 cases in [TASK-096](../../../backlog/tasks/task-096%20-%20Cirrhosis-v4-sample-cases-per-project-group-7-14-3635-5249-with-case-codes-precirrhosis-excluded-and-the-liver-area-fallback-DEC-047.md), polygon fix in TASK-098). Task `lseg_cirrhosis_v4`. This file **replaces** the [TASK-087](../../../backlog/tasks/task-087%20-%20Fix-the-cirrhosis-sample-file-and-its-train-val-test-split-dataset-record-with-counts-per-split-DEC-044.md) file (kept below, not to be used: 2,064 of its positives had no polygon, [TASK-088](../../../backlog/tasks/task-088%20-%20Train-lseg_cirrhosis_v4-on-the-fixed-sample-file-and-write-the-EXP-record-DEC-043-DEC-045.md) notes).

## Result

- Sample file: `derived/cirrhosis_v4_dec047_samples_df.pkl` in `261023_plain` (plain, machine01 only). Columns: sample number, `taskcrops_df` ids, datasource group, positive, split, final case, one case per project group (7, 14, 36, 52), liver source. Encrypted copy in the enc1 store at the same path ([DEC-024](../../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).
- Table sha256: `59e174bf6b7343b3c5f1150e11f35bbaa7fa57786251be85b785fbd397c8c55a` (checked again on the plain file). A changed table is a new file name (DEC-044 rule 7).
- Seed 97 (test search and train/val split); minimum shorter side 128 px; no Qwen3-VL step (DEC-046).
- Reader check: the training sample reader (`SampleReader`, plain style) accepted all 13,777 samples (train 10,331, val 2,068, test 1,378; none refused as not eligible).

## Open points (counts only)

1. **Group 52 with 49 has 0 samples.** Every 52 case and 52U is 0, so the 49-52 pairing could not be assessed. The freeze was accepted with this (user, 2026-11-09).
2. **Positive share is 4.6%** (639 of 13,777; 95% CI 4.3-5.0), against 18.8% in the TASK-087 record.
3. **5,666 samples are in no project group** (final case `none`, of 31,104 samples).
4. Test holds 0 samples with a 36 case, and 29 of the 31 `7P1` positives; train and val hold the 36 samples.

## Cases (DEC-047), all 31,104 samples before the filters

"Crop-group pairs" counts a crop once per group it belongs to. "Final" counts samples by their final case.

| Case | Crop-group pairs | Final |
|---|---|---|
| 7P1 | 35 | 35 |
| 7N1 | 3,379 | 3,379 |
| 7E1 | 0 | 0 |
| 7E2 | 0 | 0 |
| 7E3 | 0 | 0 |
| 7E4 | 2,447 | 2,447 |
| 14P1 | 338 | 338 |
| 14N1 | 9,442 | 9,348 |
| 14E1 | 1,878 | 1,878 |
| 14E3 | 4,587 | 4,585 |
| 14E4 | 1,017 | 1,017 |
| 36P1 | 303 | 303 |
| 36N1 | 1,309 | 1,309 |
| 36E1 | 399 | 399 |
| 36E2 | 28 | 28 |
| 36E3 | 0 | 0 |
| 36E4 | 167 | 167 |
| 36U | 0 | 0 |
| 52P1 | 0 | 0 |
| 52N1 | 0 | 0 |
| 52E1 | 0 | 0 |
| 52E2 | 0 | 0 |
| 52E3 | 0 | 0 |
| 52E4 | 0 | 0 |
| 52U | 0 | 0 |
| xE5 | 205 | 205 |
| xC1 | 0 | 0 |
| none (in no group) | - | 5,666 |

Pairing: 36U = 0, so every crop of project 36 pairs with project 35. Project 52 has no crop, so 52U = 0 and nothing pairs with 49. Case counts after each later filter step were not produced by the freeze; the table below gives the cases of the samples that remain.

## Counts after each filter step

| Step | Samples | Positives | Negatives | Groups |
|---|---|---|---|---|
| 1 All samples | 31,104 | - | - | 70 |
| 2 Eligible (DEC-047 cases, rule 3) | 14,712 | 676 | 14,036 | 55 |
| 3 No `quality` or `exclusion` choice (rule 4) | 13,861 | 639 | 13,222 | 54 |
| 4 Frame not skipped in v1 (rule 4) | 13,847 | 639 | 13,208 | 54 |
| 5 Shorter side at least 128 px (rule 5) | 13,777 | 639 | 13,138 | 53 |

## Counts per split

| Split | Samples | Share of samples | Positives | Negatives | Positive share (95% CI) | Datasource groups |
|---|---|---|---|---|---|---|
| train | 10,331 | 75.0% | 478 | 9,853 | 4.6% (4.2-5.0) | 41 |
| val | 2,068 | 15.0% | 97 | 1,971 | 4.7% (3.9-5.7) | 41 |
| test | 1,378 | 10.0% | 64 | 1,314 | 4.6% (3.7-5.9) | 11 |
| all | 13,777 | 100% | 639 | 13,138 | 4.6% (4.3-5.0) | 53 |

Group counts do not add up: train and val share datasources (random split, DEC-044 rule 10); the 11 test groups are in no other split (rule 9). Test positive share equals the whole set's (limit 2 points). All sizes are inside the DEC-044 ranges (train 70-85%, val 15-23%, test 8-13%), so rule 11 did not trigger.

## Final case of the samples in the file, per split

| Final case | train | val | test | all |
|---|---|---|---|---|
| 7P1 | 2 | 0 | 29 | 31 |
| 7N1 | 2,112 | 423 | 593 | 3,128 |
| 14P1 | 252 | 48 | 35 | 335 |
| 14N1 | 6,764 | 1,350 | 721 | 8,835 |
| 36P1 | 224 | 49 | 0 | 273 |
| 36N1 | 977 | 198 | 0 | 1,175 |
| all other codes (including 52 and xC1) | 0 | 0 | 0 | 0 |
| all | 10,331 | 2,068 | 1,378 | 13,777 |

Group cases in the file (crop-group pairs): group 7: 3,128 7N1 and 31 7P1; group 14: 8,929 14N1, 335 14P1, 2 14E3 (the sample is included by another group); group 36: 1,175 36N1 and 273 36P1; group 52: none.

## Liver area (DEC-047 section 5)

| Split | Own `liver` polygon | Fallback from the image | No liver area |
|---|---|---|---|
| train | 10,292 | 5 | 34 |
| val | 2,058 | 6 | 4 |
| test | 1,370 | 1 | 7 |
| all | 13,720 | 12 | 45 |

---

## Earlier file (TASK-087, superseded; do not use)

### Result (TASK-087 file)

- Sample file: `derived/cirrhosis_v4_samples_df.pkl` in `261023_plain` (plain, machine01 only), columns: sample number, `taskcrops_df` ids, datasource group, positive, split. An encrypted copy is in the enc1 store at the same path ([DEC-024](../../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).
- Table sha256: `854a87c949ab0a64bbad92c985a7938a212ec2ae14901660c04305e0da066f66` (checked on the plain file after the run). A changed table is a new file name (DEC-044 rule 7).
- Seed 87 (test search and train/val split); minimum shorter side 128 px (chosen by the user, 2026-11-05).
- **The Qwen3-VL quality step was not used** (DEC-046; DEC-044 rule 6 does not apply). Bad samples are left out only by `quality` or `exclusion` choice labels and by frames skipped in the local project "[TASK-032](../../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes v1" (66 skipped of 1,371 tasks at the time: 802 submitted, 66 skipped, 503 still to go). Poor-quality crops with neither a label nor a skip stay in the set.

### Counts after each filter step

| Step | Samples | Positives | Negatives | Groups |
|---|---|---|---|---|
| 1 All samples | 31,104 | - | - | 70 |
| 2 Eligible (DEC-043, rule 3) | 19,047 | 4,467 | 14,580 | 62 |
| 3 No `quality` or `exclusion` choice (rule 4) | 16,300 | 3,083 | 13,217 | 60 |
| 4 Frame not skipped in v1 (rule 4) | 16,251 | 3,047 | 13,204 | 60 |
| 5 Shorter side at least 128 px (rule 5) | 16,181 | 3,047 | 13,134 | 59 |

Positive share of the final set: 18.8% (3,047 of 16,181).

### Counts per split

| Split | Samples | Share of samples | Positives | Negatives | Positive share | Groups |
|---|---|---|---|---|---|---|
| train | 12,135 | 75.0% | 2,286 | 9,849 | 18.8% | 47 |
| val | 2,428 | 15.0% | 457 | 1,971 | 18.8% | 45 |
| test | 1,618 | 10.0% | 304 | 1,314 | 18.8% | 12 |
| all | 16,181 | 100% | 3,047 | 13,134 | 18.8% | 59 |

Group counts do not add up: train and val share datasources (random split, DEC-044 rule 10); the 12 test groups are in no other split (rule 9). Test cirrhosis share equals the whole set's (18.8%; limit 2 points). All sizes are inside the DEC-044 ranges (train 70-85%, val 15-23%, test 8-13%), so rule 11 did not trigger.

Reading: validation shares datasources with train, so validation scores are optimistic; test is the unbiased split (DEC-044, Consequences).

### Review status per split

Known-good: the frame was finished in v1 without a skip and the crop has no `quality` choice (known-bad crops were dropped by rule 4). Unreviewed: all other samples. Known flags come from `derived/cirrhosis_v4_quality_min128_df.pkl` ([cirrhosis_candidates.md](cirrhosis_candidates.md)).

| Split | Samples | Known-good | of which positive | Unreviewed | of which positive | Known-good share |
|---|---|---|---|---|---|---|
| train | 12,135 | 308 | 84 | 11,827 | 2,202 | 2.5% |
| val | 2,428 | 51 | 11 | 2,377 | 446 | 2.1% |
| test | 1,618 | 94 | 22 | 1,524 | 282 | 5.8% |
| all | 16,181 | 453 | 117 | 15,728 | 2,930 | 2.8% |

Only 2.8% of samples were looked at by the user. The rest may hold dark, blurred or marked crops that no label caught. Test has a higher known-good share (5.8%) than train (2.5%).
