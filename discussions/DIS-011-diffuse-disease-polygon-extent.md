---
id: DIS-011
title: Diffuse-disease polygons may cover part of the organ
status: concluded
created: 2026-11-03
outcomes: []
related: [DEC-006, DIS-001]
---
# DIS-011: Diffuse-disease polygons may cover part of the organ

## Question

Should a diffuse disease (steatosis grades, cirrhosis, precirrhosis, hepatitis,
nephritis, cholecystitis, cystitis, thyroiditis, prostatitis) be drawn on the whole
organ, or only on the area that shows it? Raised as Q5 of the [TASK-008](../../backlog/tasks/task-008%20-%20Proper-labeling-documentation.md) label guide
(`docs/label-guide.md`), because [DEC-006](../decisions/DEC-006-losses-optim-tracking.md) counts the liver's diffuse-disease polygons
as the liver outline in the organ layer of the layered disease tasks
(`ORGAN_OUTLINES` in `src/sonoai/tasks/disease.py`).

Findings in dataset version 261023 (aggregates, measured in memory for TASK-008):
the measured diffuse liver labels cover a median of 97.7-105.4% of the liver
polygon, but some cover much less. Steatosis grade 1: median 101.3% of the liver
polygon (P25-P75 84.0-103.7, 4,809 crops). Grade 2: median 97.7% (P25-P75
66.0-101.9, 568 crops).

## Options considered

- **A, whole organ always**: keeps DEC-006's organ layer valid as it is. But it does
  not match how the disease shows, and some 261023 polygons already cover part of
  the organ. This was the guide's first proposed default.
- **B, the affected area only**: matches the disease and the existing drawings.
  But the organ layer can no longer treat these polygons as the organ outline.
- **C, the affected area, plus a separate organ polygon whenever a diffuse disease
  is drawn**: gives both layers clean targets for new projects, but costs more
  labeling and does not fix 261023.

## Conclusion

**B** (user, 2026-11-03): "Diffuse does not always mean affect the whole organ. So
let's just treat it as normal label." A diffuse-disease polygon covers the area that
shows the disease, which may be the whole organ or part of it. The label guide
(TASK-008) states this, and the old rule "draw a diffuse disease on the whole organ"
is removed.

The effect on the organ layer is not decided here. It goes to [TASK-055](../../backlog/tasks/task-055%20-%20Layered-disease-tasks-treat-diffuse-disease-polygons-as-the-whole-organ-outline-but-they-may-cover-only-part-of-it.md) (Parked
until decided), which will produce a DEC amending DEC-006.

## Open questions

- Organ layer for diffuse polygons (TASK-055): keep counting them as the outline,
  use them only where no organ polygon exists, or ignore the organ layer outside
  drawn organ polygons.
