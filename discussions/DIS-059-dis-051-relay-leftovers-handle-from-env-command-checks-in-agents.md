---
id: DIS-059
title: Relay leftovers of DIS-051 - scripts read the member handle from .env, and agents check shell commands against the command policy themselves
status: concluded
created: 2026-11-25
outcomes: [DEC-104]
related: [DIS-051, DIS-055, DEC-032, DEC-091, DEC-093]
---
# DIS-059: Relay leftovers of [DIS-051](DIS-051-multi-member-work-without-conflicts.md)

## Question

The last lead session on the DIS-051 follow-ups (multi-member work) reported two gaps:

1. **Member handle.** `sonoai.team.member_handle()` and every Python tool that calls it
   (`scripts/reserve_id.py`, the run tracker) read `SONOAI_MEMBER` from the process environment
   only. `.env` is not loaded, so in a shell that has not exported `.env` the ID ledger
   ([DEC-093](../decisions/DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md)) and runs ([DEC-092](../decisions/DEC-092-logs-and-runs-one-folder-per-member-handle.md)) stop with "SONOAI_MEMBER is not set". `scripts/worktree.sh` and
   `scripts/gpu_tensorboard.sh` already fall back to `.env`; the Python side does not.
2. **Command checks inside agents.** CLAUDE.md tells every session to ask the `command-reviewer`
   agent before a shell command that installs software, changes git state, reaches another
   machine, and so on. Agents started by `/lead` (method, data, exp, infra, aws) have no tool to
   start another agent, so a brief that tells them to ask it stalls. This was found during the
   multi-member work but is not specific to it.

## Options considered

For gap 2:

- **The agent reads `docs/command-policy.md` itself** and applies it; on ASK or DENY it stops and
  returns the command to the lead (or the user). One read of the policy file (about 12 KB) per
  agent, cheaper than starting a command-reviewer agent per command.
- **The agent returns every such command to the lead**, which asks the command-reviewer. Safer
  (a second opinion), but each command costs a round trip and stops the agent.

## Conclusion

- Gap 1: a small `method` task, [TASK-271](../../backlog/tasks/task-271%20-%20Python-tools-read-SONOAI_MEMBER-from-the-main-checkouts-.env-when-the-environment-lacks-it-like-worktree.sh-DIS-059.md) below; no decision needed.
- Gap 2: the user chose the first option: [DEC-104](../decisions/DEC-104-agents-check-shell-commands-against-the-command-policy-themselves.md).
  Its text changes (CLAUDE.md, agent files, docs/agents.md) are [TASK-272](../../backlog/tasks/task-272%20-%20Agents-check-shell-commands-against-docs-command-policy.md-themselves-and-return-ASK-or-DENY-commands-DEC-104.md); they change the guards,
  so the merge waits for the user.
- Not taken up now (user, 2026-11-25): [TASK-189](../../backlog/tasks/task-189%20-%20Define-the-junior-role-what-a-junior-may-do-which-data-and-machines-who-reviews-and-merges.md) (define the junior role) and [TASK-190](../../backlog/tasks/task-190%20-%20Label-Studio-for-a-senior-use-machine01-leads-server-or-a-second-server-with-its-own-state.md) (Label
  Studio for a senior).

## Open questions

None.
