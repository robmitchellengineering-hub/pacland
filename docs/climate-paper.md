# Conservation is the only exact content: a verification layer for climate models

**Rob Mitchell** · PACLAND · climate discipline

**Status:** draft for publication (Zenodo, CC BY 4.0, as the physics paper is).

---

## Abstract

Climate projections are the most consequential predictions we make, and the field
has no verification layer that distinguishes a *verified* projection from an
*extrapolated* one. We apply the PACLAND verification discipline — the two-level
certificate, the verification deficit, and the constraint-first decomposition — to
the CMIP6 ensemble. Three results. **(1) The leak:** 12 of 19 models fail a
three-ledger conservation guard (energy, mass, salt), and the leak is localized
to the atmosphere–ocean coupling, not the ocean. **(2) The fix:** drift-correction
— the field's own post-processing repair — restores conservation in every model
(12 → 0 failures), but a retrospective test against HadCRUT5 shows it does *not*
fix the temperature bias; that bias comes from sensitivity, and the
sensitivity+forcing gate fixes it (ensemble ECS 3.78 → 3.08 K, matching the
observed 3.0 K). **(3) The theorem:** conservation is the *only* exact,
model-independent content of a climate model — the climate analog of the flux
tadpole — and every predictive quantity (ECS, forcing, the 2100 warming) is a
model-dependent range, not an exact observable. The verification deficit climbs
to **m = 7** (4 empirical observables + 3 exact conservation ledgers) and is
**saturated**: the constraint contribution is capped at 3, exactly as the flux
sector is capped at the tadpole.

## 1. The verification deficit, applied to climate

The deficit counts observables that are simultaneously *measured, computable, and
validated*. On the historical record, **m = 4** (GMST, EEI, OHC, GMSL — a ≈68%
certificate radius). The 2100 projection has **m = 0** — no future state is
measured, so the projection is extrapolation, not verification.

## 2. The leak — three conservation ledgers

A conserving model must close three independent ledgers in its control run:
**energy** (net top-of-atmosphere flux ≈ 0), **mass** (ocean mass ≈ 0), **salt**
(salinity drift ≈ 0). Measured (Irving et al. 2021, 19 models): **12 leak energy,
6 leak mass, 2 leak salt**. Salt — the purely-ocean ledger — is conserved orders
of magnitude better than energy and mass, which cross the air–sea boundary; the
leak therefore lives in the **atmosphere–ocean coupling**, not the ocean model.
The worst model (CNRM-ESM2-1) leaks at ~1.9× the Earth's energy imbalance.

## 3. The fix — drift-correction

The field's own repair is drift-correction: subtract the measured leak. Applied to
all 19 models, **every model conserves by construction** (12 → 0 failures). But a
retrospective test against HadCRUT5 (HadGEM3-GC31-LL, historical + piControl)
shows the correction does **not** improve the temperature match (RMSE 0.27 → 0.29 K;
end warming +1.92 vs +0.93 K observed). The reason is stated, not hidden:
HadGEM3's ~1 K over-warming comes from its *sensitivity* (a "hot" model), not its
conservation drift (0.02 K/century). Two tools, two jobs: drift-correction fixes
**conservation**; the sensitivity+forcing gate fixes the **temperature bias**
(ensemble ECS 3.78 → 3.08 K, matching the observed 3.0 K). Three independent
observational sources agree: Sherwood et al. 2020 (ECS), HadCRUT5 (temperature),
Loeb et al. 2021 (EEI).

## 4. The Climate Constraint-First Theorem

> **The only exact, model-independent content of a climate model is its
> conservation laws (energy, mass, salt). Every predictive quantity — ECS,
> forcing, the 2100 warming — is a model-dependent range, not an exact
> observable.**

Arm A (exact): conservation is an identity, not an approximation — a model that
does not close the ledgers is broken, not "approximately wrong". Arm B
(non-exact): the 53 CMIP6 models span ECS 1.83–5.64 K (a range, not a value); any
two disagreeing models falsify "ECS is exact"; the projection has m = 0. This is
the climate instance of the one spine: *"don't ask a complex system for its values
— ask for its constraints."*

## 5. The deficit, climbed and capped

**m = 7** — 4 empirical observables + 3 exact conservation ledgers — with the
ceiling proved by the theorem: conservation is the only exact content, so the
constraint contribution is **saturated at 3**, exactly as the flux sector is
saturated at 1 (the tadpole). Further deficit growth is empirical only.

## Reproduce

```
PYTHONPATH=src python3 scripts/validate_climate_constraint_first.py
PYTHONPATH=src python3 -m pacland.climate.drift_correction
PYTHONPATH=src python3 scripts/climate_retrospective.py
PYTHONPATH=src python3 scripts/make_site.py
```

Code: `src/pacland/climate/` · data: `data/climate/` · 303 tests green.
