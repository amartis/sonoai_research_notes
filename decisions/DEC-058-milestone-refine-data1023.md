---
id: DEC-058
title: Milestone refine-data1023 - sample-label index and presence tables of dataset 261023 in four steps, repeatable on later versions
status: proposed
area: [datasets, labeling, workflow]
created: 2026-11-12
from: [DIS-027]
related: [DEC-051, DEC-052, DEC-053, DEC-059]
superseded_by:
---
# DEC-058: Milestone refine-data1023 - sample-label index and presence tables of dataset 261023 in four steps, repeatable on later versions

## Context

[DIS-027](../discussions/DIS-027-fact-driven-model-and-sample-label-index.md): the user
wants one way to read the labels of dataset version 261023 that can be made stricter or
looser, and that repeats on later dataset versions. Today each training task reads the
labels its own way (for example the cirrhosis v4 sample cases,
[DEC-047](DEC-047-cirrhosis-v4-cases-per-project-group-and-liver-fallback.md)). The QA report
([labeling_qa_measures.md](../datasets/261023/labeling_qa_measures.md)) and the
interpretation rules ([interpretation_rules.md](../datasets/261023/interpretation_rules.md),
R01-R64) are the starting point.

## Decision

- **Milestone `m-3` "refine-data1023"** on the board. "1023" is dataset version 261023.
  Its description is its membership rule ([DEC-051](DEC-051-milestone-membership-rule.md)):
  the model, the fact relations config, the index and presence code, the 261023 index and
  presence tables with their dataset records, the rule respect statistics, and the policy
  decisions. Not: training on presence tables (m-1), dataset v2 (m-2), labeling tools,
  board tooling.
- **Four steps**, in the user's order:
  1. define the fact-driven model ([DEC-059](DEC-059-fact-driven-model-sample-label-index-presence-policies.md),
     doc `docs/fact-driven-model.md`);
  2. define the fact kinds of 261023 in a config (tag to label, QA tag to fact kind and the
     content tags it closes);
  3. build the sample-label index of 261023;
  4. build sample-label presence tables of 261023, one per presence policy.
- **Tables** are derived tables of the dataset (`<dataset>/derived/`, plain style, machine01
  only), named by [DEC-053](DEC-053-table-naming-and-preservation.md):
  `sample_label_index_v1_df.pkl` and `sample_label_presence_<policy>_df.pkl`, each with an
  `.xlsx` copy for browsing. Never overwritten; a changed table is a new version.
- **Later dataset versions** reuse the code. Each version gets its own fact relations config
  (its labeling projects differ) and its own tables inside its own folder.
- The first presence policies are chosen by the user **after** seeing the index counts and
  the rule respect statistics, not before.

## Consequences

- Board: milestone `m-3` and the tasks of the plan in DIS-027 (created in the
  `consult-refine-data1023` branch).
- Related open tasks stay where they are for now:
  [TASK-062](../../backlog/tasks/task-062%20-%20Decide-the-rule-for-leaving-out-quality-and-case-exclusion-crops-from-train-val-test-DIS-012.md)
  (rule for leaving out quality and case-exclusion crops) may be answered by a presence
  policy; [TASK-065](../../backlog/tasks/task-065%20-%20Explain-the-6-labeling-projects-of-261023-with-no-crop-row-23-of-choice-pairs.md)
  (projects with no crop row) bears on which projects enter the index.
