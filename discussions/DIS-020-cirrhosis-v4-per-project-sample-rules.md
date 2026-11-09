---
id: DIS-020
title: Per-project sample rules for cirrhosis v4 - case codes per project group, precirrhosis excluded, liver-area fallback
status: concluded
created: 2026-11-09
outcomes: [DEC-047]
related: [DEC-043, DEC-044, DEC-046, DEC-034, DIS-019]
---
# DIS-020: Per-project sample rules for cirrhosis v4

## Question

The user wants the samples of `lseg_cirrhosis_v4` chosen by explicit rules for each
labeling project, each outcome named by a case code (for example 7P1, 14E3), and a
fallback for the liver area when a crop has no liver polygon of its own. Today one strict
rule applies to all projects ([DEC-043](../decisions/DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md) rule 5) and a liver polygon is required.

Why now: no v4 run exists. [TASK-088](../../backlog/tasks/task-088%20-%20Train-lseg_cirrhosis_v4-on-the-fixed-sample-file-and-write-the-EXP-record-DEC-043-DEC-045.md) (first v4 training run) is blocked because the fixed sample
file holds 2,064 samples marked positive that have no polygon at all (a reader and
target bug, [TASK-092](../../backlog/tasks/task-092%20-%20Sample-reader-drops-every-flags_df-row-null-G-so-eligibility-and-the-organ-VOID-rule-miss-choices-and-offered-options.md)). The sample file must be frozen again anyway.

## What the configs show

- Only projects 7, 14, 36 and 52 offer the `hepatic_cirrhosis` polygon
  (`configs/data/label_projects.yaml`), so the user's project list covers every project
  with a cirrhosis outline. Project 1 offers a cirrhosis choice only and drops out.
- The `hepatic_cirrhosis` choice is offered in 7, 35 and 49. Project 14 has no cirrhosis
  choice; its cirrhosis polygon sits in the `fat_regions` group, whose "looked at" choices
  are `hepatic_steatosis_checked` and `heaptic_steatosis_absent`.
- Skip choices (`skip_*`): 7 (discard_reason), 14 (image_quality), 35, 36 and 49. Project
  52 has none.
- `hepatic_precirrhosis` is a polygon in 36 and 52 and a choice in 49.
- `cannotdiag` is in project 7's `tumor_check` group, not a cirrhosis label.

## Options considered

1. **Precirrhosis and `cannotdiag`.** The user's rules do not name them; read literally, a
   crop with only a precirrhosis polygon would be a negative.
   - **A**: exclude both (DEC-043 did).
   - **B**: follow the rules literally.
   - **C** (chosen): exclude precirrhosis; `cannotdiag` is an ordinary choice, because its
     group is about tumors, not cirrhosis.
2. **Project 14 negatives.** "At least one non-skip choice" includes `anatomy_checked`
   alone, where the labeler may never have looked at the cirrhosis polygon group.
   - **A** (chosen): 14P1 and 14N1 need `hepatic_steatosis_checked` or
     `heaptic_steatosis_absent`.
   - **B**: any non-skip choice.
3. **Liver fallback.** What counts as "liver-related", and what if there is none at all.
   - **A** (chosen): liver, the structures merged into it, and liver disease and sign
     polygons, from every crop of the same image; a sample with no liver area still
     takes part, and pred-in-liver is reported over the samples with a liver area.
   - **B**: organ outlines only.
   - **C**: exclude samples with no liver area.

## Conclusion

The user accepted the rules with 1C, 2A and 3A on 2026-11-09:
[DEC-047](../decisions/DEC-047-cirrhosis-v4-cases-per-project-group-and-liver-fallback.md). The task keeps
the name `lseg_cirrhosis_v4` because nothing was trained on it; the new sample file gets a
new file name ([DEC-044](../decisions/DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) rule 7). The user asked to see the count of every case code.

Board: TASK-092 (reader keeps flags rows) to To Do; [TASK-096](../../backlog/tasks/task-096%20-%20Cirrhosis-v4-sample-cases-per-project-group-7-14-3635-5249-with-case-codes-precirrhosis-excluded-and-the-liver-area-fallback-DEC-047.md) (`method`, case rules and
liver fallback in code); [TASK-097](../../backlog/tasks/task-097%20-%20Re-freeze-the-cirrhosis-v4-sample-file-under-the-DEC-047-cases-dataset-record-with-one-count-per-case-code-per-group-and-per-split.md) (`data`, new freeze, counts per case); TASK-088 waits
for TASK-097.

## Open questions

- Assumptions stated in DEC-047 (the "52N1 (49, 36)" typo read as (49, 52); crops in two
  project groups; unpaired 35/36 and 49/52 crops counted as 36U and 52U). The user can
  change them after seeing the TASK-097 counts.
