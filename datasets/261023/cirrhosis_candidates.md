# Cirrhosis candidate samples on 261023_plain: counts per filter step and size report

[TASK-085](../../../backlog/tasks/task-085%20-%20Cirrhosis-candidate-samples-on-261023_plain-counts-per-filter-step-and-the-size-report-the-user-picks-the-minimum-crop-side-DEC-044.md), [DEC-044](../../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md), [DEC-043](../../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md). Aggregates only; no images, file names or identifiers. Counts, no model, no split. Reporting checklists (CLAIM, STARD): not applicable.

Computed on 2026-11-05 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)) with `sonoai-data sample-set candidates 261023_plain` from the code repo at commit eb57cd5 ([TASK-083](../../../backlog/tasks/task-083%20-%20Sample-set-builder-one-sample-per-image-and-crop-box-rule-filters-with-counts-size-report-datasource-group-test-split-and-random-train-val-DEC-044.md)). Task `lseg_cirrhosis_v4`. Sample = one image plus one crop box (DEC-044 rule 1); a group is a set of datasources that share an image.

## Terms

- **Sample**: image hash plus crop box. **Positive**: has a cirrhosis polygon. **Group**: datasource group (DEC-044 rule 2).
- **Frame skipped in v1**: skipped in the local project "B-mode boxes v1". The skipped list was refreshed from the local Label Studio before the run (66 skipped of 1,371 tasks; the saved list had 8). Later skips are not in this table.

## Counts after each step (DEC-044 rules 3-4)

| Step | Samples | Positives | Negatives | Groups |
|---|---|---|---|---|
| 1 All samples | 31,104 | - | - | 70 |
| 2 Eligible (DEC-043) | 19,047 | 4,467 | 14,580 | 62 |
| 3 No `quality` or `exclusion` choice | 16,300 | 3,083 | 13,217 | 60 |
| 4 Frame not skipped in v1 | 16,251 | 3,047 | 13,204 | 60 |

Positive share after step 4: 18.8% (3,047 of 16,251).

## Size report (rule 5): samples after step 4 by shorter side of the crop

Shorter side = min(width, height) of the crop box, in pixels of the source image.

| Minimum (px) | Dropped | Dropped positive | Dropped negative | Kept | Kept positive | Kept negative | Kept groups |
|---|---|---|---|---|---|---|---|
| 64 | 0 | 0 | 0 | 16,251 | 3,047 | 13,204 | 60 |
| 96 | 69 | 0 | 69 | 16,182 | 3,047 | 13,135 | 59 |
| 128 | 70 | 0 | 70 | 16,181 | 3,047 | 13,134 | 59 |
| 160 | 94 | 2 | 92 | 16,157 | 3,045 | 13,112 | 59 |
| 192 | 115 | 2 | 113 | 16,136 | 3,045 | 13,091 | 59 |
| 224 | 128 | 2 | 126 | 16,123 | 3,045 | 13,078 | 59 |
| 256 | 832 | 39 | 793 | 15,419 | 3,008 | 12,411 | 58 |

Reading: the loss is small up to 224 px (at most 0.8% of samples, 2 positives); 256 px drops 5.1% of samples (39 positives, 1.3% of positives) and one more group. One group is lost already at 96 px.

## Tables written inside `261023_plain` (`derived/`, plain, never leave machine01)

- `derived/cirrhosis_v4_candidates_df.pkl`: the 16,251 samples after step 4 (output of the command).
- `derived/cirrhosis_v4_quality_samples_df.pkl`: the 19,047 eligible samples with a `known` column (good, bad or empty) and `in_candidates` (true for the 16,251 candidates). It is the `--samples` table for `sonoai-label ai-label frames --question quality`, so that bad examples are in the list.
- `derived/cirrhosis_v4_quality_min128_df.pkl`: the same, for samples with shorter side at least 128 px (see below).

**Known rule** (accepted, task note of TASK-085; "quality only", 2026-11-05): bad if the crop has a choice label with role `quality`, or its frame was skipped in v1; good if its frame was finished in v1 without a skip; the quality choice wins when both apply. Everything else, including crops whose only filter choice has role `exclusion`, is unknown (empty). Note that step 3 above still drops quality and exclusion crops from the candidates.

| known | Samples (eligible) | Groups | Samples (at least 128 px) | Groups |
|---|---|---|---|---|
| good | 453 | 54 | 453 | 54 |
| bad | 1,442 | 36 | 1,413 | 35 |
| unknown | 17,152 | - | 17,080 | - |
| total | 19,047 | 62 | 18,946 | 61 |

Bad splits into 1,388 by a quality choice only, 49 by a skip only and 5 with both (1,393 have a quality choice). Exclusion-only crops (no quality choice, frame not skipped): 1,354, all unknown; 30 of them sit in frames finished in v1 and are not counted as good. Known-good is small because only 802 of 1,371 v1 tasks were finished when this was computed (503 still to go), so the acceptance test of DEC-044 rule 6 has 453 known-good samples. The known column was made with a one-off script, not repo code.

The candidate crop list for the GPU box exists only as enc1 (`ai-label frames`); no plain list leaves machine01 ([DEC-024](../../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).

## Chosen minimum shorter side

Chosen by the user on 2026-11-05: **128 px** shorter side (DEC-044 rule 5). It leaves 16,181 samples (3,047 positives, 13,134 negatives, 59 groups) after step 5.

The 128 px table is `derived/cirrhosis_v4_quality_min128_df.pkl` (plain, machine01 only): 18,946 samples in 61 groups, of which 16,181 are candidates; known counts in the table above.

The enc1 crop list for the GPU box is not made yet: `ai-label frames --question quality` needs a few-shot examples table from the search part (a prompt-tuning input) and the data passphrase typed by the user.
