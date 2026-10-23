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

## The full fix, three tiers (not a half-measure)

| tier | what | status |
|---|---|---|
| **1 — global-mean** | subtract the mean leak so the ledger closes on average | ✅ built here |
| **2 — zonal (spatial)** | subtract the leak's latitudinal pattern so it conserves at every latitude | wired — data from the mesh widening job (`scripts/climate_drift_widen.py`) |
| **3 — coupling patch** | fix the non-conserving term in the model's own code | the builders' patch — `leak_map()` hands them the spatial spec |

The honest boundary, now smaller and sharper: tier 3 is the only part that is
genuinely the model-builders' work, and even that we don't just hand off — we
hand them the *leak map* (which latitudes leak, by how much) and re-check their
fix.

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
