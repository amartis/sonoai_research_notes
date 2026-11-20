---
id: DIS-042
title: RunPod pods get enc1 images from S3 and back up encrypted checkpoints to S3
status: concluded
created: 2026-11-20
outcomes: [DEC-083]
related: [DEC-001, DEC-005, DEC-023, DEC-024, DEC-052, DEC-080, DIS-008]
---
# DIS-042: RunPod pods get enc1 images from S3 and back up encrypted checkpoints to S3

## Question

Epic 1 runs on RunPod ([DEC-080](../decisions/DEC-080-epic1-optimisation-strategy.md) rule 5),
and each pod is rented for a short time. Copying the `261023_enc1` store from machine01 to
every pod is slow (machine01's uplink); a cloud-to-cloud download from S3, where the enc1
images already go ([DEC-024](../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)),
should be much faster. The user asked (2026-11-20) how a pod should get access to S3, and
added that checkpoints should go to S3 as well, so a pod can be terminated soon after its run.

## Options considered

**Read access from the pod.**

- **A, presigned GET URLs** (chosen): machine01 signs one URL per blob under
  `datasets/<version>_enc1/` just before a pod starts; the pod downloads the list (aria2c).
  No AWS credentials on the pod and no IAM change. A URL stops working when the signing
  credentials expire, so at most the 12 h of an `aws login` session
  ([AWS: presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url)).
- **B, short-lived STS role**: a read-only role assumed on machine01, its credentials handed
  to the pod (`aws s3 sync`). Simpler download, but IAM changes by the user and credentials
  on the pod.
- **C, read-only IAM user key** in a RunPod secret: works unattended, but a permanent key
  sits at a third party. Rejected.

**Tables.** The S3 copy holds images only (DEC-024); training also needs the store's
manifest and its table blobs (the enc1 copy of the epic 1 sample file, label tables).

- **A, rsync the non-image part from machine01** (chosen): images from S3, then rsync the
  rest of `261023_enc1` (manifest, `kdf.json`, `style`, table blobs: small). The pod's store
  equals the local one; DEC-024 is unchanged for datasets.
- **B, enc1 tables on S3 too**: only S3 needed, but amends DEC-024; would win if pods had to
  start while machine01 is off.

**Where the data sits on the pod.**

- **A, the pod's own disk, downloaded per pod** (chosen): no data-center lock, so any Secure
  Cloud A100 will do; no volume fee.
- **B, a network volume, filled once**: no per-pod download, and RunPod's S3-compatible API
  fills a volume without a pod, but only in a few data centers, and every pod must then run
  in the volume's data center
  ([RunPod: S3-compatible API](https://docs.runpod.io/storage/s3-api),
  [RunPod: network volumes](https://docs.runpod.io/storage/network-volumes)).

**Checkpoints** (the user's addition): encrypted on the pod with the store key (chosen) or
uploaded plain. Plain weights of a model trained on patient images would be readable to
anyone with bucket access; encrypted, S3 still holds ciphertext only, and the same
passphrase decrypts them. Write access by a presigned POST policy for the run's prefix
(chosen, matches the GET URLs) or an STS role. Which backups: the user chose every 10th
epoch, every epoch past 60 % of the run that is the best so far, and the final epoch, each
named by its epoch number.

**Cost.** S3 data transfer out to the internet: 100 GB a month free across the account,
then about 0.09 USD/GB in us-east-1 (third-party pages, 2026; not checked on AWS's own
pricing page):
[Cloudflare](https://www.cloudflare.com/learning/cloud/what-is-aws-data-transfer-pricing/),
[AWS News Blog, 100 GB free](https://aws.amazon.com/blogs/aws/aws-free-tier-data-transfer-expansion-100-gb-from-regions-and-1-tb-from-amazon-cloudfront-per-month).
Uploads into S3 are believed free (unverified). The store's size was not measured here
(`sonoai-data push-s3 261023_enc1 --dry-run` prints it). S3-to-RunPod speed is unmeasured.

## Conclusion

[DEC-083](../decisions/DEC-083-runpod-enc1-images-from-s3-and-encrypted-checkpoint-backups.md) (accepted 2026-11-20):
presigned GET URLs for the images, rsync of the store's non-image part from machine01, data
on the pod's disk, and encrypted checkpoint backups under `runs/` on S3 through a presigned
POST policy. Board tasks: [TASK-216](../../backlog/tasks/task-216%20-%20S3-bucket-for-RunPod-DEC-083-bucket-policy-allows-encrypted-run-backups-under-runs-and-the-261023_enc1-images-on-S3.md) (aws: bucket policy, image push), [TASK-217](../../backlog/tasks/task-217%20-%20Presigned-S3-access-for-RunPod-pods-DEC-083-GET-URL-list-for-an-enc1-dataset-POST-policy-for-runs-run-pod-side-download-into-the-store-folder-synthetic-tests-with-a-fake-S3.md) (method:
presigning, pod download), [TASK-218](../../backlog/tasks/task-218%20-%20Encrypted-checkpoint-backups-to-S3-from-RunPod-runs-DEC-083-rule-4-every-10th-epoch-best-so-far-past-60-percent-final-epoch-machine01-command-to-list-download-and-decrypt-them-resume-from-a-backup-synthetic-tests.md) (method: backups, fetch, resume), [TASK-219](../../backlog/tasks/task-219%20-%20RunPod-data-from-S3-in-run.sh-and-the-runbook-DEC-083-presign-on-machine01-aria2c-download-and-rsync-of-the-stores-non-image-part-on-the-pod-checkpoint-backups-on-fetch-backups-to-machine01.md) (infra:
run.sh and runbook); [TASK-197](../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md) now also waits on TASK-219.

## Open questions

- Should the small run files (config, metrics, eval records, logs) also go to S3,
  encrypted, at the end, so no rsync is needed before terminate? Not asked for; they go by
  rsync for now.
- How long backups are kept on S3 (lifecycle rule): not decided; kept until deleted.
