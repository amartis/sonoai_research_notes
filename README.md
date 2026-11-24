# research_notes

Lab notebook for the sonoai ultrasound ML project. Separate git repo from the
code in `..` (which ignores this folder).

```
INDEX.md       generated overview of all DIS / DEC / EXP notes and their links
discussions/   DIS-NNN: a discussion, the options weighed, and what came out of it
decisions/     DEC-NNN: short records of choices that shape the project (ADR style)
experiments/   EXP-NNN: hypothesis, runs, results, conclusion
journal/       daily notes: journal/2026/2026-10-22.md
datasets/      dataset/label versions, cleaning decisions, statistics (aggregates only)
literature/    paper notes
templates/     copy these to start a note
tools/         build_index.py (regenerates INDEX.md, links IDs in note text);
               setup_merge.py + post_merge_index.sh (INDEX.md merge setup)
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
5. **Index.** Run `python tools/build_index.py` after any change to a note;
   it links IDs in the text (see "Links in note text") and rewrites
   `INDEX.md`. Commit both with the notes. `--check` changes nothing and
   exits 1 if `INDEX.md` is stale, an ID in the text is unlinked or unknown,
   or a link does not resolve.

Rules:

- IDs are sequential per prefix, three digits, never reused or renumbered.
  File name is `<ID>-<short-slug>.md`; the `id` in front matter must match.
- Every DEC has `area: [..]` in front matter: one or more of `data-security`,
  `datasets`, `labeling`, `training`, `workflow`, `infra`, `aws` (list fixed by
  DEC-040; a new area is a new DEC that edits the list and `AREAS` in
  `tools/build_index.py`). Pick by what the decision governs now, not by where it
  came from; use two areas only when it truly governs both (e.g. an AWS service
  that holds patient data: `aws`, `data-security`). Superseded DECs get an area too.
  `INDEX.md` lists accepted DECs by area; `--check` fails on a missing or unknown area.
- Links live in front matter: `from` (what this came out of), `outcomes`
  (DIS only: what it produced), `related` (anything else),
  `superseded_by` (DEC only). `INDEX.md` shows them as links. Mention IDs
  freely in the text too; the index tool links them.
- Board task IDs (`TASK-NNN`) go in the text, not front matter: front matter
  only resolves DIS / DEC / EXP links.
- Code commits in `..` name the task and records they implement, e.g. a
  trailer `Refs: TASK-015, DEC-006`, so `git -C .. log --grep TASK-015`
  finds them.
- TSK records are replaced by Backlog.md tasks; no TSK was ever created.
- The journal stays the free-form daily log; it refers to IDs.

## After a merge (INDEX.md)

`INDEX.md` is generated, so it never needs a hand-resolved conflict. Once per clone, run
`python3 tools/setup_merge.py` (a merge driver and a post-merge hook live in each clone's own
git config, so a new clone must run it; it is in `docs/onboarding.md` step 3). `.gitattributes`
sends `INDEX.md` to the driver `index`, which keeps our copy without a conflict; the hook then runs
`tools/build_index.py` and puts the regenerated `INDEX.md` into the merge commit.

- Conflicts in note files themselves are still resolved by hand. `git commit` does not run the hook
  (git runs post-merge only from `git merge`), so after resolving run `python3 tools/build_index.py`,
  stage `INDEX.md` with the resolution before committing (or `git commit --amend --no-edit` after),
  and confirm with `python3 tools/build_index.py --check`.
- After a fast-forward (`git pull`) or `--squash` merge, without the setup, or after a rebase,
  cherry-pick or stash pop (the driver silently keeps our `INDEX.md` there and no hook runs): run
  `python3 tools/build_index.py` and commit `INDEX.md`. Never edit `INDEX.md` by hand.
- If `core.hooksPath` points to a tracked folder, setup adds an untracked `post-merge` file there;
  do not commit it, or call `tools/post_merge_index.sh` from your own hook.

## Links in note text

Links between notes are made by `tools/build_index.py`, not by hand (DEC-021).
Write IDs as plain text; each run turns the first bare mention of each
DIS / DEC / EXP / TASK ID in a note into a relative markdown link, e.g.
`DEC-012` becomes `[DEC-012](DEC-012-dataset-docs-layout.md)` in a decision.

- Notes covered: `discussions/`, `decisions/`, `experiments/`, `journal/`,
  `datasets/`, `literature/`. Not `README.md`, `INDEX.md` or `templates/`.
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
