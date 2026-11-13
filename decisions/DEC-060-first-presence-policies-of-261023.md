---
id: DEC-060
title: First presence policies of 261023 - strict_v1, loose_v1 and posrich_v1, after dropping rule items below 95% respect, with a steatosis grade-mismatch state
status: accepted
area: [labeling, datasets]
created: 2026-11-13
from: [DIS-028]
related: [DEC-053, DEC-058, DEC-059]
superseded_by:
---
# DEC-060: First presence policies of 261023 - strict_v1, loose_v1 and posrich_v1, after dropping rule items below 95% respect, with a steatosis grade-mismatch state

## Context

[TASK-122](../../backlog/tasks/task-122%20-%20Decide-the-first-presence-policies-of-261023-for-example-strict-loose-positive-rich-after-the-index-counts-and-the-rule-respect-statistics-DEC-059.md)
(milestone m-3 refine-data1023, [DEC-058](DEC-058-milestone-refine-data1023.md)). A
**presence policy** is a named, versioned function that turns the rows of the sample-label
index into presence states
([DEC-059](DEC-059-fact-driven-model-sample-label-index-presence-policies.md) section 4,
[fact-driven-model.md](../../docs/fact-driven-model.md) section 5). The first policies were to
be chosen after the index counts
([sample_label_index.md](../datasets/261023/sample_label_index.md)) and the respect statistics
of the interpretation rules R01-R64 ([rule_respect.md](../datasets/261023/rule_respect.md));
[interpretation_rules.md](../datasets/261023/interpretation_rules.md) said that rules not
respected are dropped, with the cut-off set by the user after seeing the values. Evidence,
options and the counts behind each choice:
[DIS-028](../discussions/DIS-028-first-presence-policies-of-261023.md). Names follow
[docs/glossary.md](../../docs/glossary.md). Pn = labeling project n.

This decision amends DEC-059 section 4 in one point: a presence table has a third kept state,
`positive_grade_mismatch`, for the steatosis grade labels (section 4 below).

## Decision

### 1. Which rule items the policies use

A **rule item** is one interpretation rule in one labeling project (for example R18 in P7).

- A rule item whose respected share in rule_respect.md is **below 95%** is dropped: no policy
  uses it.
- **Always used, whatever the share**: the skip rules, because a labeler may set several skip
  tags and still label a poor image: skip-sample (A3, category C1: R19, and R18 for those skip
  tags), skip-task (A10, C6: R18 for those skip tags), R42 (P14 `skip_untouched`), and
  skip-part (A4, C2: R20, R21). Also the second-pass rules (B3: R55-R63) and repeat labeling
  (B4: R64): their share measures how much two labelings disagree, which is what the
  policies handle (section 3), not whether a reading is right.
- R18 and R42 are read with ignored tags allowed (rule_respect.md open point 1).
- A rule item whose share is not known (no case, or fewer than 5 tested with the respected
  count masked) is kept. One whose share is known with fewer than 5 tested (0 respected) is
  judged on that share.

Table 1. Rule items dropped by the 95% cut-off, with their effect on the policies.
Shares from rule_respect.md; "out of index v1" = the labeling project has no crop rows, so the
item has no effect until a later index includes it (TASK-125).

| Rule item | Share | Effect |
|---|---|---|
| R08 P14 `anatomy_absent` | 0% (fewer than 5 tested) | the tag no longer closes the 17 tags of `anatomy_liver` |
| R10 P14 `heaptic_steatosis_absent` | below 83.4% (6 tested) | the tag no longer closes the 10 disease tags of `fat_regions` |
| R17 P14 `imagequality_checked` | 92.3% | none (already an ignored tag) |
| R33 P35 generic `tumor`, generic `cyst` | below 95% (exact shares not shown: counts under 5) | the two `exclusive_sets` entries are not checked by `strict_v1` |
| R48 P36-P39, P41-P47, P50 | 0.0-3.4% | none (no policy uses R48) |
| R14 P9; R25 P11; R33 P49 generic `tumor`; R35 P52; R36 P11; R50 P9 | 29.4%; 0.0%; 91.3%; 71.0%; 0% (fewer than 5); 93.6% | out of index v1 |

