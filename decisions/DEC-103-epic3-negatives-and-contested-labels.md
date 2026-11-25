---
id: DEC-103
title: Epic 3 negatives and contested labels - every known negative counts and is reported by diffuse disease with an own bar for cirrhosis; contested labels are unknown and reported apart
status: accepted
area: [training, datasets]
created: 2026-11-25
from: [DIS-058]
related: [DEC-060, DEC-100, DEC-101, DEC-102]
superseded_by:
---
# DEC-103: Epic 3 negatives and contested labels

## Context

Points 5 and 6 of [DIS-056](../discussions/DIS-056-epic3-spot-liver-disease-mission.md); counts and
options in [DIS-058](../discussions/DIS-058-epic3-negatives-contested-labels-quality-skips.md).
Hepatoma positives are almost never known to be free of diffuse disease (fewer than 5 of 1,367 on
index v2), and cirrhosis is 58% of them but 2.9% of the samples negative for all four spot classes.
So a model that flags cirrhotic livers passes an overall specificity of 0.90
([DEC-100](DEC-100-epic3-mission-spot-liver-diseases.md) rule 4) without finding lesions.

## Decision

1. **Every known negative counts**, with or without diffuse liver disease, in training, validation and test.
2. **Negatives are reported in four parts**, by the strict_v1 states on index v2; the first that
   matches: cirrhosis (`hepatic_cirrhosis` positive); other diffuse disease (a steatosis grade 1
   to 3 positive or positive_grade_mismatch, or `hepatitis` or `hepatic_precirrhosis` positive);
   none (steatosis grade 0 positive, `hepatic_cirrhosis` and `hepatitis` negative); not known (the
   rest). Specificity and the no-prediction score on negatives (DEC-100 rule 5) are given for each
   part with n and 95% CI. The definitions are the analyst's, those of the counts in DIS-058.
3. **Own bar for cirrhosis.** Specificity on the cirrhosis negatives has its own bar, so that a model
   that flags every cirrhotic liver fails. The metrics session sets the value, how its interval is
   read, and for which of the two items of DEC-100 rule 4 (any spot class, hepatoma) it holds, before the
   first test result and after the number of cirrhosis negatives in test is known. This adds to
   DEC-100 rule 4; the other bars are unchanged.
4. **Contested labels** (P35 and P36 disagree; 304 samples in 4 datasource groups: hepatoma 252,
   hemangioma 65, cyst 25 pairs) stay unknown: no target in strict_v1 and loose_v1 training, not
   scored in validation or test, and their pixels are never background (DEC-100 rule 3). The other
   known pairs of these samples are used. posrich_v1, low priority, trains on them as positives.
5. **Contested results apart.** For the contested samples in test groups, the share the model flags,
   by class and by which project gave the label, is a descriptive table: no bar, not used for model
   selection.

## Consequences

- Validation and test hold only cases the readers agree on, so their scores are optimistic for hard cases.
- The split (point 7) reports the cirrhosis negatives per part. With few of them in test the bar
  of rule 3 has to be read with its interval.
- Counts of the parts after the quality-skip change of [DEC-102](DEC-102-quality-skips-other-organ-projects-index-v2.md):
  all four spot classes negative 13,656 = cirrhosis 418, other diffuse 8,299, none 4,512, not known 427;
  hepatoma negative 14,306 = 470, 8,699, 4,604, 533.
- A doctor's third reading of the 304 samples stays possible; it would come as new tables, not as a change of the 261023 labels.
