---
id: DEC-101
title: Labeling group skip - P7 skip_otherdisease sets aside only the steatosis answers, read through a second fact relations config and sample-label index v2; presence policies keep their versions
status: accepted
area: [datasets, labeling]
created: 2026-11-25
from: [DIS-056]
related: [DEC-053, DEC-059, DEC-060, DEC-061, DEC-100]
superseded_by:
---
# DEC-101: Labeling group skip and sample-label index v2

> Number: this record was `DEC-092` until 2026-11-25. Two records had that number, made in two
> clones at once; this one, not yet shared, took a new number ([DEC-093](DEC-093-id-ledger-number-reservations-task-claims-offline-modes.md)). Commits up to then
> cite it as `DEC-092`.

## Context

The fact relations config of 261023 lists P7 `skip_otherdisease` as a task skip, so the index puts
the skip on every label of the task, and every policy answers `none` there ([DEC-060](DEC-060-first-presence-policies-of-261023.md) Table 2, line 1).
A hepatoma polygon drawn in that task counts as nothing. The reading is R18 (2026-11-12); in P7 it
is respected in 0 of 2,471 labeling tasks (strict reading), but DEC-060 keeps skip rules whatever
their share.

The user (2026-11-25): the tag means the steatosis judgement is skipped because another disease
makes the image hard to grade; it should be read as a labeling group skip, by a new data
interpretation, not by new policy versions. 719 of the 729 tagged samples carry the tumour check
`checked` alone.

## Decision

1. **New fact kind `group_skip`** (target level: labeling group; global term, accepted by the user): the labeler
   sets aside some tag groups, or named tags of them, of a labeling task. The index puts the item
   only on the rows of those labels. A task skip is unchanged.
2. **P7 `skip_otherdisease` is a group skip** of tag group `fat_regions` and of the four grade tags of
   `classify_case`. `classify_case` also holds disease choices, which are not skipped.
   The same tag in P1 (no samples) is not changed.
3. **New files, old ones kept** ([DEC-053](DEC-053-table-naming-and-preservation.md)): a second fact relations config of 261023, the sample-label
   index v2 built with it, and presence tables whose names also carry the index tag. Index v1 and
   the v1 tables stay; Epic 1 keeps using them.
4. **Policies keep their names and rules.** The shared task answer (DEC-060 Table 2, line 1) reads: the
   task has a task skip, or a group skip on the label. Grading tasks (section 3) are read without a
   group skip, as without a task skip. On index v1, which has no group skip, the tables must
   come out identical; a test checks it. This amends [DEC-059](DEC-059-fact-driven-model-sample-label-index-presence-policies.md) section 2 and DEC-060 Table 2.
5. Other skips are not changed here. Quality skips of kidney and gallbladder projects on liver
   samples are a later point of [DIS-056](../discussions/DIS-056-epic3-spot-liver-disease-mission.md); index v2 is built after it, so that one rebuild covers both.

## Consequences

| Class | strict_v1, index v1 to v2 | loose_v1 | posrich_v1 |
|---|---|---|---|
| `hepatoma` positive | 932 to 1,367 | 932 to 1,367 | 1,184 to 1,619 |
| `hepatoma` negative | 13,477 to 13,654 | 15,205 to 15,383 | 15,205 to 15,383 |
| `hemangioma` positive | 166 to 198 | 168 to 200 | 233 to 265 |
| `hepatic_cyst` positive | 92 to 108 | 93 to 109 | 118 to 134 |
| `hepatic_stone` positive | 296 | 296 | 296 |
| `ascites` positive | 103 | 103 | 159 |

Table 1. Pairs per class, simulated in memory by changing only the facts of index v1, with the v1
policies unchanged; no table written. Under strict_v1 and posrich_v1 no pair changes outside the 7
labels of tag group `tumor_regions`.

- Skipping the whole tag group `classify_case` gives the same counts for hepatoma, hemangioma and
  cyst under strict_v1 and posrich_v1. Using the existing undecided closure instead also does, but the
  grades given on these tasks would then count: 28 steatosis pairs change state.
- Cirrhosis among hepatoma positives where known: strict 360 of 813 (v1), 788 of 1,248 (v2);
  posrich v2 1,051 of 1,619. Largest datasource group's share of hepatoma positives: strict 15% and 34%,
  posrich v2 29%.
- `hepatic_cirrhosis` positives under strict_v1 rise from 673 to 1,264. A later cirrhosis task must say
  which index it uses.
- Code: a `method` task (fact kind, config, index and table names, synthetic tests), then a `data` task
  (index v2, presence tables, record).
