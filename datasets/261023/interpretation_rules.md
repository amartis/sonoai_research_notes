# Data interpretation rules of the labeling projects of dataset version 261023

Asked by the user on 2026-11-12 (no board task). Builds on
[labeling_qa_measures.md](labeling_qa_measures.md) (the QA report: measure codes A1-A7 and
B1-B3, categories C1-C5 of its Amendment 1). Names follow the
[glossary](../../../docs/glossary.md) (DEC-056: labeling project, tag group, tag, sample,
labeling task, given labeling). Tag lists:
[label_projects.yaml](../../../configs/data/label_projects.yaml); roles of choice tags:
[choice_labels.yaml](../../../configs/data/choice_labels.yaml) (DEC-036).

**Status: draft.** Every rule here is a candidate. How far each rule is respected in the
labeled data is the next step and is not measured here; rules that are not respected will
be dropped. Aggregates only; no images, file names or identifiers. Not reviewed.

## Summary

_(filled when the project-relationship step is done)_

## Terms

- **Interpretation rule** (rule): a statement of how a given labeling of one tag changes
  the reading of another tag, a tag group, a labeling task or a sample. Each rule has a
  subject, a measure code and a target.
- **Subject**: the tag whose given labeling triggers the rule (labeling project, tag group,
  tag name), or a state of the labeling task (for example "no given labeling").
- **Measure code**: the QA measure the rule comes from: A1-A7, B1-B3 of the QA report, or
  a code proposed here (A8, A9, B4; marked "proposed"). The category (C1-C5) follows in
  brackets.
- **Target**: what the rule changes: a tag, a tag group, the labeling task (all its tags),
  or the sample (the labeling tasks of other labeling projects on the same sample).
- **Scope**: where the target is looked for: the same labeling task, the same labeling
  group (one tag group of the task), or the same sample in another labeling project.
- **Reading**: how the target is read when the rule applies: negative (the finding is not
  there), missing (no label), left out (the sample or task gives no label), or compared
  (two entries of one fact).
- **Expected in the data**: the statement that the respect statistics will test.
- **Pn**: labeling project n (`project_id` n). "Same task" = the same labeling task.
- **Visited**: the labeler worked on the labeling task (or one labeling group of it).
- **Family**: labeling projects that share their samples (Section 1).

## Method

1. Listed every tag of the 38 labeling projects from `label_projects.yaml` (621 tags).
2. For every QA measure of the QA report, wrote down which tags are its subjects and what
   they act on, from the tag groups, the role map and the label guide
   ([label-guide.md](../../../docs/label-guide.md) section 3, Q1-Q14).
3. Added links between tags that the QA report did not name but that the tag lists imply
   (options that exclude each other, one tag that implies another). These carry new
   codes, marked "proposed (analyst)".
4. One row per pattern of tags, with every tag listed, so that each rule stays tag-level
   but the table stays short. Project families (Section 1) group the cross-project rules.

## 1. Project relationships

