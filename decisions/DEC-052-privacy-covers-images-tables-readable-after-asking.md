---
id: DEC-052
title: Patient privacy covers the images only; tables, file and folder names are readable after the user approves a list per task
status: accepted
area: [data-security, workflow]
created: 2026-11-11
from: []
related: [DEC-018, DEC-024, DEC-032]
superseded_by:
---
# DEC-052: Patient privacy covers the images only; tables, file and folder names are readable after the user approves a list per task

## Context

Until now the hard rules in `CLAUDE.md` treated images *and* labels as patient data.
Claude could not print, list or summarise any data file, file name or folder name under
the data roots, only counts and aggregates (the rule also appears in
[DEC-018](DEC-018-plain-style-for-local-research.md), "Unchanged"). That made table
work (taskcrops, label tables, `derived/` tables) slow, because every check went
through a notebook the user had to run. On 2026-11-11 the user narrowed patient privacy
to the images. They asked to keep one control: Claude asks which data sheets it will
read or write before it does so.

## Decision

- **Patient data = the images.** Claude never opens, displays, renders or describes
  an image, as before.
- **Tables, file names and folder names** under the data roots may be read and
  analysed for a task the user gave. Before starting, Claude lists each table it will
  read or write (dataset version, file, read or write, why), and the user approves it.
  One approval covers that list for that task. A new table needs a new ask.
- **Agents**: the list is a `tables:` line in the board task, written by `/consult`
  and approved with the task. An agent whose task lacks the line, or needs another
  table, stops and returns the question. The lead does not spawn such a task without
  an approved list.
- **The hook** (`.claude/hooks/guard_patient_data.py`) asks ("Allow once") on a direct
  Read of a table file under a data root, and on a Write/Edit of one inside `derived/`.
  It still denies images, folders (Grep, Glob), shell commands that name a data root,
  and the key and passphrase files. Python reaching a table through `sonoai.paths` is
  not seen by the hook; there the rule depends on Claude following it.
- **Unchanged**: committed text (commits, board, notes, EXP and dataset records,
  notebooks) holds no table rows, file names, folder names or identifiers, only
  aggregates. Writes stay inside `derived/`. No data copies elsewhere. No enc1
  decryption to disk. Passphrase and key rules unchanged.
  [DEC-024](DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)
  still holds: no plain table, file name or folder name goes to S3, EC2, RunPod or
  the GPU box.
- **Accepted exposure**: a table Claude reads reaches Anthropic's API as part of the
  conversation. The user accepted this. Images never do.
- File names (for example `taskcrops_df.filepath2`) are readable on the same terms.
  Whether the original names hold patient identifiers was not checked. They are kept
  out of committed text for that reason.

## Consequences

- Rule text: `CLAUDE.md` (patient-data section), `docs/command-policy.md` (D1 narrowed,
  new A10), `docs/workflow.md` (assigned-task step 3), `.claude/agents/data.md` and
  `exp.md`, `.claude/skills/consult` and `lead`. Branch `claude/privacy-tables-only`.
- Hook and its tests: `.claude/hooks/guard_patient_data.py`,
  `tests/test_guard_patient_data.py`.
- To reverse: revert the merge commit and mark this DEC superseded.
