# Cirrhosis v4 sample file and train/val/test split on 261023_plain

[TASK-087](../../../backlog/tasks/task-087%20-%20Fix-the-cirrhosis-sample-file-and-its-train-val-test-split-dataset-record-with-counts-per-split-DEC-044.md), [DEC-044](../../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md), [DEC-046](../../decisions/DEC-046-cirrhosis-v4-drops-the-qwen3-vl-quality-step.md), [DEC-043](../../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md). Aggregates only; no images, file names or identifiers. Counts and a fixed split, no model. Reporting checklists (CLAIM, STARD): not applicable.

Made on 2026-11-05 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)) with `sonoai-data sample-set freeze 261023_plain --min-side 128 --no-verdicts --seed 87` (code with `--no-verdicts`, [TASK-095](../../../backlog/tasks/task-095%20-%20sample-set-freeze-explicit-no-verdicts-flag-so-the-cirrhosis-v4-sample-file-is-fixed-without-the-Qwen3-VL-step-DEC-046.md)). Task `lseg_cirrhosis_v4`. Candidate list and size report: [cirrhosis_candidates.md](cirrhosis_candidates.md).

## Result

- Sample file: `derived/cirrhosis_v4_samples_df.pkl` in `261023_plain` (plain, machine01 only), columns: sample number, `taskcrops_df` ids, datasource group, positive, split. An encrypted copy is in the enc1 store at the same path ([DEC-024](../../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).
- Table sha256: `854a87c949ab0a64bbad92c985a7938a212ec2ae14901660c04305e0da066f66` (checked on the plain file after the run). A changed table is a new file name (DEC-044 rule 7).
- Seed 87 (test search and train/val split); minimum shorter side 128 px (chosen by the user, 2026-11-05).
- **The Qwen3-VL quality step was not used** (DEC-046; DEC-044 rule 6 does not apply). Bad samples are left out only by `quality` or `exclusion` choice labels and by frames skipped in the local project "[TASK-032](../../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes v1" (66 skipped of 1,371 tasks at the time: 802 submitted, 66 skipped, 503 still to go). Poor-quality crops with neither a label nor a skip stay in the set.

## Counts after each filter step

| Step | Samples | Positives | Negatives | Groups |
|---|---|---|---|---|
| 1 All samples | 31,104 | - | - | 70 |
| 2 Eligible (DEC-043, rule 3) | 19,047 | 4,467 | 14,580 | 62 |
| 3 No `quality` or `exclusion` choice (rule 4) | 16,300 | 3,083 | 13,217 | 60 |
| 4 Frame not skipped in v1 (rule 4) | 16,251 | 3,047 | 13,204 | 60 |
| 5 Shorter side at least 128 px (rule 5) | 16,181 | 3,047 | 13,134 | 59 |

Positive share of the final set: 18.8% (3,047 of 16,181).

## Counts per split

| Split | Samples | Share of samples | Positives | Negatives | Positive share | Groups |
|---|---|---|---|---|---|---|
| train | 12,135 | 75.0% | 2,286 | 9,849 | 18.8% | 47 |
| val | 2,428 | 15.0% | 457 | 1,971 | 18.8% | 45 |
| test | 1,618 | 10.0% | 304 | 1,314 | 18.8% | 12 |
| all | 16,181 | 100% | 3,047 | 13,134 | 18.8% | 59 |

Group counts do not add up: train and val share datasources (random split, DEC-044 rule 10); the 12 test groups are in no other split (rule 9). Test cirrhosis share equals the whole set's (18.8%; limit 2 points). All sizes are inside the DEC-044 ranges (train 70-85%, val 15-23%, test 8-13%), so rule 11 did not trigger.

Reading: validation shares datasources with train, so validation scores are optimistic; test is the unbiased split (DEC-044, Consequences).

## Review status per split

Known-good: the frame was finished in v1 without a skip and the crop has no `quality` choice (known-bad crops were dropped by rule 4). Unreviewed: all other samples. Known flags come from `derived/cirrhosis_v4_quality_min128_df.pkl` ([cirrhosis_candidates.md](cirrhosis_candidates.md)).

| Split | Samples | Known-good | of which positive | Unreviewed | of which positive | Known-good share |
|---|---|---|---|---|---|---|
| train | 12,135 | 308 | 84 | 11,827 | 2,202 | 2.5% |
| val | 2,428 | 51 | 11 | 2,377 | 446 | 2.1% |
| test | 1,618 | 94 | 22 | 1,524 | 282 | 5.8% |
| all | 16,181 | 453 | 117 | 15,728 | 2,930 | 2.8% |

Only 2.8% of samples were looked at by the user. The rest may hold dark, blurred or marked crops that no label caught. Test has a higher known-good share (5.8%) than train (2.5%).
