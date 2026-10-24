# Climate Constraint-First Theorem — the only exact content is conservation

The climate analog of the physics tower. Physics: the only exact structure in
the flux landscape is the **constraint** (the tadpole FᵀJH — the unique
invariant), and every other observable (W₀, masses, g_s) is non-exact noise.
Climate: the only exact, model-independent content of a climate model is
**conservation** — and every predictive quantity (ECS, forcing, the 2100
warming) is a model-dependent range, not an exact observable.

Reproduce: `PYTHONPATH=src python3 scripts/validate_climate_constraint_first.py`.

## Arm A — conservation is exact (the climate "tadpole")

A model must close three ledgers: **energy** (First Law), **mass** (continuity),
**salt** (tracer conservation). These are *identities*, not approximations — a
model that does not close them is not "approximately wrong", it is **broken**.
The measured drift proves the point: **14 of 19 models leak**, and the worst
(CNRM-ESM2-1, +1.48 W/m²) leaks at ~1.9× the Earth's energy-imbalance signal —
the violation is the *size of the projection*, not a rounding error.

So conservation is the exact, always-true constraint — exactly as the tadpole is
the exact, always-true invariant in the flux sector.

## Arm B — predictions are not exact (the climate "W₀")

The 53 CMIP6 models span **ECS 1.83–5.64 K**. A range, not a value — so no
single exact ECS exists; any two disagreeing models falsify "ECS is exact".
The 2100 projection has **m = 0** (no future state measured) — extrapolation,
not an exact observable.

So ECS, forcing, and the projection are model-dependent — non-exact, exactly as
W₀ and the mass spectrum are non-exact in the flux sector.

## The deficit consequence — m = 7, with a proven ceiling

The physics deficit counts empirical observables *plus* the exact constraint
(topology 4 + tadpole 1 + SM 4 = 9). The climate mirror: **4 empirical
observables (GMST, EEI, OHC, GMSL) + 3 exact conservation ledgers = m = 7**
(`conservation_deficit()` in `drift_correction.py`).

The ceiling is proved by the theorem itself: conservation is the **only** exact
content, so the constraint contribution to m is **capped at 3** — exactly as the
flux sector is capped at 1 (the tadpole). Further deficit growth is empirical
observables only, never new exact constraints.

## What this means for the verification layer

The verification layer gates on the **exact** thing (conservation) and brackets
the **non-exact** thing (ECS), exactly as the physics gates on the tadpole and
brackets W₀:

| | exact (the constraint) | non-exact (the range) |
|---|---|---|
| **physics** | tadpole FᵀJH — gate on it | W₀, masses — bracket them |
| **climate** | conservation (3 ledgers) — gate on it | ECS 2.5–4.0 K, forcing — bracket them |

That is the climate arm of the one spine: **"don't ask a complex system for its
values — ask for its constraints."**
