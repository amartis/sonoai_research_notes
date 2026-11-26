---
id: DEC-111
title: Epic 3 more data - train and test on the 261023 sample file only; no book images; public liver sets postponed (possibly epic 4); the request to the Tiyarattanachai 2021 authors is sent
status: accepted
area: [datasets]
created: 2026-11-26
from: [DIS-064]
related: [DEC-063, DEC-100, DEC-108]
superseded_by:
---
# DEC-111: Epic 3 more data

## Context

Point 8 (more data) of the epic 3 handoff in
[DIS-056](../discussions/DIS-056-epic3-spot-liver-disease-mission.md) (epic 3 mission discussion).
Counts of the book images and the public sets:
[DIS-064](../discussions/DIS-064-epic3-data-preparation-task-form-more-data.md) (epic 3 data
preparation, task form and more data), Facts checked.

## Decision

Accepted by the user on 2026-11-26.


1. **Epic 3 uses the epic 3 sample file of 261023 only**
   ([DEC-108](DEC-108-epic3-split-test-and-validation-by-whole-groups.md), epic 3 split, rule 5)
   for training, validation and test.
2. **No book images.** The labeling projects P49 and P52 (book images, no crop rows) and P1
   (steatosis scoring, not placed on samples) are not used in epic 3.
   [TASK-065](../../backlog/tasks/task-065%20-%20Explain-the-6-labeling-projects-of-261023-with-no-crop-row-23-of-choice-pairs.md)
   (projects with no crop row) keeps its own scope and is not an epic 3 task.
3. **Public liver sets are postponed**, possibly to epic 4: AUL, TCIA B-mode-and-CEUS-Liver and the
   others listed in DIS-056 handoff point 3. Each would need its record under
   [DEC-063](DEC-063-public-non-patient-datasets-root.md) (public non-patient datasets).
4. **The request to the authors of Tiyarattanachai 2021** (PLOS ONE,
   [10.1371/journal.pone.0252882](https://doi.org/10.1371/journal.pone.0252882)) was sent by the user
   before 2026-11-26. A reply, if any, is taken up in a new discussion; data received would be a new
   datasource and need its own decision.

## Consequences

- The epic 3 claim ([DEC-100](DEC-100-epic3-mission-spot-liver-diseases.md) rule 1) stays "agrees with readers on datasource groups of 261023 not
  seen in training"; there is no external test.
- Hemangioma and cyst stay at about 200 and 116 positives.
