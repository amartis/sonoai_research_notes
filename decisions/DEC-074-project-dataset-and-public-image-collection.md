---
id: DEC-074
title: Glossary term Dataset becomes Project dataset (plain "dataset" still allowed where clear); public non-patient data is a public image collection
status: accepted
area: [workflow, datasets]
created: 2026-11-18
from: [DIS-036]
related: [DEC-002, DEC-057, DEC-063, DEC-072, DEC-073]
superseded_by:
---
# DEC-074: Project dataset and public image collection

## Context

The harvest pass of [DEC-073](DEC-073-how-new-terms-are-coined.md) point 6
([DIS-036](../discussions/DIS-036-term-harvest-pass.md)) found that "public dataset" (MedNIST,
Imagenette under `SONOAI_PUBLIC_DATA_ROOT`, [DEC-063](DEC-063-public-non-patient-datasets-root.md))
reuses the glossary term **Dataset** with another meaning: a glossary Dataset is one content
version in one style ([DEC-002](DEC-002-dataset-files-structure.md)), and a public image
collection has neither. The glossary term also narrows the common ML word "dataset": on master
on 2026-11-18 about 63 uses in docs, records and code already mean the general sense (public,
Roboflow, external datasets), out of 494 uses of the word in 114 docs and records (case-insensitive
grep, whole word).

## Decision

1. **Public image collection.** An external, non-patient image collection used as it is
   (MedNIST, Imagenette 320; DEC-063), under `SONOAI_PUBLIC_DATA_ROOT`. It has no version and no
   style and is not a datasource. Other names: public dataset (DEC-063 and older text).
2. **Project dataset.** The glossary row Dataset is renamed Project dataset: one content
   version in one style, named by its codename `<version>_<style>` (DEC-002). Other names:
   dataset.
3. **Plain "dataset" stays allowed** where it clearly means a project dataset. Write "project
   dataset" where other datasets (public image collections, scraped or external datasets) also
   come up. Compounds keep their short form: dataset version, dataset record, dataset style,
   dataset folder, codename.
4. **Code names do not change** ([DEC-073](DEC-073-how-new-terms-are-coined.md) point 5):
   `sonoai.paths.dataset_dir`, `sonoai-data`, `research_notes/datasets/`, the codename and
   `SONOAI_PUBLIC_DATA_ROOT`.

## Consequences

- Rows to change in the global glossary (Index, Table 2 related terms, Datasets section, the
  other-names table): carried by [TASK-177](../../backlog/tasks/task-177%20-%20Harvest-pass-on-existing-terms-with-the-DEC-073-rules-keep-rename-or-replace-with-descriptive-words-sort-into-the-global-glossary-or-the-Epic-1-terms-file-DEC-072-DEC-073.md)
  (term harvest), row B3.
- Older records and docs keep their words ([DEC-056](DEC-056-labeling-terminology-single-glossary.md) rule); no doc or code edits.
- Alternatives not taken (DIS-036): keep Dataset as it is (the general-sense uses stay
  ambiguous); require "project dataset" in all new text (high, ongoing cost against 494 old uses
  and the code names; would win if outside datasets come up side by side often, e.g. the
  scraping milestone m-4).
