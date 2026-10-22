# research_notes

Lab notebook for the sonoai ultrasound ML project. Separate git repo from the
code in `..` (which ignores this folder).

```
journal/       daily notes: journal/2026/2026-10-22.md
experiments/   one file per experiment: hypothesis, runs, results, conclusion
datasets/      dataset/label versions, cleaning decisions, statistics (aggregates only)
literature/    paper notes
decisions/     short records of choices that shape the project (ADR style)
templates/     copy these to start a note
```

## Linking to code and runs

- Code: commit hash of the `ml_research` repo (`git -C .. rev-parse --short HEAD`).
- Runs: run name; `runs/<name>/config.json` and `meta.json` hold the full config and commit.

## Privacy

No patient images, crops, screenshots of images, file/case names, or
identifiers here. Plots of metrics and aggregate statistics are fine.
The `.gitignore` blocks image and table files as a backstop.
