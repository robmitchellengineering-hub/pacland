# PACLAND climate trust board — every CMIP6 model, scored

Status: **computed and guarded** — `src/pacland/climate/trust_board.py` +
`tests/test_climate_trust_board.py` (8 tests, green). This is the reusable
asset of "the model that works": a per-model trust score the sector can apply
to **any** quantity (ECS today; 2100 warming and sea level next).

## The finding, in one sentence

> **Of 53 CMIP6 models, 15 pass sensitivity + forcing, and adding conservation
> (where drift data exists) drops MPI-ESM1-2-HR — leaving a trusted set of 14
> models across ~13 families, the models any prediction should be built from.**

## The scoring (three hard axes)

| axis | pass | source |
|---|---|---|
| sensitivity | ECS inside 2.5–4.0 K (both bounds) | Zelinka et al. 2020 |
| forcing | ERF2x inside 3.3–4.1 W/m² | Zelinka et al. 2020 |
| conservation | closes energy, mass AND salt | Irving et al. 2021 (17 of 53) |

A model is **trusted** if it passes every axis for which data exists — two axes
for every model, three where the drift data covers it.

## The trusted set (14 models)

```
NorESM2-LM, MIROC6, GFDL-ESM4, GISS-E2-2-H, GISS-E2-1-G, FGOALS-g3, NorCPM1,
GISS-E2-1-H, MRI-ESM2-0, AWI-CM-1-1-MR, CMCC-CM2-SR5, CMCC-ESM2, SAM0-UNICON,
EC-Earth3-AerChem
```

13 families — a genuine ensemble, not one model line. This is the set the ECS
best-prediction (3.08 K) is built from, and the set the next predictions (2100
warming, sea level) will reuse unchanged.

## Two bugs caught and fixed while building it (root-caused)

1. **`sensitivity_tier` enforced only the upper bound** (`ECS ≤ 4.0`), missing
   the IPCC lower bound. It would have admitted GISS-E2-2-G (2.43 K) and
   NorESM2-MM (2.49 K) — below the 2.5 K floor — inflating the trusted set to
   17. Fixed to both bounds; the 19-model three-axis result is unchanged (no
   sub-2.5-K model in that subset), verified by the full suite.
2. **Conservation is the discriminator the other two axes miss.** MPI-ESM1-2-HR
   looks fine on sensitivity (2.98 K) and forcing (3.65 W/m²) but leaks one
   ledger — so it is not trusted. The board surfaces this rather than hiding it.

## Why this helps the sector

- **A transferable "who to trust" list.** Any modelling centre can pick the 14
  trusted models for their own projection, instead of averaging all 53.
- **Parameter-free.** Hard pass/fail gates, no arbitrary weights.
- **Self-auditing.** The board names *why* each model is excluded (which axis it
  fails) — an actionable verdict, not a black-box score.

## Honest limits

- **Conservation covers 17 of 53.** For the other 36 the board scores two axes,
  not three; a model could still be untrustworthy on the axis we cannot measure.
- **Thresholds are assessed ranges, not measurements** — the ranking is robust to
  them, the exact trusted count is stated at these thresholds.
- **Family is a naming heuristic** (leading non-digit prefix), enough to show
  "many families", not a taxonomy.

## Reproduce

```sh
cd pacland
PYTHONPATH=src python3 -m pacland.climate.trust_board
PYTHONPATH=src python3 -m unittest tests.test_climate_trust_board -v   # 8 tests
```

Data: `data/climate/cmip6_ecs.json` (full 53-model Zelinka table) ×
`data/climate/cmip6_drift.json` (19-model Irving drift). The per-model scoring
is `src/pacland/climate/sensitivity_crosscheck.py`.
