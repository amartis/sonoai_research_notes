---
id: DEC-059
title: Fact-driven model of labels - fact items by target level and fact kind, the sample-label index, and presence tables from named presence policies
status: proposed
area: [labeling, datasets]
created: 2026-11-12
from: [DIS-027]
related: [DEC-036, DEC-044, DEC-045, DEC-052, DEC-053, DEC-057, DEC-058]
superseded_by:
---
# DEC-059: Fact-driven model of labels - fact items by target level and fact kind, the sample-label index, and presence tables from named presence policies

## Context

[DIS-027](../discussions/DIS-027-fact-driven-model-and-sample-label-index.md) (milestone
refine-data1023, [DEC-058](DEC-058-milestone-refine-data1023.md)). The user proposed a
**fact-driven model**: labeling facts, linked to each other through sample-free facts,
together support one presence state (positive, negative, unknown) per sample and label.
The user's first list of target levels and fact styles:

| Target level | Fact styles (user, first list) |
|---|---|
| Sample | quality |
| Sample, Label | presence (the result) |
| Labeling task | visited |
| Sample, Labeling | value, confirmed |

Table 0. The user's first list, 2026-11-12.

Inputs: the QA measures A1-A10, B1-B4 and categories C1-C6 of
[labeling_qa_measures.md](../datasets/261023/labeling_qa_measures.md), and the interpretation
rules R01-R64 of [interpretation_rules.md](../datasets/261023/interpretation_rules.md).
Names follow [docs/glossary.md](../../docs/glossary.md)
([DEC-057](DEC-057-glossary-for-the-whole-research-project.md)): labeling project, tag group,
tag, label, sample, labeling task, labeling group, labeling, given labeling.

## Decision

### 1. The model

- A **labeling fact** is a statement the labeling tables make about one target. One
  instance is a **fact item**: its **fact kind**, its target, its value, and its source
  (labeling project, labeling task, tag).
- Fact items bear on each other and on sample-label pairs through **fact relations**. Fact
  relations come from **sample-free facts**: facts that hold for every sample. These are the
  schema of the glossary's Figure 1 (a labeling task is done on one sample, a tag means one
  label, ...), the tag-to-label map, and which QA tag closes which content tags. Sample-free
  facts live in configs, not in a data table.
- A **presence policy** combines the fact items of one sample and one content label into a
  **presence state**: positive, negative or unknown.
- **Content tag** (and content label): a tag that says something is in the sample: organ,
  disease, sign, image area. **QA tag**: a tag of a QA measure (absent answer, checked mark,
  skip reason, cannot decide, AI verdict, text note). Index rows are content labels; the
  given labelings of QA tags become fact items of other kinds.
- Split of the earlier work: the **subject-to-target links** of the interpretation rules
  (which QA tag closes which tags) are sample-free facts used to build the index. Their
  **readings** (negative, missing, left out, compared) and how strict to be go into the
  presence policies.

### 2. Target levels and fact kinds

Table 1. Fact kinds of the fact-driven model: target level, what one fact item says, its
values, and the QA measure (category) and interpretation rules it comes from.

| Target level | Fact kind | One fact item says | Values | From (QA measure, category; rules) |
|---|---|---|---|---|
| Sample | quality | a labeling task on the sample calls the image unusable | the skip tag | A3 (C1); R19 |
| Labeling task (labeling group in P7, P14) | visited | the labeling task (group) was worked on: it has a given labeling | visited, not visited | C3 derived; R38-R40, R42 |
| Labeling task | task skip | the project's own question cannot be asked on this sample | the skip tag | A10 (C6); R18 |
| Labeling group | closure | the labeler closed a set of content tags of the task | checked, absent, undecided | A2 (C3); A1 (C4); A4 (C2); R01-R17, R20, R21 |
| Labeling | value | a content tag was given or not | given (with `cnt`), not given | `flags_df` `cnt` |
| Sample + label | presence | the result of one presence policy | positive, negative, unknown | (output) |

Changes against the user's first list (Table 0):

1. **Labeling group** is added as a level, for closures: P14's marks are per tag group
   (R16), and R05, R07-R10 close a tag group or part of one. "Labeling group" here also
   covers the part of a tag group that a closure names (R06, R10).
2. **Task skip** is added at the labeling task level (A10, category C6 of the QA report).
3. "Sample, Labeling" is written **Labeling**: a labeling's labeling task already fixes
   its sample.
4. **"Confirmed" is split in two.** *Closure* (stored): a not-given value is meant (the
   group was checked, or answered "absent"). *Conformance* (not stored): two entries of one
   fact agree or conflict (C4: A5, A8, A9, B3, B4). A presence policy computes conformance:
   from the items of one row when the entries share a label (A5 same task, B3 second pass,
   B4 repeat), or by looking up another row of the same sample (A8 exclusive options, A9
   implied tag).

Not used as fact kinds: A6 AI verdict and A7 text note (ignored, QA report Amendment 1);
`hepatic_steatosis__unknown` (not used); B1 one finding per project and B2 staged routing
(project design; R48, `skip_no_organ_found` against the routing source, is a conformance
check).

### 3. Sample-label index

- File `<dataset>/derived/sample_label_index_v1_df.pkl`, with an `.xlsx` copy
  ([DEC-053](DEC-053-table-naming-and-preservation.md) naming and preservation).
