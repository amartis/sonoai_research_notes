# Crops that lose their organ target under DEC-034 (261023_plain)

[TASK-058](../../../backlog/tasks/task-058%20-%20Count-crops-whose-diffuse-disease-polygon-has-no-organ-polygon-DEC-034.md), [DEC-034](../../decisions/DEC-034-organ-layer-from-organ-polygons-only.md), [DIS-011](../../discussions/DIS-011-diffuse-disease-polygon-extent.md). Exploratory. Aggregates only; no
images, file names or identifiers; counts below 5 are shown as "<5", and no
pair of numbers here differs by a masked count. Computed on 2026-11-03 on
`261023_plain` ([DEC-018](../../decisions/DEC-018-plain-style-for-local-research.md)), in memory, with the task code of the code repo's
`master` at commit 60db495 (v3 liver tasks, [TASK-055](../../../backlog/tasks/task-055%20-%20Layered-disease-tasks-treat-diffuse-disease-polygons-as-the-whole-organ-outline-but-they-may-cover-only-part-of-it.md)). Nothing was written to the
dataset.

Reporting checklists (CLAIM, STARD): not applicable. This is a count of training
targets: no model is trained or evaluated, no split is made.

## Terms

- **v2, v3**: the task versions `lseg_<disease>_v2` (class map of DEC-006:
  diffuse polygons also count as the liver) and `lseg_<disease>_v3` (class map of
  DEC-034: only liver polygons count as the liver).
- **Organ layer**: the segmentation channel for the whole liver (background or
  liver).
- **Disease layer**: the segmentation channel for the disease classes of the task.
- **`ignore_index`**: the label value that the loss skips; pixels with it are
  neither trained nor scored.
- **Crop**: one row of `taskcrops_df` (one labelled task image). Polygon tasks
  without a crop row (83 for steatosis, 173 for cirrhosis, 183 for hepatoma) are left out.
- **Eligible crop**: a crop the task samples. Eligibility is the same in v2 and v3
  (DEC-034, rule 4): the crop shows the liver (a polygon of the liver, its
  structures, diseases or signs) and comes from a labeling project that annotates
  the task's disease; for steatosis it must also carry a grade polygon.
- **Liver polygon**: a polygon with the label `liver`. In v3 only these draw the
  organ layer.
- **Diffuse polygon**: a polygon of steatosis (any grade, `__ignore`, `__unknown`),
  cirrhosis, precirrhosis or hepatitis. In v2 these also drew the organ layer
  ([DEC-006](../../decisions/DEC-006-losses-optim-tracking.md)).
- **Loses its organ target**: an eligible crop with a diffuse polygon and no liver
  polygon. In v2 its organ layer was drawn from the diffuse polygon; in v3 it is
  ignored (`ignore_index`) in the whole crop.

## Results

Table 1. Eligible crops of the liver layered-segmentation tasks in 261023_plain,
by whether the crop keeps an organ-layer target in v3. Shares are % of the task's
eligible crops. CIs: Wilson score interval (treats crops as independent) and
datasource cluster bootstrap (4,000 resamples of datasources, percentile).

| Task | Eligible crops, n (datasources) | Crops with a liver polygon (keep the organ target), n (%) | Crops with a diffuse polygon but no liver polygon (lose the organ target in v3), n (%) | Lost share, 95% CI Wilson | Lost share, 95% CI datasource bootstrap | Crops with neither (organ layer ignored already in v2), n |
|---|---|---|---|---|---|---|
| `lseg_steatosis` | 14,071 (57) | 9,298 (66.1) | 4,773 (33.9) | 33.1-34.7 | 13.8-61.3 | 0 (every eligible crop has a grade polygon) |
| `lseg_cirrhosis` | 16,340 (57) | 9,983 (61.1) | 6,303 (38.6) | 37.8-39.3 | 18.4-63.6 | 54 |
| `lseg_hepatoma` | 16,545 (57) | 9,983 (60.3) | 6,508 (39.3) | 38.6-40.1 | 18.9-64.3 | 54 |

Hepatitis has no layered task. A hepatitis task with the same eligibility rule
would have exactly the counts of the hepatoma row (its labeling projects give the
same counts); 176 of its lost crops carry a hepatitis polygon.

Table 2. The crops that lose the organ target, by what else they carry. The
shares are descriptive and have no CIs.

| Task | Lost crops, n | Lost crops with a polygon of the task's own disease, n | Share of lost crops in the datasource with most of them, % | Share of lost crops in the 3 datasources with most of them, % |
|---|---|---|---|---|
| `lseg_steatosis` | 4,773 | 4,773 (a grade polygon) | 31.3 | 54.6 |
| `lseg_cirrhosis` | 6,303 | 1,428 (cirrhosis) | 24.3 | 45.7 |
| `lseg_hepatoma` | 6,508 | 1,293 (hepatoma) | 23.5 | 44.7 |

The lost crops are a whole-datasource effect, not scattered crops:

- 42 of the 57 eligible datasources have at least one crop with a liver polygon.
  The other 15 datasources have no liver polygon at all.
- All but <5 of the lost crops (in every task) lie in those 15 datasources. Under
  v3 the organ layer is never trained on these 15 datasources.
- The lost crops carry steatosis polygons (4,773 in every task), cirrhosis
  polygons (1,428 for cirrhosis and hepatoma, 53 for steatosis), hepatitis polygons
  (176; 21 for steatosis) and, for hepatoma only, precirrhosis polygons (205); a
  crop may carry several.

Steatosis only (DEC-034, rule 3): in its 4,773 lost crops (33.9%) every pixel
outside the grade polygons is now ignored in the disease layer, where v2 made the
area outside the diffuse polygon background. That layer is the assessed one
([DEC-034](../../decisions/DEC-034-organ-layer-from-organ-polygons-only.md), Consequences: only the disease layer is assessed), so
in a third of the steatosis crops the disease layer has no background pixels in
training or evaluation.

## Limitations

- Crops of one datasource are not independent (same device, site and labelers);
  the Wilson intervals are too narrow for that reason. The datasource bootstrap
  intervals are wide because the effect sits in whole datasources.
- Counts are of crops, not patients; the dataset has no patient key.
- Whether the diffuse polygons in the 15 datasources cover the whole liver is not
  known: DIS-011 measured coverage only in crops that have both polygons.

## Recommendation

Keep DEC-034 as it is: the organ layer is not scored, 9,298-9,983 crops from 42
datasources still train it, and the fallback would rest entirely on diffuse
polygons whose extent is unmeasured in the 15 datasources that would use it.
Revisit (new DEC) if v3 runs do poorly on those datasources; the best alternative
is a positive-only fallback (diffuse area counts as organ where no liver polygon
exists, everything else ignored, so no "not organ" is taught on unlabelled liver).
