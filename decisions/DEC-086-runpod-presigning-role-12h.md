---
id: DEC-086
title: RunPod presigned URLs and POST policy are signed with a 12 h signing role assumed on machine01, so they last 12 h (amends DEC-083 rules 1 and 5)
status: superseded
area: [data-security, aws, infra]
created: 2026-11-23
from: [DIS-044]
related: [DEC-083, DEC-024, DEC-026]
superseded_by: DEC-088
---
# DEC-086: A 12 h signing role for the RunPod presigned access

## Context

[DEC-083](DEC-083-runpod-enc1-images-from-s3-and-encrypted-checkpoint-backups.md) rules 1 and 5 assume the URLs and the POST policy
signed on machine01 last up to 12 h. They are signed with `aws login` credentials, which last
15 minutes each (refreshed for up to 12 h). A presigned URL stops working when its signing
credentials expire, so they last about 15 minutes ([TASK-217](../../backlog/tasks/task-217%20-%20Presigned-S3-access-for-RunPod-pods-DEC-083-GET-URL-list-for-an-enc1-dataset-POST-policy-for-runs-run-pod-side-download-into-the-store-folder-synthetic-tests-with-a-fake-S3.md), [TASK-221](../../backlog/tasks/task-221%20-%20Decide-signing-credentials-for-the-DEC-083-presigned-URLs-and-POST-policy-that-live-longer-than-the-15-minute-aws-login-credentials.md); sources in
[DIS-044](../discussions/DIS-044-checkpoint-backup-term-and-presign-lifetime.md)).

## Decision

1. **Signing role.** A role `claude-agent-runpod-presign`, set up as a CloudFormation stack in
   `deploy/aws/` with the `claude-agent-boundary`. `MaxSessionDuration` 12 h. Its trust policy
   names only the IAM user `claude-agent`. It may only do `s3:GetObject` on
   `datasets/*_enc1/*` and `runs/*`, and `s3:PutObject` on `runs/*`, in
   `claude-agent-sonoai-data`. The bucket policy of DEC-083 rule 7 still limits what lands under
   `runs/`.
2. **Use.** On machine01 the presign code assumes the role from the `agent-toolkit` (`aws
   login`) credentials with a 12 h session, and uses it only to sign. Listing stays with the
   profile. The role's credentials stay in RAM: they are never written to disk and never go to
   the pod.
3. **Lifetime: 12 h.** The image GET URL list, the resume URLs and the POST policy expire
   12 h after signing (the role session). Each pod gets one POST policy. A run that outlasts it
   gets a fresh policy copied to the pod (DEC-083 rule 5, unchanged). Meanwhile the checkpoint
   backups wait on the pod and are retried.
4. **IAM change by the user.** A statement in `claude-agent-deploy.json` lets `claude-agent`
   call `sts:AssumeRole` on that role only. The user applies it in the IAM console (as for the
   rest of that policy).
5. **Check first (unverified).** Before the code relies on 12 h, the aws agent assumes the
   role with `DurationSeconds` 43200 from `aws login` credentials and reports the expiry. If
   it is capped at 1 h (role chaining) or refused, the question goes back to `/consult`, with this
   fallback as the default: machine01 re-signs every ~10 minutes and copies the policy to the pod.
6. **Amends DEC-083** rules 1 and 5: "the signing session" there now means this role session.

## Consequences

- One IAM statement and one new stack. The presign commands get the role (an option and an
  env var), and the runbook ([TASK-219](../../backlog/tasks/task-219%20-%20RunPod-data-from-S3-in-run.sh-and-the-runbook-DEC-083-presign-on-machine01-aria2c-download-and-rsync-of-the-stores-non-image-part-on-the-pod-checkpoint-backups-on-fetch-backups-to-machine01.md)) signs with it.
- A leaked POST policy allows writes of `.enc` keys under one run's prefix, up to the size
  limit, for at most 12 h, in a versioned bucket. A leaked GET list exposes ciphertext only.
- Runs longer than 12 h still need the user to copy a fresh policy to the pod.
- Reversal: cheap. Delete the stack and the statement, and sign with `aws login` again.
