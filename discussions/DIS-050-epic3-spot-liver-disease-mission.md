---
id: DIS-050
title: Epic 3 - diagnosing spot liver diseases - mission, classes, bar, and the reading of P7 skip_otherdisease
status: open
created: 2026-11-25
outcomes: [DEC-091, DEC-092]
related: [DEC-059, DEC-060, DEC-065, DEC-076, DIS-048, DIS-049, EXP-003]
---
# DIS-050: Epic 3 - diagnosing spot liver diseases

## Question

The user wants a research epic that builds a model for spot liver diseases. Points 1 to 4 of a
12-point list (mission, classes, truth, use and bar) are discussed here; points 5 to 12 follow
in their own sessions. "Spot" is the non-diffuse shape of
[labels-261023](../../docs/labels-261023.md).

## Facts checked

Counts from three tables of 261023_plain that the user approved for this task (strict_v1
presence table, sample-label index v1, taskcrops table; read only, aggregates, in memory). A
sample is one crop of one image; the data has no patient key. Groups are datasource groups.

| Class | Positive | Negative | Groups with a positive (with at least 20) | Largest group's share |
|---|---:|---:|---:|---:|
| `hepatoma` | 932 | 13,477 | 18 (11) | 15% |
| `hemangioma` | 166 | 14,425 | 13 (2) | 43% |
| `hepatic_cyst` | 92 | 14,540 | 12 (1) | 29% |
| `hepatic_stone` | 296 | 15,068 | 38 (5) | 16% |
| `ascites` (liver_ascites and two ascites signs join it) | 103 | 15,767 | 10 (2) | 40% |

Table 1. Classes under strict_v1. Ascites reaches the user's threshold of 30 positives. 14,260
samples have a known state for the first four classes, 11,084 for all five; 12,879 are negative
for the first four and 1,428 positive for at least one.

- Liver polygon present on all but <5 of the 932 hepatoma positives. Hepatoma and stone are both positive
  on 42 samples, the most common pair.
- Cirrhosis where known: 360 of 813 hepatoma positives, 263 of 13,252 hepatoma negatives.
- Hepatoma in projects 35 (choice) and 36 (polygon), 2,232 shared samples, 4 groups: both 314,
  35 only 24, 36 only 228, neither 1,666; Cohen's kappa 0.65, positive agreement 0.71.
  Hemangioma 0.72 and 0.73, cyst 0.74 and 0.74. Whether the same people labelled both is unknown.
- 253 of the 296 stone positives come from one labeling project (P50).
- Median polygon area of the crop: hepatoma 2.8%, hemangioma 0.7%, cyst 0.7%, stone 0.2%
  ([label-guide](../../docs/label-guide.md)).
- `skip_otherdisease` in P7: 729 samples in 10 groups; 719 of them carry the tumour check
  `checked` alone. P7 gives no labels on the Epic 1 organ rows (0 non-quality facts), so the
  Epic 1 tables do not change.
- Published comparison, read in the PDF: Tiyarattanachai 2021 (10.1371/journal.pone.0252882)
  trained on 20,432 lesions with pathology or CT/MRI truth; detection 87.0% internal, 75.0%
  external.

## Options considered

