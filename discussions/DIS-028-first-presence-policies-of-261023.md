---
id: DIS-028
title: First presence policies of 261023 after the index counts and the rule respect statistics (TASK-122)
status: concluded
created: 2026-11-13
outcomes: [DEC-060]
related: [DEC-053, DEC-058, DEC-059]
---
# DIS-028: First presence policies of 261023 after the index counts and the rule respect statistics (TASK-122)

## Question

Which presence policies come first for dataset version 261023, and what is the rule text of
each: when a sample-label pair is positive, when negative, what stays unknown
([TASK-122](../../backlog/tasks/task-122%20-%20Decide-the-first-presence-policies-of-261023-for-example-strict-loose-positive-rich-after-the-index-counts-and-the-rule-respect-statistics-DEC-059.md),
[DEC-059](../decisions/DEC-059-fact-driven-model-sample-label-index-presence-policies.md)
section 4). Now, because the sample-label index v1
([sample_label_index.md](../datasets/261023/sample_label_index.md), [TASK-120](../../backlog/tasks/task-120%20-%20Build-the-261023-sample-label-index-v1-and-its-dataset-record-DEC-059.md)) and the respect
statistics of R01-R64 ([rule_respect.md](../datasets/261023/rule_respect.md), [TASK-121](../../backlog/tasks/task-121%20-%20Respect-statistics-of-the-interpretation-rules-R01-R64-of-261023-from-the-sample-label-index-values-only-the-user-sets-thresholds-after-DEC-059.md)) are
in, and [TASK-123](../../backlog/tasks/task-123%20-%20Presence-policies-registry-the-policies-chosen-in-TASK-122-sonoai-data-sample-label-presence-tests-on-synthetic-rows-DEC-059.md) (policy code) waits on this choice. During the session the user added two
questions: which rules to drop first (interpretation_rules.md says rules not respected are
dropped), and how steatosis grades that differ between labelings should be read. Pn = labeling
project n; names follow [docs/glossary.md](../../docs/glossary.md).

## Evidence

Table 1. What the index and the respect statistics say about each choice a policy makes.
Shares are respected labeling tasks (or sample-label pairs) over tested ones, from
rule_respect.md unless another record is named; n is the number tested. The intervals there
treat units as independent and are too narrow (rule_respect.md, Method).

| Choice in a policy | Evidence (261023) |
|---|---|
| Negatives from a closure ("absent" or "checked") | "Absent" answers hold in 98.2-100% of labeling tasks for every rule part with n ≥ 30 (R01-R07, R11; e.g. R05 P50 13,613 of 13,613, R07 P7 3,489 of 3,494). "Checked" marks are set with 98.5-100% of drawn findings for every part with n ≥ 30 (R13, R15, R16). Exception: R14, P9 `checked`, 29.4% of 3,999 (P9 is not in index v1). |
| Negatives without a closure (visited, not given) | P2 (anatomy), P33 (AI-drafted organs), P35 (organ and disease choices) and the P7 grade choices offer no closure for these tags, so a not-given tag there is the labeler's silence. The tables cannot tell how often it is a true negative. The QA report counts 1,866 submitted labeling tasks without a closing mark ([labeling_qa_measures.md](../datasets/261023/labeling_qa_measures.md), "What this means" 5). |
| Two labeling projects on one fact (second pass, B3) | When at least one side gives the label, both give it in: R55 P35 organ choices against P33 organ polygons 67.4% (n = 8,919 sample-label pairs); R56 P35 disease choices against the organ projects P36-P47 31.1-83.2% (P36 liver 39.1%, n = 2,056); R57 the same steatosis grade 57.9% (n = 995); R61 P2 and P7 against P14 64.3-87.6% (n = 124-226). The QA report reads these as systematic differences between the passes, not as corrected errors. |
| Repeat labeling inside one project (B4) | Identical choice tags in 81.1% (P7, n = 53 labeling-task pairs) to 100% (P22-P24, n = 110-111) (R64). |
| A quality skip and the other projects on the sample (R19) | The other projects' labeling tasks on a sample with a quality skip also skip it, or are empty, in 0.0-97.7% of tasks by project; below 20% for P19-P24, P28, P35, P50. The QA report found that skips depend on the question and the labeler (819 against at most 10 on the same images). |
| Other tags after a skip (R18) | In P7, P9, P14 and P50, skipped labeling tasks still carry other tags (0.0-34.5% respected; P1 and P14 12.8% and 34.5% when ignored tags are allowed). |
| Conformance inside one task (A5, A8, A9) | R22-R24 97.5-99.7%; R27-R32 98.7-100%; R34 99.2-99.5%; R36, R37 above 96.0%; R49 99.6-100% (every rule part with n ≥ 30). Checking them changes few pairs. |
| Size of the index | 1,227,979 rows (sample, content label), 29,233 samples, 100 content labels. Value items: 119,890 given against 1,305,577 not given (8.4% given). Closures: 70,863 absent, 44,321 checked, 1,312 undecided. |

