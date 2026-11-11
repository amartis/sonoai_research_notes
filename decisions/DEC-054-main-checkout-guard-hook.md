---
id: DEC-054
title: A project hook denies Claude's file edits in the main checkout except research_notes/ and logs/; Claude Code's background-session guard is off
status: accepted
area: [workflow]
created: 2026-11-11
from: []
related: [DEC-028, DEC-053]
superseded_by:
---
# DEC-054: A project hook denies Claude's file edits in the main checkout except research_notes/ and logs/; Claude Code's background-session guard is off

## Context

Claude Code blocks Write and Edit in the main checkout for background sessions until
the session calls `EnterWorktree` (`worktree.bgIsolation`, default `"worktree"`). The
setting has two values only, `"worktree"` and `"none"`, with no path exemption
(Claude Code settings reference, `worktree.bgIsolation`, read 2026-11-11). So it also
blocked `research_notes/`, a separate repo that [DEC-028](DEC-028-worktrees-for-parallel-sessions.md) commits directly on its `main`:
on 2026-11-11 a background session could not write [DEC-053](DEC-053-table-naming-and-preservation.md) and the user had to copy it
by hand. The guard also steers to the app's worktrees, which DEC-028 does not use.
DEC-028 itself was enforced only by instructions in `CLAUDE.md`.

## Decision

- `.claude/settings.local.json` (machine-only, kept out of git by `.git/info/exclude`)
  sets `"worktree": {"bgIsolation": "none"}`.
- A PreToolUse hook, `.claude/hooks/guard_main_checkout.py`, denies Claude's Write,
  Edit, MultiEdit and NotebookEdit on any path that resolves (links followed) into the
  main checkout, except `research_notes/` and `logs/`, in every session (background or
  not). Paths in worktrees and outside the repo pass. Shell commands are not checked.
- DEC-028's "a one-line fix may use the main checkout" no longer holds for Claude's file
  edits: they go through a worktree.

## Consequences

- Rule text: `CLAUDE.md` (Git worktrees) and `docs/workflow.md` (Git: branches and
  sessions). Tests: `tests/test_guard_main_checkout.py` (synthetic repos).
- Background sessions write DIS and DEC records in `research_notes/` directly.
- Undo: remove the settings line and the hook entry in `.claude/settings.json`.
