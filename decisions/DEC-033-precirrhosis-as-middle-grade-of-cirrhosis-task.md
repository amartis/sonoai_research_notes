---
id: DEC-033
title: Precirrhosis returns to the cirrhosis task as the middle of three ordered grades
status: proposed      # proposed | accepted | superseded
area: [training]
created: 2026-11-02
from: [DIS-001]
related: [DEC-004, DEC-006]
superseded_by:
---
# DEC-033: Precirrhosis returns to the cirrhosis task as the middle of three ordered grades

## Context

[DIS-001](../discussions/DIS-001-deferred-disease-task-questions.md), item 1, and board task
[TASK-001.01](../../backlog/tasks/task-001.01%20-%20Decide-whether-precirrhosis-returns-to-the-cirrhosis-task.md). `lseg_cirrhosis_v2` ([DEC-006](DEC-006-losses-optim-tracking.md)) leaves out every
sample with a `hepatic_precirrhosis` polygon (205 samples in dataset 261023), so that data is
not used.

Medical background:

- "Precirrhosis" is not a term of the main staging systems. A search found no definition in
  guidelines or reviews. The nearest standard terms:
  - METAVIR fibrosis stages (biopsy): F3 = many septa without cirrhosis, F4 = cirrhosis.
    Stage wording checked on secondary tables only; the primary paper (Bedossa and Poynard,
    1996) was not read.
  - cACLD, compensated advanced chronic liver disease (Baveno VI consensus): F3 and F4
    together in patients without symptoms, because tests other than biopsy cannot separate
    them well. Liver stiffness < 10 kPa rules it out and > 15 kPa strongly suggests it
    (de Franchis 2015, [doi:10.1016/j.jhep.2015.05.022](https://doi.org/10.1016/j.jhep.2015.05.022)).
    A study of 5,648 patients proposed < 8 and > 12 kPa instead (Papatheodoridi 2021,
    [doi:10.1016/j.jhep.2020.11.050](https://doi.org/10.1016/j.jhep.2020.11.050)).
- B-mode images separate the stages poorly. In 156 patients with chronic viral hepatitis
  and biopsy as reference, a three-sign ultrasound score detected F4 with 66% accuracy and
  >= F3 with 62% (Choong 2012,
  [doi:10.4103/2156-7514.101000](https://doi.org/10.4103/2156-7514.101000)). Expect readers
  and models to confuse precirrhosis with cirrhosis.
- Assumption, not checked: our annotators used "precirrhosis" for a liver with early signs
  (coarse texture, slightly blunt edge) but no clear cirrhosis (for example surface nodules).
  The project's labels carry no biopsy or elastography result.

Options (DIS-001): keep precirrhosis out (as now); merge it into cirrhosis; or add it as its
own class with half credit for a neighbouring miss.

## Decision

1. **Ask the annotators first.** Before the new task is built, the labeling team states in
   one or two sentences what separated precirrhosis from cirrhosis and from a normal liver.
   If they used no consistent rule, this decision is withdrawn and precirrhosis stays out.
2. **New task version `lseg_cirrhosis_v3`.** The disease layer has three ordered classes:
   background (0), precirrhosis (1), cirrhosis (2). Cirrhosis is drawn after precirrhosis, so
   cirrhosis wins where the two polygons overlap.
3. **Scoring.** Same rule as steatosis grades (DEC-006):
   `ordinal_satisfaction(3, {0: 1.0, 1: 0.5})`. Exact class 1.0, one step off 0.5 (for
   example cirrhosis predicted as precirrhosis), two steps off 0.
4. **Samples.** Same eligibility as v2 without the `exclude` rule, so the 205 samples join.
5. **v2 stays registered** for comparison with runs already made. Changing the classes or the
   scoring is a new task version ([DEC-004](DEC-004-training-tasks.md), DEC-006).

## Consequences

- About 205 more samples train and score. Their split assignment follows the existing
  datasource split; no split changes.
- Background in the disease layer covers both the liver without disease and the area outside
  the liver. So a precirrhosis prediction outside the liver earns 0.5 instead of 0. Check this
  with the first run; if it inflates scores, restrict the half credit to liver pixels (a
  method change and a new version).
- Reported results for v3 must also give the cirrhosis-vs-rest score (precirrhosis counted
  as not cirrhosis), so they stay comparable with v2.
- Work: a `method` task (touches `src/sonoai/tasks/disease.py`, synthetic tests) after this
  decision is accepted and step 1 is answered. Closes TASK-001.01.
- If precirrhosis turns out to be used inconsistently, merging it into cirrhosis is not the
  fallback: keeping it out is, because merging would teach early signs as cirrhosis.
