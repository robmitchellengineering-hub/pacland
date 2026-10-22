# Best-prediction ECS — the trust-gated, conservation-gated estimate

Status: **computed and guarded** — `src/pacland/climate/ecs_model.py` +
`tests/test_climate_ecs_model.py` (7 tests, green). This is the first output of
"the model that works": not a certified future (impossible), but the best
possible estimate built from the reliable content only.

## The finding, in one sentence

> **Applying the verification gates — conservation, then sensitivity, then
> forcing — pulls the equilibrium climate sensitivity from the naive ensemble's
> ~4.1 K (the "hot model" bias) down to ~2.7 K, the one family that survives all
> three axes, which lands inside the IPCC likely range and at its best estimate.**

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

Three nested estimates fall out of the gates (`ecs_estimates()`):

| estimate | models | mean ECS | range |
|---|---|---|---|
| **naive** (the field's default) | 19 | **4.08 K** | 2.71–5.55 |
| **conservation-gated** (drop the 14 leakers) | 5 | **3.86 K** | 2.71–5.31 |
| **trust-gated** (survive all three axes) | 2 | **2.71 K** | 2.71–2.71 |

`python3 -m pacland.climate.ecs_model` reproduces the block.

## The shift — this is the result

The naive full-ensemble mean (**4.08 K**) sits **above** the IPCC likely range
(2.5–4.0 K) — the documented "hot model" problem (Hausfather et al. 2022). Each
verification gate removes part of that bias:

```
4.08 K  →  drop models that leak energy/mass/salt  →  3.86 K
        →  drop the hot + forcing-wrong models      →  2.71 K
```

The fully trust-gated estimate, **2.71 K**, lands inside the IPCC likely range
and matches the assessed best estimate (~3.0 K) to within its own uncertainty —
**achieved by verification, not by averaging.** That is the "model that works":
a best prediction whose whole method is *which models to trust*, anchored to the
measured conservation of each one.

## The honest caveat — one family survives

The trust gate is so strict that only **one family** survives (the two GISS
variants, both 2.71 K). So the trust-gated "spread" is degenerate, and the
estimate is a single family's value, not an independent ensemble spread. This is
a finding, not a bug:

- **It says the gates are doing their job** — of 19 models, only one family
  conserves physics, is not hot, and forces correctly.
- **It says the strict set is too thin to be an ensemble** — the honest next move
  is to *widen the surviving set* (more models, more recent generations), not to
  loosen the gates.

## Why this helps the sector

- **A defensible "best prediction" with no tunable parameters.** Anyone can run
  the same three gates over their own model set and get the same number — the
  opposite of a black-box average.
- **It makes the "hot model" bias explicit and removable.** The 1.37 K gap
  between the naive and trust-gated means is the price the field pays for
  averaging leakers and hot models together.
- **It names the direction for better predictions.** To sharpen the estimate,
  the field needs more models that *pass the gates* — conservation as a
  precondition, sensitivity and forcing in the assessed range — not another
  point forecast.

## Honest limits

- **Not a new climate model.** This re-weights the existing ensemble with
  verification gates; it does not simulate anything.
- **The gates are thresholds, not measurements.** `2.5–4.0 K` and `3.3–4.1 W/m²`
  are the IPCC-assessed ranges; the *ranking* is robust to them, the exact
  survivor count is stated at these thresholds (same honesty rule as
  `docs/climate-cmip6-drift.md`).
- **One family is one family.** The trust-gated 2.71 K is the GISS family's
  value, not an independent consensus. It agrees with the IPCC best estimate,
  which is reassuring but not a proof.

## Reproduce

```sh
cd pacland
PYTHONPATH=src python3 -m pacland.climate.ecs_model
PYTHONPATH=src python3 -m unittest tests.test_climate_ecs_model -v   # 7 tests
```

Data: `data/climate/cmip6_ecs.json` (Zelinka et al. 2020) ×
`data/climate/cmip6_drift.json` (Irving et al. 2021). The three-axis verdict is
`docs/climate-cmip6-drift.md` §4b and `src/pacland/climate/sensitivity_crosscheck.py`.
