---
id: DEC-107
title: Literature files live in one shared folder on machine01-host, reached on every machine through the ignored link research_notes/literature/files
status: accepted
area: [workflow, infra]
created: 2026-11-25
from: [DIS-062]
related: [DEC-021, DEC-052, DEC-078, DEC-092]
superseded_by:
---
# DEC-107: Literature files in one shared folder

## Context

Paper files (PDFs, books, any other format) are kept out of git, so each copy lived only on the
machine of the member who downloaded it, and links in the literature notes were broken on every
other machine ([DIS-062](../discussions/DIS-062-literature-files-shared-between-members.md),
literature files shared between members).

## Decision

1. **One shared copy.** Literature files live in one folder on machine01-host, shared over Samba
   like `logs/` and `runs/` (SMB 3.1.1 with encryption, [DEC-078](DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md),
   team roles and trusted workstations) and mounted at `/mnt/sonoai_literature` on
   machine01-senior. Its path is `SONOAI_LITERATURE_ROOT` in `.env`. It is never under the data
   root. The files stay out of git.
2. **One link per machine.** Each machine has one ignored symbolic link,
   `research_notes/literature/files`, pointing at that folder. Inside it, one folder per set of
   literature files, named like the tracked folder that holds its index
   (`research_notes/literature/<name>/README.md`).
3. **Links in notes.** Notes link a file as `files/<name>/<file>` relative to
   `research_notes/literature/` (with the matching `../` prefix from elsewhere). Any file format is
   allowed.
4. **Adding files.** A member saves new files in the shared folder and adds the row to the tracked
   index; never overwrites, renames or deletes a file another member added.
5. **Not patient data.** Literature files hold no patient data and no data-root names; the
   patient-data rules ([DEC-052](DEC-052-privacy-covers-images-tables-readable-after-asking.md), images are
   patient data, tables readable after asking) do not apply to them, and nothing from the data root goes there.

## Consequences

- One setup step per machine (mount, `.env` line, link); a new member gets it in onboarding.
- While the share is not mounted, the links are broken on machine01-senior.
- The 64 existing links to local PDFs and the three index files are rewritten once; the
  per-folder ignore files are replaced by one rule in `research_notes/.gitignore`.
- Copyright of sharing the copies inside the team: assumed acceptable, not checked (DIS-062).
- Carried out by [TASK-276](../../backlog/tasks/task-276%20-%20Literature-files-through-one-link-research_notes-literature-files-link-script-one-ignore-rule-rewrite-the-note-links-onboarding-and-writing-docs-DEC-107.md) (link script, ignore rules, link rewrite, docs) and [TASK-277](../../backlog/tasks/task-277%20-%20Roll-out-the-shared-literature-folder-the-Samba-share-on-machine01-host-the-mount-and-link-on-machine01-senior-existing-files-moved-in-user-steps-DEC-107.md) (roll-out,
  user steps).