_(pending: shared samples and images between the labeling projects; needs `taskcrops_df`
and `flags_df`, read after the user's ok)_

## 2. Rules inside one labeling task

### 2.1 Explicit "absent" answer (A1)

Table 1. Rules from explicit "absent" answers (measure A1, category C4 double
conformance; the answer also closes the visit, C3). Reading for every row: target tags not
given in the same task are true negatives. Expected for every row: no target tag is given
in the same task.

| Rule | Subject (labeling project: tag) | Measure code | Target (scope) | Note |
|---|---|---|---|---|
| R01 | P15, P26 `gallbladder_polyp_absent`; P19 `gallbladder_stone_absent`; P20 `renal_calculus_absent`; P21 `nephritis_absent`; P22 `hydronephrosis_absent`; P23 `nephrocystosis_absent`; P24 `renal_carcinoma_absent`; P27 `cholecystitis_absent`; P28, P32 `gallbladder_tumor_absent` | A1 (C4) | the project's one polygon tag of the same finding, e.g. P20 `renal_calculus` (same task) | one finding per project (B1) |
| R02 | P29 `breast_disease_no` | A1 (C4) | polygon tags `breast_tumor`, `breast_abscess` (same task) | |
| R03 | P30 `lung_absent` | A1 (C4) | polygon tags `lung_disease_1`, `lung_disease_2` (same task) | both targets are ignored by recipes (label-guide Q8) |
| R04 | P31 `thyroiditis_abscent` | A1 (C4) | polygon tags `thyroid_tumor`, `thyroid_cyst`, `thyroiditis` (same task) | open: the name says thyroiditis only; the role map reads all three |
| R05 | P37 `kidney_nodisease`, P39 `bladder_nodisease`, P42 `prostate_nodisease`, P43 `disk_nodisease`, P45 `thyroid_nodisease`, P50 `no_hepatic_stone` (group `checking`) | A1 (C4) | every polygon tag of group `diseases` of the same project (same task) | |
| R06 | P46 `uterus_nodisease` | A1 (C4) | group `diseases` without `pregnancy` and `ovarian_follicle` (same task) | these two are not diseases (role map) |
| R07 | P7 `notfound` (group `tumor_check`) | A1 (C4) | tag group `tumor_regions`, 7 polygon tags (same task) | |
| R08 | P14 `anatomy_absent` | A1 (C4) | tag group `anatomy_liver`, 17 polygon tags (same task) | |
| R09 | P14 `signs_absent` | A1 (C4) | tag group `liver_signs`, 16 polygon tags (same task) | |
| R10 | P14 `heaptic_steatosis_absent` | A1 (C4) | steatosis tags of group `fat_regions`: `hepatic_steatosis__0`-`__3`, `__ignore` (same task) | open: whether it also covers the 7 disease tags of the same group |
| R11 | P49 `spine_nodisease`, `thyroid_nodisease`, `uterus_nodisease`, `prostate_nodisease`, `bladder_nodisease`, `kidney_nodisease`, `bursa_nodisease` (each in its group `check_disease__<Organ>`) | A1 (C4) | the disease choice tags of the same tag group (same task); uterus as R06 | choice against choice, not polygon |
| R12 | P47, P52 `bursa_nodisease` (a polygon: outline of a normal bursa) | A1, polygon form (proposed, analyst) | polygon tag `bursitis` (same task) | the only "absent" answer that is a polygon |

### 2.2 "Checked" mark (A2)

Table 2. Rules from "checked" marks (measure A2, category C3 visited check). Reading for
every row: with the mark, target tags not given are true negatives; without the mark and
without another closing answer, they are missing. Expected for every row: every task with
a given target tag also carries the mark (the mark was set every time).

| Rule | Subject (labeling project: tag) | Measure code | Target (scope) | Note |
|---|---|---|---|---|
| R13 | P36-39, P41-47, P50 `checked` (group `checking`) | A2 (C3) | every polygon tag of group `diseases` of the same project (same task) | P36, P38, P41, P44, P47 have no "absent" answer: the mark is their only closure |
| R14 | P9 `checked` (group `discard_reason`) | A2 (C3) | tag group `anatomy_liver`, 16 sign polygon tags (same task) | |
| R15 | P7 `checked` (group `tumor_check`) | A2 (C3) | tag group `tumor_regions` (same task) | in P7 it also means "found and drawn": R24 |
| R16 | P14 `anatomy_checked`, `signs_checked`, `hepatic_steatosis_checked`, `signal_regions_checked` | A2 (C3) | each mark's own tag group: `anatomy_liver`, `liver_signs`, `fat_regions`, `signal_regions` (same labeling group) | the visit is per labeling group, not per task |
| R17 | P14 `imagequality_checked` (group `image_quality`) | A2 (C3) (proposed, analyst; role `other` in the map) | the skip tags of group `image_quality` (same task): none given = quality accepted | expected also: never given with a skip tag of the group |

### 2.3 Skip reason (A3) and "cannot decide" (A4)

Table 3. Rules from skip reasons (measure A3, category C1 skip-sample) and "cannot
decide" answers (measure A4, category C2 skip-part). The skip tags of each project are
listed in Table 7.

| Rule | Subject (labeling project: tag) | Measure code | Target (scope) | Reading | Expected in the data |
|---|---|---|---|---|---|
| R18 | every skip tag of Table 7 (roles `quality` and `exclusion`, with `skip_anatomyunclear`) | A3 (C1) | the labeling task: all its other tags (same task) | left out: the task gives no label; its tags are missing, not negative | no other given labeling in the task, except other skip tags and text notes |
| R19 | the skip tags that describe the image: role `quality`, `skip_notultrasound`, `skip_anatomyunclear` | A3 (C1) | the sample: the labeling tasks of the other projects of its family (same sample) | left out of every project's labels ("leaves the sample out as a whole") | the other projects on the same sample also skip it, or leave it without a given labeling |
| R20 | P7 `cannotdiag` (group `tumor_check`) | A4 (C2) | tag group `tumor_regions` (same task) | missing, not negative; the rest of the task stays | no `tumor_regions` polygon in the task |
| R21 | P7, P14 polygon `hepatic_steatosis__ignore` (group `fat_regions`) | A4 (C2) | the grade polygon tags `hepatic_steatosis__0`-`__3` inside its outline (same task, pixel level) | the outlined area has no grade (not grade 0) | it does not overlap a grade polygon of the task (label-guide Q1: drawn beside graded areas) |

R19 leaves out the exclusion skips that name the project's own question (`skip_no_organ_found`,
`skip_notliver`, `skip_smallliver`, `skip_notabdomen`, `skip_otherdisease`,
`skip_othercase`, `skip_toofat`, `skip_liver_c`): "the kidney is not in view" does not make
the sample useless for the liver. Those stay at task scope (R18). This split is the
analyst's, not the user's.

