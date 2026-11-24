---
id: DEC-091
title: Every team member has a member handle, set as SONOAI_MEMBER in .env and listed in a team table in docs/team.md that the team lead or a senior edits (amends DEC-078)
status: proposed
area: [workflow, infra]
created: 2026-11-24
from: [DIS-051]
related: [DEC-078]
superseded_by:
---
# DEC-091: Member handles and the team table

## Context

Several team members now work at once, each on their own workstation
([DEC-078](DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md)). Their logs, runs,
branches and reserved numbers need an owner, and no existing name identifies a person:
`SONOAI_MACHINE` names a machine profile for training and `SONOAI_ACTOR` names an agent
([DIS-051](../discussions/DIS-051-multi-member-work-without-conflicts.md)).

## Decision

1. **Member handle.** Every team member has a member handle: lowercase letters and digits, short,
   unique in the team, never reused. By default it is the member's Linux user name. The first two
   are `dev01` (team lead) and `dev02` (senior).
2. **Where it is set.** `SONOAI_MEMBER=<handle>` in the workstation's `.env` (gitignored, linked into
   every worktree). `.env.example` lists it. Not in a separate file.
3. **Team table.** `docs/team.md` gets one table of members: handle, role, workstation. It replaces
   the "Used by" column of the workstation table. The team lead or a senior adds, changes or retires
   a row (amends DEC-078, where only the team lead did). A retired handle keeps its row, marked
   retired.
4. **Checked, not trusted.** Every tool that uses the handle (logs, runs, ID ledger, branch names)
   reads it through one helper, which stops with a clear message when `SONOAI_MEMBER` is unset or
   is not an active row of the team table.
5. The handle is not a secret and not patient data; it may appear in committed text, branch names
   and the ID ledger.

## Consequences

- One helper in `src/sonoai/` reads and checks the handle; `.env.example`, `team.md` and
  `onboarding.md` (step 5) change. Carried out by a board task.
- [DEC-092](DEC-092-logs-and-runs-one-folder-per-member-handle.md), [DEC-093](DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md) and [DEC-094](DEC-094-member-handle-in-branch-and-agent-names.md) build on the handle.
- Reversal: cheap; the variable and the table column can be dropped.
