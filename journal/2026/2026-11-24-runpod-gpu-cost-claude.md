# 2026-11-24

What did the RunPod pod of the epic 1 seed-0 runs cost, and could a cheaper 24 GB GPU (RTX 4090
or RTX 3090) do the same job? Can the pod's data move to a new pod? Written by Claude (Opus 5.5)
at the user's request. Exploratory cost analysis, not an EXP record and not a decision. No
images, tables or file names were read; only run metadata (`meta.json`, `metrics.jsonl`,
`train.log` timings and val means) and RunPod's own reads.

Abbreviations and terms: **A100**, NVIDIA A100 SXM 80 GB; **Secure Cloud**, RunPod's data-centre
tier, the only tier the runbook allows; **step**, one optimiser step of the global batch of 32;
**step-time ratio**, step time on another GPU divided by step time on the A100; **TF32**, the
19-bit tensor-core float format that PyTorch uses for convolutions by default; **volume disk**,
a pod's `/workspace` disk, tied to that pod's machine; **container disk**, the pod's own
disk, cleared when the pod stops; **R1 to R6**, the six epic 1 recipes ([DEC-080](../../decisions/DEC-080-epic1-optimisation-strategy.md)).

## Summary

1. **The pod cost $24.93 for 9.69 h of training.** Pod `1l262wv9deksxv` (A100, Secure Cloud,
   US-MD-1, $2.19/h) ran R1 to R6 of [TASK-197](../../../backlog/tasks/task-197%20-%20Epic-1-runs-on-RunPod-R1-to-R6-at-seed-0-then-seeds-1-and-2-of-the-best-recipe-shift-test-EXP-record-with-the-DEC-076-verdict-per-recipe-DEC-080.md) one after another on 2026-11-24, 00:45 to
   about 12:05 UTC. 85% of the paid GPU time was training; about 1.6 h went on setup
   (59 min before R1) and gaps between runs (45 min in total). Table 1.
2. **A 24 GB card is very likely cheaper for the same job.** Secure Cloud prices: RTX 4090
   $0.89/h (0.406 of the A100 price), RTX 3090 $0.50/h (0.228). The cheaper card wins while
   its step-time ratio stays below 2.46 (4090) or 4.38 (3090). The estimated ratios are
   0.8 to 1.8 (4090) and 1.2 to 2.5 (3090). These are estimates from the specs, not
   measurements (Table 3).
3. **The work still to do is small:** seeds 1 and 2 of R4, the recipe with the highest
   val mean W1 at seed 0 (0.8689 against R6 0.8687). About $9.40 on the A100; about $3.80 to
   $6.20 on a 4090 and $2.50 to $4.60 on a 3090 (Table 4).
4. **Same result only if micro-batch 32 fits in 24 GB.** Both cards then run the same
   arithmetic as the A100 (TF32 convolutions, FP32 matrix multiplies), and only rounding
   differs. If it does not fit, the plan falls back to accumulation (for example 16 × 2). The
   decoders' BatchNorm would then see fewer samples, and DEC-080 rule 5.5 already says such
   runs are not compared directly with the RunPod runs. Peak memory was never logged
   ([TASK-196.02](../../../backlog/tasks/task-196.02%20-%20RunPod-for-epic-1-later-TensorBoard-SSH-tunnel-and-1-epoch-timing-runs-of-R1-and-R4-DEC-080-rule-5.md), acceptance criterion 2, not ticked).
5. **Stock now (RunPod catalog read, Secure Cloud):** RTX 4090 available (low), only in
   EU-RO-1. RTX 3090 none. A100 SXM low, in EUR-IS-1, US-KS-2 and US-MD-1.
6. **Moving the pod's data is possible but not worth it.** The pod is stopped, so its
   container disk, which held the enc1 store, is already cleared. The 40 GB volume disk
   (code, venv, pretrained weights, run folders, logs, per the runbook) is tied to the pod's
   machine in US-MD-1. Every run folder is already on machine01, and the checkpoint backups
   are on S3. A fresh 4090 pod set up with the runbook loses nothing.

