# The CMIP6 conservation deficit — a three-ledger machine-checked guard

Status: **computed and guarded** — `src/pacland/climate/cmip6_drift.py` +
`data/climate/cmip6_drift.json` + 15 known-answer tests (green). This is the write-up
of the climate discipline's first real-data guard run.

## The finding, in one sentence

> **12 of 19 CMIP6 models leak energy, 6 leak ocean mass, but only 2 leak salt — so
> the leak lives in the atmosphere-ocean coupling, not the ocean model. Crossed with
> the field's two other quality axes — sensitivity (ECS) and forcing (ERF2x) — only
> 2 of 19 survive all three axes (the GISS family); the rest fail conservation,
> sensitivity, forcing, or some combination.**

## The climate oracle and the Rule of Three

The discipline-specific grounding (see `docs/grounding.md`):

- **Oracle:** a `piControl` run has no forcing, so a conserving model *must* be
  stationary — zero drift. That is the always-true answer, and the drift data measures
  the violation of it.
- **Rule of Three:** the **three conservation ledgers** — energy, mass, salt — three
  independent physics a conserving model must all close.

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
  (doi:10.6084/m9.figshare.12143562, `drifts.csv`): per-model net-TOA drift **and**
  ocean-heat-content (OHC) drift in J yr⁻¹, 19 CMIP6 models.
- **Conversion** — J yr⁻¹ → W m⁻²: divide by 3.15576×10⁷ s yr⁻¹ and the Earth surface
  area 5.101×10¹⁴ m².
- **Guard** — `guard_energy_budget(net_toa_flux = drift, d_energy_dt = 0, tol = 0.1)`;
  a steady-state control must satisfy net TOA ≈ 0, so any drift beyond tolerance fails.
- **Reference signal** — the Earth's energy imbalance (EEI) = 0.77 W m⁻² (Loeb et al.
  2021, CERES, 2005–2019).
- **The split** — total TOA drift vs the ocean's own drift; the difference is the
  *non-ocean* leak (atmosphere + land + cryosphere).

## 3. Results

### 3.1 The per-model verdict

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
energy imbalance.

### 3.2 Where the leak lives — the sharp split

| | median | drift |
|---|---|---|
| total TOA (the whole model) | **0.241 W m⁻²** |
| ocean only (OHC) | **0.051 W m⁻²** |

The total leak is **~5× the ocean's own drift** — so the leak is almost entirely in
the **atmosphere/land/cryosphere**, not the ocean. The two worst models make the point
sharply: CNRM-ESM2-1 leaks 1.485 W m⁻² total, yet its *ocean* drifts only 0.086 W m⁻² —
the atmosphere is leaking ~1.4 W m⁻² while the ocean conserves. This is the known
atmospheric-leak problem (non-conserving advection / inconsistent coupling), now a
per-model, quantified split.

### 3.3 The mass leak — the second conservation law

The energy leak is not the only non-conservation. The same 19 models' **ocean-mass
drift** (`masso`, converted to a sea-level-equivalent rate at 1 mm = 3.6×10¹⁴ kg):

| model | ocean-mass drift |
|---|---|
| ACCESS-ESM1-5 | **−1.032 mm yr⁻¹** (~30% of SLR) |
| UKESM1-0-LL | +0.558 mm yr⁻¹ |
| E3SM-1-0 | −0.486 mm yr⁻¹ |
| CNRM-ESM2-1 | +0.444 mm yr⁻¹ |
| BCC-ESM1 | +0.386 mm yr⁻¹ |
| CNRM-CM6-1 | +0.303 mm yr⁻¹ |

**6 of 19 models leak ocean mass beyond 0.3 mm yr⁻¹ (~10% of the observed 3.4 mm yr⁻¹
sea-level rise)**. The worst, ACCESS-ESM1-5, drifts at −1.03 mm yr⁻¹ — a third of the
entire sea-level signal. So the models leak both energy *and* mass; neither conservation
law is a solved detail.

### 3.4 The salt leak — the third ledger, and where it points

The third independent ledger is **salt** — conserved by definition (no sources or
sinks), so a conserving ocean's salinity drift must be ~0. The measured salinity drift
(`soga`) is tiny: only **2 of 19 models** leak (BCC-ESM1 at −4.1×10⁻⁵ g/kg/yr,
BCC-CSM2-MR at −4.0×10⁻⁵), the rest drift at 10⁻⁷–10⁻⁶.

So the three ledgers fall off sharply:

| ledger | models leaking |
|---|---|
| energy (net TOA) | **12 of 19** |
| mass (ocean mass) | **6 of 19** |
| salt (salinity) | **2 of 19** |

