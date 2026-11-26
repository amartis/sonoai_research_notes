---
id: DEC-110
title: Epic 3 task form - one softmax over background, the four spot classes and ascites with the Epic 1 allowed-class sets; a stone takes its overlap with a mass; a sigmoid comparison run later
status: proposed
area: [training]
created: 2026-11-26
from: [DIS-064]
related: [DEC-066, DEC-068, DEC-100, DEC-103, DEC-108, DEC-109]
superseded_by:
---
# DEC-110: Epic 3 task form

## Context

[DIS-064](../discussions/DIS-064-epic3-data-preparation-task-form-more-data.md) (epic 3 data
preparation, task form and more data) Table 3: outlines of two classes overlap on 20 sample-class
pairs; serious overlap is always a stone inside a mass (13); hepatoma, hemangioma and cyst only touch
at their edges (5). Table 5 compares one softmax with allowed-class sets (the user's plan) and one
sigmoid per class. Epic 1's form is [DEC-066](DEC-066-epic1-model-task-label-set-softmax.md)
(Epic 1 task definition: one softmax, an allowed-class set per pixel, label-set losses).

## Decision

1. **Classes and output.** Six classes in this order: background, `hepatoma`, `hemangioma`,
   `hepatic_cyst`, `hepatic_stone`, `ascites`. One softmax per pixel; the prediction is the argmax.
2. **Target: an allowed-class set per pixel**, by DEC-066 rule 3, with each class's strict_v1 state
   on index v2 from the epic 3 sample file
   ([DEC-108](DEC-108-epic3-split-test-and-validation-by-whole-groups.md), epic 3 split, rule 5):
   inside the outlines of positive classes, those classes; elsewhere background plus the unknown
   classes plus the positive classes without an outline; a negative class is never in a set.
   Contested pairs ([DEC-103](DEC-103-epic3-negatives-and-contested-labels.md), epic 3 negatives and
   contested labels, rule 4) are unknown, so they are never a background-only target.
   `ascites` joins the labels `ascites`, `liver_ascites`, `sign_liver_ascites` and
   `sign_liquid_near_liver` (one meaning, label-guide Q7).
3. **A stone takes its overlap with a mass.** Where an outline of a positive `hepatic_stone` overlaps
   an outline of a positive `hepatoma`, `hemangioma` or `hepatic_cyst`, the set is {`hepatic_stone`}
   alone. Every other overlap of positive classes keeps both (DEC-066 rule 3a). At scoring, a stone
   predicted inside a mass outline counts for that mass as well; the metrics point writes the scoring rule.
4. **Positives without an outline** (3 pairs) follow DEC-066 rule 3b. They give no image-level target
   in training. This amends [DEC-100](DEC-100-epic3-mission-spot-liver-diseases.md) rule 3 ("a positive without a polygon has an image-level target
   only") for the softmax form. They are scored at image level in validation and test.
5. **Image-level score per class** is taken from the pixel probabilities of the class; how is set at
   the metrics point. The per-sample record keeps it as a continuous value from the first run
   (DEC-100 rule 5).
6. **Losses**: the label-set losses of DEC-066 rule 4; the choice, weights and the low importance of
   ascites (DEC-100 rule 2) are set at the optimisation point.
7. **Sigmoid comparison run, later.** After the first softmax results, one comparison run of the
   chosen recipe with one sigmoid per class and the loss of an unknown class masked on the sample.
   Its code and plan are a later task; it does not block the first runs.

## Consequences

- Hepatoma loses about 5% of its outline as a training target on 13 samples (rule 3).
- The task is a new registered task kind; it reads the state and outline columns of the sample file.
  Its metrics come after the metrics point, so adding them changes its fingerprint ([DEC-004](DEC-004-training-tasks.md)): either a
  new version or a one-time waiver as in [DEC-076](DEC-076-epic1-metrics-label-set-score-selection-ci-and-pass-rule.md) rule 6.2, decided then.
- Code: a `method` task for the task definition and target (synthetic tests); a Parked task for the
  sigmoid comparison run.
- Reversal: before the task code, low; after training, new runs.
