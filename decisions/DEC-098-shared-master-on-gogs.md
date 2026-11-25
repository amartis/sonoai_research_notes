---
id: DEC-098
title: One shared master (research_notes main) on Gogs, the same name locally and on the remote; before each push the member fetches, merges, resolves and runs check.sh; that push needs no go-ahead; GitHub origin becomes the team lead's backup (amends DEC-014 and DEC-028)
status: accepted
area: [workflow, infra]
created: 2026-11-25
from: [DIS-055]
related: [DEC-014, DEC-028, DEC-078, DEC-091, DEC-093]
superseded_by:
---
# DEC-098: One shared master on Gogs

## Context

Two team members ([DEC-078](DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md),
[DEC-091](DEC-091-member-handles-and-team-table.md)) merge into `master` on their own
workstations. Gogs ([DEC-014](DEC-014-gogs-git-remote.md)) is now reachable from the team's
workstations and holds the ID ledger ([DEC-093](DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md)).
`docs/onboarding.md` still says to use GitHub `origin` only, `master` tracks `origin`, and every
push needs the user's go-ahead (CLAUDE.md, command policy A4).

## Decision

1. **One shared branch.** The code repo has one `master` and `research_notes/` one `main`, on Gogs,
   with the same name locally and on the remote. No per-member branches, no pull requests.
2. **The push flow**, in the main checkout of each repo:
   1. commit your own board changes (status moves, ready labels);
   2. `git fetch gogs`;
   3. `git merge gogs/master` (research_notes: `gogs/main`), a merge and not a rebase, because a
      rebase drops the merge commits of worktree branches;
   4. `scripts/check.sh`;
   5. `git push gogs master` (research_notes: `main`); a refused push goes back to step 2.
3. **Conflicts.** The member who pushes resolves them. An agent that meets a conflict stops and tells
   the member; it never resolves one alone.
4. **No go-ahead for that push** when `scripts/check.sh` passed and the push is plain: no `--force`,
   no other branch, no other remote. Every other push still needs a go-ahead. This takes effect when
   the CLAUDE.md line and the command-policy entry of TASK-188 are in place; until then A4 holds.
5. **GitHub `origin`** becomes the team lead's backup, pushed with a go-ahead as before.

## Consequences

- [TASK-188](../../backlog/tasks/task-188%20-%20Shared-master-on-Gogs-the-fetch-merge-check-and-push-flow-for-every-member-pushes-without-a-go-ahead-and-a-count-of-unmerged-commits-in-consult-and-lead.md)
  writes the flow into the docs and onboarding, proposes the command-policy entry (fetch, conflict-free
  merge and push), and makes `/consult` and `/lead` report unmerged commits on Gogs at the start.
  [TASK-022](../../backlog/tasks/task-022%20-%20Gogs-server-docs-docs-infra-gogs.md-and-the-README-setup-for-the-gogs-remote-of-both-repos-DEC-014.md)
  documents the Gogs server.
- Amends DEC-014 (Gogs is the team's shared remote, GitHub the backup) and [DEC-028](DEC-028-worktrees-for-parallel-sessions.md) (the push rule).
- Each clone sets `gogs/master` (research_notes: `gogs/main`) as the upstream once.
- Members see each other's tasks and board moves after their next merge; the ID ledger already keeps
  numbers and task starts from clashing in the meantime.