### 2.4 Same fact entered twice (A5)

Table 4. Rules from two entries of one fact in one labeling task (measure A5, category C4
double conformance). Reading for every row: the two entries are compared; when they
disagree, the fact is a conflict.

| Rule | Subject (labeling project: tag) | Measure code | Target (scope) | Expected in the data |
|---|---|---|---|---|
| R22 | P7 grade choices `hepatic_steatosis__0`-`__3` (group `classify_case`) | A5 (C4) | grade polygon tags of group `fat_regions` (same task) | the chosen grade equals the highest drawn grade |
| R23 | P7 disease choices `hepatoma`, `hemangioma`, `hepatic_cyst`, `hepatic_cirrhosis`, `gastric_tumor` (group `classify_case`) | A5 (C4) (added, analyst) | the polygon tag of the same name in group `tumor_regions` (same task) | choice given if and only if the polygon is given |
| R24 | P7 `checked` (group `tumor_check`) | A5 (C4) | tag group `tumor_regions` (same task) | `checked` if and only if at least one `tumor_regions` polygon |
| R25 | P11 `hepatorenal_contrast_liverbrighter` (choice) | A5 (C4) (added, analyst) | polygon tag `sign_hepatorenal_wall_highecho` (same task) | both or neither (role-map note) |
| R26 | P14 polygon `liver_ascites` (group `anatomy_liver`) | A5 (C4) (added, analyst) | polygon tags `sign_liver_ascites`, `sign_liquid_near_liver` (group `liver_signs`, same task) | drawn together; one meaning (label-guide Q7) |

### 2.5 Options that exclude each other (A8, proposed) and implied tags (A9, proposed)

Two kinds of link are not QA measures of the QA report but are built into the tag lists.
Proposed codes (analyst): **A8 exclusive options**: at most one tag of a set per task;
two given make the answer a conflict. **A9 implied tag**: the subject implies the target;
the subject without the target is a conflict. Both are double conformance (C4).

