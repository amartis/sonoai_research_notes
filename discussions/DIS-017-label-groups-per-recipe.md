---
id: DIS-017
title: Label groups are chosen per recipe, not fixed in task code
status: concluded
created: 2026-11-04
outcomes: [DEC-041]
related: [DEC-003, DEC-004, DEC-034]
---
# DIS-017: Label groups are chosen per recipe, not fixed in task code

## Question

[TASK-057](../../backlog/tasks/task-057%20-%20Apply-the-TASK-008-label-answers-to-the-task-code-disease-classes-ignored-labels.md) was to apply the [TASK-008](../../backlog/tasks/task-008%20-%20Proper-labeling-documentation.md) label answers (docs/label-guide.md, section 3) as new
task versions in `src/sonoai/tasks/`. The Q9 answer says that whether a finding is a
lesion or diffuse is a medical question, and training should treat these labels as
disease. When asked how the next lesion versions should group labels, the user answered
(2026-11-04) that label groups (disease or organ, diffuse or lesion) should be decided
for each training setup, not hard-coded in Python; the label guide is a guide for
writing recipes and plans. Under [DEC-004](../decisions/DEC-004-training-tasks.md) each
task's class map is fixed in code, so this departs from a recorded decision.

## Options considered

Where the label groups live:

- **A, recipe** (chosen): under [DEC-003](../decisions/DEC-003-trainrecipe-files-structure.md) the recipe says *what* is trained and
  is machine-independent; plans of one recipe stay comparable.
- **B, plan**: lets one recipe vary its groups without a copy, but two plans of one
  recipe would then train different problems.

What stays in Python:

- **A, task kinds** (chosen): target form (mask, boxes, organ + disease layers), sample
  eligibility, metrics, and the "unknown label is an error" rule stay in code. The
  current v1-v3 tasks stay registered and frozen, as examples and for runs that cite them.
- **B, delete the old versions**: simpler code, but only safe if no run cites them
  (not checked).

How results stay comparable:

- **A, fingerprint** (chosen): each run stores the resolved class map and its
  fingerprint; results compare only when task kind, class-map fingerprint, dataset
  version and split match. A recipe may give its grouping a short name for reading.
- **B, shared named label sets** in YAML under `configs/train/`: better if many recipes
  reuse the same groups; can be added later on top of A.

## Conclusion

The user accepted the three defaults (A, A, A) on 2026-11-04:
[DEC-041](../decisions/DEC-041-label-groups-per-recipe.md). The other TASK-008 answers:
Q6 (`gallbladder_polyp` and `gallbladder_tumor` as two separate classes) becomes the
grouping of the first recipe that uses them, not a new task version. Q8 (`lung_disease_1`,
`lung_disease_2`, `vessel` ignored) and Q1 (`hepatic_steatosis__unknown` polygon ignored)
are already met by the current code: `lung_disease_1` is not used by any task,
`lung_disease_2` and `__unknown` have no polygons in 261023, and `vessel` is kept out of
the loss in `seg_anatomy_v1`. Carried out by TASK-057 (method).

## Open questions

- Whether any run cites the v1-v3 tasks (decides if they can ever be removed).
- Shared named label sets (option B of the third question), if recipes start repeating
  the same groups.
