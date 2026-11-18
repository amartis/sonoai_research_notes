# Epic 1 anatomy candidate table of dataset version 261023 (G+Q+C+S, shorter side at least 224 px)

[TASK-164 (epic 1 anatomy candidate table on 261023_plain)](../../../backlog/tasks/task-164%20-%20Epic-1-anatomy-candidate-table-on-261023_plain-run-the-TASK-163-builder-at-224-px-dataset-record-with-counts-per-flag-organ-state-and-datasource-group-polygon-overlap-and-in-crop-area-DEC-069.md), [DEC-069 (epic 1 data preparation)](../../decisions/DEC-069-epic1-data-preparation.md), [DIS-033 (epic 1 data preparation)](../../discussions/DIS-033-epic1-data-preparation.md). Inputs: [sample_label_index.md](sample_label_index.md), [sample_label_presence.md](sample_label_presence.md). Table format: [derived.md](../../../docs/datasets/styles/derived.md). Names follow the [glossary](../../../docs/glossary.md).

**Status: descriptive counts, first build; for the user to read before point 3 (splitting).** The record counts which samples of 261023 are candidates for the epic 1 anatomy task under the filters DEC-069 fixed. It sets no rule and no threshold; the three points in the section "For the user" wait for the user. Aggregates only: no images, file names, folder names or identifiers. Datasource group numbers are the integer `datasource_id` groups used in the dataset records. Built on 2026-11-18 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)). Not reviewed.

Reporting checklists (CLAIM, STARD): not applicable. These are counts of a filter; no model is trained or evaluated and no split is made. No confidence intervals: every number is a complete count of the dataset version, not an estimate from a sample.

