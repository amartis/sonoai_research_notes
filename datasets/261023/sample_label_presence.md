# Sample-label presence tables of dataset version 261023: strict_v1, loose_v1, posrich_v1

[TASK-124](../../../backlog/tasks/task-124%20-%20Build-the-261023-sample-label-presence-tables-of-the-chosen-policies-dataset-record-comparing-counts-per-label-and-state-across-policies-DEC-059.md), [DEC-059](../../decisions/DEC-059-fact-driven-model-sample-label-index-presence-policies.md), [DEC-060](../../decisions/DEC-060-first-presence-policies-of-261023.md), [DEC-061](../../decisions/DEC-061-a9-value-absent-target-side-and-task-123-readings.md). Model and policy text: [fact-driven-model.md](../../../docs/fact-driven-model.md) section 5. Index it reads: [sample_label_index.md](sample_label_index.md). Table format: [derived.md](../../../docs/datasets/styles/derived.md). Names follow the [glossary](../../../docs/glossary.md).

**Status: descriptive counts, first build.** This record counts sample-label pairs per content label and presence state under the three policies chosen in DEC-060. It chooses no policy for training and sets no threshold. Aggregates only: no images, file names, folder names or identifiers; counts of 1 to 4 are shown as `<5`. Built on 2026-11-17 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)). Not reviewed.

