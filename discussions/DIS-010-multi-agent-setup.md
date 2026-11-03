---
id: DIS-010
title: Multi-agent setup - agent roles, consult and lead sessions, parallel writers
status: concluded
created: 2026-11-02
outcomes: [DEC-032]
related: [DEC-007, DEC-009, DEC-026, DEC-027, DEC-028]
---
# DIS-010: Multi-agent setup - agent roles, consult and lead sessions, parallel writers

## Question

The user asked (2026-10-29) to move to multi-agent development: which subagent
roles to have, what to observe when defining the project's flow and scopes, which
practices work, and whether to run several copies of one agent type. On
2026-11-02 they added two session types (skills): one to discuss, decide and
create tasks with them, and one lead session that keeps taking the next ready
task and hands it to named agents.

Before this, the repo had three agents: `infra`, `cloud` (AWS, [DEC-026](../decisions/DEC-026-cloud-agent-runs-cloud-services.md)) and
`command-reviewer`.

## What to observe when setting scopes and flow

Scope lines go where three things are low at once: files shared between tasks,
context shared between tasks, and permissions shared between tasks. Human gates go
where work is hard to undo. Measures, cheapest first:

| Observe | Decides | Measure |
| --- | --- | --- |
| Files that change together | scope boundaries | co-change in `git log` |
| Context a task must read first | what stays in one agent | the task's "read first" list |
| Sensitivity (patient data, keys, cloud, GPU) | least-privilege agents, hooks | tools and paths a task used |
| Dependencies, waits | flow order | time in each board status |
| User attention | what agents may decide alone | interruptions per task |
| Rework found in review | which checks to automate | review findings in task notes |
| Reversibility (code vs labels, splits, metrics) | where a human gate is required | tag per task |
| Cost and time per task type | model per role, parallel or not | tokens and wall-clock per task |

*Table 1. Observation points for defining scopes and flow (the agent's proposal,
agreed by the user as a way to review the setup later).*

## Practices considered

- Start with one agent; add agents only when observation shows a need
  ([Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents)).
- Many readers, few writers: read-only subagents search and review; writers must
  not share files. Cognition reports that parallel writers make conflicting,
  unstated decisions
  ([Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents);
  [follow-up, 2026](https://cognition.com/blog/multi-agents-working)).
- Orchestrator and workers: one lead holds the plan and decisions; each worker gets
  a full brief (goal, inputs, output, limits, done) and returns a summary
  ([Anthropic, multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system);
  [Claude Code subagents](https://code.claude.com/docs/zh-CN/sub-agents.md)).
- A checker separate from the maker; tests first, then a review model, then a
  person for hard-to-undo steps (evaluator-optimizer pattern, Anthropic above).
- Multi-agent work costs many more tokens: about 15x a chat, per Anthropic's
  research-system post. **Unverified**: read in search summaries only; the post
  itself could not be fetched on 2026-10-29.
- Shared state lives in files (board, DIS/DEC), and hard rules in hooks, not only
  in prompts (the agent's judgment; the repo already works this way).

## Options considered

- **Agent per board scope (`coord`, `method`, `data`, `exp`, `infra`) plus a
  read-only reviewer.** First proposal.
- **The same, without `coord`**, once the user asked for a consult skill and a lead
  skill: `coord` overlapped with both. Consult takes triage, decisions and task
  creation (they need the user); the "next ready task" check is mechanical and
  becomes a script the lead calls. Chosen by the user. `coord` stays as a board
  project (task scope).
- **Several copies of one agent type**: yes for readers (reviewer, Explore,
  command-reviewer) and for exp runs; for writers only on non-overlapping
  `touches`; never for agents that own one shared resource (aws, infra, the board).
- **Parallel writers**: [DEC-007](../decisions/DEC-007-session-branches-no-worktrees.md) forbade them; [DEC-028](../decisions/DEC-028-worktrees-for-parallel-sessions.md) (2026-10-30) allows one
  worktree per session. The user set a limit of 2 writers at once, on
  non-overlapping `touches`.
- **Merges by the lead**: ask per merge (old rule) or merge alone when clean. The
  user chose a split: ask for tasks with logical complexity, formulas, training or
  data preparation; the lead merges the rest itself when the review is clean and
  `scripts/check.sh` passes.
- **exp auto mode**: GPU box only (chosen), GPU box plus RunPod under a price cap
  (needs the passphrase in a RunPod secret for unattended runs), or always ask.
- **Name of the AWS agent**: the user renamed `cloud` to `aws`; its log becomes
  `logs/aws-agent.md`.
- **Spawn names**: `<type>-t<NNN>-<topic>` (chosen; same string as the worktree
  topic) or `<type>-<number>`.

## Conclusion

Agreed with the user on 2026-10-29 and 2026-11-02; recorded as
[DEC-032](../decisions/DEC-032-agent-roster-consult-and-lead-skills.md).

## Open questions

- Review the roster after about two weeks of use against Table 1 (agent's
  suggestion); drop agents that do not pay off.
- Whether exp auto mode should later cover RunPod (needs a DEC on where the
  passphrase lives).
