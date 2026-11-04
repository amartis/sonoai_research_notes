---
id: DIS-015
title: A view of task dependencies on the board
status: concluded
created: 2026-11-03
outcomes: [DEC-039]
related: [DEC-031, DEC-038]
---
# DIS-015: A view of task dependencies on the board

## Question

The user wants to see the dependencies between tasks on the Backlog.md board.

What Backlog.md 1.55.3 offers, checked on 2026-11-03 on the running board and in its CLI:
- the web UI's task detail page has a "Dependency Graph" section (depends on and
  dependents, direct and total, with status);
- `backlog task <id> --plain` prints the same tree;
- kanban cards show no dependencies, and there is no whole-board dependency view;
- no plugin or custom-view mechanism was found (likely, not certain);
- Documents pages render Mermaid diagrams.

## Options considered

- **Layout**: one Mermaid page per milestone (plus one for tasks with no milestone),
  versus one page of all open tasks. With 67 tasks, one graph is hard to read.
- **Refresh**: from the same hooks as the `ready` label
  ([DEC-038](../decisions/DEC-038-ready-label-derived-by-script.md)), versus only at board
  start and post-merge (colours would lag).

## Conclusion

The user took the defaults ([DEC-039](../decisions/DEC-039-task-dependency-pages.md)):
one page per milestone, refreshed by the same hooks as the `ready` label. Board task: [TASK-069](../../backlog/tasks/task-069%20-%20Mermaid-dependency-pages-on-the-board-one-per-milestone-refreshed-with-the-ready-label-DEC-039.md).

## Open questions

- Whether Mermaid `click` links to task pages work in the board's renderer (checked in TASK-069).
