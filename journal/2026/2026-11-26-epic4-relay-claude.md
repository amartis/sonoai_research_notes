# 2026-11-26

Relay note for epic 4 (public ultrasound datasets, [DEC-117](../../decisions/DEC-117-epic4-mission-public-ultrasound-datasets.md),
the epic 4 mission): where the epic stands and what each next session takes on. Written by Claude
(Opus 5.5) at the user's request, at the end of the session that wrote the stage 1 study. Not a
decision; it points at the records that are. Public dataset names only; no project data.

Terms: **tier A to D** = how far a download runs unattended (A no login, B a token once, C a manual
step per dataset, D not automatable); **wave 1 to 3** = the download order of the study, Section 5
(tier A, then B, then C). Both are labels of the study only.

## Done

| Item | Where | State |
|---|---|---|
| Mission | [DEC-117](../../decisions/DEC-117-epic4-mission-public-ultrasound-datasets.md) | accepted 2026-11-26 |
| Stage 1 study: census, download plan, AWS design | [epic4-public-ultrasound-datasets-study.md](../../literature/epic4-public-ultrasound-datasets-study.md) | written; nothing decided |
| Eight research notes behind it | [epic4-public-ultrasound-datasets-notes/](../../literature/epic4-public-ultrasound-datasets-notes/) | written |

Table 1. Epic 4 records as of 2026-11-26. None of the files above is committed yet.

## Observations

| Item | Value | Source |
|---|---|---|
| Census rows, five organ groups | 271 (breast and thyroid 54, heart, lung and vessels 51, fetal and gynaecologic 43, abdomen and urology 37, other 86) | study, Table 2 |
| Rows scriptable with no login (tier A) | about 143 (my tally) | study, Section 0 |
| Wave 1 size (tier A sets) | about 1,246 GB; about 766 GB without the 480 GB EchoXFlow echo set | study, Table 5 |
| Real public images with upper-abdominal organ masks | about 1,300 (AUL, Open Kidney, the Vitale set), plus 926 simulated | study, Section 0 |
| Upper-abdominal public images without a signed agreement | about 48,300 before dedup | study, Section 2 |

Table 2. Key numbers.

- **Open questions** for the user: the three of the study, Section 7 (storage rule for public
  ultrasound images, commercial use, the credential for machine01), plus the epic 2 boundary and
  epic 4 retrieval rules (DEC-117 point 4, not decided).
- **Details left out of the study's main text** are now its Section 11 (Table 9, 22 rows), among them
  two AWS security findings about today's setup (Table 9, row 17) that are worth a Triage task.
- **Cost**: the eight researchers of that session ran into the account's API spend limits twice; five
  stopped right after writing their notes, so their last self-checks may be missing. Long sessions
  cost more per turn; start each next step in a new session.
- **Gogs** (shared git server): the DEC-117 number is reserved in the ID ledger; the study, the notes,
  DEC-117 and this note are not committed. A commit and push need the user's ask.

## Next

One session per row. "Can start" names what it waits for.

| # | Session | Scope | Can start |
|---|---|---|---|
| 1 | `/consult` | the open questions above; the storage rule becomes a new DEC (it amends the last bullet of [DEC-063](../../decisions/DEC-063-public-non-patient-datasets-root.md), the public non-patient datasets root); file the AWS findings of the study's Table 9, row 17 as a Triage task | now |
| 2 | Research round 2, new session, inline or at most two agents with a budget | study, Section 12, round 2: plan file draft, high-priority abdomen and liver checks, skipped sources, terms, AWS prices | now; does not wait for 1 |
| 3 | `/consult` | board tasks: plan file, bucket stack, downloader stack, host tests, wave 1 run | after 1 and 2 |
| 4 | `/lead` | the tasks of row 3 | after 3 |
| 5 | Research rounds 3 and 4 | study, Section 12: stage 2 preparation; a disease and organ census for the later focuses of DEC-117 | after 4, or earlier if budget allows |

Table 3. Next sessions for epic 4.