Table 5. Rules from exclusive options (A8) and implied tags (A9), proposed. Reading for
A8 rows: two tags of the set in one task make the set's answer a conflict (missing). For
A9 rows: a subject without its target is a conflict.

| Rule | Subject (labeling project: tag) | Measure code | Target (scope) | Expected in the data |
|---|---|---|---|---|
| R27 | P1, P7 grade choices `hepatic_steatosis__0`-`__3` (`classify_case`); P35, P49 the same tags (`check_disease__Liver`) | A8 (C4) | the other grades of the same group (same task) | at most one grade per task |
| R28 | P7 `checked`, `notfound`, `cannotdiag` (`tumor_check`) | A8 (C4) | each other (same task) | exactly one per visited task without a skip |
| R29 | P9 `hepatorenal_contrast_possible` | A8 (C4) | P9 `hepatorenal_contrast_impossible` (same task) | not both |
| R30 | P38, P49 `gallbladder_contracted`, `gallbladder_normalsized`, `gallbladder_dilated` (choices); P52 the same as polygons | A8 (C4) | each other (same task); `gallbladder_deformed` may join any | at most one size state per task (label-guide Q11) |
| R31 | P14 `anatomy_checked`, `signs_checked`, `hepatic_steatosis_checked` | A8 (C4) | the "absent" mark of the same group (same task) | not both (QA report section 3 reads the pairs as exclusive) |
| R32 | P9, P14 polygons `sign_liverskin_coarse`, `sign_liveredge_blunt`; P11 `sign_hepatorenal_wall_highecho`, `sign_gallbladderwall_vivid`, `sign_diaphragm_vivid` | A8 (C4) | their opposites: `sign_liverskin_smooth`, `sign_liveredge_sharp`; `sign_hepatorenal_wall_normal`, `sign_gallbladderwall_unvivid`, `sign_diaphragm_unvivid` / `_unseen` (same task) | not both |
| R33 | P35, P49, P52 generic `tumor`, `cyst` (`check_disease__AnyOrgan`) | A8 (C4) | the organ-specific tumor and cyst tags of the same project (same task) | not both (label-guide Q12: generic only when no organ-specific tag fits); weak, two lesions can differ |
| R34 | P35, P49 every tag of group `check_disease__<Organ>` (disease, "no disease" and size tags) for an organ with an anatomy tag | A9 (C4) | the organ choice of group `check_anatomy`: `bladder`, `gallbladder`, `kidney`, `knee`, `liver`, `lung`, `prostate` (P35) or `prostate_gland` (P49), `spine`, `stomach`, `thyroid`, `uterus` (same task) | the organ is chosen whenever a tag of its disease group is |
| R35 | P52 disease polygons of group `check_disease__<Organ>` | A9 (C4) | the organ polygon of group `check_anatomy` (same task) | the organ is drawn; weak, drawing the organ may not have been asked |
| R36 | P9, P11, P14 `hepatorenal_contrast_liverbrighter` | A9 (C4) | `hepatorenal_contrast_possible` (same task) | "liver brighter" only where the contrast could be judged |
| R37 | P14 polygon tags of `fat_regions` and `liver_signs` | A9 (C4) | the organ polygon of the finding in group `anatomy_liver`: `liver`; `gallbladder` for `gallbladder_stone`; `stomach` for `gastric_tumor` (same task) | the organ is drawn whenever its finding is (organ layer, DEC-034) |

### 2.6 Visit of a labeling task (C3, derived)

Table 6. Rules on whether a labeling task (or labeling group) was visited (category C3
visited check, derived from the project design: QA report Table 12).

