---
id: DEC-014
title: Self-hosted Gogs on machine01 as the git remote of both repos
status: accepted
created: 2026-10-28
from: [DIS-003]
related: [DEC-007]
superseded_by:
---
# DEC-014: Self-hosted Gogs on machine01 as the git remote of both repos

## Context

Neither the code repo nor `research_notes/` has a remote; every decision and
the board exist only on machine01, a VM guest on machine02. DIS-003 weighed a
bare mirror on machine02, private hosted repos (GitHub), git bundles to the
user's own storage, and a self-hosted git service (Forgejo / Gitea / Gogs).
The user chose Gogs, hosted on machine01.

## Decision

- **Gogs** runs on machine01 as a systemd user service, HTTP and SSH bound to
  `127.0.0.1` only (`http://localhost:3000`, builtin SSH on port 2222),
  SQLite, data in `~/apps/gogs-data/` (outside both repos and the data roots).
  Registration is disabled after the user's own account exists. Pushes use a
  dedicated key, `~/.ssh/gogs_localhost` (set as `core.sshCommand` in both
  repos). Set up 2026-10-28 (Gogs 0.14.3, TASK-021).
- The code repo and `research_notes/` each get a remote named `gogs` holding
  private repos `ml_research` and `research_notes`. `master` (code) and `main`
  (notes) are pushed there after a merge or notes commit.
- The rules on content are unchanged: no patient data, data files, keys or
  `.env` in either repo; the pre-commit guards stay the gate.
- Pushing to `gogs` still needs the user's go-ahead until the workflow docs
  say otherwise.

## Consequences

- Both repos have a real remote with a web UI; branches and history can be
  browsed at `localhost:3000`.
- **Not a backup**: Gogs stores its repos on the same VM disk as the working
  copies. An off-machine copy (the Gogs data folder or git bundles to storage
  off machine02's hardware) is still to be decided.
- Gogs has no push mirrors and a slow security-fix record; it is acceptable
  here because it listens on localhost only and has one user.
- `docs/workflow.md` and `CLAUDE.md` ("the repo has no remote") need updating
  once the setup works.
