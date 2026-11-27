# research_notes

Lab notebook for the sonoai ultrasound ML project. Separate git repo from the
code in `..` (which ignores this folder).

```
discussions/   DIS-NNN: a discussion, the options weighed, and what came out of it
decisions/     DEC-NNN: short records of choices that shape the project (ADR style)
experiments/   EXP-NNN: hypothesis, runs, results, conclusion
journal/       daily notes: journal/2026/2026-10-22.md
datasets/      dataset/label versions, cleaning decisions, statistics (aggregates only)
literature/    paper notes
templates/     copy these to start a note
tools/         build_index.py (links IDs in note text, checks front matter, lists DECs by area)
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
   (`../backlog/tasks/`, managed with the `backlog` CLI; see `../docs/workflow.md`),
   not a TSK record here. It carries a scope (`coord`, `data`, `method`,
   `exp`, `infra`), the files or areas it `touches`, and acceptance criteria,
   and points back with `--ref` at the DEC it came from (a small, obvious
   task may come straight from a DIS).
4. **Log.** Progress lives on the task: plan, notes (code commit, run
   names, problems) and final summary. Status goes
   `Triage → To Do → In Progress → Review → Done` (or `Parked` while it
   waits on a decision); small, obvious tasks skip Triage (DEC-009). The why stays here in DIS / DEC / EXP.
5. **Links.** Run `python tools/build_index.py` after any change to a note;
   it links IDs in the text (see "Links in note text"). Commit with the notes.
   `--check` changes nothing and exits 1 if an ID in the text is unlinked or
   unknown, a link does not resolve, or front matter is wrong.
   `--area <area>` prints the accepted DECs of one area. There is no committed
   index (dropped 2026-11-26); `--index` writes a local, gitignored `INDEX.md`
   if you want an overview to browse.

Rules:

- IDs are sequential per prefix, three digits, never reused or renumbered.
  File name is `<ID>-<short-slug>.md`; the `id` in front matter must match.
- Every DEC has `area: [..]` in front matter: one or more of `data-security`,
  `datasets`, `labeling`, `training`, `workflow`, `infra`, `aws` (list fixed by
  DEC-040; a new area is a new DEC that edits the list and `AREAS` in
  `tools/build_index.py`). Pick by what the decision governs now, not by where it
  came from; use two areas only when it truly governs both (e.g. an AWS service
  that holds patient data: `aws`, `data-security`). Superseded DECs get an area too.
  `--area` lists accepted DECs by area; `--check` fails on a missing or unknown area.
- Links live in front matter: `from` (what this came out of), `outcomes`
  (DIS only: what it produced), `related` (anything else),
  `superseded_by` (DEC only). Mention IDs
  freely in the text too; the index tool links them.
- Board task IDs (`TASK-NNN`) go in the text, not front matter: front matter
  only resolves DIS / DEC / EXP links.
- Code commits in `..` name the task and records they implement, e.g. a
  trailer `Refs: TASK-015, DEC-006`, so `git -C .. log --grep TASK-015`
  finds them.
- TSK records are replaced by Backlog.md tasks; no TSK was ever created.
- The journal stays the free-form daily log; it refers to IDs.

## Old INDEX.md merge setup (remove once per clone)

`INDEX.md` was a committed, generated file with its own merge driver and post-merge hook
(TASK-245). It is no longer committed, so that setup is not needed. A clone that ran the old
`tools/setup_merge.py` removes it once (the hook body `tools/post_merge_index.sh` is now a no-op,
so nothing breaks before that):

```bash
git config --remove-section merge.index; rm -f "$(git rev-parse --git-path hooks/post-merge)"
```

## Links in note text

Links between notes are made by `tools/build_index.py`, not by hand (DEC-021).
Write IDs as plain text; each run turns the first bare mention of each
DIS / DEC / EXP / TASK ID in a note into a relative markdown link, e.g.
`DEC-012` becomes `[DEC-012](DEC-012-dataset-docs-layout.md)` in a decision.

- Notes covered: `discussions/`, `decisions/`, `experiments/`, `journal/`,
  `datasets/`, `literature/`. Not `README.md` or `templates/`.
- TASK IDs (subtasks too, e.g. `TASK-001.01`) link to the task file under
  `../backlog/tasks/` (or `completed/`, `archive/tasks/` once moved there).
- Left alone: front matter, fenced code, code spans, existing links (an ID
  anywhere in a link's text counts as linked), URLs, HTML comments, and the
  note's own ID. Later mentions of an ID stay plain, so a second run changes
  nothing.
- An ID with no note or task (e.g. one not created yet) is an error; put it in
  a code span to mention it anyway.
- If a link breaks (for example, a task file is renamed), `--check` reports
  it: replace the link with the bare ID and run the tool again.

## Linking to code and runs

- Code: commit hash of the `ml_research` repo (`git -C .. rev-parse --short HEAD`).
- Runs: run name; `runs/<name>/config.json` and `meta.json` hold the full config and commit.

## Privacy

No patient images, crops, screenshots of images, file/case names, or
identifiers here. Plots of metrics and aggregate statistics are fine.
The `.gitignore` blocks image and table files as a backstop.
