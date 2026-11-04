---
id: DEC-041
title: Label groups (class maps) are set in the recipe; task code keeps the task kind
status: accepted
area: [training, labeling]
created: 2026-11-04
from: [DIS-017]
related: [DEC-003, DEC-004, DEC-034]
superseded_by:
---
# DEC-041: Label groups (class maps) are set in the recipe; task code keeps the task kind

## Context

[DEC-004](DEC-004-training-tasks.md) defines a task as type + labels + class map +
targets + metrics, all fixed in `src/sonoai/tasks/`, and bumps the task version for any
class-map change. The groupings in code (lesions by appearance in `lesions.py`, organ
lists, disease classes) therefore decide medical questions in Python: whether a finding
is a lesion or diffuse, which labels merge. The user's answers to [TASK-008](../../backlog/tasks/task-008%20-%20Proper-labeling-documentation.md) (Q6, Q9) and
[DIS-017](../discussions/DIS-017-label-groups-per-recipe.md) say these choices belong to
each training setup, with the label guide as a guide.

## Decision

Amends DEC-004 (class map in code, versioning) and [DEC-003](DEC-003-trainrecipe-files-structure.md) (recipe fields):

1. **The recipe sets the class map.** A recipe gives its classes and the label values
   that make each class (merged values, `IGNORE`, `VOID`). Plans do not change it: plans
   of one recipe train the same problem (DEC-003).
2. **Task code keeps the task kind**: target form (mask, boxes, organ + disease layers),
   sample eligibility, metrics, and the rule that a label value missing from the class
   map is an error. These still change only through a new version in code.
3. **The registered v1-v3 tasks stay**, unchanged and frozen, as examples and for any
   run that cites them. They are not extended with new groupings.
4. **Comparability:** each run stores the resolved spec (kind + class map) in `task.json`
   and its fingerprint in `meta.json`, as today. Results compare only when task kind,
   class-map fingerprint, dataset version and split all match. A recipe may give its
   grouping a short readable name; the fingerprint, not the name, decides.

## Consequences

- New groupings need no new task version in code; a mistake in a grouping is fixed in
  the recipe, and the fingerprint changes.
- Two recipes with the same kind but different groups are not comparable, even if their
  names look alike; reports must compare by fingerprint.
- TASK-008 Q6 (`gallbladder_polyp`, `gallbladder_tumor` as separate classes) becomes the
  first recipe grouping; Q8 and Q1 need no change (DIS-017).
- If many recipes repeat a grouping, shared named label sets under `configs/train/` can
  be added later (a new DEC).
- Carried out by [TASK-057](../../backlog/tasks/task-057%20-%20Apply-the-TASK-008-label-answers-to-the-task-code-disease-classes-ignored-labels.md) (method).
