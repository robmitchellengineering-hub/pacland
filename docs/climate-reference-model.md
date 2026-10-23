# The verified reference model — GISS-E2-1-G

Status: **computed and guarded** — `src/pacland/climate/reference_model.py` +
`tests/test_climate_reference_model.py` (9 tests, green).

## The finding, in one sentence

> **Of 19 CMIP6 models with full conservation data, exactly one passes all three
> verification gates — GISS-E2-1-G — and its ECS, 2.71 K, is the single-model
> best prediction: the number from the one model we can fully verify.**

## Why this model, and not the ensemble

The three gates are conservation (energy + mass + salt), sensitivity (ECS inside
2.5–4.0 K), and forcing (ERF2x inside 3.3–4.1 W/m²). Only GISS-E2-1-G — and its
variant GISS-E2-1-G-CC — survives all three:

| fact | value |
|---|---|
| axes passed | **3/3** |
| ECS | **2.71 K** |
| ERF2x | 3.95 W/m² |
| conservation | 0 ledgers leaked |

The wider 15-model gate gives 3.08 K, and the IPCC best estimate is ~3.0 K.
GISS's 2.71 K sits inside the same likely range, reached by the *strictest*
possible gate — the single most-defensible number in the whole ensemble.

## What "use the stable variant" means here

The model's prediction is its **sensitivity** (2.71 K per CO₂ doubling) — the
physics it actually predicts. The 2100 warming is sensitivity **× the forcing
pathway**, and the pathway is a *scenario input* (a label), not a model output.
So the verified reference model pins the physics; the scenario is chosen by the
question you ask.

## Its own 2100 projection (Nazarenko et al. 2022)

The model's own SSP runs ([Nazarenko et al. 2022](https://doi.org/10.1029/2021MS002871),
JAMES 14, e2021MS002871) give the verified model's answer to "how bad does it
get", by 2100 relative to 1850–1880:

| scenario | 2100 warming |
|---|---|
| **SSP5-8.5** (high emissions) | **4.6–5.2 °C** |
| SSP1-2.6 (strong mitigation) | below 2 °C (one variant 2.2 °C) |
| SSP1-1.9 (aggressive mitigation) | below 2 °C |

**Note the ECS method-dependence, stated rather than hidden:** the model's own
paper reports its effective sensitivity as **2.9–3.0 °C**, while our gate uses
Zelinka's cross-model-consistent **2.71 K**. Both sit inside the IPCC likely
range; the gap is estimation method (the Gregory regression vs the model's own
2×CO₂ run), not an error.

## Honest limits

- **One family is one family.** GISS-E2-1-G's 2.71 K is a single model's value,
  not an independent consensus — its agreement with the IPCC best estimate is
  reassuring, not a proof.
- **The gate is strict by design.** It collapses 19 models to one because the
  other 18 fail at least one of conservation, sensitivity, or forcing. That is
  the point: the reference model is the one that does not fail.
- **This is a characterisation of the model, not a re-run.** No GISS simulation
  was performed; the verdict is assembled from Irving 2021 (drift) and Zelinka
  2020 (ECS/ERF2x).

## Reproduce

```sh
cd pacland
PYTHONPATH=src python3 -m pacland.climate.reference_model
PYTHONPATH=src python3 -m unittest tests.test_climate_reference_model -v   # 9 tests
```

Data: `data/climate/cmip6_drift.json` (Irving 2021) × `data/climate/cmip6_ecs.json`
(Zelinka 2020). The three-axis verdict is `src/pacland/climate/sensitivity_crosscheck.py`.
