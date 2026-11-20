---
id: DEC-083
title: RunPod pods download enc1 images from S3 by presigned URLs and back up encrypted checkpoints to S3 by a presigned POST policy (amends DEC-024)
status: accepted
area: [data-security, aws, infra, training]
created: 2026-11-20
from: [DIS-042]
related: [DEC-001, DEC-005, DEC-023, DEC-024, DEC-052, DEC-080]
superseded_by:
---
# DEC-083: RunPod data from S3, encrypted checkpoint backups to S3

## Context

Epic 1 runs on short-lived RunPod Secure Cloud pods ([DEC-080](DEC-080-epic1-optimisation-strategy.md) rule 5). Copying the enc1
store from machine01 to each pod is slow; S3 already holds the enc1 images ([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).
The user wants pods to read the images from S3 and to back up checkpoints to S3, so a pod
can be terminated soon after its run ([DIS-042](../discussions/DIS-042-runpod-data-from-s3-and-checkpoint-backups-to-s3.md)).

## Decision

1. **Images from S3, by presigned GET URLs.** Just before a pod starts, machine01 (the
   `agent-toolkit` profile) lists `s3://claude-agent-sonoai-data/datasets/<version>_enc1/`
   and signs one GET URL per object. The URL list goes to the pod (scp); the pod downloads
   it with aria2c into its store folder. The pod holds no AWS credentials. URLs expire with
   the signing session (at most 12 h); they are signed again for each pod.
2. **The rest of the store from machine01.** The non-image part of `<version>_enc1`
   (`manifest.enc`, `kdf.json`, `style` and the table blobs) is rsynced from machine01, so
   the pod's store equals the local one, and a store check passes before training. The S3
   copy stays images only (DEC-024 unchanged for datasets).
3. **Data on the pod's own disk**, downloaded per pod; no network volume for data. Any
   Secure Cloud data center with the GPU can be used.
4. **Checkpoint backups to S3, encrypted.** On the pod the trainer uploads `last.pt` (full
   state: model, optimiser, schedule, epoch) after these epochs `e` (1-based, of `E` total):
   - every 10th epoch;
   - every epoch with `e > 0.6 × E` that is the best so far (the epoch that writes `best.pt`);
   - the final epoch.

   Names carry the epoch: `runs/<run>/checkpoints/e010.pt.enc`, `e023_best.pt.enc`,
   `e030_last.pt.enc` (one file per epoch, suffix of the strongest rule). Each file is
   AES-256-GCM ciphertext with the **store key** (the key of `<version>_enc1`, already in
   RAM for training), AAD its path under `runs/<run>/`; the store's `kdf.json` (not secret)
   is copied to `runs/<run>/kdf.json`. So the **same passphrase** decrypts the backups, with
   `sonoai.secure`. Uploads run in the background; a failed one does not stop the run, is
   logged and retried at the next backup. The numbers 10 and 0.6 are options with these
   defaults.
5. **Write access by a presigned POST policy** signed on machine01 for the prefix
   `runs/<run>/` only, with a size limit and the session's expiry. A run that outlasts it
   keeps training; the user copies a fresh policy to the pod, which the uploader re-reads.
6. **On machine01** a command lists a run's backups, downloads the chosen ones and decrypts
   them in RAM into the run folder under the runs root. The small run files (config,
   metrics, eval records, logs) still go to machine01 by rsync before terminate. A new pod
   can resume from a backup (downloaded by presigned GET, decrypted on the pod).
7. **Amends DEC-024**: S3 may also hold run backups under `runs/`, enc1-style ciphertext
   only. The bucket policy allows `runs/*` keys ending in `.enc`, plus `runs/*/kdf.json`.

## Consequences

- Each pod start needs machine01 for the URL list, the POST policy and the rsync; the user
  is there anyway (DEC-080 rule 5).
- S3 transfer out (images to each pod, backups to machine01) is billed past 100 GB a month
  (about 0.09 USD/GB, unverified); backups are billed as storage until deleted.
- If the store is rebuilt with another passphrase, older backups still need the old one.
- Reversal: cheap. Go back to rsync of the store; delete `runs/` on S3.
- Tasks: [TASK-216](../../backlog/tasks/task-216%20-%20S3-bucket-for-RunPod-DEC-083-bucket-policy-allows-encrypted-run-backups-under-runs-and-the-261023_enc1-images-on-S3.md) (aws), [TASK-217](../../backlog/tasks/task-217%20-%20Presigned-S3-access-for-RunPod-pods-DEC-083-GET-URL-list-for-an-enc1-dataset-POST-policy-for-runs-run-pod-side-download-into-the-store-folder-synthetic-tests-with-a-fake-S3.md) and [TASK-218](../../backlog/tasks/task-218%20-%20Encrypted-checkpoint-backups-to-S3-from-RunPod-runs-DEC-083-rule-4-every-10th-epoch-best-so-far-past-60-percent-final-epoch-machine01-command-to-list-download-and-decrypt-them-resume-from-a-backup-synthetic-tests.md) (method), [TASK-219](../../backlog/tasks/task-219%20-%20RunPod-data-from-S3-in-run.sh-and-the-runbook-DEC-083-presign-on-machine01-aria2c-download-and-rsync-of-the-stores-non-image-part-on-the-pod-checkpoint-backups-on-fetch-backups-to-machine01.md) (infra); [TASK-197](../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md) waits
  on TASK-219.
