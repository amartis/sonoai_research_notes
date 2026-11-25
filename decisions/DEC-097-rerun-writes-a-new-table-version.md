---
id: DEC-097
title: A writer that runs again writes the full table as the next version (_v2, _v3, ...) and never replaces the earlier file; identical content writes nothing; readers take the highest version unless given a name (applies DEC-053 to reruns)
status: accepted
area: [datasets, workflow]
created: 2026-11-25
from: [DIS-055]
related: [DEC-053]
superseded_by:
---
# DEC-097: A rerun writes a new table version

## Context

[DEC-053](DEC-053-table-naming-and-preservation.md) says a table, once written, is not changed.
[TASK-244](../../backlog/tasks/task-244%20-%20Table-writers-refuse-to-overwrite-an-existing-table-under-derived-DEC-053-now-that-members-write-to-the-shared-data-root.md) made the writers of `derived/` tables refuse to replace an existing file, but left three
writers that add rows to their existing table in place (`sonoai-label pull`, the AI-box import and
the quality import) as recorded exceptions. `sonoai-data label-summary` replaces its csv and md
under the reports folder, outside any dataset, on every run.

## Decision

1. **New version per rerun.** A writer whose table already exists writes the full new table as the
   next free version, `<name>_v2`, `_v3` and so on, the way sample files already do
   (`sonoai.data.sample_sets.write_sample_file`). The earlier file stays byte-identical.
2. **Identical content writes nothing.** The writer says the content is unchanged.
3. **Readers take the highest version** of a table name unless they are given a name. A record
   (EXP, dataset record) names the exact version it uses.
4. **Scope.** Tables under a dataset's `derived/` and report tables outside a dataset; the csv and
   md of `label-summary` are versioned together (both or neither).
5. Outdated versions stay where they are or move to `obsolete/` as DEC-053 says; none is deleted.

## Consequences

- [TASK-250](../../backlog/tasks/task-250%20-%20Each-pull-or-import-writes-a-new-versioned-result-table-instead-of-adding-rows-to-the-existing-one-DEC-053.md)
  (pulls and AI imports) and [TASK-251](../../backlog/tasks/task-251%20-%20label-summary-writes-a-new-version-of-its-csv-and-md-on-a-rerun-instead-of-replacing-them-DEC-053.md)
  (label-summary) carry it; the TASK-244 exceptions end with TASK-250.
- Readers outside `src/sonoai/labeling/` and in notebooks become follow-up tasks; `notebooks/human/`
  stays the user's.
- Disk use grows by one table per changed rerun; the tables are small.
- Not chosen for label-summary: refusing a rerun unless `--overwrite` is given by name, which keeps
  one fixed file name but loses the old content when used.