Counts from the index (in memory, read only, 2026-11-13, with the rules agreed below: quality
skip takes the sample out, task skips and undecided closures give nothing, R08 and R10 in P14
dropped, the within-task grade rule applied but not yet the rules between grading tasks, which
move a few hundred grade rows; a one-off script, not kept):

Table 2. Effect of closure-only negatives (the `strict_v1` negative rule) on index v1 of 261023,
against negatives from any visited labeling task (`loose_v1`, `posrich_v1`). The quality-skip
rule is applied first in all three policies: it takes 3,518 of 29,233 samples (12.0%; 129,662
index rows) out.

| Quantity | Value |
|---|---|
| Negative pairs from a closure or a visited task (loose) | 674,476 |
| of these with a closure (kept by strict) | 406,076 (60.2%) |
| of these from visited tasks without a closure (unknown in strict) | 268,400 (39.8%) |
| Samples with at least one such pair | 20,624 of 25,715 (80.2%) |
| Samples with no known pair left under closure-only negatives | 89 (0.3%) |
| Content labels with no negative under closure-only | 19 of 100 (among them the organs knee, prostate, thyroid, uterus; both hepatorenal contrast labels; the four gallbladder size states; generic tumor and cyst) |
| Labeling projects giving the open answers of those pairs | P35 202,328 pairs; P33 58,139; P2 25,919; P14 19,175; P7 8,390; P38, P29, P46, P31, P36 under 5,000 each |
| Positive pairs: no disagreement / any given (strict and loose before A8, A9 / posrich) | 87,646 / 94,393 (6,747 conflicts) |

Table 3. Steatosis grade gap on samples of index v1 with two or more grading tasks, after the
skips (task grade = chosen grade, or highest drawn grade). Counts are samples.

| Grading tasks compared | Gap 0 | Gap 1 | Gap 2 or more |
|---|---:|---:|---:|
| P35 choice against P36 polygons | 572 | 387 | 30 |
| P7 against P14 | 77 | 17 | 0 |
| P7 repeat labeling | 22 | <5 | 0 |

Inside one P7 task, the chosen grade differs from the highest drawn grade in 22 of 3,261 tasks
(all by one level); 23 tasks choose two or more grades (P7, P35). Gap 1 gives 810 grade label
rows where the grading tasks disagree; gap 2 or more gives 60. A further 533 grade rows have a
grading task against a task that gave no grade at all.

## Options considered

### 1. How many first policies, and how they differ

- **A (chosen): three policies as a ladder**, `strict_v1`, `loose_v1`, `posrich_v1`. Each step
  changes one thing, so [TASK-124](../../backlog/tasks/task-124%20-%20Build-the-261023-sample-label-presence-tables-of-the-chosen-policies-dataset-record-comparing-counts-per-label-and-state-across-policies-DEC-059.md) shows each step's effect per label.
