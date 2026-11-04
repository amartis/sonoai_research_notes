---
id: DEC-039
title: Generated Mermaid dependency pages on the board, one per milestone, refreshed with the ready label
status: accepted
created: 2026-11-03
from: [DIS-015]
related: [DEC-031, DEC-038]
superseded_by:
---
# DEC-039: Generated Mermaid dependency pages on the board, one per milestone, refreshed with the ready label

## Context

[DIS-015](../discussions/DIS-015-task-dependency-view.md): Backlog.md 1.55.3 shows
dependencies only per task (task detail page, CLI). The board has no whole-board view,
but its Documents pages render Mermaid.

## Decision

- A script writes a "Dependencies" section under the board's Documents. It holds one
  page per milestone plus one page for tasks with no milestone. The pages are read-only,
  gitignored copies like the [DEC-031](DEC-031-records-and-docs-on-the-task-board.md) pages.
- Each page has one Mermaid graph:
  - nodes: the open tasks, plus Done tasks that still block an open task (for context);
  - solid arrow: blocked by (`--dep`); dashed arrow: subtask of (`-p`);
  - node colour by status; ready tasks get a thick green border; Parked tasks with
    `needs-decision` are orange;
  - a dependency on a task in another milestone is shown as a small linked node.
- The pages are written by `scripts/board_mirror.py` (board start, git post-merge) and
  after each ready-label sync (Backlog.md `onStatusChange`, the Claude PostToolUse hook;
  [DEC-038](DEC-038-ready-label-derived-by-script.md)). Like the sync, they are written
  only in the main checkout.
- Task text in the graph is ID and title only; titles carry no patient data (workflow rules).

## Consequences

- No git churn: the pages are gitignored.
- Board task: [TASK-069](../../backlog/tasks/task-069%20-%20Mermaid-dependency-pages-on-the-board-one-per-milestone-refreshed-with-the-ready-label-DEC-039.md) (infra). It edits a hook script (`.claude/hooks/`), so its merge
  waits for the user ([DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)).