## The pod: what it ran and what it cost

Table 1. Seed-0 runs of TASK-197 on pod `1l262wv9deksxv`, in the order they ran. 30 epochs,
micro-batch 32, no accumulation, fp32 without autocast; 463 steps per epoch. Wall time comes
from `meta.json` (start to end). Step time is the median gap between consecutive training
steps in `metrics.jsonl`. Cost = wall time × $2.19/h.

| Run (recipe) | Start, UTC | Wall time, min | Median step time, s | Median epoch incl. evaluation, s | Cost at $2.19/h, $ |
|---|---|---|---|---|---|
| R1 transunet, ImageNet-21k weights | 01:43 | 100.9 | 0.308 | 180 | 3.68 |
| R4 DINOv3 ConvNeXt-B, MLP decoder | 03:29 | 98.8 | 0.317 | 183 | 3.61 |
| R5 DINOv3 ConvNeXt-B, UNet decoder | 05:14 | 95.8 | 0.305 | 178 | 3.50 |
| R6 DINOv3 ConvNeXt-B, UPerNet decoder | 06:59 | 116.3 | 0.379 | 212 | 4.24 |
| R2 transunet, from scratch | 09:05 | 106.3 | 0.308 | 185 | 3.88 |
| R3 resenc_unet, from scratch | 11:06 | 63.1 | 0.156 | 109 | 2.30 |
| **All six** | | **581.2 (9.69 h)** | | | **21.21** |

Table 2. Billing of the pod (RunPod `list-pod-billing`, hourly buckets, 2026-11-24).

| Item | Amount, $ |
|---|---|
| GPU, 11.33 h at $2.19/h | 24.80 |
| Disk, while running | 0.13 |
| **Total** | **24.93** |
| of which training (Table 1) | 21.21 |
| of which setup, gaps and tail | about 3.6 |

- From the training steps alone, evaluation (val and test every epoch, train every 5) takes
  about 20% of an epoch. R1: 180 s per epoch, of which 143 s are training steps.
- The pod's own clock and the billing buckets differ by a few minutes at the end (R3 ends at
  12:09 in `meta.json`; the last billing bucket covers about 5 min after 12:00). Unexplained.
- The pod is stopped (status EXITED). Its volume disk keeps billing, at a higher rate than
  while it runs, until the pod is terminated (RunPod concept rule
  `pod-billing.stopped-disk-rate`). The rate itself was not read.

## The cheaper cards

What sets the speed. The recipes use fp32 without autocast (DEC-080 rule 4). PyTorch then uses
TF32 for convolutions (`torch.backends.cudnn.allow_tf32` is True) and full FP32 for matrix
multiplies (`torch.backends.cuda.matmul.allow_tf32` is False). Checked on machine01 with
torch 2.11.0; the runs used torch 2.11.0+cu128. The A100 is faster on TF32 convolutions and on
memory-bound operations (norms, element-wise operations). The consumer cards are faster on
FP32 matrix multiplies: the ViT layers of transunet and the pointwise layers of ConvNeXt.

Table 3. Peak specs (vendor or spec sites, see Sources) and the estimated step-time ratio
against the A100. Price: RunPod catalog, Secure Cloud, read on 2026-11-24.

| GPU | Memory, GB | FP32, TFLOPS | TF32 tensor, dense, TFLOPS | Memory bandwidth, GB/s | Secure price, $/h | Break-even step-time ratio | Estimated step-time ratio (not measured) | Secure stock now |
|---|---|---|---|---|---|---|---|---|
| A100 SXM 80 GB | 80 | 19.5 | 156 | 2,039 | 2.19 | 1 | 1 | low (EUR-IS-1, US-KS-2, US-MD-1) |
| RTX 4090 | 24 | 82.6 | 82.6 | 1,008 | 0.89 | 2.46 | 0.8 to 1.8 | low (EU-RO-1) |
| RTX 3090 | 24 | 35.6 | 35.6 | 936 | 0.50 | 4.38 | 1.2 to 2.5 | none |