| Rule | Subject | Measure code | Target (scope) | Reading | Expected in the data |
|---|---|---|---|---|---|
| R38 | any given labeling of a labeling task, in every project except P3, P7, P11, P14, P52 | C3, derived | every tag of the project (same task) | visited: tags not given are true negatives | every submitted task (`task_stat` `annotated`) has a given labeling |
| R39 | any given labeling of a labeling group, P7 and P14 | C3, derived | the tags of that tag group only (same labeling group) | a group with nothing given and no group mark was not visited: its tags are missing | not testable from the tables (reading only) |
| R40 | a labeling task with no given labeling (`task_stat` `empty` or `draft`, `annotated` without any mark, or no crop row and no mark), all projects | C3 | every tag of the task | missing, not negative | none (definition) |
| R41 | a P11 labeling task | C3, none | P11 polygon tags not given | missing, never negative (no closing answer exists) | none (definition) |
| R42 | P14 `skip_untouched` | C3 (proposed, analyst; meaning not documented) | the labeling task (same task) | not visited: every tag missing | no other given labeling in the task |
| R43 | a P52 labeling task | C3, open | P52 polygon tags not given | open: the first 1,271 tasks were visited, the rest were not (QA report section 5) | to decide |

Table 7. Skip tags (subjects of R18 and R19) per labeling project of 261023, with their
role in the map. Q = role `quality`, E = role `exclusion`; * = in R19 (describes the image).

| Labeling project | Skip tags |
|---|---|
| P1 | `skip_toofat` E, `skip_lowdim` Q*, `skip_cropped` Q*, `skip_liver_c` E, `skip_otherdisease` E |
| P2 | `skip_notultrasound` E*, `skip_lowdim` Q*, `skip_anatomyunclear` E* |
| P3, P4 | `skip_notultrasound` E*, `skip_lowdim` Q*, `skip_coarse` Q* |
| P7 | `skip_lowdim` Q*, `skip_notliver` E, `skip_smallliver` E, `skip_otherdisease` E |
| P9 | `skip_coarse` Q*, `skip_blurred` Q*, `skip_darkened` Q*, `skip_smallliver` E, `skip_brightened` Q*, `skip_cropped` Q*, `skip_lowdim` Q*, `skip_notliver` E, `skip_anatomyunclear` E* |
| P11 | `skip_lowdim` Q*, `skip_notliver` E, `skip_anatomyunclear` E* |
| P14 | `skip_notultrasound` E*, `skip_coarse` Q*, `skip_paperscan` Q*, `skip_olddevice` Q*, `skip_darkened` Q*, `skip_notabdomen` E, `skip_smallliver` E, `skip_brightened` Q*, `skip_cropped` Q*, `skip_blurred` Q*, `skip_toomanyannotations` Q* (`skip_untouched`: R42) |
| P15, P20-24, P26-32 | `skip_badimagequality` Q* |
| P33 | `skip_anatomyunclear` E* |
| P35 | `skip_badimagequality` Q*, `skip_othercase` E |
| P36-39, P41-47, P50 | `skip_no_organ_found` E, `skip_badimagequality` Q* |
| P49 | `skip_badimagequality` Q*, `skip_notultrasound` E*, `skip_othercase` E |
| P19, P52 | none |

## 3. Rules between labeling projects

_(pending Section 1: staged routing B2, one finding per project B1, second pass B3, repeat
labeling inside one project B4 (proposed), and R19's families)_

## 4. Not used

- `hepatic_steatosis__unknown` (P1, P7 choice; P3 polygon): not used at all (QA report
  Amendment 1). A task with `unknown` and no grade has no steatosis label.
- A6 AI verdict (P33 `ai_correct`, `ai_almost`, `changed`) and A7 text notes: ignored
  (Amendment 1). The P33 verdict still counts as a given labeling for R38.
- `has_other_disease`, `has_other_anatomy` (P35, P49): category C5, no rule yet. A
  candidate: a sample with `has_other_disease` is not a "no disease" negative.

## 5. Open points

- R04 (`thyroiditis_abscent` targets), R10 (`heaptic_steatosis_absent` targets), R16
  (whether `hepatic_steatosis_checked` covers the disease tags of `fat_regions`).
- R19: whether a skip-sample reason leaves the sample out of every project (as C1 says),
  or only out of its own labeling task.
- The proposed codes A8, A9 and B4 are the analyst's; the QA report does not have them.
