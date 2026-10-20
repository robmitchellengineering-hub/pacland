# Colibri evaluation — run frontier LLMs locally on RAM + NVMe (no GPU)

Rob's idea (2026-10-20): use [Colibri](https://github.com/JustVugg/colibri) to run the
research LLMs on a machine we own, removing the graphics-card cost — and develop it
further (RAID0 NVMe, and possibly embed it in MorpheOS). This is the assessment of
whether that works and what the machine should be.

## What Colibri is

Pure-C inference engine (Apache 2.0) that runs very large mixture-of-experts models
(GL-M-5.2 744B, DeepSeek V4 Flash 284B, Kimi K3 2.8T, …) on commodity hardware by
**streaming the routed-expert weights off disk** into RAM only when the router asks.
OpenAI- and Anthropic-compatible API at `localhost:8000`. No GPU required; optional
Vulkan (any GPU incl. integrated) / CUDA / Metal tiers.

## The architecture (why "so much RAM")

A MoE model splits into two parts:

- **Dense part** (attention, shared experts, embeddings) — read on **every token**, so
  it must be resident in RAM. GLM-5.2 int4 ≈ **9.9 GB**; DeepSeek V4 Flash ≈ **16 GB**.
- **Routed experts** (~90% of parameters) — streamed from disk on demand, **no RAM**.

So RAM holds only the dense core + a cache of the hottest experts. The lever to cut
the RAM floor further is Colibri's **dense conversion**: their Inkling engine drops
**120 GB → 25 GB** by converting the dense weights to int4. That is the answer to
"why so much RAM" and the fix already exists in-tree.

## Disk is the bottleneck — but only until it isn't

Colibri's own measurements (`docs/multidisk.md`):

- **2 independent NVMe drives: +37.5%** decode (0.80 → 1.10 tok/s, `DIRECT=1`).
- **A 3rd drive: neutral** (within run-to-run noise).
- **Hard ceiling:** GLM-5.2 fully RAM-resident = **1.83 tok/s** on a 16-core Ryzen —
  that is the **CPU** bound, not disk.

**Conclusion: RAID0 across 5 NVMe is over-provisioned.** The bottleneck moves from disk
to CPU after ~2 drives, and extra bandwidth is wasted. Spend on RAM (expert-cache
residency) and CPU (the decode ceiling) first, then 2–3 NVMe, not 5.

## Two machine profiles — this is the key insight

There are two *different* compute costs, and they need two different machines:

| cost | what | the machine it wants |
|---|---|---|
| **JAX numeric** (h12=25→272 flux sampling) | the "bigger machine" | NVIDIA GPU (the `compute-plan.md` RTX 4090 build) |
| **LLM inference** (research fan-outs, adversarial review) | the bigger *spend* | RAM + CPU + NVMe, **no GPU** (Colibri) |

Colibri removes the GPU from the second, not the first. They are not interchangeable.

## The no-GPU box (for the LLM half)

| part | pick | why |
|---|---|---|
| CPU | Ryzen 9 7950X / 9950X (16c/32t) | the decode ceiling is CPU-bound |
| RAM | 64 GB (128 GB for GLM-5.2 resident) | more RAM = more resident experts = faster |
| Storage | 2× 2 TB NVMe Gen4 (RAID0 or `COLI_MODEL_MIRROR`) | the +37.5% lives in the first two drives |
| GPU | none (iGPU already helps some models) | that is the whole point |

≈ USD 1,500–2,000, vs the ~$3,500–4,000 GPU build.

## The honest speed caveat

Even on this box, DeepSeek V4 Flash runs **~1–1.6 tok/s**; the API runs six agents in
parallel at hundreds of tok/s. Colibri is **free but slow** (overnight/batch fan-outs),
not a drop-in replacement for the interactive fan-outs. Complementary, not a swap.

## Next test before any build (rent-first, ~$5–20)

Rent a RAM-heavy CPU instance (Hetzner / Vast.ai CPU node / AWS r7a/r8g 64 GB+),
install Colibri, run DeepSeek V4 Flash 284B, and measure:

1. does its output quality hold up for the theorem-hunt / adversarial-review prompts;
2. actual tok/s on a 16-core box (confirm ~1–1.6);
3. whether the fan-out *throughput* (parallel agents) can ever be met locally.

If (1)+(2) pass, buy the box. If only (2) matters and (3) never closes, keep the API
for interactive work and use Colibri for batch.

## MorpheOS note (deferred)

Embedding a local model in the AI-native OS is a real direction, but it is a
*different* repo and workstream. Before touching it, read `MORPHEOS-BRIEFING.md` in
this workspace. Colibri already runs on a 25 GB laptop (GLM-5.2 at 0.05–0.1 tok/s
cold); the laptop-usable tier is Qwen3.6-35B (~6–10 tok/s) plus the tiny "System One"
decision models (Laya / GLiNER2.5-Decide, ~250 ms) — the last are the natural fit for
an OS-level assistant that answers quick decisions, not long generations.
