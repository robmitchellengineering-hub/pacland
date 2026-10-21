# The CMIP6 conservation deficit — a machine-checked guard on model energy drift

Status: **computed and guarded** — `src/pacland/climate/cmip6_drift.py` +
`data/climate/cmip6_drift.json` + 5 known-answer tests (green). This is the write-up
of the climate discipline's first real-data guard run.

## The finding, in one sentence

> **12 of 19 CMIP6 models fail a machine-checked energy-conservation guard, and two of
> them — CNRM-ESM2-1 and CNRM-CM6-1 — leak energy at ~1.9× the Earth's own energy
> imbalance.**

## 1. Why conservation is the first thing to check

A coupled climate model is a numerical solution of conservation laws (energy, mass,
momentum, salt). If a model does not conserve energy, its physics cannot be right no
matter how well it reproduces any single observable — a leak is not a bias to tune
away, it is energy being created or destroyed by the numerics. The cleanest place to
measure conservation is the **pre-industrial control** run (`piControl`): in steady
state, the net top-of-atmosphere (TOA) radiative flux must be **zero** — energy in
equals energy out. A non-zero drift is the leak.

Irving, Hobbs, Church & Zika (2021) measured exactly this across CMIP6 and concluded
that *"model drift tends to be even larger in net top-of-atmosphere radiation,
indicating a loss (or 'leakage') of heat in the coupled climate system."* That finding
lives in a paper. Here it is a **guard**: a pass/fail test a model's raw output must
satisfy, with the leak quantified against a reference signal.

## 2. Method

- **Data** — the open figshare release of Irving et al. 2021
  (doi:10.6084/m9.figshare.12143562, `drifts.csv`): per-model net-TOA drift in J yr⁻¹,
  19 CMIP6 models.
- **Conversion** — J yr⁻¹ → W m⁻²: divide by 3.15576×10⁷ s yr⁻¹ and the Earth surface
  area 5.101×10¹⁴ m².
- **Guard** — `guard_energy_budget(net_toa_flux = drift, d_energy_dt = 0, tol = 0.1)`;
  a steady-state control must satisfy net TOA ≈ 0, so any drift beyond tolerance fails.
- **Reference signal** — the Earth's energy imbalance (EEI) = 0.77 W m⁻² (Loeb et al.
  2021, CERES, 2005–2019).

## 3. Results — the per-model verdict

| model | institution | net-TOA drift (W m⁻²) | guard | vs EEI |
|---|---|---|---|---|
| CNRM-ESM2-1 | CNRM-CERFACS | **+1.485** | ❌ FAIL | **1.93×** |
| CNRM-CM6-1 | CNRM-CERFACS | **+1.460** | ❌ FAIL | **1.90×** |
| IPSL-CM6A-LR | IPSL | +0.665 | ❌ FAIL | 0.86× |
| BCC-CSM2-MR | BCC | −0.544 | ❌ FAIL | 0.71× |
| MPI-ESM1-2-LR | MPI-M | +0.421 | ❌ FAIL | 0.55× |
| BCC-ESM1 | BCC | −0.402 | ❌ FAIL | 0.52× |
| ACCESS-CM2 | CSIRO | +0.368 | ❌ FAIL | 0.48× |
| MPI-ESM-1-2-HAM | HAMMOZ | +0.350 | ❌ FAIL | 0.45× |
| ACCESS-ESM1-5 | CSIRO | −0.246 | ❌ FAIL | 0.32× |
| GFDL-CM4 | NOAA-GFDL | +0.241 | ❌ FAIL | 0.31× |
| MPI-ESM1-2-HR | MPI-M | +0.207 | ❌ FAIL | 0.27× |
| HadGEM3-GC31-LL | MOHC | +0.190 | ❌ FAIL | 0.25× |
| GISS-E2-1-G-CC | NASA-GISS | +0.070 | ✅ pass | 0.09× |
| E3SM-1-1 | E3SM | −0.068 | ✅ pass | 0.09× |
| GISS-E2-1-G | NASA-GISS | +0.056 | ✅ pass | 0.07× |
| EC-Earth3 | EC-Earth | +0.035 | ✅ pass | 0.05× |
| E3SM-1-0 | E3SM | −0.023 | ✅ pass | 0.03× |
| UKESM1-0-LL | MOHC | +0.022 | ✅ pass | 0.03× |
| EC-Earth3-Veg | EC-Earth | +0.018 | ✅ pass | 0.02× |

**Headline:** 12 of 19 fail the conservation guard; 2 leak faster than the Earth's
energy imbalance. The seven clean models drift at 0.02–0.07 W m⁻² — an order of
magnitude below the leakers.

## 4. What this means

The kicker is the **leak-vs-signal** comparison. A model projecting the Earth's energy
imbalance (0.77 W m⁻²) while *leaking* 1.5 W m⁻² is carrying an internal error roughly
twice the size of the signal it is asked to forecast. That error is invisible in skill
scores — a drifting model can still reproduce the historical record — and it is not
captured by ensemble spread, which treats every member as equally credible.

Conservation is therefore not a solved detail of CMIP6; it is a **hard, quantified
defect in most models**, and in two of them it exceeds the climate signal itself.

## 5. Honest limits

- This **re-expresses** Irving et al. 2021's measurement as a machine-checked guard; it
  is not a new measurement. The contribution is the pass/fail gate and the
  leak-vs-EEI ratio, not the underlying numbers.
- `tol = 0.1 W m⁻²` is a chosen threshold; the **ranking** is robust to it, the
  12-fail **count** is stated at this threshold.
- The drift is measured in `piControl`. Operational projections **remove** drift in
  post-processing (Irving et al. note improved budget closure after removal), so the
  guard targets the model's *raw* conservation — the defect the post-processing papers
  over — not the published, drift-corrected output.
- The set is 19 CMIP6 models (the subset Irving et al. analyzed), not the full
  ~40-model ensemble.

## 6. Reproduce

```sh
cd pacland
python3 scripts/climate_cmip6_drift.py                       # full verdict table
PYTHONPATH=src python3 -m unittest tests.test_climate_cmip6_drift -v   # known-answer tests
```
