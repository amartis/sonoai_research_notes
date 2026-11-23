---
id: DEC-085
title: Global glossary term Checkpoint backup (encrypted copy of last.pt on S3, DEC-083), and the S3 bucket row also covers runs/
status: accepted
area: [workflow, training, infra]
created: 2026-11-23
from: [DIS-044]
related: [DEC-083, DEC-072, DEC-073, DEC-023]
superseded_by:
---
# DEC-085: Global term Checkpoint backup

## Context

[DEC-083](DEC-083-runpod-enc1-images-from-s3-and-encrypted-checkpoint-backups.md) rule 4 and [TASK-218](../../backlog/tasks/task-218%20-%20Encrypted-checkpoint-backups-to-S3-from-RunPod-runs-DEC-083-rule-4-every-10th-epoch-best-so-far-past-60-percent-final-epoch-machine01-command-to-list-download-and-decrypt-them-resume-from-a-backup-synthetic-tests.md) added encrypted checkpoint
backups from RunPod runs to S3. The phrase recurs in records, tasks, docs and code. Plain
"backup" is ambiguous here ([DIS-044](../discussions/DIS-044-checkpoint-backup-term-and-presign-lifetime.md)). The glossary row for the S3 bucket still says "enc1
images only".

## Decision

1. **Checkpoint backup** is a global term ([DEC-072](DEC-072-term-scopes-global-glossary-and-epic-terms-files.md) point 1), topic
   training, passing the screen of [DEC-073](DEC-073-how-new-terms-are-coined.md) point 1 as set out in DIS-044. Row: "An encrypted copy of a run's
   `last.pt` (full state) that the trainer uploads to the S3 bucket under
   `runs/<run>/checkpoints/` after the epochs of DEC-083 rule 4 (periodic, best epoch, last
   epoch); it decrypts with the store passphrase. Not the local `best.pt` / `last.pt`, not the
   Common box copies." Read more: DEC-083, this DEC.
2. The **S3 bucket** row becomes: "`claude-agent-sonoai-data`: holds enc1 images under
   `datasets/` and checkpoint backups under `runs/`, ciphertext only." Read more adds DEC-083.
3. The kinds of checkpoint backup (periodic backup, backup of the best epoch, backup of the
   last epoch) and "backups not yet uploaded" stay as descriptive words, with no rows.

## Consequences

- [TASK-222](../../backlog/tasks/task-222%20-%20Glossary-the-S3-bucket-row-also-covers-encrypted-checkpoint-backups-under-runs-DEC-083.md) applies both rows in the index table and the topic sections.
- Reversal: cheap. Rename the term and keep the old name under "Other names".
