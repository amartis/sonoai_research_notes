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

Board [TASK-267](../../backlog/tasks/task-267%20-%20Board-watchdog-stop-a-Backlog.md-board-that-refreshes-itself-without-end.md) (board watchdog) carries the work: `scripts/board_watchdog.py`, the Claude Code hook
`ensure_board_watchdog.py` (session start, after Bash calls), the git `post-merge` hook and
`scripts/servers.sh` start it. It stops only `backlog browser` processes working in this repo or
its worktrees, and Label Studio keeps running. Duplicates of decisions and discussions are found and
named in the report and lower the threshold, like duplicate tasks. The user agreed on 2026-11-25 to
the test on real Backlog.md and to the merge after it.

No DEC: it is tooling that changes no rule.

## Correction, 2026-11-25 (later the same day)

The likely cause above was incomplete, and Table 1 missed the trigger because no task was changed
while its servers ran. A client against the live board (no duplicate ID in the checkout) got 145
announcements in 15 s, each answered with a 3.6 MB search. The watchdog then stopped that board.

Measured on clones of this repo, Backlog.md 1.55.3, a fresh server per row, one run each, one
client, 4 s after the change:

| Setting and branches | Change while the server runs | Announcements in 4 s |
|---|---|---|
| `check_active_branches: true`, this repo's branches | note, status, title, file renamed, renumbered, deleted, added, archived, merged, commit on a branch (10 rows) | 24 to 31 in every row, 28 to 32 after the commit; 0 after a restart |
| true, `master` only | note; added | 0 |
| true, one branch identical to `master`, or with an older text of one task, or with one task `master` lacks | note | 0 |
| true, one branch with the old file name of one renamed task | note | 31 |
| `check_active_branches: false`, this repo's branches | the same 10 changes | 0 in every row, also after the commit |
| false, one duplicate ID in the checkout | duplicate added; then another task edited; then the duplicate removed | 0; 34; 0 |
| false, duplicate decision ID added | decision added | 0 |

Table 2. What starts the loop. With false, two clients and six task edits over 60 s gave 6
announcements each. The renumbered row first showed 36 because the test reused [TASK-268](../../backlog/tasks/task-268%20-%20Board-stop-reading-other-branches-check_active_branches-off-the-trigger-of-the-endless-refresh.md), a real
number; with a free number it is 0.

- Trigger: a task file renamed here (how it got the new name does not matter; in 1.55.3 a CLI title edit kept the file name) while a branch of the last 30 days
  still has the old name, then any task change while the server runs. A restart clears it until the
  next change. [TASK-022](../../backlog/tasks/task-022%20-%20Gogs-server-docs-docs-infra-gogs.md-and-the-README-setup-for-the-gogs-remote-of-both-repos-DEC-014.md) (renamed) on the kept branches was that trigger.
- Why the code does it (reading only): the visible list keeps one entry per ID and is compared with
  a list that holds both file names.
- Fix: `check_active_branches: false` in `backlog/config.yml`, board TASK-268 (board setting). Cost: edits in a
  worktree show on the board after the merge; the CLI does not count tasks on other branches
  (`reserve_id.py task-create` finds a taken number in the ledger and tries again).
- Remaining case: a real duplicate ID in the checkout. The commit check ([DEC-093](../decisions/DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md)) reports it and
  the watchdog stops the board.

## Choice, 2026-11-25: relay instead of the setting

The user asked whether `check_active_branches: false` drops utility, and chose a relay that keeps it on,
plus a warning for each number (task, DEC, DIS, EXP) with several names. `scripts/board_relay.py`
sits in front of the unchanged board and drops "tasks-updated" messages when no file under
`backlog/` and no local branch changed.

| Clone of this repo, one renamed task, one branch with its old name; client behind the board for 20 s, one run per row | Announcements | in the last 10 s |
|---|---:|---:|
| No relay, note appended | 88 | 54 |
| No relay, real duplicate ID and an edit | 65 | 46 |
| Relay, no change | 0 | 0 |
| Relay, note, status, title, file renamed, renumbered, deleted, added, archived, merged (9 rows) | 4 or 5 | 0 |
| Relay, real duplicate ID and an edit | 7 | 0 |
| Relay or no relay, commit on a branch that touches a task | 0 | 0 |

Table 3. Behind the relay each change reached the client (last row excepted: no announcement with or
without the relay). Two clients, 60 s of edits: 20 announcements each, none in the last 10 s.

Correction of the cost named above: the board always shows the working copy's version of a task,
so notes or a Review status from a worktree do not show before the merge with the setting on either
(checked: status Review on another branch, the board kept Triage). What the setting gives is tasks
that exist only on other branches and their numbers.

## Open questions

- A board started by hand, with no Claude session or merge afterwards, is not watched.
- The loop rate with several open tabs was not measured.
