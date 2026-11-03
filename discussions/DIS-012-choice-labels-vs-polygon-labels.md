---
id: DIS-012
title: Choice labels as a double check of polygon labels, and image-quality choices, in 261023
status: concluded
created: 2026-11-03
outcomes: [DEC-036]
related: [DEC-012, DEC-018, DEC-034]
---
# DIS-012: Choice labels as a double check of polygon labels, and image-quality choices, in 261023

## Question

Dataset version 261023 has 146 per-image choice labels next to its 114 polygon labels
(`docs/labels-261023.md`, from [TASK-008](../../backlog/tasks/task-008%20-%20Proper-labeling-documentation.md)). On 2026-11-03 the user noted:
- Many choices say that a related polygon label should be present (e.g. `gallbladder`,
  `hepatoma`) or absent (e.g. `renal_calculus_absent`, `kidney_nodisease`). They can
  double-check the polygons when the training, validation and test sets are built.
- Some choices describe image quality (e.g. `skip_blurred`, `skip_coarse`). Samples of poor
  quality could be left out of training.

The user wants one table that relates choice labels to polygon labels, covers image
quality in the same table, and carries statistics. The user asked whether leaving
poor-quality samples out of training makes sense.

## Options considered

**Unit of matching**
- **Same image region** (image file plus region, `filepath2` and `roi_i`, across all
  projects). Choices from projects 35 and 49 have no polygons in the same project; their
  polygons come from other projects. This is also the unit training uses. Chosen.
- **Same labeling task only.** Simpler, but misses every pair across projects.

**Roles of choice labels**
- **Six roles**: presence, absence, checked marker, image quality, case exclusion, other.
  Chosen. Some names mislead, so the roles keep them apart:
  - `skip_toofat`, `skip_otherdisease`, `skip_notliver`, `skip_liver_c`,
    `skip_no_organ_found` and similar say what the case is, not how good the image is.
    Dropping them as "bad quality" would remove hard or unusual cases.
  - `hepatorenal_contrast_*` sits in the `image_quality` tag group but describes a
    steatosis sign.
  - `checked` and `*_checked` mean the labeler looked: a missing polygon there is a true
    negative, which is itself a double check.
- **Three roles** (presence, absence, quality-or-skip): shorter, but mixes the two kinds of
  skip.

**Statistics**
- **Agreement and conflicts** per choice: crops, datasources, projects; share with the
  related polygon (95% Wilson CI); conflict counts in both directions; for quality and
  exclusion rows, the share that still got polygons. Chosen.
- **Counts only**: faster to read, no audit.

## Is leaving poor-quality samples out of training sensible?

Yes for training, with four limits (reasoning, not a cited source):
1. Only some projects offered quality choices. A crop without a quality flag is not known
   to be good; it may simply never have been asked.
2. The test set should look like what the model will see in use. If poor images occur in
   use, report test metrics on all crops and on the quality-filtered crops, not only the
   filtered ones.
3. Case exclusions (point above) are not quality and need their own rule.
4. Skipped crops often have no polygons at all. They must not count as negatives; the
   conflict columns of the table show how often this happens.

The filtering rule itself is not decided here. It waits for the table's numbers.

## Conclusion

Recorded in [DEC-036](../decisions/DEC-036-choice-polygon-relation-table.md): a hand-made map
from each choice label to its role and related polygon labels, code that computes the
relation table, and a dataset record with the table for 261023. Board tasks are listed in
DEC-036.

## Open questions

- The rule for leaving out poor-quality and case-exclusion crops from training and test
  (a Parked task, waiting on the table).
