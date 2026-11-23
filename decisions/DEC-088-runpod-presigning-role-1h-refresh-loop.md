---
id: DEC-088
title: RunPod presigned URLs and POST policy are signed with a 1 h session of the signing role, and machine01 re-signs the POST policy every 45 minutes and copies it to the pod (supersedes DEC-086)
status: accepted
area: [data-security, aws, infra]
created: 2026-11-23
from: [DIS-046]
related: [DEC-086, DEC-083, DEC-024, DEC-026]
superseded_by:
---
# DEC-088: A 1 h signing role session and a 45-minute refresh loop for RunPod presigning

## Context

[DEC-086](DEC-086-runpod-presigning-role-12h.md) chose a signing role with a 12 h session and made
rule 5 a test first. [TASK-227](../../backlog/tasks/task-227%20-%20Signing-role-for-RunPod-presigning-DEC-085-stack-claude-agent-runpod-presign-with-a-12-h-session-the-sts-AssumeRole-statement-for-the-user-to-apply-and-a-12-h-AssumeRole-test-from-aws-login-credentials.md) deployed the role. The user applied the `sts:AssumeRole`
statement. A 12 h AssumeRole from `aws login` credentials was then refused because it exceeds
the 1 h limit for role chaining. So a role session lasts 1 h at most, and so do the URLs and the
POST policy signed with it ([DIS-046](../discussions/DIS-046-runpod-presign-1h-cap-refresh-loop.md)).

## Decision

1. **Role and IAM statement stay** as in DEC-086 rules 1 and 4: the stack
   `claude-agent-runpod-presign` and the `sts:AssumeRole` statement that the user applied.
   `MaxSessionDuration` stays at 12 h in the stack. Role chaining caps every session at 1 h
   anyway.
2. **Use** as in DEC-086 rule 2. On machine01 the presign code assumes the role from the
   `agent-toolkit` (`aws login`) credentials, with `DurationSeconds` 3600, and uses it only
   to sign. Listing stays with the profile. The role credentials stay in RAM: never written to disk,
   never sent to the pod.
3. **Lifetime: 1 h.** The image GET URL list, the resume URLs and the POST policy expire when
   the role session does, 1 h after signing. The GET list and the resume URLs are signed once,
   when they are needed. If a download takes longer, they are signed again and
   `aria2c -c` resumes it.
4. **Refresh loop on machine01.** A script, `deploy/runpod/refresh_policy.sh`, runs in tmux on
   machine01 for the whole run. Every ~45 minutes it signs a fresh POST policy for the run and
   copies it to the pod, to the path run.sh gives the backups. It logs one line per refresh, with
   no URL, key or policy content. If a refresh fails, the loop keeps retrying. The pod
   re-reads the policy before each upload. While the policy is expired, the checkpoint backups
   wait on the pod and go up with the next one ([TASK-218](../../backlog/tasks/task-218%20-%20Encrypted-checkpoint-backups-to-S3-from-RunPod-runs-DEC-083-rule-4-every-10th-epoch-best-so-far-past-60-percent-final-epoch-machine01-command-to-list-download-and-decrypt-them-resume-from-a-backup-synthetic-tests.md), unchanged).
5. **Past 12 h.** `aws login` refreshes its credentials for up to 12 h. For a run that outlasts
   that, the loop fails until the user runs `aws login` again. Then it picks up by itself.
   The runbook says so.
6. **Supersedes DEC-086.** [DEC-083](DEC-083-runpod-enc1-images-from-s3-and-encrypted-checkpoint-backups.md) rules 1 and 5 read with this decision: "the signing session"
   is a 1 h role session, and a fresh policy reaches the pod from the loop of rule 4.

## Consequences

- No change in AWS: the stack and the statement from TASK-227 serve as they are.
- [TASK-228](../../backlog/tasks/task-228%20-%20Presign-with-the-signing-role-DEC-085-signing_client-assumes-claude-agent-runpod-presign-for-a-12-h-session-role-arn-SONOAI_PRESIGN_ROLE_ARN-on-runpod-urls-runpod-post-policy-and-backup-resume-urls-synthetic-tests-with-a-stubbed-STS.md) asks for a 3600 s session (not 43200 s). Its short-expiry warning must stay
  quiet for a fresh 1 h role session. [TASK-219](../../backlog/tasks/task-219%20-%20RunPod-data-from-S3-in-run.sh-and-the-runbook-DEC-083-presign-on-machine01-aria2c-download-and-rsync-of-the-stores-non-image-part-on-the-pod-checkpoint-backups-on-fetch-backups-to-machine01.md) adds the
  loop script and its runbook steps.
- machine01, its `aws login` session and its SSH to the pod must stay up while a run trains, or
  backups go up late. Training itself does not depend on them.
- A leaked POST policy allows writes of `.enc` keys under one run's prefix, up to the size
  limit, for at most 1 h, in a versioned bucket. That is a smaller window than DEC-086's 12 h.
- Reversal: cheap. Stop the loop. To drop the role, delete the stack and the statement and
  sign with `aws login` directly (15 min, re-signed every ~10 min).
