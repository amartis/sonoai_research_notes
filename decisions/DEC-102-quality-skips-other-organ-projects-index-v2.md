---
id: DEC-102
title: Quality skips of labeling projects that ask only about organs other than the liver set aside only their own labeling task, in the second fact relations config and sample-label index v2
status: accepted
area: [datasets, labeling]
created: 2026-11-25
from: [DIS-058]
related: [DEC-053, DEC-059, DEC-060, DEC-100, DEC-101]
superseded_by:
---
# DEC-102: Quality skips of other organs' projects, index v2

## Context

Under R19, a quality skip by any labeling project sets the whole sample aside in every presence
policy ([DEC-060](DEC-060-first-presence-policies-of-261023.md) section 4, the user's reading of
2026-11-12). [DIS-058](../discussions/DIS-058-epic3-negatives-contested-labels-quality-skips.md):
P21 (nephritis) set it on 819 samples and the other kidney projects on 8 of the same samples; on
all 925 samples where only P15, P21 or P27 set one, a liver-question project gave labels and set
none of its own quality tags. So such a skip says the image is bad for that project's question,
not that it is bad for the liver.

## Decision

1. In `configs/data/fact_relations_261023_v2.yaml` the quality skip (`skip_badimagequality`) of the
   23 labeling projects that ask only about organs other than the liver (P15, P20 to P24, P26 to
   P32, P37 to P39, P41 to P47) is a **task skip**: it sets aside only its own labeling task (R18).
2. The quality skips of P1, P2, P3, P4, P7, P9, P11, P14, P33, P35, P36, P49 and P50 keep setting the
   whole sample aside (R19).
3. Index v2 only. The first config, index v1 and its presence tables are not changed
   ([DEC-053](DEC-053-table-naming-and-preservation.md)); Epic 1 keeps using them. The policies
   keep their names and rules: a quality item still makes every pair of its sample unknown.
4. This closes rule 5 of [DEC-101](DEC-101-group-skip-and-sample-label-index-v2.md) and amends, for index v2,
   R19 and DEC-060 section 4 step 1 as far as rule 1 says.

## Consequences

| Class, strict_v1 | Index v2, quality skips as now | Index v2, this decision |
|---|---|---|
| `hepatoma` positive / negative | 1,367 / 13,654 | 1,417 / 14,306 |
| `hemangioma` positive / negative | 198 / 15,005 | 204 / 15,700 |
| `hepatic_cyst` positive / negative | 108 / 15,137 | 116 / 15,830 |
| `hepatic_stone` positive / negative | 296 / 15,068 | 296 + <5 / 15,776 |
| `ascites` positive / negative | 103 / 15,767 | 136 / 16,491 |
| all four spot classes negative | 13,020 | 13,656 |

Table 1. Pairs per class, simulated in memory from index v1; no table written. The middle column is
the strict_v1 column of DEC-101 Table 1 for the same index v2.

- 1,002 samples in 41 datasource groups are freed for every label, not only the liver's. A later
  kidney or gallbladder task must say which index it uses.
- Cirrhosis among hepatoma positives where known: 828 of 1,298 (DEC-101: 788 of 1,248).
- Code: config edit and its test, `docs/fact-driven-model.md` section 3 and `docs/datasets/styles/derived.md`
  (a `data` task), then [TASK-264](../../backlog/tasks/task-264%20-%20Build-the-261023-sample-label-index-v2-labeling-group-skip-and-the-strict_v1-and-loose_v1-presence-tables-on-it-dataset-record-with-counts-per-class-and-state-against-v1-DEC-101.md) (index v2 and presence tables) uses the edited config.
