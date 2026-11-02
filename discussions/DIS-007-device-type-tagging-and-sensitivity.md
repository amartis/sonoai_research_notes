---
id: DIS-007
title: Inferring the ultrasound device type of each image, and how sensitive models and diagnosis are to it
status: parked
created: 2026-10-29
outcomes: []
related: [DIS-001]
---
# DIS-007: Inferring the ultrasound device type of each image, and how sensitive models and diagnosis are to it

## Question

The user asked (2026-10-28) to tag training images with the inferred
ultrasound device type and, if possible, to assess how sensitive results are
to it, because diagnosis may differ with device quality.

Context from the repo on that date: `sonoai.data.datasource` already assumes
that one datasource (one origin of images; see `src/sonoai/data/datasource.py`)
usually means one device, protocol and patient group. `261023_plain` has 72
datasources. No device metadata exists in code or notes yet.

## Options considered

**What "device type" means.** Each level needs a different method:

| Level | Example | How hard to infer |
| --- | --- | --- |
| Vendor / model | cart scanner vs handheld | medium: on-screen layout gives it away |
| Probe | convex / linear / phased | easy: sector geometry, depth |
| Export path | DICOM vs screen capture vs photo of the monitor | easy: resolution, compression, borders |
| Quality tier | high-end / mid-range / handheld | hard, and a judgement call |

Table 1. Levels of "device type"; quality tier is the one that matters for
the clinical question, the others are ways to reach it.

**Where the labels come from**, cheapest and most reliable first:

1. Metadata already held: DICOM `Manufacturer` / `ManufacturerModelName` /
   transducer fields where originals exist, and collection records per site.
   A datasource-level device register (`datasource_id -> vendor, model, probe,
   tier, confidence`) may cover most datasources with no ML.
2. Hand-crafted image features: image size and aspect, fan position and shape,
   UI chrome (colour bars, depth scale), JPEG quantization tables, noise and
   speckle spectrum.
3. Clustering of pretrained-encoder embeddings, checked against the register;
   finds datasources that mix devices and gives per-image tags.
4. A supervised device classifier trained on the register, for new data.

Patient-data caution: the strongest device cues are burned-in text and
overlays, which can hold patient identifiers. Any overlay feature runs in
memory and outputs only a class or feature vector; avoid OCR unless needed.

**Measuring sensitivity.** Device is confounded with site, patient group,
disease prevalence and annotator, so a naive per-device drop may be about
population. Candidate methods:

- Per-device / per-tier metrics with 95% CIs, bootstrapped over datasources
  (fits the matrix and eval work in [TASK-014](../../backlog/tasks/task-014%20-%20Matrix-score-formulas-for-NumPy-and-torch-matrices-DEC-013.md), [TASK-017](../../backlog/tasks/task-017%20-%20Image-level-matrices-and-evaluatetask-model-loader-DEC-006.md) as a grouping key).
- Leave-one-device-out training and testing.
- Controlled degradation: make high-end images look low-end (resolution,
  speckle/noise, compression, dynamic range) and measure the drop; separates
  quality from population because the patients stay the same.
- Matched comparisons where one site used two devices, or a disease appears
  across tiers.
- Separate (a) model performance shift from (b) label shift: ground truth may
  be less reliable or differently distributed on worse devices; (b) needs
  per-tier label statistics and ideally inter-rater agreement.

**Board fit.** `data`: device register, per-image tag column or sidecar table
under the dataset's `derived/`. `method`: feature extractors, clustering or
classifier, stratified metrics, degradation transforms (synthetic tests).
`exp`: clustering on real data, tagging runs, leave-one-device-out and
degradation experiments.

## Conclusion

Parked on 2026-10-29 at the user's request, before any decision. No DEC and no
board task yet. Reopen when the user picks this up; start from the open
questions below, then draft DECs and tasks.

## Open questions

1. Do any datasources have DICOM headers or collection records naming the
   machine?
2. Which level is needed: vendor/model, probe, or quality tier? If tier, who
   defines the tiers?
3. Is the goal model robustness (a), clinical label differences (b), or both?
4. One tag per datasource, or per image (needed if datasources mix devices)?
