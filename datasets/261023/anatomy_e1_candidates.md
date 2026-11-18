# Epic 1 anatomy candidate table of dataset version 261023 (G+Q+C+S, shorter side at least 224 px)

[TASK-164 (epic 1 anatomy candidate table on 261023_plain)](../../../backlog/tasks/task-164%20-%20Epic-1-anatomy-candidate-table-on-261023_plain-run-the-TASK-163-builder-at-224-px-dataset-record-with-counts-per-flag-organ-state-and-datasource-group-polygon-overlap-and-in-crop-area-DEC-069.md), [DEC-069 (epic 1 data preparation)](../../decisions/DEC-069-epic1-data-preparation.md), [DIS-033 (epic 1 data preparation)](../../discussions/DIS-033-epic1-data-preparation.md). Inputs: [sample_label_index.md](sample_label_index.md), [sample_label_presence.md](sample_label_presence.md). Table format: [derived.md](../../../docs/datasets/styles/derived.md). Names follow the [glossary](../../../docs/glossary.md).

**Status: descriptive counts, first build; for the user to read before point 3 (splitting).** The record counts which samples of 261023 are candidates for the epic 1 anatomy task under the filters DEC-069 fixed. It sets no rule and no threshold; the three points in the section "For the user" wait for the user. Aggregates only: no images, file names, folder names or identifiers. Datasource group numbers are the integer `datasource_id` groups used in the dataset records. Built on 2026-11-18 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)). Not reviewed.

Reporting checklists (CLAIM, STARD): not applicable. These are counts of a filter; no model is trained or evaluated and no split is made. No confidence intervals: every number is a complete count of the dataset version, not an estimate from a sample.

Key: sample = one crop of the sample-label index v1 (n = 29,233); candidate = a sample with none of the flags G, Q, C, S; first set = liver, kidney, stomach, gallbladder ([DEC-066](../../decisions/DEC-066-epic1-model-task-label-set-softmax.md)); pair = one sample and one first-set organ; state = presence state under `strict_v1` (positive, negative, or unknown when the pair is not in the presence table); datasource group = the group of the sample's labeling task with the lowest `taskcrops_df` id ([DEC-044](../../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 2, as the builder does).

## Summary

