# Respect statistics of the interpretation rules R01-R64 of dataset version 261023

[TASK-121](../../../backlog/tasks/task-121%20-%20Respect-statistics-of-the-interpretation-rules-R01-R64-of-261023-from-the-sample-label-index-values-only-the-user-sets-thresholds-after-DEC-059.md), [DEC-059](../../decisions/DEC-059-fact-driven-model-sample-label-index-presence-policies.md). Rules: [interpretation_rules.md](interpretation_rules.md) (64 candidate rules, their measure codes, targets and "expected in the data" statements). Sample-label index v1: [sample_label_index.md](sample_label_index.md). Names follow the [glossary](../../../docs/glossary.md) ([DEC-056](../../decisions/DEC-056-labeling-terminology-single-glossary.md), [DEC-057](../../decisions/DEC-057-glossary-for-the-whole-research-project.md)).

**Status: exploratory, descriptive values only.** This record measures how far each rule holds in the labeled data. It sets no threshold, marks no rule kept or dropped, and gives no verdict: the user sets the thresholds after seeing these values ([interpretation_rules.md](interpretation_rules.md), Decisions). Aggregates only: no images, file names, folder names or identifiers; counts of 1 to 4 are shown as `<5`. Measured on 2026-11-13 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)). Not reviewed.

Reporting checklists (CLAIM, STARD): not applicable. This is a count of how labels relate to each other; no model is trained or evaluated and no split is made.

## Summary

1. **59 of the 64 rules were measured; 5 cannot be tested from the tables** (R39, R40, R41, R43, R54; Table 2). Of the 59, R21 and R64 report overlap values instead of a respected share (Tables 12 to 14), and R26 has no case (its subject tag is never given). R08, R09, R16 (signs mark) and R36 (P11) have fewer than 5 cases.
2. **Most within-task rules hold in 96% to 100% of the cases where their subject is given** (R01 to R07, R11 to R13, R15, R16 anatomy and fat marks, R20, R22 to R24, R27 to R32, R34, R36, R37 and R38; Tables 3, 4, 7, 8, 9). R10 holds in fewer than 5 of 6 cases. The values that differ most: R14 29.4% (P9 `checked`), R17 92.3%, R25 0 of 195, R33 91.3% to 100.0% (weak rule), R35 71.0%, R42 0.0% in the strict reading.
3. **R18 (after a skip, nothing else is given) depends on the labeling project**: 100% in most single-finding projects, 0.0% in P1, P7, P9, P14 and P50 (strict reading), 24.3% in P2. Allowing ignored tags raises P1 to 12.8% and P14 to 34.5% and leaves P7, P9 and P50 at about 0% (Table 5, two readings).
4. **R19 (a skip that describes the image leaves the sample out of every project)**: the other projects' tasks carry a skip or have no given labeling in 0.0% to 97.7% of the tasks, depending on the target project (Table 6). It is below 20% for the one-finding projects P19 to P24, P28, P35, P50.
5. **Between-project rules**: routing rules R44 to R47 hold in 99.8% to 100.0% (Table 10). R48 (a "no organ found" skip with no routing source tag) holds in 0 to 3.4% of the tasks. Second-pass rules R55 to R63 agree on 82% to 99% of all (sample, label) pairs in most pair sets (exceptions: R56 with P41 60.0% of 20 pairs, R61 P11 against P14 13.9% of 36, R62 66.8%). Counting only pairs with at least one side given, both sides give the label in 31% to 94% of the pairs, except R61 (P11 against P14) 0 of 31 and R62 0 of 417 (Table 11).
6. **R21** (ignore polygon against grade polygons): no ignore polygon has more than 0.012 of its area inside grade polygons (P14); 5 of 18 (P7) and 12 of 57 (P14) have any overlap (Table 12). **R64** (repeat labeling): identical choice tags in 43 of 53 pairs (P7) and 47 of 52 (P2), at least 108 of 111 in P20 to P24 (110 of 110 in P24); median polygon area ratio 0.858 and median IoU 0.742 (P2), 0.729 (P7) (Tables 13, 14).
7. **Not independent tests**: R19 and R50 on P4, P9 and P11, whose samples come from a task-order link that was found with skip tags ([interpretation_rules.md](interpretation_rules.md), Section 5).

## Method

