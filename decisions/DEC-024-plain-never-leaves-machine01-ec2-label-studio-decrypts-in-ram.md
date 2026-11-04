---
id: DEC-024
title: Plain-style data never leaves machine01; S3 holds enc1 images only; Label Studio on EC2 decrypts them in RAM
status: accepted
area: [data-security, aws]
created: 2026-10-29
from: []
related: [DEC-005, DEC-018, DEC-022, DEC-023]
superseded_by:
---
# DEC-024: Plain-style data never leaves machine01; S3 holds enc1 images only; Label Studio on EC2 decrypts them in RAM

## Context

[DEC-023](DEC-023-aws-s3-for-enc1-and-ec2-for-label-studio.md) put the enc1
dataset files on S3 and the Label Studio server on EC2, and left open how images
reach Label Studio there, how the key gets there, and access control. On
2026-10-29 the user asked for the code to deploy both, and settled these points
in chat.

## Decision

- **Hard rule: plain-style data never leaves machine01.** No `<version>_plain`
  file, plain image, plain table, file name or folder name goes to S3, EC2,
  RunPod, the GPU box or any other machine or service. Only enc1 ciphertext
  leaves. This is enforced in five places: the upload code (refuses anything
  that is not a finished enc1 store), the patient-data hook (denies Claude's
  AWS, RunPod and upload tool calls, and outbound shell commands, that name
  plain data), the command policy (rule D1), the bucket policy (accepts only
  `datasets/*_enc1/` and `code/` keys) and the agent's IAM policy (denies
  `*_plain*` and `*_submit1*` keys).
  The [DEC-022](DEC-022-label-studio-open-to-outside-helpers.md) helper session is the one exception already accepted: helpers'
  browsers display plain images that machine01's own Label Studio serves.
- **S3 holds enc1 images only.** For a dataset, the bucket gets the image blobs
  of `<version>_enc1`, plus `style`, `kdf.json` and a newly encrypted manifest
  that lists the images only. The S3 copy is a valid, smaller enc1 store; the
  tables (`taskcrops_df`, label tables) stay on machine01. Keys mirror the data
  root: `s3://<bucket>/datasets/<version>_enc1/...`, the same relative paths as
  under `$SONOAI_DATA_FILES_ROOT`. The bucket is `claude-agent-sonoai-data`
  (the IAM policy allows only `claude-agent-*` buckets).
- **Label Studio on EC2 decrypts in RAM.** A small image server on the instance
  reads image blobs from S3 and decrypts them in memory; nothing plain is
  written to the instance disk. The user types the passphrase over an SSM
  (AWS Systems Manager) session each time the image server starts; it is not
  stored on AWS.
- **Access by SSM port forwarding only.** The instance has no inbound port and
  no SSH; the user reaches Label Studio at `http://127.0.0.1:<port>` on
  machine01 through `aws ssm start-session` port forwarding. Public HTTPS for
  outside helpers is a later, separate decision.

## Consequences

- Amends DEC-023 (closes its open points except public access) and the
  `CLAUDE.md` rule on where the encrypted store may go: S3 is now allowed.
- Label Studio's own state on EC2 (database, annotations) is label data on AWS.
  It lives on an encrypted EBS volume of the instance.
- Each image server start needs the user at a terminal to type the passphrase.
- The `claude-agent` IAM policy and boundary must be extended (EC2, SSM, instance
  profiles) before agents can deploy the stack; the user applies them in the
  IAM console.
- Training from S3 (GPU box, RunPod) is not covered: the S3 copy has no tables.
