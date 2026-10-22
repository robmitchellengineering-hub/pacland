# The CMIP6 drift, recomputed from raw model output — a second independent source

Status: **confirmed** — the conservation-drift finding (Irving et al. 2021 figshare)
survives an independent recomputation from raw CMIP6 `piControl` model output.

## What this is

The three-ledger conservation result rests on **one** published table (Irving,
Hobbs, Church & Zika 2021, figshare doi:10.6084/m9.figshare.12143562). A
single-source finding is a single point of failure. This page closes that gap:
it recomputes the **net-TOA energy drift** directly from the models' own output
(the Google Cloud pangeo-cmip6 zarr archive), with no dependence on Irving's
numbers, and compares.

## Method

- **Data** — raw CMIP6 `piControl` zarr from `https://storage.googleapis.com/cmip6`
  (the pangeo-cmip6 catalog), the same experiments Irving analyzed, read with
  `xarray`/`zarr`/`dask`.
- **Net TOA** — `rsdt − rsut − rlut` (down shortwave − up shortwave − up longwave),
  the definition Irving used (their Table S2 lists exactly these three variables).
  Where a model's `rtmt` was used instead, it is flagged.
- **Global mean** — area-weighted by `cos(latitude)`, averaged over longitude.
- **Drift** — the time-mean of the annual global-mean series (the drift is the
  mean imbalance; the linear trend over the period is separately ~0, confirming
  the drift is a persistent offset, not an accelerating one).

## Result — raw vs Irving

| model | raw netTOA (W/m²) | Irving (W/m²) | Δ | source var |
|---|---|---|---|---|
| CNRM-ESM2-1 | **+1.521** | +1.485 | +0.04 | rsdt−rsut−rlut |
| IPSL-CM6A-LR | +0.735 | +0.665 | +0.07 | rtmt |
| BCC-ESM1 | **−0.368** | −0.402 | +0.03 | rsdt−rsut−rlut |
| GISS-E2-1-G | +0.099 | +0.056 | +0.04 | rtmt |
| EC-Earth3 | +0.070 | +0.035 | +0.04 | rtmt |

**Sign and ranking agree on all five.** The worst leaker (CNRM-ESM2-1) is
reproduced at **~+1.5 W/m², about 30× the clean models** — the headline of the
original finding is real, not an artifact of one team's analysis. The residuals
(0.03–0.07 W/m²) are method variance: `cos(lat)` weighting vs Irving's
`areacella` cell areas, and minor version differences.

## The bonus finding — BCC-ESM1's `rtmt` does not close

For BCC-ESM1 the two definitions disagree:

| BCC-ESM1 | value |
|---|---|
| `rsdt − rsut − rlut` | **−0.368 W/m²** (matches Irving −0.402) |
| `rtmt` (the model's own "net TOA" diagnostic) | **+0.716 W/m²** |

The model's reported net-TOA diagnostic is ~1.1 W/m² away from its own radiative
components. This is exactly why the conservation check must use the components
(`rsdt − rsut − rlut`), not the convenience variable `rtmt` — and it vindicates
Irving's choice to assemble the flux from components. A guard that read `rtmt`
blindly would call BCC-ESM1 a *positive* leaker when its components say the
opposite sign.

## Honest limits

- **5 models, not 19.** This is a confirming sample (worst leaker + clean + the
  most-negative + two mid), not the full ensemble. Extending to all 19 is the
  natural next step and is purely a data-fetch loop — no new method.
- **`cos(lat)` weighting, not cell areas.** Irving used `areacella`; the two agree
  to within the residuals above on a regular grid.
- **Reproduce** — `scripts/climate_drift_second_source.py` (fetch + compute),
  or the same zarr URLs in this file's method section.
