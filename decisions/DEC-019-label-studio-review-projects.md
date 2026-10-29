---
id: DEC-019
title: Local Label Studio for review projects, one project per review task, driven through its API
status: accepted
created: 2026-10-28
from: [DIS-005]
related: [DEC-017, DEC-018, DEC-012]
superseded_by:
---
# DEC-019: Local Label Studio for review projects, one project per review task, driven through its API

## Context

Reviews such as [TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) (about 1,400 B-mode boxes) are too slow in notebook
widgets. No labeling server exists; plain data may not leave machine01
([DEC-018](DEC-018-plain-style-for-local-research.md)). [DIS-005](../discussions/DIS-005-labeling-tool-and-default-env.md).

## Decision

- **Tool**: Label Studio, installed in the default venv ([DEC-020](DEC-020-default-venv-matches-gpu-box.md)), running on
  machine01 only, bound to `127.0.0.1:8080`, with local file serving rooted at
  `$SONOAI_DATA_FILES_ROOT/datasets`. Server state in `$SONOAI_LABELSTUDIO_ROOT`
  (default `$SONOAI_DATA_FILES_ROOT/labelstudio/`). Sign-up disabled; usage
  telemetry off where Label Studio allows.
- **One project per review task**, named `<TASK-NNN> <topic> v<k>` (e.g.
  `TASK-032 B-mode boxes v1`), defined in
  `configs/labeling/projects/<task>-<slug>.yaml` and using an interface from
  `configs/labeling/interfaces/<kind>.xml`.
- **Automation**: `sonoai-label` (package `sonoai.labeling`) does every step
  through the API:
  - `server`: start Label Studio with the settings above;
  - `create <project>`: draw the sample, write the tasks file, create the
    project, connect local storage, import tasks with pre-annotations;
  - `status <project>`: done / total counts;
  - `pull <project>`: export annotations, keep the raw export, convert it to
    the result table.
  The agent runs these; the user only labels in the browser.
- **Credentials**: the user creates the single Label Studio account once and
  puts its API token in `.env` (`LABEL_STUDIO_API_KEY`). Code reads it from the
  environment and never prints, logs or stores it elsewhere; the agent never
  creates accounts or handles the password or token.
- **File layout**: as in DIS-005, "Where labeling-project files live". Tasks
  files and exports hold image paths, so they stay in
  `<version>_plain/derived/labeling/<project>/`; result tables in
  `<version>_plain/derived/`; only definitions, interfaces, code and docs are
  committed. Existing label tables are never modified.
- **First kind**: `bmode_boxes` (rectangle label `bmode`, up to two per frame,
  plus a "no B-mode image" choice), whose result table has the columns of the
  TASK-032 review table, so the review notebook's results cell reads it as is.

## Consequences

- Reviews happen in the browser at `localhost:8080`; notebook widgets are a
  fallback only.
- New review tasks add a project YAML (and a new kind only when needed).
- Label Studio state is patient data: it lives under the data root, is never
  committed and never shipped.
