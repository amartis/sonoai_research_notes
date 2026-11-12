# Quality-assurance measures in the labeling projects of dataset version 261023

Asked by the user on 2026-11-11 (no board task). Related:
[DIS-012](../../discussions/DIS-012-choice-labels-vs-polygon-labels.md) (choice labels as a double check of polygon labels),
[DEC-036](../../decisions/DEC-036-choice-polygon-relation-table.md) (choice-polygon relation table),
[choice_polygon_check.md](choice_polygon_check.md) (the region-level record this report builds on),
[labels-261023.md](../../../docs/labels-261023.md) (every label and project).
Exploratory. Aggregates only; no images, file names or identifiers; counts 1-4 are
shown as "<5". Not committed and not reviewed yet.

**Amended 2026-11-11** after the user's review: the measures are grouped into five
categories with their own codes (C1 skip-sample, C2 skip-part, C3 visited check,
C4 double conformance, C5 other), and some options move between measures A1-A5. No
count changed. See [Amendments](#amendments).

**Quality-assurance (QA) measure** here means: something built into a labeling project
so that a human labeling error can be noticed.

## Summary

1. **Ten kinds of QA measure were found** (Table 2). Seven work inside one task and are
   statements by the labeler: an explicit "absent" answer, a "checked" mark, a skip
   reason, a "cannot decide" option, a second entry of the same fact, a verdict on an AI
   draft, and a free-text note. Three work between projects: one finding per project,
   staged routing (organ first, findings second), and a second pass over the same images
   by another project.
2. **The in-task measures were used widely and are consistent inside a task.** 71,551
   tasks carry an "absent" answer and 37,282 a "checked" mark (of 151,017 tasks with any
   mark). An "absent" answer and a polygon of the same finding sit on the same task in
   28 of 71,058 cases (0.04%). In project 7 the image-level steatosis grade equals the
   highest polygon grade in 3,572 of 3,596 tasks (99.3%, 95% CI 99.0-99.6).
3. **These measures show omissions and slips, not wrong judgments.** Where two passes
   on the same image exist, agreement is much lower: positive agreement 0.806 for organs
   (project 35 choices against project 33 polygons, n = 3,925 regions) and 0.573 for
   diseases (project 35 choices against the polygons of projects 36-47). Steatosis
   grades match in 576 of 995 regions (57.9%, 54.8-60.9).
4. **The disagreements have a direction.** The polygon pass graded steatosis higher than
   the choice pass in 396 regions and lower in 23. It drew cirrhosis, nephritis, cystitis
   and cholecystitis far more often than the choice pass chose them; the choice pass chose
   hepatic duct and hepatitis far more often than the polygon pass drew them. This points
   to different working definitions between passes, not only to random slips.
5. **Not in the data:** a second annotation of the same task, the labeler's identity,
   time stamps, a review or accept/reject status, known-answer test tasks, and any record
   of how a disagreement was settled. Every task has exactly one annotation.
6. **The four sheets agree with each other** (Table 1): same 621 options in the
   project-labels sheet and the flags table; polygon counts equal in all 109,276
   task-label cells; one annotation id per task in both label tables.

## Terms

- **Task**: one image crop shown to a labeler in one project (`task_id`). **Mark**: any
  option of a task with a count above 0 (a choice, a polygon or a text note).
- **Region**: one image file plus its region number, across projects (as in
  [choice_polygon_check.md](choice_polygon_check.md)); 31,252 regions.
- **Pass**: one project's labeling of a region. Two passes on one region are the only
  place where two human judgments can be compared.
- **Role** of a choice label (`checked`, `absence`, `quality`, `exclusion`, `presence`,
  `other`): from the map [choice_labels.yaml](../../../configs/data/choice_labels.yaml)
  (DEC-036). The three AI verdict labels of project 33 are counted apart here.
- **Kappa**: Cohen's kappa, agreement of two yes/no labelings beyond chance (1 = perfect,
  0 = chance level). **Positive agreement**: 2 x both / (2 x both + only first + only
  second), over label-region pairs; it ignores the many pairs where both say "no".
- **IoU**: intersection over union of two filled outlines (1 = identical).

## Data and method

