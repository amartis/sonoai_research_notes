---
id: DIS-046
title: DEC-086 rule 5 - the 12 h signing role session is capped at 1 h, so how the RunPod POST policy is kept fresh
status: concluded
created: 2026-11-23
outcomes: [DEC-088]
related: [DEC-086, DEC-083, DIS-044]
---
# DIS-046: The 1 h cap on the signing role session, and the refresh loop

## Question

[DEC-086](../decisions/DEC-086-runpod-presigning-role-12h.md) rule 5 said: before the code relies
on a 12 h role session, test it. If it is capped at 1 h or refused, bring the question back here.
The default then was a refresh loop that re-signs about every 10 minutes.
[TASK-227](../../backlog/tasks/task-227%20-%20Signing-role-for-RunPod-presigning-DEC-085-stack-claude-agent-runpod-presign-with-a-12-h-session-the-sts-AssumeRole-statement-for-the-user-to-apply-and-a-12-h-AssumeRole-test-from-aws-login-credentials.md) ran the test on 2026-11-23.

## Facts checked

- TASK-227 deployed the stack `claude-agent-runpod-presign`, and the user applied the
  `sts:AssumeRole` statement. An AssumeRole with `DurationSeconds` 43200 from `aws login`
  credentials was refused: it "exceeds the 1 hour session limit for role chaining" (the agent's
  report, `logs/aws-agent.md`). So AWS counts `aws login` credentials as a role session.
  This settles the open question of [DIS-044](DIS-044-checkpoint-backup-term-and-presign-lifetime.md).
- Role chaining caps a session at 1 h
  ([IAM, using roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html), read in
  DIS-044).
- `aws login` credentials are refreshed for up to 12 h (SDK reference, read in DIS-044).
- The pod already re-reads the POST policy file before each upload. An expired policy leaves the
  backups waiting, and the next backup retries them ([TASK-218](../../backlog/tasks/task-218%20-%20Encrypted-checkpoint-backups-to-S3-from-RunPod-runs-DEC-083-rule-4-every-10th-epoch-best-so-far-past-60-percent-final-epoch-machine01-command-to-list-download-and-decrypt-them-resume-from-a-backup-synthetic-tests.md), `sonoai.cloud.backup`).

## Options considered

**Signing.**

- **The role, 1 h session, re-signed every ~45 minutes** (chosen). The role and the IAM statement
  already exist. A 1 h window gives the pod's image download, and any machine01 or SSH hiccup,
  four times the slack of 15 minutes. It is the same loop, run four times less often.
  This departs from DEC-086 rule 5's default, for those reasons.
- **`aws login` directly, 15 minutes, re-signed every ~10 minutes**: DEC-086 rule 5 as written.
  It would win if we wanted less in AWS (the stack and the statement could go).
- **A signing-only IAM user with long-term keys**: up to 7 days, one policy per run, no loop.
  It would win only if machine01 could not stay up during runs. The keys would sit on disk and
  need rotating, and the user would have to create the user. Not chosen.

**Where the loop lives.**

- **A shell script `deploy/runpod/refresh_policy.sh`** (chosen), run in tmux on machine01, next to
  run.sh and the runbook (TASK-219).
- **A `--every` option on `sonoai-data runpod-post-policy`**: unit-tested, but it puts scp to
  another machine into the package code.

**Runs past the 12 h of `aws login`.**

- **The user runs `aws login` again** (chosen). Until then the loop fails, logs it and keeps
  retrying. Backups wait on the pod and go up late. Nothing is lost.
- **Fully unattended**: would need long-term keys or IAM Roles Anywhere (not checked), so a new
  discussion.

## Conclusion

The user accepted the three defaults:
[DEC-088](../decisions/DEC-088-runpod-presigning-role-1h-refresh-loop.md) supersedes DEC-086.
[TASK-228](../../backlog/tasks/task-228%20-%20Presign-with-the-signing-role-DEC-085-signing_client-assumes-claude-agent-runpod-presign-for-a-12-h-session-role-arn-SONOAI_PRESIGN_ROLE_ARN-on-runpod-urls-runpod-post-policy-and-backup-resume-urls-synthetic-tests-with-a-stubbed-STS.md) changes to a 3600 s
session, with no short-expiry warning for a fresh role session.
[TASK-219](../../backlog/tasks/task-219%20-%20RunPod-data-from-S3-in-run.sh-and-the-runbook-DEC-083-presign-on-machine01-aria2c-download-and-rsync-of-the-stores-non-image-part-on-the-pod-checkpoint-backups-on-fetch-backups-to-machine01.md) adds the refresh
loop script and the runbook steps. TASK-227 needs no more AWS work.

## Open questions

- None.
