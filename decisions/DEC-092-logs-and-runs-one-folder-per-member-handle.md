---
id: DEC-092
title: logs/ and runs/ stay on machine01-host's shares with one folder per member handle - write only your own folder, read all, no shared folder, roots from .env (supersedes DEC-089)
status: accepted
area: [workflow, infra, data-security]
created: 2026-11-24
from: [DIS-051]
related: [DEC-026, DEC-032, DEC-078, DEC-089, DEC-091]
superseded_by:
---
# DEC-092: logs/ and runs/ with one folder per member handle

## Context

machine01-host shares its `logs/` and `runs/` over SMB 3.1.1 with encryption, and machine01-senior
mounts both ([DEC-078](DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md),
`docs/onboarding.md` step 7). Both folders are flat today, so two members would append to the same
log and write runs of the same name into the same folder.
[DEC-089](DEC-089-logs-folder-own-git-repo.md) planned a git repo for `logs/` with one file per
workstation; it was never carried out, and the user dropped it
([DIS-051](../discussions/DIS-051-multi-member-work-without-conflicts.md)).

## Decision

1. **One folder per member handle** ([DEC-091](DEC-091-member-handles-and-team-table.md)):
   `logs/<handle>/` (e.g. `logs/<handle>/aws-agent.md`, `logs/<handle>/exp-runs.md`,
   `logs/<handle>/reports/`) and `runs/<handle>/<run>/`.
2. **Write only your own folder, read all.** Code writes under the current member's handle only.
   Readers that need every member's entries read `logs/*/<log>`; a run is found by name across
   `runs/*/`, so records can keep naming runs by run name.
3. **No shared folder.** Text the whole team needs goes into a committed repo, not onto a share.
4. **Roots from `.env`.** `SONOAI_LOGS_ROOT` and `SONOAI_RUNS_ROOT` name the share roots (on
   machine01-host its own folders, elsewhere the mounts); code adds `<handle>` through
   `sonoai.paths`. Worktrees reach the logs through these variables.
5. **Not committed, machine01 only.** Logs and runs are not in git. They may hold file names, so
   they stay on machine01 like the data root ([DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)). [DEC-026](DEC-026-cloud-agent-runs-cloud-services.md) and [DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md) ("local only") stand
   again in this sense: local to machine01's shares.
6. **Existing files.** The current flat logs and run folders move once into the team lead's folder
   (`dev01`), with a script that shows what it will move and moves only on the user's go-ahead.
7. **Supersedes DEC-089.** Its task, [TASK-231](../../backlog/archive/tasks/task-231%20-%20logs-as-its-own-git-repo-DEC-089-one-log-file-per-workstation-a-setup-script-and-the-logs-repos-own-privacy-hook.md), is archived.

## Consequences

- The aws log writer, the exp run-log reader, run lookup (`compare_runs.py` and the like), the
  `aws` and `exp` agents, `worktree.sh` (its `logs` link), `CLAUDE.md`, `.env.example` and the docs
  that name these logs change. Agents and `CLAUDE.md` changes wait for the user to merge (DEC-032).
  Carried out by a board task.
- `onboarding.md` 7c drops "do not mount the share as your `logs/`" and "keep `SONOAI_RUNS_ROOT` on
  your own `runs/`".
- Runs fetched from the GPU box or RunPod land under the member's own folder on the share; their
  bytes cross the SMB link, which stays inside machine02.
- Reversal: cheap; folders can be flattened again.
