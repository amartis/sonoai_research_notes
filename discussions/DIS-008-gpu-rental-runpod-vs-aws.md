---
id: DIS-008
title: GPU rental for training, RunPod Secure Cloud vs AWS EC2
status: open
created: 2026-10-29
outcomes: []
related: [DEC-001, DEC-005, DEC-020, DEC-023, DEC-024]
---
# DIS-008: GPU rental for training, RunPod Secure Cloud vs AWS EC2

## Question

Training runs on the Windows GPU box (machine02) and, when that is not enough,
on rented GPUs. Until now the only rental named in the notes was RunPod, Secure
Cloud only ([DEC-001](../decisions/DEC-001-encrypted-data-store.md)), with a
runbook in `deploy/runpod/README.md`. Since 2026-10-29 the project also has an
AWS account, with enc1 images on S3 and Label Studio on EC2
([DEC-023](../decisions/DEC-023-aws-s3-for-enc1-and-ec2-for-label-studio.md),
[DEC-024](../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)).
The user asked (2026-10-29) how renting GPUs on AWS compares with RunPod.

## Options considered

Prices were read on 2026-10-29: RunPod from its own pricing page, AWS from
Vantage (a third-party tracker of the AWS price list, updated the same day;
region not labelled on the page, probably US East). The AWS H100 price
matches a second source (Opslyft). Prices change often; recheck before
budgeting.

**Table 1. On-demand price for one GPU, in US dollars per hour (2026-10-29).**

| GPU (memory) | RunPod Secure Cloud (USD/h) | AWS on-demand (USD/h, instance) | AWS spot (USD/h) | AWS / RunPod |
|---|---|---|---|---|
| L4 (24 GB) | 0.59 | 0.81 (g6.xlarge) | 0.62 | 1.4 |
| L40S (48 GB) | 1.09 | 1.86 (g6e.xlarge) | 1.65 | 1.7 |
| A100 | 1.79 (80 GB) | 21.96 for 8 × 40 GB (p4d.24xlarge); no 1-GPU size | 18.55 (8 GPUs) | 1.5 per GPU, but 8 GPUs minimum |
| H100 (80 GB) | 2.89 (PCIe) / 3.99 (SXM) | 6.88 (p5.4xlarge) | 4.49 | 1.7 to 2.4 |

Spot: spare AWS capacity, cheaper but can be reclaimed at any time.
RunPod Community Cloud is cheaper still but excluded by DEC-001.

Example: 100 GPU-hours costs 109 USD (RunPod) vs 186 USD (AWS) on an L40S,
and 289 to 399 USD vs 688 USD on an H100.

**Table 2. Other differences.**

| | RunPod Secure Cloud | AWS EC2 |
|---|---|---|
| Ready in this repo | Yes: `deploy/runpod/` (Dockerfile matching [DEC-020](../decisions/DEC-020-default-venv-matches-gpu-box.md), `run.sh`, rsync of enc1 data) | No: needs a deploy path, an IAM policy that allows GPU instances, and a new DEC for training data on EC2 |
| First GPU | Minutes | New accounts have a GPU vCPU quota of 0 ("Running On-Demand G and VT instances", "... P instances"); an increase must be requested per region and may be refused at first |
| Compliance | SOC 2 Type II; HIPAA claimed; a BAA (business associate agreement) is case by case | BAA self-service in AWS Artifact; only listed HIPAA-eligible services are covered |
| Storage | Network volume 0.07 USD/GB-month | EBS disk billed separately (price not checked) |
| Data transfer | No fee listed | 100 GB/month out to the internet free, then per GB (rate not checked) |
| Billing | Per second | Per second, 60 s minimum (Linux) |
| Cheaper options | Reservations through sales | Spot; reserved (L40S 1-year: 1.17 USD/h) |

- **A, RunPod Secure Cloud only** (current state): cheapest on-demand by a
  factor of 1.4 to 2.4, already set up, quick to start. Cons: the BAA is not
  automatic; data goes to a second provider.
- **B, AWS EC2 only**: one provider for storage, labeling and training; the
  enc1 images already sit on S3 in the same account. Cons: 1.4 to 2.4 times
  the price, the GPU quota starts at 0, no 1-GPU A100, and new deploy work.
  Training from S3 is not yet possible: the S3 copy holds images only, no
  tables (DEC-024).
- **C, RunPod by default, AWS as a fallback**: keep A; set up B only if a
  need below appears.

## Conclusion

Not decided. Recommendation (from the agent, not yet agreed): **C**. Keep
RunPod Secure Cloud for rented training; consider AWS only if

- the institution requires the data under a signed BAA, or on AWS only;
- AWS credits make it cheaper in practice; or
- RunPod has no capacity for the GPU needed.

Choosing B would extend where enc1 data and the key go (DEC-001, DEC-024), so
it needs its own DEC before any data moves.

## Open questions

- Which legal frame applies (HIPAA, GDPR or another)? This decides whether a
  BAA matters. Assumed unknown.
- Does the user have AWS credits?
- If S3 becomes the training source, same-region S3 to EC2 transfer is
  believed to be free and S3 to RunPod is charged as transfer out. Unverified.

## Sources (checked 2026-10-29)

- RunPod pricing: <https://www.runpod.io/pricing>
- Vantage instance pages: <https://instances.vantage.sh/aws/ec2/g6.xlarge>,
  <https://instances.vantage.sh/aws/ec2/g6e.xlarge>,
  <https://instances.vantage.sh/aws/ec2/p4d.24xlarge>,
  <https://instances.vantage.sh/aws/ec2/p5.4xlarge>
- Opslyft, AWS GPU pricing: <https://www.opslyft.com/blog/aws-gpu-pricing>
- AWS EC2 instance quotas: <https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-quotas.html>
- AWS HIPAA (BAA in AWS Artifact): <https://aws.amazon.com/compliance/hipaa-compliance/>
- AWS on-demand pricing (billing, free transfer): <https://aws.amazon.com/ec2/pricing/on-demand/>
- RunPod SOC 2 Type II: <https://www.runpod.io/blog/runpod-achieves-soc-2-type-ii-certification>
- RunPod HIPAA and GDPR: <https://www.runpod.io/press/runpod-achieves-hipaa-and-gdpr-compliance>
- RunPod BAA help article: <https://contact.runpod.io/hc/en-us/articles/50120688006163>
