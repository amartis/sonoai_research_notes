---
id: DEC-012
title: Dataset docs - style specs in docs/, one notes folder per dataset version
status: accepted
created: 2026-10-28
from: [DIS-003]
related: [DEC-002, DEC-005, DEC-008, DEC-011]
superseded_by:
---
# DEC-012: Dataset docs - style specs in docs/, one notes folder per dataset version

## Context

[DEC-002](DEC-002-dataset-files-structure.md) puts each style doc in `{data_files_root}/dataset_styles/<style>.md`
and "a copy or summary" in `research_notes/datasets/`. Each of those files
mixes a format spec (storage, images, tables, polygon coordinates, build and
check) with a "Datasets in this style" register. Code docstrings cite the notes
copy, which is not present on every machine. The labeling-project tag table of
version 261023 (label definitions, no patient data) sits gitignored at the
code repo root; `configs/data/label_projects.yaml` is exported from it.

## Decision

- **Style specs**: `docs/datasets/styles/<style>.md` in the code repo is the
  source of truth for each style's format ([DEC-011](DEC-011-docs-vs-research-notes.md)). Code and README cite it.
- **Data root copy**: `{data_files_root}/dataset_styles/<style>.md` stays, so
  the data describes itself, as a copy of the `docs/` spec (not edited there).
- **Dataset versions**: one folder per version in
  `research_notes/datasets/<version>/` (e.g. `261023/`), with `README.md` as
  the register: the styles built (codenames), built from, dates, check results,
  cleaning decisions and aggregate statistics. It takes over the "Datasets in
  this style" tables. There is no `research_notes/datasets/styles/`.
- **Tag table**: the 261023 table moves to
  `research_notes/datasets/261023/label_projects.xlsx` (renamed; no "(plain)").
  The notes `.gitignore` gets a narrow exception for `datasets/*/label_projects.xlsx`
  only; all other spreadsheets stay blocked.
- **`configs/data/label_projects.yaml`** names in its header the dataset
  version (and table) it was exported from.
- This replaces DEC-002's sentence "A copy or summary goes in
  `research_notes/datasets/` so the decision is versioned"; the rest of
  DEC-002 stands. Versioning of the specs now comes from the code repo.

## Consequences

- One source of truth per spec, versioned with the code that implements it.
- A dataset version's history and label definitions are found in one folder.
- Version folders hold text and the tag table only: no images, label files or
  identifiers.
