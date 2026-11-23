---
id: DIS-044
title: Follow-ups of TASK-218 - the global term checkpoint backup, and how long the RunPod presigned URLs and POST policy last
status: concluded
created: 2026-11-23
outcomes: [DEC-085, DEC-086]
related: [DEC-083, DEC-072, DEC-073, DEC-024, DIS-042]
---
# DIS-044: Checkpoint backup as a global term, and the lifetime of the RunPod presigned access

## Question

[TASK-218](../../backlog/tasks/task-218%20-%20Encrypted-checkpoint-backups-to-S3-from-RunPod-runs-DEC-083-rule-4-every-10th-epoch-best-so-far-past-60-percent-final-epoch-machine01-command-to-list-download-and-decrypt-them-resume-from-a-backup-synthetic-tests.md) built the encrypted checkpoint backups of [DEC-083](../decisions/DEC-083-runpod-enc1-images-from-s3-and-encrypted-checkpoint-backups.md)
rule 4. Two questions came back from it (2026-11-23):

1. Should "checkpoint backup" get a row in the global glossary ([DEC-073](../decisions/DEC-073-how-new-terms-are-coined.md)
   point 4: a global term is chosen with the user)? [TASK-222](../../backlog/tasks/task-222%20-%20Glossary-the-S3-bucket-row-also-covers-encrypted-checkpoint-backups-under-runs-DEC-083.md) also waits on the user's wording
   for the S3 bucket row, which still says "enc1 images only".
2. How long should the S3 upload permission (the presigned POST policy a pod uses for its
   backups) last? DEC-083 rules 1 and 5 assume the signing session gives up to 12 h. [TASK-217](../../backlog/tasks/task-217%20-%20Presigned-S3-access-for-RunPod-pods-DEC-083-GET-URL-list-for-an-enc1-dataset-POST-policy-for-runs-run-pod-side-download-into-the-store-folder-synthetic-tests-with-a-fake-S3.md)
   found that it gives about 15 minutes ([TASK-221](../../backlog/tasks/task-221%20-%20Decide-signing-credentials-for-the-DEC-083-presigned-URLs-and-POST-policy-that-live-longer-than-the-15-minute-aws-login-credentials.md), Parked).

## Facts checked (AWS documentation, read 2026-11-23)

- `aws login` credentials "expire in 15 minutes, but the CLI and SDKs will automatically
  refresh them as needed up to 12 hours"
  ([SDK reference, login credentials](https://docs.aws.amazon.com/sdkref/latest/guide/feature-login-credentials.html);
  [CLI sign-in](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html)).
- A presigned URL signed with temporary credentials "expires when the credential expires";
  with long-term IAM user keys it can last up to 7 days (SigV4)
  ([S3 user guide, presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)).
  The page covers PUT and GET. That a presigned POST behaves the same way is assumed, not verified.
- AssumeRole `DurationSeconds` is 900 to 43200 s, up to the role's `MaxSessionDuration`
  (1 to 12 h). Role chaining (role credentials used to assume another role) caps it at 1 h. That cap
  "does not apply to the initial assumption of a role from user credentials"
  ([AssumeRole API](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html);
  [IAM, using roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html)).
  **Unverified:** whether temporary credentials from `aws login` (IAM user `claude-agent`)
  count as user credentials here. No page says either way.
- The `claude-agent` policy has no `sts:AssumeRole` today. It may create roles named
  `claude-agent-*` with the `claude-agent-boundary`, and that boundary allows S3 on the
  `claude-agent-*` buckets (`deploy/aws/`).

## Options considered

**Term.** The screen of DEC-073 point 1:

- (a) It recurs: DEC-083, seven board tasks, `deploy/aws/README.md`, and code that the
  RunPod runs of any epic use (`CheckpointBackup`, `--backup-policy`).
- (b) No term says it already. Plain "backup" overlaps the off-machine backup of [TASK-027](../../backlog/tasks/task-027%20-%20Choose-and-set-up-the-off-machine-copy-repos-runs-models.md) and
  the Common box copies, and "checkpoint" alone means the local `best.pt` / `last.pt`.
- (c) The descriptive phrase is a full sentence.

Options:

- **Checkpoint backup** (chosen): the words that code, DEC-083 and the tasks already use. Its
  scope is global, because it is training and infra code that no single epic owns.
- **S3 checkpoint backup**: names the place, which would help if a second kind of
  checkpoint backup appeared. Longer, and it no longer matches the code.
- **No row**: rejected, because readers would have to find the meaning in DEC-083.

**Lifetime of the upload permission.**

- **12 h, one POST policy per pod** (chosen). A run needs nothing from machine01 while it
  trains. A leaked policy can only write `.enc` keys under one run's prefix, up to a size
  limit, in a versioned bucket. 12 h is the longest a role session can last.
- **Expected run length + 1 h**: a smaller window if the policy leaks, but it needs an estimate
  per run and a fresh policy whenever the estimate is short.
- **15 min, refreshed**: machine01 signs a new policy every ~10 minutes and copies it to the
  pod, which already re-reads it before each upload. It needs no IAM change, but machine01 and
  its SSH to the pod must stay up for the whole run, and it ends when the 12 h `aws login`
  session ends.

**Signing credentials.**

- **A signing role** (chosen): `claude-agent-runpod-presign`, assumed on machine01 from the
  `aws login` credentials with a 12 h session and used only to sign. It needs one IAM statement,
  which the user applies.
- **Refresh loop**: keeps `aws login` as the signer. It is the fallback if the role session
  is capped at 1 h.
- **IAM user with long-term keys**: URLs could last up to 7 days, but the keys would sit on
  disk and need rotating, and the agent policy cannot create users. Rejected.

## Conclusion

The user accepted all three defaults:

- [DEC-085](../decisions/DEC-085-global-term-checkpoint-backup.md): global term **Checkpoint
  backup**, and new wording for the S3 bucket row. Applied by TASK-222.
- [DEC-086](../decisions/DEC-086-runpod-presigning-role-12h.md): a signing role, with the URLs and
  the POST policy lasting 12 h. This amends DEC-083 rules 1 and 5. The role, the IAM statement
  and the 12 h test go to an `aws` task ([TASK-227](../../backlog/tasks/task-227%20-%20Signing-role-for-RunPod-presigning-DEC-085-stack-claude-agent-runpod-presign-with-a-12-h-session-the-sts-AssumeRole-statement-for-the-user-to-apply-and-a-12-h-AssumeRole-test-from-aws-login-credentials.md)), and the code that signs with the role goes
  to a `method` task ([TASK-228](../../backlog/tasks/task-228%20-%20Presign-with-the-signing-role-DEC-085-signing_client-assumes-claude-agent-runpod-presign-for-a-12-h-session-role-arn-SONOAI_PRESIGN_ROLE_ARN-on-runpod-urls-runpod-post-policy-and-backup-resume-urls-synthetic-tests-with-a-stubbed-STS.md)). [TASK-219](../../backlog/tasks/task-219%20-%20RunPod-data-from-S3-in-run.sh-and-the-runbook-DEC-083-presign-on-machine01-aria2c-download-and-rsync-of-the-stores-non-image-part-on-the-pod-checkpoint-backups-on-fetch-backups-to-machine01.md) (run.sh and runbook) now waits on both. TASK-221 is
  answered.

## Open questions

- Is a role assumed from `aws login` credentials capped at 1 h (role chaining)? The `aws`
  task tests this first. If it is capped, the question comes back here, with the refresh loop
  as the default.
