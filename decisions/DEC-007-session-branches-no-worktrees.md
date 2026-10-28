---
id: DEC-007
title: Sessions use branches in the main checkout, never git worktrees
status: accepted
created: 2026-10-27
from: []
related: []
superseded_by:
---
# DEC-007: Sessions use branches in the main checkout, never git worktrees

## Context

Several agent sessions (Claude Code, the desktop app) work on this repo. The
tooling can give each session its own git worktree, but a worktree does not
carry the gitignored, machine-specific pieces the workflow depends on:
`.env` (data roots), `CLAUDE.local.md`, and the nested `research_notes/`
repo. Worktrees also leave stray checkouts and branches under
`.claude/worktrees/` and make it unclear which copy is current. The project
has one person driving it, so running sessions in parallel is not needed yet.

## Decision

Hard rule: no git worktrees. Every agent or session works in the main
checkout on its own branch:

- Start from an up-to-date `master`: `git switch -c claude/<short-topic> master`,
  and commit only on that branch.
- When done and the user agrees, merge with `git switch master && git merge
  --no-ff claude/<short-topic>`, then delete the branch. Never push or merge
  without the user's go-ahead.
- One checkout holds one branch, so only one session edits files at a time.
  Before switching branches, `git status` must be clean; if another session's
  changes are there, stop and ask instead of stashing or switching.
- Never run `git worktree add` or ask the tooling for a worktree; start new
  sessions with worktrees turned off.
- `research_notes/` is its own repo; notes are committed directly on its `main`.

## Consequences

- `.env`, `CLAUDE.local.md` and `research_notes/` are always where the code
  expects them.
- Sessions that edit files run one after another; the board's `touches:` line
  still tells which tasks may conflict once parallel work is reconsidered.
- Revisiting worktrees (e.g. for parallel agents) needs a new DEC that
  supersedes this one.
