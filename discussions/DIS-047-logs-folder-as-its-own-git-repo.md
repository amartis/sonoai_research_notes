---
id: DIS-047
title: logs/ as its own git repository, so logs from other team members can be merged
status: concluded
created: 2026-11-23
outcomes: [DEC-089]
related: [DEC-014, DEC-026, DEC-032, DEC-054, DEC-078]
---
# DIS-047: logs/ as its own git repository

## Question

`logs/` is ignored by the code repo and stays on one machine ("local only", [DEC-026](../decisions/DEC-026-cloud-agent-runs-cloud-services.md) and [DEC-032](../decisions/DEC-032-agent-roster-consult-and-lead-skills.md)).
The team now has a second workstation (machine01-senior, [DEC-078](../decisions/DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md)).
Its logs reach machine01-host only by hand: `logs/imported_logs/` holds two copied files. The
user asked whether `logs/` should become its own git repository, so that logs from other
developers, and their experiments, can be merged safely.

## Facts checked

- `logs/` holds 8 files (108 KB): two append-only action logs (the aws agent's log and the exp
  agent's run log), three one-off reports, one script, and the two imported logs.
- Two pieces of code use fixed paths: `src/sonoai/cloud/labelstud.py` appends to the aws
  agent's log, and `src/sonoai/tracking/pending.py` reads the exp run log. The agents `aws` and
  `exp` write to the same two files.
- A pattern scan of `logs/` found no image file names, no `dsid` folder names, no IP addresses and
  no EC2 instance IDs. The words "passphrase" (8 lines) and "_plain" (2 lines) appear; with long
  tokens masked, every one of those lines is a mention (for example "stopped before the
  passphrase prompt"), not a secret or a file name.
- The code repo's pre-commit hook (`.githooks/pre-commit`) calls `scripts/` by a relative path,
  so another repo cannot use it as it is.
- Gogs ([DEC-014](../decisions/DEC-014-gogs-git-remote.md)) listens only on `127.0.0.1` of
  machine01-host (`docs/onboarding.md`), so a senior cannot reach it today. The user plans to
  share the Gogs server and may change the remote later.
- Side finding: `research_notes/` has no `core.hooksPath` set, so it has no privacy hook, and it
  has a GitHub `origin` remote. [TASK-028](../../backlog/tasks/task-028%20-%20Pre-commit-hook-for-the-research_notes-repo-DEC-016.md) (pre-commit hook for the research_notes repo, in
  Triage) already covers it.

## Options considered

**Where the shared logs live.**

- **A separate git repo in `logs/`** (chosen). It follows the `research_notes/` pattern. It stays
  in the main checkout and is shared by every worktree, as now ([DEC-054](../decisions/DEC-054-main-checkout-guard-hook.md)). Logs change often and
  are written by machines, so they do not clutter the history of the code or the notes.
- **A folder `research_notes/logs/`**: no third repo, but logs would fill the history of the
  curated notes. It would win if a third repo became a burden to keep in sync.

**Avoiding merge conflicts.** Each writer appends to the end of the same file, and git reports
that as a conflict on every merge.

- **One file per workstation** (chosen), e.g. `exp-runs/machine01-host.md`. No conflicts and
  no merge setup; readers read every file in the folder.
- **`*.md merge=union` in `.gitattributes`**: no code change, but it relies on a merge driver
  that every clone must keep, and it can interleave lines.

**Remote.**

- **Gogs only** (chosen by the user): the user will share the Gogs server and can change the
  remote later.
- **A private GitHub repo plus Gogs**, as for `research_notes/`: the senior could push today.
- **Gogs, lead only, logs copied by hand as now.**

**What goes into the repo.**

- **Action logs and reports; scripts stay out** (chosen). The reports hold aggregates only. The
  script belongs to its task's code, not to a log; it stays on disk, ignored by the logs repo.
- **Reports in `research_notes/`**: first suggested, then dropped: reports lack the notes'
  front matter and index.

## Conclusion

The user accepted: a separate repo in `logs/`, Gogs as its only remote, one file per workstation,
the imported logs filed as machine01-senior's, reports in, script out.
[DEC-089](../decisions/DEC-089-logs-folder-own-git-repo.md) records it; an infra board task
carries it out. The missing privacy hook in `research_notes/` stays with TASK-028.

## Open questions

- How the Gogs server is shared with the team: the user's choice, outside this decision.
