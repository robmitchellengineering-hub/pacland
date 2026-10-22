# Sampling frontier — the stabilised regime ends at h12 = 4 (measured 2026-10-22)

The "bigger systems" run at h12=25 returned 0 vacua; the question was whether that
is a bug or the physics. It is the physics, and the boundary is now measured.

## The frontier

| h12 | model_ID | cond(metric `I=Im N`) | critical points / 3 batches (60 candidates) |
|---|---|---|---|
| 2  | 1 | 2.4e1  | **9** |
| 3  | 2 | 3.9e2  | **6** |
| 3  | 3 | 1.4e1  | **1** (1 SUSY) |
| 4  | 1 | 6.3e2  | **2** |
| 4  | 2 | 2.5e3  | **2** |
| 5  | 1 | 3.1e4  | **0** |

- **h12 ≤ 4 has isolated SUSY flux vacua** and they are samplable (rates 1–15%).
- **h12 ≥ 5 is the cliff**: cond(metric) jumps to ~1e4+ and the count drops to 0.
  That is the distance-conjecture tower — beyond ~4 moduli the field-space metric
  develops near-flat directions and the isolated-vacua regime ends (see
  `docs/h12-25-sampling-wall.md` for the ISD-matrix mechanism).

So the quantitative boundary is: **stabilised (exact-structure) regime h12 ≤ 4 →
open-moduli regime h12 ≥ 5.**

## A data bug was masking h12=3

`model_ID=1` at h12=3 has **no Kähler-cone hyperplanes** (`lcs_tree.hyperplanes is
None`), so the moduli sampler crashes in `find_interior_points` before any
candidate is generated. Other h12=3 model_IDs (2, 3, 4) carry the data and work.
`scripts/sample_h12_gen.py` takes `model_ID` explicitly so the frontier can be
sampled on a valid model.

## The full run — 14 models, 5,885 vacua (2026-10-22, sharded on `pacland-rog`)

| h12 | model | crit pts | SUSY | SUSY% | W₀ med (10^) | g_s max | `N_flux` | `L` |
|---|---|---|---|---|---|---|---|---|
| 2 | m1 | 500 | 120 | 24% | 6.3 | 0.48 | [1, 274] | 276 |
| 2 | m2 | 500 | 202 | 40% | 1.8 | 0.50 | [2, 118] | 120 |
| 2 | m3 | 504 | 49 | 10% | 20.2 | 0.49 | [1, 129] | 148 |
| 2 | m4 | 501 | 114 | 23% | 2.1 | 0.49 | [1, 118] | 124 |
| 2 | m5 | 500 | 124 | 25% | 2.2 | 0.50 | [1, 134] | 136 |
| 2 | m6 | 502 | 192 | 38% | 2.1 | 0.50 | [1, 132] | 132 |
| 2 | m7 | 417 | 154 | 37% | 1.8 | 0.49 | [1, 217] | 276 |
| 3 | m2 | 504 | 7 | 1% | 63.7 | 0.48 | [1, 135] | 136 |
| 3 | m3 | 408 | 141 | 35% | 1.7 | 0.50 | [2, 104] | 104 |
| 3 | m4 | 505 | 131 | 26% | 2.6 | 0.50 | [1, 120] | 120 |
| 4 | m1 | 159 | 8 | 5% | 17.1 | 0.50 | [1, 76] | 76 |
| 4 | m2 | 171 | 0 | 0% | 64.5 | 0.36 | [1, 64] | 104 |
| 4 | m3 | 500 | 2 | 0.4% | 63.2 | 0.29 | [1, 112] | 128 |
| 4 | m4 | 214 | 1 | 0.5% | 62.9 | 0.49 | [1, 108] | 136 |

**Aggregate:** h12=2 → 3,424 pts / 955 SUSY (**27.9%**) · h12=3 → 1,417 / 279
(**19.7%**) · h12=4 → 1,044 / 11 (**1.1%**) · h12=5 → 0. Total **5,885 critical
points, 1,245 SUSY vacua.**

## What the full run shows

1. **The SUSY fraction collapses ~25×** from h12=2 (28%) → h12=3 (20%) → h12=4 (1%)
   → h12=5 (~1%). The frontier is a measured curve, not a single cliff.
2. **The constraint holds everywhere** — all 5,885 vacua satisfy `N_flux ≤ L`, no
   exceptions.
3. **W₀ is free** — spans ~77 orders of magnitude (`10^0.1` to `10^78.9`); `g_s` stays
   weak (`< 0.5`).
4. **W₀ median tracks the SUSY fraction** — the SUSY-rich models (h12=3 m3/m4, ~30%)
   have small `W₀` (median `10^1.7`–`10^2.6`), while the SUSY-poor models (h12=4
   m2/m3/m4, ~0%) have huge `W₀` (median `10^63`–`10^65`). SUSY vacua live at small
   `W₀`; as h12 grows the sampler stops finding them and returns only large-`W₀`
   non-SUSY critical points.

## Correction (2026-10-22) — h12=5 is NOT 0, it is ~1–2%

The "h12=5 → 0" above was a **sampler artifact, not physics.** The standard sampler
(`sample_critical_points`) solves `dV = 0`, whose Hessian becomes ill-conditioned at
h12 ≥ 5 (the flat metric directions), so it *stalls* and reports no critical points.
Solving **`D W = 0` directly** (the F-terms) avoids the Hessian entirely, and it
finds SUSY vacua at h12=5: **1/100 trials (|DW| → 1e-9), ~1–2%.** So the SUSY fraction
at h12=5 is ~1%, not 0 — SUSY continues past the old wall, just rare.

The real lesson: **the frontier is a solver limit, not a physics boundary.** To sample
h12 ≥ 5, use the SUSY equations (`D W = 0`), not the potential gradient (`dV = 0`).

Vacuum JSONs are committed at `data/h12_<h>_m<m>_stats.json` (14 files; each vacuum
carries flux, moduli, tau, residual, is_susy).
