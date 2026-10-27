# research_notes

Lab notebook for the sonoai ultrasound ML project. Separate git repo from the
code in `..` (which ignores this folder).

```
INDEX.md       generated overview of all DIS / DEC / EXP notes and their links
discussions/   DIS-NNN: a discussion, the options weighed, and what came out of it
decisions/     DEC-NNN: short records of choices that shape the project (ADR style)
tasks/         retired: work items are Backlog.md tasks in ../backlog/ (see below)
experiments/   EXP-NNN: hypothesis, runs, results, conclusion
journal/       daily notes: journal/2026/2026-10-22.md
datasets/      dataset/label versions, cleaning decisions, statistics (aggregates only)
literature/    paper notes
templates/     copy these to start a note
tools/         build_index.py (regenerates INDEX.md)
```

## Workflow: discussion → decision → task

```
DIS-007 ──▶ DEC-007, DEC-008 ──▶ TASK-015, TASK-016 ──▶ EXP-003
   ▲                                   │
   └──────── a new question comes up ──┘  (DIS-009)
```

1. **Discuss.** A topic gets `discussions/DIS-NNN-slug.md` (status `open`): the
   question, options, conclusion, open questions. It ends `concluded` or `parked`.
2. **Decide.** Each lasting choice becomes `decisions/DEC-NNN-slug.md`, first
   `proposed`, then `accepted` once agreed. Decisions are not rewritten later:
   a change of mind is a new DEC, and the old one becomes `superseded`
   (`superseded_by: DEC-NNN`). Small clarifications may amend in place.
3. **Task.** Work to do becomes a Backlog.md task in the code repo
   (`../backlog/tasks/`, managed with the `backlog` CLI; see `../CLAUDE.md`),
   not a TSK record here. It carries the goal and acceptance criteria, and
   points back at the DIS / DEC it came from with `--ref`. A small, obvious
   task may come straight from a DIS.
4. **Log.** Progress lives on the task: plan, notes (code commit, run
   names, problems) and final summary. Status goes
   `To Do → In Progress → Review → Done` (or `Parked` while it waits on a
   decision). The why stays here in DIS / DEC / EXP.
5. **Index.** Run `python tools/build_index.py` after any change to front
   matter; commit `INDEX.md` with the notes. `--check` verifies it is current
   and that every link resolves.

Rules:

- IDs are sequential per prefix, three digits, never reused or renumbered.
  File name is `<ID>-<short-slug>.md`; the `id` in front matter must match.
- Links live in front matter: `from` (what this came out of), `outcomes`
  (DIS only: what it produced), `related` (anything else),
  `superseded_by` (DEC only). Mention IDs freely in the text too.
- Board task IDs (`TASK-NNN`) go in the text, not front matter:
  `build_index.py` only resolves DIS / DEC / EXP links.
- Code commits in `..` name the task and records they implement, e.g. a
  trailer `Refs: TASK-015, DEC-006`, so `git -C .. log --grep TASK-015`
  finds them.
- TSK records are replaced by Backlog.md tasks; no TSK was ever created.
- The journal stays the free-form daily log; it refers to IDs.

## Linking to code and runs

- Code: commit hash of the `ml_research` repo (`git -C .. rev-parse --short HEAD`).
- Runs: run name; `runs/<name>/config.json` and `meta.json` hold the full config and commit.

## Privacy

No patient images, crops, screenshots of images, file/case names, or
identifiers here. Plots of metrics and aggregate statistics are fine.
The `.gitignore` blocks image and table files as a backstop.