1. **20,011 of 29,233 samples (68.5%) are candidates**; 9,222 (31.5%) are excluded.
2. **The rule** (DEC-069 Table 1): a sample is out when any of G (no first-set organ is positive or negative), Q (a quality-skip fact item), C (a first-set organ positive without a polygon) or S (the crop's shorter side is below **224 px** of the source image; a side of exactly 224 is kept) holds. Same filters for every split.
3. **G excludes 9,063 samples, S 938, Q 3,518, C 0.** Overlaps between flags are in Table 2. S alone removes 159 samples that G and Q keep.
4. **Positive pairs lost are few and all through S**: liver 137 of 15,325 (0.9%), kidney 93 of 9,982 (0.9%), stomach 10 of 3,562 (0.3%), gallbladder 45 of 2,212 (2.0%). G cannot remove a positive and Q removes none (0). The first-set pairs lost by G and Q are mostly unknown ones.
5. **Eleven datasource groups (3,061 samples) have no candidate left**, and 16 groups lose at least half of their samples (6,790 of 8,122). Details in Table 5.
6. **Overlap is rare except for the gallbladder** (58.0% of its positive pairs overlap another first-set organ's polygon; liver 10.6%, stomach 4.9%, kidney 3.1%; Table 6). 3 liver positive pairs have a polygon that covers no pixel of the crop.

## Method

**Tables read** (plain style via `sonoai.paths.dataset_dir`, [DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md); the list was approved with TASK-164): `derived/sample_label_index_v1_df.pkl`, `derived/sample_label_presence_strictv1_df.pkl`, `images/taskcrops_df.pkl`, `labels/polygons_df.pkl`. **Written** (a new file; no table was changed, [DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md)): `derived/anatomy_e1_candidates_v1_261023_plain_df.pkl` (29,233 rows, 19 columns: sample number, crop box and sides, `short_side`, `group`, the four flags `flag_G`, `flag_Q`, `flag_C`, `flag_S`, `candidate`, and `state_liver`, `state_kidney`, `state_stomach`, `state_gallbladder`). No split is in the table (DEC-069 item 7).

Command (writes the one new file under `derived/`; refuses when it exists; run first with `--report-only`, which wrote nothing, and the two runs printed identical reports):

```bash
sonoai-data anatomy-e1-candidates 261023_plain --config configs/data/anatomy_e1.yaml
```

| Item | Value |
|---|---|
| Config | `configs/data/anatomy_e1.yaml`, `version: 1`, `index: v1`, `policy: strict_v1`, `min_side: 224` |
| Code commit | `d87fd045153efdfb5d65a747a1d989450efb1867` (master with the [TASK-163 (candidate builder)](../../../backlog/tasks/task-163%20-%20Epic-1-anatomy-candidate-builder-GQCS-exclusion-flags-at-a-224-px-minimum-side-counts-per-flag-organ-state-and-datasource-group-first-set-polygon-overlap-and-in-crop-polygon-area-report-sonoai-data-command-synthetic-tests-DEC-069.md) builder; the run was made from a worktree at this commit) |
| sha256 of the table | `1448ca703ed84d2839539f242c550bb7259d701d4dbbde37b3b23daf5323eb0d` |
| Run date | 2026-11-18 |

**Checks.** The builder's own checks passed: positive-with-polygon pairs 31,081 (liver 15,325, kidney 9,982, stomach 3,562, gallbladder 2,212), none without polygon rows; positive-without-polygon pairs 0. **Independent recount** from the written table (a separate script, pandas only, on the table itself): the sha256 above, 29,233 unique samples, flag counts, the 6 flag patterns, candidates 20,011, states per organ (all samples and candidates), per-group samples and losses, and G recomputed from the four states (equal to `flag_G` on every row); S recomputed from the crop box (equal to `short_side` below 224, 938). All matched the printed report. The overlap and area counts (Tables 6 to 8) need the polygons and are **not** recounted from the table; they come from the builder, whose two runs agreed.

## 1. Flags

Table 1. Samples excluded and left per set of flags (n = 29,233 samples; excluded = any flag of the set; the rows with C add nothing, C = 0). The full 15 sets are in the builder report; the rows that differ are shown.

| Flags applied | Excluded | Left |
|---|---|---|
| G | 9,063 | 20,170 |
| Q | 3,518 | 25,715 |
| C | 0 | 29,233 |
| S | 938 | 28,295 |
| G+Q | 9,063 | 20,170 |
| G+S | 9,222 | 20,011 |
| Q+S | 4,430 | 24,803 |
| **G+Q+C+S (the rule)** | **9,222** | **20,011** |

Table 2. Samples per exact pattern of flags (n = 29,233; the patterns not listed have 0 samples).

| Pattern | Samples |
|---|---|
| none (candidate) | 20,011 |
| G only | 4,792 |
| G and Q | 3,492 |
| G and S | 753 |
| S only | 159 |
| G, Q and S | 26 |
| Q only, C (any pattern) | 0 |

Every sample with Q also has G (3,518 = 3,492 + 26): a quality-skip sample has no first-set organ in a kept state, so Q adds nothing beyond G in this dataset version.

## 2. Organs and states

Table 3. First-set pairs per organ and state, all samples and candidates (n = 29,233 samples; n = 20,011 candidates; each organ's three states add up to the sample count of its column). Positive pairs without a polygon are 0 for every organ.

| Organ | Positive, all | Positive, candidates | Negative, all | Negative, candidates | Unknown, all | Unknown, candidates |
|---|---|---|---|---|---|---|
| liver | 15,325 | 15,188 | 4,303 | 4,281 | 9,605 | 542 |
| kidney | 9,982 | 9,889 | 5,610 | 5,564 | 13,641 | 4,558 |
| stomach | 3,562 | 3,552 | 11,032 | 10,953 | 14,639 | 5,506 |
| gallbladder | 2,212 | 2,167 | 12,765 | 12,728 | 14,256 | 5,116 |

Table 4. Positive pairs lost by the filters, per organ (n = positive pairs of all samples; lost = the sample is not a candidate; all losses are through S).

| Organ | Positive pairs, n | Lost | Lost share, % | Left |
|---|---|---|---|---|
| liver | 15,325 | 137 | 0.9 | 15,188 |
| kidney | 9,982 | 93 | 0.9 | 9,889 |
| stomach | 3,562 | 10 | 0.3 | 3,552 |
| gallbladder | 2,212 | 45 | 2.0 | 2,167 |

20,011 candidates; 19,870 of them have at least one first-set positive (141 have only negatives).

## 3. Datasource groups

67 groups; 56 keep at least one candidate. Table 5 lists the groups that lose at least 25% of their samples (21 of 67); the other 46 lose less (44 of them under 15%).

Table 5. Datasource groups losing at least 25% of their samples (n = samples of the group; the flag columns count samples with the flag, which overlap; the other groups are not shown).

| Group | Samples, n | Lost | Lost share, % | Left |
|---|---|---|---|---|
| 9 | 100 | 100 | 100.0 | 0 |
| 12 | 722 | 722 | 100.0 | 0 |
| 13 | 781 | 781 | 100.0 | 0 |
| 14 | 500 | 500 | 100.0 | 0 |
| 47 | 261 | 261 | 100.0 | 0 |
| 48 | 250 | 250 | 100.0 | 0 |
| 49 | 228 | 228 | 100.0 | 0 |
| 50 | 159 | 159 | 100.0 | 0 |
| 51 | 57 | 57 | 100.0 | 0 |
| 117 | 2 | 2 | 100.0 | 0 |
| 140 | 1 | 1 | 100.0 | 0 |
| 115 | 542 | 516 | 95.2 | 26 |
| 141 | 28 | 26 | 92.9 | 2 |
| 6 | 1,261 | 983 | 78.0 | 278 |
| 5 | 756 | 570 | 75.4 | 186 |
| 201 | 2,474 | 1,634 | 66.1 | 840 |
| 203 | 1,056 | 454 | 43.0 | 602 |
| 11 | 60 | 22 | 36.7 | 38 |
| 204 | 1,013 | 293 | 28.9 | 720 |
| 161 | 11 | 3 | 27.3 | 8 |
| 118 | 1,116 | 285 | 25.5 | 831 |

Reading: the 11 groups with no candidate hold 3,061 samples (10.5% of 29,233; G in 2,982, Q in 50, S in 857 of them). The loss is G for the large groups (5, 6, 115, 118, 201, 203, 204: no first-set organ in a kept state); S hits every sample of groups 14, 48 and 9 (500, 250 and 100 samples, together with G) and 26 of 28 samples of group 141 (no G there: S is its whole loss). Largest groups left: 116 (2,723 of 3,294), 121 (1,854), 2 (1,421), 122 (1,056), 119 (1,020).

## 4. Polygon overlap and in-crop area (DEC-069 rule 6, DIS-033 point d)

A positive pair's mask is the union of its polygons placed in the crop as the training reader places them; overlap = at least one pixel shared with the mask of another first-set organ that is positive with a polygon. The builder defines the measures; none of them is a rule.

Table 6. Positive pairs with polygon whose mask overlaps another first-set positive organ's mask (n = pairs; share = overlapping / pairs; pooled share = overlap pixels / mask pixels; median and max are over the overlapping pairs, of overlap pixels / mask pixels).

| Organ | Subset | Pairs, n | With pixels | Overlapping | Overlapping share, % | Pooled share, % | Median | Max |
|---|---|---|---|---|---|---|---|---|
| liver | all | 15,325 | 15,322 | 1,626 | 10.6 | 0.05 | 0.004 | 0.983 |
| liver | candidates | 15,188 | 15,185 | 1,606 | 10.6 | 0.05 | 0.004 | 0.983 |
| kidney | all | 9,982 | 9,982 | 304 | 3.0 | 0.02 | 0.004 | 0.992 |
| kidney | candidates | 9,889 | 9,889 | 292 | 3.0 | 0.02 | 0.003 | 0.992 |
| stomach | all | 3,562 | 3,562 | 175 | 4.9 | 0.07 | 0.004 | 0.956 |
| stomach | candidates | 3,552 | 3,552 | 173 | 4.9 | 0.07 | 0.004 | 0.956 |
| gallbladder | all | 2,212 | 2,212 | 1,283 | 58.0 | 2.06 | 0.032 | 1.000 |
| gallbladder | candidates | 2,167 | 2,167 | 1,276 | 58.9 | 2.07 | 0.032 | 1.000 |

Table 7. Positive pairs with polygon by in-crop mask area, share of the crop area (n = pairs; candidates only; the all-samples counts are in the builder report).

| Organ | [0, 0.001) | [0.001, 0.01) | [0.01, 0.05) | [0.05, 0.1) | [0.1, 0.25) | [0.25, 0.5) | [0.5, 1] | Total |
|---|---|---|---|---|---|---|---|---|
| liver | 3 | 8 | 2,036 | 3,950 | 6,734 | 2,267 | 190 | 15,188 |
| kidney | 0 | 2 | 3,389 | 3,463 | 2,850 | 183 | 2 | 9,889 |
| stomach | 1 | 605 | 2,902 | 43 | 1 | 0 | 0 | 3,552 |
| gallbladder | 8 | 202 | 1,583 | 278 | 85 | 11 | 0 | 2,167 |

Table 8. Positive pairs with polygon by in-crop mask area in pixels of the crop (n = pairs; candidates only; the columns are `[lo, hi)`, the last is 50,000 and above).

| Organ | 0 (no pixel) | 1 to 99 | 100 to 999 | 1,000 to 9,999 | 10,000 to 49,999 | 50,000 and above | Total |
|---|---|---|---|---|---|---|---|
| liver | 3 | 0 | 0 | 577 | 5,609 | 8,999 | 15,188 |
| kidney | 0 | 0 | 1 | 159 | 5,050 | 4,679 | 9,889 |
| stomach | 0 | 0 | 49 | 1,608 | 1,873 | 22 | 3,552 |
| gallbladder | 0 | 4 | 88 | 1,256 | 785 | 34 | 2,167 |

In the all-samples counts the small-pixel bins are larger (liver 42 pairs in 100 to 999, kidney 61, stomach 2 in 1 to 99 and 57 in 100 to 999, gallbladder 5 and 92); the 224 px filter removes most of them. Mask areas are in pixels of the source-image crop, before the stretch to 224 x 224.

## For the user

No rule is proposed here (DEC-069: a rule is added only by a new DEC, if the counts call for it). Three things to look at:

1. **Groups with little or nothing left.** 11 groups (3,061 samples) have no candidate; groups 5, 6, 115 and 201 keep 186, 278, 26 and 840 of 756, 1,261, 542 and 2,474. This matters for the split by datasource group (point 3): 56 groups remain.
2. **Gallbladder.** It has the fewest positives (2,167 in candidates) and the largest relative loss (2.0%); 58.9% of its candidate positive pairs overlap another organ's mask, though only 2.07% of its mask pixels pooled and a median of 0.032 of a mask per overlapping pair. The overlap is mostly small slivers; the maximum is 1.000 for some pairs (mask fully inside another organ's mask).
3. **Tiny areas.** In candidates, pairs whose mask is under 0.1% of the crop: liver 3, stomach 1, gallbladder 8 (kidney 0); 3 liver pairs have no pixel in the crop (a polygon that falls outside or collapses after clipping). Under 1% of the crop: stomach 606, gallbladder 210, liver 11, kidney 2. Whether to drop, keep or cap them is the user's decision.

## Limitations

Counts only; no check of label quality inside the crops. Datasource groups follow the lowest labeling task id (DEC-044), so a sample whose tasks come from several groups is counted in one. The overlap counts assume the tag-to-label mapping of the index; they were not recounted outside the builder.
