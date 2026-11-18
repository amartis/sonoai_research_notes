---
id: DIS-036
title: Term harvest pass - keep, rename or descriptive words for the terms of the open glossary tasks and Epic 1
status: concluded
created: 2026-11-18
outcomes: [DEC-074]
related: [DIS-035, DEC-072, DEC-073, DEC-057, DEC-063, DEC-002]
---
# DIS-036: Term harvest pass

## Question

[DEC-073](../decisions/DEC-073-how-new-terms-are-coined.md) point 6: apply the coining rules to
the existing terms of the open glossary tasks and the Epic 1 words, and sort each into the
global glossary or the Epic 1 terms file ([DEC-072](../decisions/DEC-072-term-scopes-global-glossary-and-epic-terms-files.md)).
Taken in `/consult` on [TASK-177](../../backlog/tasks/task-177%20-%20Harvest-pass-on-existing-terms-with-the-DEC-073-rules-keep-rename-or-replace-with-descriptive-words-sort-into-the-global-glossary-or-the-Epic-1-terms-file-DEC-072-DEC-073.md)
(term harvest).

## Options considered

- **The harvest table.** 47 rows from 8 open glossary tasks and the Epic 1 records
  ([DEC-065](../decisions/DEC-065-mission-upper-abdomen-anatomy-segmentation.md) to [DEC-070](../decisions/DEC-070-anatomy-label-set-task-states-in-sample-file.md)): 19 keep, 11 rename, 16 descriptive words with no row, 1 group left as
  it is. Label facts, the B-mode box detector and the split method go to the global glossary
  (no research epic, or general code); Epic 1 words go to the Epic 1 terms file. The user
  approved it as drafted, with two choices:
  - **First set**: "anatomy organ classes" (recommended), "own-class organs" or "Epic 1 organ
    classes". The user chose **Epic 1 organ classes**.
  - **Public dataset** collides with the glossary term Dataset (DEC-073 point 3). Options:
    keep it with a note (recommended first), or rename it **public image collection** (chosen
    by the user).
- **Dataset itself.** The user asked whether the glossary term Dataset should become "project
  dataset", since it narrows the common ML word (about 63 general-sense uses out of 494 uses
  in 114 docs and records, master, 2026-11-18).
  - **A, keep Dataset**: no cost; the general-sense uses stay ambiguous.
  - **B, rename the row, plain word still allowed where clear** (recommended, chosen): a few
    glossary rows; compounds (dataset version, dataset record) and code names unchanged.
  - **C, rename and always write "project dataset"**: high, ongoing cost against the old uses
    and the code names; would win if outside datasets come up side by side often (scraping,
    milestone m-4).

## Conclusion

- The approved table is in TASK-177, now To Do after [TASK-175](../../backlog/tasks/task-175%20-%20Glossary-folder-move-docs-glossary.md-to-docs-glossary-global-glossary.md-add-docs-glossary-README.md-term-scopes-and-coining-rules-and-the-Epic-1-terms-file-DEC-072-DEC-073.md) (glossary folder) and [TASK-176](../../backlog/tasks/task-176%20-%20Reviewer-terms-check-and-lead-consult-for-term-scopes-and-coining-rules-global-or-epic-terms-file-collision-promotion-the-DEC-073-screen-DEC-072-DEC-073.md)
  (reviewer terms check). The glossary tasks it replaces are archived; [TASK-128](../../backlog/tasks/task-128%20-%20Link-the-sample-label-index-record-glossary-rows-for-visited-and-ignored-tag-P3-in-the-v1-out-of-scope-list-DEC-059.md) keeps its two
  non-glossary parts.
- [DEC-074](../decisions/DEC-074-project-dataset-and-public-image-collection.md) (accepted, the
  user chose B): Project dataset and public image collection.

## Open questions

- None.
