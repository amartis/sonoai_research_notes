---
id: DIS-030
title: Mission of research epic 1 - a first working upper-abdomen anatomy segmentation model from the strict_v1 presence table
status: open
created: 2026-11-17
outcomes: [DEC-065]
related: [EXP-003, DEC-044, DEC-059, DEC-060, DEC-061]
---
# DIS-030: Mission of research epic 1 - a first working upper-abdomen anatomy segmentation model

## Question

The user wants training work built on the `strict_v1` presence table of 261023
([DEC-060](../decisions/DEC-060-first-presence-policies-of-261023.md)), starting with an
upper-abdomen anatomy segmentation model. The focus is a **first working model**, after the
cirrhosis model failed on held-out datasources
([EXP-003](../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md):
val DSC 0.696, test DSC 0.047). This session sets the mission in one DEC, detailed enough that
later sessions need not ask basic questions. Six points are then settled one per session:
data preparation, splitting, metrics, model task definition, model choice, optimisation
strategy.

## Options considered

**1. The bar for "working".**
- **A (chosen): a provisional bar now**, on test datasource groups seen in neither train nor
  val: liver DSC ≥ 0.85, other first-set organs ≥ 0.70, ≥ 90% of closed-negative samples with
  no predicted organ, val-minus-test DSC ≤ 0.10 per organ. The numbers are our choice, not from
  literature. The metrics session may change them before the first full run only.
- **B: criteria only, numbers in the metrics session.** Would win if the user wanted val
  results of a sanity run first.

**2. Which organs in the first model** (strict_v1 positives with polygon in brackets).
- **A (chosen): five large organs**: liver (15,325), kidney (9,982), stomach (3,562),
  gallbladder (2,212), spleen (961). Pool for a later version: hepatic_duct, intestine,
  portal_vein, hepatic_vascular_branch, diaphragm.
- **B: all ten.** Would win if thin vessels and ducts were needed now; risks the first result.
- **C: four, without kidney** (labelled mid abdomen in labels-261023). Would win if "upper
  abdomen" had to be literal.

**3. Name of the whole effort.** "Plan" already means how and where one recipe runs
([DEC-003](../decisions/DEC-003-trainrecipe-files-structure.md), glossary).
- Analyst's proposal: "training programme".
- **Chosen (the user's term): "research epic"**. No clash in docs, records or board.

**4. Order of the six points.** The user listed: data preparation, splitting, metrics, model
task definition, model choice, optimisation. The analyst set the order to model task
definition first, then data preparation, splitting, metrics, model choice, optimisation,
because the task definition (classes, target form, unknown handling) decides which samples
enter and how they are scored. Reversible; recorded in DEC-065 Table 3.

## Conclusion

[DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md) records the
mission, the provisional bar, the first set and pool of organs, the fixed inputs (261023,
`strict_v1` only, unknown is never background, test held out by datasource group), the
non-goals, and the six points with their starting leans.

Noted by the analyst: in the cirrhosis task, val was split at random within the train
datasource groups ([DEC-044](../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 10, the user's choice), so val could not show the test
failure. This is a likely contributor, not a confirmed cause; the splitting session takes it
up.

## Open questions

The six points of DEC-065 section 6, one consult session each.
