---
id: DIS-001
title: Deferred disease-task questions (precirrhosis, kidney tasks, image-level area)
status: parked        # open | concluded | parked
created: 2026-10-23
outcomes: []          # DEC-NNN / TSK-NNN this discussion produced
related: [DEC-004, DEC-006]
---
# DIS-001: Deferred disease-task questions (precirrhosis, kidney tasks, image-level area)

## Question

While reviewing DEC-006 (2026-10-23) three questions were set aside so the
next run would contain only tasks judged sound: `lseg_steatosis_v2`,
`lseg_cirrhosis_v2` (without precirrhosis) and `lseg_hepatoma_v2`. This
record holds them until they are taken up.

1. **Precirrhosis.** `lseg_cirrhosis_v2` drops it: samples with a
   precirrhosis polygon are not eligible (205 in 261023). Bring it back? If
   so, is precirrhosis -> cirrhosis an adjacent miss (satisfaction 0.5), as
   with neighbouring steatosis grades?
2. **Kidney tasks** (`renal_calculus`, `hydronephrosis`). Parked with no
   `_v2`. Kidney outlines are almost absent in their crops (3 of 1,963 stone
   crops), so the organ layer would barely train, and same-project negatives
   are few (468 and 524). What gives organ evidence and enough negatives?
3. **Image-level prediction area.** DEC-006 first looked for the predicted
   image class only inside the liver outline. It was amended to the whole
   crop for both ground truth and prediction, because ~0.5% of hepatoma
   polygons extend past the liver outline and a perfect prediction scored
   0.995. Is the whole crop the right rule, or should both sides be
   restricted to the organ (and the overhanging polygons handled)?

## Options considered

1. Precirrhosis
   - **Keep it out** (current): clean cirrhosis-vs-normal task.
   - **Separate class, adjacent miss**: needs a graded satisfaction like
     steatosis (`ordinal`).
   - **Merge into cirrhosis**: simplest, but loses the distinction.
2. Kidney tasks
   - **Flags as organ evidence**: every renal-calculus crop has flags
     containing "renal" and "calcul" (`flags_df`, 181 values); they may act
     as image-level organ / diagnosis labels where no kidney polygon exists.
     Flag names and meaning not yet reviewed (also an open question in
     DEC-006).
   - **Negatives from all projects**: more negatives, but possibly never
     looked at for that disease.
   - **Annotate kidney outlines** on the affected crops.
3. Image-level area
   - **Whole crop** (current, implemented).
   - **Organ outline for both sides**, clipping ground truth to the outline
     as well, so a perfect prediction still scores 1.

## Conclusion

Parked on 2026-10-23. The next run covers the three liver tasks only.
Reopen when the next run's results are in, or before the task set is
extended beyond those three tasks. Each answer should become a DEC that
amends or supersedes the relevant part of DEC-006.

## Open questions

- Review the `flags_df` values (names and meaning, aggregates only) before
  deciding question 2.
