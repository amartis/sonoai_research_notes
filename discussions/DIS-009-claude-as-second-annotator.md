---
id: DIS-009
title: Claude as a second, blind annotator for the TASK-032 B-mode boxes
status: concluded
created: 2026-10-30
outcomes: [DEC-029]
related: [DEC-017, DEC-019, DEC-024, DEC-025, DEC-026]
---
# DIS-009: Claude as a second, blind annotator for the [TASK-032](../../backlog/tasks/task-032%20-%20Run-the-B-mode-cropper-on-a-dataset-version-polygon-check-reviewed-set-box-table-DEC-017.md) B-mode boxes

## Question

On 2026-10-30 the user asked for Claude to join TASK-032 as a second labeling user, using
the best model available. The rule they set: no annotator should be able to see the other
annotator's work. In TASK-032 a human remote assistant labels B-mode boxes on aws-labelstud
([DEC-025](../decisions/DEC-025-aws-labelstud-public-https.md)): 1,371 frames from 72
datasources, at most two boxes per frame, or "No B-mode image". The questions were:
- where Claude's labels go;
- which model looks at the frames;
- how the frames reach the model without breaking
  [DEC-024](../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md).

## Options considered

**Where the labels go**
- **Same aws-labelstud project.** Label Studio Community has no roles and no project
  membership, so every account sees every annotation. Hiding annotators from each other
  needs Enterprise. Rejected.
- **Local mirror project on machine01** (the user's proposal). It holds the same frames,
  and Claude is its only annotator. The two servers keep the annotators apart by design,
  and there is no extra AWS traffic. Chosen.

**Which model**
- **Open vision-language model on the GPU box** (for example Qwen3-VL-8B, 4-bit):
  - Pro: nothing leaves the user's machines.
  - Con: weaker judgement than Claude.
- **Claude Opus 5.5 through the Anthropic API**:
  - Pro: the strongest judgement for the hard frames (two views, colour Doppler, no
    B-mode image).
  - Con: the frames go to Anthropic.
  - The user chose this, saying the frames come from public datasets and that they allow
    it for the labeling projects they name.
- **Claude Opus 5.5 through Bedrock on aws-labelstud**: no faster, needs IAM changes, and
  goes against the cloud agent's rules
  ([DEC-026](../decisions/DEC-026-cloud-agent-runs-cloud-services.md)). Rejected.

**How the frames reach the model**
- **The `cloud` subagent fetching frames from aws-labelstud** (the user asked if this
  would be faster). No:
  - It runs in the same session on machine01.
  - The slow part is the model looking at each frame, not moving about 150 MB.
  - Its rules forbid reading image-server memory.
- **Claude Code subagents opening frames with tools**: needs the CLAUDE.md image rule and
  the patient-data hook relaxed, and is hard to reproduce.
- **A batch script on machine01** that reads the plain frames in memory and sends them
  through the Message Batches API: reproducible, with a fixed model, prompt and version,
  and no change to the image-reading rule for agents. Chosen.

A one-frame test on 2026-10-30, with an image the user pasted into chat, gave Claude's box
within 7 px of the cropper's (IoU 0.96, n = 1). That shows the format works. It says
nothing about accuracy on the sample.

## Conclusion

Recorded in [DEC-029](../decisions/DEC-029-claude-labels-named-labeling-projects.md):
- Claude Opus 5.5 labels a local mirror of the TASK-032 project through the API.
- Only frames of labeling projects the user names are sent.
- The run is blind to the human's labels and to the cropper's boxes.
- The comparison follows once both sets are done.

Board tasks: `TASK-032.01` (`method`, the code) and `TASK-032.02` (`exp`, the run and EXP record).

## Open questions

- No record says which of the 72 datasources are public datasets. The user's statement in
  chat is the basis for DEC-029.
