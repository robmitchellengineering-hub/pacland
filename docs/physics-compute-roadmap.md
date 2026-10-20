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

**Refinement (Rob, 2026-10-20): old gaming laptops, not bare GPUs.** A gaming laptop is a
self-contained mesh node — CPU + RAM + storage + network + power in one box, exactly the
"one agent per machine" unit the mesh is built for. This is the better shape:

- **CPU tier (h12=25):** the laptops' CPUs do the work (`scipy`, 4 GB). Each laptop adds
  4–8 cores to the candidate-parallelism. **No GPU needed at all.**
- **Their GPUs are a bonus, not the point.** Mobile GPUs are throttled + 6–8 GB VRAM: fine
  for h12=25's small batched Hessians, useless for h12=272 (needs 24 GB+). So the laptop
  GPU does not change the h12=272 answer — still rent a modern GPU for that tier.
- **Caveats:** sustained load throttles laptop CPUs and wears them; run them plugged in
  (battery removed or charge-limited) and expect the boost clock to sag. N laptops = N
  things to keep updated and reliable — the mesh loop/watchdog already does most of that.

**Concrete example — the Legion Go (already a mesh node as `win-2`).** Ryzen Z1 Extreme
(8c/16t Zen 4) + Radeon 780M iGPU + 16 GB LPDDR5X, small and low-power. It is the exact
architecture the Colibri evaluation names as the CPU/iGPU sweet spot, just at the small
end: the 780M is the GPU in Colibri's own "machine A" (Qwen3.6-35B at 6.0 tok/s CPU /
9.9 Vulkan-iGPU), and 16 threads is ample for the h12=25 `scipy` sampler (4 GB). Its only
limits: **16 GB RAM** (no big frontier models — DeepSeek V4 Flash wants 16/32 GB) and **no
CUDA** (780M is an iGPU). A few of these = a cheap, quiet, low-power compute pool; their
CPUs do the flux work, and their iGPU can run the *small* local models for free.

**The efficient system is a sharder, not a GPU pool.** The mesh already provides the hard
part (git-as-bus dispatch, one job per node). What's missing is ~100 lines: split the
candidate list into shards, dispatch each shard to a node, aggregate the results back.
That is lever 3 made concrete.

**Verdict:** add old gaming laptops as cheap CPU+RAM mesh nodes for the CPU tier —
genuinely worth it, self-contained, and the mesh already supports them. Their GPUs are a
free bonus, not the reason. Still rent a modern GPU for the h12=272 tier.

## Potential MorpheOS route (flagged)

Two things here are candidate MorpheOS routes (its AI layer and mesh pillar): **a local
model embedded in the OS** (Colibri, see `colibri-evaluation.md`) and **distributed
compute over a device mesh** (the sharder above). They are recorded here as the canonical
home; a MorpheOS `plan` PR is the mechanism to promote them there, pending Rob's go and a
read of the repo's `HANDOFF.md` + `docs/20-build-plan.md`.
