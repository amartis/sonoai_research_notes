---
id: DEC-104
title: An agent that cannot start the command-reviewer reads docs/command-policy.md itself and applies it; on ASK or DENY it stops and returns the command (amends the command-approvals rule in CLAUDE.md)
status: accepted
area: [workflow]
created: 2026-11-25
from: [DIS-059]
related: [DEC-032]
superseded_by:
---
# DEC-104: Agents check shell commands against the command policy themselves

## Context

CLAUDE.md ("Command approvals") tells every session to ask the `command-reviewer` agent before a
shell command that installs software, changes config outside the repo, reaches another machine or
service, changes git state, or that it is unsure about. Agents started by `/lead` have no tool to
start another agent, so they cannot follow it and stall ([DIS-059](../discussions/DIS-059-dis-051-relay-leftovers-handle-from-env-command-checks-in-agents.md)).

## Decision

1. A session that can start agents (a main session: `/lead`, `/consult`, a member's own session)
   keeps asking the `command-reviewer` as before.
2. An agent that cannot start one reads `docs/command-policy.md` itself (once per run) and applies
   it to such a command, citing the rule IDs in its plan or notes.
3. On ALLOW it runs the command. On ASK or DENY it does not run it: it stops and returns the
   command, the rule IDs and why, to whoever started it (the lead or the user).
4. Claude Code's permissions and hooks still apply; a blocked command never goes around the block.

## Consequences

- Agents no longer stall on the command-reviewer step; the policy file stays the one source.
- Cost: one read of the policy file (about 12 KB) per agent run, less than one extra agent per
  command.
- Text changes: CLAUDE.md, `.claude/agents/{method,data,exp,infra,aws}.md`, `docs/agents.md`
  ([TASK-272](../../backlog/tasks/task-272%20-%20Agents-check-shell-commands-against-docs-command-policy.md-themselves-and-return-ASK-or-DENY-commands-DEC-104.md)).
