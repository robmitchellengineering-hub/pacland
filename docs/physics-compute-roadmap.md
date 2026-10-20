# Physics compute — removing the GPU, and whether pooling cheap machines works

Rob's questions (2026-10-20): can we do for the *hard physics compute* (JAX flux-vacua
sampling) what Colibri does for LLM inference — drop the expensive graphics card — and
would pooling enough cheap old machines across the Rob mesh build an efficient system?

## Why the two compute problems are different shapes

| | LLM inference (Colibri) | physics compute (flux vacua) |
|---|---|---|
| bound by | **memory** (weights move) | **FLOPs** (dense linear algebra) |
| structure | **sparse** — MoE routes ~5% of experts per token | **dense** — Newton solve, Hessian O(n³) |
| Colibri's trick | stream the inactive 95% from disk | *no equivalent slab to skip* |

So Colibri's disk-streaming does not port. What ports is the *principle*: **don't do the
expensive work you don't need yet.** Three concrete forms:

## The three levers (the actual "no-GPU" project)

1. **Algorithmic staging** — the true analogue. Newton computes a full Hessian every
   step. Quasi-Newton (L-BFGS) approaches the critical point with cheap rank-1 updates
   (O(n²), no Hessian); the full Hessian is paid **once, at the end, to certify** the
   critical point. "Don't compute the expensive thing until you're sure you need it."
2. **Fix the JAX-CPU path.** The 96 GB OOM is *"the vmapped Newton solver's JIT tracing"*
   (`jax.vmap + while_loop + linalg.solve`), not a fundamental need — `solver="scipy"`
   already runs h12=25 in **4 GB**. A **chunked** JAX-CPU solve (batch manually, not
   `vmap`) may run fast on CPU with no OOM and no GPU. Worth trying before any hardware.
3. **Candidate-parallelism.** Each vacuum is an independent Newton solve — embarrassingly
   parallel. Fan the sampler across the mesh's **40 cores** (mac 8 + win-2 16 + win 16)
   and "hundreds of vacua" drops from ~a day on one core to ~tens of minutes, free.

## The honest boundary

- **h12=25**: solvable CPU-only via levers 2+3 on what we already own.
- **h12=272**: the real frontier — Hessian is 544×544, ~1000× more work per candidate.
  Here a GPU genuinely buys what no cheap trick replaces, *unless* lever 1 or the
  Picard-Fuchs / period structure yields a shortcut. A research bet, not a sure thing.

## Pooling cheap old machines — the assessment

**The workload is the deciding fact, and it pools well.** Embarrassingly parallel over
candidates = the SETI@home/Folding@home shape: no fast interconnect, each machine chews
its own shard. That part of Rob's instinct is right.

**But "old GPUs" is the weak half:**

- **CPU tier (h12=25):** runs on CPU (`scipy`, 4 GB). Old/free CPU boxes work — and the
  mesh already has 40 cores. **No GPU needed at all.**
- **Old GPUs for the GPU tier (h12=272):** poor ROI. One RTX 4090 ≈ 82 TFLOPS FP32 vs a
  GTX 1060 ≈ 4.4 — so ~18 old cards at $60 each ($1,080) plus 18 host machines, power and
  management, vs one 4090 (~$1,800) or **renting** one at ~$0.40/hr. Pascal cards sit at
  the edge of JAX/CUDA support, and 6–8 GB VRAM is fine for h12=25's small Hessians but
  not h12=272. Renting a modern GPU for a few hours beats maintaining a pile of old cards.

**The efficient system is a sharder, not a GPU pool.** The mesh already provides the
hard part (git-as-bus dispatch, one job per node). What's missing is ~100 lines: split the
candidate list into shards, dispatch each shard to a node, aggregate the results back.
That is lever 3 made concrete, and it needs no new hardware.

**Verdict:** pool old **CPU** boxes (free/cheap) for the CPU tier — genuinely worth it,
and mostly already in hand. Do **not** buy old GPUs — rent a modern one for the bursty
GPU tier. Build the sharder on top of the mesh dispatch.

## Potential MorpheOS route (flagged)

Two things here are candidate MorpheOS routes (its AI layer and mesh pillar): **a local
model embedded in the OS** (Colibri, see `colibri-evaluation.md`) and **distributed
compute over a device mesh** (the sharder above). They are recorded here as the canonical
home; a MorpheOS `plan` PR is the mechanism to promote them there, pending Rob's go and a
read of the repo's `HANDOFF.md` + `docs/20-build-plan.md`.
