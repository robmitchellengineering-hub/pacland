# SCREAM — the oracle behind STRATA: does *it* leak?

Status: **computed and guarded** — `src/pacland/climate/scream_conservation.py` +
`tests/test_climate_scream_conservation.py` (12 tests, green). This closes the
term the STRATA report left open: STRATA is verified against SCREAM
(reference-fidelity, `p̂_g`); this asks the next level, **is the oracle itself
right against the Earth** (`p̂_e`).

## The answer, in one sentence

> **SCREAM does not leak energy in the CMIP6 drift sense — its physics enforces
> energy conservation (a built-in fixer), and its parent lineage (E3SM) is
> verified among the cleanest of 19 CMIP6 models. But it leaks *mass* in the
> parent lineage, and the two numbers that would settle the km-scale question —
> the fixer's magnitude and a long-run drift — are not published, so they are
> UNKNOWN, not clean.**

## Evidence, from three primary sources

**1. The parent lineage is measured clean on energy** (`data/climate/cmip6_drift.json`,
Irving et al. 2021). E3SM-1-0 and E3SM-1-1 carry the atmosphere physics SCREAM
inherits. Recomputed from the repo's own data:

| model | net-TOA drift | ocean-mass drift | ledgers failed |
|---|---|---|---|
| E3SM-1-0 | **−0.023 W/m²** | **−0.486 mm/yr** (leaks) | 1 (mass) |
| E3SM-1-1 | **−0.068 W/m²** | +0.080 mm/yr | 0 |

Against the observed Earth energy imbalance (**0.77 W/m²**, Loeb 2021 CERES) and
the worst CMIP6 leaker (**+1.49 W/m²**, CNRM-ESM2-1), E3SM's energy drift is
30–65× cleaner than the worst and 11–33× smaller than EEI.

**2. SCREAM's physics *enforces* energy conservation** — primary source,
[`check_energy.F90`](https://github.com/E3SM-Project/scream/blob/master/components/eam/src/physics/cam/check_energy.F90)
in the E3SM-Project/scream repository. It checks column total-energy to **1e-14**
relative error and water to **1e-10**, and it runs an **energy fixer** — verbatim:
*"add a globally uniform heating term to account for any change of total
energy."* The global energy budget is forced closed every physics step.

**3. The wall.** The STRATA-published data cannot independently re-measure the
km-scale drift: the [HuggingFace Zarr](https://huggingface.co/datasets/nvidia/STRATA-SCREAM-sdecadal)
is subsampled to 14 emulator variables (no radiation), the raw output is ~33 TB
on [NERSC tape](https://portal.nersc.gov/archive/home/n/ndk/www/STRATA2026), and
the runs are 17-day forced (not `piControl`), so the CMIP6 drift oracle — "no
forcing ⇒ zero drift" — does not transfer.

## The two honest gaps (what "no leak" does *not* mean)

1. **The fixer hides the raw error.** The fixer *corrects* the global imbalance
   every step; its magnitude *is* the raw physics energy error. That number is
   not in the published output, so "enforced" is not the same as "the raw
   physics conserves."
2. **Nonhydrostatic energy conservation is an open question.** SCREAM's km-scale
   core is nonhydrostatic; energy-conserving nonhydrostatic physics is an active
   research area ([GMD 17, 1429, 2024](https://gmd.copernicus.org/articles/17/1429/2024/)).
   And the parent lineage *does* leak mass (E3SM-1-0: −0.486 mm/yr).

## Why this matters for the STRATA finding

STRATA's reference-fidelity is fidelity to SCREAM. This module shows SCREAM is a
*good* oracle on energy — enforced and lineage-clean — so STRATA's reference is
not a leaky one on the energy axis. The residual risk is elsewhere: the fixer's
hidden magnitude, the mass ledger, and the nonhydrostatic core — none of which
STRATA's released output can expose, because STRATA drops the fluxes entirely.

## Reproduce

```sh
cd pacland
PYTHONPATH=src python3 -m pacland.climate.scream_conservation        # the summary block
PYTHONPATH=src python3 -m unittest tests.test_climate_scream_conservation -v   # 12 tests
```

References: Irving et al. 2021 (figshare doi:10.6084/m9.figshare.12143562);
Loeb et al. 2021 (CERES EEI, GRL 48, e2021GL093047);
[`check_energy.F90`](https://github.com/E3SM-Project/scream/blob/master/components/eam/src/physics/cam/check_energy.F90);
GMD 17, 1429–1442, 2024 (nonhydrostatic energy-conserving physics).
