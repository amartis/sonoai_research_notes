---
id: DIS-027
title: Fact-driven model of labels, the sample-label index and presence tables of dataset 261023 (milestone refine-data1023)
status: open
created: 2026-11-12
outcomes: [DEC-058, DEC-059]
related: [DEC-036, DEC-044, DEC-045, DEC-047, DEC-051, DEC-052, DEC-053, DEC-057]
---
# DIS-027: Fact-driven model of labels, the sample-label index and presence tables of dataset 261023 (milestone refine-data1023)

## Question

The user (2026-11-12, `/consult`) wants a milestone **refine-data1023** whose goal is a
**sample-label index** (`sample_label_index_df`) of dataset version 261023, built so that the
same steps repeat on later versions. Each row is one sample and one label and holds the fact
items that support the presence state of the label in the sample. Presence policies of
different strictness turn the index into **sample-label presence tables**
(`sample_label_presence_<version>`, `.pkl` and `.xlsx`): positive, negative or unknown.
Stricter policies give fewer pairs with strong support; looser ones give more; some
policies must raise the number of positives, which are rare. Neither table lists every
sample-label pair: labeling projects cover different samples, and a pair not in the table is
unknown.

The user's steps: (1) define the fact-driven model, (2) redefine the fact styles, (3) build
the index, (4) build the presence tables. The user asked to be consulted on the fact styles
and on new terms, and for a DIS and DEC for the milestone, then docs and tasks to carry out
one by one. The QA report and the interpretation rules of 261023 are hints for the fact
styles and the starting point of the policies.

## Options considered

### Fact styles (fact kinds) and target levels

- **A: the user's four levels as given** (Table 0 of [DEC-059](../decisions/DEC-059-fact-driven-model-sample-label-index-presence-policies.md)). Pros: short. Cons: has no
  place for P14's per-group "checked" and "absent" marks or for closures that close a tag
  group (R05, R07-R10, R16); a task-scope skip (A10) and a sample-scope skip (A3) would both
  have to be "quality"; "confirmed" can mean two different things.
- **B (recommended): the four levels plus a labeling group level for closures, a task skip
  kind, and "confirmed" split into closure (stored) and conformance (computed by a policy)**
  (DEC-059 Table 1). Pros: every QA measure the user kept (A1-A5, A8-A10, B3, B4) has one
  home; the index stays a store of observations, the judgment stays in policies. Cons: one
  more level and two more kinds to learn.
- **C: B, and conformance also stored as fact items in the index.** Wins if several policies
  need the same cross-label checks (A8 exclusive options, A9 implied tag) and repeating them
  in each policy is slow or error-prone. Cost to reverse from B: low (index v2).

### Layout of an index row

- **A (recommended): one row per sample and content label, with a `facts` list column**
  (the fact items) plus one count column per fact kind and value. Pros: the user's row unit;
  a policy reads one row as one case, so it stays short and readable; nothing lost. Cons: a
  list column is awkward in pandas and shows as text in the `.xlsx`.
- **B: a long fact-item table (one row per fact item) plus a thin index of counts.** Wins if
  policies are written as vectorised pandas code and speed matters. Cons: two tables; the
  row unit is no longer the sample-label pair.
- **C: counts only.** Smallest. Cons: loses which labeling project said what, so a policy
  cannot trust one project over another (for example P36's polygons over P35's choices, or
  ignore P21's quality skips, QA report section 6).

Size (estimate, not counted): 261023 has 5,559,898 labelings over 201,273 labeling tasks,
143,152 of them with a crop row. The index will probably hold 1-3 million rows; one Excel
sheet holds at most 1,048,576 rows (pandas `ExcelFormatter.max_rows`, checked 2026-11-12), so
the `.xlsx` may need several sheets.

### Names

- "fact style" against **fact kind** (recommended): "style" already means the dataset style
  (plain, enc1, submit1) and the datastyle part of a table name ([DEC-053](../decisions/DEC-053-table-naming-and-preservation.md)); "kind" matches the
  existing "task kind".
- "conversion logic" against **presence policy** (recommended): "logic" is the first part of
  a table name (DEC-053), and "reading" is the effect of one interpretation rule.
- "confirmed" against **closure** and **conformance**: see the fact kinds above.

## Plan (tasks, created once the user accepts)

Table 1. Planned work of milestone refine-data1023, in order. Scope as in
[workflow.md](../../docs/workflow.md); tables as in [DEC-052](../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md) (all under `261023_plain`).

| Step | Work | Scope | After | Tables |
|---|---|---|---|---|
| 1 | Doc `docs/fact-driven-model.md`, context-map row, glossary terms | consult (this session) | | none |
| 2 | Fact relations config of 261023 (`configs/data/fact_relations_261023.yaml`) from R01-R63 and the label projects | data | 1 | none |
| 3 | Fact items and index builder, `sonoai-data sample-label-index`, synthetic tests | method | 1 | none |
| 3 | Build the 261023 index v1 and its dataset record | data | 2, 3 | read `images/taskcrops_df.pkl`, `labels/flags_df.pkl`; write `derived/sample_label_index_v1_df.pkl`, `.xlsx` |
| 3 | Respect statistics of R01-R64 from the index; the user sets thresholds after seeing them | data | index built | read the index, `labels/flags_df.pkl`, `labels/polygons_df.pkl`, `images/taskcrops_df.pkl`; write none |
| 4 | Decide the first presence policies (Parked, needs-decision) | user | index, respect statistics | |
| 4 | Presence policy registry, the chosen policies, `sonoai-data sample-label-presence`, synthetic tests | method | builder, policy decision | none |
| 4 | Build the 261023 presence tables and a dataset record comparing counts per label and state across policies | data | policies | read the index; write `derived/sample_label_presence_<policy>_df.pkl`, `.xlsx` |
| - | Decide whether P4, P9, P11 (linked to P2 by task order) enter a later index (Parked, needs-decision) | user | | |

## Conclusion

Pending the user's answers to the three open questions below. The milestone `m-3` was added
in the `consult-refine-data1023` branch (not merged yet).

## Open questions

1. **Fact kinds**: accept DEC-059 Table 1 (option B above)? Default: yes.
2. **Terms**: accept DEC-059 Table 2, with "fact kind" and "presence policy"? Default: yes.
3. **Index layout and scope**: one row per sample and content label with a `facts` list,
   labeling tasks with a crop row only, file `sample_label_index_v1_df.pkl`? Default: yes.