| # | Question | Analyst's recommendation | Chosen by the user (2026-11-25) |
|---|---|---|---|
| 1 | Mission and bar | Outline plus image-level yes/no; claim "agrees with readers", sensitivity 0.80, specificity 0.90 (analyst's numbers) | Image-level presence bar understood; also track DSC and W1/W2-like scores, GT-by-prediction confusion matrix, sensitivity-specificity curve and AUC. Details at the metrics stage |
| 2 | Classes | Hepatoma, and haemangioma plus cyst merged | Hepatoma, hemangioma, hepatic_cyst, hepatic_stone as own classes; ascites if above 30 positives, low importance and left out of balancing; some balancing strategy |
| 3 | More than 430 hepatoma samples under P7 `skip_otherdisease` | Count them, by a new presence policy | Yes, later by a new data interpretation instead of a policy. The tag means P7 skips the steatosis judgement because another disease makes the image hard to grade |

Table 2. Points 1 to 3 as put and answered. The analyst had described question 1 as a hepatoma
bar; the user's reading is a disease-agnostic presence bar. DEC-091 proposes both.

## Does Epic 1 already read the tag this way?

No. `strict_v1` sets the whole P7 task aside (R18), so its tumour labels are unknown; the
sample stays for other projects. Epic 1 is unaffected, because P7 gives none of its organ labels.

The same holds for loose_v1 and posrich_v1: all three share the step that sets the task aside. The
user (2026-11-25) asked to try several policies, posrich_v1 included; DEC-091 rule 3 and DEC-092 take
this up. The user then (2026-11-25) declined new policy versions and asked for a new data
interpretation that reads `skip_otherdisease` as a labeling group skip; DEC-092 was rewritten.

## Conclusion

Accepted by the user on 2026-11-25: [DEC-091](../decisions/DEC-091-epic3-mission-spot-liver-diseases.md)
(mission) and [DEC-092](../decisions/DEC-092-group-skip-and-sample-label-index-v2.md) (labeling group
skip, index v2). Policy order: strict_v1, then loose_v1, posrich_v1 low priority; the user agreed that
posrich lowers label quality.

Said once by the analyst: no pathology is recorded for any label, so the claim is agreement with
readers; hemangioma and cyst are too few for a per-class bar (Epic 1 asked at least 200 test
positives per organ, [DEC-075](../decisions/DEC-075-epic1-split-values-tolerance-and-minimum-counts.md)); counting the P7 hepatomas raises the cirrhosis share of hepatoma
positives (DEC-092), so the shortcut test matters more. loose_v1 adds almost no positives
and about 1,700 hepatoma negatives from tasks that never closed the label.

Term decided (global): **labeling-group skip** (`group_skip`). Phrase it replaces: "a skip tag that
sets aside only some tag groups, or named tags of them, of its task". It recurs (config, index, docs)
and no existing fact kind says it. Other name considered: `part_skip`.

## Next session (handoff)

1. **Points 5 and 6, negatives and label conflicts.** To settle: which negatives count
   (diffuse disease or none, reported separately); the contested labels (hepatoma 252, hemangioma 65,
   cyst 25 under strict_v1, all projects 35 and 36); and whether quality skips of other organs'
   projects apply to the liver: 67 hepatoma samples with a given label are unknown for a quality
   skip, most of them from kidney and gallbladder projects (P15, P21, P27), and 33 of the ascites
   ones from P21. R19 is the user's reading of 2026-11-12. Index v2 is built after this point.
2. **Point 7, split.** Table 1 gives the groups per class; one split for every policy.
3. **Point 8, more data.** Public sets to check: SMC-LUD 2026 (Figshare article 31112716; an
   unreviewed audit questions its patient split), AUL 2022 (Zenodo 7272660, CC BY 4.0), TCIA
   B-mode-and-CEUS-Liver (10.7937/TCIA.2021.v4z7-tc39, CC BY 4.0). Each needs its own decision
   ([DEC-063](../decisions/DEC-063-public-non-patient-datasets-root.md)). Tiyarattanachai 2021 (10.1371/journal.pone.0252882): no repository or data committee in
   the paper or its supplement; ask the corresponding author, then plosone@plos.org. No request sent.
   What to ask for: images with lesion boxes and diagnoses (at least the external test sets),
   pseudonymous patient and study IDs, hospital and machine model, how each diagnosis was confirmed;
   if refused, which committee handles requests, or evaluation of our model at their site.
4. **Points 9 to 12.** Task form (overlapping classes: hepatoma and stone on 42 samples), metrics
   (DEC-091 rule 5), model, input size, optimisation with balancing, organisation.

## Open questions

The points above; none block the code task of DEC-092.
