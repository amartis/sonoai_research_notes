---
id: DEC-089
title: logs/ becomes its own git repository on Gogs, with one log file per workstation, reports in and scripts out, and its own privacy hook (amends the "local only" logs of DEC-026 and DEC-032)
status: accepted
area: [workflow, infra, data-security]
created: 2026-11-23
from: [DIS-047]
related: [DEC-014, DEC-026, DEC-032, DEC-054, DEC-078]
superseded_by:
---
# DEC-089: logs/ becomes its own git repository

## Context

`logs/` is ignored by the code repo and kept on one machine: the aws agent's action log
([DEC-026](DEC-026-cloud-agent-runs-cloud-services.md)) and the exp agent's run log ([DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)) are "local only". With a second workstation
([DEC-078](DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md)), logs from other team members can reach machine01-host only by hand
([DIS-047](../discussions/DIS-047-logs-folder-as-its-own-git-repo.md)).

## Decision

1. **Own repo.** `logs/` becomes a git repository of its own, branch `main`, like
   `research_notes/`. It stays in the main checkout, ignored by the code repo, and shared by every
   worktree as now ([DEC-054](DEC-054-main-checkout-guard-hook.md)).
2. **Remote: Gogs** ([DEC-014](DEC-014-gogs-git-remote.md)), no GitHub remote. The user may
   change the remote later. Pushing needs the user's go-ahead, as for the other repos.
3. **One file per workstation.** Each log is a folder with one file per workstation, named as in
   `docs/team.md` Table 2, e.g. `aws-agent/machine01-host.md` and `exp-runs/machine01-host.md`.
   A variable in `.env` names the workstation. Writers append only to their own workstation's
   file; readers read every file in the folder. The current files become machine01-host's; the
   files in `logs/imported_logs/` become machine01-senior's.
4. **Contents.** Action logs and reports (in `reports/`) are committed. Scripts and other files
   that are not logs or reports stay out: they are ignored by the logs repo, not deleted.
5. **Privacy.** The rule for committed text applies (`CLAUDE.md`): no table rows, file names,
   folder names, identifiers, keys or passphrase. The logs repo has its own pre-commit hook. It
   refuses at least the data and binary file types that the code repo's hook refuses, and image
   file names in added lines. Before the first commit, the existing files are checked the same
   way.
6. **Amends DEC-026 and DEC-032** where they call these logs "local only" or "not committed".
   Everything else in them stands.

## Consequences

- Code that uses a fixed log path changes: the log writer in `sonoai.cloud.labelstud` and the
  reader in `sonoai.tracking.pending`. So do the `aws` and `exp` agents, the docs that name the
  logs, and the "not committed" wording in `CLAUDE.md`, `.gitignore` and the guard hook's
  docstring. Changes to `CLAUDE.md`, agents and hooks wait for the user to merge (DEC-032).
- The move of the existing files must run after that code is merged, or the old code recreates
  the old files. A script does the setup once, on each workstation.
- Until the Gogs server is shared, only machine01-host can push. Other workstations commit
  locally and send their logs as before.
- Reversal: cheap. Remove `logs/.git` and the Gogs repo; the files stay as plain ignored files.
