---
id: DEC-053
title: Table naming logic_version_datastyle, and tables are preserved - new versions as new files, outdated ones to obsolete/
status: accepted
area: [datasets, workflow]
created: 2026-11-11
from: []
related: [DEC-018, DEC-037, DEC-044, DEC-052]
superseded_by:
---
# DEC-053: Table naming logic_version_datastyle, and tables are preserved - new versions as new files, outdated ones to obsolete/

## Context

On 2026-11-11 the user set two conventions for dataframes, data sheets and Excel
tables. Some tables already followed them (`derived/bmode_boxes_v2_df.pkl` kept v1
beside it, [DEC-037](DEC-037-cropper-v2-and-second-review-project.md); [DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md) says "a changed table is a new file name, never an
overwrite"), but no general rule was written down. The derived-tables doc still told
sessions to rebuild the box table with `--overwrite`.

## Decision

- **Naming (a convention, not a strict rule).** A new table's variable and file name
  use up to three parts, in this order: `<logic>_<version>_<datastyle>`, e.g. variable
  `taskcrops_261023_df`, file `taskcrops_261023_df.pkl`. All three are good to have;
  none is required (logic and datastyle are the usual coding habit anyway, so the
  convention mainly adds the version and fixes the order). The version is any short
  tag that identifies it, e.g. a date `261023`, `v2`, or a decision id `dec053`; it
  has no `_` and is valid in a Python name. Datastyle is the object kind (`df`), not
  the dataset style (`plain`, `enc1`). Existing tables keep their names.
- **Preservation.** A table, once written, is rarely changed. Overwriting or editing
  an existing table file needs the user's explicit yes, asked with a clear warning
  (which file, what changes, that the old content is lost). The table-list approval
  of [DEC-052](DEC-052-privacy-covers-images-tables-readable-after-asking.md) does not cover it.
- A table with added columns or a patch is a new file with a new version in its name.
- An obsolete or outdated table moves to `obsolete/` in its own directory (e.g.
  `derived/obsolete/`); it is not deleted.

## Consequences

- Rule text: [docs/conventions.md](../../docs/conventions.md) (new general doc,
  section "Tables: naming and preservation"), linked from `CLAUDE.md` (patient-data
  hard rules and Conventions) and the context map `docs/README.md`.
  [docs/datasets/styles/derived.md](../../docs/datasets/styles/derived.md) points to it,
  and its box-table note no longer says `--overwrite`.
- `make-enc` skips `derived/obsolete/` with the rest of `derived/`, but encrypts an
  `obsolete/` folder under `images/` or `labels/` into the enc1 store.
- Not changed: the `--overwrite` flags of `sonoai-data` (three commands). Without the
  flag they already refuse to replace a table; with it they replace the file instead
  of moving the old one to `obsolete/`. Changing that is a separate task.
- Not changed: [docs/command-policy.md](../../docs/command-policy.md) (only the user
  changes it); rule A10 does not yet name overwrites.