Break-even step-time ratio = A100 price ÷ card price.

- The estimated ratios are the analyst's reading of the specs, with low to medium confidence.
  The cards should do better on transunet and ConvNeXt (more matrix-multiply work) and worse on
  R3 (all convolutions with InstanceNorm).
- A rough check against one measured consumer card: [EXP-003](../../experiments/EXP-003-transunet-r50-b16-from-scratch-512-and-224-lseg-cirrhosis-v4.md)'s 224 px transunet run (the same
  `transunet` model class as R1) on the GPU box's RTX 3060 took 9.9 min per epoch. That epoch
  had 10,331 train samples and evaluated train, val and test every epoch. Scaled with R1's
  per-sample rates on the A100, the same epoch would take about 3.3 min, so the 3060 was about
  3 times slower than the A100. That run used micro-batch 8, different data and a different
  machine, so this is weak evidence. With the 3060's specs (12.7 TFLOPS FP32, 360 GB/s;
  unverified), it points to a 3090 near the low end of its range.
- The 4090 pod minimum is 8 vCPUs (catalog). The A100 pod had 18, and the machine profile
  uses 8 loader workers. If data loading is the limit, a 4090 pod with few vCPUs is slower.
  Not checked.

Table 4. Projected cost: projected hours × catalog price. For the six runs, setup and gaps
are held at the A100's 1.64 h; for the remaining pair, setup is taken as 1 h.

| GPU, step-time ratio | Six seed-0 runs again, h | Six runs, $ | Seeds 1 and 2 of R4, h | Seeds 1 and 2 of R4, $ |
|---|---|---|---|---|
| A100, measured | 11.3 | 24.93 | 4.3 | about 9.40 |
| RTX 4090, 1.0 | 11.3 | 10.10 | 4.3 | 3.80 |
| RTX 4090, 1.3 | 14.2 | 12.70 | 5.3 | 4.70 |
| RTX 4090, 1.8 | 19.1 | 17.00 | 6.9 | 6.20 |
| RTX 3090, 1.2 | 13.3 | 6.60 | 5.0 | 2.50 |
| RTX 3090, 1.8 | 19.1 | 9.50 | 6.9 | 3.50 |
| RTX 3090, 2.5 | 25.9 | 12.90 | 9.2 | 4.60 |

For the remaining pair, the cheaper cards save about $3 to $7 in total. The 3090 is the
cheapest on paper but has no Secure stock now, and it takes up to about twice as long in wall
time.

## Would the result change?

- **Micro-batch 32 fits in 24 GB:** same recipe, same arithmetic. The kernels differ, so
  rounding differs. The runs are already non-deterministic on one GPU (no deterministic mode is
  set), so the effect should be smaller than the seed-to-seed spread. Record the GPU per run in
  the EXP record.
