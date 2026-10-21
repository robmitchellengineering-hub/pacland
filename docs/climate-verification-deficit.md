# Climate verification deficit — the first climate report (playbook item #1)

Status: **computed and guarded** — `src/pacland/climate/` + `tests/test_climate_deficit.py`
(3 tests, green). The reusable pacland machinery (`certificate.py`, `deficit.py`) is
imported unchanged; this file records the climate result and its honest limits.

## The headline, in one sentence

> **A climate model's fit to the observed past is certified only to ~68% tolerance over
> `m = 4` observables — and its 2100 projection is, strictly, extrapolation, not
> verification, because no future state is measured.**

## The two-tier structure (why the projection is the weak spot)

The deficit's honest rule (pacland's own V2 correction, restated): a *validation point*
needs the model output `O(x)` **and** an independent observation `c*(x)` on the **same**
state `x`. For the future that pairing never exists — so:

| tier | what it covers | `m` | certificate radius (δ = 0.025) |
|---|---|---|---|
| **historical record** | observables the model reproduces against real observations | **4 of 12** | **0.679 (~68%)** |
| **projection targets** | the 2100 quantities policy actually consumes | **0 of 5** | **∞ (vacuous)** |

`radius = sqrt(ln(1/δ) / (2m))`. At `m = 4` that is `sqrt(ln 40 / 8) ≈ 0.679`. To reach a
1% certificate you need `m ≈ 18,000` simultaneously-measured+computable+validated
observables — three orders of magnitude beyond what the historical record can supply.
Contrast: the string-theory SM floor was `m = 19` → ~31%; climate's *past* is weaker, and
its *future* is total.

## The m-count (what actually counts)

The four that count toward `m` (measured + computable + validated on the record):

| observable | measured by | status |
|---|---|---|
| GMST | HadCRUT5 / GISTEMP / Berkeley Earth | ✅ validated |
| EEI (TOA energy imbalance) | CERES (+ Argo) | ✅ validated |
| OHC (0–2000 m) | Argo (+ GRACE/altimetry) | ✅ validated |
| GMSL | tide gauges + satellite altimetry | ✅ validated (ice-sheet term partial) |

Everything else is measured + computable but **not** validated (Arctic sea ice — models
*underestimate* the decline; AMOC — short record; ENSO — realism varies; precip, ice
sheets, extremes — known biases), so it contributes nothing to the certificate today.
The full set is `src/pacland/climate/observables.py`.

## The ACE worked example — "reference-fidelity ≠ reality-fidelity"

The two-level certificate is `p_* ≤ p̂_g + p̂_e + radius_s + radius_e`, where:
- `p̂_g` = **candidate-vs-oracle** (the model vs its reference), and
- `p̂_e` = **oracle-vs-truth** (the reference vs the Earth).

ACE (AI2 Climate Emulator, [arXiv:2310.02074](https://arxiv.org/abs/2310.02074)) is
"verified" as *fidelity to a reference GCM* (FV3GFS) over ">90% of tracked variables" —
that is `p̂_g` alone. The `p̂_e` term — is the *reference GCM itself* right against the
Earth? — is never computed, and for a 100-year projection it **cannot** be, because the
Earth's future is the missing `c*`. So today's headline "verification" of a climate
emulator certifies a model against *another model*, not against the Earth. That is the
sentence the deficit makes rigorous.

## Honest limits (so this never overclaims)

- **"validated" ≠ "validated for the future."** It means "reproduces the historical
  record within the observed/ensemble spread." The projection is a different claim with
  no ground truth, and the deficit is precisely the *statement of that gap*.
- **`m = 4` is the optimistic count.** Even the four are not equally clean (GMSL's
  ice-sheet term, EEI's 0.7–1.0 W/m² spread). Tightening `m` downward makes the number
  *worse*, not better — so the 68% is a ceiling on certifiability, not a floor on doubt.
- **This is a characterisation, not a prediction.** It says "you are here," not "here is
  the answer." Same honesty rule as pacland v1.
- **The constraint side is not yet counted.** Irving et al. 2021's CMIP6 mass/energy
  drift (`docs/climate-gap-analysis.md` §6) is the raw material for the *guard-suite*
  (the next build) — a per-model conservation-violation scalar, which is a different
  object from this observable deficit.

## Reproduce

```
cd pacland && PYTHONPATH=src python3 -m pacland.climate.deficit
PYTHONPATH=src python3 -m unittest tests.test_climate_deficit -v
```