Tables read on machine01 on 2026-11-11, in memory, read only (user's ok, DEC-052):
`flags_df` (5,559,898 rows: one row per task and offered option, with a count),
`polygons_df` (984,908 points of 129,815 polygons) and `taskcrops_df` (143,152 crop
rows) of `261023_plain`, and the project-labels sheet (`project_labels_df`, plain copy;
633 rows, 38 projects), which is kept outside the dataset folder.

- Steps: (1) compared the sheets with each other; (2) listed the QA-type options per
  project from the project-labels sheet; (3) counted their use per project from
  `flags_df`; (4) checked contradictions inside a task; (5) placed tasks on regions with
  `taskcrops_df` and compared passes of different projects on the same region; (6)
  compared the two labelings of images that occur twice inside one project.
- 95% confidence intervals (CI): Wilson score interval for shares (as in
  choice_polygon_check.md); percentile bootstrap over regions (2,000 resamples, seed 0)
  for kappa. Both treat tasks or regions as independent, which they are not (regions of
  one datasource are alike), so the intervals are too narrow. A datasource bootstrap is
  not meaningful for projects 33-47: they rest on 4 datasources.
- IoU: outlines were filled on a 256 x 256 grid from the polygon coordinates. No image
  was opened.
- Code: one-off scripts, not in the repo (see Limitations).

## Results

### 1. The sheets agree with each other

Table 1. Checks between the four sheets of 261023 (computed 2026-11-11).

| Check | Result |
|---|---|
| Options (project, tag type, tag group, label) in the project-labels sheet and in `flags_df` | 621 in each; 0 in only one |
| Rows per task in `flags_df` = options of the project in the sheet | 37 of 38 projects; project 35 has 70 rows per task against 68 in the sheet (two uterus options appear twice, and each choice is then counted twice: 300 rows with count 2) |
| Options listed more than once in a project (same decoded name) | 5 polygon options in projects 2, 14, 19, 38, 52 (e.g. `kidney` 6 times in project 2); their counts must be summed |
| Polygon count per task and label, `flags_df` against `polygons_df` | 109,276 cells in both tables, 0 in only one; equal in all 109,276 once repeated options are summed |
| Annotation id | Present on all 346,028 rows with a count above 0 and on no other row; exactly 1 annotation per task (151,017 tasks) and 1 task per annotation; same id in `polygons_df` for all 53,473 polygon tasks |
| Tasks in `flags_df` and `taskcrops_df` | All 143,152 crop rows are tasks of `flags_df` with the same project; 58,121 tasks of 8 projects (1, 3, 4, 9, 11, 30, 49, 52) have no crop row |
| Task status in `taskcrops_df` against marks | `annotated` 120,839 (1,914 of them without any mark), `empty` 22,303 (none has a mark), `draft` 10 |
| Polygon structure | 8 of 129,815 polygons have fewer than 3 points; 14 are not closed; 682 (0.5%) have a coordinate outside 0-100; 0 exact duplicates inside a task |

### 2. The QA measures found

Table 2. QA measures built into the 38 labeling projects of 261023, with their use and
what the comparison of the sheets showed. Tasks = tasks with at least one such mark, of
151,017 tasks with any mark (201,273 tasks in all). Amendment 1 groups these measures into
categories C1-C5 (Table 9) and revises rows A1-A5 (Table 11).

| # | Measure | How it can reveal an error | Projects that offer it | Tasks that used it | What the sheets show |
|---|---|---|---|---:|---|
| A1 | Explicit "absent" answer (`..._absent`, `..._nodisease`, `notfound`, `no_hepatic_stone`) | An empty task no longer looks like a negative; an unanswered task stands out | 24 (7, 14, 15, 19-24, 26-32, 37, 39, 42, 43, 45, 46, 49, 50) | 71,551 | In the kidney projects 20-24 only 37 of 52,240 tasks have no answer. Same-task conflict with a related polygon: 28 of 71,058 (0.04%) |
| A2 | "Checked" mark (`checked`, `anatomy_checked`, `hepatic_steatosis_checked`, `signs_checked`, `signal_regions_checked`, `imagequality_checked`) | The labeler states that a group of labels was looked at, so missing polygons are meant | 15 (7, 9, 14, 36-39, 41-47, 50) | 37,282 (without `imagequality_checked`, which has role `other` in the map: 13,169 tasks of project 14) | Project 14: 14,503 of 14,553 tasks with anatomy polygons carry the mark (99.7%). The mark is optional: 1,866 submitted tasks of project 14 have no mark at all |
| A3 | Skip reason: image quality (`skip_lowdim`, `skip_badimagequality`, ...) or case exclusion (`skip_notliver`, `skip_no_organ_found`, ...) | Unusable or out-of-scope images are named instead of left empty | 36 (all but 19 and 52) | 8,358 quality; 11,193 exclusion | Not a stable property of the image: on the same 10,448 regions, project 21 set `skip_badimagequality` on 819 and each of the other four kidney projects on at most 10 |
| A4 | "Cannot decide" option (`hepatic_steatosis__unknown`, `cannotdiag`, `skip_anatomyunclear`, polygon `hepatic_steatosis__ignore`) | Doubt is recorded instead of a forced guess | 1, 2, 3, 7, 9, 11, 14, 33 | e.g. `cannotdiag` 1,239; `unknown` 2,472 in project 7 | Meaning is unclear in project 7: `unknown` was chosen together with a grade in 1,322 of 5,914 tasks (22.4%) |
| A5 | Same fact entered twice in one task (image-level choice and polygon label) | A slip in one of the two entries shows as a contradiction | 7 (grade choice and graded polygons; `tumor_check` and tumor polygons), 14 (group marks and polygons) | 5,914 (project 7) | Grade choice = highest polygon grade in 3,572 of 3,596 tasks (99.3%); `notfound` with a tumor polygon in 5 of 3,494 |
| A6 | AI draft with a human verdict (`ai_correct`, `ai_almost`, `changed`) | The labeler must judge every pre-drawn outline; the verdict tells how often the draft was wrong | 33 | 3,933 of 4,239 | `changed` 49.1% (47.5-50.7), `ai_correct` 42.4% (40.9-44.0), `ai_almost` 8.5% (7.6-9.4) |
| A7 | Free-text note | The labeler can report a problem the options do not cover | 36 (all but 35 and 49) | 956 | Rarely used (0.6% of marked tasks); 553 of the notes are in project 52 and 294 in project 9 |
| B1 | One finding per project | One yes/no decision per image and finding; nothing can be forgotten in a long list | 15, 19-24, 26-28, 32, 50 | - | Projects 20-24: 99.9% of tasks answered in each; 0, 1, 2, 3, 4 or 5 of the five kidney findings drawn on 6,988 / 2,359 / 721 / 292 / 81 / <5 regions |
| B2 | Staged routing: a project receives only images where an earlier project recorded the organ | An "absent" answer is given only where the organ is in view; `skip_no_organ_found` reports a wrong earlier organ label | 15-28, 50 (from projects 2 and 14); 36-47 (from 33 and 35) | - | Table 4 |
| B3 | Second pass over the same images by another project (image-level check, then polygons) | Two judgments of the same finding can be compared | 35 with 33; 35 with 36-47; 49 with 52 | - | Tables 5 and 6; the disagreements were not settled in the sheets |

Table 3. Use of the in-task measures per labeling project of 261023. Tasks with at least
one mark of each kind; "not labelled" and "submitted without any mark" come from the task
status in `taskcrops_df` (n/a: the project has no crop rows).

| Project | Title | Tasks | With any mark | With polygons | "Checked" mark | AI verdict | "Absent" answer | Quality skip | Exclusion skip | Text note | Not labelled | Submitted without any mark |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Project 1-1. Score Liver Fat Levels4000 | 5,913 | 5,913 | 0 | 0 | 0 | 0 | 179 | 495 | 0 | n/a | n/a |
| 2 | Project 1-2. Liver Ultrasound Anatomy | 5,913 | 5,913 | 5,511 | 0 | 0 | 0 | 1,381 | 1,537 | <5 | 0 | 0 |
| 3 | Project 1-3. Mark Fat Level Regions | 5,913 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | n/a | n/a |
| 4 | Project 1-4. Mark Ultrasound Area | 5,913 | 5,913 | 5,912 | 0 | 0 | 0 | <5 | 6 | <5 | n/a | n/a |
| 7 | 1-5. Liver Fatness Level | 23,652 | 5,914 | 4,331 | 1,160 | 0 | 3,494 | 1,377 | 1,154 | <5 | 17,738 | 0 |
| 9 | 1-6. Signs | 5,913 | 5,913 | 3,999 | 2,844 | 0 | 0 | 3,177 | 1,745 | 294 | n/a | n/a |
| 11 | Project 1-6-B. Additional Fatty Liver Signs | 5,913 | 1,517 | 947 | 0 | 0 | 0 | 203 | 368 | 0 | n/a | n/a |
| 14 | P-2-1-Liver Diag Complex(1) | 17,262 | 15,390 | 14,553 | 14,541 | 0 | 8 | 515 | 279 | 26 | 6 | 1,866 |
| 15 | 260220 Gallbladder Polyp | 6,858 | 2,301 | 80 | 0 | 0 | 2,116 | 105 | 0 | 0 | 4,556 | <5 |
| 19 | 260220e Gallstone (B1) | 846 | 845 | 11 | 0 | 0 | 834 | 0 | 0 | 0 | 0 | <5 |
| 20 | 260221a-Nephrolithiasis | 10,448 | 10,442 | 1,859 | 0 | 0 | 8,586 | <5 | 0 | 0 | 0 | 6 |
| 21 | 260221b-Nephritis | 10,448 | 10,442 | 1,406 | 0 | 0 | 8,218 | 819 | 0 | 0 | 0 | 6 |
| 22 | 260221c-Hydronephrosis | 10,448 | 10,440 | 1,255 | 0 | 0 | 9,179 | 10 | 0 | 0 | 0 | 8 |
| 23 | 260221d-Nephrocystosis | 10,448 | 10,441 | 347 | 0 | 0 | 10,094 | <5 | 0 | 0 | 0 | 7 |
| 24 | 260221e-Renal Carcinoma | 10,448 | 10,438 | 140 | 0 | 0 | 10,295 | <5 | 0 | 0 | 0 | 10 |
| 26 | 260220 Gallbladder Polyp (2) | 712 | 711 | 145 | 0 | 0 | 560 | 7 | 0 | 0 | 0 | <5 |
| 27 | 260220b Cholecystitis (IB12) (2) | 1,571 | 1,571 | 650 | 0 | 0 | 819 | 102 | 0 | 0 | 0 | 0 |
| 28 | 260220c Cholecystoma | 1,571 | 1,566 | 116 | 0 | 0 | 1,436 | 16 | 0 | 0 | <5 | <5 |
| 29 | Breast Diseases | 2,958 | 2,958 | 2,649 | 0 | 0 | 283 | 28 | 0 | 0 | 0 | 0 |
| 30 | Lung Disease | 3,949 | 607 | 113 | 0 | 0 | 217 | 277 | 0 | 0 | n/a | n/a |
| 31 | GRC - thyroid | 77 | 77 | 72 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| 32 | GRC - abdomenal | 803 | 803 | 15 | 0 | 0 | 788 | 0 | 0 | 0 | 0 | 0 |
| 33 | 260507-Liver Ultrasound Anatomy | 4,239 | 4,239 | 3,942 | 0 | 3,933 | 0 | 0 | 300 | 37 | 0 | 0 |
| 35 | 20260506 Anatomy and Disease Check | 4,239 | 4,239 | 0 | 0 | 0 | 0 | 21 | <5 | 0 | 0 | 0 |
| 36 | 260618a Liver Disease on Dom1 | 2,411 | 2,411 | 2,244 | 2,242 | 0 | 0 | 41 | 149 | 19 | 0 | 0 |
| 37 | Kidney Diseases on Dom-1 | 880 | 879 | 496 | 498 | 0 | 294 | 8 | 85 | <5 | 0 | <5 |
| 38 | 20260618c GB on Dom1 | 1,039 | 1,038 | 638 | 644 | 0 | 0 | <5 | 82 | 0 | 0 | <5 |
| 39 | 202601618D Bladder | 519 | 519 | 378 | 378 | 0 | 84 | <5 | 56 | <5 | 0 | 0 |
| 41 | 20260618E Lung Disease on Dom1 | 11 | 11 | 10 | 10 | 0 | 0 | 0 | <5 | <5 | 0 | 0 |
| 42 | 20260618F Prostate Disease on Dom1 | 106 | 106 | 71 | 71 | 0 | 33 | 0 | <5 | 0 | 0 | 0 |
| 43 | 20260618G Spine Disease on Dom1 | 56 | 56 | 37 | 37 | 0 | 7 | <5 | 11 | 0 | 0 | 0 |
| 44 | 20260618H Stomach | 521 | 521 | 0 | 373 | 0 | 0 | <5 | 147 | 0 | 0 | 0 |
| 45 | 20260618I Thyroid Disease on Dom1 | 19 | 19 | 12 | 13 | 0 | 5 | 0 | <5 | 0 | 0 | 0 |
| 46 | 20260618J Uterus | 545 | 545 | 391 | 403 | 0 | 89 | 0 | 50 | 16 | 0 | 0 |
| 47 | 260618k Knee Diagnosis on Dom 1 | 180 | 180 | 155 | 155 | 0 | 0 | 0 | 25 | <5 | 0 | 0 |
| 49 | P260709. CheckAnatDisease (Books) | 13,659 | 10,948 | 0 | 0 | 0 | 494 | 52 | 4,649 | 0 | n/a | n/a |
| 50 | P260826 - Hepatic Stone | 13,924 | 13,920 | 255 | 13,913 | 0 | 13,613 | 26 | 48 | <5 | 0 | <5 |
| 52 | P260910. DiagAnatDisease (book images) | 10,948 | 1,271 | 733 | 0 | 0 | 0 | 0 | 0 | 553 | n/a | n/a |
| | **All 38 projects** | **201,273** | **151,017** | **53,473** | **37,282** | **3,933** | **71,551** | **8,358** | **11,193** | **956** | **22,303** | **1,914** |

Reading of Table 3 by time (project ids rise with time; titles carry dates such as
260220 and 260910, read as year-month-day, an assumption):

- **Projects 1-11**: only skip reasons and a text field. Project 7 added `tumor_check`
  (`checked` / `notfound` / `cannotdiag`) and a second entry of the steatosis grade.
- **Project 14**: a `checked` / `absent` pair for each polygon group and
  `imagequality_checked`.
- **Projects 15-32**: one finding per project with an "absent" answer and
  `skip_badimagequality`.
- **Projects 33 and 35**: AI drafts with a verdict, and an image-level check project on
  the same images.
- **Projects 36-47 and 50**: `checked`, a "no disease" answer in 7 of the 12 projects,
  and `skip_no_organ_found`.
- **Projects 49 and 52**: image-level check, then polygons on the same images. Project 52
  has no in-task QA option except the text field.

### 3. Inside one task: what the measures caught, and what they left open

- **"Absent" against polygons**: 28 conflicts in 71,058 "absent" answers of projects that
  also offer the polygon (0.04%, 95% CI 0.03-0.06). The region-level record found 37 of
  20,581 regions (0.2%) across projects; both say the same.
- **Options that exclude each other, chosen together**: two steatosis grades in 5 tasks
  (project 7) and 18 tasks (project 35); two `tumor_check` answers, two AI verdicts or
  `possible` with `impossible` in <5 tasks each; none for the gallbladder size options
  and the `checked` / `absent` pairs of project 14.
- **Project 7** (5,914 labelled tasks): `tumor_check` was answered in all but 23 tasks.
  `checked` without a tumor polygon: 12 tasks; a tumor polygon without `tumor_check`: 14.
- **Project 14** (15,390 tasks with a mark): the "absent" options were used in 8 tasks
  only. So a task without polygons of a group and without the group's mark is not
  resolved: 832 tasks for anatomy and 5,414 for fat regions. The sign and signal-region
  groups were almost not used (sign polygons on <5 tasks, no signal-region polygon).
- **Submitted without any mark**: 1,914 tasks, 1,866 of them in project 14 (10.8% of its
  17,255 submitted tasks, 10.4-11.3). Nothing tells "looked at, nothing to label" from
  "submitted by mistake". `skip_untouched` (223 tasks) may be the same case; its meaning
  is not documented.
- **Projects without an "absent" option**: in project 38 (gallbladder) 307 of 1,038
  marked tasks (29.6%, 26.9-32.4) carry only a size choice, with no polygon and no
  `checked` mark; "no disease" cannot be told from "not finished" there. Projects 2, 4,
  9, 11, 33, 36, 41, 44, 47 and 52 also offer polygons without an "absent" choice.
- **Project 3** (5,913 tasks) has no mark at all. **Project 7** lists each of its 5,913
  regions 4 times (23,652 tasks); one copy was labelled and 17,738 tasks were never
  touched. Whether the copies were meant for repeat labelling is not recorded.

### 4. Between projects: routing

Table 4. Staged routing in 261023: share of a later project's regions (labelled or not)
that carry the organ in an earlier project.

| Later project(s) | Regions | Earlier record of the organ | Regions with it |
|---|---:|---|---:|
| 20-24 (five kidney findings) | 10,448 each | kidney polygon in project 2 or 14 | 10,448 (100%); these are all kidney-polygon regions of projects 2 and 14 |
| 50 (hepatic stone) | 13,924 | liver polygon in project 2 or 14 | 13,923 (100.0%) |
| 19, 26, 27, 28 (gallbladder findings) | 846; 712; 1,571; 1,571 | gallbladder polygon in project 2 or 14 | 100% each |
| 15 (gallbladder polyp) | 6,858 | gallbladder polygon in project 2 or 14 | 1,734 (25.3%): all gallbladder-polygon regions plus others |
| 36-39, 42-47 (ten organ projects of the 33/35 family) | 6,276 in all | organ or organ-disease choice in project 35, or organ polygon in project 33 | 6,265 (99.8%) |

- Every region where project 35 chose a disease of an organ went to that organ's project
  (3,547 of 3,548).
- `skip_no_organ_found` is the later labeler's report that the routed organ is not
  there. It was set on 610 of 6,287 tasks of projects 36-47 (9.7%, 9.0-10.5), most often
  for the stomach (147 of 521, 28.2%, 24.5-32.2), and on 48 of 13,924 tasks of project
  50 (0.3%, 0.3-0.5). All 48 of those regions carry a liver polygon in project 2 or 14.

### 5. Between projects: agreement of two passes on the same region

Table 5. Organ choices of project 35 against organ polygons of project 33 on the same
region (n = 3,925 regions: project 33 gave a verdict, no skip in either project), per
organ offered in both. Kappa with 95% CI (bootstrap over regions; blank where a count
is below 5).

| Organ label | Both | Choice only | Polygon only | Kappa (95% CI) |
|---|---:|---:|---:|---|
| `liver` | 2,162 | 19 | 206 | 0.883 (0.868-0.897) |
| `bladder` | 424 | 32 | 46 | 0.905 (0.883-0.925) |
| `uterus` | 411 | 36 | 68 | 0.873 (0.848-0.896) |
| `knee` | 122 | 21 | 17 | 0.860 (0.812-0.901) |
| `kidney` | 685 | 37 | 142 | 0.856 (0.836-0.876) |
| `gallbladder` | 838 | 92 | 148 | 0.834 (0.814-0.854) |
| `spleen` | 79 | 24 | 12 | 0.810 (0.745-0.869) |
| `prostate` | 82 | 22 | 23 | 0.779 (0.716-0.835) |
| `spine` | 39 | <5 | 14 | |
| `thyroid` | 10 | <5 | 8 | |
| `heart` | 24 | 0 | 0 | 1.000 |
| `pancreatin` (pancreas) | 58 | 55 | 17 | 0.608 (0.518-0.689) |
| `ascites` | 20 | 37 | 5 | 0.483 (0.338-0.609) |
| `hepatic_duct` | 974 | 1,063 | 38 | 0.449 (0.426-0.475) |
| `stomach` | 78 | 24 | 413 | 0.230 (0.185-0.274) |
| `intestine` | 0 | 0 | 277 | 0.000 |
| **All 16** | **6,006** | **1,466** | **1,434** | positive agreement 0.806 (0.799-0.813) |

- Agreement did not depend on the AI verdict of project 33: positive agreement 0.802
  (`ai_correct`, 1,668 regions), 0.824 (`ai_almost`, 331) and 0.806 (`changed`, 1,927).
- `intestine` was never chosen in project 35 on these regions and `stomach` rarely; the
  polygon project drew both. `hepatic_duct` was chosen about twice as often as drawn.

Table 6. Disease choices of project 35 against disease polygons of the organ projects
36-47 on the same region, summed over the labels offered in both. n = regions of the
organ project without a skip. A region counts once per label.

| Organ project | Regions, n | Both | Choice only | Polygon only | Positive agreement |
|---|---:|---:|---:|---:|---:|
| 36 liver | 2,244 | 1,367 | 1,285 | 1,345 | 0.510 |
| 37 kidney | 791 | 191 | 27 | 397 | 0.474 |
| 38 gallbladder | 952 | 428 | 66 | 334 | 0.682 |
| 39 bladder | 462 | 226 | 14 | 156 | 0.727 |
| 46 uterus | 495 | 166 | 43 | 123 | 0.667 |
| 47 knee | 155 | 124 | 16 | 9 | 0.908 |
| 41-45 (lung, prostate, spine, stomach, thyroid) | 548 | 80 | 11 | 25 | 0.816 |
| **All** | | **2,582** | **1,462** | **2,389** | **0.573** |

- Lowest kappa per label: `hepatitis` 0.055 (37 both, 335 choice only, 108 polygon
  only), `hepatic_steatosis__2` 0.154, `hepatic_steatosis__3` 0.173, `nephritis` 0.231
  (113 both, 314 polygon only), `cystitis` 0.298 (154 polygon only),
  `hepatic_cirrhosis` 0.467 (399 polygon only), `cholecystitis` 0.466 (214 polygon only).
- Highest: `cystolithiasis` 0.833, `pregnancy` 0.808, `prostate_stone` 0.749,
  `hepatic_cyst` 0.737, `gallbladder_stone` 0.728, `hemangioma` 0.717.
- "No disease" answers of the organ projects rarely met a disease choice of project 35:
  <5 of 294 (kidney), 8 of 84 (bladder), <5 of 89 (uterus), 0 of 45 (prostate, spine,
  thyroid).

Table 7. Steatosis grade chosen in project 35 against the grade drawn in project 36 on
the same region (n = 995 regions with exactly one grade in each).

| Measure | Value |
|---|---|
| Same grade | 576 of 995 (57.9%, 95% CI 54.8-60.9) |
| Within one grade | 964 of 995 (96.9%, 95.6-97.8) |
| Polygon grade higher / lower than the choice grade | 396 / 23; mean difference +0.41 grade |
| Quadratic weighted kappa | 0.624 (0.588-0.658) |

- **Projects 2 and 7** (same 5,913 regions): `skip_lowdim` was set by both on 1,370
  regions and by one only on 17 (kappa 0.992); `skip_anatomyunclear` (project 2) and
  `cannotdiag` (project 7) coincide on 1,216 regions (kappa 0.966). 1,308 of the 1,381
  `skip_lowdim` regions lie in 2 of the 11 datasources. The sheets cannot tell whether
  the two projects judged these independently or one decision was carried over.
- **Projects 1 and 7** have the same number of tasks (5,913 labelled) and the same
  choice list, but project 1 has no crop rows, so its tasks cannot be matched to images.
  The label mix differs strongly: grade 0 on 1,541 against 458 tasks, grade 2 on 560
  against 1,229, grade 3 on 458 against 88, `unknown` on 130 against 2,472.
- **Projects 49 and 52** have no crop rows. Project 52 has 10,948 tasks, the number of
  marked tasks of project 49. Matching them by task order (an inference) gives the same
  label in 967 of 1,304 polygon task-labels of project 52 (74.2%, 71.7-76.5) against
  8.6% for a random match, so the order link holds. On it: project 52 was worked on for
  its first 1,271 tasks (11.6%); on the 762 of those without a skip in project 49 the
  positive agreement is 0.596 (944 both, 1,052 choice only, 226 polygon only); 94 tasks
  got polygons although project 49 had skipped the image.

### 6. Repeat labelling that was not planned

A few images occur twice inside a project under two file names (same image content and
crop box). No pair has the same polygon points, so each copy was labelled on its own.
These pairs are the only repeat labelling inside a project.

Table 8. Agreement of the two labelings of repeated images inside one project
(261023; pairs of tasks with the same image content).

| Project | Pairs | Identical label set (95% CI) | Outline overlap, mean IoU (pairs) |
|---|---:|---|---|
| 2 (anatomy polygons) | 52 | 36 (69.2%, 55.7-80.1) | `liver` 0.814 (36); `kidney` 0.806 (13); `intestine` 0.700 (7); `stomach` 0.542 (6); `hepatic_blood_duct` 0.306 (17) |
| 7 (steatosis regions) | 53 | 39 (73.6%, 60.4-83.6) | fat regions of any grade 0.706 (29) |
| 20-24 (kidney findings) | 509 | 504 (99.0%, 97.7-99.6) | not computed |

In projects 20-24 nearly all pairs are "absent" twice. Of the 11 pairs with a polygon
in either copy, 6 have it in both.

## What this means

1. **Most measures are self-reports.** A1-A7 are entered by the same person in the same
   task as the label they protect. They reveal a forgotten task or a slip between two
   entries. They cannot reveal a wrong disease, grade or outline, because the labeler
   repeats the same belief. This is why same-task consistency is 99.3-99.96% while
   agreement between passes is 57-81%. Same-task consistency should not be read as
   accuracy.
2. **Only the staged design can reveal a wrong judgment**, and only where it exists:
   the 4,239 regions of projects 33-47, and the images of projects 49 and 52. For the
   large liver and kidney families (projects 2, 7, 14, 15-28, 50) each finding was judged
   once; the routing there protects the "absent" answers (the organ is in view) but does
   not test the finding itself.
3. **The second pass was not used to settle disagreements.** Both values stay in the
   sheets and no label says which one is right. Table 6 is therefore a measure of how
   uncertain these disease labels are, not a list of corrected errors.
4. **The disagreements are systematic**, so more care alone would not remove them:
   the polygon pass grades steatosis about 0.4 grade higher on average, and whole labels
   (`hepatitis`, `nephritis`, `cystitis`, `hepatic_cirrhosis`, `hepatic_duct`,
   `stomach`) are used differently by the two passes. A shared definition per label would
   have to come before any agreement target.
5. **Optional marks leave gaps exactly where they matter**: 1,866 submitted tasks
   without a mark, the unused "absent" options of project 14, projects without a "no
   disease" option, and `unknown` chosen together with a grade.
6. **Skip reasons depend on the question and the labeler** (819 against at most 10 on
   the same images). They say "I could not answer this question on this image", not "this
   image is bad". This matters for the open rule on leaving out such crops
   ([TASK-062](../../../backlog/tasks/task-062%20-%20Decide-the-rule-for-leaving-out-quality-and-case-exclusion-crops-from-train-val-test-DIS-012.md),
   rule for leaving out quality and case-exclusion crops).
7. **Without labeler identity and time, classic QA numbers cannot be computed**:
   agreement between labelers, error rate per labeler, drift over time. It is also
   unknown whether two passes were made by different people.

## Limitations

- Exploratory; one analyst; no second check of the scripts. The scripts are one-off and
  not in the repo.
- 58,121 tasks of 8 projects have no crop row and could not be placed on images
  ([TASK-065](../../../backlog/tasks/task-065%20-%20Explain-the-6-labeling-projects-of-261023-with-no-crop-row-23-of-choice-pairs.md),
  the projects with no crop row). The link between projects 49 and 52 is inferred from
  task order; the link between projects 1 and 7 is assumed and not testable.
- Intervals treat regions as independent; projects 33-47 rest on 4 datasources.
- Roles of choice labels come from the DEC-036 map; another map changes the counts.
- Two passes that disagree do not tell which one is right. No reference standard exists
  in these sheets.
- Whether the labeling tool recorded labeler, time or review status is unknown; the four
  sheets do not hold them.
- Medical readings of the disagreements (e.g. why `hepatitis` is rarely drawn) were not
  checked by a doctor.

## Possible next steps (not decided)

- Decide which pass is the training target for the disease labels of the 33-47 family,
  or have the disagreeing regions judged again (about 3,850 label-region pairs).
- Use Table 6 and Table 7 as the label-noise estimate when test metrics for these labels
  are reported.
- Export labeler, time and review status from the labeling tool if it still has them.
- Keep the repeated images (Table 8) as a small test-retest set.
- In new projects make the closing answer required ("absent" or "checked"), and add a
  "no disease" option where it is missing.

# Amendments

## Amendment 1 (2026-11-11; category codes added 2026-11-12): five categories of QA measure, reassigned options

From the user's review of Table 2 on 2026-11-11. It changes how the measures are
grouped and where some options belong. It changes no count: Tables 1-8 and the text
above stay as they were. Notes marked "(analyst)" are additions by the analyst, not the
user's decisions.

- **Sample**: the user's term for one labelled image crop, the unit of the planned
  per-sample label table `sample_label_df` (not in the repo yet).
- **Codes**: categories have the codes C1-C5, new in this amendment. Measures keep their
  codes from Table 2: A1-A7 (inside one task) and B1-B3 (between projects). A C code
  always names a category; an A or B code always names a measure.

### Categories

Table 9. The five categories (C1-C5) of quality-assurance (QA) measure in the labeling
projects of 261023 (user's definitions, 2026-11-11), with the measures of Table 2 that
belong to each (measure code and short name).

| Category code | Category | What it does | Measures in the category |
|---|---|---|---|
| C1 | Skip-sample | Leaves the sample out as a whole | A3 skip reason (image quality or case exclusion) |
| C2 | Skip-part | Leaves some labelings of the sample out; the rest of the sample stays | A4 "cannot decide" for one part of the labeling |
| C3 | Visited check | The labeler leaves at least one positive mark as a trace of the visit, so that a missing label is a real negative | A2 "checked" mark; or derived from the project design (Table 12) |
| C4 | Double conformance | Compares two or more labelings of the same aspect of a sample, to avoid the subjectivity of a single assessment; the labelings may differ in style (choice, polygon) | A1 explicit "absent" answer; A5 same fact entered twice in one task; B3 second pass by another project |
| C5 | Other | Not one of the above | A6 AI draft with a human verdict; A7 free-text note; B1 one finding per project; B2 staged routing |

Measures A6 and A7 (both in C5) are not important and are ignored when `sample_label_df`
is built.

### Changes to measures A1-A5

Table 10. Options of 261023 that move between QA measures, or whose reading changes, in
Amendment 1. Projects and crops from [labels-261023.md](../../../docs/labels-261023.md)
(crops = crops with the option); project-14 task counts from Table 3.

| Option | Kind | Projects | Crops or tasks, n | Measure before | Measure now | Reason (user) |
|---|---|---|---:|---|---|---|
| `hepatic_steatosis__unknown` | per-image choice | 1, 7 | 2,602 crops | A4 | Not used at all | Its use is not consistent: in project 7 it was chosen together with a grade in 1,322 of 5,914 tasks (22.4%) |
| `cannotdiag` | per-image choice, group `tumor_check` | 7 | 1,239 crops | A4 | A4 | It skips one labeling job, not the image: the disease polygons of group `tumor_regions` are not labelled |
| `skip_anatomyunclear` | per-image choice | 2, 9, 11, 33 | 3,124 crops | A4 | A3 | With unclear anatomy neither anatomy nor diagnostic labels make sense, so the sample has no place in training |
| `hepatic_steatosis__ignore` | polygon, group `fat_regions` | 7, 14 | 73 crops | A4 | A4 | Marks an area of the image whose steatosis is not graded. Always note that it is a polygon, not a choice |
| "Checked" group marks of project 14 (`anatomy_checked`, `hepatic_steatosis_checked`, `signs_checked`, `signal_regions_checked`) | per-image choice | 14 | 14,541 tasks | A2 and A5 | A2 | A mark per group that the group was looked at is a visited check (C3) |
| "Absent" group marks of project 14 (`anatomy_absent`, `heaptic_steatosis_absent`, `signs_absent`) | per-image choice | 14 | 8 tasks | A1 and A5 | A1 | An "absent" mark per group is an absent answer |

Table 11. Measures A1-A5 of Table 2 after Amendment 1, with the category of each
(measures A6-B3 unchanged; their categories are in Table 9). A category can hold
several measures, so a category code can appear on more than one row: A1 and A5 are
both in C4, as is B3 (not shown). Task counts stay as in Table 2.

| Measure code | Category | Measure | How it can reveal an error | Projects that offer it |
|---|---|---|---|---|
| A1 | C4 Double conformance | Explicit "absent" answer, including the project-14 group marks (`anatomy_absent`, ...) | An empty task no longer looks like a negative; the answer can be compared with the polygons of the same group | 24 (unchanged) |
| A2 | C3 Visited check | "Checked" mark, including the project-14 group marks (`anatomy_checked`, ...) | The labeler states that a group of labels was looked at, so missing polygons are meant | 15 (unchanged) |
| A3 | C1 Skip-sample | Skip reason: image quality or case exclusion, now with `skip_anatomyunclear` | Unusable or out-of-scope samples are named and left out as a whole | 36 (unchanged; 2, 9, 11 and 33 already offered other skip reasons) |
| A4 | C2 Skip-part | "Cannot decide" for one part of the labeling: `cannotdiag` (choice), `hepatic_steatosis__ignore` (polygon) | Doubt is recorded instead of a forced guess. Unlike A3, A4 states that one aspect of labeling the sample is uncertain; it does not say the whole sample should be left out | 2 (7, 14); was 8 |
| A5 | C4 Double conformance | Same fact entered twice in one task, project 7 only: grade choice and graded polygons; `tumor_check` and tumor polygons | A slip in one of the two entries shows as a contradiction | 1 (7); was 2 |

Notes (analyst):

1. **No count in Tables 2-3 changes.** The project-14 marks were already counted in A2
   (14,541 tasks) and A1 (8 tasks). `skip_anatomyunclear` has role `exclusion` in the
   DEC-036 map, so it was probably already in the A3 exclusion count (11,193 tasks); the
   one-off script was not re-run to confirm this.
2. **`cannotdiag` mostly coincides with `skip_anatomyunclear`.** On the regions of
   projects 2 and 7 the two coincide on 1,216 regions (kappa 0.966, Section 5). So most
   `cannotdiag` samples leave as whole samples through measure A3 (C1 skip-sample), and
   `cannotdiag` as measure A4 (C2 skip-part) acts alone
   on about 23 regions (1,239 - 1,216; assumes one labelled task per region in project 7,
   as Section 3 found).
3. **Dropping `hepatic_steatosis__unknown`** is read here as: the steatosis grade of
   projects 1 and 7 comes from the grade options alone; a task with `unknown` and no grade
   has no steatosis label (missing, not grade 0). In project 7 that is 1,150 of the
   2,472 tasks with `unknown` (2,472 - 1,322). The polygon of the same name (project 3)
   was never used.
4. **Measure A1 also works as a visited check (C3).** An "absent" answer is a positive
   mark that shows the visit and makes the negative real, which is the goal of C3. It
   stays in C4 (double conformance) as well: the answer can be compared with the polygons
   of its group (28 conflicts in 71,058, Section 3). Table 12 therefore shows both.

### Projects without a visited check (C3)

**23 of the 38 projects offer no "checked" mark (measure A2, the explicit visited
check)**: 1, 2, 3, 4, 11, 15, 19-24, 26-33, 35, 49, 52. Of these, 15 offer an "absent"
answer (measure A1) instead; 8 offer neither: 1, 2, 3, 4, 11, 33, 35, 52.

**Derived visited check (C3)** (user, 2026-11-11): a project without an explicit mark can be
considered to have a visited check if the labeler should make at least one positive
labeling on every task they visit (for example a grade, an organ, an "absent" answer, an
AI verdict or a skip reason). Then a task with any mark was visited, and its missing
labels are real negatives; a task without any mark was not visited, and its labels are
missing, not negative. The sheets do not record whether a project required such a mark;
Table 12 judges it from the options offered and their use in Table 3 (analyst). By this
reading **20 of the 23 projects have a derived visited check**; project 11 has none,
project 3 was never labelled, and project 52 is unclear.

Table 12. Labeling projects of 261023 without a "checked" mark (measure A2): polygon
use, "absent" answer (measure A1) and derived visited check (C3) of each. Tasks with
polygons and marked tasks from Table 3; the derived check and its reason are the
analyst's reading.

| Project | Tasks with polygons, n (of marked tasks) | "Absent" answer (measure A1) offered | Derived visited check (C3) | Reason |
|---|---|---|---|---|
| 1 Score Liver Fat Levels | 0 (5,913) | No | Yes | Every visited task needs a grade (grade 0 included) or a skip reason |
| 2 Liver Ultrasound Anatomy | 5,511 (5,913) | No | Yes | Every image shows some anatomy to outline; if not, a skip reason (`skip_anatomyunclear`, ...) is due |
| 3 Mark Fat Level Regions | 0 (0) | No | No | No task has any mark: the project was not labelled |
| 4 Mark Ultrasound Area | 5,912 (5,913) | No | Yes | Every image has an ultrasound area to outline |
| 11 Additional Fatty Liver Signs | 947 (1,517) | No | No | An image may show no sign, and there is no "absent" option: "no sign" and "not visited" both leave no mark |
| 15, 19, 20-24, 26-28 (gallbladder and kidney, one finding each) | 11-1,859 per project | Yes | Yes | The "absent" answer closes every task without a polygon |
| 29-32 (breast, lung, thyroid, abdominal) | 15-2,649 per project | Yes | Yes | The "absent" answer closes every task without a polygon |
| 33 Liver Ultrasound Anatomy (AI drafts) | 3,942 (4,239) | No | Yes | Every task with an AI draft needs a verdict (3,933 tasks), else a skip reason; measure A6 itself stays in C5 (other) |
| 35 Anatomy and Disease Check | 0 (4,239) | No | Yes | Every image shows at least one organ to choose, else a skip reason is due |
| 49 CheckAnatDisease (Books) | 0 (10,948) | Yes (494 tasks) | Yes | The "absent" answer closes every task without a choice |
| 52 DiagAnatDisease (book images) | 733 (1,271) | No | Unclear | No skip reason or "absent" option, only a text note, so a book image with nothing to outline leaves no mark. The marked tasks are the first 1,271 in order (Section 5), which fits "labelled in order, then stopped" |

Where measure A2 is offered it is partial (Section 3): in project 7 the `checked` mark covers
only group `tumor_check`; in project 14 the marks are optional; in project 38, 307
marked tasks carry only a size choice. Tasks submitted without any mark (1,914, of which
1,866 in project 14; Table 3) break both rules: they were submitted, yet left no trace.
The safe reading is "not visited": their labels are missing, not negative (analyst).

