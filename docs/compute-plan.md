# Compute plan — the dream machine, and the GPU rental for now

What hardware the PACLAND work actually needs, what it costs, and the turn-key
cloud-GPU rental that unblocks the "bigger machine" (h12=25→272 flux-vacua sampling)
today. Companion script: `scripts/gpu_bootstrap.sh`.

## What the work actually needs (bottleneck-first)

| workload | the bottleneck | what fixes it |
|---|---|---|
| **JAXVacua** (h12=25→272) — the "bigger machine" | single-threaded `scipy` Newton ~43 s/candidate; the vmapped JAX trace OOM'd at ~96 GB on CPU | **NVIDIA GPU + JAX/CUDA** — the one thing that changes the game |
| **CYTools** (polytope triangulation) | single-threaded per polytope, parallel over a corpus | many cores |
| **Lean 4 + Mathlib** | `lake build`, mathlib cache 7.2 GB | NVMe + decent CPU (the 16 GB Mac already does it) |
| **sympy exact proofs** | single-threaded symbolic | one fast core |
| **fan-outs / adversarial review** | model tokens — *not* local hardware | API budget, not a PC |

**The honest headline:** the only component that meaningfully accelerates the stuck
piece is an **NVIDIA GPU for JAX**. Everything else any mid-range machine does.

## The dream machine

| component | pick | why |
|---|---|---|
| GPU | **RTX 4090 24 GB** (or RTX 6000 Ada 48 GB) | JAX on CUDA turns the vmapped Newton solve from OOM/43 s into batched-GPU; 48 GB removes the memory anxiety |
| CPU | **Ryzen 9 7950X** (16c/32t) | CYTools corpus + sympy + Lean in parallel |
| RAM | **64 GB DDR5** (128 GB with the 6000 Ada) | the 96 GB trace explosion is never a wall again |
| Storage | **2 TB NVMe Gen4** | mathlib cache + data + venvs, instant |
| OS | Ubuntu 24.04 | JAX/CUDA/Lean are first-class on Linux |

## Cost

USD, with AUD at **1 USD ≈ 1.52 AUD** (approximate — parts shift with market).

**Recommended workhorse — ~USD 3,500–4,000 (~AUD 5,300–6,100):**
- RTX 4090 (24 GB) — ~USD 1,800 (~AUD 2,750)
- Ryzen 9 7950X + board — ~USD 700 (~AUD 1,050)
- 64 GB DDR5 — ~USD 200 (~AUD 300)
- 2 TB NVMe + PSU/case/cooling — ~USD 500 (~AUD 750)

**No-compromises — ~USD 9,000–12,000 (~AUD 13,700–18,300):**
- RTX 6000 Ada (48 GB) — ~USD 7,000 (or a used A6000 48 GB at ~USD 3,500)
- Threadripper 7960X + 128 GB DDR5 — the rest

**Cloud GPU (no upfront) — the path chosen for now:**
- A100 40 GB on Lambda — ~USD 1.29/hr (~AUD 1.96/hr)
- RTX 4090 spot on Vast.ai — ~USD 0.40/hr (~AUD 0.61/hr)
- RunPod 4090/A100 — in between

## The GPU rental plan (turn-key)

**Recommendation for a first run:** rent an **A100 40 GB on Lambda** (simplest,
fixed price, CUDA 12 image) or a **4090 on Vast.ai** (cheapest). Both give JAX a
CUDA device; the 4090 is ~3× cheaper and plenty for h12=25 sampling.

**Steps (numbered for a phone):**

1. **Lambda Labs** — https://lambdalabs.com/service/gpu-cloud — sign up, add a card.
2. Launch an instance: **Ubuntu 22.04/24.04 + CUDA 12**, pick **1× A100 40 GB**
   (or **1× RTX 4090** on the Vast/RunPod equivalent).
3. Copy the SSH command Lambda shows, and run it in a terminal.
4. Paste this single line on the instance (installs JAX+CUDA, JAXVacua, CYTools,
   clones pacland, verifies the GPU and the quintic known-answer):

```
curl -sSL https://raw.githubusercontent.com/robmitchellengineering-hub/pacland/main/scripts/gpu_bootstrap.sh | bash
```

5. When it prints `bootstrap complete`, start sampling:

```
cd pacland && source .venv/bin/activate
python scripts/sample_h12_25.py 30 h12_25_vacua.json
```

**What "working" looks like:** step 4 prints `GPU OK` and `CYTools OK (1, 101)`; step
5 writes `h12_25_vacua.json` and prints `DONE`. That is the memory-safe sampler running
with a GPU-backed JAX (the `jax[cuda12]` install makes `jax.devices()` list the GPU).

**Bootstrap script:** `scripts/gpu_bootstrap.sh` (committed; self-contained, asserts
its own result). Untested on a live GPU from here — the one knob is `jax[cuda12]` vs
`jax[cuda11]`, which must match the image's CUDA version.

## The honest caveat

The expensive thing in this project so far has been the **research fan-outs (peak token
credits)** — no PC fixes that. The dream machine and the GPU rental buy the *compute*
(JAX, CYTools, Lean, sympy), not the LLM agents. Budget the two separately.
