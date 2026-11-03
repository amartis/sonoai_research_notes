---
id: DEC-029
title: Claude (Anthropic API) may label the frames of labeling projects the user names, starting with TASK-032
status: superseded
created: 2026-10-30
from: [DIS-009]
related: [DEC-017, DEC-019, DEC-024, DEC-026]
superseded_by: DEC-035
---
# DEC-029: Claude (Anthropic API) may label the frames of labeling projects the user names, starting with [TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md)

> Superseded on 2026-11-03, before acceptance, by [DEC-035](DEC-035-qwen3-vl-second-annotator-on-gpu-box.md): the user chose Qwen3-VL-8B
> (4-bit) on the GPU box instead of the Anthropic API. Nothing below took effect.

## Context

[DIS-009](../discussions/DIS-009-claude-as-second-annotator.md): the user wants Claude as a
second, blind annotator for the TASK-032 B-mode boxes. The user states that the frames come
from public datasets, and allows Claude to view them for the labeling projects the user
names. Until now
[DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)
let no plain image leave machine01, and command-policy rule D1 denies it.

## Decision

- **Allowed projects only.** The Anthropic API (model `claude-opus-5-5`) may receive the
  plain frames of labeling projects the user names here, one project at a time. The first
  is `task-032-bmode-boxes`: the 1,371 frames imported into its aws-labelstud project.
  - The allowed projects are the table below, mirrored in the code's `ALLOWED` list
    (`src/sonoai/labeling/ai_annotator.py`).
  - The code reads the frame list from the source project's state file and refuses any
    other frame.
- **How frames go.** A script on machine01 (`sonoai-label ai-label`) reads each frame in
  memory and sends it through the Message Batches API.
  - Nothing plain is written outside the dataset folder.
  - Only the frame's pixels and the guide's rules go; no file names or folder names.
  - The API key comes from `.env` (`ANTHROPIC_API_KEY`). Agents never see it.
- **Where the labels go.** A local mirror project on machine01
  (`task-032-bmode-boxes-ai`), under an `ai-annotator` account that the user creates.
  Its token is in `.env` (`LABEL_STUDIO_AI_API_KEY`).
- **Blind.**
  - Claude never sees the cropper's boxes.
  - The pipeline never reads the human's annotations until its own labels are frozen
    (model id, prompt hash and code version, recorded as `model_version`).
  - Tuning uses a fixed 72-frame subset of the sample, scored only against the cropper and
    the existing label polygons.
- **No change for agents' own tools.** The CLAUDE.md rule that agents never open images
  with their tools stays. So does the patient-data hook.

| Allowed project | frames | allowed on |
| --- | --- | --- |
| task-032-bmode-boxes | 1,371 | 2026-10-30 (on acceptance) |

## Consequences

- Partly supersedes DEC-024: the API sends frames of allowed projects to Anthropic.
  Everything else in DEC-024 stands.
- The user adds a matching exception to rule D1 in `docs/command-policy.md`. Only the user
  changes that file.
- `docs/services.md` (online services) and the patient-data section of `CLAUDE.md` name
  the exception.
- Each run costs money. The price is checked before the run (rule A4: ask).
- A frame sent to the API cannot be taken back. Adding a project to the table above is the
  user's decision each time.
