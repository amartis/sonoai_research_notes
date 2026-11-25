---
id: DIS-058
title: Epic 3 points 5 and 6 - negatives, contested labels, and quality skips of other organs' projects
status: concluded
created: 2026-11-25
outcomes: [DEC-102, DEC-103]
related: [DIS-028, DIS-056, DEC-060, DEC-100, DEC-101]
---
# DIS-058: Epic 3 points 5 and 6

## Question

[TASK-263](../../backlog/tasks/task-263%20-%20Decide-epic-3-points-5-and-6-which-negatives-count-contested-labels-of-projects-35-and-36-and-whether-quality-skips-of-other-organs-projects-R19-set-aside-liver-labels-DIS-056.md) (decide points 5 and 6 of epic 3), handoff point 1 of
[DIS-056](DIS-056-epic3-spot-liver-disease-mission.md): which samples count as negative for a spot
liver disease, what the labels that projects 35 and 36 dispute count as, and whether quality skips
of kidney and gallbladder projects set aside liver labels (R19). Sample-label index v2 is built
after the last one.

## Facts checked

Counts from three tables of 261023_plain that the user approved for this session (sample-label
index v1, strict_v1 presence table, taskcrops table; read only, in memory, aggregates; no table
written). Index v2 was simulated in memory from index v1 with the rules of
[DEC-101](../decisions/DEC-101-group-skip-and-sample-label-index-v2.md); it gave that record's
Table 1 counts, and the strict_v1 rerun on v1 equals the stored table (494,441 pairs). Policy
strict_v1 unless said otherwise. A sample is one crop of one image; the data has no patient key;
groups are datasource groups. Pn = labeling project n.

**Quality skips.** 3,518 of 29,233 samples have a quality skip.

- P21 (nephritis) set `skip_badimagequality` on 819 samples. All 819 also have a task of P20,
  P22, P23 or P24 (the other four kidney projects); one of those four set a quality skip on 8 of them (1.0%).
- 925 samples have a quality skip from P15, P21 or P27 only. On all 925 a liver-question project
  gave a label (P14 on 693, P2 and P7 on 232) and, having its own quality tags, set none.
- The R19 respect statistics agree: in P20 and P22 to P24 under 1% of the labeling tasks on flagged
  samples also skip or are empty ([rule_respect.md](../datasets/261023/rule_respect.md) Table 6).

| Class, strict_v1 on index v2 | Quality skips as now (positive / negative) | Other-organ projects' skips freed (positive / negative) |
|---|---|---|
| `hepatoma` | 1,367 / 13,654 | 1,417 / 14,306 |
| `hemangioma` | 198 / 15,005 | 204 / 15,700 |
| `hepatic_cyst` | 108 / 15,137 | 116 / 15,830 |
| `hepatic_stone` | 296 / 15,068 | 296 + <5 / 15,776 |
| `ascites` | 103 / 15,767 | 136 / 16,491 |
| all four spot classes negative | 13,020 | 13,656 |

Table 1. Pairs per class under today's quality-skip reading and the reading of
[DEC-102](../decisions/DEC-102-quality-skips-other-organ-projects-index-v2.md). 1,002 samples in 41 groups are
freed. No class gains a new group. Freeing only P15, P21 and P27: hepatoma 1,411, ascites 136,
all four negative 13,628. Freeing every quality skip: hepatoma 1,429, hemangioma 209.