**Tables read** (read only, in memory, plain style via `sonoai.paths.dataset_dir`, [DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md); the user's ok was given with TASK-121): `labels/flags_df.pkl` (5,559,898 labelings), `images/taskcrops_df.pkl` (143,152 crop rows), `labels/polygons_df.pkl` (984,908 polygon points; R21 and R64 only). `derived/sample_label_index_v1_df.pkl` is on the list but was not needed: every value below comes from the three tables above with the tag lists of `configs/data/label_projects.yaml` and `configs/data/fact_relations_261023.yaml` (skip kinds, ignored tags, label synonyms). Nothing was written apart from this record. The analysis ran in memory and the code is not in the repo (one-off, as the rules analysis; see Limitations).

**Definitions.**

- **Given**: a labeling with count above 0 in `flags_df`, for one labeling task (`project_id`, `task_id`), tag group and tag. **Visited** (labeling task): at least one given labeling of any tag. For P7 and P14, whose visit unit is the tag group ([DEC-059](../../decisions/DEC-059-fact-driven-model-sample-label-index-presence-policies.md)), the cross-project rules (R55 to R63) count a tag group as worked on when one of its tags, or its mark, is given.
- **Sample**: image hash plus crop box from `taskcrops_df` ([DEC-044](../../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 1). Projects without crop rows (P1, P3, P30, P49, P52, and P4, P9, P11) cannot be placed on samples. For P4, P9 and P11 the task at position i in task-id order takes the sample of the P2 task at position i (5,913 tasks each; the inferred task-order link of interpretation_rules.md Section 1, not re-verified here). P49 and P52 are matched by order: the 10,948 visited P49 tasks in task-id order against the 10,948 P52 tasks in task-id order. P1 and P30 have no link, so only rules inside the task apply to them (R03, R18, R27).
- **Skip tags** are the `quality` and `task_skip` kinds of `fact_relations_261023.yaml` (interpretation_rules.md Table 5, plus P14 `skip_untouched` for R42).
- **Tested, respected** (every row of Tables 3 to 11): the unit is named in the "Test" column. A unit is *tested* when the rule's subject is given (or, for "if and only if" and agreement rules, when at least one of the two sides is given, as stated in the row). It is *respected* when the rule's "expected in the data" statement holds. Share = respected / tested, with a 95% Wilson interval. Where the share would let a reader recover a count of 1 to 4 (a count shown as `<5`, or 1 to 4 tested units not respected), the share is shown as a bound (`>99.9` means above 99.9%; `<8.4` below 8.4%), with no interval, and `withheld` when fewer than 5 units were tested. In those rows the respected cell shows a bound as well.
- The rows are per labeling project where the projects differ. The intervals treat units as independent. They are not: tasks of one sample, samples of one datasource and the five kidney projects P20 to P24 on the same 10,340 samples are correlated. The intervals are therefore too narrow; no clustered interval was computed.

**Overlap measures (R21, R64).** Polygons are drawn on the image in percent coordinates (0 to 100). Each polygon was filled on a 500 by 500 grid (0.2 percent per cell) from its points; the polygons of one tag in one task were merged (union). A ratio of areas or an overlap share does not change when the axes are scaled, so the crop aspect ratio is not needed. No image was opened or rendered.

- R21: **share of the ignore polygon's own area that lies inside the union of the grade polygons (`hepatic_steatosis__0` to `__3`) of the same task**. Chosen because the rule's expected statement is "it does not overlap a grade polygon": 0 is "no overlap", and the share is not diluted by large grade polygons. For reading, the task-level IoU (intersection over union) of the union of ignore polygons against the union of grade polygons is also shown.
- R64: for each pair of visited tasks of one project on one sample, the **area ratio** (smaller over larger area of the tag's merged polygons in the two tasks; the rule says "similar areas") and the **IoU** (adds position). Only tags given in both tasks have both values.
- Reference points (shares at 0.01, 0.05, 0.10, 0.50; 0.5, 0.7, 0.9) are **for reading only**; none is proposed as a threshold.

## 1. Which rules were measured

Table 1. Coverage of the 64 rules. "Measured" = a respected share (or, for R21 and R64, overlap values) from the tables. A rule is listed once.

| Group | Rules | Measured | Notes |
|---|---|---|---|
| Absent answers | R01 to R12 | 12 of 12 | R08, R09: fewer than 5 cases; R11 (spine) and R12 (P52): subject never given |
| Checked marks | R13 to R17 | 5 of 5 | R16 signal-region mark: no case; signs mark: fewer than 5 |
| Skip and cannot decide | R18 to R21 | 4 of 4 | R21: overlap values only (Table 12) |
| Same fact twice | R22 to R26 | 5 of 5 | R26: no case |
| Exclusive options, implied tags | R27 to R37 | 11 of 11 | |
| Visit | R38 to R43 | 2 of 6 (R38, R42) | R39, R40, R41, R43 not testable (Table 2); R38 only for projects with crop rows |
| Routing and one finding per project | R44 to R54 | 10 of 11 | R54 not testable |
| Second pass | R55 to R63 | 9 of 9 | R61: two of seven parts have no pair (Table 11) |
| Repeat labeling | R64 | 1 of 1 | overlap values (Tables 13, 14) |
| **All** | R01 to R64 | **59 of 64** | |

Table 2. Rules that cannot be tested from the tables, with the reason.

| Rule | Reason |
|---|---|
| R39 | Its expected statement is "not testable from the tables (reading only)" in interpretation_rules.md: whether a tag group of P7 or P14 was visited is a reading of the design. |
| R40 | A definition ("a labeling task with no given labeling is not visited"); it has no expected statement. |
| R41 | Part of R38 for P11. P11 has no crop rows, so `taskcrops_df` has no `task_stat` for its tasks and "every submitted task has a given labeling" cannot be tested. |
| R43 | The same for P52. |
| R54 | A definition ("a tag that no visited labeling task on the sample offers is missing"); no expected statement. |

R38 (Table 9) is also not testable for the projects without crop rows (P1, P3, P4, P9, P11, P30, P49, P52); it is measured for 28 projects (those with crop rows, without P7 and P14, R39).

## 2. Rules inside one labeling task

### 2.1 Absent answers and checked marks (R01 to R17)

Table 3. R01 to R12, "absent" answers: the share of labeling tasks with the answer given in which none of the target polygon tags (or disease choice tags, for P49) is given. Tag lists are those of interpretation_rules.md (R10: the 10 disease tags of `fat_regions`; R11: the other tags of the group, without `pregnancy` and `ovarian_follicle` for the uterus). n = labeling tasks.

| Rule | Labeling project | Test (unit; tested = subject given) | n tested | n respected | Respected, % (95% CI) |
|---|---|---|---:|---:|---|
| R01 | P15 | `gallbladder_polyp_absent` given: target polygon tag(s) not given | 2,116 | 2,116 | 100.0 (99.8-100.0) |
| R01 | P26 | `gallbladder_polyp_absent` given: target polygon tag(s) not given | 560 | >555 | >99.1 |
| R01 | P19 | `gallbladder_stone_absent` given: target polygon tag(s) not given | 834 | 834 | 100.0 (99.5-100.0) |
| R01 | P20 | `renal_calculus_absent` given: target polygon tag(s) not given | 8,586 | >8,581 | >99.9 |
| R01 | P21 | `nephritis_absent` given: target polygon tag(s) not given | 8,218 | >8,213 | >99.9 |
| R01 | P22 | `hydronephrosis_absent` given: target polygon tag(s) not given | 9,179 | >9,174 | >99.9 |
| R01 | P23 | `nephrocystosis_absent` given: target polygon tag(s) not given | 10,094 | >10,089 | >99.9 |
| R01 | P24 | `renal_carcinoma_absent` given: target polygon tag(s) not given | 10,295 | >10,290 | >99.9 |
| R01 | P27 | `cholecystitis_absent` given: target polygon tag(s) not given | 819 | 819 | 100.0 (99.5-100.0) |
| R01 | P28 | `gallbladder_tumor_absent` given: target polygon tag(s) not given | 1,436 | >1,431 | >99.6 |
| R01 | P32 | `gallbladder_tumor_absent` given: target polygon tag(s) not given | 788 | 788 | 100.0 (99.5-100.0) |
| R02 | P29 | `breast_disease_no` given: target polygon tag(s) not given | 283 | >278 | >98.2 |
| R03 | P30 | `lung_absent` given: target polygon tag(s) not given | 217 | 217 | 100.0 (98.3-100.0) |
| R04 | P31 | `thyroiditis_abscent` given: target polygon tag(s) not given | 5 | 5 | 100.0 (56.6-100.0) |
| R05 | P37 | `kidney_nodisease` given: target polygon tag(s) not given (5 tags) | 294 | 294 | 100.0 (98.7-100.0) |
| R05 | P39 | `bladder_nodisease` given: target polygon tag(s) not given | 84 | 84 | 100.0 (95.6-100.0) |
| R05 | P42 | `prostate_nodisease` given: target polygon tag(s) not given (5 tags) | 33 | 33 | 100.0 (89.6-100.0) |
| R05 | P43 | `disk_nodisease` given: target polygon tag(s) not given | 7 | 7 | 100.0 (64.6-100.0) |
| R05 | P45 | `thyroid_nodisease` given: target polygon tag(s) not given | 5 | 5 | 100.0 (56.6-100.0) |
| R05 | P50 | `no_hepatic_stone` given: target polygon tag(s) not given | 13,613 | 13,613 | 100.0 (100.0-100.0) |
| R06 | P46 | `uterus_nodisease` given: target polygon tag(s) not given (5 tags) | 89 | 89 | 100.0 (95.9-100.0) |
| R07 | P7 | `notfound` given: target polygon tag(s) not given (7 tags) | 3,494 | 3,489 | 99.9 (99.7-99.9) |
| R08 | P14 | `anatomy_absent` given: target polygon tag(s) not given (17 tags) | <5 | 0 | withheld |
| R09 | P14 | `signs_absent` given: target polygon tag(s) not given (16 tags) | <5 | <5 | withheld |
| R10 | P14 | `heaptic_steatosis_absent` given: target polygon tag(s) not given (10 tags) | 6 | <5 | <8.4 |
| R11 | P49 | `spine_nodisease` given: target polygon tag(s) not given | 0 | 0 | – |
| R11 | P49 | `thyroid_nodisease` given: target polygon tag(s) not given | 9 | 9 | 100.0 (70.1-100.0) |
| R11 | P49 | `uterus_nodisease` given: target polygon tag(s) not given (5 tags) | 32 | 32 | 100.0 (89.3-100.0) |
| R11 | P49 | `prostate_nodisease` given: target polygon tag(s) not given (5 tags) | <5 | <5 | withheld |
| R11 | P49 | `bladder_nodisease` given: target polygon tag(s) not given | 44 | 44 | 100.0 (92.0-100.0) |
| R11 | P49 | `kidney_nodisease` given: target polygon tag(s) not given (5 tags) | 359 | 359 | 100.0 (98.9-100.0) |
| R11 | P49 | `bursa_nodisease` given: target polygon tag(s) not given | 69 | 69 | 100.0 (94.7-100.0) |
| R12 | P47 | `bursa_nodisease` given: target polygon tag(s) not given | 22 | 22 | 100.0 (85.1-100.0) |
| R12 | P52 | `bursa_nodisease` given: target polygon tag(s) not given | 0 | 0 | – |

Table 4. R13 to R17, "checked" marks: the share of labeling tasks with a target polygon given (R13 to R16) that also carry the mark, and, for R17, the share of tasks with `imagequality_checked` that carry no skip tag of the group. P41's group `diseases` includes the organ polygon `lung` (read literally; P41 has 11 labeling tasks). n = labeling tasks.

| Rule | Labeling project | Test (unit; tested = subject given) | n tested | n respected | Respected, % (95% CI) |
|---|---|---|---:|---:|---|
| R13 | P36 | a disease polygon tag given: `checked` also given | 2,244 | >2,239 | >99.7 |
| R13 | P37 | a disease polygon tag given: `checked` also given | 496 | 496 | 100.0 (99.2-100.0) |
| R13 | P38 | a disease polygon tag given: `checked` also given | 638 | >633 | >99.2 |
| R13 | P39 | a disease polygon tag given: `checked` also given | 378 | 378 | 100.0 (99.0-100.0) |
| R13 | P41 | a disease polygon tag given: `checked` also given | 10 | 10 | 100.0 (72.2-100.0) |
| R13 | P42 | a disease polygon tag given: `checked` also given | 71 | 71 | 100.0 (94.9-100.0) |
| R13 | P43 | a disease polygon tag given: `checked` also given | 37 | 37 | 100.0 (90.6-100.0) |
| R13 | P44 | a disease polygon tag given: `checked` also given | 0 | 0 | – |
| R13 | P45 | a disease polygon tag given: `checked` also given | 12 | 12 | 100.0 (75.8-100.0) |
| R13 | P46 | a disease polygon tag given: `checked` also given | 391 | >386 | >98.7 |
| R13 | P47 | a disease polygon tag given: `checked` also given | 133 | 133 | 100.0 (97.2-100.0) |
| R13 | P50 | a disease polygon tag given: `checked` also given | 255 | 255 | 100.0 (98.5-100.0) |
| R14 | P9 | a sign polygon given: `checked` also given | 3,999 | 1,177 | 29.4 (28.0-30.9) |
| R15 | P7 | a `tumor_regions` polygon given: `checked` also given | 1,165 | 1,148 | 98.5 (97.7-99.1) |
| R16 | P14 | a `anatomy_liver` polygon given: `anatomy_checked` also given | 14,553 | 14,503 | 99.7 (99.5-99.7) |
| R16 | P14 | a `liver_signs` polygon given: `signs_checked` also given | <5 | <5 | withheld |
| R16 | P14 | a `fat_regions` polygon given: `hepatic_steatosis_checked` also given | 9,972 | 9,904 | 99.3 (99.1-99.5) |
| R16 | P14 | a `signal_regions` polygon given: `signal_regions_checked` also given | 0 | 0 | – |
| R17 | P14 | `imagequality_checked` given: no skip tag of `image_quality` given | 13,169 | 12,156 | 92.3 (91.8-92.8) |

### 2.2 Skip reasons (R18 to R21, R42)

Table 5. R18 and R42, after a skip nothing else is given. R18: labeling tasks with a skip tag of interpretation_rules.md Table 5 given; respected when no other labeling is given except skip tags and text notes. Two readings of "other labeling" are shown because they give different counts: **strict** (any other tag counts) and **ignored tags allowed** (tags the config lists as ignored, for example `hepatic_steatosis__unknown`, `imagequality_checked`, `has_other_disease`, the P33 AI verdicts, do not count). R42: labeling tasks of P14 with `skip_untouched` given, text notes excluded. P3 was never labeled. n = labeling tasks.

| Rule | Labeling project | Test | n tested | n respected, `skip` tags only (strict) | % (95% CI) | n respected, ignored tags allowed | % (95% CI) |
|---|---|---|---:|---:|---|---:|---|
| R18 | P1 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 674 | 0 | 0.0 (0.0-0.6) | 86 | 12.8 (10.5-15.5) |
| R18 | P2 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 1,652 | 402 | 24.3 (22.3-26.5) | 402 | 24.3 (22.3-26.5) |
| R18 | P3 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 0 | 0 | – | 0 | – |
| R18 | P4 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 7 | <5 | <7.2 | <5 | <7.2 |
| R18 | P7 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 2,471 | 0 | 0.0 (0.0-0.2) | <5 | <0.1 |
| R18 | P9 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 3,415 | 0 | 0.0 (0.0-0.1) | 0 | 0.0 (0.0-0.1) |
| R18 | P11 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 569 | 569 | 100.0 (99.3-100.0) | 569 | 100.0 (99.3-100.0) |
| R18 | P14 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 794 | 0 | 0.0 (0.0-0.5) | 274 | 34.5 (31.3-37.9) |
| R18 | P15 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 105 | 105 | 100.0 (96.5-100.0) | 105 | 100.0 (96.5-100.0) |
| R18 | P20 | skip tag of Table 5 given: no other labeling (not skip, not text) given | <5 | <5 | withheld | <5 | withheld |
| R18 | P21 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 819 | 819 | 100.0 (99.5-100.0) | 819 | 100.0 (99.5-100.0) |
| R18 | P22 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 10 | 10 | 100.0 (72.2-100.0) | 10 | 100.0 (72.2-100.0) |
| R18 | P23 | skip tag of Table 5 given: no other labeling (not skip, not text) given | <5 | <5 | withheld | <5 | withheld |
| R18 | P24 | skip tag of Table 5 given: no other labeling (not skip, not text) given | <5 | <5 | withheld | <5 | withheld |
| R18 | P26 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 7 | 7 | 100.0 (64.6-100.0) | 7 | 100.0 (64.6-100.0) |
| R18 | P27 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 102 | 102 | 100.0 (96.4-100.0) | 102 | 100.0 (96.4-100.0) |
| R18 | P28 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 16 | 16 | 100.0 (80.6-100.0) | 16 | 100.0 (80.6-100.0) |
| R18 | P29 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 28 | 28 | 100.0 (87.9-100.0) | 28 | 100.0 (87.9-100.0) |
| R18 | P30 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 277 | 277 | 100.0 (98.6-100.0) | 277 | 100.0 (98.6-100.0) |
| R18 | P31 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 0 | 0 | – | 0 | – |
| R18 | P32 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 0 | 0 | – | 0 | – |
| R18 | P33 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 300 | 279 | 93.0 (89.5-95.4) | 279 | 93.0 (89.5-95.4) |
| R18 | P35 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 23 | >18 | >78.2 | 23 | 100.0 (85.7-100.0) |
| R18 | P36 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 166 | 166 | 100.0 (97.7-100.0) | 166 | 100.0 (97.7-100.0) |
| R18 | P37 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 87 | 87 | 100.0 (95.8-100.0) | 87 | 100.0 (95.8-100.0) |
| R18 | P38 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 86 | >81 | >94.1 | >81 | >94.1 |
| R18 | P39 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 57 | 57 | 100.0 (93.7-100.0) | 57 | 100.0 (93.7-100.0) |
| R18 | P41 | skip tag of Table 5 given: no other labeling (not skip, not text) given | <5 | <5 | withheld | <5 | withheld |
| R18 | P42 | skip tag of Table 5 given: no other labeling (not skip, not text) given | <5 | <5 | withheld | <5 | withheld |
| R18 | P43 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 12 | 12 | 100.0 (75.8-100.0) | 12 | 100.0 (75.8-100.0) |
| R18 | P44 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 148 | 148 | 100.0 (97.5-100.0) | 148 | 100.0 (97.5-100.0) |
| R18 | P45 | skip tag of Table 5 given: no other labeling (not skip, not text) given | <5 | <5 | withheld | <5 | withheld |
| R18 | P46 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 50 | 50 | 100.0 (92.9-100.0) | 50 | 100.0 (92.9-100.0) |
| R18 | P47 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 25 | 25 | 100.0 (86.7-100.0) | 25 | 100.0 (86.7-100.0) |
| R18 | P49 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 4,691 | 4,480 | 95.5 (94.9-96.1) | 4,480 | 95.5 (94.9-96.1) |
| R18 | P50 | skip tag of Table 5 given: no other labeling (not skip, not text) given | 73 | 0 | 0.0 (0.0-5.0) | 0 | 0.0 (0.0-5.0) |
| R42 | P14 | `skip_untouched` given: no other labeling (not text) given | 223 | 0 | 0.0 (0.0-1.7) | >218 | >97.7 |

Table 6. R19, a skip that describes the image (a `quality` skip tag, starred in interpretation_rules.md Table 5) leaves the sample out of every project. Unit: a labeling task of project B on a sample where another project has a `quality` skip given. Respected when that task carries any skip tag or has no given labeling. The second block of columns restricts to tasks with a given labeling, where "no given labeling" cannot make the task respect the rule. "Crop-row projects" = sources with crop rows; "task-order-linked" = sources P4, P9 or P11, whose sample is inferred (not independent tests; Section 5 of interpretation_rules.md). For P4, P9 and P11 as target, all other projects are sources. n = labeling tasks.

| Rule | Labeling project (B) | Skip source | n tasks of B on flagged samples | n respected | % (95% CI) | of these, tasks with a given labeling | n respected | % (95% CI) |
|---|---|---|---:|---:|---|---:|---:|---|
| R19 | P2 | crop-row projects | 1,630 | 1,372 | 84.2 (82.3-85.9) | 1,630 | 1,372 | 84.2 (82.3-85.9) |
| R19 | P2 | task-order-linked projects (P4, P9, P11) | 3,286 | 1,502 | 45.7 (44.0-47.4) | 3,286 | 1,502 | 45.7 (44.0-47.4) |
| R19 | P4 | all other projects | 3,581 | 7 | 0.2 (0.1-0.4) | 3,581 | 7 | 0.2 (0.1-0.4) |
| R19 | P7 | crop-row projects | 7,616 | 7,442 | 97.7 (97.4-98.0) | 1,905 | 1,731 | 90.9 (89.5-92.1) |
| R19 | P7 | task-order-linked projects (P4, P9, P11) | 13,144 | 11,703 | 89.0 (88.5-89.6) | 3,287 | 1,846 | 56.2 (54.5-57.8) |
| R19 | P9 | all other projects | 2,053 | 1,845 | 89.9 (88.5-91.1) | 2,053 | 1,845 | 89.9 (88.5-91.1) |
| R19 | P11 | all other projects | 3,518 | 3,168 | 90.1 (89.0-91.0) | 857 | 507 | 59.2 (55.8-62.4) |
| R19 | P14 | crop-row projects | 754 | 15 | 2.0 (1.2-3.3) | 754 | 15 | 2.0 (1.2-3.3) |
| R19 | P14 | task-order-linked projects (P4, P9, P11) | <5 | 0 | withheld | <5 | 0 | withheld |
| R19 | P15 | crop-row projects | 548 | 235 | 42.9 (38.8-47.1) | 369 | 56 | 15.2 (11.9-19.2) |
| R19 | P15 | task-order-linked projects (P4, P9, P11) | 472 | 45 | 9.5 (7.2-12.5) | 472 | 45 | 9.5 (7.2-12.5) |
| R19 | P19 | crop-row projects | 282 | 0 | 0.0 (0.0-1.3) | 282 | 0 | 0.0 (0.0-1.3) |
| R19 | P19 | task-order-linked projects (P4, P9, P11) | 472 | <5 | <0.2 | 471 | 0 | 0.0 (0.0-0.8) |
| R19 | P20 | crop-row projects | 1,037 | 0 | 0.0 (0.0-0.4) | 1,037 | 0 | 0.0 (0.0-0.4) |
| R19 | P20 | task-order-linked projects (P4, P9, P11) | 605 | 0 | 0.0 (0.0-0.6) | 605 | 0 | 0.0 (0.0-0.6) |
| R19 | P21 | crop-row projects | 263 | 45 | 17.1 (13.0-22.1) | 262 | 44 | 16.8 (12.8-21.8) |
| R19 | P21 | task-order-linked projects (P4, P9, P11) | 605 | 68 | 11.2 (9.0-14.0) | 604 | 67 | 11.1 (8.8-13.8) |
| R19 | P22 | crop-row projects | 1,034 | 7 | 0.7 (0.3-1.4) | 1,033 | 6 | 0.6 (0.3-1.3) |
| R19 | P22 | task-order-linked projects (P4, P9, P11) | 605 | <5 | <0.1 | 605 | <5 | <0.1 |
| R19 | P23 | crop-row projects | 1,038 | <5 | <0.1 | 1,036 | <5 | <0.1 |
| R19 | P23 | task-order-linked projects (P4, P9, P11) | 605 | <5 | <0.1 | 603 | 0 | 0.0 (0.0-0.6) |
| R19 | P24 | crop-row projects | 1,035 | <5 | <0.1 | 1,035 | <5 | <0.1 |
| R19 | P24 | task-order-linked projects (P4, P9, P11) | 605 | <5 | <0.1 | 603 | 0 | 0.0 (0.0-0.6) |
| R19 | P26 | crop-row projects | 31 | <5 | <1.7 | 31 | <5 | <1.7 |
| R19 | P27 | crop-row projects | 124 | 41 | 33.1 (25.4-41.7) | 124 | 41 | 33.1 (25.4-41.7) |
| R19 | P27 | task-order-linked projects (P4, P9, P11) | 311 | 20 | 6.4 (4.2-9.7) | 311 | 20 | 6.4 (4.2-9.7) |
| R19 | P28 | crop-row projects | 179 | 10 | 5.6 (3.1-10.0) | 179 | 10 | 5.6 (3.1-10.0) |
| R19 | P28 | task-order-linked projects (P4, P9, P11) | 311 | 6 | 1.9 (0.9-4.1) | 311 | 6 | 1.9 (0.9-4.1) |
| R19 | P33 | crop-row projects | 69 | 23 | 33.3 (23.4-45.1) | 69 | 23 | 33.3 (23.4-45.1) |
| R19 | P35 | crop-row projects | 345 | 21 | 6.1 (4.0-9.1) | 345 | 21 | 6.1 (4.0-9.1) |
| R19 | P36 | crop-row projects | 29 | 16 | 55.2 (37.5-71.6) | 29 | 16 | 55.2 (37.5-71.6) |
| R19 | P37 | crop-row projects | 19 | 5 | 26.3 (11.8-48.8) | 19 | 5 | 26.3 (11.8-48.8) |
| R19 | P38 | crop-row projects | 29 | 10 | 34.5 (19.9-52.7) | 29 | 10 | 34.5 (19.9-52.7) |
| R19 | P39 | crop-row projects | 10 | <5 | <5.0 | 10 | <5 | <5.0 |
| R19 | P41 | crop-row projects | <5 | 0 | withheld | <5 | 0 | withheld |
| R19 | P42 | crop-row projects | <5 | 0 | withheld | <5 | 0 | withheld |
| R19 | P44 | crop-row projects | 14 | <5 | <3.6 | 14 | <5 | <3.6 |
| R19 | P46 | crop-row projects | 27 | <5 | <1.9 | 27 | <5 | <1.9 |
| R19 | P47 | crop-row projects | 20 | 11 | 55.0 (34.2-74.2) | 20 | 11 | 55.0 (34.2-74.2) |
| R19 | P50 | crop-row projects | 719 | 7 | 1.0 (0.5-2.0) | 719 | 7 | 1.0 (0.5-2.0) |
| R19 | P50 | task-order-linked projects (P4, P9, P11) | 1,764 | 10 | 0.6 (0.3-1.0) | 1,764 | 10 | 0.6 (0.3-1.0) |

### 2.3 Same fact twice, exclusive options, implied tags (R20, R22 to R37)

Table 7. R20 and R22 to R26. R22: tasks with exactly one grade choice and at least one grade polygon; respected when the choice equals the highest grade drawn. R23 to R25 ("if and only if"): tested = at least one of the two sides given; respected = both given. R26: P14 `liver_ascites` polygon given; respected when both `sign_liver_ascites` and `sign_liquid_near_liver` are given. n = labeling tasks, except R23 (task and tag pairs).

| Rule | Labeling project | Test (unit; tested = subject given) | n tested | n respected | Respected, % (95% CI) |
|---|---|---|---:|---:|---|
| R20 | P7 | `cannotdiag` given: no `tumor_regions` polygon given | 1,239 | 1,239 | 100.0 (99.7-100.0) |
| R22 | P7 | exactly one grade choice and at least one grade polygon: choice equals highest grade drawn | 3,596 | 3,572 | 99.3 (99.0-99.6) |
| R23 | P7 | (task, tag) pairs where the choice or the polygon of one of 5 tags is given: both given | 1,701 | >1,696 | >99.7 |
| R24 | P7 | `checked` or a `tumor_regions` polygon given: both given | 1,177 | 1,148 | 97.5 (96.5-98.3) |
| R25 | P11 | `hepatorenal_contrast_liverbrighter` or `sign_hepatorenal_wall_highecho` given: both given | 195 | 0 | 0.0 (0.0-1.9) |
| R26 | P14 | `liver_ascites` polygon given: both `sign_liver_ascites` and `sign_liquid_near_liver` given | 0 | 0 | – |

R22 detail: 3,601 P7 tasks have a grade choice and a grade polygon, of which 5 have two or more grade choices (left out of the test); 1,163 have a grade choice and no grade polygon, and 18 have a grade polygon and no grade choice (not compared). R25 detail: the choice is given in fewer than 5 tasks and the polygon in 194, never both.

Table 8. R27 to R37. R27, R29 to R32 (exclusive options): tested = at least one tag of the set given; respected = not more than one (R29, R31, R32: not both). R28: P7 tasks with the tumor group worked on and no skip tag; respected when exactly one of `checked`, `notfound`, `cannotdiag` is given. R33 (weak rule): generic `tumor` or `cyst` given; respected when none of the organ-specific tags of the config list is given. R34 to R37 (implied tags): subject given; respected when the implied tag is given. n = labeling tasks, except where the test column names pairs.

| Rule | Labeling project | Test (unit; tested = subject given) | n tested | n respected | Respected, % (95% CI) |
|---|---|---|---:|---:|---|
| R27 | P1 | at least one grade choice given: exactly one | 5,783 | 5,783 | 100.0 (99.9-100.0) |
| R27 | P7 | at least one grade choice given: exactly one | 4,764 | 4,759 | 99.9 (99.8-100.0) |
| R27 | P35 | at least one grade choice given: exactly one | 1,425 | 1,407 | 98.7 (98.0-99.2) |
| R27 | P49 | at least one grade choice given: exactly one | 1,430 | 1,430 | 100.0 (99.7-100.0) |
| R28 | P7 | tumor group worked on, no skip tag: exactly one of `checked`, `notfound`, `cannotdiag` | 3,438 | 3,430 | 99.8 (99.5-99.9) |
| R29 | P9 | either `hepatorenal_contrast_possible` or `_impossible` given: not both | 5,911 | >5,906 | >99.9 |
| R30 | P38 | at least one size state (choice) given: exactly one | 370 | 370 | 100.0 (99.0-100.0) |
| R30 | P49 | at least one size state (choice) given: exactly one | 271 | 271 | 100.0 (98.6-100.0) |
| R30 | P52 | at least one size state (polygon) given: exactly one | 0 | 0 | – |
| R31 | P14 | `anatomy_checked` or `anatomy_absent` given: not both | 14,510 | 14,510 | 100.0 (100.0-100.0) |
| R31 | P14 | `signs_checked` or `signs_absent` given: not both | 9 | 9 | 100.0 (70.1-100.0) |
| R31 | P14 | `hepatic_steatosis_checked` or `heaptic_steatosis_absent` given: not both | 9,913 | 9,913 | 100.0 (100.0-100.0) |
| R32 | P9 | (task, opposite set) pairs with at least one tag given: not both | 3,703 | >3,698 | >99.8 |
| R32 | P14 | (task, opposite set) pairs with at least one tag given: not both | <5 | <5 | withheld |
| R32 | P11 | (task, opposite set) pairs with at least one tag given: not both | 1,099 | 1,099 | 100.0 (99.7-100.0) |
| R33 | P35 | generic `tumor` given: none of the 7 organ-specific tags given | 71 | >66 | >92.9 |
| R33 | P35 | generic `cyst` given: none of the 6 organ-specific tags given | 35 | >30 | >85.7 |
| R33 | P49 | generic `tumor` given: none of the 8 organ-specific tags given | 321 | 293 | 91.3 (87.7-93.9) |
| R33 | P49 | generic `cyst` given: none of the 6 organ-specific tags given | 178 | 170 | 95.5 (91.4-97.7) |
| R33 | P52 | generic `tumor` given: none of the 8 organ-specific tags given | 50 | 50 | 100.0 (92.9-100.0) |
| R33 | P52 | generic `cyst` given: none of the 6 organ-specific tags given | 47 | 47 | 100.0 (92.4-100.0) |
| R34 | P35 | (task, organ) pairs with a tag of the organ's disease group given: organ tag of `check_anatomy` given | 3,548 | 3,520 | 99.2 (98.9-99.5) |
| R34 | P49 | (task, organ) pairs with a tag of the organ's disease group given: organ tag of `check_anatomy` given | 6,431 | 6,399 | 99.5 (99.3-99.6) |
| R35 | P52 | (task, organ) pairs with a tag of the organ's disease group given: organ tag of `check_anatomy` given | 421 | 299 | 71.0 (66.5-75.1) |
| R36 | P9 | `hepatorenal_contrast_liverbrighter` given: `hepatorenal_contrast_possible` given | 964 | >959 | >99.4 |
| R36 | P11 | `hepatorenal_contrast_liverbrighter` given: `hepatorenal_contrast_possible` given | <5 | 0 | withheld |
| R36 | P14 | `hepatorenal_contrast_liverbrighter` given: `hepatorenal_contrast_possible` given | 2,313 | >2,308 | >99.7 |
| R37 | P14 | a `fat_regions` polygon (not stone, gastric) given: `liver` polygon given | 9,926 | >9,921 | >99.9 |
| R37 | P14 | a `liver_signs` polygon given: `liver` polygon given | <5 | <5 | withheld |
| R37 | P14 | `gallbladder_stone` given: `gallbladder` polygon given | 126 | >121 | >96.0 |
| R37 | P14 | `gastric_tumor` given: `stomach` polygon given | 41 | 41 | 100.0 (91.4-100.0) |

R28 detail: of the 3,438 tested P7 tasks, 3,430 carry exactly one mark, 6 none and fewer than 5 two marks. Reading the test as "any given labeling and no skip" (instead of "tumor group worked on") gives 3,443 tested and the same 3,430 respected.

### 2.4 Visit (R38, R42)

Table 9. R38, every labeling task with `task_stat` annotated has at least one given labeling (labeling projects with crop rows, without P7 and P14). R42 is in Table 5. n = labeling tasks.

| Rule | Labeling project | Test (unit; tested = subject given) | n tested | n respected | Respected, % (95% CI) |
|---|---|---|---:|---:|---|
| R38 | P2 | task with `task_stat` annotated: at least one given labeling | 5,913 | 5,913 | 100.0 (99.9-100.0) |
| R38 | P15 | task with `task_stat` annotated: at least one given labeling | 2,302 | >2,297 | >99.7 |
| R38 | P19 | task with `task_stat` annotated: at least one given labeling | 846 | >841 | >99.4 |
| R38 | P20 | task with `task_stat` annotated: at least one given labeling | 10,448 | 10,442 | 99.9 (99.9-100.0) |
| R38 | P21 | task with `task_stat` annotated: at least one given labeling | 10,447 | 10,441 | 99.9 (99.9-100.0) |
| R38 | P22 | task with `task_stat` annotated: at least one given labeling | 10,448 | 10,440 | 99.9 (99.8-100.0) |
| R38 | P23 | task with `task_stat` annotated: at least one given labeling | 10,447 | 10,440 | 99.9 (99.9-100.0) |
| R38 | P24 | task with `task_stat` annotated: at least one given labeling | 10,448 | 10,438 | 99.9 (99.8-99.9) |
| R38 | P26 | task with `task_stat` annotated: at least one given labeling | 712 | >707 | >99.2 |
| R38 | P27 | task with `task_stat` annotated: at least one given labeling | 1,571 | 1,571 | 100.0 (99.8-100.0) |
| R38 | P28 | task with `task_stat` annotated: at least one given labeling | 1,567 | >1,562 | >99.6 |
| R38 | P29 | task with `task_stat` annotated: at least one given labeling | 2,956 | 2,956 | 100.0 (99.9-100.0) |
| R38 | P31 | task with `task_stat` annotated: at least one given labeling | 77 | 77 | 100.0 (95.2-100.0) |
| R38 | P32 | task with `task_stat` annotated: at least one given labeling | 803 | 803 | 100.0 (99.5-100.0) |
| R38 | P33 | task with `task_stat` annotated: at least one given labeling | 4,239 | 4,239 | 100.0 (99.9-100.0) |
| R38 | P35 | task with `task_stat` annotated: at least one given labeling | 4,239 | 4,239 | 100.0 (99.9-100.0) |
| R38 | P36 | task with `task_stat` annotated: at least one given labeling | 2,408 | 2,408 | 100.0 (99.8-100.0) |
| R38 | P37 | task with `task_stat` annotated: at least one given labeling | 880 | >875 | >99.4 |
| R38 | P38 | task with `task_stat` annotated: at least one given labeling | 1,038 | >1,033 | >99.5 |
| R38 | P39 | task with `task_stat` annotated: at least one given labeling | 519 | 519 | 100.0 (99.3-100.0) |
| R38 | P41 | task with `task_stat` annotated: at least one given labeling | 11 | 11 | 100.0 (74.1-100.0) |
| R38 | P42 | task with `task_stat` annotated: at least one given labeling | 106 | 106 | 100.0 (96.5-100.0) |
| R38 | P43 | task with `task_stat` annotated: at least one given labeling | 56 | 56 | 100.0 (93.6-100.0) |
| R38 | P44 | task with `task_stat` annotated: at least one given labeling | 521 | 521 | 100.0 (99.3-100.0) |
| R38 | P45 | task with `task_stat` annotated: at least one given labeling | 19 | 19 | 100.0 (83.2-100.0) |
| R38 | P46 | task with `task_stat` annotated: at least one given labeling | 545 | 545 | 100.0 (99.3-100.0) |
| R38 | P47 | task with `task_stat` annotated: at least one given labeling | 180 | 180 | 100.0 (97.9-100.0) |
| R38 | P50 | task with `task_stat` annotated: at least one given labeling | 13,924 | >13,919 | >99.9 |

## 3. Rules between labeling projects

Table 10. R44 to R53. R44 to R47 (routing): the sample-level share of samples of the later project that have the source tag on the same sample (and, for R44, the reverse). R48: tasks with `skip_no_organ_found` given; respected when the routing source tag (R46 for P50, R47 for the organ projects) is **not** given on the sample, which is the reading of the expected statement that a skip with a source tag is a conflict. R49: P7 samples with the polygon given; respected when the organ polygon is given in P2 on the same sample. R50: tasks with `skip_notliver` given on a sample where P2 has a visited task; respected when P2 has no `liver` polygon there. R51 to R53 (one finding per project): see the test column. n = samples, except R48 and R50 (labeling tasks).

| Rule | Labeling project | Test (unit; tested = subject given) | n tested | n respected | Respected, % (95% CI) |
|---|---|---|---:|---:|---|
| R44 | P20 | sample of the project: `kidney` polygon in P2 or P14 on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R44 | P20 | sample with a `kidney` polygon in P2 or P14: a task of the project on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R44 | P21 | sample of the project: `kidney` polygon in P2 or P14 on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R44 | P21 | sample with a `kidney` polygon in P2 or P14: a task of the project on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R44 | P22 | sample of the project: `kidney` polygon in P2 or P14 on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R44 | P22 | sample with a `kidney` polygon in P2 or P14: a task of the project on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R44 | P23 | sample of the project: `kidney` polygon in P2 or P14 on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R44 | P23 | sample with a `kidney` polygon in P2 or P14: a task of the project on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R44 | P24 | sample of the project: `kidney` polygon in P2 or P14 on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R44 | P24 | sample with a `kidney` polygon in P2 or P14: a task of the project on it | 10,340 | 10,340 | 100.0 (100.0-100.0) |
| R45 | P19 | sample of the project: `gallbladder` polygon in P2 or P14 on it | 845 | 845 | 100.0 (99.5-100.0) |
| R45 | P26 | sample of the project: `gallbladder` polygon in P2 or P14 on it | 712 | 712 | 100.0 (99.5-100.0) |
| R45 | P27 | sample of the project: `gallbladder` polygon in P2 or P14 on it | 1,570 | 1,570 | 100.0 (99.8-100.0) |
| R45 | P28 | sample of the project: `gallbladder` polygon in P2 or P14 on it | 1,570 | 1,570 | 100.0 (99.8-100.0) |
| R45 | P15 | sample of the project: `liver` or `gallbladder` polygon in P2 or P14 on it | 6,857 | >6,852 | >99.9 |
| R46 | P50 | sample of the project: `liver` polygon in P2 or P14 on it | 13,924 | >13,919 | >99.9 |
| R47 | P36 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 2,411 | 2,406 | 99.8 (99.5-99.9) |
| R47 | P37 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 880 | 880 | 100.0 (99.6-100.0) |
| R47 | P38 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 1,039 | >1,034 | >99.5 |
| R47 | P39 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 519 | 519 | 100.0 (99.3-100.0) |
| R47 | P41 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 11 | 11 | 100.0 (74.1-100.0) |
| R47 | P42 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 106 | 106 | 100.0 (96.5-100.0) |
| R47 | P43 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 56 | 56 | 100.0 (93.6-100.0) |
| R47 | P44 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 521 | >516 | >99.0 |
| R47 | P45 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 19 | 19 | 100.0 (83.2-100.0) |
| R47 | P46 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 545 | >540 | >99.0 |
| R47 | P47 | sample of the project: its organ given in P33 (polygon) or P35 (anatomy or disease choice) | 180 | 180 | 100.0 (97.9-100.0) |
| R48 | P36 | `skip_no_organ_found` given: the routing source tag of the sample not given | 149 | 5 | 3.4 (1.4-7.6) |
| R48 | P37 | `skip_no_organ_found` given: the routing source tag of the sample not given | 85 | 0 | 0.0 (0.0-4.3) |
| R48 | P38 | `skip_no_organ_found` given: the routing source tag of the sample not given | 82 | <5 | <0.7 |
| R48 | P39 | `skip_no_organ_found` given: the routing source tag of the sample not given | 56 | 0 | 0.0 (0.0-6.4) |
| R48 | P41 | `skip_no_organ_found` given: the routing source tag of the sample not given | <5 | 0 | withheld |
| R48 | P42 | `skip_no_organ_found` given: the routing source tag of the sample not given | <5 | 0 | withheld |
| R48 | P43 | `skip_no_organ_found` given: the routing source tag of the sample not given | 11 | 0 | 0.0 (0.0-25.9) |
| R48 | P44 | `skip_no_organ_found` given: the routing source tag of the sample not given | 147 | 0 | 0.0 (0.0-2.5) |
| R48 | P45 | `skip_no_organ_found` given: the routing source tag of the sample not given | <5 | 0 | withheld |
| R48 | P46 | `skip_no_organ_found` given: the routing source tag of the sample not given | 50 | 0 | 0.0 (0.0-7.1) |
| R48 | P47 | `skip_no_organ_found` given: the routing source tag of the sample not given | 25 | 0 | 0.0 (0.0-13.3) |
| R48 | P50 | `skip_no_organ_found` given: the routing source tag of the sample not given | 48 | 0 | 0.0 (0.0-7.4) |
| R49 | P7 | a P7 `fat_regions` polygon given: `liver` polygon in P2 on the sample | 3,590 | 3,582 | 99.8 (99.6-99.9) |
| R49 | P7 | a P7 `tumor_regions` polygon (not stone, gastric) given: `liver` in P2 | 1,119 | 1,114 | 99.6 (99.0-99.8) |
| R49 | P7 | P7 `gallbladder_stone` given: `gallbladder` in P2 | <5 | <5 | withheld |
| R49 | P7 | P7 `gastric_tumor` given: `stomach` in P2 | 41 | 41 | 100.0 (91.4-100.0) |
| R50 | P7 | `skip_notliver` given, P2 task visited: no `liver` polygon in P2 on the sample | 287 | >282 | >98.2 |
| R50 | P9 | `skip_notliver` given, P2 task visited: no `liver` polygon in P2 on the sample (task-order link) | 298 | 279 | 93.6 (90.3-95.9) |
| R50 | P11 | `skip_notliver` given, P2 task visited: no `liver` polygon in P2 on the sample (task-order link) | 47 | >42 | >89.3 |
| R51 | P20-24 | sample of any of P20-24: visited in all five projects | 10,340 | 10,304 | 99.7 (99.5-99.7) |
| R51 | P20 | sample of the project: visited in the project | 10,340 | 10,334 | 99.9 (99.9-100.0) |
| R51 | P21 | sample of the project: visited in the project | 10,340 | 10,334 | 99.9 (99.9-100.0) |
| R51 | P22 | sample of the project: visited in the project | 10,340 | 10,332 | 99.9 (99.8-100.0) |
| R51 | P23 | sample of the project: visited in the project | 10,340 | 10,333 | 99.9 (99.9-100.0) |
| R51 | P24 | sample of the project: visited in the project | 10,340 | 10,331 | 99.9 (99.8-100.0) |
| R52 | P27, 28 | sample of P27 or P28: visited in both | 1,570 | 1,565 | 99.7 (99.3-99.9) |
| R53 | P15, 26 | sample visited in P15 or P26: not visited in both | 3,011 | 3,011 | 100.0 (99.9-100.0) |

Table 11. R55 to R63, second pass by another project on the same sample (task order for R59, R61 with P4 or P9, R62, R63). Samples visited and not skipped in both projects only; for P7 and P14 the pair's tag group must be worked on. Two counts per pair set: **all pairs** (respected = both given or both not given; most pairs are "both not given", so this share is high by construction) and **pairs with at least one side given** (respected = both given). The "Labeling project" column shows the two projects. R58 and the nodisease parts of R59, R60 are one-sided tests as stated in the row. R61 has seven parts; the P9 against P14 `liver_signs` and P4 against P14 `signal_regions` parts have no sample where both sides were worked on. n = (sample, tag) pairs, except where stated.

| Rule | Labeling project | Test (unit; tested = subject given) | n tested | n respected | Respected, % (95% CI) |
|---|---|---|---:|---:|---|
| R55 | P35 / 33 | (sample, organ) pairs, P35 choice against P33 polygon (all pairs: both given or both not given) | 62,976 | 60,065 | 95.4 (95.2-95.5) |
| R55 | P35 / 33 | (sample, organ) pairs, P35 choice against P33 polygon (pairs with at least one side given: both given) | 8,919 | 6,008 | 67.4 (66.4-68.3) |
| R56 | P35 / 36 | (sample, disease) pairs, P35 choice against P36 polygon (all pairs: both given or both not given) | 13,464 | 12,211 | 90.7 (90.2-91.2) |
| R56 | P35 / 36 | (sample, disease) pairs, P35 choice against P36 polygon (pairs with at least one side given: both given) | 2,056 | 803 | 39.1 (37.0-41.2) |
| R56 | P35 / 37 | (sample, disease) pairs, P35 choice against P37 polygon (all pairs: both given or both not given) | 3,955 | 3,531 | 89.3 (88.3-90.2) |
| R56 | P35 / 37 | (sample, disease) pairs, P35 choice against P37 polygon (pairs with at least one side given: both given) | 615 | 191 | 31.1 (27.5-34.8) |
| R56 | P35 / 38 | (sample, disease) pairs, P35 choice against P38 polygon (all pairs: both given or both not given) | 3,808 | 3,408 | 89.5 (88.5-90.4) |
| R56 | P35 / 38 | (sample, disease) pairs, P35 choice against P38 polygon (pairs with at least one side given: both given) | 828 | 428 | 51.7 (48.3-55.1) |
| R56 | P35 / 39 | (sample, disease) pairs, P35 choice against P39 polygon (all pairs: both given or both not given) | 924 | 754 | 81.6 (79.0-84.0) |
| R56 | P35 / 39 | (sample, disease) pairs, P35 choice against P39 polygon (pairs with at least one side given: both given) | 396 | 226 | 57.1 (52.2-61.9) |
| R56 | P35 / 41 | (sample, disease) pairs, P35 choice against P41 polygon (all pairs: both given or both not given) | 20 | 12 | 60.0 (38.7-78.1) |
| R56 | P35 / 41 | (sample, disease) pairs, P35 choice against P41 polygon (pairs with at least one side given: both given) | 18 | 10 | 55.6 (33.7-75.4) |
| R56 | P35 / 42 | (sample, disease) pairs, P35 choice against P42 polygon (all pairs: both given or both not given) | 312 | 286 | 91.7 (88.1-94.2) |
| R56 | P35 / 42 | (sample, disease) pairs, P35 choice against P42 polygon (pairs with at least one side given: both given) | 74 | 48 | 64.9 (53.5-74.8) |
| R56 | P35 / 43 | (sample, disease) pairs, P35 choice against P43 polygon (all pairs: both given or both not given) | 44 | 35 | 79.5 (65.5-88.8) |
| R56 | P35 / 43 | (sample, disease) pairs, P35 choice against P43 polygon (pairs with at least one side given: both given) | 30 | 21 | 70.0 (52.1-83.3) |
| R56 | P35 / 44 | (sample, disease) pairs, P35 choice against P44 polygon (all pairs: both given or both not given) | 373 | >368 | >98.6 |
| R56 | P35 / 44 | (sample, disease) pairs, P35 choice against P44 polygon (pairs with at least one side given: both given) | <5 | 0 | withheld |
| R56 | P35 / 45 | (sample, disease) pairs, P35 choice against P45 polygon (all pairs: both given or both not given) | 51 | 43 | 84.3 (72.0-91.8) |
| R56 | P35 / 45 | (sample, disease) pairs, P35 choice against P45 polygon (pairs with at least one side given: both given) | 15 | 7 | 46.7 (24.8-69.9) |
| R56 | P35 / 46 | (sample, disease) pairs, P35 choice against P46 polygon (all pairs: both given or both not given) | 1,980 | 1,814 | 91.6 (90.3-92.8) |
| R56 | P35 / 46 | (sample, disease) pairs, P35 choice against P46 polygon (pairs with at least one side given: both given) | 332 | 166 | 50.0 (44.7-55.3) |
| R56 | P35 / 47 | (sample, disease) pairs, P35 choice against P47 polygon (all pairs: both given or both not given) | 155 | 130 | 83.9 (77.3-88.8) |
| R56 | P35 / 47 | (sample, disease) pairs, P35 choice against P47 polygon (pairs with at least one side given: both given) | 149 | 124 | 83.2 (76.4-88.4) |
| R57 | P35 / 36 | samples with exactly one P35 grade choice and a P36 grade polygon: choice equals highest grade drawn | 995 | 576 | 57.9 (54.8-60.9) |
| R58 | P35 / 37 | `kidney_nodisease` given in P37: no P35 disease choice of the organ group given | 294 | >289 | >98.2 |
| R58 | P35 / 39 | `bladder_nodisease` given in P39: no P35 disease choice of the organ group given | 84 | 76 | 90.5 (82.3-95.1) |
| R58 | P35 / 42 | `prostate_nodisease` given in P42: no P35 disease choice of the organ group given | 33 | 33 | 100.0 (89.6-100.0) |
| R58 | P35 / 43 | `disk_nodisease` given in P43: no P35 disease choice of the organ group given | 7 | 7 | 100.0 (64.6-100.0) |
| R58 | P35 / 45 | `thyroid_nodisease` given in P45: no P35 disease choice of the organ group given | 5 | 5 | 100.0 (56.6-100.0) |
| R58 | P35 / 46 | `uterus_nodisease` given in P46: no P35 disease choice of the organ group given | 89 | >84 | >94.3 |
| R59 | P49 / 52 | (task, tag) pairs over 80 tags in both projects, matched by task order (all pairs: both given or both not given) | 60,960 | 59,666 | 97.9 (97.8-98.0) |
| R59 | P49 / 52 | (pairs with at least one side given: both given) | 2,238 | 944 | 42.2 (40.1-44.2) |
| R59 | P49 / 52 | P49 `<organ>_nodisease` given: no disease polygon of the group in P52 (task order) | 52 | >47 | >90.3 |
| R60 | P19 / 7 | P19 `gallbladder_stone` polygon against P7 `gallbladder_stone` polygon, per sample (all pairs: both given or both not given) | 591 | 582 | 98.5 (97.1-99.2) |
| R60 | P19 / 7 | P19 `gallbladder_stone` polygon against P7 `gallbladder_stone` polygon, per sample (pairs with at least one side given: both given) | 11 | <5 | <4.6 |
| R60 | P19 / 7 | P19 `gallbladder_stone_absent` given: P7 `gallbladder_stone` not given | 581 | >576 | >99.1 |
| R61 | P2 / 14 | (sample, tag) pairs, P2 anatomy polygons against P14 (all pairs: both given or both not given) | 855 | 827 | 96.7 (95.3-97.7) |
| R61 | P2 / 14 | (sample, tag) pairs, P2 anatomy polygons against P14 (pairs with at least one side given: both given) | 226 | 198 | 87.6 (82.7-91.3) |
| R61 | P7 / 14 | (sample, tag) pairs, P7 polygons against P14 `fat_regions` polygons (all pairs: both given or both not given) | 1,140 | 1,095 | 96.1 (94.8-97.0) |
| R61 | P7 / 14 | (sample, tag) pairs, P7 polygons against P14 `fat_regions` polygons (pairs with at least one side given: both given) | 126 | 81 | 64.3 (55.6-72.1) |
| R61 | P7 / 14 | (sample, tag) pairs, P7 choices against P14 `fat_regions` polygons (all pairs: both given or both not given) | 855 | 811 | 94.9 (93.2-96.1) |
| R61 | P7 / 14 | (sample, tag) pairs, P7 choices against P14 `fat_regions` polygons (pairs with at least one side given: both given) | 124 | 80 | 64.5 (55.8-72.4) |
| R61 | P9 / 14 | (sample, tag) pairs, P9 sign polygons against P14 `liver_signs` (task-order link) (all pairs: both given or both not given) | 0 | 0 | – |
| R61 | P9 / 14 | (sample, tag) pairs, P9 sign polygons against P14 `liver_signs` (task-order link) (pairs with at least one side given: both given) | 0 | 0 | – |
| R61 | P4 / 14 | (sample, tag) pairs, P4 areas against P14 `signal_regions` (task-order link) (all pairs: both given or both not given) | 0 | 0 | – |
| R61 | P4 / 14 | (sample, tag) pairs, P4 areas against P14 `signal_regions` (task-order link) (pairs with at least one side given: both given) | 0 | 0 | – |
| R61 | P9 / 14 | (sample, tag) pairs, P9 contrast choices against P14 (task-order link) (all pairs: both given or both not given) | 188 | 178 | 94.7 (90.5-97.1) |
| R61 | P9 / 14 | (sample, tag) pairs, P9 contrast choices against P14 (task-order link) (pairs with at least one side given: both given) | 170 | 160 | 94.1 (89.5-96.8) |
| R61 | P11 / 14 | (sample, tag) pairs, P11 contrast choices against P14 (task-order link) (all pairs: both given or both not given) | 36 | 5 | 13.9 (6.1-28.7) |
| R61 | P11 / 14 | (sample, tag) pairs, P11 contrast choices against P14 (task-order link) (pairs with at least one side given: both given) | 31 | 0 | 0.0 (0.0-11.0) |
| R62 | P9 / 11 | (sample, tag) pairs, P9 against P11 contrast choices (both task-order links) (all pairs: both given or both not given) | 1,256 | 839 | 66.8 (64.1-69.3) |
| R62 | P9 / 11 | (sample, tag) pairs, P9 against P11 contrast choices (both task-order links) (pairs with at least one side given: both given) | 417 | 0 | 0.0 (0.0-0.9) |
| R63 | P2 / 9 | samples, P2 `liver_ascites` against P9 `sign_liver_ascites` or `sign_liquid_near_liver` (task-order link) (all pairs: both given or both not given) | 2,477 | 2,420 | 97.7 (97.0-98.2) |
| R63 | P2 / 9 | samples, P2 `liver_ascites` against P9 `sign_liver_ascites` or `sign_liquid_near_liver` (task-order link) (pairs with at least one side given: both given) | 168 | 111 | 66.1 (58.6-72.8) |

## 4. Overlap values (R21, R64)

Table 12. R21, overlap of the P7 and P14 `hepatic_steatosis__ignore` polygons with the grade polygons of the same labeling task. Measure: share of the ignore polygon's own area inside the union of the grade polygons (fraction, 0 = no overlap; 500 by 500 grid, so a share below about 0.005 is within rasterization at shared borders). Tasks without a grade polygon count as share 0. Shares above 0.01, 0.05, 0.10 and 0.50 are reference points for reading only. No threshold is set.

| Labeling project | Tasks with an ignore polygon | of these, also a grade polygon | Ignore polygons (n) | Share of ignore area inside grade polygons: min / P25 / median / P75 / P90 / max (fraction) | Polygons with share above 0 / 0.01 / 0.05 / 0.10 / 0.50, n | Task-level IoU, union of ignore against union of grade polygons: min / median / max (n tasks) |
|---|---|---|---:|---|---|---|
| P7 | 16 | 16 | 18 | 0.000 / 0.000 / 0.000 / 0.000 / 0.002 / 0.004 | 5 / 0 / 0 / 0 / 0 | 0.000 / 0.000 / 0.003 (16) |
| P14 | 57 | 53 | 57 | 0.000 / 0.000 / 0.000 / 0.000 / 0.001 / 0.012 | 12 / <5 / 0 / 0 / 0 | 0.000 / 0.000 / 0.007 (53) |

Table 13. R64, repeat labeling inside one project: samples with two or more visited labeling tasks in one project, all pairs of those tasks (a sample with three tasks gives three pairs). "Identical choice tags": the sets of given choice tags of the two tasks are equal. "Identical polygon-tag set": the sets of given polygon tags are equal, among pairs where either task has a polygon tag given. A bound has no interval (see Method).

| Labeling project | Samples with 2 or more visited tasks | Task pairs | Pairs with identical choice tags, n | Share, % (95% CI) | Pairs with a polygon tag in either task | Identical polygon-tag set, n | Share, % (95% CI) |
|---|---:|---:|---:|---|---:|---:|---|
| P2 | 52 | 52 | 47 | 90.4 (79.4-95.8) | 41 | 26 | 63.4 (48.1-76.4) |
| P7 | 53 | 53 | 43 | 81.1 (68.6-89.4) | 31 | 24 | 77.4 (60.2-88.6) |
| P20 | 105 | 111 | >106 | >95.4 | <5 | withheld | withheld |
| P21 | 105 | 111 | >106 | >95.4 | 8 | 5 | 62.5 (30.6-86.3) |
| P22 | 105 | 111 | 111 | 100.0 (96.7-100.0) | 0 | 0 | – |
| P23 | 105 | 111 | 111 | 100.0 (96.7-100.0) | <5 | withheld | withheld |
| P24 | 104 | 110 | 110 | 100.0 (96.6-100.0) | 0 | 0 | – |
| P15, P19, P27, P28 pooled | <5 | <5 | withheld | withheld | <5 | withheld | withheld |

Table 14. R64, polygon similarity of repeat labelings: for each (pair of tasks, polygon tag) with the tag given in both tasks, the area ratio (smaller over larger) and the IoU of the merged polygons. Fractions between 0 and 1. The count columns give how many (pair, tag) values reach 0.5, 0.7 and 0.9: reference points for reading only, no threshold is set. P20 to P24 are pooled because they hold the same samples and few polygons.

| Labeling project | (pair, tag) with the tag given in both tasks | Tag given in one task only | Area ratio (smaller / larger): min / P25 / median / P75 / max | IoU: min / P25 / median / P75 / max | Area ratio at least 0.5 / 0.7 / 0.9, n | IoU at least 0.5 / 0.7 / 0.9, n |
|---|---:|---:|---|---|---|---|
| P2 | 86 | 23 | 0.381 / 0.714 / 0.858 / 0.925 / 1.000 | 0.000 / 0.496 / 0.742 / 0.849 / 0.939 | 80 / 67 / 35 | 64 / 49 / 7 |
| P7 | 34 | 10 | 0.151 / 0.716 / 0.858 / 0.940 / 0.990 | 0.121 / 0.571 / 0.729 / 0.802 / 0.941 | 32 / 27 / 14 | 29 / 21 / <5 |
| P20-P24 pooled | 6 | 5 | 0.807 / 0.893 / 0.921 / 0.964 / 0.993 | 0.762 / 0.829 / 0.843 / 0.881 / 0.903 | 6 / 6 / <5 | 6 / 6 / <5 |
| P15, P19, P27, P28 pooled | <5 | 0 | withheld (n<5) | withheld | withheld | withheld |

## Limitations

- **Exploratory, one analyst, no second check of the code.** The analysis was run in memory and the code is not kept in the repo (task rule: no scripts). The values cannot be regenerated without it; if reproducibility is wanted it is a new task (a `sonoai-data` command). Cross-checks against numbers recorded earlier: the 10,340 kidney samples of R44, the 13,923 of 13,924 P50 samples with a liver polygon (R46), the 6,855 of 6,857 P15 samples (R45) and the 0 samples visited in both P15 and P26 (R53) agree with Table 1 of interpretation_rules.md.
- **Counting readings.** Where a rule's statement allows two counts, both are shown (R18 and R42, Table 5; the "all pairs" and "at least one side given" counts of Table 11). For "if and only if" rules (R23 to R25) the tested set is the tasks where either side is given; counting all visited tasks would give higher shares.
- **Samples of P4, P9, P11 are inferred** from task order; the P2 position link was not re-verified. R19 and R50 on these projects are not independent tests.
- **No clustered intervals.** Intervals treat units as independent (see Method).
- **The rules are candidates.** A low share can mean the rule is wrong, or that the labelers worked differently (for example a mark set only sometimes), or that the table cannot show it. This record does not tell which.
- **Tag lists** are taken from the configs; tags named differently but meaning the same are not paired (interpretation_rules.md Section 5).
- Rasterization (R21, R64) is approximate to 0.2 percent of the image side; tiny overlap values are within that.

## Open points

1. **R18 and R42, what counts as "other labeling"?** Question: is a given ignored tag (`hepatic_steatosis__unknown`, `imagequality_checked`) an "other labeling" after a skip? Recommendation: do not count it, the config already treats these tags as ignored (the second column of Table 5). Why: the strict column makes P1 and P14 read 0.0%; with the ignored tags allowed they read 12.8% and 34.5%, because `hepatic_steatosis__unknown` and `imagequality_checked` are often given together with a skip. P7, P9 and P50 stay near 0% either way (other marks and grades are given with the skip). Best alternative: strict reading, if the user wants every given tag to count. Cost to reverse: none (both are in Table 5).
2. **Agreement rules, which denominator?** R23 to R25 and R55 to R63 are shown with the "at least one side given" count next to "all pairs". Recommendation: use the "at least one side given" count when the presence policies are chosen. Why: "all pairs" is dominated by pairs where both sides are empty. Best alternative: "all pairs", if the question is only "do the projects ever contradict each other". Cost to reverse: none.
3. **Should the analysis code be kept?** Recommendation: yes, as a `sonoai-data` command with tests on synthetic tables, in a new `method` task, before the policies are chosen. Why: the values decide the first presence policies and cannot be regenerated otherwise. Best alternative: keep it one-off, as the rules analysis. Cost: a small task.
