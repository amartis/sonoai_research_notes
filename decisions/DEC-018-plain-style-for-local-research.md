---
id: DEC-018
title: Local research on machine01 uses the plain dataset style
status: accepted
area: [data-security, datasets]
created: 2026-10-28
from: []
related: [DEC-002, DEC-005, DEC-017]
superseded_by:
---
# DEC-018: Local research on machine01 uses the plain dataset style

## Context

[DEC-002](DEC-002-dataset-files-structure.md) and [DEC-005](DEC-005-enc1-dataset-style.md) made `enc1` the shippable copy of a dataset version and
`plain` the local, de-obfuscated one. In practice local work ([TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md), the
B-mode cropper review) went through the encrypted store as well, so every
step on machine01 asked for the passphrase and could not be run from a plain
terminal or a notebook without it. The user found this too troublesome
(2026-10-28) and set the rule below.

## Decision

- Research on machine01 (notebooks, analysis, `sonoai-data` runs, tables
  derived from a dataset) uses the **plain** style (`<version>_plain`), read
  directly from the data root (`sonoai.paths.dataset_dir`).
- The **enc1** style stays the only form that leaves machine01: the GPU box
  (machine02) and RunPod get the encrypted store, and code running there reads
  it with `EncryptedStore`. Use it locally only to build, check or ship it.
- Tables derived from a plain dataset (e.g. the B-mode box table and the
  reviewed boxes, [DEC-017](DEC-017-bmode-cropper.md)) are written inside that dataset's folder under
  `derived/`, never elsewhere. `make-enc` then carries them into the
  encrypted copy.
- Unchanged: no data, file names or identifiers in printed output, notes,
  tasks or commits; no copies of data outside the data roots (temp files,
  caches, exported crops); plain data never leaves machine01.

## Consequences

- Local tools and notebooks need no passphrase.
- `CLAUDE.md` ("Patient data: hard rules") states the rule.
- A table derived on plain reaches the GPU box only through a rebuilt or
  resumed `make-enc` and a re-ship.
- DEC-017's box table and reviewed set live in `<version>_plain/derived/`.
