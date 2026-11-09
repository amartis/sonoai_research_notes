---
id: DEC-047
title: Cirrhosis v4 sample rules per project group with case codes, precirrhosis excluded, liver-area fallback
status: accepted
area: [training, datasets]
created: 2026-11-09
from: [DIS-020]
related: [DEC-043, DEC-044, DEC-046, DEC-034]
superseded_by:
---
# DEC-047: Cirrhosis v4 sample rules per project group, liver-area fallback

## Context

[DIS-020](../discussions/DIS-020-cirrhosis-v4-per-project-sample-rules.md). The user set
explicit sample rules for `lseg_cirrhosis_v4`, one set per labeling project group, each
outcome with a case code. This **replaces rule 5 (eligibility) of [DEC-043](DEC-043-cirrhosis-task-gt-organ-layer-predicted-cirrhosis-only.md)
and the liver part of its organ layer (rules 2-3)**. DEC-043 rules 1, 4, 6 and 7, the rest
of rules 2-3, and [DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) as changed by [DEC-046](DEC-046-cirrhosis-v4-drops-the-qwen3-vl-quality-step.md) stay. Nothing was trained on v4 yet, so the
name stays `lseg_cirrhosis_v4`; the new sample file has a new file name.

Terms: **included** = the sample takes part; **excluded** = it does not. **Positive** /
**negative** = cirrhosis present / absent. A **skip label** is a choice whose name starts
with `skip_`. "Polygon cirrhosis" = a `hepatic_cirrhosis` polygon; "choice cirrhosis" =
the `hepatic_cirrhosis` choice.

## Decision

### 1. Project groups

A sample (one image plus one crop box, DEC-044 rule 1) is judged in each group it belongs
to:

| Group | Polygons from | Choices from | Membership |
|---|---|---|---|
| 7 | 7 | 7 | the crop is in project 7 |
| 14 | 14 | 14 | the crop is in project 14 |
| 36 | 36 | 35 and 36 | the crop is in 36; it must also be in 35, else case **36U** (excluded) |
| 52 | 52 | 49 (52 has none) | the crop is in 52; it must also be in 49, else case **52U** (excluded) |

Pairing (35 with 36, 49 with 52) uses the same image hash and crop box.

### 2. Cases, checked in this order within a group (first match wins)

**Group 7, 36, 52** (`G` = 7, 36 or 52; "choice" means a choice of the group's choice
projects):

| Case | Condition | Outcome |
|---|---|---|
| GE4 | a skip label in the group's projects | excluded |
| xE5 | a `hepatic_precirrhosis` polygon or choice in any project of the sample | excluded |
| GP1 | choice cirrhosis and polygon cirrhosis | **positive**, included |
| GE1 | no choice cirrhosis, polygon cirrhosis | excluded |
| GE2 | choice cirrhosis, no polygon cirrhosis | excluded |
| GN1 | neither, and at least one other polygon or non-skip choice in the group's projects | **negative**, included |
| GE3 | neither, and nothing else | excluded |

`cannotdiag` (project 7, tumor_check group) is an ordinary choice: it is not a skip and it
counts for 7N1.

**Group 14** ("looked" = the choice `hepatic_steatosis_checked` or
`heaptic_steatosis_absent`, which show the `fat_regions` group holding the cirrhosis
polygon was looked at):

| Case | Condition | Outcome |
|---|---|---|
| 14E4 | a skip label in project 14 | excluded |
| xE5 | as above | excluded |
| 14P1 | polygon cirrhosis and looked | **positive**, included |
| 14E1 | polygon cirrhosis, not looked | excluded |
| 14N1 | no polygon cirrhosis, looked | **negative**, included |
| 14E3 | no polygon cirrhosis, not looked | excluded |

The user's rule asked for "at least one non-skip choice positive"; on 2026-11-09 the user
narrowed it to the two fat_regions choices (DIS-020 option 2A).

### 3. A crop in more than one group (assumption, the user may change it)

- Groups with case `E3` or `U` (nothing to judge in that group) are ignored.
- If any remaining group gave `E4` or `xE5`, the sample has that case.
- Else, if all remaining groups include it with the same outcome, it is included with
  that outcome.
- Else (one says positive and another negative, or one includes and another gave `E1` or
  `E2`), it is excluded as case **xC1**.

The sample file keeps every group's case; the counts report the combinations.

### 4. After the cases

DEC-044 rule 4 still applies: other `quality` or `exclusion` choices of any project of
the sample, and frames skipped in the "[TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes v1" review, drop the sample.
So do the 128 px minimum crop side (rule 5) and the split rules (rules 8-11). The counts
are reported after each step.

### 5. Liver area in the organ layer

1. If the sample's own rows (all its projects) have a `liver` polygon, the liver class is
   drawn as in DEC-043: `liver` and the structures merged into it (`portal_vein`,
   `hepatic_vascular_branch`, `hepatic_blood_duct`, `hepatic_duct`).
2. Otherwise the liver class is the union of the liver-related polygons:
   - `liver` and the merged structures;
   - liver disease and sign polygons (`LIVER_FINDINGS` in `sonoai.tasks.cirrhosis`).

   They are taken from every `taskcrops_df` row of the same image (any crop box, any
   project), mapped into this crop and clipped to it.
3. If neither gives any pixel, the sample still takes part. Its organ layer has no
   liver, and it does not count in pred-in-liver.

The other organ classes and the VOID rules of DEC-043 rule 3 stay.

### 6. Reporting

- The sample file has a column with the final case and one with each group's case.
- The freeze and the dataset record give a table with one row per case code: 7P1, 7N1,
  7E1-7E4, 14P1, 14N1, 14E1, 14E3, 14E4, 36P1, 36N1, 36E1-36E4, 36U, 52P1, 52N1,
  52E1-52E4, 52U, xE5, xC1. Each row gives the count, zero counts included. Group cases
  count each crop-group pair once.
- Also reported: the number of samples whose liver comes from the fallback (5.2) and with
  no liver area (5.3), overall and per split.
- Pred-in-liver (DEC-043 rule 6) is computed over the samples with a liver area, with
  that n.

### 7. Assumption

In the user's 52N1 rule, "(project 49, 36)" is read as "(project 49, 52)".

## Consequences

- The "must have a liver polygon" requirement is gone, so more samples can take part; some
  have a fallback liver or none.
- A sample with only a precirrhosis label is excluded, not a negative.
- Work:
  - `method`: [TASK-092](../../backlog/tasks/task-092%20-%20Sample-reader-drops-every-flags_df-row-null-G-so-eligibility-and-the-organ-VOID-rule-miss-choices-and-offered-options.md) (the reader keeps choice rows), then [TASK-096](../../backlog/tasks/task-096%20-%20Cirrhosis-v4-sample-cases-per-project-group-7-14-3635-5249-with-case-codes-precirrhosis-excluded-and-the-liver-area-fallback-DEC-047.md) (case rules
    and liver fallback);
  - `data`: [TASK-097](../../backlog/tasks/task-097%20-%20Re-freeze-the-cirrhosis-v4-sample-file-under-the-DEC-047-cases-dataset-record-with-one-count-per-case-code-per-group-and-per-split.md) (new freeze and dataset record with the case table);
  - `exp`: [TASK-088](../../backlog/tasks/task-088%20-%20Train-lseg_cirrhosis_v4-on-the-fixed-sample-file-and-write-the-EXP-record-DEC-043-DEC-045.md) runs on the new file.
