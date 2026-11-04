---
id: DEC-034
title: The organ layer of disease tasks uses organ polygons only
status: accepted
area: [datasets, training]
created: 2026-11-03
from: [DIS-011]
related: [DEC-006, DEC-033]
superseded_by:
---
# DEC-034: The organ layer of disease tasks uses organ polygons only

## Context

[DEC-006](DEC-006-losses-optim-tracking.md) assumed diffuse diseases are outlined on the whole organ, so the layered
disease tasks (`lseg_*`) count steatosis, cirrhosis, precirrhosis and hepatitis
polygons as the liver in the organ layer (`ORGAN_OUTLINES` in
`src/sonoai/tasks/disease.py`). [DIS-011](../discussions/DIS-011-diffuse-disease-polygon-extent.md) concluded that a diffuse-disease polygon
covers only the area that shows the disease: it is a normal label, not evidence of
where the organ is. Counting it as the organ would teach "not organ" on organ area
nobody outlined, and in the graded steatosis task it decides which liver area is
ignored.

## Decision

Amends DEC-006 (organ layer and graded-disease rule):

1. The organ layer is drawn only from organ polygons (`liver` for the liver tasks).
   Disease polygons no longer count as the organ.
2. In a crop with no organ polygon, the organ layer is ignored (`ignore_index`), as
   DEC-006 already does when nothing outlines the organ.
3. Graded tasks (steatosis): with an organ polygon, organ area without a grade is
   ignored, as before. Without an organ polygon, everything outside the grade
   polygons is ignored in the disease layer, because whether it is liver is unknown.
4. The class map changes, so the affected tasks get a new version (`_v3`). Sample
   eligibility (organ evidence, disease projects) is unchanged.

## Consequences

- The organ layer trains on fewer crops. How many crops have a diffuse polygon but
  no organ polygon in 261023 is not yet counted (data task). If too many are lost,
  the fallback is to use diffuse polygons as the organ only where no organ polygon
  exists (option kept open, would be a new DEC).
- The disease layer is unchanged except rule 3. The organ layer is not scored
  (only the disease layer is assessed), so reported metrics are affected only
  through training and rule 3.
- No run used the v2 tasks, so nothing has to be re-run.
- If [DEC-033](DEC-033-precirrhosis-as-middle-grade-of-cirrhosis-task.md) (precirrhosis as a cirrhosis grade) is accepted, its task version
  follows this rule too.
- Carried out by [TASK-055](../../backlog/tasks/task-055%20-%20Layered-disease-tasks-treat-diffuse-disease-polygons-as-the-whole-organ-outline-but-they-may-cover-only-part-of-it.md); counted by `TASK-058` (data).
