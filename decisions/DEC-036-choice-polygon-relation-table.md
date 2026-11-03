---
id: DEC-036
title: Map every choice label to a role and related polygon labels, and report one choice-polygon relation table per dataset version
status: accepted
created: 2026-11-03
from: [DIS-012]
related: [DEC-012, DEC-018, DEC-034]
superseded_by:
---
# DEC-036: Map every choice label to a role and related polygon labels, and report one choice-polygon relation table per dataset version

## Context

[DIS-012](../discussions/DIS-012-choice-labels-vs-polygon-labels.md): choice labels can
double-check polygon labels, and some choice labels describe image quality. The user wants
one table that relates both kinds, with statistics, starting with 261023.

## Decision

- **Map.** `configs/data/choice_labels.yaml` gives each choice label of
  `docs/labels-261023.md`:
  - `role`: one of `presence`, `absence`, `checked`, `quality`, `exclusion`, `other`;
  - `polygons`: the related polygon labels (`presence`, `absence`), or `offered` for
    `checked` (the polygon labels its project offered, from `label_projects.yaml`);
  - an optional `note`.
  The map holds label names only, no data. The user reviews it before the run.
- **Unit.** An image region: `filepath2` plus `roi_i`, across all projects. A column also
  gives agreement within the same project.
- **Statistics per choice label.** Crops, datasources, projects; share of its crops with a
  related polygon (95% Wilson CI); conflicts: an absence choice with the polygon present,
  a presence choice with no polygon; for `quality` and `exclusion`, the share that still
  got polygons. Aggregates only; counts below 5 shown as <5.
- **Outputs.**
  - The table, one row per choice label, in one dataset record per version:
    `research_notes/datasets/<version>/choice_polygon_check.md` (first: 261023).
  - A per-region flag table in the dataset folder, `derived/choice_flags_df.pkl` (role
    flags and conflicts per region, no images), for building splits later.
- **Code.** `src/sonoai/data/choice_check.py` and a `sonoai-data choice-check` command;
  tests on synthetic tables only.

## Consequences

- The rule for leaving out `quality` and `exclusion` crops is a later decision, made with
  the table's numbers (Parked task).
- A changed map changes the table: the record names the map's commit.
- New dataset versions need their choice labels added to the map.
- Board tasks: [TASK-059](../../backlog/tasks/task-059%20-%20Map-every-261023-choice-label-to-a-role-and-related-polygon-labels-DEC-036.md) (`data`, the map), [TASK-060](../../backlog/tasks/task-060%20-%20Choice-polygon-relation-table-library-code-and-sonoai-data-choice-check-DEC-036.md) (`method`, the code), [TASK-061](../../backlog/tasks/task-061%20-%20Run-choice-check-on-261023_plain-and-write-the-choice-polygon-relation-record-DEC-036.md)
  (`data`, the 261023 run and record; after 059 and 060), [TASK-062](../../backlog/tasks/task-062%20-%20Decide-the-rule-for-leaving-out-quality-and-case-exclusion-crops-from-train-val-test-DIS-012.md) (Parked, the filtering
  rule; after 061).
