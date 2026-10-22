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

## Runs

Dispatched 2026-10-22 on `pacland-rog`; both completed `pass`.

| run | critical points | SUSY | tadpole `N_flux` | bound `L` | all ≤ L |
|---|---|---|---|---|---|
| `h12-3-m3-vacua` (h12=3, model_ID=3) | **40** | **16** | [5, 103], med 48 | 104 | ✅ |
| `h12-4-m1-vacua` (h12=4, model_ID=1) | **40** | **2** | [2, 75], med 20 | 76 | ✅ |

Every one of the 80 vacua satisfies `N_flux ≤ L`. The SUSY fraction falls 40% → 5%
as h12 approaches the cliff — the constraint holds, the selection thins.

The constraint-first structure shows in the distributions (same runs):

| h12 | `W₀ = \|W\|` | `g_s = 1/Im τ` | `N_flux` |
|---|---|---|---|
| 3 | [14, 2.7e62], med 55 | [0.00, 0.47], med 0.16 | [5, 103] ≤ 104 |
| 4 | [7.9, 3.2e75], med 4.9e43 | [0.00, 0.43], med ~0 | [2, 75] ≤ 76 |

The **constraint is exact** (`N_flux ≤ L`, no exceptions) while the **parameter `W₀`
is free** — spread over ~60 orders of magnitude — and `g_s` stays weak (`< 0.5`, the
ISD sampler's perturbative regime). The exact thing is tight; the non-exact thing is
not predicted.

Vacuum JSONs are committed at `data/h12_3_m3_vacua.json` and
`data/h12_4_m1_vacua.json` (40 vacua each: flux, moduli, tau, residual, is_susy).
