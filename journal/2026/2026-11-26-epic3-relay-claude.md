# 2026-11-26

Relay note for epic 3 (spot liver diseases, [DEC-100](../../decisions/DEC-100-epic3-mission-spot-liver-diseases.md),
the epic 3 mission): where the epic stands and what each next session takes on. Written by Claude
(Opus 5.5) at the user's request, at the end of the consult session of
[DIS-064](../../discussions/DIS-064-epic3-data-preparation-task-form-more-data.md) (epic 3 data
preparation, task form and more data). Not a decision; it points at the records that are. Aggregates only.

Terms: **spot classes** = `hepatoma`, `hemangioma`, `hepatic_cyst`, `hepatic_stone`; `ascites` is a
side class (DEC-100 rule 2). **Point** = one item of the order of later points in DEC-100 rule 7
(negatives and conflicts, split, more data, task form, metrics, model and optimisation,
organisation); DEC-100 names them but does not number them, so they are named here.

## Done

| Point | Records | What was decided | Board |
|---|---|---|---|
| Mission, classes, labels, bar | [DEC-100](../../decisions/DEC-100-epic3-mission-spot-liver-diseases.md) (mission), [DEC-101](../../decisions/DEC-101-group-skip-and-sample-label-index-v2.md) (labeling-group skip, index v2); [DIS-056](../../discussions/DIS-056-epic3-spot-liver-disease-mission.md) | 2D B-mode reader's aid on 261023; four spot classes plus ascites; strict_v1 (top) then loose_v1 on index v2; provisional bar sensitivity 0.80, specificity 0.90 on test groups | [TASK-262](../../../backlog/tasks/task-262%20-%20Labeling-group-skip-group_skip-in-the-fact-relations-config-the-sample-label-index-and-the-policies-shared-reading-index-tag-in-presence-table-names-tests-on-synthetic-tables-DEC-101.md) (code), [TASK-264](../../../backlog/tasks/task-264%20-%20Build-the-261023-sample-label-index-v2-labeling-group-skip-and-the-strict_v1-and-loose_v1-presence-tables-on-it-dataset-record-with-counts-per-class-and-state-against-v1-DEC-101.md) (index v2 built; [record](../../datasets/261023/sample_label_index_v2.md)): Done |
| Negatives and conflicts | [DEC-102](../../decisions/DEC-102-quality-skips-other-organ-projects-index-v2.md) (quality skips of other organs' projects), [DEC-103](../../decisions/DEC-103-epic3-negatives-and-contested-labels.md) (negatives, contested labels); [DIS-058](../../discussions/DIS-058-epic3-negatives-contested-labels-quality-skips.md) | Every known negative counts, reported in four parts by diffuse disease; own bar for specificity on cirrhosis negatives (value at the metrics point); contested labels unknown | [TASK-263](../../../backlog/tasks/task-263%20-%20Decide-epic-3-points-5-and-6-which-negatives-count-contested-labels-of-projects-35-and-36-and-whether-quality-skips-of-other-organs-projects-R19-set-aside-liver-labels-DIS-056.md), [TASK-269](../../../backlog/tasks/task-269%20-%20Second-fact-relations-config-of-261023-quality-skips-of-the-23-labeling-projects-of-other-organs-become-task-skips-test-and-docs-DEC-102.md): Done |
| Split | [DEC-108](../../decisions/DEC-108-epic3-split-test-and-validation-by-whole-groups.md) (split by whole datasource groups); [DIS-063](../../discussions/DIS-063-epic3-split-by-datasource-groups.md) | Test and validation each about 15%, whole groups; one split for every policy | [TASK-278](../../../backlog/tasks/task-278%20-%20Split-method-validation-by-whole-test-units-as-a-spec-option-and-the-epic-3-table-of-samples-to-split-with-its-sonoai-data-command-synthetic-tests-DEC-108.md) (code), [TASK-279](../../../backlog/tasks/task-279%20-%20Epic-3-split-on-261023-build-the-table-of-samples-to-split-run-the-feasibility-report-freeze-the-sample-file-with-the-DEC-108-limits-and-its-enc1-copy-dataset-record-per-split-and-class-DEC-108.md) (frozen; [record](../../datasets/261023/spot_e3_split.md)): Done |
| Data preparation (not a DEC-100 point) | [DEC-109](../../decisions/DEC-109-epic3-input-512-no-minimum-side-two-resize-modes.md) (input 512, two resize modes) | 512 x 512, no minimum crop side; stretch and fit-scale (aspect kept, padding image 0 and target background) compared by training | [TASK-282](../../../backlog/tasks/task-282%20-%20Fit-scale-resize-mode-in-the-sample-reader-aspect-kept-longer-side-fills-the-input-centred-padding-with-image-0-and-the-target-fill-stretch-stays-the-default-synthetic-tests-DEC-109.md) (fit-scale in the reader): To Do, ready |
| More data | [DEC-111](../../decisions/DEC-111-epic3-more-data-261023-only.md) (261023 only) | No book images; public sets postponed (maybe epic 4); author request sent by the user | none |
| Task form | [DEC-110](../../decisions/DEC-110-epic3-task-form-allowed-class-sets-stone-takes-the-overlap.md) (allowed-class sets) | One softmax over background, the four spot classes and ascites; Epic 1 allowed-class sets; a stone takes its overlap with a mass, as a task parameter; sigmoid comparison run later | [TASK-281](../../../backlog/tasks/task-281%20-%20Epic-3-task-seg_spot_v1-one-softmax-over-background-four-spot-classes-and-ascites-allowed-class-set-target-with-the-stone-taking-its-overlap-with-a-mass-synthetic-tests-DEC-110.md) (task seg_spot_v1): To Do, ready; [TASK-283](../../../backlog/tasks/task-283%20-%20Epic-3-sigmoid-comparison-run-after-the-first-softmax-results-one-sigmoid-per-class-with-an-unknown-class-masked-on-the-sample-on-the-chosen-recipe-DEC-110-rule-7.md) (sigmoid comparison): Parked |

Table 1. Epic 3 points settled as of 2026-11-26. All DECs listed are accepted.

## Observations

Numbers a next session needs, from the records above (aggregates).

| Item | Value | Source |
|---|---|---|
| Samples in the epic 3 sample file | 16,176 in 55 datasource groups; train 11,329 (30 groups), validation 2,426 (14), test 2,421 (11) | split record |
| Test positives: hepatoma / hemangioma / cyst / stone | 257 / 79 / 33 / 83 | split record |
| Cirrhosis negatives (hepatoma negative, cirrhosis positive) | train 305, validation 60, test 105 | split record |
| Contested samples (DEC-103 rule 4) | 112 train, 0 validation, 191 test | split record |
| Median lesion width at 512 input: hepatoma / hemangioma / cyst / stone | 85 / 39 / 40 / 19 px | DIS-064 Table 1 |
| Outline overlaps | 20 sample-class pairs; serious only for a stone inside a mass (13) | DIS-064 Table 3 |

Table 2. Key counts.

- **Thin spots** (split record point 3): validation hemangioma 22 and cyst 19 positives, from few groups;
  test hemangioma and cyst positives each from fewer than 5 groups. Per-class results there have no
  bar (DEC-100 rule 4) and wide intervals.
- **Group count**: DEC-108 rule 1 and DIS-063 say 57 groups; the data has 55 (the split record reads 57
  as a slip). Not corrected in those records.
- **Ascites positives**: DIS-064 counts 122 under the label `ascites`; DEC-102 gives 136. Not reconciled.
- **Gogs** (shared git server): the code `master` and `research_notes` `main` hold local commits not
  pushed; a push needs the user's go-ahead.

## Next

One session per row; the order is DEC-100 rule 7. "Can start" names what it waits for.

| # | Session | Scope | Can start |
|---|---|---|---|
| 1 | `/lead` | [TASK-281](../../../backlog/tasks/task-281%20-%20Epic-3-task-seg_spot_v1-one-softmax-over-background-four-spot-classes-and-ascites-allowed-class-set-target-with-the-stone-taking-its-overlap-with-a-mass-synthetic-tests-DEC-110.md) (task seg_spot_v1) and [TASK-282](../../../backlog/tasks/task-282%20-%20Fit-scale-resize-mode-in-the-sample-reader-aspect-kept-longer-side-fills-the-input-centred-padding-with-image-0-and-the-target-fill-stretch-stays-the-default-synthetic-tests-DEC-109.md) (fit-scale resize), two method agents; their files do not overlap | now |
| 2 | `/consult` | **Metrics**, [TASK-284](../../../backlog/tasks/task-284%20-%20Decide-epic-3-metrics-image-level-score-from-the-pixel-probabilities-scoring-of-a-stone-inside-a-mass-outline-the-cirrhosis-specificity-bar-from-the-test-counts-interval-method-DEC-100-rules-4-and-5-DEC-103-rule-3-DEC-110.md): image-level score from pixel probabilities; scoring of a stone inside a mass outline; final bar values; cirrhosis bar with 105 test cirrhosis negatives; group-bootstrap intervals; the descriptive table of the 191 contested test samples (DEC-103 rule 5); per-sample record; new task version or waiver ([DEC-004](../../decisions/DEC-004-training-tasks.md)). Creates the evaluation task | now (the split record is in) |
| 3 | `/consult` | **Model and optimisation**: architecture and pretraining (Epic 1 found the DINOv3 ConvNeXt-B recipes best at 224, [DIS-052](../../discussions/DIS-052-epic1-next-recipes-after-six-seed0-runs.md)); loss choice and weights, low importance of ascites; balancing method (DEC-100 rule 6); augmentation and normalisation at 512; checkpoint selection on validation groups | after 2 |
| 4 | `/lead` | Evaluation task from 2; recipe and model tasks from 3 | after 1 to 3 |
| 5 | `/consult` | **Organisation**: run plan (stretch against fit-scale, DEC-109 rule 3; strict_v1 then loose_v1, DEC-100 rule 3; seeds; RunPod), milestone check, EXP record layout | after 3 |
| 6 | exp session | First runs and the EXP record | after 4 and 5 |
| 7 | `/consult` | Sigmoid comparison run, [TASK-283](../../../backlog/tasks/task-283%20-%20Epic-3-sigmoid-comparison-run-after-the-first-softmax-results-one-sigmoid-per-class-with-an-unknown-class-masked-on-the-sample-on-the-chosen-recipe-DEC-110-rule-7.md); then code and run tasks | after 6 |

Table 3. Next sessions. Rows 2 and 3 could share one session if the user wants; 3 needs the
selection criterion from 2.

Not epic 3 (left as they are): [TASK-065](../../../backlog/tasks/task-065%20-%20Explain-the-6-labeling-projects-of-261023-with-no-crop-row-23-of-choice-pairs.md)
(projects with no crop row), [TASK-265](../../../backlog/tasks/task-265%20-%20Epic-1-candidate-builder-reads-the-presence-table-by-policy-only-pass-the-configs-index-tag-to-presence_name-DEC-101.md)
(index tag in the Epic 1 candidate builder), [TASK-266](../../../backlog/tasks/task-266%20-%20derived.md-presence-section-still-says-not-yet-built-for-261023-TASK-124-is-done-give-the-build-date-and-link-the-dataset-record.md)
(stale line in derived.md; check whether [TASK-274](../../../backlog/tasks/task-274%20-%20Docs-sample-label-index-v2-of-261023-is-built-update-derived.md-and-fact-driven-model.md-TASK-264.md), index v2 docs, already fixed it).
