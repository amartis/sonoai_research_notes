---
id: DEC-030
title: A public copy of the TASK-032 labeller's guide, with its 8 example frames served from S3
status: proposed
created: 2026-10-30
from: []
related: [DEC-023, DEC-024, DEC-025, DEC-029]
superseded_by:
---
# DEC-030: A public copy of the [TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) labeller's guide, with its 8 example frames served from S3

## Context

The labeller's guide for TASK-032 is at `/guide/task-032/` on aws-labelstud
([DEC-025](DEC-025-aws-labelstud-public-https.md)). Only logged-in users can see it. It
holds 14 drawn diagrams and 8 example frames, which the image server decrypts from
`261023_enc1`. The user wants a public copy that anyone with the link can open, with the
frames served from S3 instead of the image server. The user states that these frames come
from public datasets. No record says which datasources are public (see
[DIS-009](../discussions/DIS-009-claude-as-second-annotator.md), open questions).
[DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md) and
command-policy rule D1 deny sending plain images off machine01.

## Decision

- **Only these 8 frames.** The 8 example frames in the built guide
  (`build/labeling/task-032-bmode-boxes/index.html`, built 2026-10-30) may be published
  as plain image files. No other frame is covered.
- **Where they go.** A new bucket, `claude-agent-sonoai-guide`, private, served only through
  CloudFront (HTTPS). The frames are stored under blob-id names (no file or folder names
  from the dataset). They are not stored in `claude-agent-sonoai-data`, which stays
  enc1-only ([DEC-023](DEC-023-aws-s3-for-enc1-and-ec2-for-label-studio.md)).
- **What the page holds.** The guide's text and diagrams, and the 8 frames with their
  captions. It holds no file names, no Label Studio links that need a login, and no tokens.
- **How frames go.** A script on machine01 reads each frame from `261023_plain` in memory
  and uploads it. Nothing plain is written outside the dataset folder.

## Consequences

- Partly supersedes DEC-024 for these 8 frames only. Everything else in DEC-024 stands.
- The user adds a matching exception to rule D1 in `docs/command-policy.md`. Only the user
  changes that file.
- A published frame cannot be taken back: anyone may copy it, and caches may keep it after
  the bucket is deleted.
- Adding frames, or publishing another guide, needs a new decision.
