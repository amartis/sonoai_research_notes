---
id: DEC-065
title: Mission of the first research epic - a working upper-abdomen anatomy segmentation model on 261023, trained from the strict_v1 presence table
status: accepted
area: [training, datasets]
created: 2026-11-17
from: [DIS-030]
related: [DEC-003, DEC-006, DEC-043, DEC-044, DEC-049, DEC-050, DEC-053, DEC-059, DEC-060, DEC-061]
superseded_by:
---
# DEC-065: Mission of the first research epic - a working upper-abdomen anatomy segmentation model on 261023, trained from the strict_v1 presence table

## Context

**Why now.** The cirrhosis model did not generalise. In [EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md),
the best run (cirr-v4-tu-e30-r5, pretrained TransUNet, 224 px) had cirrhosis DSC (Dice
similarity coefficient) 0.696 (95% CI 0.529–0.741) on val (n = 2,068 samples, 97 positive)
and 0.047 (0.005–0.143) on test (n = 1,378, 64 positive, datasource groups not seen in
training). Val was split at random from the train datasource groups
([DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 10, the user's
choice), so val shared datasources with train and could not show this gap before test.

**What is new.** The labels of 261023 can now be read through the fact-driven model
([DEC-059](DEC-059-fact-driven-model-sample-label-index-presence-policies.md)): the presence
table of policy `strict_v1` ([DEC-060](DEC-060-first-presence-policies-of-261023.md),
[DEC-061](DEC-061-a9-value-absent-target-side-and-task-123-readings.md)) gives, per sample and
content label, positive or negative; a missing pair is unknown. Counts:
[sample_label_presence.md](../datasets/261023/sample_label_presence.md) (strict_v1 table:
494,441 pairs, sha256 `05b3f423...fa77`). A **sample** is one crop of one image
([glossary](../../docs/glossary.md)).

**Term.** A **research epic** is one mission DEC plus the point decisions, board tasks, runs
and EXP records that carry it (the user's name, chosen in
[DIS-030](../discussions/DIS-030-mission-upper-abdomen-anatomy-segmentation.md)). It is not a
**plan** in the DEC-003 sense (how and where one recipe runs,
[training-concepts.md](../../docs/training-concepts.md)), and not a **milestone** (a board group
of tasks, [DEC-051](DEC-051-milestone-membership-rule.md)): this epic's tasks sit in milestone m-1
(train on dataset 261023). This DEC is the mission of **epic 1, upper-abdomen anatomy
segmentation**.

## Decision

### 1. Mission

Build the project's **first working model**: a 2D segmentation model that outlines the large
upper-abdomen organs on B-mode crops of dataset version 261023, trained and tested only on
labels the `strict_v1` presence table calls positive or negative, and shown to work on
datasource groups it never saw in training or model selection.

The model is the goal and also a test of the whole path (labels → sample set → split →
training → evaluation). Anatomy is chosen because it has the most labels, large and visible
targets, and less reader disagreement than disease extent; if this model fails on held-out
datasources, the path is at fault, not the hard disease task.

### 2. What "working" means (provisional bar)

Measured on the **test split** (datasource groups that are in neither train nor val), on the
checkpoint selected on val, with 95% CIs by cluster bootstrap over datasource groups (as in
EXP-003). The model works when all three hold:

| # | Criterion | Measure | Bar |
|---|---|---|---|
| W1 | Organs are outlined | DSC per class, mean over test samples where the class is positive | liver ≥ 0.85; every other first-set class ≥ 0.70 |
| W2 | No phantom organs | share of test samples where the class is a closed negative and the model predicts none of it | ≥ 0.90 per class |
| W3 | It generalises | val DSC minus test DSC, per class | ≤ 0.10 |

Table 1. The provisional bar of a working model. The numbers are our choice for a first
model, not taken from literature. The metrics session may change the bar before the first
full training run; after test results have been seen, the bar is not changed for that run.

### 3. Scope: which organs

The first model segments a **first set** of large organs. The **candidate pool** holds the
classes a later version may add. The final class list and target form are settled in the
model-task-definition session; this section bounds it.

| Content label | Region (labels-261023) | strict_v1 positive with polygon | strict_v1 negative (closed) | strict_v1 unknown | Place |
|---|---|---|---|---|---|
| `liver` | upper abdomen | 15,325 | 4,303 | 5,767 | first set |
| `kidney` | mid abdomen | 9,982 | 5,610 | 9,803 | first set |
| `stomach` | upper abdomen | 3,562 | 11,032 | 10,801 | first set |
| `gallbladder` | upper abdomen | 2,212 | 12,765 | 10,418 | first set |
| `spleen` | upper abdomen | 961 | 12,712 | 11,722 | first set |
| `hepatic_duct` | upper abdomen | 8,000 | 8,408 | 8,987 | pool (thin structure; meaning to confirm) |
| `intestine` | mid abdomen | 2,507 | 12,013 | 10,875 | pool |
| `portal_vein` | upper abdomen | 2,278 | 12,712 | 10,405 | pool (thin structure) |
| `hepatic_vascular_branch` | upper abdomen | 1,620 | 12,339 | 5,670 | pool (thin structure) |
| `diaphragm` | upper abdomen | 942 | 12,647 | 6,040 | pool (thin line) |
| `hepatic_blood_duct` | upper abdomen | 2,762 | 0 | 5,814 | out: no strict negative |
| `lung` | chest | 795 | 12,792 | 6,041 | out: chest |
| `heart` | chest | 24 | 13,583 | 6,022 | out: chest, too few |
| `common_biliary_duct` | upper abdomen | 86 | 13,497 | 5,968 | out: too few |
| `pancreatin` | upper abdomen | 62 | 13,578 | 5,989 | out: too few |
| `spine` | musculoskeletal | 39 | 13,583 | 6,007 | out: too few |

Table 2. Anatomy labels of 261023 that are outlined by polygon, with their sample-label pair
counts under `strict_v1` (one pair = one sample and one label), and their place in this
epic. Source: [sample_label_presence.md](../datasets/261023/sample_label_presence.md)
Tables 4 and 5; region column from [labels-261023.md](../../docs/labels-261023.md). Unknown
includes quality-skipped samples. `kidney` is listed as mid abdomen but is labelled in the
same anatomy projects and is kept in the first set.

### 4. Fixed inputs and rules

1. Dataset version **261023**, plain style on machine01
   ([DEC-018](DEC-018-plain-style-for-local-research.md)), enc1 copy for the GPU box.
2. Labels come only from the **`strict_v1` presence table** and the polygons of its positive
   pairs. An **unknown pair is never background**: a sample's unknown label adds no loss and no
   score for that label. `loose_v1` and `posrich_v1` are for later comparison only.
3. **Test is held out by datasource group** ([DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md)
   rule 2). Whether val is also held out by group is the splitting session's choice; the
   cirrhosis result is the reason to ask.
4. A fixed, versioned **sample file** under `derived/`
   ([DEC-053](DEC-053-table-naming-and-preservation.md)), with a dataset record of counts per
   split and class; aggregates only in committed text.
5. Training runs through the existing stack: recipes and plans
   ([DEC-003](DEC-003-trainrecipe-files-structure.md)), `sonoai.tracking.Run`, per-sample
   confusion matrices ([DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md)), the GPU box.
6. **Simplest working choice first.** Where two options are close, take the one already in
   the repo and already shown to train (for example a pretrained encoder over from scratch,
   EXP-003). New methods come after the bar is met.

### 5. Not in this mission

- Disease labels, signs, grades, and use of the model inside a disease task (a later
  epic may use its organ masks, for example as the organ layer of
  [DEC-043](DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md)).
- The best possible accuracy, architecture search, 3D or video.
- Dataset version 261105 (milestone m-2).
- Fixing the cirrhosis val-to-test gap (its own task; this epic may inform it).

### 6. The six points, one session each

Each point gets its own consult session and its own DEC that cites this one. Order (each
depends on the ones before it):

| Order | Point | Question to settle | What we know now | Starting lean (open) |
|---|---|---|---|---|
| 1 | Model task definition | Classes, target form, how positive / negative / unknown become loss and score | Labels are partly known per sample: a sample can have liver positive and spleen unknown | One output layer per class (sigmoid); polygon mask for positives, empty mask for closed negatives, loss masked out for unknowns |
| 2 | Data preparation | Which samples enter, min crop size, quality skips, choice-only positives, input size | 3,490 liver pairs are unknown as `sample_quality_skip`; some positives have no polygon | Samples with at least one first-set class positive or negative; choice-only positives give no mask loss |
| 3 | Splitting | Test and val units, sizes, class coverage per split | Cirrhosis val was random and hid the test failure | Test and val both held out by datasource group; each first-set class with enough positives in each |
| 4 | Metrics | Final bar, checkpoint selection rule, CI method | Section 2 bar is provisional | Section 2 bar; select on val mean DSC over the first set |
| 5 | Model choice | Architecture and pretraining | Pretrained TransUNet beat from scratch on val (EXP-003); registered: `resenc_unet`, `transunet`, `swin_unet`, `transunet_r50_b16` | A pretrained model already in the registry |
| 6 | Optimisation strategy | Loss, optimiser, schedule, augmentation, epochs, sanity steps | [DEC-006](DEC-006-losses-optim-tracking.md) defaults; `us_mild_v1` augmentation ([DEC-049](DEC-049-mild-ultrasound-augmentation-us-mild-v1.md)) | DEC-006 defaults; first overfit a small subset, then the full run |

Table 3. The six points of this epic in the order they are settled, with what is
already known and the lean each session starts from. A lean is not a decision.

## Consequences

- The six point sessions start from this DEC and do not reopen sections 1, 4 and 5 without a
  new DEC.
- The points are taken one at a time: each point's board tasks are created in its own session, after its DEC is accepted. (Changed by the user on 2026-11-17: the six Parked point tasks first made, [TASK-147](../../backlog/tasks/task-147%20-%20Epic-1-point-1-model-task-definition-classes-target-form-and-how-positive-negative-and-unknown-pairs-become-loss-and-score-DEC-065.md) to [TASK-152](../../backlog/tasks/task-152%20-%20Epic-1-point-6-optimisation-strategy-loss-optimiser-schedule-augmentation-epochs-and-sanity-steps-for-the-anatomy-model-DEC-065.md), were archived.)
- Build and training tasks are created only after their point DECs are accepted.
- If the bar of section 2 is not met, the EXP record says which criterion failed, and the
  next step is chosen in a consult session, not by tuning on test.
