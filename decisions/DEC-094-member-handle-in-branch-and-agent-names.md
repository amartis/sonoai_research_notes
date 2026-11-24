---
id: DEC-094
title: The member handle goes into branch names (claude/<handle>/<topic>) and wherever an agent name leaves the workstation (SONOAI_ACTOR, board note prefix, report line) (amends DEC-028 and DEC-032)
status: proposed
area: [workflow]
created: 2026-11-24
from: [DIS-051]
related: [DEC-028, DEC-032, DEC-091, DEC-093]
superseded_by:
---
# DEC-094: The member handle in branch and agent names

## Context

`scripts/worktree.sh` makes branches named `claude/<topic>`, and agent names are
`<type>-t<NNN>-<topic>` ([DEC-028](DEC-028-worktrees-for-parallel-sessions.md),
[DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)). Two members pushing to one remote can
pick the same topic, and board notes and logs do not say whose agent wrote them
([DIS-051](../discussions/DIS-051-multi-member-work-without-conflicts.md)).

## Decision

1. **Branches.** `scripts/worktree.sh new <topic>` makes branch `claude/<handle>/<topic>`, with the
   handle from `SONOAI_MEMBER` ([DEC-091](DEC-091-member-handles-and-team-table.md)). The worktree
   folder stays `../ml_research-wt/<topic>`: it is local to the workstation. Existing branches keep
   their names.
2. **Agent names stay `<type>-t<NNN>-<topic>`** inside a workstation: a task claim
   ([DEC-093](DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md)) means only one
   member works on a task.
3. **Where a name leaves the workstation it carries the handle:** `SONOAI_ACTOR=<handle>/<name>`,
   the board note prefix `[<handle>/<name>]` and the first line of the report.
4. Notes already on the board are not rewritten.

## Consequences

- `worktree.sh`, `docs/agents.md`, `docs/workflow.md`, the agents (`SONOAI_ACTOR`, note prefix),
  `/lead` and `CLAUDE.md` (worktree rule) change; the user merges guard files (DEC-032). Carried
  out by a board task.
- The glossary row "Agent name" names the handle prefix.
- Reversal: cheap.