The fact relations config of 261023 lists the dropped rule items, so the policies read them
from it and a later dataset version has its own list.

### 2. Task answer

For each labeling task on an index row, a policy reads the **task answer**: what that labeling
task says about the row's content label on its sample. It is read from the task's own fact
items on the row, by the first matching line of Table 2.

Table 2. Task answer of one labeling task for one content label on its sample; the first line
that matches gives the answer. Rule numbers as in interpretation_rules.md.

| Order | Task answer | When | Rules |
|---|---|---|---|
| 1 | `none` | the task has a `task_skip` item; or (P7, P14, visit unit tag group) no tag group of the task that offers the label was visited | R18, R39, R40 |
| 2 | `none` | the label is a steatosis grade (`hepatic_steatosis__0` to `__3`) and a grade rule of section 3 ignores the task's grading | section 3 |
| 3 | `given` | a value item of the task for the label is given (any tag of the label, in any tag group of the task) | value items |
| 4 | `none` | an `undecided` closure of the task covers the label (`cannotdiag`, `hepatic_steatosis__ignore`) | R20, R21 |
| 5 | `closed` | an `absent` or `checked` closure of the task covers the label, and its rule item is not dropped | R01-R16 |
| 6 | `open` | otherwise: the task was visited, did not give the label, and did not close it | R38 |

- A task gives the label when any of its tags of that label is given: a choice and a polygon
  of the same name in one task never split it (A5).
- Several labeling tasks on one row are compared the same way, whatever links them: a second
  pass by another labeling project (B3), a repeat labeling inside one project (B4), or any
  other labeling project that offers the label on the same sample.
- A `quality` item takes the whole sample out (section 4, step 1), so it needs no line here.

### 3. Steatosis grades

The **grade of a grading task** on a sample is its chosen grade, or its highest drawn grade, or
both when they are equal (as R22 and R57 compare them). A grading task is a labeling task that
gives at least one steatosis grade label.

1. **Within one task**: when the chosen grade differs from the highest drawn grade (R22), or
   two or more grades are chosen (R27), the labeler's grading is inconsistent: the task
   answers `none` for every grade label.
2. **Between tasks on one sample** (two labeling projects, or a repeat labeling inside one):
   the sample's **grade gap** is the highest minus the lowest grade of its grading tasks.
   - Gap 0: the policy's ordinary rules apply.
   - Gap 1: on a grade label row where grading tasks disagree (some answer `given`, the others
     `closed` or `open`), the state is **`positive_grade_mismatch`** with `grade_gap` 1, in
     every policy. Rows where they agree follow the ordinary rules.
   - Gap 2 or more: every grading task of the sample answers `none` for every grade label
     (both gradings are ignored).
   - When a task that gives no grade at all disagrees with a grading task, the row follows the
     policy's ordinary rules (a presence conflict, not a grade gap).

### 4. The three policies

Steps shared by all three, before the policy's own rules:

1. If any labeling task on the sample has a `quality` item, every pair of the sample is unknown
   (`sample_quality_skip`; R19).
2. The grade rules of section 3.

Table 3. The three presence policies of 261023 after the shared steps: how each turns the task
answers of one sample-label pair into a state. From left to right, each column changes one
thing (in bold). "Given", "closed", "open" count the labeling tasks on the row with that
answer.

| | `strict_v1` | `loose_v1` | `posrich_v1` |
|---|---|---|---|
| Positive when | given ≥ 1, closed = 0, open = 0, and the kept A8 and A9 checks pass | given ≥ 1, closed = 0, open = 0 **(no A8, A9 checks)** | **given ≥ 1** |
| Negative when | given = 0, closed ≥ 1 | given = 0, **closed + open ≥ 1** | as `loose_v1` |
| Unknown reasons | `sample_quality_skip`, `grade_ignored`, `conflict`, `conformance`, `no_closure`, `no_answer` | `sample_quality_skip`, `grade_ignored`, `conflict`, `no_answer` | `sample_quality_skip`, `grade_ignored`, `no_answer` |
| Table file | `sample_label_presence_strictv1_df.pkl` | `sample_label_presence_loosev1_df.pkl` | `sample_label_presence_posrichv1_df.pkl` |

