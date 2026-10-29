---
id: DIS-005
title: Dedicated labeling tool for review tasks, and a default env matching the GPU box
status: concluded
created: 2026-10-28
outcomes: [DEC-019, DEC-020]
related: [DEC-017, DEC-018, DEC-012]
---
# DIS-005: Dedicated labeling tool for review tasks, and a default env matching the GPU box

## Question

[TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) asks the user to review about 20 B-mode boxes per datasource (about
1,400 frames, 72 datasources). The first attempt used ipywidgets sliders in
the review notebook; the user found labeling inside VS Code not human
friendly (2026-10-28) and asked for a dedicated labeling tool, with one
labeling project per review task, driven end to end by the agent through the
tool's API.

Label Studio needs its own Python environment, which raised a second
question: which venv is the default on machine01.

## Options considered

- **Tool**:
  - **Label Studio** (pip, runs locally, no Docker): rectangle editing with
    pre-annotations (the cropper's boxes as editable proposals), keyboard
    shortcuts, a REST API and SDK for creating projects, importing tasks and
    exporting annotations; local file serving reads images from the data root,
    so nothing is uploaded. Our polygon coordinates are already in Label
    Studio's percent convention. Chosen.
  - CVAT: comparable box editing, but heavier (normally Docker, not installed
    on machine01) and nothing extra for box review.
  - Browser tools that upload images (e.g. makesense.ai): ruled out by the
    data rules.
  - Keep the notebook sliders: kept only as a fallback.
- **Where the server runs**: no labeling server exists today; the labels in
  use are files only. A server on machine02 could not serve plain data
  ([DEC-018](../decisions/DEC-018-plain-style-for-local-research.md)), so a local one on machine01, bound to 127.0.0.1.
- **Automation**: the user creates projects by hand vs. the agent drives
  everything through the API (create project, connect local storage, import
  tasks with pre-annotations, report progress, export and convert). The user
  chose full automation. Limits: the agent does not create accounts or handle
  passwords or tokens, so the user creates the one Label Studio account once
  and puts its API token in `.env`; code reads it from the environment.
- **Environment**: (A) a separate venv just for Label Studio next to
  `py310_for_ml`; (B) one new default venv that matches the GPU box training
  env (Python 3.12, torch 2.11.0) and also runs Label Studio. Label Studio
  1.23.2 needs Python >= 3.10 and numpy >= 2.2.6, compatible with our pins.
  The user chose B.

## Conclusion

Agreed with the user on 2026-10-28; carried by [DEC-019](../decisions/DEC-019-label-studio-review-projects.md) (Label Studio for
review projects, layout of their files) and [DEC-020](../decisions/DEC-020-default-venv-matches-gpu-box.md) (default venv), both
accepted 2026-10-28. Board tasks: [TASK-034](../../backlog/tasks/task-034%20-%20New-default-venv-py312_for_ml-matching-the-GPU-box-with-Label-Studio-DEC-020.md) (`infra`: the new default venv), [TASK-035](../../backlog/tasks/task-035%20-%20Local-Label-Studio-server-on-machine01-for-review-projects-DEC-019.md)
(`infra`: the local Label Studio server), [TASK-036](../../backlog/tasks/task-036%20-%20sonoai.labeling-package-and-sonoai-label-CLI-bmode_boxes-project-kind-DEC-019.md) (`method`: the
`sonoai.labeling` package and `sonoai-label` CLI). TASK-032 waits on
TASK-035 and TASK-036.

### Where labeling-project files live

| What | Where | In git |
|---|---|---|
| Code: API client, export/import per project kind, `sonoai-label` CLI | `src/sonoai/labeling/` | yes |
| Labeling interfaces (Label Studio XML), one per project kind | `configs/labeling/interfaces/<kind>.xml` | yes |
| Project definitions: task, kind, dataset, sample, source and result tables | `configs/labeling/projects/<task>-<slug>.yaml` (e.g. `task-032-bmode-boxes.yaml`) | yes |
| How-to | `docs/labeling.md` | yes |
| Per-project data: tasks file (image paths), raw exports | `<version>_plain/derived/labeling/<project>/` | no (data root) |
| Result tables (e.g. reviewed boxes) | `<version>_plain/derived/` (e.g. `bmode_review_df.pkl`) | no (data root) |
| Label Studio server state (database, uploads, logs) | `$SONOAI_LABELSTUDIO_ROOT`, default `$SONOAI_DATA_FILES_ROOT/labelstudio/` | no (data root) |
| URL and API token | `.env` (`SONOAI_LABELSTUDIO_URL`, `LABEL_STUDIO_API_KEY`) | no |
| Aggregate results per project | `research_notes/datasets/<version>/` | notes repo |

The labeling projects that produced the labels in use (tag tables and
`configs/data/label_projects.yaml`, [DEC-012](../decisions/DEC-012-dataset-docs-layout.md)) are historical and stay where
they are; review projects never modify the existing label tables.

## Open questions

- Telemetry: which Label Studio settings turn off usage reporting, checked in
  TASK-035.
- Whether machine01 gets a CUDA or a CPU build of torch 2.11.0 (machine01 is
  a VM; no GPU expected), settled in TASK-034.