Key: sample = one crop of the sample-label index v1 (n = 29,233); candidate = a sample with none of the exclusion flags G, Q, C, S (G: no first-set organ is positive or negative; Q: the sample has a quality-skip fact item; C: a first-set organ is positive without a polygon; S: the crop box's shorter side is below 224 px; defined in full in Summary item 2); first set = liver, kidney, stomach, gallbladder ([DEC-066](../../decisions/DEC-066-epic1-model-task-label-set-softmax.md)); pair = one sample and one first-set organ; state = presence state under `strict_v1` (positive, negative, or unknown when the pair is not in the presence table); datasource group = the group of the sample's labeling task with the lowest `taskcrops_df` id ([DEC-044](../../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 2, as the builder does).

## Summary

1. **20,011 of 29,233 samples (68.5%) are candidates**; 9,222 (31.5%) are excluded.
2. **The rule** (DEC-069 Table 1): a sample is out when any of G (no first-set organ is positive or negative), Q (a quality-skip fact item), C (a first-set organ positive without a polygon) or S (the crop box's shorter side is below **224 px** of the source image; a side of exactly 224 is kept) holds. Same filters for every split.
3. **G excludes 9,063 samples, S 938, Q 3,518, C 0.** Overlaps between flags are in Table 2. S alone removes 159 samples that G and Q keep.
4. **Positive pairs lost are few and all through S**: liver 137 of 15,325 (0.9%), kidney 93 of 9,982 (0.9%), stomach 10 of 3,562 (0.3%), gallbladder 45 of 2,212 (2.0%). G cannot remove a positive and Q removes none (0). The first-set pairs lost by G and Q are mostly unknown ones.
5. **Eleven datasource groups (3,061 samples) have no candidate left**, and 16 datasource groups have at least half of their samples excluded (6,790 of 8,122). Details in Table 5 and Table A2.
6. **Overlap is rare except for the gallbladder** (among candidates, 58.9% of its positive pairs overlap another first-set organ's mask; liver 10.6%, stomach 4.9%, kidney 3.0%; Table 6, where the all-samples shares are also given). 3 liver positive pairs have a polygon that covers no pixel of the crop.

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

Table 1. Samples excluded and left per set of flags (n = 29,233 samples; excluded = any flag of the set; G = no first-set organ positive or negative, Q = quality-skip fact item, C = first-set organ positive without a polygon, S = crop box shorter side below 224 px). The sets that differ are shown; all 15 are in Table A1.

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
| Q only, or any pattern with C | 0 |

Every sample with Q also has G (3,518 = 3,492 + 26): a quality-skip sample has no first-set organ positive or negative, so Q adds nothing beyond G in this dataset version.

## 2. Organs and states

Table 3. First-set pairs per organ and state, all samples and candidates (n = 29,233 samples; n = 20,011 candidates; each organ's three states add up to 29,233 for all samples and to 20,011 for candidates). Positive pairs without a polygon are 0 for every organ.

| Organ | Positive, all | Positive, candidates | Negative, all | Negative, candidates | Unknown, all | Unknown, candidates |
|---|---|---|---|---|---|---|
| liver | 15,325 | 15,188 | 4,303 | 4,281 | 9,605 | 542 |
| kidney | 9,982 | 9,889 | 5,610 | 5,564 | 13,641 | 4,558 |
| stomach | 3,562 | 3,552 | 11,032 | 10,953 | 14,639 | 5,506 |
| gallbladder | 2,212 | 2,167 | 12,765 | 12,728 | 14,256 | 5,116 |

Table 4. Positive pairs lost by the filters, per organ (n = positive pairs of all samples; lost = the pair's sample is excluded; all losses are through S).

| Organ | Positive pairs, n | Lost | Lost share, % | Left |
|---|---|---|---|---|
| liver | 15,325 | 137 | 0.9 | 15,188 |
| kidney | 9,982 | 93 | 0.9 | 9,889 |
| stomach | 3,562 | 10 | 0.3 | 3,552 |
| gallbladder | 2,212 | 45 | 2.0 | 2,167 |

20,011 candidates; 19,870 of them have at least one first-set positive (141 have only negatives).

## 3. Datasource groups

67 groups; 56 keep at least one candidate. Table 5 lists the datasource groups that have at least 25% of their samples excluded (21 of 67); the other 46 lose less (44 of them under 15%). The full table of 67 datasource groups is Table A2.

Table 5. Datasource groups with at least 25% of their samples excluded (n = samples of the datasource group; excluded = not a candidate; the other 46 datasource groups are in Table A2).

| Datasource group | Samples, n | Excluded | Excluded share, % | Left (candidates) |
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
| 201 | 2,474 | 1,634 | 66.0 | 840 |
| 203 | 1,056 | 454 | 43.0 | 602 |
| 11 | 60 | 22 | 36.7 | 38 |
| 204 | 1,013 | 293 | 28.9 | 720 |
| 161 | 11 | 3 | 27.3 | 8 |
| 118 | 1,116 | 285 | 25.5 | 831 |

Reading: the 11 datasource groups with no candidate hold 3,061 samples (10.5% of 29,233; G in 2,982, Q in 50, S in 857 of them). The exclusion is mainly G for the large datasource groups (5, 6, 115, 118, 201, 203, 204: no first-set organ positive or negative); S hits every sample of datasource groups 14, 48 and 9 (500, 250 and 100 samples, together with G) and 26 of 28 samples of datasource group 141 (no G there: S is its whole exclusion). Largest numbers of candidates left, by datasource group: 116 (2,723 of 3,294), 121 (1,854), 2 (1,421), 122 (1,056), 119 (1,020).

## 4. Polygon overlap and in-crop area (DEC-069 rule 6, DIS-033 point d)

A positive pair's mask is the union of its polygons placed in the crop as the training reader places them; overlap = at least one pixel shared with the mask of another first-set organ that is positive with a polygon. The builder defines the measures; none of them is a rule.

Table 6. Positive pairs with polygon whose mask overlaps another first-set positive organ's mask (n = pairs; overlapping share = overlapping pairs / pairs; pooled share = sum of overlap pixels / sum of mask pixels; median and max are over the overlapping pairs, of overlap pixels / the pair's own mask pixels; all shares in %).

| Organ | Subset | Pairs, n | With pixels | Overlapping | Overlapping share, % | Pooled share, % | Median overlap, % of the pair's mask | Maximum overlap, % of the pair's mask |
|---|---|---|---|---|---|---|---|---|
| liver | all | 15,325 | 15,322 | 1,626 | 10.6 | 0.1 | 0.4 | 98.3 |
| liver | candidates | 15,188 | 15,185 | 1,606 | 10.6 | 0.1 | 0.4 | 98.3 |
| kidney | all | 9,982 | 9,982 | 304 | 3.0 | 0.0 | 0.4 | 99.2 |
| kidney | candidates | 9,889 | 9,889 | 292 | 3.0 | 0.0 | 0.3 | 99.2 |
| stomach | all | 3,562 | 3,562 | 175 | 4.9 | 0.1 | 0.4 | 95.6 |
| stomach | candidates | 3,552 | 3,552 | 173 | 4.9 | 0.1 | 0.4 | 95.6 |
| gallbladder | all | 2,212 | 2,212 | 1,283 | 58.0 | 2.1 | 3.2 | 100.0 |
| gallbladder | candidates | 2,167 | 2,167 | 1,276 | 58.9 | 2.1 | 3.2 | 100.0 |

Table 7. Positive pairs with polygon by in-crop mask area, share of the crop area (n = pairs; candidates only, n = 20,011 samples; bins `[lo, hi)`, the last `[0.5, 1]`; the all-samples counts are in Table A3).

| Organ | In-crop area, share of the crop: [0, 0.001) | [0.001, 0.01) | [0.01, 0.05) | [0.05, 0.1) | [0.1, 0.25) | [0.25, 0.5) | [0.5, 1] | Total |
|---|---|---|---|---|---|---|---|---|
| liver | 3 | 8 | 2,036 | 3,950 | 6,734 | 2,267 | 190 | 15,188 |
| kidney | 0 | 2 | 3,389 | 3,463 | 2,850 | 183 | 2 | 9,889 |
| stomach | 1 | 605 | 2,902 | 43 | 1 | 0 | 0 | 3,552 |
| gallbladder | 8 | 202 | 1,583 | 278 | 85 | 11 | 0 | 2,167 |

Table 8. Positive pairs with polygon by in-crop mask area in pixels of the crop (n = pairs; candidates only; the columns are `[lo, hi)`, the last is 50,000 and above; the all-samples counts are in Table A4).

| Organ | In-crop area, px: 0 (no pixel) | 1 to 99 | 100 to 999 | 1,000 to 9,999 | 10,000 to 49,999 | 50,000 and above | Total |
|---|---|---|---|---|---|---|---|
| liver | 3 | 0 | 0 | 577 | 5,609 | 8,999 | 15,188 |
| kidney | 0 | 0 | 1 | 159 | 5,050 | 4,679 | 9,889 |
| stomach | 0 | 0 | 49 | 1,608 | 1,873 | 22 | 3,552 |
| gallbladder | 0 | 4 | 88 | 1,256 | 785 | 34 | 2,167 |

The 224 px filter changes the small-pixel bins (Table A4 for all samples, Table 8 for candidates) differently per organ: liver 100 to 999 px, 42 pairs to 0; kidney 100 to 999 px, 61 to 1; stomach 1 to 99 px, 2 to 0, and 100 to 999 px, 57 to 49; gallbladder 1 to 99 px, 5 to 4, and 100 to 999 px, 92 to 88. So it removes nearly all small-mask pairs of liver and kidney, and only part of those of stomach and gallbladder. Mask areas are in pixels of the source-image crop, before the stretch to 224 x 224.

## For the user

No rule is proposed here (DEC-069: a rule is added only by a new DEC, if the counts call for it). Three things to look at:

1. **Datasource groups with little or nothing left.** 11 datasource groups (3,061 samples) have no candidate; datasource groups 5, 6, 115 and 201 keep 186, 278, 26 and 840 of 756, 1,261, 542 and 2,474. This matters for the split by datasource group (point 3): 56 datasource groups remain.
2. **Gallbladder.** It has the fewest positives (2,167 in candidates) and the largest relative loss of positive pairs (2.0%); 58.9% of its candidate positive pairs overlap another organ's mask (Table 6), though the overlap is 2.1% of its mask pixels pooled and a median of 3.2% of the pair's mask per overlapping pair. The overlap is mostly small slivers; the maximum is 100.0% for some pairs (the whole mask lies inside another organ's mask).
3. **Tiny areas.** In candidates, pairs whose mask is under 0.1% of the crop: liver 3, stomach 1, gallbladder 8 (kidney 0); 3 liver pairs have no pixel in the crop (a polygon that falls outside or collapses after clipping). Under 1% of the crop: stomach 606, gallbladder 210, liver 11, kidney 2. Whether to drop, keep or cap them is the user's decision.

## Limitations

Counts only; no check of label quality inside the crops. Datasource groups follow the lowest labeling task id (DEC-044), so a sample whose tasks come from several datasource groups is counted in one. The overlap counts assume the tag-to-label mapping of the index; they were not recounted outside the builder.

## Appendix: complete report counts

All counts of the builder report that the tables above show in part (aggregates only; the same run and table as in Method).

Table A1. Samples excluded and left per set of flags (n = 29,233 samples; excluded = any flag of the set; C is 0 everywhere, so a set with C equals the set without it).

| Flags applied | Excluded | Left |
|---|---|---|
| G | 9,063 | 20,170 |
| Q | 3,518 | 25,715 |
| C | 0 | 29,233 |
| S | 938 | 28,295 |
| G+Q | 9,063 | 20,170 |
| G+C | 9,063 | 20,170 |
| G+S | 9,222 | 20,011 |
| Q+C | 3,518 | 25,715 |
| Q+S | 4,430 | 24,803 |
| C+S | 938 | 28,295 |
| G+Q+C | 9,063 | 20,170 |
| G+Q+S | 9,222 | 20,011 |
| G+C+S | 9,222 | 20,011 |
| Q+C+S | 4,430 | 24,803 |
| G+Q+C+S | 9,222 | 20,011 |

Table A2. All 67 datasource groups (n = samples of the datasource group; excluded = not a candidate; every row checked against the written table).

| Datasource group | Samples, n | Excluded | Excluded share, % | Left (candidates) |
|---|---|---|---|---|
| 1 | 616 | 1 | 0.2 | 615 |
| 2 | 1,559 | 138 | 8.9 | 1,421 |
| 3 | 735 | 67 | 9.1 | 668 |
| 4 | 226 | 25 | 11.1 | 201 |
| 5 | 756 | 570 | 75.4 | 186 |
| 6 | 1,261 | 983 | 78.0 | 278 |
| 7 | 120 | 8 | 6.7 | 112 |
| 8 | 100 | 1 | 1.0 | 99 |
| 9 | 100 | 100 | 100.0 | 0 |
| 10 | 400 | 51 | 12.8 | 349 |
| 11 | 60 | 22 | 36.7 | 38 |
| 12 | 722 | 722 | 100.0 | 0 |
| 13 | 781 | 781 | 100.0 | 0 |
| 14 | 500 | 500 | 100.0 | 0 |
| 47 | 261 | 261 | 100.0 | 0 |
| 48 | 250 | 250 | 100.0 | 0 |
| 49 | 228 | 228 | 100.0 | 0 |
| 50 | 159 | 159 | 100.0 | 0 |
| 51 | 57 | 57 | 100.0 | 0 |
| 112 | 330 | 24 | 7.3 | 306 |
| 113 | 32 | 1 | 3.1 | 31 |
| 114 | 763 | 0 | 0.0 | 763 |
| 115 | 542 | 516 | 95.2 | 26 |
| 116 | 3,294 | 571 | 17.3 | 2,723 |
| 117 | 2 | 2 | 100.0 | 0 |
| 118 | 1,116 | 285 | 25.5 | 831 |
| 119 | 1,312 | 292 | 22.3 | 1,020 |
| 120 | 47 | 0 | 0.0 | 47 |
| 121 | 1,866 | 12 | 0.6 | 1,854 |
| 122 | 1,097 | 41 | 3.7 | 1,056 |
| 124 | 34 | 2 | 5.9 | 32 |
| 126 | 681 | 18 | 2.6 | 663 |
| 127 | 39 | 0 | 0.0 | 39 |
| 128 | 170 | 2 | 1.2 | 168 |
| 129 | 315 | 0 | 0.0 | 315 |
| 130 | 143 | 0 | 0.0 | 143 |
| 131 | 70 | 0 | 0.0 | 70 |
| 132 | 72 | 1 | 1.4 | 71 |
| 133 | 150 | 1 | 0.7 | 149 |
| 135 | 16 | 0 | 0.0 | 16 |
| 137 | 69 | 1 | 1.4 | 68 |
| 138 | 492 | 25 | 5.1 | 467 |
| 140 | 1 | 1 | 100.0 | 0 |
| 141 | 28 | 26 | 92.9 | 2 |
| 142 | 55 | 1 | 1.8 | 54 |
| 143 | 1 | 0 | 0.0 | 1 |
| 144 | 41 | 0 | 0.0 | 41 |
| 145 | 277 | 0 | 0.0 | 277 |
| 146 | 127 | 1 | 0.8 | 126 |
| 147 | 31 | 1 | 3.2 | 30 |
| 148 | 314 | 2 | 0.6 | 312 |
| 149 | 32 | 1 | 3.1 | 31 |
| 150 | 166 | 0 | 0.0 | 166 |
| 151 | 8 | 0 | 0.0 | 8 |
| 153 | 194 | 0 | 0.0 | 194 |
| 154 | 304 | 0 | 0.0 | 304 |
| 155 | 467 | 1 | 0.2 | 466 |
| 156 | 168 | 5 | 3.0 | 163 |
| 157 | 5 | 0 | 0.0 | 5 |
| 158 | 174 | 0 | 0.0 | 174 |
| 159 | 21 | 0 | 0.0 | 21 |
| 160 | 146 | 2 | 1.4 | 144 |
| 161 | 11 | 3 | 27.3 | 8 |
| 201 | 2,474 | 1,634 | 66.0 | 840 |
| 202 | 576 | 79 | 13.7 | 497 |
| 203 | 1,056 | 454 | 43.0 | 602 |
| 204 | 1,013 | 293 | 28.9 | 720 |

Table A3. Positive pairs with polygon by in-crop mask area, share of the crop area, all samples (n = pairs; bins `[lo, hi)`, the last `[0.5, 1]`; candidates are in Table 7).

| Organ | [0, 0.001) | [0.001, 0.01) | [0.01, 0.05) | [0.05, 0.1) | [0.1, 0.25) | [0.25, 0.5) | [0.5, 1] | Total |
|---|---|---|---|---|---|---|---|---|
| liver | 3 | 8 | 2,039 | 3,971 | 6,810 | 2,299 | 195 | 15,325 |
| kidney | 0 | 2 | 3,390 | 3,497 | 2,903 | 188 | 2 | 9,982 |
| stomach | 1 | 606 | 2,910 | 44 | 1 | 0 | 0 | 3,562 |
| gallbladder | 8 | 202 | 1,598 | 297 | 96 | 11 | 0 | 2,212 |

Table A4. Positive pairs with polygon by in-crop mask area in pixels of the crop, all samples (n = pairs; bins `[lo, hi)`, the last 50,000 and above; candidates are in Table 8).

| Organ | [0, 1) | [1, 100) | [100, 1000) | [1000, 10000) | [10000, 50000) | [50000, inf) | Total |
|---|---|---|---|---|---|---|---|
| liver | 3 | 0 | 42 | 663 | 5,618 | 8,999 | 15,325 |
| kidney | 0 | 0 | 61 | 187 | 5,055 | 4,679 | 9,982 |
| stomach | 0 | 2 | 57 | 1,608 | 1,873 | 22 | 3,562 |
| gallbladder | 0 | 5 | 92 | 1,293 | 788 | 34 | 2,212 |
