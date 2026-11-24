---
id: DEC-093
title: An ID ledger on Gogs reserves every record and task number and holds task claims - a script fetches, appends and pushes it; hooks only check; the member chooses what happens offline (ask, stock, local, tmp, stop)
status: proposed
area: [workflow, infra]
created: 2026-11-24
from: [DIS-051]
related: [DEC-014, DEC-028, DEC-032, DEC-038, DEC-091]
superseded_by:
---
# DEC-093: ID ledger for record and task numbers, task claims and offline modes

## Context

Each member, and each worktree session, creates DIS, DEC and EXP records and board tasks. Numbers
come from the local checkout, so two members can take the same number. Scanning every branch
before creating does not close the gap: unpushed branches of other members are invisible,
deleted branches free their numbers for reuse, and fetch and push still race. Two `/lead`
sessions can also start the same ready task, because board status lives on branches
([DIS-051](../discussions/DIS-051-multi-member-work-without-conflicts.md)).

## Decision

1. **ID ledger.** A branch `id-ledger` in the code repo, on the `gogs` remote
   ([DEC-014](DEC-014-gogs-git-remote.md)), holds one append-only text file. Each line is one
   reservation or claim: kind and number, member handle
   ([DEC-091](DEC-091-member-handles-and-team-table.md)), UTC time, short title. Titles follow
   the rule for committed text: no table rows, file names, folder names or identifiers. The file is
   marked `merge=union`.
2. **What it covers.** DIS, DEC and EXP numbers (in `research_notes/`), task numbers, subtask
   numbers and milestone numbers. It is seeded once with the highest number in use per kind. A
   reserved number that ends up unused is marked dropped and never issued again.
3. **One script does the network work.** `scripts/reserve_id.py` fetches only the ledger branch,
   appends the next free numbers, commits and pushes. If the push is refused because another member
   pushed first, it fetches and retries. It prints only the numbers. Pushes of the ledger branch
   by this script need no go-ahead; every other push still does (amends DEC-014 and the command
   policy for this one branch).
4. **Board tasks.** The board CLI picks task numbers itself. The script fetches first, runs the
   CLI so it can see remote branches, then registers the number the CLI chose. If another member
   holds it, the new task is archived and created again before any work is done on it.
5. **Hooks and checks only check, with no network.** A Claude Code hook denies writing a new
   record file whose number is not reserved by this member in the local copy of the ledger.
   `scripts/check.sh` and the pre-commit hook fail on two files with the same ID.
6. **Task claims.** Before `/lead` spawns an agent on a task, the script adds a claim line for the
   task to the ledger. `ready_tasks.py` reads the ledger and leaves out tasks claimed by anyone. If
   two members claim at once, git lets one push through and the other lead moves on. A claim ends
   when the task reaches Review or Done, or on release by hand. A claim older than 3 days is
   reported to the user. A claim is a lock, not a status: status stays on the board.
7. **When Gogs cannot be reached, the member chooses.** `SONOAI_ID_OFFLINE` in `.env`:
   - `ask` (default): the script asks which of the modes below to use this time;
   - `stock`: hand out numbers reserved earlier while online (`reserve_id.py stock ...`);
   - `local`: the workstation issues the next number itself, recorded as provisional;
   - `tmp`: temporary ids such as `DEC-dev02-tmp1`, renamed on reconnect;
   - `stop`: refuse and wait.

   On reconnect, `reserve_id.py sync` registers provisional numbers. One that another member took
   meanwhile is renumbered: files and references in the working tree are fixed in a new commit
   (no history rewrite), and the ledger records the old and new number so commit trailers that name
   the old one can be resolved. A pre-push hook refuses to push while unsynced provisional numbers
   exist, so a number is never renumbered after it left the workstation. Claims cannot be stocked;
   offline, a claim is provisional under `local` and is checked the same way.

## Consequences

- New script and tests (synthetic, with a temporary bare repo), a new hook, a duplicate-ID check, a
  pre-push hook, changes to `/consult` and `/lead` and to `ready_tasks.py`, and an edit of the
  command policy. Hooks, skills and the policy are guard files: the user merges ([DEC-032](DEC-032-agent-roster-consult-and-lead-skills.md)).
  Carried out by three board tasks.
- Numbers may have gaps (dropped reservations). "Never renumber or reuse" still holds for every
  number that has left a workstation.
- Gogs must be reachable from every workstation; the user sets that up.
- Reversal: medium. Removing the ledger brings back local numbering; the numbers already issued
  stay valid.
