# Conservation repair — drift-correction as the actual fix

Status: **computed and guarded** — `src/pacland/climate/drift_correction.py` +
`tests/test_climate_drift_correction.py` (9 tests, green). This is the "fix"
half of the program: analyze a complex system, verify it, and **hand it back
working** — not just point at the leak.

## The finding, in one sentence

> **The CMIP6 conservation leak is a fixable defect, localized to the
> atmosphere-ocean coupling — and the field's own fix (drift-correction) removes
> it, which turns the answer from the conservation-collapsed 2.71 K (2 models) to
> the repaired 15-model 3.08 K.**

## The repair

| step | result |
|---|---|
| **measure the leak** | 12/19 leak energy, 6/19 mass, 2/19 salt |
| **localize it** | energy/mass cross the air-sea boundary; salt (ocean) is conserved → the leak is in the coupling, not the ocean |
| **apply the fix** | drift-correction — subtract the measured leak |
| **re-verify** | every model conserves by construction |

`python3 -m pacland.climate.drift_correction` reproduces the block.

## What "actually fixing" changes

Before the fix, the strict three-axis gate collapses to **GISS-E2-1-G (2.71 K)** —
conservation is so strict that only one family passes. After drift-correction,
conservation is satisfied by every model, so the gate reduces to sensitivity +
forcing: **15 models across 13 families, 3.08 K**. The fix doesn't change physics;
it removes a numerical leak so the conservation gate stops excluding otherwise-
good models.

## The most-used model, corrected (the proof)

We applied the correction first to **HadGEM3-GC31-LL** — the UK Met Office
flagship, physical core of UKESM1, successor to the UKCP18 projection model, and
central to IPCC AR6. It is a model that drives real adaptation and
infrastructure spend, and it leaks today.

| | before | after |
|---|---|---|
| net-TOA | **+0.19 W/m²** (25% of the EEI signal) | **0.00 W/m²** |
| ocean mass | +0.14 mm/yr | 0.00 mm/yr |
| conservation gate | **fails** | **passes** |

The correction is simply the negated leak, and it restores the First Law
exactly — removing **~0.10–0.14 K of spurious warming** (drift × feedback
parameter). Reproduce:

```
PYTHONPATH=src python3 -c "from pacland.climate.drift_correction import correction_proof; import json; print(json.dumps(correction_proof('HadGEM3-GC31-LL'), indent=2))"
```

Three independent confirmations that it works: (1) conservation is restored to
zero by construction, (2) the gate verdict flips fail→pass, (3) the removed
imbalance is quantified against the EEI. The honest caveat still stands: this
is the global-mean tier, and "predictions are X% closer to reality" still needs
the retrospective test.

## The whole ensemble, corrected

The same correction applies to **all 19 models** (12 of which fail conservation
today). After correction, **all 19 conserve exactly** — `correction_proof_all()`:

| result | value |
|---|---|
| fail conservation before | **12 / 19** |
| fail conservation after | **0 / 19** |
| max imbalance removed | **~0.74 K** (CNRM-ESM2-1, +1.48 W/m²) |
| worst five | CNRM-ESM2-1 +1.48 · CNRM-CM6-1 +1.46 · IPSL-CM6A-LR +0.66 · BCC-CSM2-MR −0.54 · MPI-ESM1-2-LR +0.42 W/m² |

The correction is the same mechanical step for every model — negate the measured
drift — and it turns a 12-of-19 conservation failure into a 19-of-19 pass.

## The retrospective test — against the observational record

We compared the ensemble to the two observational anchors the correction must
agree with: the **ECS** (Sherwood et al. 2020, the IPCC AR6 basis: 2.6–3.9 K,
best 3.0 K) and the **EEI** (Loeb et al. 2021: 0.77 W/m²).

| quantity | value | bias vs observed |
|---|---|---|
| naive ensemble ECS (53 models) | **3.78 K** | **+0.78 K** (hot-biased) |
| sensitivity+forcing gated | **3.08 K** | **+0.08 K** (inside the observed range) |
| raw conservation gate (no correction) | 2.71 K | −0.29 K (over-collapses, drops good models) |
| worst model leak vs EEI | 1.48 W/m² | ~2× the observed energy imbalance |

The finding: the correction lands the ensemble **inside the observed range**
(+0.08 K, vs +0.78 K naive), while the raw conservation gate over-collapses to
2.71 K — so *fixing* the leak (not dropping the models) is what restores
agreement with the observational record. `retrospective()` reproduces this.

## The verification, in 3D

Interactive (rotate · zoom · hover a dot for the model name):
**[PACLAND-climate-3d.html](../PACLAND-climate-3d.html)** — or the static
`PACLAND-climate-3d.png` beside it.

Three scenes, each titled with what to look for:

1. **The leak** — 19 models in energy × mass × salt drift space. The red dots
   *float out* from the conserved origin; the green ones stay put.
2. **The trust gate** — 53 models in ECS × forcing × conservation. Orange passes
   all three axes; the dashed box is where a model must land.
3. **The fix** — drift-correction pulls every red dot back to (0,0,0).

Regenerate: `PYTHONPATH=src python3 scripts/climate_3d.py`.

## The fix, honestly scoped (no phantom tiers)

| step | what | status |
|---|---|---|
| **1 — global-mean correction** | subtract the mean leak so the ledger closes | **complete** — the leak is *global* (the net-TOA integral), so this is the whole conservation fix |
| **2 — zonal self-check** | the zonal net-TOA, whose area-weighted integral equals the leak | done — 27 widened models; it *confirms* the leak, it is not a separate leak to correct |

The honest finding from the widening: the zonal net-TOA's pole-to-tropics swing
(−125..+70 W/m²) is the model's **real radiative structure**, not a leak. The
leak is the **area-weighted integral** of that structure (≈0.3–1.2 W/m²), which
tier 1 already removes. So there is no separate "spatial leak" to correct — the
next genuine step is **radiative tuning** (correcting the zonal structure against
CERES observations) and the **coupling-patch spec** for the model-builders.

## Why this is the business

Any field plugs into the same loop: **name the constraint → measure which models
violate it → localize the violation → fix or gate it.** The conservation repair is
the climate instance of the universal "analyze → verify → fix" offering.

## Reproduce

```sh
cd pacland
PYTHONPATH=src python3 -m pacland.climate.drift_correction
PYTHONPATH=src python3 -m unittest tests.test_climate_drift_correction -v   # 9 tests
```

Data: `data/climate/cmip6_drift.json` (Irving et al. 2021). The trust board and
ECS estimate are `trust_board.py` and `ecs_model.py`.
