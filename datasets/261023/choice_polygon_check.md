# Choice labels and polygon labels on the same image region (261023_plain)

[TASK-061](../../../backlog/tasks/task-061%20-%20Run-choice-check-on-261023_plain-and-write-the-choice-polygon-relation-record-DEC-036.md), [DEC-036](../../decisions/DEC-036-choice-polygon-relation-table.md), [DIS-012](../../discussions/DIS-012-choice-labels-vs-polygon-labels.md). Exploratory. Aggregates only; no
images, file names or identifiers; counts 1-4 are shown as "<5", and a total with
one masked part is shown as "a + <5".

Computed on 2026-11-03 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)) with
`sonoai-data choice-check 261023_plain` from the code repo's `master` at commit
99fa875:

- **Map**: `configs/data/choice_labels.yaml` at commit 197ad1b
  ([TASK-059](../../../backlog/tasks/task-059%20-%20Map-every-261023-choice-label-to-a-role-and-related-polygon-labels-DEC-036.md), merged in f82e0ee; `skip_smallliver` and
  `skip_anatomyunclear` are `exclusion`). A changed map changes this table.
- **Code**: `src/sonoai/data/choice_check.py` and the `choice-check` command at
  commit bb3d26d ([TASK-060](../../../backlog/tasks/task-060%20-%20Choice-polygon-relation-table-library-code-and-sonoai-data-choice-check-DEC-036.md), merged in 99fa875).
- **Written**: the per-region flag table `derived/choice_flags_df.pkl` inside
  `261023_plain` only (31,252 regions; role flags and conflict flags, no images).

Reporting checklists (CLAIM, STARD): not applicable. This is a count of labels:
no model is trained or evaluated, no split is made, no thresholds are chosen.

## Terms

- **Choice label**: a per-image label picked from a list in a labeling project
  (`flags_df` rows with tag type `choice`).
- **Region**: one image file plus its region number (`roi_i`), across all labeling
  projects. It is the unit of every count. The 143,152 crop rows of `taskcrops_df`
  fall on 31,252 regions (one region is labelled by up to several projects).
- **Role** (from the map): `presence` (a finding or organ is in the image; a related
  polygon is expected), `absence` (the related findings are not there), `checked`
  (the labeler looked for the project's polygon labels; no polygon is a true
  negative), `quality` (how good the image is), `exclusion` (what the case is: other
  disease, not liver, no organ), `other`.
- **Related polygon**: a polygon with a label in the map entry (`presence`,
  `absence`); for `checked`, a label its project offered; for `quality`,
  `exclusion` and `other`, any polygon. Polygons from every project on the region
  count.
- **Not checkable** (`presence` only): no project that labeled the region offered a
  related polygon label, so a missing polygon says nothing. Left out of the share
  and the conflicts.
- **Conflict**: `presence` on a checkable region with no related polygon; `absence`
  with a related polygon.
- **Same-project share**: share of regions whose related polygon came from a project
  that also gave the choice.

## Method

- Choices and polygons were joined to `taskcrops_df` by task. Pairs whose task
  has no crop row cannot be placed on a region and were left out (Data coverage,
  below).
