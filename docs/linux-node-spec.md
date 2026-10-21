# Dedicated Linux compute nodes — the cheap path to native Linux on the mesh

Why this exists: the flux sampler (JAXVacua + cytools) is **Linux-only**, and the mesh's
only Linux today is two 4 vCPU / 4 GB VMs on `win-2`. Dual-boot was considered and rejected
(manual, fragile, and the Mac must never leave macOS — it is the way-in). This spec is the
clean alternative: **add dedicated Linux machines as permanent mesh nodes**, no flipping.

**Status (2026-10-21):** the first dedicated node is live — **`pacland-rog`** (ASUS GL752VW,
i7-6700HQ 8 threads / 32 GB, Ubuntu 24.04.5). Toolchain installed (`~/cytools-venv`:
cytools 1.4.12, jaxvacua 0.1.2), sampler at `~/sample_h12_25.py`, mesh loop running.
First h12=25 shard run dispatched overnight 2026-10-21 (`n_target=100, max_batches=800`).

## What a node needs (flux sampling + general Linux compute)

| resource | minimum | why |
|---|---|---|
| CPU | 8+ threads | the `scipy` solver is ~1 thread/candidate; more cores = more parallel candidates |
| RAM | 16 GB | the solver needs ~1.5 GB; more RAM = more candidates in flight |
| GPU | **none** | h12=25 runs on CPU; h12=272 is rented, not bought |
| disk | 100+ GB SSD | models, venvs, `data/` |
| OS | Ubuntu 24.04 | first-class for JAX / cytools / Lean |

## Cheapest options (used, ~AUD 200–500)

- **Used gaming laptop with Linux** (the earlier idea) — self-contained CPU+RAM+disk+network in one box.
- **Business SFF desktop** (Dell OptiPlex / HP EliteDesk / Lenovo ThinkCentre) — cheapest per core, expandable RAM, built for 24/7.
- **Used mini-PC** — quiet, low power, stacks well.

For the LLM / Colibri side (separate from this), the upgrade is the Ryzen AI Max 395 —
see `colibri-evaluation.md`.

## Install (one-time, ~30 min)

1. Install **Ubuntu 24.04** (server, headless is fine).
2. Join the mesh as a node:
   ```sh
   git clone https://github.com/robmitchellengineering-hub/harness-mesh ~/harness-mesh
   cd ~/harness-mesh && ./scripts/oneclick-node.sh --host <name>
   ```
3. Install the oracle stack (see `toolchain.md`):
   ```sh
   sudo apt-get install -y libgmp-dev libgmpxx4ldbl
   python3 -m venv ~/cytools-venv && ~/cytools-venv/bin/pip install cytools jaxvacua
   ```
4. Copy the sampler (or clone the repo):
   ```sh
   curl -sSL https://raw.githubusercontent.com/robmitchellengineering-hub/pacland/main/scripts/sample_h12_25.py -o ~/sample_h12_25.py
   ```

Then it is a shard target for `scripts/shard_vacua.sh <n_total> <node> ...`.

## What it buys

Each node adds its cores to the candidate-parallelism. One 8-core node roughly doubles the
current Linux capacity (2 × 4-vCPU VMs); three nodes make "hundreds of vacua" an overnight
run instead of a multi-day one. No GPU, no dual-boot, no risk to `win-2` (AirMatrix) or the Mac (way-in).
