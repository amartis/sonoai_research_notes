---
id: DEC-032
title: Agent roster, named spawns, /consult and /lead skills, up to 2 parallel writers
status: accepted
created: 2026-11-02
from: [DIS-010]
related: [DEC-026, DEC-027, DEC-028, DEC-009]
superseded_by:
---
# DEC-032: Agent roster, named spawns, /consult and /lead skills, up to 2 parallel writers

## Context

The user asked to work with several agents at once
([DIS-010](../discussions/DIS-010-multi-agent-setup.md)): one session that discusses and
decides with them, and one lead session that keeps taking the next ready board task
and hands it to agents. [DEC-028](DEC-028-worktrees-for-parallel-sessions.md) already gives
each session its own worktree.

## Decision

**Agents** (`.claude/agents/`):

| Agent | Writes | Several at once |
| --- | --- | --- |
| `method` (new) | `src/`, `tests/` (synthetic data only) | yes, on non-overlapping `touches` |
| `data` (new) | `configs/data/`, dataset `derived/` (aggregates only) | yes, on non-overlapping `touches` |
| `exp` (new) | `configs/experiments/`, EXP records, `logs/exp-runs.md` | yes for runs; EXP records one at a time |
| `reviewer` (new) | nothing (read-only; runs `scripts/check.sh`) | yes, one per focus: code, privacy, writing |
| `aws` (renamed from `cloud`) | AWS actions, `logs/aws-agent.md` | no |
| `infra` (kept) | as before | no |
| `command-reviewer` (kept) | nothing | yes |

No `coord` agent: triage, decisions and task creation belong to `/consult`; the
ready-task check is `scripts/ready_tasks.py`. `coord` remains a board project.

**Spawn names**: `<type>-t<NNN>-<topic>` (e.g. `method-t015-losses`), or
`<type>-<topic>` without a task. The name is the worktree topic, the branch
`claude/<name>`, `SONOAI_ACTOR`, the prefix of board notes, and the first line of
every report (`[<name>]`).

**Skills**:

- `/consult [topic]`: interactive with the user. Discussion → DIS, DEC drafts as
  `proposed` (accepted only on the user's yes), board tasks with scope, `touches`,
  criteria, deps and refs; triage of the Triage queue. Never spawns writers.
- `/lead`: one pass of the lead loop; `/loop /lead` keeps it running. It runs
  `scripts/ready_tasks.py`, spawns writers by task project (at most **2 writers at
  once**, on non-overlapping `touches`), spawns reviewers on each finished branch,
  and merges or asks (below). Items that need the user go out in one message.

**Merges into `master`**:

- The lead **asks the user** when the task's project is `method`, `data` or `exp`,
  when the diff touches `src/sonoai/{models,losses,metrics,train*,data}`,
  `configs/data/` or `configs/experiments/`, when it changes a formula, or when the
  lead is unsure.
- Otherwise (docs, tooling, infra, board text) the lead merges itself once the
  reviewers find nothing and `scripts/check.sh` passes, then removes the worktree.
  This amends DEC-028's "merge once the user agrees" for that class only.
- Tasks still stop in Review; only the user moves them to Done.

**exp runs**: a run is pending when its config has no run folder under `RUNS_ROOT`
and no line in `logs/exp-runs.md`. Mode `approve` (default) asks before each run;
mode `auto` starts the next pending run on the GPU box (machine02) itself and tells
the user to type the passphrase. RunPod runs always ask, with the hourly price
(Secure Cloud, enc1 only). The agent never handles the passphrase.

**Rename**: the `cloud` agent of [DEC-026](DEC-026-cloud-agent-runs-cloud-services.md) and [DEC-027](DEC-027-agent-ssh-to-aws-labelstud-through-ssm.md) is now `aws` (assignee `@aws`,
log `logs/aws-agent.md`); its rules are unchanged. The `sonoai.cloud` package keeps
its name.

Command-policy rules follow the user's go-ahead on this DEC: E1-E3 for exp, M1 for
the lead's merges, the AWS section renamed.

## Consequences

- Up to two writers work at once; reviewers and exp runs add parallel work without
  file conflicts.
- Simple changes reach `master` without waiting for the user; complex ones wait,
  batched.
- A finished spawn wakes the lead, so there is no polling; idle `/loop` passes come
  every 30 minutes.
- To undo: a new DEC; delete the agent files and skills, restore the cloud name.
