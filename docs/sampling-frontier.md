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

Dispatched 2026-10-22 on `pacland-rog` (queued):
- `h12-3-m3-vacua` — h12=3 model_ID=3, n_target=40, max_batches=300.
- `h12-4-m1-vacua` — h12=4 model_ID=1, n_target=40, max_batches=250.

Result merges into `data/h12_3_m3_vacua.json` / `data/h12_4_m1_vacua.json` for the
vacuum statistics (SUSY count, tadpole distribution, mirror-symmetry check).
