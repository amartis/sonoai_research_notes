---
id: DIS-057
title: Board refresh loop from duplicate IDs, and the watchdog that stops it
status: concluded
created: 2026-11-25
outcomes: []
related: [DEC-031, DEC-093]
---
# DIS-057: Board refresh loop from duplicate IDs, and the watchdog that stops it

## Question

The task board (Backlog.md web UI) sometimes refreshes `/api/search` without end when task files
share an ID, in one branch or across branches; Firefox then fills the disk with discarded cache
("doomed") entries. The user does not want to fix Backlog.md, but wants a script and a hook that
notice the pattern, also for decisions and discussions, and force-stop the board server.

## Facts checked

Backlog.md 1.55.3, read from the installed program, then measured on a synthetic board
(2026-11-25) with a small client that does what a browser tab does: on each "tasks-updated"
message it requests `/api/search` and `/api/tasks/duplicates`.

| Synthetic board | Announcements |
|---|---|
| 20 tasks, no duplicate | 0 in 10 s |
| 20 tasks, one ID twice in the working copy (server already running) | 85 in 8 s |
| 20 tasks, one ID twice in the working copy (fresh server) | 85 in 8 s |
| 20 tasks, one ID on two branches with different files | 86 in 8 s |
| 20 tasks, one duplicate decision ID and one duplicate document ID | 0 in 8 s |
| 270 tasks on 18 extra branches, no duplicate | 0 in 20 s (and 30 s) |
| 270 tasks on 18 extra branches, one ID twice | 79 in 20 s |

Table 1. Refresh announcements of one board server with one client, one run per row.

- Likely cause, from reading the code (not confirmed by changing it): the server keeps one entry
  per ID for the visible tasks but compares it with the full list of files, so with a duplicate
  every read counts as a change. It announces it, each tab reads again, and the loop closes.
- Duplicate decisions and documents alone did not loop in this test. Other ways to trigger a loop
  were not tried.
- Firefox itself, and the growth of its cache, were not measured.

## Options considered

- **Stop on the symptom** (chosen): count the server's announcements through its own websocket
  for 20 s in four 5 s parts; stop when every part has enough (1 with a duplicate in the working
  copy, 3 otherwise). A burst of edits does not fill every part.
- **Stop on duplicates alone**: simpler, but stops boards that do not loop, and cross-branch
  findings cannot be told from a task renamed on one branch.
- **Change Backlog.md**: ruled out by the user.

## Conclusion

Board TASK-267 (board watchdog) carries the work: `scripts/board_watchdog.py`, the Claude Code hook
`ensure_board_watchdog.py` (session start, after Bash calls), the git `post-merge` hook and
`scripts/servers.sh` start it. It stops only `backlog browser` processes working in this repo or
its worktrees, and Label Studio keeps running. Duplicates of decisions and discussions are found and
named in the report and lower the threshold, like duplicate tasks. The user agreed on 2026-11-25 to
the test on real Backlog.md and to the merge after it.

No DEC: it is tooling that changes no rule.

## Open questions

- A board started by hand, with no Claude session or merge afterwards, is not watched.
- The loop rate with several open tabs was not measured.