Key: sample-label pair = one sample and one content label; n = number of sample-label pairs unless a row says samples; pair in the presence table = a pair in a kept state (positive, positive_grade_mismatch or negative; [derived.md](../../../docs/datasets/styles/derived.md#derivedsample_label_presence_policytag_dfpkl-sample-label-presence-table-dec-059-dec-060)); with polygon = a labeling task that gives the label gives it in a polygon tag group, so a pixel target exists (column [`has_polygon`](../../../docs/datasets/styles/derived.md#derivedsample_label_presence_policytag_dfpkl-sample-label-presence-table-dec-059-dec-060) of the presence table); choice only = the labeling tasks give it only as a choice tag (`has_polygon` false). `given_contested` (posrich_v1 only) = given by one task while another task answers `closed` or `open`.

Reporting checklists (CLAIM, STARD): not applicable. These are counts of how labels are read into presence states; no model is trained or evaluated and no split is made. No confidence intervals: the numbers are complete counts of the dataset version, not estimates from a sample.

## Summary

1. **Three presence tables were written**, one per policy, each as `.pkl` and `.xlsx` in `derived/` of `261023_plain` (Table 1). The sample-label index v1 has 1,227,979 pairs on 29,233 samples; the presence tables keep only positive, positive_grade_mismatch and negative pairs. Unknown pairs are left out and counted here (Table 2); the unknown reasons (`conflict`, `no_closure` and the others) are defined in the [presence table section of derived.md](../../../docs/datasets/styles/derived.md#derivedsample_label_presence_policytag_dfpkl-sample-label-presence-table-dec-059-dec-060).
2. **Positives barely differ in strict_v1 and loose_v1** (87,615 and 87,646, a difference of 31) and are 5,877 more in posrich_v1 (93,523: 5,877 `given_contested` pairs, the pairs strict_v1 and loose_v1 call unknown `conflict`). positive_grade_mismatch is 810 in all three.
3. **Negatives and unknowns differ the most.** strict_v1 has 406,016 negatives (closed only); loose_v1 and posrich_v1 have 674,416, which adds 268,400 `open` pairs that strict_v1 calls unknown (`no_closure`). Unknown pairs: 733,538 (strict_v1), 465,107 (loose_v1), 459,230 (posrich_v1). In all three policies, 329,348 `no_answer` and 129,662 `sample_quality_skip` pairs are unknown in all.
4. **The gains are uneven across labels** (Table 8): five labels hold 14% of the open negatives and five hold 47% of the contested positives. Open means no closure was checked; contested means another labeling task's answer conflicts.
5. **Samples with at least one pair in the presence table**: 25,127 (strict_v1), 25,216 (loose_v1, posrich_v1) of 29,233 (Table 3).

## Method

**Tables read** (plain style via `sonoai.paths.dataset_dir`, [DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md); the table list was approved with TASK-124): the sample-label index v1 (read). **Written** (new files only, [DEC-053](../../decisions/DEC-053-table-naming-and-preservation.md)): the three presence tables below. No other table was read. The counts of unknown pairs per label and reason are not in the tables, so they were taken by running the registered policies again in memory over the same index; the rerun gave tables equal to the stored ones for all three policies.

Command, once per policy (changes the dataset folder by adding the two files; refuses when either exists):

```bash
sonoai-data sample-label-presence 261023_plain --index v1 --policy <policy>
```

The policy rules are in `sonoai-data presence-policies` and DEC-060 section 4. The fact relations config (`configs/data/fact_relations_261023.yaml`) differs from the one the index was built with; the policies read only its policy entries and the index is used as built (the command prints this note).

Table 1. The written presence tables (pairs in the table = positive, positive_grade_mismatch, negative).

| Policy | Presence table (`.pkl` and `.xlsx` in `derived/`) | Pairs in the table | sha256 of the `.pkl` |
|---|---|---|---|
| strict_v1 | presence table of strict_v1 | 494,441 | `05b3f4230c46e2319683d1caf7410c148a925e3b453afb0b9183d89adc91fa77` |
| loose_v1 | presence table of loose_v1 | 762,872 | `4fc02a64d7f13ea792972441c81f875bbce15166a038a5f7ef16ebf0081d9659` |
| posrich_v1 | presence table of posrich_v1 | 768,749 | `e261bc38b04575c5648c2128a1e41102d163f6c251c9ad1bb27fb6dec4ae3a27` |

## 1. Comparison of the policies

Table 2. Sample-label pairs per presence state and reason, all content labels, per policy (n = 1,227,979 pairs of the index for each policy; the three columns each add up to it). A reason that a policy does not use is 0.

| Count (sample-label pairs) | strict_v1 | loose_v1 | posrich_v1 |
|---|---|---|---|
| Positive, given, with polygon | 79,656 | 79,677 | 79,677 |
| Positive, given, choice only | 7,959 | 7,969 | 7,969 |
| Positive, given_contested | 0 | 0 | 5,877 |
| **Positive, all** | 87,615 | 87,646 | 93,523 |
| positive_grade_mismatch | 810 | 810 | 810 |
| Negative, closed | 406,016 | 406,016 | 406,016 |
| Negative, open | 0 | 268,400 | 268,400 |
| **Negative, all** | 406,016 | 674,416 | 674,416 |
| Unknown, conflict | 5,877 | 5,877 | 0 |
| Unknown, conformance | 31 | 0 | 0 |
| Unknown, grade_ignored | 220 | 220 | 220 |
| Unknown, no_answer | 329,348 | 329,348 | 329,348 |
| Unknown, no_closure | 268,400 | 0 | 0 |
| Unknown, sample_quality_skip | 129,662 | 129,662 | 129,662 |
| **Unknown, all** | 733,538 | 465,107 | 459,230 |
| **Rows of the presence table** (positive, mismatch, negative) | 494,441 | 762,872 | 768,749 |
| **Index rows (all pairs)** | 1,227,979 | 1,227,979 | 1,227,979 |

Table 3. Samples per policy (n = samples of the sample-label index; one sample can have pairs in several states).

| Samples | strict_v1 | loose_v1 | posrich_v1 |
|---|---|---|---|
| In the sample-label index | 29,233 | 29,233 | 29,233 |
| With at least one pair in the presence table | 25,127 | 25,216 | 25,216 |
| With at least one positive pair | 23,959 | 23,961 | 24,135 |
| With at least one positive_grade_mismatch pair | 406 | 406 | 406 |
| With at least one negative pair | 22,034 | 25,200 | 25,200 |
| With no pair in the presence table (all pairs unknown) | 4,106 | 4,017 | 4,017 |

How far the policies differ, from Table 2: strict_v1 against loose_v1 differ in 268,400 pairs (negative `open` against unknown `no_closure`) and 31 pairs (positive against unknown `conformance`); loose_v1 against posrich_v1 differ in 5,877 pairs (positive `given_contested` against unknown `conflict`).

Table 4. Per content label (100 labels): positive pairs (given and given_contested), negative pairs (closed and open) and unknown pairs (all reasons) under each policy. Labels in alphabetical order. A label with 0 positives in every policy has no given labeling.

| Content label | Positive strict_v1 | Positive loose_v1 | Positive posrich_v1 | Negative strict_v1 | Negative loose_v1 | Negative posrich_v1 | Unknown strict_v1 | Unknown loose_v1 | Unknown posrich_v1 |
|---|---|---|---|---|---|---|---|---|---|
| `adenoma_uterus` | 22 | 22 | 22 | 446 | 449 | 449 | 77 | 74 | 74 |
| `annotation_symbol` | 0 | 0 | 0 | 0 | 0 | 0 | 15,390 | 15,390 | 15,390 |
| `ascites` | 103 | 103 | 159 | 15,767 | 21,246 | 21,246 | 9,525 | 4,046 | 3,990 |
| `bladder` | 501 | 501 | 579 | 13,505 | 16,947 | 16,947 | 5,623 | 2,181 | 2,103 |
| `bladder_tumor` | <5 | <5 | <5 | 453 | 453 | 453 | 63 | 63 | 63 |
| `breast_abscess` | 140 | 140 | 140 | 283 | 6,682 | 6,682 | 6,774 | 375 | 375 |
| `breast_cyst` | 0 | 0 | 0 | 0 | 3,892 | 3,892 | 4,239 | 347 | 347 |
| `breast_tumor` | 2,512 | 2,512 | 2,512 | 281 | 4,310 | 4,310 | 4,404 | 375 | 375 |
| `bursitis` | 123 | 123 | 148 | 5 | 3,744 | 3,744 | 4,111 | 372 | 347 |
| `cholecystitis` | 808 | 810 | 1,048 | 982 | 4,229 | 4,229 | 4,019 | 770 | 532 |
| `common_biliary_duct` | 164 | 164 | 164 | 13,497 | 17,361 | 17,361 | 5,968 | 2,104 | 2,104 |
| `cyst` | 21 | 21 | 21 | 0 | 3,871 | 3,871 | 4,218 | 347 | 347 |
| `cystitis` | 220 | 226 | 386 | 84 | 3,506 | 3,506 | 3,935 | 507 | 347 |
| `cystolithiasis` | 14 | 16 | 21 | 438 | 3,871 | 3,871 | 3,787 | 352 | 347 |
| `diaphragm` | 942 | 942 | 942 | 12,647 | 16,583 | 16,583 | 6,040 | 2,104 | 2,104 |
| `doppler_area` | 0 | 0 | 0 | 0 | 0 | 0 | 15,390 | 15,390 | 15,390 |
| `gallbladder` | 2,212 | 2,212 | 2,447 | 12,765 | 18,958 | 18,958 | 10,418 | 4,225 | 3,990 |
| `gallbladder_contracted` | 159 | 159 | 159 | 0 | 774 | 774 | 879 | 105 | 105 |
| `gallbladder_deformed` | 194 | 194 | 194 | 0 | 739 | 739 | 844 | 105 | 105 |
| `gallbladder_dilated` | 29 | 29 | 29 | 0 | 904 | 904 | 1,009 | 105 | 105 |
| `gallbladder_normalsized` | 176 | 176 | 176 | 0 | 757 | 757 | 862 | 105 | 105 |
| `gallbladder_polyp` | 244 | 245 | 290 | 2,901 | 6,161 | 6,161 | 4,105 | 844 | 799 |
| `gallbladder_stone` | 293 | 294 | 391 | 12,729 | 16,056 | 16,056 | 12,373 | 9,045 | 8,948 |
| `gallbladder_tumor` | 126 | 126 | 144 | 2,667 | 5,931 | 5,931 | 3,814 | 550 | 532 |
| `gastric_tumor` | 49 | 49 | 51 | 12,737 | 16,338 | 16,338 | 12,609 | 9,008 | 9,006 |
| `heart` | 24 | 24 | 24 | 13,583 | 17,502 | 17,502 | 6,022 | 2,103 | 2,103 |
| `hemangioma` | 166 | 168 | 233 | 14,425 | 16,156 | 16,156 | 10,804 | 9,071 | 9,006 |
| `hepatic_abscess` | 0 | 0 | 0 | 2,229 | 2,232 | 2,232 | 182 | 179 | 179 |
| `hepatic_blood_duct` | 4,286 | 4,286 | 4,290 | 0 | 3,576 | 3,576 | 5,814 | 2,238 | 2,234 |
| `hepatic_cirrhosis` | 673 | 673 | 1,115 | 13,545 | 15,274 | 15,274 | 11,177 | 9,448 | 9,006 |
| `hepatic_cyst` | 92 | 93 | 118 | 14,540 | 16,271 | 16,271 | 10,763 | 9,031 | 9,006 |
| `hepatic_duct` | 8,000 | 8,000 | 9,116 | 8,408 | 12,289 | 12,289 | 8,987 | 5,106 | 3,990 |
| `hepatic_precirrhosis` | 205 | 205 | 205 | 2,026 | 2,027 | 2,027 | 180 | 179 | 179 |
| `hepatic_steatosis__0` | 5,954 | 5,955 | 6,124 | 6,111 | 10,018 | 10,018 | 13,179 | 9,271 | 9,102 |
| `hepatic_steatosis__1` | 7,053 | 7,058 | 7,305 | 6,220 | 8,657 | 8,657 | 11,755 | 9,313 | 9,066 |
| `hepatic_steatosis__2` | 1,426 | 1,427 | 1,518 | 10,543 | 14,518 | 14,518 | 13,171 | 9,195 | 9,104 |
| `hepatic_steatosis__3` | 99 | 99 | 140 | 11,349 | 16,110 | 16,110 | 13,910 | 9,149 | 9,108 |
| `hepatic_stone` | 296 | 296 | 296 | 15,068 | 15,071 | 15,071 | 967 | 964 | 964 |
| `hepatic_vascular_branch` | 1,620 | 1,620 | 1,620 | 12,339 | 15,906 | 15,906 | 5,670 | 2,103 | 2,103 |
| `hepatitis` | 336 | 336 | 777 | 13,883 | 15,608 | 15,608 | 11,176 | 9,451 | 9,010 |
| `hepatoma` | 932 | 932 | 1,184 | 13,477 | 15,205 | 15,205 | 10,986 | 9,258 | 9,006 |
| `hepatorenal_contrast_liverbrighter` | 1,632 | 1,634 | 1,634 | 0 | 10,057 | 10,057 | 13,758 | 3,699 | 3,699 |
| `hepatorenal_contrast_possible` | 3,915 | 3,915 | 3,915 | 0 | 7,776 | 7,776 | 11,475 | 3,699 | 3,699 |
| `herniated_disk` | 20 | 21 | 30 | 14 | 3,862 | 3,862 | 4,205 | 356 | 347 |
| `hydronephrosis` | 1,266 | 1,266 | 1,287 | 8,786 | 11,900 | 11,900 | 4,519 | 1,405 | 1,384 |
| `intestine` | 2,507 | 2,507 | 2,783 | 12,013 | 18,622 | 18,622 | 10,875 | 4,266 | 3,990 |
| `kidney` | 9,982 | 9,982 | 10,156 | 5,610 | 11,249 | 11,249 | 9,803 | 4,164 | 3,990 |
| `knee` | 123 | 123 | 160 | 0 | 3,733 | 3,733 | 4,116 | 383 | 346 |
| `ligamenta_flava_hypertrophy` | 17 | 17 | 17 | 27 | 27 | 27 | 12 | 12 | 12 |
| `liquid_near_uterus` | 81 | 81 | 81 | 388 | 390 | 390 | 76 | 74 | 74 |
| `liver` | 15,325 | 15,325 | 15,526 | 4,303 | 5,879 | 5,879 | 5,767 | 4,191 | 3,990 |
| `lung` | 796 | 796 | 801 | 12,792 | 16,724 | 16,724 | 6,041 | 2,109 | 2,104 |
| `myoma_uterus` | 80 | 81 | 145 | 328 | 3,747 | 3,747 | 3,831 | 411 | 347 |
| `myoma_uterus_or_adenomyosis` | 99 | 100 | 100 | 0 | 3,792 | 3,792 | 4,140 | 347 | 347 |
| `nephritis` | 1,498 | 1,498 | 1,817 | 8,263 | 11,372 | 11,372 | 4,812 | 1,703 | 1,384 |
| `nephrocystosis` | 301 | 301 | 310 | 9,765 | 12,879 | 12,879 | 4,506 | 1,392 | 1,383 |
| `ovarian_cyst` | 34 | 36 | 102 | 367 | 3,790 | 3,790 | 3,838 | 413 | 347 |
| `ovarian_follicle` | 22 | 23 | 41 | 342 | 3,851 | 3,851 | 3,875 | 365 | 347 |
| `pancreatin` | 62 | 62 | 133 | 13,578 | 17,393 | 17,393 | 5,989 | 2,174 | 2,103 |
| `parasite` | 6 | 6 | 6 | 0 | 3,886 | 3,886 | 4,233 | 347 | 347 |
| `pleuritis` | 5 | 6 | 7 | 0 | 3,885 | 3,885 | 4,234 | 348 | 347 |
| `portal_vein` | 2,278 | 2,278 | 2,280 | 12,712 | 19,125 | 19,125 | 10,405 | 3,992 | 3,990 |
| `possible_endosis` | 22 | 22 | 22 | 446 | 449 | 449 | 77 | 74 | 74 |
| `pregnancy` | 21 | 21 | 32 | 349 | 3,860 | 3,860 | 3,869 | 358 | 347 |
| `prostate` | 81 | 81 | 126 | 0 | 3,767 | 3,767 | 4,158 | 391 | 346 |
| `prostate_cyst` | <5 | <5 | <5 | 97 | 3,888 | 3,888 | 4,140 | 349 | 347 |
| `prostate_edema` | <5 | <5 | <5 | 97 | 97 | 97 | 5 | 5 | 5 |
| `prostate_stone` | 39 | 39 | 52 | 49 | 3,840 | 3,840 | 4,151 | 360 | 347 |
| `prostate_tumor` | <5 | <5 | <5 | 98 | 98 | 98 | 5 | 5 | 5 |
| `prostatitis` | 5 | 5 | 16 | 85 | 3,876 | 3,876 | 4,149 | 358 | 347 |
| `prostatomegaly` | 5 | 5 | 5 | 0 | 3,887 | 3,887 | 4,234 | 347 | 347 |
| `renal_calculus` | 1,888 | 1,888 | 1,950 | 8,125 | 11,238 | 11,238 | 4,560 | 1,447 | 1,385 |
| `renal_carcinoma` | 144 | 144 | 153 | 9,918 | 13,032 | 13,032 | 4,508 | 1,394 | 1,385 |
| `sign_attenuation` | <5 | <5 | <5 | 7 | 8 | 8 | 15,381 | 15,380 | 15,380 |
| `sign_gallbladder_wall_hypertrophy` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_gallbladder_wall_hypertrophy_exterior` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_gallbladder_wall_hypertrophy_interior` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_geographic_liver_background` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_hepatic_blood_duct_narrow_background` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_hepatic_blood_duct_narrow_object` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_hepatic_vein_hypertrophy` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_liver_shrinkage` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_liveredge_blunt` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_liveredge_sharp` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_liverskin_coarse` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `sign_liverskin_smooth` | <5 | <5 | <5 | 8 | 9 | 9 | 15,381 | 15,380 | 15,380 |
| `sign_particles_uneven_background` | 0 | 0 | 0 | 8 | 10 | 10 | 15,382 | 15,380 | 15,380 |
| `skin_tumor` | 13 | 13 | 13 | 0 | 3,879 | 3,879 | 4,226 | 347 | 347 |
| `spine` | 39 | 39 | 55 | 13,583 | 17,471 | 17,471 | 6,007 | 2,119 | 2,103 |
| `spleen` | 961 | 961 | 996 | 12,712 | 20,409 | 20,409 | 11,722 | 4,025 | 3,990 |
| `stenosis` | <5 | <5 | <5 | 42 | 42 | 42 | 12 | 12 | 12 |
| `stomach` | 3,562 | 3,562 | 3,990 | 11,032 | 17,415 | 17,415 | 10,801 | 4,418 | 3,990 |
| `thyroid` | 10 | 10 | 19 | 0 | 3,874 | 3,874 | 4,229 | 355 | 346 |
| `thyroid_cyst` | 19 | 19 | 19 | 21 | 3,950 | 3,950 | 4,276 | 347 | 347 |
| `thyroid_tumor` | 57 | 57 | 61 | 13 | 3,908 | 3,908 | 4,246 | 351 | 347 |
| `thyroiditis` | 11 | 11 | 15 | 17 | 3,954 | 3,954 | 4,288 | 351 | 347 |
| `tumor` | 47 | 47 | 47 | 0 | 3,845 | 3,845 | 4,192 | 347 | 347 |
| `ultrasound_area` | 0 | 0 | 0 | 0 | 0 | 0 | 15,390 | 15,390 | 15,390 |
| `uterus` | 411 | 411 | 514 | 0 | 3,379 | 3,379 | 3,828 | 449 | 346 |
| `weak_signal_area` | 0 | 0 | 0 | 0 | 0 | 0 | 15,390 | 15,390 | 15,390 |

## 2. Counts per content label and state, per policy

The columns are the states and reasons of Table 2. A label with no row in the index has no counts here and is unknown by the rule of the index.

Table 5. strict_v1: sample-label pairs per content label, state and reason.

| Content label | Positive, given, with polygon | Positive, given, choice only | positive_grade_mismatch | Negative, closed | Negative, open | Unknown, conflict | Unknown, conformance | Unknown, grade_ignored | Unknown, no_answer | Unknown, no_closure | Unknown, sample_quality_skip |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `adenoma_uterus` | 22 | 0 | 0 | 446 | 0 | 0 | 0 | 0 | 47 | <5 | 27 |
| `annotation_symbol` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 0 | 1,257 |
| `ascites` | 103 | 0 | 0 | 15,767 | 0 | 56 | 0 | 0 | 500 | 5,479 | 3,490 |
| `bladder` | 501 | 0 | 0 | 13,505 | 0 | 78 | 0 | 0 | 500 | 3,442 | 1,603 |
| `bladder_tumor` | <5 | 0 | 0 | 453 | 0 | 0 | 0 | 0 | 52 | 0 | 11 |
| `breast_abscess` | 140 | 0 | 0 | 283 | 0 | 0 | 0 | 0 | <5 | 6,399 | 374 |
| `breast_cyst` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | <5 | 3,892 | 346 |
| `breast_tumor` | 2,509 | <5 | 0 | 281 | 0 | 0 | 0 | 0 | <5 | 4,029 | 374 |
| `bursitis` | 116 | 7 | 0 | 5 | 0 | 25 | 0 | 0 | <5 | 3,739 | 346 |
| `cholecystitis` | 805 | <5 | 0 | 982 | 0 | 238 | <5 | 0 | <5 | 3,247 | 531 |
| `common_biliary_duct` | 86 | 78 | 0 | 13,497 | 0 | 0 | 0 | 0 | 501 | 3,864 | 1,603 |
| `cyst` | 0 | 21 | 0 | 0 | 0 | 0 | 0 | 0 | <5 | 3,871 | 346 |
| `cystitis` | 211 | 9 | 0 | 84 | 0 | 160 | 6 | 0 | <5 | 3,422 | 346 |
| `cystolithiasis` | 13 | <5 | 0 | 438 | 0 | 5 | <5 | 0 | <5 | 3,433 | 346 |
| `diaphragm` | 942 | 0 | 0 | 12,647 | 0 | 0 | 0 | 0 | 501 | 3,936 | 1,603 |
| `doppler_area` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 0 | 1,257 |
| `gallbladder` | 2,212 | 0 | 0 | 12,765 | 0 | 235 | 0 | 0 | 500 | 6,193 | 3,490 |
| `gallbladder_contracted` | 0 | 159 | 0 | 0 | 0 | 0 | 0 | 0 | 76 | 774 | 29 |
| `gallbladder_deformed` | 0 | 194 | 0 | 0 | 0 | 0 | 0 | 0 | 76 | 739 | 29 |
| `gallbladder_dilated` | 0 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | 76 | 904 | 29 |
| `gallbladder_normalsized` | 0 | 176 | 0 | 0 | 0 | 0 | 0 | 0 | 76 | 757 | 29 |
| `gallbladder_polyp` | 243 | <5 | 0 | 2,901 | 0 | 45 | <5 | 0 | <5 | 3,260 | 798 |
| `gallbladder_stone` | 292 | <5 | 0 | 12,729 | 0 | 97 | <5 | 0 | 5,458 | 3,327 | 3,490 |
| `gallbladder_tumor` | 125 | <5 | 0 | 2,667 | 0 | 18 | 0 | 0 | <5 | 3,264 | 531 |
| `gastric_tumor` | 48 | <5 | 0 | 12,737 | 0 | <5 | 0 | 0 | 5,516 | 3,601 | 3,490 |
| `heart` | 24 | 0 | 0 | 13,583 | 0 | 0 | 0 | 0 | 500 | 3,919 | 1,603 |
| `hemangioma` | 165 | <5 | 0 | 14,425 | 0 | 65 | <5 | 0 | 5,516 | 1,731 | 3,490 |
| `hepatic_abscess` | 0 | 0 | 0 | 2,229 | 0 | 0 | 0 | 0 | 117 | <5 | 62 |
| `hepatic_blood_duct` | 2,762 | 1,524 | 0 | 0 | 0 | <5 | 0 | 0 | <5 | 3,576 | 2,233 |
| `hepatic_cirrhosis` | 670 | <5 | 0 | 13,545 | 0 | 442 | 0 | 0 | 5,516 | 1,729 | 3,490 |
| `hepatic_cyst` | 90 | <5 | 0 | 14,540 | 0 | 25 | <5 | 0 | 5,516 | 1,731 | 3,490 |
| `hepatic_duct` | 8,000 | 0 | 0 | 8,408 | 0 | 1,116 | 0 | 0 | 500 | 3,881 | 3,490 |
| `hepatic_precirrhosis` | 205 | 0 | 0 | 2,026 | 0 | 0 | 0 | 0 | 117 | <5 | 62 |
| `hepatic_steatosis__0` | 5,950 | <5 | 151 | 6,111 | 0 | 169 | <5 | 55 | 5,557 | 3,907 | 3,490 |
| `hepatic_steatosis__1` | 7,051 | <5 | 367 | 6,220 | 0 | 247 | 5 | 55 | 5,521 | 2,437 | 3,490 |
| `hepatic_steatosis__2` | 1,424 | <5 | 255 | 10,543 | 0 | 91 | <5 | 55 | 5,559 | 3,975 | 3,490 |
| `hepatic_steatosis__3` | 97 | <5 | 37 | 11,349 | 0 | 41 | 0 | 55 | 5,563 | 4,761 | 3,490 |
| `hepatic_stone` | 296 | 0 | 0 | 15,068 | 0 | 0 | 0 | 0 | 159 | <5 | 805 |
| `hepatic_vascular_branch` | 1,620 | 0 | 0 | 12,339 | 0 | 0 | 0 | 0 | 500 | 3,567 | 1,603 |
| `hepatitis` | 333 | <5 | 0 | 13,883 | 0 | 441 | 0 | 0 | 5,520 | 1,725 | 3,490 |
| `hepatoma` | 932 | 0 | 0 | 13,477 | 0 | 252 | 0 | 0 | 5,516 | 1,728 | 3,490 |
| `hepatorenal_contrast_liverbrighter` | 0 | 1,632 | 0 | 0 | 0 | 0 | <5 | 0 | 2,442 | 10,057 | 1,257 |
| `hepatorenal_contrast_possible` | 0 | 3,915 | 0 | 0 | 0 | 0 | 0 | 0 | 2,442 | 7,776 | 1,257 |
| `herniated_disk` | 20 | 0 | 0 | 14 | 0 | 9 | <5 | 0 | <5 | 3,848 | 346 |
| `hydronephrosis` | 1,266 | 0 | 0 | 8,786 | 0 | 21 | 0 | 0 | <5 | 3,114 | 1,383 |
| `intestine` | 2,507 | 0 | 0 | 12,013 | 0 | 276 | 0 | 0 | 500 | 6,609 | 3,490 |
| `kidney` | 9,982 | 0 | 0 | 5,610 | 0 | 174 | 0 | 0 | 500 | 5,639 | 3,490 |
| `knee` | 123 | 0 | 0 | 0 | 0 | 37 | 0 | 0 | 0 | 3,733 | 346 |
| `ligamenta_flava_hypertrophy` | 17 | 0 | 0 | 27 | 0 | 0 | 0 | 0 | 11 | 0 | <5 |
| `liquid_near_uterus` | 81 | 0 | 0 | 388 | 0 | 0 | 0 | 0 | 47 | <5 | 27 |
| `liver` | 15,325 | 0 | 0 | 4,303 | 0 | 201 | 0 | 0 | 500 | 1,576 | 3,490 |
| `lung` | 795 | <5 | 0 | 12,792 | 0 | 5 | 0 | 0 | 501 | 3,932 | 1,603 |
| `myoma_uterus` | 75 | 5 | 0 | 328 | 0 | 64 | <5 | 0 | <5 | 3,419 | 346 |
| `myoma_uterus_or_adenomyosis` | 0 | 99 | 0 | 0 | 0 | 0 | <5 | 0 | <5 | 3,792 | 346 |
| `nephritis` | 1,493 | 5 | 0 | 8,263 | 0 | 319 | 0 | 0 | <5 | 3,109 | 1,383 |
| `nephrocystosis` | 301 | 0 | 0 | 9,765 | 0 | 9 | 0 | 0 | <5 | 3,114 | 1,382 |
| `ovarian_cyst` | 33 | <5 | 0 | 367 | 0 | 66 | <5 | 0 | <5 | 3,423 | 346 |
| `ovarian_follicle` | 20 | <5 | 0 | 342 | 0 | 18 | <5 | 0 | <5 | 3,509 | 346 |
| `pancreatin` | 62 | 0 | 0 | 13,578 | 0 | 71 | 0 | 0 | 500 | 3,815 | 1,603 |
| `parasite` | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | <5 | 3,886 | 346 |
| `pleuritis` | 5 | 0 | 0 | 0 | 0 | <5 | <5 | 0 | <5 | 3,885 | 346 |
| `portal_vein` | 2,278 | 0 | 0 | 12,712 | 0 | <5 | 0 | 0 | 500 | 6,413 | 3,490 |
| `possible_endosis` | 22 | 0 | 0 | 446 | 0 | 0 | 0 | 0 | 47 | <5 | 27 |
| `pregnancy` | 21 | 0 | 0 | 349 | 0 | 11 | 0 | 0 | <5 | 3,511 | 346 |
| `prostate` | 81 | 0 | 0 | 0 | 0 | 45 | 0 | 0 | 0 | 3,767 | 346 |
| `prostate_cyst` | <5 | 0 | 0 | 97 | 0 | <5 | 0 | 0 | <5 | 3,791 | 346 |
| `prostate_edema` | <5 | 0 | 0 | 97 | 0 | 0 | 0 | 0 | <5 | 0 | <5 |
| `prostate_stone` | 39 | 0 | 0 | 49 | 0 | 13 | 0 | 0 | <5 | 3,791 | 346 |
| `prostate_tumor` | <5 | 0 | 0 | 98 | 0 | 0 | 0 | 0 | <5 | 0 | <5 |
| `prostatitis` | 5 | 0 | 0 | 85 | 0 | 11 | 0 | 0 | <5 | 3,791 | 346 |
| `prostatomegaly` | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | <5 | 3,887 | 346 |
| `renal_calculus` | 1,887 | <5 | 0 | 8,125 | 0 | 62 | 0 | 0 | <5 | 3,113 | 1,384 |
| `renal_carcinoma` | 144 | 0 | 0 | 9,918 | 0 | 9 | 0 | 0 | <5 | 3,114 | 1,384 |
| `sign_attenuation` | <5 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_gallbladder_wall_hypertrophy` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_gallbladder_wall_hypertrophy_exterior` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_gallbladder_wall_hypertrophy_interior` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_geographic_liver_background` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_hepatic_blood_duct_narrow_background` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_hepatic_blood_duct_narrow_object` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_hepatic_vein_hypertrophy` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_liver_shrinkage` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_liveredge_blunt` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_liveredge_sharp` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_liverskin_coarse` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_liverskin_smooth` | <5 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `sign_particles_uneven_background` | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 14,123 | <5 | 1,257 |
| `skin_tumor` | 0 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | <5 | 3,879 | 346 |
| `spine` | 39 | 0 | 0 | 13,583 | 0 | 16 | 0 | 0 | 500 | 3,888 | 1,603 |
| `spleen` | 961 | 0 | 0 | 12,712 | 0 | 35 | 0 | 0 | 500 | 7,697 | 3,490 |
| `stenosis` | <5 | 0 | 0 | 42 | 0 | 0 | 0 | 0 | 11 | 0 | <5 |
| `stomach` | 3,562 | 0 | 0 | 11,032 | 0 | 428 | 0 | 0 | 500 | 6,383 | 3,490 |
| `thyroid` | 10 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 3,874 | 346 |
| `thyroid_cyst` | 19 | 0 | 0 | 21 | 0 | 0 | 0 | 0 | <5 | 3,929 | 346 |
| `thyroid_tumor` | 57 | 0 | 0 | 13 | 0 | <5 | 0 | 0 | <5 | 3,895 | 346 |
| `thyroiditis` | 11 | 0 | 0 | 17 | 0 | <5 | 0 | 0 | <5 | 3,937 | 346 |
| `tumor` | 0 | 47 | 0 | 0 | 0 | 0 | 0 | 0 | <5 | 3,845 | 346 |
| `ultrasound_area` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 0 | 1,257 |
| `uterus` | 411 | 0 | 0 | 0 | 0 | 103 | 0 | 0 | 0 | 3,379 | 346 |
| `weak_signal_area` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 0 | 1,257 |
| **All labels** | 79,656 | 7,959 | 810 | 406,016 | 0 | 5,877 | 31 | 220 | 329,348 | 268,400 | 129,662 |

Table 6. loose_v1: sample-label pairs per content label, state and reason.

| Content label | Positive, given, with polygon | Positive, given, choice only | positive_grade_mismatch | Negative, closed | Negative, open | Unknown, conflict | Unknown, grade_ignored | Unknown, no_answer | Unknown, sample_quality_skip |
|---|---|---|---|---|---|---|---|---|---|
| `adenoma_uterus` | 22 | 0 | 0 | 446 | <5 | 0 | 0 | 47 | 27 |
| `annotation_symbol` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 1,257 |
| `ascites` | 103 | 0 | 0 | 15,767 | 5,479 | 56 | 0 | 500 | 3,490 |
| `bladder` | 501 | 0 | 0 | 13,505 | 3,442 | 78 | 0 | 500 | 1,603 |
| `bladder_tumor` | <5 | 0 | 0 | 453 | 0 | 0 | 0 | 52 | 11 |
| `breast_abscess` | 140 | 0 | 0 | 283 | 6,399 | 0 | 0 | <5 | 374 |
| `breast_cyst` | 0 | 0 | 0 | 0 | 3,892 | 0 | 0 | <5 | 346 |
| `breast_tumor` | 2,509 | <5 | 0 | 281 | 4,029 | 0 | 0 | <5 | 374 |
| `bursitis` | 116 | 7 | 0 | 5 | 3,739 | 25 | 0 | <5 | 346 |
| `cholecystitis` | 807 | <5 | 0 | 982 | 3,247 | 238 | 0 | <5 | 531 |
| `common_biliary_duct` | 86 | 78 | 0 | 13,497 | 3,864 | 0 | 0 | 501 | 1,603 |
| `cyst` | 0 | 21 | 0 | 0 | 3,871 | 0 | 0 | <5 | 346 |
| `cystitis` | 212 | 14 | 0 | 84 | 3,422 | 160 | 0 | <5 | 346 |
| `cystolithiasis` | 13 | <5 | 0 | 438 | 3,433 | 5 | 0 | <5 | 346 |
| `diaphragm` | 942 | 0 | 0 | 12,647 | 3,936 | 0 | 0 | 501 | 1,603 |
| `doppler_area` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 1,257 |
| `gallbladder` | 2,212 | 0 | 0 | 12,765 | 6,193 | 235 | 0 | 500 | 3,490 |
| `gallbladder_contracted` | 0 | 159 | 0 | 0 | 774 | 0 | 0 | 76 | 29 |
| `gallbladder_deformed` | 0 | 194 | 0 | 0 | 739 | 0 | 0 | 76 | 29 |
| `gallbladder_dilated` | 0 | 29 | 0 | 0 | 904 | 0 | 0 | 76 | 29 |
| `gallbladder_normalsized` | 0 | 176 | 0 | 0 | 757 | 0 | 0 | 76 | 29 |
| `gallbladder_polyp` | 244 | <5 | 0 | 2,901 | 3,260 | 45 | 0 | <5 | 798 |
| `gallbladder_stone` | 293 | <5 | 0 | 12,729 | 3,327 | 97 | 0 | 5,458 | 3,490 |
| `gallbladder_tumor` | 125 | <5 | 0 | 2,667 | 3,264 | 18 | 0 | <5 | 531 |
| `gastric_tumor` | 48 | <5 | 0 | 12,737 | 3,601 | <5 | 0 | 5,516 | 3,490 |
| `heart` | 24 | 0 | 0 | 13,583 | 3,919 | 0 | 0 | 500 | 1,603 |
| `hemangioma` | 167 | <5 | 0 | 14,425 | 1,731 | 65 | 0 | 5,516 | 3,490 |
| `hepatic_abscess` | 0 | 0 | 0 | 2,229 | <5 | 0 | 0 | 117 | 62 |
| `hepatic_blood_duct` | 2,762 | 1,524 | 0 | 0 | 3,576 | <5 | 0 | <5 | 2,233 |
| `hepatic_cirrhosis` | 670 | <5 | 0 | 13,545 | 1,729 | 442 | 0 | 5,516 | 3,490 |
| `hepatic_cyst` | 91 | <5 | 0 | 14,540 | 1,731 | 25 | 0 | 5,516 | 3,490 |
| `hepatic_duct` | 8,000 | 0 | 0 | 8,408 | 3,881 | 1,116 | 0 | 500 | 3,490 |
| `hepatic_precirrhosis` | 205 | 0 | 0 | 2,026 | <5 | 0 | 0 | 117 | 62 |
| `hepatic_steatosis__0` | 5,951 | <5 | 151 | 6,111 | 3,907 | 169 | 55 | 5,557 | 3,490 |
| `hepatic_steatosis__1` | 7,056 | <5 | 367 | 6,220 | 2,437 | 247 | 55 | 5,521 | 3,490 |
| `hepatic_steatosis__2` | 1,425 | <5 | 255 | 10,543 | 3,975 | 91 | 55 | 5,559 | 3,490 |
| `hepatic_steatosis__3` | 97 | <5 | 37 | 11,349 | 4,761 | 41 | 55 | 5,563 | 3,490 |
| `hepatic_stone` | 296 | 0 | 0 | 15,068 | <5 | 0 | 0 | 159 | 805 |
| `hepatic_vascular_branch` | 1,620 | 0 | 0 | 12,339 | 3,567 | 0 | 0 | 500 | 1,603 |
| `hepatitis` | 333 | <5 | 0 | 13,883 | 1,725 | 441 | 0 | 5,520 | 3,490 |
| `hepatoma` | 932 | 0 | 0 | 13,477 | 1,728 | 252 | 0 | 5,516 | 3,490 |
| `hepatorenal_contrast_liverbrighter` | 0 | 1,634 | 0 | 0 | 10,057 | 0 | 0 | 2,442 | 1,257 |
| `hepatorenal_contrast_possible` | 0 | 3,915 | 0 | 0 | 7,776 | 0 | 0 | 2,442 | 1,257 |
| `herniated_disk` | 21 | 0 | 0 | 14 | 3,848 | 9 | 0 | <5 | 346 |
| `hydronephrosis` | 1,266 | 0 | 0 | 8,786 | 3,114 | 21 | 0 | <5 | 1,383 |
| `intestine` | 2,507 | 0 | 0 | 12,013 | 6,609 | 276 | 0 | 500 | 3,490 |
| `kidney` | 9,982 | 0 | 0 | 5,610 | 5,639 | 174 | 0 | 500 | 3,490 |
| `knee` | 123 | 0 | 0 | 0 | 3,733 | 37 | 0 | 0 | 346 |
| `ligamenta_flava_hypertrophy` | 17 | 0 | 0 | 27 | 0 | 0 | 0 | 11 | <5 |
| `liquid_near_uterus` | 81 | 0 | 0 | 388 | <5 | 0 | 0 | 47 | 27 |
| `liver` | 15,325 | 0 | 0 | 4,303 | 1,576 | 201 | 0 | 500 | 3,490 |
| `lung` | 795 | <5 | 0 | 12,792 | 3,932 | 5 | 0 | 501 | 1,603 |
| `myoma_uterus` | 76 | 5 | 0 | 328 | 3,419 | 64 | 0 | <5 | 346 |
| `myoma_uterus_or_adenomyosis` | 0 | 100 | 0 | 0 | 3,792 | 0 | 0 | <5 | 346 |
| `nephritis` | 1,493 | 5 | 0 | 8,263 | 3,109 | 319 | 0 | <5 | 1,383 |
| `nephrocystosis` | 301 | 0 | 0 | 9,765 | 3,114 | 9 | 0 | <5 | 1,382 |
| `ovarian_cyst` | 35 | <5 | 0 | 367 | 3,423 | 66 | 0 | <5 | 346 |
| `ovarian_follicle` | 21 | <5 | 0 | 342 | 3,509 | 18 | 0 | <5 | 346 |
| `pancreatin` | 62 | 0 | 0 | 13,578 | 3,815 | 71 | 0 | 500 | 1,603 |
| `parasite` | 0 | 6 | 0 | 0 | 3,886 | 0 | 0 | <5 | 346 |
| `pleuritis` | 6 | 0 | 0 | 0 | 3,885 | <5 | 0 | <5 | 346 |
| `portal_vein` | 2,278 | 0 | 0 | 12,712 | 6,413 | <5 | 0 | 500 | 3,490 |
| `possible_endosis` | 22 | 0 | 0 | 446 | <5 | 0 | 0 | 47 | 27 |
| `pregnancy` | 21 | 0 | 0 | 349 | 3,511 | 11 | 0 | <5 | 346 |
| `prostate` | 81 | 0 | 0 | 0 | 3,767 | 45 | 0 | 0 | 346 |
| `prostate_cyst` | <5 | 0 | 0 | 97 | 3,791 | <5 | 0 | <5 | 346 |
| `prostate_edema` | <5 | 0 | 0 | 97 | 0 | 0 | 0 | <5 | <5 |
| `prostate_stone` | 39 | 0 | 0 | 49 | 3,791 | 13 | 0 | <5 | 346 |
| `prostate_tumor` | <5 | 0 | 0 | 98 | 0 | 0 | 0 | <5 | <5 |
| `prostatitis` | 5 | 0 | 0 | 85 | 3,791 | 11 | 0 | <5 | 346 |
| `prostatomegaly` | 0 | 5 | 0 | 0 | 3,887 | 0 | 0 | <5 | 346 |
| `renal_calculus` | 1,887 | <5 | 0 | 8,125 | 3,113 | 62 | 0 | <5 | 1,384 |
| `renal_carcinoma` | 144 | 0 | 0 | 9,918 | 3,114 | 9 | 0 | <5 | 1,384 |
| `sign_attenuation` | <5 | 0 | 0 | 7 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_gallbladder_wall_hypertrophy` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_gallbladder_wall_hypertrophy_exterior` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_gallbladder_wall_hypertrophy_interior` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_geographic_liver_background` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_hepatic_blood_duct_narrow_background` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_hepatic_blood_duct_narrow_object` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_hepatic_vein_hypertrophy` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_liver_shrinkage` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_liveredge_blunt` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_liveredge_sharp` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_liverskin_coarse` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_liverskin_smooth` | <5 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `sign_particles_uneven_background` | 0 | 0 | 0 | 8 | <5 | 0 | 0 | 14,123 | 1,257 |
| `skin_tumor` | 0 | 13 | 0 | 0 | 3,879 | 0 | 0 | <5 | 346 |
| `spine` | 39 | 0 | 0 | 13,583 | 3,888 | 16 | 0 | 500 | 1,603 |
| `spleen` | 961 | 0 | 0 | 12,712 | 7,697 | 35 | 0 | 500 | 3,490 |
| `stenosis` | <5 | 0 | 0 | 42 | 0 | 0 | 0 | 11 | <5 |
| `stomach` | 3,562 | 0 | 0 | 11,032 | 6,383 | 428 | 0 | 500 | 3,490 |
| `thyroid` | 10 | 0 | 0 | 0 | 3,874 | 9 | 0 | 0 | 346 |
| `thyroid_cyst` | 19 | 0 | 0 | 21 | 3,929 | 0 | 0 | <5 | 346 |
| `thyroid_tumor` | 57 | 0 | 0 | 13 | 3,895 | <5 | 0 | <5 | 346 |
| `thyroiditis` | 11 | 0 | 0 | 17 | 3,937 | <5 | 0 | <5 | 346 |
| `tumor` | 0 | 47 | 0 | 0 | 3,845 | 0 | 0 | <5 | 346 |
| `ultrasound_area` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 1,257 |
| `uterus` | 411 | 0 | 0 | 0 | 3,379 | 103 | 0 | 0 | 346 |
| `weak_signal_area` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 1,257 |
| **All labels** | 79,677 | 7,969 | 810 | 406,016 | 268,400 | 5,877 | 220 | 329,348 | 129,662 |

Table 7. posrich_v1: sample-label pairs per content label, state and reason.

| Content label | Positive, given, with polygon | Positive, given, choice only | Positive, given_contested | positive_grade_mismatch | Negative, closed | Negative, open | Unknown, grade_ignored | Unknown, no_answer | Unknown, sample_quality_skip |
|---|---|---|---|---|---|---|---|---|---|
| `adenoma_uterus` | 22 | 0 | 0 | 0 | 446 | <5 | 0 | 47 | 27 |
| `annotation_symbol` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 1,257 |
| `ascites` | 103 | 0 | 56 | 0 | 15,767 | 5,479 | 0 | 500 | 3,490 |
| `bladder` | 501 | 0 | 78 | 0 | 13,505 | 3,442 | 0 | 500 | 1,603 |
| `bladder_tumor` | <5 | 0 | 0 | 0 | 453 | 0 | 0 | 52 | 11 |
| `breast_abscess` | 140 | 0 | 0 | 0 | 283 | 6,399 | 0 | <5 | 374 |
| `breast_cyst` | 0 | 0 | 0 | 0 | 0 | 3,892 | 0 | <5 | 346 |
| `breast_tumor` | 2,509 | <5 | 0 | 0 | 281 | 4,029 | 0 | <5 | 374 |
| `bursitis` | 116 | 7 | 25 | 0 | 5 | 3,739 | 0 | <5 | 346 |
| `cholecystitis` | 807 | <5 | 238 | 0 | 982 | 3,247 | 0 | <5 | 531 |
| `common_biliary_duct` | 86 | 78 | 0 | 0 | 13,497 | 3,864 | 0 | 501 | 1,603 |
| `cyst` | 0 | 21 | 0 | 0 | 0 | 3,871 | 0 | <5 | 346 |
| `cystitis` | 212 | 14 | 160 | 0 | 84 | 3,422 | 0 | <5 | 346 |
| `cystolithiasis` | 13 | <5 | 5 | 0 | 438 | 3,433 | 0 | <5 | 346 |
| `diaphragm` | 942 | 0 | 0 | 0 | 12,647 | 3,936 | 0 | 501 | 1,603 |
| `doppler_area` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 1,257 |
| `gallbladder` | 2,212 | 0 | 235 | 0 | 12,765 | 6,193 | 0 | 500 | 3,490 |
| `gallbladder_contracted` | 0 | 159 | 0 | 0 | 0 | 774 | 0 | 76 | 29 |
| `gallbladder_deformed` | 0 | 194 | 0 | 0 | 0 | 739 | 0 | 76 | 29 |
| `gallbladder_dilated` | 0 | 29 | 0 | 0 | 0 | 904 | 0 | 76 | 29 |
| `gallbladder_normalsized` | 0 | 176 | 0 | 0 | 0 | 757 | 0 | 76 | 29 |
| `gallbladder_polyp` | 244 | <5 | 45 | 0 | 2,901 | 3,260 | 0 | <5 | 798 |
| `gallbladder_stone` | 293 | <5 | 97 | 0 | 12,729 | 3,327 | 0 | 5,458 | 3,490 |
| `gallbladder_tumor` | 125 | <5 | 18 | 0 | 2,667 | 3,264 | 0 | <5 | 531 |
| `gastric_tumor` | 48 | <5 | <5 | 0 | 12,737 | 3,601 | 0 | 5,516 | 3,490 |
| `heart` | 24 | 0 | 0 | 0 | 13,583 | 3,919 | 0 | 500 | 1,603 |
| `hemangioma` | 167 | <5 | 65 | 0 | 14,425 | 1,731 | 0 | 5,516 | 3,490 |
| `hepatic_abscess` | 0 | 0 | 0 | 0 | 2,229 | <5 | 0 | 117 | 62 |
| `hepatic_blood_duct` | 2,762 | 1,524 | <5 | 0 | 0 | 3,576 | 0 | <5 | 2,233 |
| `hepatic_cirrhosis` | 670 | <5 | 442 | 0 | 13,545 | 1,729 | 0 | 5,516 | 3,490 |
| `hepatic_cyst` | 91 | <5 | 25 | 0 | 14,540 | 1,731 | 0 | 5,516 | 3,490 |
| `hepatic_duct` | 8,000 | 0 | 1,116 | 0 | 8,408 | 3,881 | 0 | 500 | 3,490 |
| `hepatic_precirrhosis` | 205 | 0 | 0 | 0 | 2,026 | <5 | 0 | 117 | 62 |
| `hepatic_steatosis__0` | 5,951 | <5 | 169 | 151 | 6,111 | 3,907 | 55 | 5,557 | 3,490 |
| `hepatic_steatosis__1` | 7,056 | <5 | 247 | 367 | 6,220 | 2,437 | 55 | 5,521 | 3,490 |
| `hepatic_steatosis__2` | 1,425 | <5 | 91 | 255 | 10,543 | 3,975 | 55 | 5,559 | 3,490 |
| `hepatic_steatosis__3` | 97 | <5 | 41 | 37 | 11,349 | 4,761 | 55 | 5,563 | 3,490 |
| `hepatic_stone` | 296 | 0 | 0 | 0 | 15,068 | <5 | 0 | 159 | 805 |
| `hepatic_vascular_branch` | 1,620 | 0 | 0 | 0 | 12,339 | 3,567 | 0 | 500 | 1,603 |
| `hepatitis` | 333 | <5 | 441 | 0 | 13,883 | 1,725 | 0 | 5,520 | 3,490 |
| `hepatoma` | 932 | 0 | 252 | 0 | 13,477 | 1,728 | 0 | 5,516 | 3,490 |
| `hepatorenal_contrast_liverbrighter` | 0 | 1,634 | 0 | 0 | 0 | 10,057 | 0 | 2,442 | 1,257 |
| `hepatorenal_contrast_possible` | 0 | 3,915 | 0 | 0 | 0 | 7,776 | 0 | 2,442 | 1,257 |
| `herniated_disk` | 21 | 0 | 9 | 0 | 14 | 3,848 | 0 | <5 | 346 |
| `hydronephrosis` | 1,266 | 0 | 21 | 0 | 8,786 | 3,114 | 0 | <5 | 1,383 |
| `intestine` | 2,507 | 0 | 276 | 0 | 12,013 | 6,609 | 0 | 500 | 3,490 |
| `kidney` | 9,982 | 0 | 174 | 0 | 5,610 | 5,639 | 0 | 500 | 3,490 |
| `knee` | 123 | 0 | 37 | 0 | 0 | 3,733 | 0 | 0 | 346 |
| `ligamenta_flava_hypertrophy` | 17 | 0 | 0 | 0 | 27 | 0 | 0 | 11 | <5 |
| `liquid_near_uterus` | 81 | 0 | 0 | 0 | 388 | <5 | 0 | 47 | 27 |
| `liver` | 15,325 | 0 | 201 | 0 | 4,303 | 1,576 | 0 | 500 | 3,490 |
| `lung` | 795 | <5 | 5 | 0 | 12,792 | 3,932 | 0 | 501 | 1,603 |
| `myoma_uterus` | 76 | 5 | 64 | 0 | 328 | 3,419 | 0 | <5 | 346 |
| `myoma_uterus_or_adenomyosis` | 0 | 100 | 0 | 0 | 0 | 3,792 | 0 | <5 | 346 |
| `nephritis` | 1,493 | 5 | 319 | 0 | 8,263 | 3,109 | 0 | <5 | 1,383 |
| `nephrocystosis` | 301 | 0 | 9 | 0 | 9,765 | 3,114 | 0 | <5 | 1,382 |
| `ovarian_cyst` | 35 | <5 | 66 | 0 | 367 | 3,423 | 0 | <5 | 346 |
| `ovarian_follicle` | 21 | <5 | 18 | 0 | 342 | 3,509 | 0 | <5 | 346 |
| `pancreatin` | 62 | 0 | 71 | 0 | 13,578 | 3,815 | 0 | 500 | 1,603 |
| `parasite` | 0 | 6 | 0 | 0 | 0 | 3,886 | 0 | <5 | 346 |
| `pleuritis` | 6 | 0 | <5 | 0 | 0 | 3,885 | 0 | <5 | 346 |
| `portal_vein` | 2,278 | 0 | <5 | 0 | 12,712 | 6,413 | 0 | 500 | 3,490 |
| `possible_endosis` | 22 | 0 | 0 | 0 | 446 | <5 | 0 | 47 | 27 |
| `pregnancy` | 21 | 0 | 11 | 0 | 349 | 3,511 | 0 | <5 | 346 |
| `prostate` | 81 | 0 | 45 | 0 | 0 | 3,767 | 0 | 0 | 346 |
| `prostate_cyst` | <5 | 0 | <5 | 0 | 97 | 3,791 | 0 | <5 | 346 |
| `prostate_edema` | <5 | 0 | 0 | 0 | 97 | 0 | 0 | <5 | <5 |
| `prostate_stone` | 39 | 0 | 13 | 0 | 49 | 3,791 | 0 | <5 | 346 |
| `prostate_tumor` | <5 | 0 | 0 | 0 | 98 | 0 | 0 | <5 | <5 |
| `prostatitis` | 5 | 0 | 11 | 0 | 85 | 3,791 | 0 | <5 | 346 |
| `prostatomegaly` | 0 | 5 | 0 | 0 | 0 | 3,887 | 0 | <5 | 346 |
| `renal_calculus` | 1,887 | <5 | 62 | 0 | 8,125 | 3,113 | 0 | <5 | 1,384 |
| `renal_carcinoma` | 144 | 0 | 9 | 0 | 9,918 | 3,114 | 0 | <5 | 1,384 |
| `sign_attenuation` | <5 | 0 | 0 | 0 | 7 | <5 | 0 | 14,123 | 1,257 |
| `sign_gallbladder_wall_hypertrophy` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_gallbladder_wall_hypertrophy_exterior` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_gallbladder_wall_hypertrophy_interior` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_geographic_liver_background` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_hepatic_blood_duct_narrow_background` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_hepatic_blood_duct_narrow_object` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_hepatic_vein_hypertrophy` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_liver_shrinkage` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_liveredge_blunt` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_liveredge_sharp` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_liverskin_coarse` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_liverskin_smooth` | <5 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `sign_particles_uneven_background` | 0 | 0 | 0 | 0 | 8 | <5 | 0 | 14,123 | 1,257 |
| `skin_tumor` | 0 | 13 | 0 | 0 | 0 | 3,879 | 0 | <5 | 346 |
| `spine` | 39 | 0 | 16 | 0 | 13,583 | 3,888 | 0 | 500 | 1,603 |
| `spleen` | 961 | 0 | 35 | 0 | 12,712 | 7,697 | 0 | 500 | 3,490 |
| `stenosis` | <5 | 0 | 0 | 0 | 42 | 0 | 0 | 11 | <5 |
| `stomach` | 3,562 | 0 | 428 | 0 | 11,032 | 6,383 | 0 | 500 | 3,490 |
| `thyroid` | 10 | 0 | 9 | 0 | 0 | 3,874 | 0 | 0 | 346 |
| `thyroid_cyst` | 19 | 0 | 0 | 0 | 21 | 3,929 | 0 | <5 | 346 |
| `thyroid_tumor` | 57 | 0 | <5 | 0 | 13 | 3,895 | 0 | <5 | 346 |
| `thyroiditis` | 11 | 0 | <5 | 0 | 17 | 3,937 | 0 | <5 | 346 |
| `tumor` | 0 | 47 | 0 | 0 | 0 | 3,845 | 0 | <5 | 346 |
| `ultrasound_area` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 1,257 |
| `uterus` | 411 | 0 | 103 | 0 | 0 | 3,379 | 0 | 0 | 346 |
| `weak_signal_area` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,133 | 1,257 |
| **All labels** | 79,677 | 7,969 | 5,877 | 810 | 406,016 | 268,400 | 220 | 329,348 | 129,662 |

Per-label trade-off. The gains of loose_v1 and posrich_v1 over strict_v1 are concentrated in a few labels. Under loose_v1 and posrich_v1 the five labels with the most added open negatives take 38,552 of the 268,400 open pairs (14%). Under posrich_v1 the five labels with the most `given_contested` positives take 2,746 of the 5,877 (47%), and they add the most to hepatitis (336 to 777 positives) and `hepatic_cirrhosis` (673 to 1,115). Strength: an open negative means no closure was checked (the labeler did not close the label's set), so it is a weaker negative than a closed one; a `given_contested` positive means another labeling task answers `closed` or `open` for the same pair, so it is a positive that another task disputes.

Table 8. The labels with the largest gains over strict_v1 (n = sample-label pairs; no count here is from 1 to 4). Left: open negatives added by loose_v1 and posrich_v1 (strict_v1 has none, Table 5). Right: `given_contested` positives added by posrich_v1 (strict_v1 and loose_v1 have none, Table 6).

| Content label (open negatives) | Negatives strict_v1 | Negatives loose_v1, posrich_v1 | Open added | Content label (contested positives) | Positives strict_v1 | Positives posrich_v1 | Contested added |
|---|---|---|---|---|---|---|---|
| `hepatorenal_contrast_liverbrighter` | 0 | 10,057 | 10,057 | `hepatic_duct` | 8,000 | 9,116 | 1,116 |
| `hepatorenal_contrast_possible` | 0 | 7,776 | 7,776 | `hepatic_cirrhosis` | 673 | 1,115 | 442 |
| `spleen` | 12,712 | 20,409 | 7,697 | `hepatitis` | 336 | 777 | 441 |
| `intestine` | 12,013 | 18,622 | 6,609 | `stomach` | 3,562 | 3,990 | 428 |
| `portal_vein` | 12,712 | 19,125 | 6,413 | `nephritis` | 1,498 | 1,817 | 319 |

## Limitations

- Counts of 1 to 4 are shown as `<5` in every row. This is a display convention, not protection: a `<5` cell can be recovered exactly by subtraction from other numbers of this record, namely Table 4 against Tables 5 to 7 (the positive, negative and unknown sums of a label), the row sums of a label whose pair total is known from the other cells, and the all-labels totals. The reason this is acceptable: the cells are pair counts per content label, aggregates with no rows, file names or identifiers, and the images and tables stay on machine01 ([DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md)). The display is kept so that a small count is not read as a precise one at a glance.
- The sample-label index was built with an earlier fact relations config than the one the policies now read. The policies use only their policy entries (`exclusive_sets`, `implied_tags`, `dropped_rule_items`), and the index is taken as built.
- Counts are pairs, not patients or independent samples: the samples of one datasource or one patient are correlated, and no split is applied here. The per-label counts of different policies describe the same samples and are not independent.
- The `.xlsx` copies are for browsing; the `.pkl` is the source.
- The code that made the per-label counts of this record is a one-off in-memory run of the registered policies; it is not in the repo. The tables themselves come from `sonoai-data sample-label-presence`.

## Conclusion and next steps

The policies are close in their positives (87,615 to 93,523 pairs) and differ in their negatives (406,016 against 674,416) and unknowns (733,538 to 459,230). The trade-off is between the 268,400 open negatives (no closure checked) and the 5,877 contested positives (another labeling task disputes them). Per label (Table 8) the gain is uneven: for example `hepatorenal_contrast_liverbrighter` and `hepatorenal_contrast_possible` have no negative at all under strict_v1 and get 10,057 and 7,776 open ones, and hepatitis more than doubles its positives (336 to 777) with contested ones. Both gains are weaker evidence than the strict_v1 pairs. Which table training reads is a decision for the user.