- **B: the two ends only** (`strict_v1`, `posrich_v1`). Would win if the extra negatives of
  `loose_v1` were not wanted. The comparison would mix two changes in one step.
- **C: one policy with switches.** The rule text of a named policy would no longer be short and
  fixed.

### 2. Which rules to drop before the policies

- **Chosen (user): drop each rule item (one rule in one labeling project) below 95% respect,
  but always apply the skip rules** (skip-sample, skip-task, skip-part), because a labeler may
  set several skip tags and still label a poor image.
- **Second pass (B3) and repeat labeling (B4) are exempt too** (analyst's recommendation,
  accepted). Under the cut-off every B3 item of index v1 falls below 95% when only pairs with
  one side given count; dropping them would make a given label stand whatever the other pass
  says, so strict and loose positives would equal posrich positives. Their low share measures
  disagreement, which is what the policies handle. The alternative, the cut-off on "all pairs",
  would keep R55, R61 P2/P14 and P7/P14 polygons and drop the others.
- Effect in index v1 (DEC-060 Table 1): two P14 closures (R08, R10) and the R33 checks of P35.

### 3. Scope of a quality skip (R19)

- **Chosen (user): the whole sample, in all three policies** (the user's reading of R19,
  2026-11-12; kept under the skip exemption).
- Not chosen: the whole sample in `strict_v1` only (analyst's first recommendation: other
  projects labeled most such samples), or the skipping task only.

### 4. Negatives in `strict_v1` where a project offers no closure

- **Chosen: closure only.** Cost (Table 2): 268,400 negative pairs (39.8%) become unknown in
  `strict_v1`; 89 samples have no known pair left; 19 labels have no strict negative.
  `loose_v1` and `posrich_v1` keep these negatives.
- Not chosen: visited is enough where the project offers no closure for the label.

### 5. Steatosis grades that differ

- **Chosen (user)**: grading is ambiguous and labelers can be inconsistent. Inside one task, a
  chosen grade that differs from the drawn grade is a human mistake: both labelings are
  ignored. Between two labelings (two projects, or a repeat) that differ by one level, the pair
  gets a new state, `positive_grade_mismatch`, with the gap recorded.
- **Where**: in the presence tables (state plus a `grade_gap` column), computed by the policies
  (analyst's recommendation, accepted). Index v1 already holds both gradings with project,
  task and tag group, and DEC-059 keeps such judgments out of the index. Not chosen: an
  index v2 with a grade-gap column (it would win if tools other than the policies needed the
  gap).
- **Gap of two levels or more** between labelings: both gradings ignored, in every policy, as
  inside one task (accepted default). Not chosen: an ordinary conflict, with contested
  positives in `posrich_v1`.

## Conclusion

The user accepted, on 2026-11-13: three first policies `strict_v1`, `loose_v1`, `posrich_v1`;
rule items below 95% respect are dropped, except the skip rules, B3 and B4; a quality skip takes
the whole sample out in every policy; `strict_v1` negatives need a closure; steatosis grade
rules as in option 5. Recorded as
[DEC-060](../decisions/DEC-060-first-presence-policies-of-261023.md). Board:
TASK-123 (policy code, now naming the three policies) and TASK-124 (the three tables and their
record).

Analyst's choices, told to the user: R18 and R42 read with ignored tags allowed; rule items
with an unknown share kept; tasks choosing two or more grades ignored for grades like a
within-task mismatch; the new state used in all three policies; a repeat inside one project
treated like two projects; a grade row where the other task gave no grade at all is an
ordinary conflict; each policy writes a `reason` column.

## Open questions

- R48 (`skip_no_organ_found` against the routing source) was dropped at 0.0-3.4%; a later
  strict version could instead read it as a conflict on the routed organ, which needs the
  routing map in the fact relations config.
- Open point 3 of rule_respect.md (keep the respect analysis as a `sonoai-data` command) is
  not decided here.