Rule text, written as the policy docstrings (after the shared steps):

**`strict_v1`**: fewer pairs, strong support.

1. If at least one task answers `given`:
   - if another task answers `closed` or `open`, unknown (`conflict`);
   - else if a kept conformance check fails, unknown (`conformance`): **A8**, a task that gives
     the label also gives another tag of an `exclusive_sets` entry that holds the label's tag;
     **A9**, the label's tag is the subject of an `implied_tags` entry and its target is not
     given where the entry names it (the same task, or the named labeling project on the same
     sample), or the entry has `value: absent` and its target is given;
   - else positive (reason `given`).
2. If no task answers `given` and at least one answers `closed`, negative (reason `closed`).
3. Otherwise unknown: `no_closure` when a task answers `open`; `grade_ignored` when a grade rule
   set a task's answer to `none`; else `no_answer`.

**`loose_v1`**: more pairs, weaker negatives.

1. If at least one task answers `given`: unknown (`conflict`) when another task answers
   `closed` or `open`; else positive (reason `given`).
2. If no task answers `given` and at least one answers `closed` or `open`, negative (reason
   `closed` when a task answers `closed`, else `open`).
3. Otherwise unknown (`grade_ignored` or `no_answer`, as in `strict_v1`).

**`posrich_v1`**: more positives, which are rare.

1. If at least one task answers `given`, positive: reason `given`, or `given_contested` when
   another task answers `closed` or `open`.
2. If no task answers `given` and at least one answers `closed` or `open`, negative (reason as
   in `loose_v1`).
3. Otherwise unknown (`grade_ignored` or `no_answer`).

### 5. Output

- **States kept in a presence table**: `positive`, `negative` and, for the steatosis grade
  labels only, `positive_grade_mismatch`. Unknown pairs are left out, as before.
- **Added columns** beside those of fact-driven-model.md Table 3: `reason` (the reason of the
  state, e.g. `given_contested`, `open`, `grade_mismatch`) and `grade_gap` (the sample's grade
  gap on steatosis grade rows of samples with two or more grading tasks; empty otherwise).
  A trainer can then leave out contested positives, `open` negatives or mismatched grades
  without a new policy.
- **Basis**: the tasks answering `given` for a positive; the grading tasks of the row for
  `positive_grade_mismatch`; the tasks answering `closed` (`strict_v1`), or `closed` and
  `open` (the other two), for a negative.
- The summary sheet counts rows per label, state and reason, and the unknown index rows per
  reason. Pairs not in the index stay unknown and are not counted per reason.

### 6. Not in the first policies

- **R48** (dropped, Table 1).
- **An answered single choice as a closure** (one chosen grade closing the other grades): not
  used. In `strict_v1`, P7 and P35 grade choices give positives but no negatives.
- The `second_pass` entries of the config are not needed: every task on a row is compared.
- P4, P9, P11: not in index v1
  ([TASK-125](../../backlog/tasks/task-125%20-%20Decide-whether-P4-P9-and-P11-linked-to-P2-only-by-task-order-enter-a-later-sample-label-index-DEC-059.md)).

## Consequences

- [TASK-123](../../backlog/tasks/task-123%20-%20Presence-policies-registry-the-policies-chosen-in-TASK-122-sonoai-data-sample-label-presence-tests-on-synthetic-rows-DEC-059.md)
  implements sections 1-5: the dropped rule items in the fact relations config, the task
  answer, the grade rules, the three policies, the `reason` and `grade_gap` columns and the new
  state; [TASK-124](../../backlog/tasks/task-124%20-%20Build-the-261023-sample-label-presence-tables-of-the-chosen-policies-dataset-record-comparing-counts-per-label-and-state-across-policies-DEC-059.md)
  builds the three table pairs and compares them per label, state and reason.
- The glossary entry "presence state" gains `positive_grade_mismatch`.
- A changed rule is a new version (for example `strict_v2`) with its own table file; earlier
  tables stay ([DEC-053](DEC-053-table-naming-and-preservation.md)).
