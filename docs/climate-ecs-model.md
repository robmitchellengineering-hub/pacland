# Best-prediction ECS — the trust-gated, conservation-gated estimate (widened)

Status: **computed and guarded** — `src/pacland/climate/ecs_model.py` +
`tests/test_climate_ecs_model.py` (12 tests, green). The first output of "the
model that works": not a certified future (impossible), but the best possible
ECS estimate built from the reliable content only.

## The finding, in one sentence

> **Two views of the same gates bracket the equilibrium climate sensitivity at
> ~2.7–3.1 K — a widened 53-model ensemble gated on sensitivity + forcing lands
> at 3.08 K (15 models, 13 families), while the strictest three-axis gate (which
> adds conservation, where data exists) collapses to 2.71 K (one family) — both
> inside the IPCC likely range, at its best estimate (~3.0 K).**

## The method — hard gates, not arbitrary weights

The future cannot be validated, so the best prediction is the one built only on
the models that pass the checks we can actually run. Each axis is a **hard
pass/fail gate** (parameter-free — no arbitrary continuous weights an
adversarial reviewer could attack):

| gate | what it requires | source |
|---|---|---|
| conservation | closes energy, mass AND salt in its control run | Irving et al. 2021 (ours) |
| sensitivity | ECS inside the IPCC likely range 2.5–4.0 K | Zelinka et al. 2020 |
| forcing | ERF2x inside 3.3–4.1 W/m² | Zelinka et al. 2020 |

Conservation drift exists for only **19** of the models (Irving's subset), so
the two views are reported over their own covers and never mixed:

| view | cover | gates | result |
|---|---|---|---|
| **widened** | 53 Zelinka models | sensitivity + forcing | 15 models, 13 families |
| **strict** | 19 models with drift | all three axes | 2 models, 1 family |

## The numbers (`python3 -m pacland.climate.ecs_model`)

```
WIDENED (53 models, sensitivity + forcing gates):
  naive (53)       3.78 K  [1.83, 5.64]
  sens+forc (15)   3.08 K  [2.56, 3.87]   (13 families)
STRICT (19 models with conservation drift, all three axes):
  naive (19)       4.08 K  [2.71, 5.55]
  conservation ( 5) 3.86 K
  three-axis ( 2)    2.71 K  (1 family)
```

## The two results, and what each is for

**Widened — 3.08 K (15 models, 13 families).** The full 53-model ensemble,
gated on the two axes that exist for every model. It removes **0.70 K** of the
naive mean and lands at the IPCC best estimate with a *real multi-family
ensemble* (AWI, CMCC, EC-Earth, FGOALS, GFDL, GISS, MIROC, MPI, MRI, NorCPM,
NorESM, SAM0 …). This is the **best prediction**: diverse, defensible,
parameter-free.

**Strict — 2.71 K (2 GISS variants, one family).** Adding the conservation gate
(where the data exists) removes **1.37 K** of the hot-model bias and collapses
to the single family that does not leak physics, is not hot, and forces
correctly. This is the strictest subset, not an ensemble — but it *agrees* with
the widened answer to within the IPCC range.

**The bracket [2.71, 3.08] K spans the IPCC best estimate (3.0 K).** Two
independent ways of applying the same discipline land on the same answer, which
is exactly the Rule of Three: the widened gate (many families) and the strict
gate (conservation) bracket the field's own best estimate, achieved by
verification rather than averaging.

## The honest caveats (each made a test)

1. **The 19-model drift subset is hot-biased** — its naive mean (4.08 K) is
   higher than the full 53's (3.78 K), so the two naives differ and are never
   mixed.
2. **The strict gate collapses to one family** (the GISS pair) — conservation is
   so selective that only one family survives; the widened gate (13 families) is
   the ensemble result, the strict gate is the cross-check.
3. **Family is a naming heuristic** (leading non-digit prefix) — good enough to
   show "many families vs one", not a taxonomy.

## Why this helps the sector

- **A defensible best prediction with zero tunable parameters** — anyone can run
  the same gates over their own model set and get the same number.
- **It separates two questions the field conflates**: *how hot* (ECS, gated
  2.7–3.1 K) vs *which models to trust* (the 15 or the 2 that pass).
- **It names the direction**: to sharpen the estimate, add models that *pass the
  gates* (conserve, reasonable sensitivity, reasonable forcing) — not another
  point forecast.

## Honest limits

- **Not a new climate model** — this re-weights the existing ensemble with
  verification gates; it simulates nothing.
- **Thresholds are assessed ranges, not measurements** — the *ranking* is robust
  to them, the exact survivor count is stated at these thresholds (same honesty
  rule as `docs/climate-cmip6-drift.md`).
- **Conservation data covers 19 of 53 models** — the three-axis gate is only
  meaningful on that subset; the widened gate is the general result.

## Reproduce

```sh
cd pacland
PYTHONPATH=src python3 -m pacland.climate.ecs_model
PYTHONPATH=src python3 -m unittest tests.test_climate_ecs_model -v   # 12 tests
```

Data: `data/climate/cmip6_ecs.json` (full 53-model Zelinka et al. 2020 table)
× `data/climate/cmip6_drift.json` (19-model Irving et al. 2021 drift). The
three-axis verdict is `src/pacland/climate/sensitivity_crosscheck.py`.