- **It does not fit:** accumulation makes the BatchNorm layers see fewer samples (the
  transunet decoder; the DINOv3 decoders, including R4's head). DEC-080 rule 5.5 already
  treats such runs as not directly comparable, so seeds 1 and 2 of R4 would no longer match
  seed 0.
- **Memory estimate (not measured):** EXP-003 measured peak reserved memory for the official
  transunet at 512 px: 5.65, 7.91 and 9.99 GiB at micro-batch 2, 3 and 4. Scaled by pixel
  count, that gives about 15 GiB at 224 px and micro-batch 32. It does not cover R4's ConvNeXt-B,
  for which no figure exists.
- **Recipe changes such as bf16 autocast or less frequent evaluation** would also save time,
  but they change the recipe, so seeds 1 and 2 would no longer match seed 0. Not considered.

## Moving the data from pod `1l262wv9deksxv`

- **What is left on the pod.** The pod has a 40 GB container disk and a 40 GB volume disk at
  `/workspace`, not a network volume (the runbook asks for a network volume). The enc1 store
  sat on the container disk (`/root/data`, per the runbook). RunPod clears the container disk
  on stop (concept rule `container-disk.what-survives`), so the dataset is no longer on the
  pod. The volume disk still holds, per the runbook, the code, the venv, the pretrained weights,
  `/workspace/runs` and the logs. Not checked on the pod.
- **How a move would work.** The volume disk belongs to the pod's machine, and only that pod
  can use it (`pod-volume-disk.machine-level-not-data-center-level`). The API has no migrate
  action; the console offers migration only when a stopped pod cannot get its GPU back
  (`pod-migration.not-in-rest-v2`). A copy therefore needs the old pod started again: with its
  A100 at $2.19/h, or with zero GPUs. The files would then go to the new pod with
  `runpodctl send` / `receive`, or rsync over direct SSH (the proxy SSH carries a shell only,
  `pod-ssh-access.proxy-vs-direct`). The 4090 stock is in EU-RO-1, the pod in US-MD-1.
- **Data rules.** Only enc1 ciphertext may go to RunPod ([DEC-024](../../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md)). The volume disk holds no
  plain data, per the runbook, and the dataset is gone from the pod in any case.
- **Reading.** Nothing on the pod is needed. Run folders are on machine01; checkpoint
  backups are on S3 ([DEC-083](../../decisions/DEC-083-runpod-enc1-images-from-s3-and-encrypted-checkpoint-backups.md)). The venv and weights can be rebuilt in minutes. Images come
  from S3 and tables from machine01 again, as in the runbook. A copy would cost more time and
  A100 hours than it saves.

## Done

- Read pod `1l262wv9deksxv`, its hourly billing, and the Secure GPU catalog with stock
  (RunPod `get-pod`, `list-pod-billing`, `list-gpu-types`, `get-gpu-type`), plus the RunPod
  concept rules on disks, migration and file transfer.
- Timed the six seed-0 runs from their run folders on machine01 (run metadata only), and read
  the best val mean W1 per run.
- Checked the PyTorch TF32 defaults on machine01. Looked up the GPU specs on the web.
- Changed nothing: no pod was started, stopped or terminated, and no config was edited.

## Next (proposed, not agreed)

1. Decide whether seeds 1 and 2 of R4 may run on a 24 GB card. DEC-080 rule 5.1 names one
   A100 80 GB, so this needs a decision.
2. If yes: add a machine profile (for example `runpod_4090`; `run.sh` sets
   `SONOAI_MACHINE=runpod_a100`) and R4 plans for seeds 1 and 2. Then run a short check on a
   4090 pod: peak memory at micro-batch 32 (`torch.cuda.max_memory_reserved`) and step time,
   about $1 including setup. Go on only if memory stays under about 22 GB and the step-time
   ratio is under 2.
3. Use a network volume in the pod's data centre, as the runbook asks, so later runs can reuse
   the venv and weights.
4. Terminate pod `1l262wv9deksxv` once no one needs its volume disk (the user's action).

## Sources

- RunPod reads made on 2026-11-24 (catalog, pod, billing, concept rules).
- A100: [NVIDIA A100 product page and datasheet](https://www.nvidia.com/en-us/data-center/a100/).
- RTX 4090: [vast.ai RTX 4090 specs](https://vast.ai/pricing/gpu/RTX-4090),
  [Tom's Hardware, Ada Lovelace](https://www.tomshardware.com/news/nvidia-reveals-secrets-of-ada-lovelace-gpus);
  the [Ada whitepaper](https://images.nvidia.com/aem-dam/Solutions/geforce/ada/nvidia-ada-gpu-architecture.pdf)
  appendix was not read.
- RTX 3090: [Tom's Hardware, RTX 3090](https://www.tomshardware.com/news/nvidia-geforce-rtx-3090-ga102-everything-we-know),
  [wccftech spec table](https://wccftech.com/nvidia-geforce-rtx-3090-24-gb-official-launch-price-specs-performance/amp/);
  the [GA102 whitepaper](https://images.nvidia.com/aem-dam/en-zz/Solutions/geforce/ampere/pdf/NVIDIA-ampere-GA102-GPU-Architecture-Whitepaper-V1.pdf)
  appendix was not read.
- RTX 3060 specs: from memory, unverified.