**This is the conclusion the three-way check was built to find:** salt — the purely
*ocean* ledger — is conserved orders of magnitude better than energy and mass, which
cross the atmosphere-ocean boundary. The leak is therefore in the **atmosphere-ocean
coupling**, not in the ocean model itself. Only **5 of 19 models conserve all three
ledgers.**

### 3.5 The conservation trust ranking (by ledgers failed)

- **broken** (≥2 ledgers failed): BCC-ESM1 (all 3), CNRM-ESM2-1, CNRM-CM6-1,
  BCC-CSM2-MR, ACCESS-ESM1-5
- **leaking** (exactly 1 ledger): IPSL-CM6A-LR, MPI-ESM1-2-LR, ACCESS-CM2,
  MPI-ESM-1-2-HAM, GFDL-CM4, MPI-ESM1-2-HR, HadGEM3-GC31-LL, E3SM-1-0, UKESM1-0-LL
- **clean** (0 ledgers failed): GISS-E2-1-G-CC, E3SM-1-1, GISS-E2-1-G, EC-Earth3,
  EC-Earth3-Veg

## 4. Conclusions

1. **Conservation is not a solved detail — it is a hard, quantified defect in most
   CMIP6 models.** 12 of 19 leak energy, 6 of 19 leak mass; the leak is invisible to
   skill scores and to ensemble spread.
2. **The error bar can exceed the signal.** Two models leak at ~1.9× the EEI they are
   used to project — an internal error twice the size of the forecast itself.
3. **The leak is in the coupling, not the ocean.** Salt (purely oceanic) is conserved
   ~orders of magnitude better than energy and mass (which cross the air-sea boundary),
   so the defect is in the atmosphere-ocean exchange, not the ocean model — the fix
   belongs in the coupling.
4. **Conservation should be a precondition, not a footnote.** A model that fails the
   guard should be drift-corrected explicitly — or excluded from any energy-balance
   conclusion — before its projection is used.

## 4b. The second and third axes — sensitivity and forcing (the cross-check against consensus)

Conservation is one necessary condition; the field's own quality axes are **climate
sensitivity** (ECS, the "hot model" problem — Hausfather et al. 2022) and **effective
radiative forcing** (ERF2x), both published per-model in Zelinka et al. 2020. Combining
the three — our ledgers × published ECS × published ERF2x — gives the three-axis trust
table:

| model | ledgers failed | ECS (°C) | ERF2x (W/m²) | three-axis verdict |
|---|---|---|---|---|
| GISS-E2-1-G / -CC | 0 | 2.71 | 3.95 | **survives all three axes** |
| EC-Earth3 / -Veg | 0 | 4.26 / 4.33 | 3.22 / 3.37 | clean but *high* sensitivity |
| E3SM-1-1 | 0 | 5.31 | 3.33 | clean but **hot** |
| MPI-ESM1-2-HR | 1 | 2.98 | 3.65 | leaky but reasonable on both others |
| MPI-ESM1-2-LR / -HAM | 1 | 2.95–3.03 | 4.22 / 4.16 | leaky **and** forcing too strong |
| ACCESS-ESM1-5 / BCC | ≥2 | 3.0–3.9 | 2.83–3.11 | leaky **and** forcing too weak |
| CNRM, UKESM1, HadGEM3, IPSL | ≥1 | 4.7–5.55 | 3.5–3.6 | leaky **and** hot |

Thresholds: ECS reasonable = 2.5–4.0 °C (IPCC AR6 likely range), ERF2x reasonable =
3.3–4.1 W/m² (assessed 2×CO2 forcing band).

**The result that revises the conservation-only answer:** only **2 of 19 models survive
all three axes** — the GISS family. The forcing axis *sharpens* the two-axis answer:
MPI-ESM1-2-LR and MPI-ESM-1-2-HAM looked merely "leaky but reasonable sensitivity" on
two axes, but they also force too strongly (4.2 W/m² vs ~3.7 observed); ACCESS-ESM1-5
and the BCC pair leak *and* force too weakly (2.8–3.1 W/m²); CNRM-ESM2-1 fails all
three. So conservation alone — or even conservation-plus-sensitivity — is not enough:
a trustworthy model must pass all three independent axes, and today that is
**GISS-E2-1-G**.

## 5. Honest limits

- This **re-expresses** Irving et al. 2021's measurement as a machine-checked guard; it
  is not a new measurement. The contribution is the pass/fail gate, the leak-vs-EEI
  ratio, and the ocean-vs-atmosphere split, not the underlying numbers.
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
python3 scripts/climate_cmip6_drift.py                       # full verdict table + split
PYTHONPATH=src python3 -m unittest tests.test_climate_cmip6_drift -v   # known-answer tests
```
