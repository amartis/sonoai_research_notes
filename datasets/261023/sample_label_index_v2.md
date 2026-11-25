# Sample-label index v2 of 261023 (261023_plain) and the strict_v1 and loose_v1 presence tables on it

[TASK-264](../../../backlog/tasks/task-264%20-%20Build-the-261023-sample-label-index-v2-labeling-group-skip-and-the-strict_v1-and-loose_v1-presence-tables-on-it-dataset-record-with-counts-per-class-and-state-against-v1-DEC-101.md),
[DEC-101](../../decisions/DEC-101-group-skip-and-sample-label-index-v2.md) (labeling group skip),
[DEC-102](../../decisions/DEC-102-quality-skips-other-organ-projects-index-v2.md) (quality skips of other organs' projects),
[DEC-103](../../decisions/DEC-103-epic3-negatives-and-contested-labels.md) (negatives in four parts, contested labels),
[DEC-100](../../decisions/DEC-100-epic3-mission-spot-liver-diseases.md). Layout follows [sample_label_index.md](sample_label_index.md) (index v1)
and [sample_label_presence.md](sample_label_presence.md) (presence tables on v1). Descriptive counts; aggregates only: no images,
file names, folder names or identifiers; counts of 1 to 4 are shown as `<5`.

Reporting checklists (CLAIM, STARD): not applicable. This is a count of labels: no model is trained or evaluated, no split is
made, no threshold is chosen. No CIs: every number is a count of the full table, not an estimate from a sample.

## Summary

1. **Index v2 and two presence tables were written** as new files in `derived/` of `261023_plain`; the v1 files are unchanged
   (Table 1, sha256 before and after). Index v2 has the same 1,227,979 rows and 29,233 samples as v1; only the facts on the rows
   differ (Table 2).
2. **Every strict_v1 count equals the simulated count of DEC-102 Table 1** (Table 4): hepatoma 1,417 positive and 14,306 negative,
   hemangioma 204 and 15,700, hepatic cyst 116 and 15,830, hepatic stone 296 + `<5` and 15,776, ascites 136 and 16,491; all four spot
   classes negative 13,656. No difference to explain. The four parts of the negatives (418, 8,299, 4,512, 427) and the cirrhosis
   share of hepatoma positives (828 of 1,298 where known) equal DEC-103 and DEC-102 too (Tables 5 and 6).
3. **Every changed pair is explained by the two decisions; this was checked.** 50,055 pairs on 1,616 samples change between index
   v1 and v2. Each is on a sample that is no longer set aside by a quality skip (43,632 pairs; "such samples" below), on a sample with a
   labeling-group skip of P7 (a "group skip" below) that is not such a sample (4,243), or on both (2,180). Pairs on neither kind of
   sample: 0 (Table 10). The 1,002 such samples lie in 41 datasource groups.
4. **Contested pairs are unchanged**: hepatoma 252, hemangioma 65, hepatic cyst 25, hepatic stone 0, the same 304 samples as in
   DEC-103, in `<5` datasource groups, under both policies; ascites has 56 more, of another kind (Table 8).

## Method

**Tables read** (plain style via `sonoai.paths.dataset_dir`, [DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md),
[DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md); list approved with the task on 2026-11-25):
`images/taskcrops_df.pkl`, `labels/flags_df.pkl` (inputs of the index), `derived/sample_label_index_v1_df.pkl` and
`derived/sample_label_presence_strictv1_df.pkl` (comparison). **Written**, new files only
([DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md); no `--overwrite`): index v2 and the strict_v1 and loose_v1
presence tables on it, each as `.pkl` and `.xlsx`. No other table was read; loose_v1 on index v1 was recomputed in memory
from index v1 with the registered policy and not written. The `.xlsx` copies were not opened.
The analysis below ran in memory, in scripts kept outside the repo and outside the dataset, and wrote no file.

Commands (code at commit b217ef3 of the repo; config `configs/data/fact_relations_261023_v2.yaml`, sha256 prefix `c4076c4e711ac39b`,
passed to all three):

```bash
sonoai-data sample-label-index 261023_plain --relations configs/data/fact_relations_261023_v2.yaml --version v2
sonoai-data sample-label-presence 261023_plain --index v2 --policy strict_v1 --relations configs/data/fact_relations_261023_v2.yaml
sonoai-data sample-label-presence 261023_plain --index v2 --policy loose_v1 --relations configs/data/fact_relations_261023_v2.yaml
```

Table 1. Files written and v1 files checked. sha256 of the two v1 tables on the approved list, taken before the build and after
the last command: equal. The other v1 files (index `.xlsx`, loose_v1, posrich_v1, strict_v1 `.xlsx`) are not on the list and were
not read: their size and modification time (`stat`) are the same before and after.

| File in `derived/` | Rows / sheets | sha256 of the `.pkl` |
|---|---|---|
| index v2 (`.pkl` and `.xlsx`) | 1,227,979 rows; 2 row sheets | `6581730acd1a2a4f765482fd1d5f665f2a31f0a25f8bb838b003b6d42ede964a` |
| strict_v1 on index v2 (`.pkl` and `.xlsx`) | 524,052 rows; 1 row sheet | `4260af13e6f3765d203924d32fd81982a5d931b504c1955989d8ffd787fd3d2f` |
| loose_v1 on index v2 (`.pkl` and `.xlsx`) | 795,101 rows; 1 row sheet | `31ab7ab74c615b41340db1975f8be850828c9b93e8a480c0f84365e182f86f5f` |
| index v1 (unchanged) | | `b08b9e011689073872de4ee6e16b18d61802761a18a99c85dd72764bb79acf49` before and after |
| strict_v1 on index v1 (unchanged) | | `05b3f4230c46e2319683d1caf7410c148a925e3b453afb0b9183d89adc91fa77` before and after |

**Checks.** (1) `n_group_skip` (the count of labeling-group skip items) is not 0: 730 labeling-group skip fact items (2,920 copies on index rows, all of P7), so the v2 config was
used. (2) No quality item of index v2 comes from one of the 23 projects of DEC-102 rule 1: quality items come from 7 projects, all
of the list in rule 2 (P2, P7, P14, P33, P35, P36, P50; the others of the list have no quality item in index v2). (3) The presence tables rebuilt in
memory from the index with the registered policies equal the stored ones on sample, label, state and reason: strict_v1 on v1,
strict_v1 on v2 and loose_v1 on v2. (4) The sample numbers of index v2 equal those of
`sample_sets.build_samples`, which gives the datasource groups used below (67 groups, as in v1).

**Masking check.** A script over the tables of this record compared every pair of cells in a row and in a column, every cell with
the sum of 2 to 4 other cells of its row or column, and every pair of numbers of 100 or more anywhere in the record. After the
merges and omissions noted in Tables 3, 6, 7 and 9 and the omission of a table of gross gains, every pair 1 to 4 apart that is left
inside a table is between unrelated numbers (different classes, labels or kinds), not a version, a policy, or a total and its parts.
Differences of label totals over all labels can still be worked out from the file row counts of Table 1 and from the v1 record
(for example the positive_grade_mismatch count); these are totals over all labels, not small cells of a class, and nothing more is
masked for them. The check ran on this record only.

**First index run.** The first run of the index command was started in the foreground with its output piped to `tail -40`; the
shell tool moved it to the background after 180 s. It printed nothing and wrote no file: `derived/` held no index v2 afterwards, and
the second run was not refused. The cause is unknown (probably the process or its pipe was closed when the tool moved it; not
verified). The second run, with its output going to the tool's own log, finished with exit code 0 and wrote the files of Table 1. After
the work, `derived/` held these 6 new files and no partial or temporary file (names and `stat` listed, nothing else opened).

Terms as in [sample_label_index.md](sample_label_index.md) and [sample_label_presence.md](sample_label_presence.md): sample-label pair,
presence state, strict_v1, loose_v1. **Datasource group**: [DEC-044](../../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 2 (shown as counts and shares only, no ids). **Spot classes**:
`hepatoma`, `hemangioma`, `hepatic_cyst`, `hepatic_stone` ("all four spot classes negative" means a known negative on each of the four);
`ascites` is listed beside them. Pairs are counted over the pairs of the table in the state named; **groups** is the number of
datasource groups with at least one such pair; **top share** is the largest group's share of those pairs.

## 1. What index v2 changes in the index

Table 2. Fact items, index v1 against v2 (items counted once, as in Table 2 of the v1 record). Visited, closure and value items do
not change.

| Fact kind | v1 | v2 | Change |
|---|---|---|---|
| quality | 6,317 | 5,209 | -1,108 (quality skips of the 23 projects, now task skips) |
| task_skip | 2,321 | 2,699 | +1,108 and -730 (the 730 P7 `skip_otherdisease` items, now group skips) |
| group_skip | 0 | 730 | +730 (P7 `skip_otherdisease`, tag group `fat_regions` and the four steatosis grade tags) |
| visited, closure, value | 192,323, 116,496, 1,425,467 | the same | 0 |

Samples with a quality item: 3,518 in v1, 2,516 in v2; 1,002 no longer set aside by a quality skip (in 41 datasource groups), none new. The sum of the changes
in Table 2 checks: 2,321 + 1,108 - 730 = 2,699.

## 2. Counts per spot class and state, v1 against v2

Table 3. strict_v1, sample-label pairs per class and state, index v1 and index v2 (n = pairs; groups = datasource groups with a
pair; top share = largest group's share). 67 groups in the index. hepatic_stone positives in v2: 296 + `<5`. Groups with negatives in v1 are written "v2 - <5": fewer by less than 5 than in v2
(Section 7, trace a).

| Class | State | v1 n | v1 groups | v1 top share | v2 n | v2 groups | v2 top share |
|---|---|---|---|---|---|---|---|
| `hepatoma` | positive | 932 | 18 | 15% | 1,417 | 18 | 35% |
| `hepatoma` | negative | 13,477 | v2 - <5 | 20% | 14,306 | 55 | 21% |
| `hemangioma` | positive | 166 | 13 | 43% | 204 | 13 | 35% |
| `hemangioma` | negative | 14,425 | v2 - <5 | 19% | 15,700 | 55 | 19% |
| `hepatic_cyst` | positive | 92 | 12 | 29% | 116 | 12 | 30% |
| `hepatic_cyst` | negative | 14,540 | v2 - <5 | 18% | 15,830 | 55 | 19% |
| `hepatic_stone` | positive | 296 | 38 | 16% | 296 + <5 | 38 | 16% |
| `hepatic_stone` | negative | 15,068 | v2 - <5 | 18% | 15,776 | 55 | 19% |
| `ascites` | positive | 103 | 10 | 40% | 136 | 10 | 40% |
| `ascites` | negative | 15,767 | v2 - <5 | 17% | 16,491 | 48 | 18% |

Table 4. strict_v1 on index v2 against the simulated counts of DEC-102 Table 1, and against DEC-101 Table 1 (group skip only,
simulated) for the part that did not change. Counts are positive / negative; "match" means equal. The middle column is the
simulation with the group skip and today's quality skips (DEC-102 Table 1, middle column; DEC-101 Table 1 for the positives).

| Class | v1 (this record) | v2 with the group skip only (DEC-101/102, simulated) | v2 expected, DEC-102 (simulated) | v2 built | Match |
|---|---|---|---|---|---|
| `hepatoma` | 932 / 13,477 | 1,367 / 13,654 | 1,417 / 14,306 | 1,417 / 14,306 | yes |
| `hemangioma` | 166 / 14,425 | 198 / 15,005 | 204 / 15,700 | 204 / 15,700 | yes |
| `hepatic_cyst` | 92 / 14,540 | 108 / 15,137 | 116 / 15,830 | 116 / 15,830 | yes |
| `hepatic_stone` | 296 / 15,068 | 296 / 15,068 | 296 + <5 / 15,776 | 296 + <5 / 15,776 | yes |
| `ascites` | 103 / 15,767 | 103 / 15,767 | 136 / 16,491 | 136 / 16,491 | yes |
| all four spot classes negative | 12,879 | 13,020 | 13,656 | 13,656 | yes |

Reading of Table 4. The group skip alone (v1 to the middle column) moves only the tumour labels, as DEC-101 says: hepatoma,
hemangioma and cyst gain positives; `hepatic_stone` and `ascites` do not change. The quality-skip change (middle to last column) adds
to every class; ascites gains the most in share (103 to 136, 32%). The 1,002 samples are no longer set aside by a quality skip for any of their labels. The v1 column's all-four
negative figure (12,879) is computed here from index v1 in memory; the simulated 13,020 of [DIS-058](../../discussions/DIS-058-epic3-negatives-contested-labels-quality-skips.md) is the middle column. The
datasource groups: no class gains a positive group (18, 13, 12, 38 and 10 groups before and after). The negatives gain <5 groups in each class (Table 3);
for hepatoma and for ascites it is the same group, which holds <5 samples, every one of them no longer set aside by a quality skip of P27 (trace
in Section 7; the other classes' new group was not compared).

The hepatoma positives' largest datasource group rises from 15% to 35% of them with the group skip (DEC-101: 34% before the
quality change).

## 3. The four parts of the negatives by diffuse disease (DEC-103 rule 2)

The first part that matches, by the strict_v1 states on index v2: **cirrhosis** (`hepatic_cirrhosis` positive); **other diffuse
disease** (a `hepatic_steatosis__1` to `__3` positive or positive_grade_mismatch, or `hepatitis` or `hepatic_precirrhosis`
positive); **none** (`hepatic_steatosis__0` positive, `hepatic_cirrhosis` and `hepatitis` negative); **not known** (the rest).

Table 5. Negatives in four parts, strict_v1 on index v2: samples (datasource groups). Overall = all four spot classes negative;
then each class's negatives. The overall row and the hepatoma row equal DEC-103 Consequences (418 / 8,299 / 4,512 / 427 and
470 / 8,699 / 4,604 / 533).

| Negative for | Samples | Cirrhosis | Other diffuse disease | None | Not known |
|---|---|---|---|---|---|
| all four spot classes (overall) | 13,656 (55) | 418 (26) | 8,299 (48) | 4,512 (51) | 427 (16) |
| `hepatoma` | 14,306 (55) | 470 (26) | 8,699 (48) | 4,604 (51) | 533 (24) |
| `hemangioma` | 15,700 (55) | 1,293 (26) | 9,045 (48) | 4,601 (51) | 761 (25) |
| `hepatic_cyst` | 15,830 (55) | 1,321 (26) | 9,110 (48) | 4,603 (51) | 796 (25) |
| `hepatic_stone` | 15,776 (55) | 1,326 (26) | 9,046 (48) | 4,518 (51) | 886 (26) |
| `ascites` (beside the four) | 16,491 (48) | 609 (17) | 6,216 (38) | 4,374 (42) | 5,292 (34) |

Same parts, index v1, overall row (all four negative, 12,879 samples): cirrhosis 241, other diffuse 7,897, none 4,319, not known 422.
The cirrhosis negatives rise from 241 to 418. Trace (Section 7): 177 samples enter and none leave; 135 are samples with a P7 group
skip whose v1 answers on cirrhosis and on three of the four spot classes were all "no answer" (the task skip covered every
label), and 42 are such samples (no longer set aside by a quality skip) whose five answers were all "quality skip" in v1. The 241 + 135 = 376 equals the figure
of DIS-058 for the group skip only.

Hepatoma positives in the same parts (1,417 samples in 18 groups; for contrast with the negatives): cirrhosis 828 (15 groups),
other diffuse disease 436 (18), none or not known 153 (10 or more groups).

Reading. Cirrhosis is 58% of the hepatoma positives (828 of 1,417) and 3.1% of the all-four-negative samples (418 of 13,656), as
DEC-103 says (2.9% before the quality change). The own bar for cirrhosis (DEC-103 rule 3) rests on 418 samples in 26 groups,
470 against hepatoma. Which of them fall in a test group is a question of the split ([TASK-270](../../../backlog/tasks/task-270%20-%20Decide-epic-3-point-7-one-datasource-group-split-for-every-policy-with-enough-cirrhosis-negatives-in-test-DIS-056.md), one datasource-group split for every policy; not part of this task).

## 4. Cirrhosis state of the positives and hepatoma by cirrhosis state

Table 6. strict_v1, cirrhosis state of the positives of each class: samples with `hepatic_cirrhosis` positive / negative /
not known (neither state in the presence table). Rows left out to avoid showing a small count or a small difference between versions or policies: index v1 of `hemangioma`, `hepatic_cyst` and
`hepatic_stone`, and index v2 of `hepatic_stone`.

| Class | Index | Positives | Cirrhosis positive | Cirrhosis negative | Not known | Groups with a cirrhosis-positive sample |
|---|---|---|---|---|---|---|
| `hepatoma` | v1 | 932 | 360 | 453 | 119 | 9 |
| `hepatoma` | v2 | 1,417 | 828 | 470 | 119 | 15 |
| `hemangioma` | v2 | 204 | 48 | 146 | 10 | 6 |
| `hepatic_cyst` | v2 | 116 | 19 | 90 | 7 | <5 |
| `ascites` | v1 | 103 | 7 | 6 | 90 | <5 |
| `ascites` | v2 | 136 | 116 | 6 | 14 | 8 |

Hepatoma by cirrhosis state, where known: 360 of 813 (44%) in v1, 828 of 1,298 (64%) in v2. DEC-101 gives 360 of 813 (v1) and
788 of 1,248 (group skip only), DEC-102 gives 828 of 1,298: equal. The group skip adds 428 cirrhosis-positive and 7
cirrhosis-negative hepatoma positives; the quality change adds 40 and 10 (50 positives in all, as in Table 4). The 119 hepatoma
positives with no known cirrhosis state do not change. Ascites positives are almost all with cirrhosis in v2 (116 of 122 where known).

## 5. loose_v1 on index v2, five classes

Table 7. loose_v1, pairs per class and state, index v1 (recomputed in memory) and v2 (written table); groups and top share as in Table 3.
"X + <5" means the strict_v1 count of Table 3 plus fewer than 5 pairs (a difference of under 5 between the two policies is not shown). DEC-101 Table 1 (loose column, group skip only, simulated) gives hepatoma 932 to 1,367 positive and 15,205 to 15,383
negative and ascites 103; the v1 column below equals it. The v2 column adds the quality change (+50 hepatoma, +33 ascites, the same increments as
strict_v1).

| Class | State | v1 n (groups) | v2 n (groups, top share) |
|---|---|---|---|
| `hepatoma` | positive | 932 (18) | 1,417 (18, 35%) |
| `hepatoma` | negative | 15,205 (v2 - <5) | 16,047 (55, 19%) |
| `hemangioma` | positive | 166 + <5 (13) | 204 + <5 (13, 35%) |
| `hemangioma` | negative | 16,156 (v2 - <5) | 17,445 (55, 17%) |
| `hepatic_cyst` | positive | 92 + <5 (12) | 116 + <5 (12, 30%) |
| `hepatic_cyst` | negative | 16,271 (v2 - <5) | 17,574 (55, 17%) |
| `hepatic_stone` | positive | 296 (38) | 296 + <5 (38, 16%; loose_v1 equals strict_v1 here) |
| `hepatic_stone` | negative | 15,068 + <5 (v2 - <5) | 15,776 + <5 (55, 19%) |
| `ascites` | positive | 103 (10) | 136 (10, 40%) |
| `ascites` | negative | 21,246 (v2 - <5) | 22,186 (58, 14%) |

The loose_v1 negatives add the `open` pairs (no closure checked) to the strict_v1 negatives. Positives differ by 31 pairs in
total between the policies over all labels, in v1 and in v2 (Table 9); in the five classes the difference is under 5 for
hemangioma and hepatic cyst positives and for hepatic stone negatives (the `conformance` pairs of strict_v1).

## 6. Contested pairs (conflict) per class

Table 8. strict_v1 and loose_v1 on index v2: contested pairs (unknown, reason `conflict`) per class, with the labeling projects
that disagree (read from the facts of these rows). The pairs are the same on index v1 and under both policies.

| Class | Contested pairs (= samples) | Projects that disagree |
|---|---|---|
| `hepatoma` | 252 | P35 and P36 (P36 gives it, P35 does not: 228; P35 gives it, P36 does not: 24) |
| `hemangioma` | 65 | P35 and P36 (P36 gives it: 26; P35 gives it: 39) |
| `hepatic_cyst` | 25 | P35 and P36 (P36 gives it: 18; P35 gives it: 7) |
| `hepatic_stone` | 0 | none |
| `ascites` | 56 | P33 against P35, P36 or both: P33 is on one side of every one of the 56 |

DEC-103 rule 4 describes the first four rows: its 304 samples are those with a conflict in one of the four spot classes
(342 pairs on 304 samples, in `<5` datasource groups). The 56 ascites pairs are not part of those 342 and not of the 304: they are a
different kind of conflict, P33 against the other two projects, on 56 samples in `<5` groups; 8 of these 56 samples are also among
the 304, so the union is 352 samples. DEC-103 rule 4 does not cover ascites; the record leaves them unknown as the policies do.

Over all labels the `conflict` pairs are 5,877 in v1 and 5,901 in v2, on 2,735 and 2,749 samples in 9 datasource groups; the 24
more pairs are all on labels outside the five classes.

## 7. What changed outside the liver labels, and why

Table 9. Pairs per state and reason over all 100 content labels (n = 1,227,979 pairs, the same index rows in both), index v1
against v2, strict_v1 and loose_v1. The v1 columns equal Table 2 of the presence record. Two rows are merged (positive_grade_mismatch
with unknown grade_ignored) and the presence-table row total is left out. Differences of label totals over all labels can still be
worked out from the file row counts of Table 1 and from the v1 record (for example the positive_grade_mismatch count); they are
totals over all labels, not small cells of one class. The sum of the rows is 1,227,979 in each column.

| State, reason | strict_v1 v1 | strict_v1 v2 | loose_v1 v1 | loose_v1 v2 |
|---|---|---|---|---|
| positive, given | 87,615 | 93,692 | 87,646 | 93,723 |
| negative, closed | 406,016 | 429,548 | 406,016 | 429,548 |
| negative, open | 0 | 0 | 268,400 | 271,018 |
| positive_grade_mismatch and unknown, grade_ignored (together) | 1,030 | 1,036 | 1,030 | 1,036 |
| unknown, conflict | 5,877 | 5,901 | 5,877 | 5,901 |
| unknown, conformance | 31 | 31 | 0 | 0 |
| unknown, no_answer | 329,348 | 342,903 | 329,348 | 342,903 |
| unknown, no_closure | 268,400 | 271,018 | 0 | 0 |
| unknown, sample_quality_skip | 129,662 | 83,850 | 129,662 | 83,850 |

Samples with at least one pair in the presence table: 25,127 (strict_v1 on v1) to 26,099 (v2), and 25,216 (loose_v1 on v1) to
26,190 (v2) of 29,233.

**Cause of every changed pair.** A pair is changed when its state or reason differs between index v1 and v2 (the same pairs under
both policies). Each changed pair was put in one class by its sample: **no longer set aside** (the sample had a quality item in v1 and has none
in v2; "such samples") and/or **group skip** (the sample has a P7 task with a group-skip item in v2; every one of these samples had a P7 task skip
in v1, so the task lost its task skip).

Table 10. Changed pairs (n = 50,055, on 1,616 samples, 97 of 100 labels) by cause of their sample.

| Cause | Pairs | Samples |
|---|---|---|
| such sample (no longer set aside by a quality skip), no group skip | 43,632 | 920 |
| group skip, not such a sample | 4,243 | 614 |
| both | 2,180 | 82 |
| neither | 0 | 0 |

About 6,500 changed pairs are on the five classes above and about 43,600 on other labels. These "about" figures are rounded; the
ranges are per-label ranges: the cirrhosis, hepatitis, gastric and gallbladder-stone labels 1,540 to 1,590 pairs each (rounded); the steatosis
grades and organ labels such as liver, kidney, spleen, stomach, intestine, gallbladder, portal vein and hepatic duct 974 each;
the kidney-project labels 826 to 827 each (exact per-label counts). The net change per state is in Table 9; a
table of gains by new state is not given, because gross gains next to the net changes would show small counts. The 45,812 pairs
that leave the quality-skip state are exactly the pairs on such samples (43,632 + 2,180): every pair on such a sample was in
that state in v1, and no pair on a group-skip sample alone was.

**Traces of the three open points** (aggregates from the facts of the rows):

a. *The extra datasource group with negatives.* A group of <5 samples gains negatives in v2, the same group for hepatoma and for
   ascites. Every one of its samples is no longer set aside by a quality skip, and the skip in v1 was P27's (a project
   on another organ). Not a group-skip effect.
b. *Cirrhosis negatives, 241 to 418.* 177 samples enter, 0 leave. 135 are samples with a P7 group skip that are not such samples: in v1
   their P7 task skip set aside every label, so cirrhosis and three of the four spot classes (all but `hepatic_stone`) were "no
   answer"; in v2 the tumour labels and the cirrhosis label are read, as negative or positive. 42 are such samples whose cirrhosis
   and four spot labels were all "quality skip" in v1. 0 enter through neither cause. The 135 are in 9 datasource groups and the 42 in 9.
c. *Negative closed to conflict.* The hypothesis holds. The pairs (under 5; counted in the net change of "negative, closed" in
   Table 9) are on the `hepatic_cirrhosis` label of P7 samples that have a group skip and are not such samples. In v1 a P7 task of each
   had `skip_otherdisease` as a task skip, so its answer ("cirrhosis given") counted as none, and another task closed the label:
   negative. In v2 that skip is a group skip of the steatosis tags only, so the first task's answer counts, and the tasks disagree:
   unknown, `conflict`. This is a P7 effect, not a quality effect.

## Differences from the simulated numbers

None in the strict_v1 counts. Every strict_v1 count of DEC-102 Table 1 (6 rows, 11 numbers and the `<5`), the four parts of DEC-103,
the 828 of 1,298 and the 1,002 samples in 41 groups were reproduced exactly. That the build changes only what the two decisions say
was shown by Table 10, not assumed: every changed pair is on such a sample or a group-skip sample, and none is on neither.
All 1,002 such samples carry changed pairs (920 + 82).

## Limitations

- Counts, not estimates: no model is evaluated here. The numbers describe the labels as the policies read them.
- The datasource groups are those of DEC-044 rule 2; a group is a source of images, not a patient (the data has no patient key).
- The contested pairs and the other `conflict` pairs stay unknown (DEC-103 rule 4); posrich_v1 on index v2 is not built (low
  priority, not in this task).
- The cause of the failed first index run is unknown (Method).
- The partition of Table 10 is by sample, so a pair on a sample with both causes (the third row) is not split between them.

## Open points

- [docs/datasets/styles/derived.md](../../../docs/datasets/styles/derived.md) and [docs/fact-driven-model.md](../../../docs/fact-driven-model.md)
  still say index v2 is not built; they are outside this task's files and need a one-line update (a `data` or `infra` task).