**Negatives by diffuse disease** (today's quality skips; after DEC-102 in brackets).

| Part | All four spot classes negative | Hepatoma negative | Hepatoma positive |
|---|---:|---:|---:|
| Cirrhosis positive | 376 (418) | 425 (470) | 788 (828) |
| Other diffuse disease (steatosis 1 to 3, hepatitis, precirrhosis) | 7,900 (8,299) | 8,291 (8,699) | 427 (436) |
| None (steatosis 0, cirrhosis and hepatitis negative) | 4,319 (4,512) | 4,408 (4,604) | <5 |
| Not known | 425 (427) | 530 (533) | 152 (153), with the row above |

Table 2. Samples by diffuse liver disease. First matching row counts; a steatosis grade mismatch on grades
1 to 3 counts as steatosis. 70 of the 13,020 have no known liver label; 12,626 of 13,020 are in groups
with a spot positive.

- Cirrhosis is 58% of hepatoma positives and 2.9% of the all-four negatives.
- 352 of the 425 cirrhosis-positive hepatoma negatives are in the 14 groups that also hold
  hepatoma with cirrhosis (418 of 470 after DEC-102). One group holds half of the 788 positives with cirrhosis.

**Contested labels.** 304 samples in 4 groups, all conflicts of P35 (image-level choice) with P36
(polygon). 18 of them have another spot class already positive.

| Class | Contested pairs | P36 drew it, P35 left it unticked | P35 ticked it, P36 closed or left it open |
|---|---:|---:|---:|
| `hepatoma` | 252 | 228 | 24 |
| `hemangioma` | 65 | 26 | 39 |
| `hepatic_cyst` | 25 | 18 | 7 |
| `hepatic_stone` | 0 | 0 | 0 |

Table 3. Contested pairs under strict_v1, the same on index v1 and v2 and after DEC-102. P35 has no closure
for these choices, so its silence is an `open` answer. Of the 304 samples, both projects name some spot finding
(generic tumor and cyst included) on 67, only P36 on 206, only P35 on 31. P35 also leaves unticked 398 of the 701
`hepatic_cirrhosis` labels of P36 on 2,232 shared samples, so its silence is weak evidence; the tables cannot
say which side is right.

## Options considered

| # | Question | Analyst's recommendation | Chosen by the user (2026-11-25) |
|---|---|---|---|
| 1 | Quality skips of projects that ask only about other organs | Own labeling task only, all 23 such projects | The same |
| 2 | Which negatives count | All, reported by diffuse disease, own bar for cirrhosis | The same; the user asked the difference to "no own bar" and was shown it with invented numbers: a model that flags 45 of 60 cirrhotic negatives passes 0.90 overall and fails only under an own bar |
| 3 | Contested labels | Unknown, listed apart | The same |

Table 4. The three questions as put and answered.

Not chosen:
1. P15, P21 and P27 only (a list, not a principle); R19 as it is (wins if an image any reader called bad should not be used).
2. No own cirrhosis bar; negatives without diffuse disease only (the diffuse-disease shortcut would be built in).
3. A third reading by a doctor of the 304 samples (wins if one is free before the split; could add up to 252 hepatoma, 65 hemangioma and 25 cyst positives, 18%, 33% and 23% of the index v2 positives);
   counting P36's drawings as positive where P35 only left the choice unticked (needs a new policy version, which the user declined on 2026-11-25).

## Conclusion

Accepted by the user on 2026-11-25:
[DEC-102](../decisions/DEC-102-quality-skips-other-organ-projects-index-v2.md) (quality skips, index v2) and
[DEC-103](../decisions/DEC-103-epic3-negatives-and-contested-labels.md) (negatives and contested labels).
Board: [TASK-269](../../backlog/tasks/task-269%20-%20Second-fact-relations-config-of-261023-quality-skips-of-the-23-labeling-projects-of-other-organs-become-task-skips-test-and-docs-DEC-102.md) (config edit), then [TASK-264](../../backlog/tasks/task-264%20-%20Build-the-261023-sample-label-index-v2-labeling-group-skip-and-the-strict_v1-and-loose_v1-presence-tables-on-it-dataset-record-with-counts-per-class-and-state-against-v1-DEC-101.md) (index v2 and presence tables); [TASK-270](../../backlog/tasks/task-270%20-%20Decide-epic-3-point-7-one-datasource-group-split-for-every-policy-with-enough-cirrhosis-negatives-in-test-DIS-056.md) (point 7, the split) is the next decision.

Said once by the analyst: the test holds only cases readers agree on, so its scores are optimistic
for hard cases; with about 60 cirrhosis negatives in test (a guess) a measured 0.80 has a 95% Wilson interval of
0.68 to 0.88, so the bar value has to take the interval into account.

No new term: the parts of the negatives are said in words ("stratum" already means something else).

## Open questions

- How many cirrhosis negatives each split holds, and the bar value (points 7 and 10).
- Whether the model's results on the contested samples can be listed at all: they are in 4 groups,
  and only those in test groups are unseen (point 7).
