---
id: DEC-035
title: Qwen3-VL-8B (4-bit) on the GPU box is the second, blind annotator for the TASK-032 B-mode boxes
status: accepted
created: 2026-11-03
from: [DIS-009]
related: [DEC-017, DEC-024, DEC-025, DEC-029]
superseded_by:
---
# DEC-035: Qwen3-VL-8B (4-bit) on the GPU box is the second, blind annotator for the [TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes

## Context

[DIS-009](../discussions/DIS-009-claude-as-second-annotator.md) chose Claude Opus 5.5 through
the Anthropic API as the second, blind annotator for the TASK-032 B-mode boxes
([DEC-029](DEC-029-claude-labels-named-labeling-projects.md), never accepted). That needed an
exception to [DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)
and to command-policy rule D1. On 2026-11-03 the user chose the other option from DIS-009:
an open vision-language model on the GPU box, so no frame leaves the user's machines.

## Decision

- **Model.** `Qwen/Qwen3-VL-8B-Instruct` from Hugging Face (Apache-2.0; checked on the
  Hugging Face API on 2026-11-03), loaded in 4-bit. The code pins the model revision. The
  4-bit method (bitsandbytes NF4 by default) is recorded with the labels.
- **Where it runs.** The Windows GPU box (RTX 3060). It reads the frames from the enc1
  store and decrypts them in memory (`EncryptedStore.read_*`), as DEC-024 already allows.
  No plain frame is written on the GPU box. The weights are already in the common box
  (`ml_research_commonbox`, [DEC-015](DEC-015-commonbox-runs-models.md)); they are not downloaded again.
- **Which frames.** Only the 1,371 frames of the TASK-032 labeling project
  (`task-032-bmode-boxes`). The code reads the frame list from that project and refuses
  any other frame.
- **What comes back.** Per frame: its frame key (no file name or folder name), at most two
  boxes in pixels, or "No B-mode image", and `model_version` (model id and revision, 4-bit
  method, prompt hash, code version). On machine01 this table lives in the dataset folder
  under `derived/`.
- **Where the labels go.** A local mirror project on machine01's Label Studio
  (`task-032-bmode-boxes-ai`), under an `ai-annotator` account that the user creates. Its
  token is in `.env` (`LABEL_STUDIO_AI_API_KEY`).
- **Blind.**
  - The model never sees the cropper's boxes.
  - The pipeline never reads the human's annotations until its own labels are frozen
    (`model_version` fixed).
  - Prompt tuning uses a fixed 72-frame subset of the sample, scored only against the
    cropper and the existing label polygons.
- **No change for agents' own tools.** Agents still never open images with their tools,
  and the patient-data hook stays.

## Consequences

- Supersedes DEC-029. DEC-024 and command-policy rule D1 are unchanged: no frame goes to
  Anthropic or any other outside service.
- The comparison with the human annotator follows once both label sets are done.
- The judgement on hard frames (two views, colour Doppler, no B-mode image) may be weaker
  than Claude's would have been. That is untested; the comparison will show it.
- The run uses GPU-box time and no money.