- Shares: regions with a related polygon / regions (checkable regions for
  `presence`). Two 95% CIs: the Wilson score interval (Wilson 1927,
  [doi:10.1080/01621459.1927.10502953](https://doi.org/10.1080/01621459.1927.10502953); treats regions as independent), and a
  datasource cluster bootstrap (4,000 resamples of the 72 datasources with
  replacement, seed 61, percentile interval; resamples with no region of the label
  dropped). Regions never span datasources, so the per-datasource counts sum
  exactly to the totals (checked: 0 labels differ). For a label in fewer than 5
  datasources the bootstrap has too few distinct resamples to be meaningful (it can
  look exact, e.g. 35.0-35.0 for one datasource); Table 1 shows "n/a" there. A
  share of 0 in every datasource gives a bootstrap interval of 0.0-0.0 by
  construction.
- Masking (code of TASK-060): a share and its CIs are blank when the numerator or
  its complement is 1-4, or n is below 5.

## Data coverage

- 225,016 choice task-label pairs (129,760 tasks); 172,699 placed. **52,317 pairs
  (23.3%) on 23,845 tasks were left out: every choice task of 6 labeling projects
  (projects 1, 4, 9, 11, 30, 49) has no crop row.** By role of the left-out pairs:
  presence 28,217, exclusion 7,308, other 7,009, quality 6,206, checked 2,844,
  absence 733.
- 109,276 polygon task-label pairs (53,473 tasks); 92,213 placed; 17,063 (15.6%)
  on 11,704 tasks left out (the known gap of `plain.md`, also in
  [bmode_crop_check.md](bmode_crop_check.md)).
- 116 of the map's 146 choice labels occur on a placed region; 0 used labels are
  missing from the map.

## Results

Table 1. Each choice label of 261023_plain and the polygon labels on the same
image region, one row per choice label used on a placed region (n = 116), grouped
by role. Regions: regions with the choice (n per row). Related polygon labels: the
map's list (shown when 3 or fewer; "N labels (map)" otherwise), the labels offered
by the choice's project (`checked`), or any polygon (`quality`, `exclusion`,
`other`; for these the share is the share that still got polygons). Share: regions
with a related polygon / regions (checkable regions for `presence`), with the 95%
Wilson confidence interval (CI); next column: 95% datasource cluster-bootstrap CI
(4,000 resamples; "n/a" for labels in fewer than 5 datasources, where it is not
meaningful; 0.0-0.0 where no datasource has a related polygon).
Same-project share: see Terms. Conflicts: `presence` without a related polygon,
`absence` with one. "<5": a count of 1-4; "a + <5": a total with one masked part;
blank share: numerator or complement below 5 (or n below 5).

| Choice label | Role | Related polygon labels | Regions, n | Datasources, n | Labeling projects, n | Not checkable, n | With a related polygon, n | Share with a related polygon, % (95% CI Wilson) | 95% CI datasource bootstrap, % | Same-project share, % | Conflicts, n |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|---:|
| `ascites` | presence | 4 labels (map) | 60 | <5 | <5 | 0 | 31 | 51.7% (39.3-63.8) | n/a | 0.0% | 29 |
| `bladder` | presence | `bladder` | 466 | <5 | <5 | 0 | 425 | 91.2% (88.3-93.4) | n/a | 0.0% | 41 |
| `breast_tumor` | presence | `breast_tumor` | <5 | <5 | <5 | <5 | 0 |  |  |  | 0 |
| `bursitis` | presence | `bursitis` | 157 | <5 | <5 | 0 | 124 | 79.0% (72.0-84.6) | n/a | 0.0% | 33 |
| `cholecystitis` | presence | `cholecystitis` | 247 | <5 | <5 | 0 | 216 | 87.4% (82.7-91.0) | n/a | 0.0% | 31 |
| `common_biliary_duct` | presence | `common_biliary_duct` | 78 | <5 | <5 | 78 | 0 |  |  |  | 0 |
| `cyst` | presence | `cyst` | 35 | <5 | <5 | 35 | 0 |  |  |  | 0 |
| `cystitis` | presence | `cystitis` | 241 | <5 | <5 | 0 | 213 | 88.4% (83.7-91.8) | n/a | 0.0% | 28 |
| `cystolithiasis` | presence | `cystolithiasis` | 19 | <5 | <5 | 0 | 13 | 68.4% (46.0-84.6) | n/a | 0.0% | 6 |
| `gallbladder` | presence | `gallbladder` | 933 | <5 | <5 | 0 | 838 | 89.8% (87.7-91.6) | n/a | 0.0% | 95 |
| `gallbladder_contracted` | presence | `gallbladder_contracted`, `gallbladder` | 161 | <5 | <5 | 0 | 150 | 93.2% (88.2-96.1) | n/a | 0.0% | 11 |
| `gallbladder_deformed` | presence | `gallbladder` | 200 | <5 | <5 | 0 | 193 | 96.5% (93.0-98.3) | n/a | 0.0% | 7 |
| `gallbladder_dilated` | presence | `gallbladder_dilated`, `gallbladder` | 28 + <5 | <5 | <5 | 0 | 28 |  |  | 0.0% | <5 |
| `gallbladder_normalsized` | presence | `gallbladder_normalsized`, `gallbladder` | 176 + <5 | <5 | <5 | 0 | 176 |  |  | 0.0% | <5 |
| `gallbladder_polyp` | presence | `gallbladder_polyp` | 52 | <5 | <5 | 0 | 34 | 65.4% (51.8-76.8) | n/a | 0.0% | 18 |
| `gallbladder_stone` | presence | `gallbladder_stone` | 188 | <5 | <5 | 0 | 177 | 94.1% (89.8-96.7) | n/a | 0.0% | 11 |
| `gallbladder_tumor` | presence | `gallbladder_tumor` | 12 + <5 | <5 | <5 | 0 | <5 |  |  | 0.0% | 12 |
| `gastric_tumor` | presence | `gastric_tumor` | 41 + <5 | 5 | <5 | 0 | 41 |  |  |  | <5 |
| `heart` | presence | `heart` | 24 + <5 | <5 | <5 | 0 | 24 |  |  | 0.0% | <5 |
| `hemangioma` | presence | `hemangioma` | 207 | 7 | <5 | 0 | 166 | 80.2% (74.2-85.1) | 49.0-98.9 | 37.2% | 41 |
| `hepatic_blood_duct` | presence | `hepatic_blood_duct` | 1539 | <5 | <5 | 1539 | 0 |  |  |  | 0 |
| `hepatic_cirrhosis` | presence | `hepatic_cirrhosis` | 1078 | 14 | <5 | 0 | 1027 | 95.3% (93.8-96.4) | 85.8-99.3 | 67.2% | 51 |
| `hepatic_cyst` | presence | `hepatic_cyst` | 104 | 8 | <5 | 0 | 95 | 91.3% (84.4-95.4) | 76.9-100.0 | 56.7% | 9 |
| `hepatic_duct` | presence | `hepatic_duct` | 2043 | <5 | <5 | 0 | 974 | 47.7% (45.5-49.8) | n/a | 0.0% | 1069 |
| `hepatic_steatosis__0` | presence | `hepatic_steatosis__0` | 960 | 15 | <5 | 0 | 491 | 51.1% (48.0-54.3) | 25.7-78.2 | 27.6% | 469 |
| `hepatic_steatosis__1` | presence | `hepatic_steatosis__1` | 3741 | 15 | <5 | 0 | 2627 | 70.2% (68.7-71.7) | 48.2-91.1 | 62.4% | 1114 |
| `hepatic_steatosis__2` | presence | `hepatic_steatosis__2` | 1401 | 15 | <5 | 0 | 955 | 68.2% (65.7-70.6) | 26.7-95.3 | 64.3% | 446 |
| `hepatic_steatosis__3` | presence | `hepatic_steatosis__3` | 109 | 11 | <5 | 0 | 93 | 85.3% (77.5-90.8) | 66.9-93.2 | 74.3% | 16 |
| `hepatitis` | presence | `hepatitis` | 376 | <5 | <5 | 0 | 37 | 9.8% (7.2-13.3) | n/a | 0.0% | 339 |
| `hepatoma` | presence | `hepatoma` | 1138 | 13 | <5 | 0 | 1113 | 97.8% (96.8-98.5) | 93.8-99.7 | 69.9% | 25 |
| `herniated_disk` | presence | `herniated_disk` | 21 + <5 | <5 | <5 | 0 | 21 |  |  | 0.0% | <5 |
| `hydronephrosis` | presence | `hydronephrosis` | 21 | <5 | <5 | 0 | 16 | 76.2% (54.9-89.4) | n/a | 0.0% | 5 |
| `kidney` | presence | `kidney` | 737 | <5 | <5 | 0 | 685 | 92.9% (90.9-94.6) | n/a | 0.0% | 52 |
| `knee` | presence | `knee` | 163 | <5 | <5 | 0 | 125 | 76.7% (69.6-82.5) | n/a | 0.0% | 38 |
| `liver` | presence | `liver` | 2190 | <5 | <5 | 0 | 2162 | 98.7% (98.2-99.1) | n/a | 0.0% | 28 |
| `liver_ascites` | presence | 4 labels (map) | 40 | <5 | <5 | 0 | 21 | 52.5% (37.5-67.1) | n/a | 0.0% | 19 |
| `lung` | presence | `lung` | 8 + <5 | <5 | <5 | 0 | <5 |  |  | 0.0% | 8 |
| `myoma_uterus` | presence | `myoma_uterus` | 105 | <5 | <5 | 0 | 79 | 75.2% (66.2-82.5) | n/a | 0.0% | 26 |
| `myoma_uterus_or_adenomyosis` | presence | `myoma_uterus`, `adenoma_uterus` | 105 | <5 | <5 | 0 | 83 | 79.0% (70.3-85.7) | n/a | 0.0% | 22 |
| `nephritis` | presence | `nephritis` | 127 | <5 | <5 | 0 | 113 | 89.0% (82.3-93.3) | n/a | 0.0% | 14 |
| `nephrocystosis` | presence | `nephrocystosis` | 16 | <5 | <5 | 0 | 10 | 62.5% (38.6-81.5) | n/a | 0.0% | 6 |
| `ovarian_cyst` | presence | `ovarian_cyst` | 48 | <5 | <5 | 0 | 39 | 81.2% (68.1-89.8) | n/a | 0.0% | 9 |
| `ovarian_follicle` | presence | `ovarian_follicle` | 36 | <5 | <5 | 0 | 23 | 63.9% (47.6-77.5) | n/a | 0.0% | 13 |
| `pancreatin` | presence | `pancreatin` | 123 | <5 | <5 | 0 | 58 | 47.2% (38.6-55.9) | n/a | 0.0% | 65 |
| `parasite` | presence | `parasite` | 11 | <5 | <5 | 11 | 0 |  |  |  | 0 |
| `pleuritis` | presence | `pleuritis` | 9 + <5 | <5 | <5 | 0 | 9 |  |  | 0.0% | <5 |
| `pregnancy` | presence | `pregnancy` | 25 + <5 | <5 | <5 | 0 | 25 |  |  | 0.0% | <5 |
| `prostate` | presence | `prostate`, `prostate_gland` | 106 | <5 | <5 | 0 | 82 | 77.4% (68.5-84.3) | n/a | 0.0% | 24 |
| `prostate_cyst` | presence | `prostate_cyst` | <5 | <5 | <5 | 0 | <5 |  |  |  | <5 |
| `prostate_stone` | presence | `prostate_stone` | 41 + <5 | <5 | <5 | 0 | 41 |  |  | 0.0% | <5 |
| `prostatis` | presence | `prostatitis` | 5 + <5 | <5 | <5 | 0 | 5 |  |  | 0.0% | <5 |
| `prostatomegaly` | presence | `prostate`, `prostate_gland` | 5 | <5 | <5 | 0 | <5 |  |  | 0.0% | <5 |
| `renal_calculus` | presence | `renal_calculus` | 56 | <5 | <5 | 0 | 48 | 85.7% (74.3-92.6) | n/a | 0.0% | 8 |
| `renal_carcinoma` | presence | `renal_carcinoma` | 7 | <5 | <5 | 0 | <5 |  |  | 0.0% | <5 |
| `skin_tumor` | presence | `skin_tumor` | 18 | <5 | <5 | 18 | 0 |  |  |  | 0 |
| `spine` | presence | `spine` | 39 + <5 | <5 | <5 | 0 | 39 |  |  | 0.0% | <5 |
| `spleen` | presence | `spleen` | 106 | <5 | <5 | 0 | 79 | 74.5% (65.5-81.9) | n/a | 0.0% | 27 |
| `stomach` | presence | `stomach` | 105 | <5 | <5 | 0 | 78 | 74.3% (65.2-81.7) | n/a | 0.0% | 27 |
| `thyroid` | presence | `thyroid` | 10 + <5 | <5 | <5 | 0 | 10 |  |  | 0.0% | <5 |
| `thyroid_cyst` | presence | `thyroid_cyst` | <5 | <5 | <5 | 0 | <5 |  |  |  | 0 |
| `thyroid_tumor` | presence | `thyroid_tumor` | 5 | <5 | <5 | 0 | 5 | 100.0% (56.6-100.0) | n/a | 0.0% | 0 |
| `thyroiditis` | presence | `thyroiditis` | <5 | <5 | <5 | 0 | <5 |  |  |  | <5 |
| `tumor` | presence | `tumor` | 71 | <5 | <5 | 71 | 0 |  |  |  | 0 |
| `uterus` | presence | `uterus` | 472 | <5 | <5 | 0 | 413 | 87.5% (84.2-90.2) | n/a | 0.0% | 59 |
| `anatomy_absent` | absence | 17 labels (map) | <5 | <5 | <5 |  | <5 |  |  |  | <5 |
| `bladder_nodisease` | absence | `cystitis`, `cystolithiasis`, `bladder_tumor` | 84 | <5 | <5 |  | 0 | 0.0% (0.0-4.4) | n/a | 0.0% | 0 |
| `breast_disease_no` | absence | `breast_tumor`, `breast_abscess`, `breast_cyst` | 283 | 7 | <5 |  | <5 |  |  |  | <5 |
| `cholecystitis_absent` | absence | `cholecystitis` | 819 | 26 | <5 |  | 0 | 0.0% (0.0-0.5) | 0.0-0.0 | 0.0% | 0 |
| `disk_nodisease` | absence | `herniated_disk`, `stenosis`, `ligamenta_flava_hypertrophy` | 7 | <5 | <5 |  | 0 | 0.0% (0.0-35.4) | n/a | 0.0% | 0 |
| `gallbladder_polyp_absent` | absence | `gallbladder_polyp` | 2676 | 35 | <5 |  | <5 |  |  |  | <5 |
| `gallbladder_stone_absent` | absence | `gallbladder_stone` | 834 | 10 | <5 |  | <5 |  |  | 0.0% | <5 |
| `gallbladder_tumor_absent` | absence | `gallbladder_tumor` | 2224 | 36 | <5 |  | <5 |  |  |  | <5 |
| `heaptic_steatosis_absent` | absence | 5 labels (map) | 5 + <5 | <5 | <5 |  | 5 |  |  |  | 5 |
| `hydronephrosis_absent` | absence | `hydronephrosis` | 9179 | 46 | <5 |  | <5 |  |  |  | <5 |
| `kidney_nodisease` | absence | 5 labels (map) | 294 | <5 | <5 |  | 0 | 0.0% (0.0-1.3) | n/a | 0.0% | 0 |
| `nephritis_absent` | absence | `nephritis` | 8218 | 42 | <5 |  | <5 |  |  |  | <5 |
| `nephrocystosis_absent` | absence | `nephrocystosis` | 10094 | 46 | <5 |  | <5 |  |  |  | <5 |
| `no_hepatic_stone` | absence | `hepatic_stone` | 13613 | 52 | <5 |  | 0 | 0.0% (0.0-0.0) | 0.0-0.0 | 0.0% | 0 |
| `notfound` | absence | 7 labels (map) | 3494 | 11 | <5 |  | 12 | 0.3% (0.2-0.6) | 0.0-0.6 | 0.1% | 12 |
| `prostate_nodisease` | absence | 5 labels (map) | 33 | <5 | <5 |  | 0 | 0.0% (0.0-10.4) | n/a | 0.0% | 0 |
| `renal_calculus_absent` | absence | `renal_calculus` | 8586 | 46 | <5 |  | <5 |  |  |  | <5 |
| `renal_carcinoma_absent` | absence | `renal_carcinoma` | 10295 | 46 | <5 |  | <5 |  |  |  | <5 |
| `signs_absent` | absence | 16 labels (map) | <5 | <5 | <5 |  | 0 |  |  |  | 0 |
| `thyroid_nodisease` | absence | `thyroiditis`, `thyroid_tumor`, `thyroid_cyst` | 5 | <5 | <5 |  | 0 | 0.0% (0.0-43.4) | n/a | 0.0% | 0 |
| `thyroiditis_abscent` | absence | `thyroiditis`, `thyroid_tumor`, `thyroid_cyst` | 5 | <5 | <5 |  | 0 | 0.0% (0.0-43.4) | n/a | 0.0% | 0 |
| `uterus_nodisease` | absence | 5 labels (map) | 89 | <5 | <5 |  | 0 | 0.0% (0.0-4.1) | n/a | 0.0% | 0 |
| `ai_almost` | checked | offered by its project | 333 | <5 | <5 |  | 333 | 100.0% (98.9-100.0) | n/a | 100.0% |  |
| `ai_correct` | checked | offered by its project | 1669 | <5 | <5 |  | 1669 | 100.0% (99.8-100.0) | n/a | 100.0% |  |
| `anatomy_checked` | checked | offered by its project | 14508 | 45 | <5 |  | 14503 | 100.0% (99.9-100.0) | 99.9-100.0 | 100.0% |  |
| `changed` | checked | offered by its project | 1932 | <5 | <5 |  | 1922 | 99.5% (99.0-99.7) | n/a | 99.5% |  |
| `checked` | checked | offered by its project | 17384 | 56 | 13 |  | 4744 | 27.3% (26.6-28.0) | 10.5-48.6 | 27.3% |  |
| `hepatic_steatosis_checked` | checked | offered by its project | 9906 + <5 | 42 | <5 |  | 9906 |  |  |  |  |
| `signal_regions_checked` | checked | offered by its project | <5 | <5 | <5 |  | 0 |  |  |  |  |
| `signs_checked` | checked | offered by its project | 8 | <5 | <5 |  | 8 | 100.0% (67.6-100.0) | n/a | 100.0% |  |
| `skip_badimagequality` | quality | any polygon | 1116 | 42 | 18 |  | 1071 | 96.0% (94.6-97.0) | 85.9-99.1 | 0.0% |  |
| `skip_blurred` | quality | any polygon | <5 | <5 | <5 |  | <5 |  |  |  |  |
| `skip_coarse` | quality | any polygon | 511 | <5 | <5 |  | 179 | 35.0% (31.0-39.3) | n/a | 35.0% |  |
| `skip_lowdim` | quality | any polygon | 1387 | 9 | <5 |  | 1248 | 90.0% (88.3-91.4) | 76.5-91.5 | 89.8% |  |
| `skip_paperscan` | quality | any polygon | <5 | <5 | <5 |  | 0 |  |  |  |  |
| `skip_toomanyannotations` | quality | any polygon | <5 | <5 | <5 |  | <5 |  |  |  |  |
| `skip_anatomyunclear` | exclusion | any polygon | 1561 | 13 | <5 |  | 1215 | 77.8% (75.7-79.8) | 21.1-89.9 | 74.7% |  |
| `skip_no_organ_found` | exclusion | any polygon | 592 | 17 | 12 |  | 573 | 96.8% (95.0-97.9) | 95.3-99.3 |  |  |
| `skip_notabdomen` | exclusion | any polygon | 276 | <5 | <5 |  | <5 |  |  |  |  |
| `skip_notliver` | exclusion | any polygon | 287 | 7 | <5 |  | 13 | 4.5% (2.7-7.6) | 1.4-11.8 | 0.0% |  |
| `skip_notultrasound` | exclusion | any polygon | 287 | 8 | <5 |  | 24 | 8.4% (5.7-12.1) | 5.7-24.1 | 5.2% |  |
| `skip_othercase` | exclusion | any polygon | <5 | <5 | <5 |  | <5 |  |  |  |  |
| `skip_otherdisease` | exclusion | any polygon | 730 | 10 | <5 |  | 730 | 100.0% (99.5-100.0) | 100.0-100.0 | 100.0% |  |
| `skip_smallliver` | exclusion | any polygon | 145 | 7 | <5 |  | 138 | 95.2% (90.4-97.6) | 92.2-100.0 | 89.0% |  |
| `cannotdiag` | other | any polygon | 1238 | 6 | <5 |  | 1151 | 93.0% (91.4-94.3) | 90.4-100.0 | 1.0% |  |
| `has_other_anatomy` | other | any polygon | 171 | <5 | <5 |  | 76 | 44.4% (37.2-51.9) | n/a | 0.0% |  |
| `has_other_disease` | other | any polygon | 142 | <5 | <5 |  | 97 | 68.3% (60.3-75.4) | n/a | 0.0% |  |
| `hepatic_steatosis__unknown` | other | any polygon | 2471 | 10 | <5 |  | 2081 | 84.2% (82.7-85.6) | 78.1-97.3 | 36.0% |  |
| `hepatorenal_contrast_liverbrighter` | other | any polygon | 2313 | 26 | <5 |  | 1987 | 85.9% (84.4-87.3) | 53.0-100.0 | 85.9% |  |
| `hepatorenal_contrast_possible` | other | any polygon | 4776 | 31 | <5 |  | 4441 | 93.0% (92.2-93.7) | 70.5-100.0 | 93.0% |  |
| `imagequality_checked` | other | any polygon | 13169 | 46 | <5 |  | 12337 | 93.7% (93.3-94.1) | 86.7-100.0 | 93.7% |  |
| `skip_untouched` | other | any polygon | 223 | <5 | <5 |  | 0 | 0.0% (0.0-1.7) | n/a | 0.0% |  |

Table 2. Region-level summary from the flag table (n = 31,252 regions in 72
datasources). Each block starts with a group of regions ("Regions", its size n)
and gives subsets of that group ("Of which", n and % of the group). A region may
carry several roles, so the groups overlap. CI: 95% confidence interval, Wilson
score and datasource cluster bootstrap (4,000 resamples of the datasources that
hold the group, seed 61, percentile).

| Regions | n (datasources) | Of which | n (%) | 95% CI Wilson, % | 95% CI datasource bootstrap, % |
|---|---:|---|---|---|---|
| All regions | 31,252 (72) | with any choice | 26,646 (85.3%) | 84.9-85.7 | 75.4-92.2 |
| | | with any polygon | 26,807 (85.8%) | 85.4-86.2 | 79.0-91.7 |
| With a `presence` choice | 9,420 (15) | with at least one presence conflict | 3,355 (35.6%) | 34.7-36.6 | 15.8-53.3 |
| | | with a not checkable presence choice | 1,727 (18.3%) | 17.6-19.1 | 4.3-32.2 |
| With an `absence` choice | 20,581 (67) | with at least one absence conflict | 37 (0.2%) | 0.1-0.2 | 0.1-0.3 |
| With a `quality` choice | 2,989 (42) | with any polygon | 2,472 (82.7%) | 81.3-84.0 | 60.5-95.9 |
| With an `exclusion` choice | 3,525 (25) | with any polygon | 2,641 (74.9%) | 73.5-76.3 | 55.8-87.1 |
| With a `quality` or `exclusion` choice | 5,066 (45) | with any polygon | 3,805 (75.1%) | 73.9-76.3 | 59.9-87.7 |

### Largest conflicts and surprises

1. **A quarter of choice labels cannot be placed.** 52,317 of 225,016 choice
   task-label pairs (23.3%) belong to 6 labeling projects with no crop row in
   `taskcrops_df`, among them the steatosis scoring project 1 (5,913 tasks) and the
   organ and disease project 49 (10,948 tasks). They are missing from Table 1, so
   the table describes only the projects that have crops.
2. **Presence conflicts concentrate in five liver labels.** 3,355 of 9,420 regions
   with a presence choice have at least one conflict (35.6%; CIs in Table 2). The
   largest (shares and CIs in their Table 1 rows):
   `hepatic_steatosis__1` 1,114 of 3,741 checkable regions (29.8%),
   `hepatic_duct` 1,069 of 2,043 (52.3%), `hepatic_steatosis__0` 469 of 960
   (48.9%), `hepatic_steatosis__2` 446 of 1,401 (31.8%), `hepatitis` 339 of 376
   (90.2%).
   - Exploratory sensitivity check (map widened in memory only, not committed):
     counting any steatosis polygon (any grade, `__ignore`, `__unknown`) as related,
     the share with a polygon rose from 51.1% to 65.4% (grade 0), 70.2% to 77.1%
     (grade 1), 68.2% to 72.5% (grade 2) and 85.3% to 88.1% (grade 3). So 256 of
     3,741 grade-1 regions carry a polygon of another grade only, and 332 of 960
     grade-0 regions carry no steatosis polygon at all.
   - `hepatitis`: with hepatitis, cirrhosis, precirrhosis or steatosis polygons
     counted, 368 of 376 regions (97.9%) have one. Hepatitis choices are mostly
     drawn as other diffuse polygons, not as hepatitis polygons.
   - `hepatic_duct`: with any duct or vessel polygon (`hepatic_blood_duct`,
     `portal_vein`, `hepatic_vascular_branch`, `common_biliary_duct`) counted,
     66.2% (1,352 of 2,043) have one.
3. **Absence choices agree with the polygons.** 37 of 20,581 regions (0.2%, 95%
   CI 0.1-0.2 Wilson, 0.1-0.3 datasource bootstrap; Table 2) with an absence choice
   have a related polygon; the most are `notfound` (12 of 3,494,
   0.3%) and `heaptic_steatosis_absent` (5 of 5 + <5).
4. **Organ choices are confirmed only by other projects.** For every organ label
   among the presence choices (not the disease labels) the same-project share is
   0.0%: the projects that give them draw no polygons, so all agreement comes from
   other projects on the same region. Liver disease choices differ (e.g.
   `hemangioma` 37.2%, `hepatic_cirrhosis` 67.2%; Table 1).
5. **Some presence choices cannot be checked at all.** `hepatic_blood_duct` (1,539
   regions), `common_biliary_duct` (78), `tumor` (71), `cyst` (35), `skin_tumor` (18)
   and `parasite` (11): no project that labeled these regions offered the polygon
   label.
6. **Quality and exclusion choices mostly still have polygons.** 3,805 of 5,066
   regions (75.1%; CIs in Table 2) with a quality or exclusion choice carry a
   polygon (shares and CIs per label in Table 1):
   `skip_badimagequality` 96.0%, `skip_lowdim` 90.0%, `skip_otherdisease` 100.0%,
   `skip_no_organ_found` 96.8%, `skip_smallliver` 95.2%, `skip_anatomyunclear`
   77.8%. Mostly without polygons: `skip_notliver` (13 of 287, 4.5%),
   `skip_notultrasound` (24 of 287, 8.4%), `skip_notabdomen` (<5 of 276 regions
   with a polygon) and the quality label `skip_coarse` (179 of 511, 35.0%; one
   datasource, same-project share 35.0%). For
   `skip_badimagequality` the polygons come from other projects (same-project
   share 0.0%); for `skip_lowdim` and `skip_otherdisease` from the same project.
   Leaving out quality or exclusion regions therefore removes polygon-labelled
   training data ([TASK-062](../../../backlog/tasks/task-062%20-%20Decide-the-rule-for-leaving-out-quality-and-case-exclusion-crops-from-train-val-test-DIS-012.md)).
7. **The generic `checked` mark is mostly a negative.** Of 17,384 regions (56
   datasources) only 27.3% (95% CI 26.6-28.0 Wilson, 10.5-48.6 datasource bootstrap) carry a polygon
   the project offered; the rest are reviewed images without findings.

## Limitations

- Regions of one datasource are not independent (device, site, labelers). The
  Wilson intervals are too narrow for that reason; the bootstrap intervals are wide
  where one datasource holds most of a label's regions, and not meaningful with
  fewer than 5 datasources (shown as "n/a" in Table 1). The presence rows of
  Table 2 rest on 15 datasources only.
- Counts are of regions, not patients; the dataset has no patient key.
- The 6 projects without crop rows (23.3% of choice pairs) are not in the table.
- Conflicts depend on the map: a narrow related-polygon list (steatosis grades,
  `hepatitis`, `hepatic_duct`) raises the conflict count, as the sensitivity check
  shows. The map was not changed here.
- Polygons are counted by label only; whether a polygon outlines the same finding
  as the choice was not checked.