- **One row per sample and content label** that has a fact item from a visited labeling
  task (with a crop row) offering a tag of that label. Not the cross product of samples and
  labels. **A pair not in the index is unknown.**
- **Sample**: image hash + crop box ([DEC-044](DEC-044-cirrhosis-sample-set-quality-filter-and-split.md)
  rule 1, `CROP_KEY`), with its sample number
  ([DEC-045](DEC-045-per-sample-confusion-matrices-in-runs.md)).
- **Columns**: sample number and `CROP_KEY`; `label`; `facts`, the list of the row's fact
  items (fact kind, value, labeling project, labeling task, tag); one count column per fact
  kind and value; `projects`, the labeling projects with an item on the row.
- **Which fact items go on a row**: value items of the tags of that label; visited and task
  skip items of the labeling tasks that offer such a tag; closure items whose closed tags
  include such a tag; quality items of the sample (on every row of the sample).
- **Scope of v1**: labeling tasks with a crop row only (143,152 of 201,273 in 261023). P4,
  P9 and P11 (linked to P2 only by task order), P49 and P52 (no crop rows) and P1, P30 (not
  placed) are left out; a Parked task decides whether P4, P9, P11 enter a later version.
- **`.xlsx`**: a summary sheet (rows per label and fact kind) and the rows; rows beyond
  1,048,576 per sheet (Excel's limit, as enforced by pandas) go on further sheets.

### 4. Presence policies and presence tables

- A presence policy is a named, versioned Python function in `src/sonoai/`, registered by
  name (as models are), short enough to read as the rule text. The readings of the
  interpretation rules are its starting point.
- File `<dataset>/derived/sample_label_presence_<policy>_df.pkl` with an `.xlsx` copy, e.g.
  `sample_label_presence_strictv1_df.pkl` for policy `strict_v1` (a version tag has no `_`,
  DEC-053).
- One row per sample and content label with state **positive or negative**; unknown pairs
  are left out (as in the index, a missing pair is unknown), and their count per reason goes
  on the summary sheet. A positive row lists the labeling tasks it rests on, so that a
  trainer can tell a polygon positive from a choice-only positive.
- Policies differ in strictness: a strict policy keeps fewer pairs with stronger support; a
  loose one keeps more; a positive-rich one accepts weaker support for positives, which are
  rare. The first policies are chosen by the user after the index counts and the rule
  respect statistics are in ([DEC-058](DEC-058-milestone-refine-data1023.md)).

### 5. Terms

Table 2. New terms of the fact-driven model, each with its meaning and the other names
considered. They go into [docs/glossary.md](../../docs/glossary.md) once
`docs/fact-driven-model.md` defines them (DEC-057).

| Term | Meaning | Other names considered |
|---|---|---|
| Fact-driven model | Reading labels as fact items, linked by sample-free facts, combined by a presence policy into a presence state | labeling interpretation model |
| Labeling fact | A statement the labeling tables make about one target | |
| Fact item | One labeling fact: fact kind, target, value, source | fact instance |
| Fact kind | The class of a fact item: its target level, values and source | fact style (user's first word; "style" already means dataset style and the datastyle part of a table name) |
| Target level | What a fact item is about: sample, labeling task, labeling group, labeling, sample + label | |
| Sample-free fact | A fact that holds for every sample: schema, tag to label, which QA tag closes which tags | schema fact |
| Fact relation | How a fact item bears on another item or on a sample-label pair, given by a sample-free fact | labeling fact relationship (user) |
| Content tag, content label | A tag (label) that says something is in the sample: organ, disease, sign, image area | finding tag ("finding" reads as disease only) |
| QA tag | A tag of a QA measure: absent answer, checked mark, skip reason, cannot decide, AI verdict, text note | control tag (Label Studio's word for its UI elements) |
| Closure | A fact item saying the labeler closed a set of content tags: checked, absent, undecided | confirmed |
| Conformance | Whether two entries of one fact agree (C4 measures); computed by a policy | confirmed |
| Presence state | positive, negative or unknown, for one sample and one content label | presence fact |
| Presence policy | A named, versioned function from the index to presence states; sets the strictness | conversion logic, presence logic ("logic" is the first part of a table name, DEC-053), reading (one rule's effect in interpretation_rules.md) |
| Sample-label index | The table of section 3 | |
| Sample-label presence table | The table of section 4, one per presence policy | presence datasheet |

## Consequences

- New doc `docs/fact-driven-model.md` (model, Table 1, the config schema, the two tables,
  how to write a policy), a row in the context map (`docs/README.md`, labeling area) and the
  Table 2 terms in `docs/glossary.md`.
- New config `configs/data/fact_relations_261023.yaml` (label vocabulary only, no patient
  data): tag to content label, QA tag to fact kind and closed tags, visit unit per project,
  and for policies the exclusive sets (A8), implied tags (A9) and second-pass pairs (B3).
  `choice_labels.yaml` stays as the map of the choice check
  ([DEC-036](DEC-036-choice-polygon-relation-table.md)); where they differ, the new config
  counts for the index (as the interpretation rules decided for R10).
- Board tasks of the plan in DIS-027, milestone m-3.
- Each later dataset version needs its own fact relations config; the code stays.
