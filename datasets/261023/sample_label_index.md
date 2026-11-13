# Sample-label index v1 of 261023 (261023_plain)

[TASK-120](../../../backlog/tasks/task-120%20-%20Build-the-261023-sample-label-index-v1-and-its-dataset-record-DEC-059.md), [DEC-059](../../decisions/DEC-059-fact-driven-model-sample-label-index-presence-policies.md), [fact-driven model](../../../docs/fact-driven-model.md) (sections 3 and 4). Descriptive counts; aggregates only, no
images, file names or identifiers.

Built on 2026-11-13 on `261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)) with
`sonoai-data sample-label-index 261023_plain --relations configs/data/fact_relations_261023.yaml --version v1`
from the code repo at commit 4b670b8 (code: TASK-119, last change to the module 37178a2; config: TASK-118,
sha256 prefix 03fa1dd97269a29c). Inputs: `images/taskcrops_df.pkl` and `labels/flags_df.pkl`. Written, inside
the dataset only: `derived/sample_label_index_v1_df.pkl` (sha256
`b08b9e011689073872de4ee6e16b18d61802761a18a99c85dd72764bb79acf49`) and its `.xlsx` copy (2 row sheets).

Reporting checklists (CLAIM, STARD): not applicable. This is a count of labels: no model is trained or
evaluated, no split is made, no threshold is chosen. No CIs: every number is a count of the full table, not
an estimate from a sample.

## Terms

- **Labeling task**: one task of a labeling project (`task_id`); 201,273 in `flags_df`, 143,152 of them with
  a crop row in `taskcrops_df`.
- **Visited**: the labeling task has at least one labeling with a count above 0 (any tag, also an ignored one).
- **Sample**: image hash + crop box (DEC-044 rule 1). **Content label**: the label of a content tag (config
  `labels` merges synonyms). **Fact item**: one fact about a labeling task (kinds in the
  [model doc](../../../docs/fact-driven-model.md)); the index puts it on the rows of the labels it concerns.
- A (sample, label) pair not in the index is unknown (not "absent").

## Headline

| Quantity | n |
|---|---|
| Index rows (sample, content label) | 1,227,979 |
| Samples in the index | 29,233 of 31,104 in `taskcrops_df` (1,871 samples have no visited task with a crop row) |
| Content labels | 100 |
| Rows per label (min, median, max) | 56, 14,573, 25,395 |
| Labeling tasks with a crop row, visited (give fact items) | 118,935 |
| Labelings in `flags_df` (task, tag group, tag; counts summed) | 5,456,390 (from 5,559,898 rows) |
| Labelings of a tag not in its project's schema | 0 |

## Fact items per fact kind and value

Items are counted once per labeling-task fact, before the index copies an item onto the rows of each
label it concerns.

Table 1. Fact items by kind and value (n = 1,742,924 items; all 118,935 visited labeling tasks with a crop row).

| Kind | Value | Items |
|---|---|---|
| value | given (count above 0) | 119,890 |
| value | not_given (count 0) | 1,305,577 |
| visited | visited | 150,795 |
| visited | not_visited (tag-group visit unit: P7, P14) | 41,528 |
| closure | absent | 70,863 |
| closure | checked | 44,321 |
| closure | undecided | 1,312 |
| quality | (8 distinct QA tags) | 6,317 |
| task_skip | (7 distinct QA tags) | 2,321 |

Value items sum to 1,425,467; their `flags_df` count sums to 140,790 (8.4% of value items are given).

## Rows and items per labeling project

Table 2. Per labeling project (P): items, labeling tasks with items, index rows and samples with an item
of that project. A row has items of several projects, so rows do not add up to 1,227,979. Items by kind:
quality / visited / task_skip / closure / value.

| P | Items | Tasks | Rows | Samples | q / vis / skip / clo / val |
|---|---|---|---|---|---|
| 2 | 67,970 | 5,913 | 76,849 | 5,861 | 2,927 / 5,913 / 0 / 0 / 59,130 |
| 7 | 144,469 | 5,914 | 78,403 | 5,861 | 1,377 / 17,742 / 1,161 / 5,909 / 118,280 |
| 14 | 871,957 | 15,390 | 739,641 | 15,390 | 517 / 76,950 / 500 / 24,490 / 769,500 |
| 15 | 6,823 | 2,301 | 5,129 | 2,300 | 105 / 2,301 / 0 / 2,116 / 2,301 |
| 19 | 2,524 | 845 | 844 | 844 | 0 / 845 / 0 / 834 / 845 |
| 20 | 29,471 | 10,442 | 10,387 | 10,334 | 1 / 10,442 / 0 / 8,586 / 10,442 |
| 21 | 29,921 | 10,442 | 49,431 | 10,334 | 819 / 10,442 / 0 / 8,218 / 10,442 |
| 22 | 30,069 | 10,440 | 10,753 | 10,332 | 10 / 10,440 / 0 / 9,179 / 10,440 |
| 23 | 30,977 | 10,441 | 10,359 | 10,333 | 1 / 10,441 / 0 / 10,094 / 10,441 |
| 24 | 31,175 | 10,438 | 10,514 | 10,331 | 4 / 10,438 / 0 / 10,295 / 10,438 |
| 26 | 1,989 | 711 | 1,072 | 711 | 7 / 711 / 0 / 560 / 711 |
| 27 | 4,063 | 1,571 | 5,523 | 1,570 | 102 / 1,571 / 0 / 819 / 1,571 |
| 28 | 4,584 | 1,566 | 2,170 | 1,565 | 16 / 1,566 / 0 / 1,436 / 1,566 |
| 29 | 9,185 | 2,958 | 5,916 | 2,958 | 28 / 2,958 / 0 / 283 / 5,916 |
| 31 | 313 | 77 | 231 | 77 | 0 / 77 / 0 / 5 / 231 |
| 32 | 2,394 | 803 | 803 | 803 | 0 / 803 / 0 / 788 / 803 |
| 33 | 80,841 | 4,239 | 90,589 | 4,239 | 300 / 4,239 / 0 / 0 / 76,302 |
| 35 | 275,558 | 4,239 | 267,130 | 4,239 | 21 / 4,239 / 2 / 0 / 271,296 |
| 36 | 36,186 | 2,411 | 33,668 | 2,411 | 41 / 2,411 / 149 / 2,242 / 31,343 |
| 37 | 6,159 | 879 | 4,911 | 879 | 8 / 879 / 85 / 792 / 4,395 |
| 38 | 10,072 | 1,038 | 8,554 | 1,038 | 4 / 1,038 / 82 / 644 / 8,304 |
| 39 | 2,595 | 519 | 1,622 | 519 | 1 / 519 / 56 / 462 / 1,557 |
| 41 | 44 | 11 | 22 | 11 | 0 / 11 / 1 / 10 / 22 |
| 42 | 742 | 106 | 530 | 106 | 0 / 106 / 2 / 104 / 530 |
| 43 | 280 | 56 | 232 | 56 | 1 / 56 / 11 / 44 / 168 |
| 44 | 1,563 | 521 | 592 | 521 | 1 / 521 / 147 / 373 / 521 |
| 45 | 96 | 19 | 57 | 19 | 0 / 19 / 2 / 18 / 57 |
| 46 | 4,902 | 545 | 3,815 | 545 | 0 / 545 / 50 / 492 / 3,815 |
| 47 | 562 | 180 | 180 | 180 | 0 / 180 / 25 / 177 / 180 |
| 50 | 55,440 | 13,920 | 15,123 | 13,920 | 26 / 13,920 / 48 / 27,526 / 13,920 |

Tasks and items in Table 2 sum to the totals above (118,935 visited tasks with a crop row; the per-project
task counts add up to it).

## Labeling tasks left out

Table 3. All 201,273 labeling tasks by reason for being in or out of the index (each task in one row).

| Reason | Tasks |
|---|---|
| In the index (crop row, visited) | 118,935 |
| Left out: no crop row | 58,121 (32,082 visited, 26,039 not visited) |
| Left out: crop row, not visited | 24,217 |

- **No crop row**, per project (tasks, of which visited): P1 5,913 (5,913); P4 5,913 (5,913); P9 5,913
  (5,913); P11 5,913 (1,517); P30 3,949 (607); P49 13,659 (10,948); P52 10,948 (1,271); P3 5,913 (0). P1,
  P4, P9, P11, P30, P49 and P52 are the projects the model doc names as out of v1 scope (52,208 tasks); every
  one of them has no crop row. **P3 is not named there**: it also has no crop row (5,913 tasks, none visited).
  The projects out of v1 scope have crop rows for none of their tasks, so no task is left out for the scope
  alone beyond the no-crop count.
- **Crop row, not visited** (no labeling above 0), per project: P7 17,738; P15 4,557; P14 1,872; P22 8;
  P23 7; P20 6; P21 6; P28 5; P50 4; P24 10; P19, P26, P37, P38 1 each. No labeling task with a crop row
  lacks rows in `flags_df`. P7 and P14 count visits by tag group (visit unit), so a visited task of those
  projects can still carry `not_visited` items (Table 1).

## Checks

1. **Every visited labeling task with a crop row gives at least one item.** Passed: 118,935 of 118,935 tasks
   have at least one fact item; 0 without. Checked twice: on the items rebuilt in memory with
   `fact_items` and on the facts of the written index (118,935 distinct tasks appear in it). No item belongs to
   a task that is not visited with a crop row (0).
2. **Value items equal the content-tag labelings of those tasks in `flags_df`.** Passed: 1,425,467 value
   items against 1,425,467 content-tag labelings (task, tag group, tag) of the same tasks, computed from the
   raw `flags_df` rows (1,512,408 rows, summed per labeling): 0 labelings only in `flags_df`, 0 only in the
   items, 0 counts that differ; count sums 140,790 on both sides; given labelings 119,890 on both sides.
   The other labelings of those tasks (744,827 raw rows, 145,130 with a count above 0) are QA, ignored or
   text tags and have no value item, as intended.
3. **Build counters** (printed by the command): labelings of tags not in the schema 0; content tags offered
   by a visited task without a labeling 0.

## Open points

- None from the checks. One for the user: P3 has no crop rows and is not in the doc's list of projects out
  of v1 scope (Table 3). The doc section 4 list may need P3 added; I did not change it.
- The `.xlsx` copy was written but not opened (the file is a table; sheet count only from the build message).
