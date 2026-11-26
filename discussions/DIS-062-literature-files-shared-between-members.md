---
id: DIS-062
title: Literature files shared between members - one shared folder on machine01-host instead of a local copy per machine
status: concluded
created: 2026-11-25
outcomes: [DEC-107]
related: [DEC-021, DEC-052, DEC-078, DEC-092, DEC-098]
---
# DIS-062: Literature files shared between members

## Question

Each member downloads the papers of the literature notes they write, and the files stay on that
member's machine only: the PDFs are kept out of git on purpose (copyright, repo size). The links
in the notes then work on one machine and are broken on the other. The user asked for a solution.

## Facts checked

- `research_notes/literature/` holds three folders of paper files, each with a tracked index
  (`README.md`: reference number, file, version, source). Their indexes list 59, about 40 and 4
  files; machine01-senior has the 59 of one folder and none of the other two.
- The literature notes link to local PDFs 64 times (63 in one study note, 1 in another), as
  relative paths into those folders.
- Each folder ignores `*.pdf` with its own ignore file; the ignore file of the folder with 59
  files was never committed, so on another machine its PDFs would not be ignored.
- Several files could not be fetched by a script: some publishers refused scripted downloads
  (HTTP 403), and two books come from GitHub releases. A per-machine download script would not
  rebuild every folder.
- machine01-host already shares the data root, `logs/` and `runs/` with machine01-senior over
  Samba (SMB 3.1.1 with encryption; [DEC-078](../decisions/DEC-078-team-roles-trusted-workstations-data-root-over-smb3.md)
  (team roles, trusted workstations, data root over SMB3), [DEC-092](../decisions/DEC-092-logs-and-runs-one-folder-per-member-handle.md)
  (logs and runs, one folder per member handle)). A folder under the data root would not do: the
  patient-data hook blocks direct reads there.

## Options considered

- **One shared folder on machine01-host, mounted on machine01-senior** like `logs/` and `runs/`:
  one copy; a file one member adds is there for the other at once; works for files fetched by
  hand; stays out of git. Cons: a Samba share to set up once; links are broken while the share is
  not mounted. Chosen.
- **A separate private Gogs repo holding only the files**: works offline and keeps a history.
  Cons: every new paper is a commit and a push, and pushes need a go-ahead. Would win if members
  need the papers away from the share.
- **A download script that refetches each file from the index's source column**: no shared
  infrastructure. Cons: fails for the files fetched by hand; versions can drift. Dropped.
- **Linking the source URLs instead of local files**: nothing to set up. Cons: no local copy for
  reading offline or for agents that check a claim in the paper. Dropped.

Where the shared folder lives: a new Samba share (chosen), or a folder inside the `runs/` share
(no new share, but papers mixed with training runs). How notes reach it: one ignored link per
machine, `research_notes/literature/files` (chosen; the user chose `files` over `pdfs` because
literature may come in several formats), or the current paths kept with one link per file made by
a script (no note text changed, but the script must be rerun after every new paper).

## Conclusion

The user accepted the shared folder, the new Samba share and one link per machine named `files`
([DEC-107](../decisions/DEC-107-literature-files-in-one-shared-folder.md)). Board tasks:
TASK-276 (link script, ignore rules, link rewrite, onboarding and writing docs) and TASK-277
(roll-out, user steps: the share on machine01-host by the team lead, the mount and moving the
existing files on each machine).

## Open questions

- Copyright: sharing the copies inside the team on a private share is assumed to be as acceptable
  as each member's own copy; not checked.
