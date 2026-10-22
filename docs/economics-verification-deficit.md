# Economics verification deficit — discipline #3 (playbook item #3)

Status: **computed and guarded** — `src/pacland/economics/` + `tests/test_economics_{deficit,guards}.py`
(13 tests, green). The reusable pacland machinery (`certificate.py`, `deficit.py`) is
imported unchanged; this file records the economics result and its honest limits.

## The headline, in one sentence

> **A macroeconomic model's decision surface is validated over only ~4 backcast series
> (`m = 4`, ≈68% radius) — and its policy forecast, the object central banks actually
> act on, is extrapolation, not verification (`m = 0`).**

## The two-tier structure (why the forecast is the weak spot)

Same honest rule as climate and drugs: a *validation point* needs the model output O(x)
**and** an independent measurement c*(x) on the **same** state x. On the observed record
that pairing exists (backcast); for the future there is no measurement yet.

| tier | what it covers | `m` | certificate radius (δ = 0.025) |
|---|---|---|---|
| **retrospective backcast** | series the model reproduces against measured labels | **4 of 10** | **0.679 (~68%)** |
| **prospective forecast** | the projection policy actually acts on | **0 of 5** | **∞ (vacuous)** |

`radius = sqrt(ln(1/δ) / (2m))`; at `m = 4` that is ≈ 0.679. A 1% certificate needs
`m ≈ 18,000` simultaneously-measured series — three orders of magnitude beyond any
macro dataset.

## The m-count

The four that count (measured + computable + validated on the backcast record):

| series | measured by | status |
|---|---|---|
| real GDP growth | national accounts | ✅ validated (in-sample) |
| CPI inflation | national accounts | ✅ validated (in-sample) |
| unemployment rate | labour-force survey | ✅ validated (in-sample) |
| short-term policy rate | central bank | ✅ validated (in-sample) |

The rest — current-account balance, wage growth, productivity, consumption, residential
investment, house prices — are measured + computable but not validated to the same
confidence, so they contribute nothing today. Full set: `src/pacland/economics/observables.py`.

**"Validated" is the honest weak sense.** It means "reproduces the measured series
*in-sample*" — not out-of-sample, which is what a forecast actually is, and where the
field's own record is the failure to beat a random walk.

## The two anchors (from the gap analysis)

- **Meese & Rogoff 1983** (*Journal of International Economics* 14(1–2):3–24) — the
  field's own census: structural exchange-rate models fail to beat a random walk out of
  sample, and later models do not restore the beat. The "validated" forecasts were, in
  large part, in-sample artifacts — so even `m = 4` is the *optimistic* read.
- **Rossi 2013** (*Journal of Economic Literature* 51(4):1063–1119) — the survey
  confirming that exchange-rate predictability is elusive and time-varying; and
  **Gürkaynak, Kısacıkoğlu & Rossi** (CEPR DP 9576) find DSGE models forecast no better
  out-of-sample than simple VARs.

## The accounting guard-suite (the falsification half)

The field already runs national-accounting identities as bookkeeping; the guard-suite
wraps them as pass/fail, mutation-tested checks (`src/pacland/economics/guards.py`):

| guard | what it forbids |
|---|---|
| `guard_circular_flow` | income ≢ expenditure ≢ output (a flow leak) |
| `guard_sectoral_balances` | (S−I)+(T−G)+(M−X) ≠ 0 (sectors that don't sum) |
| `guard_stock_flow` | Δstock ≠ flow (a stock moving without its flow) |
| `guard_budget_constraint` | spending beyond income + borrowing |
| `guard_nonnegative_price` | negative prices or quantities |

Each has a seeded-fault mutation test proving it goes red on the fault it exists to catch.

## What is exact vs what is free

The economy's *exact* content is the accounting identities, and they are exact **by
definition**: double-entry bookkeeping makes income ≡ expenditure and the sectoral
balances sum to zero *by construction* — no model, no data, no symmetry argument needed.
Walras' law adds the one genuine invariance this field has — only **relative prices** are
determined (rescaling the unit of account changes nothing). And Sonnenschein–Mantel–Debreu
proves the deepest version of the point: the aggregate data can never *select* the model,
because any aggregate behaviour consistent with Walras' law + homogeneity is realizable by
*some* economy — so the deep parameters (β, σ, φ, …) are not merely unpredicable, they are
**unidentifiable from aggregates**. The reliable content is what the accounts forbid; the
free content is everything behavioural.

## The theoretical axis, built — set-identification (the "better model")

`src/pacland/economics/identification.py` makes the SMD point a check, not a citation:

- **Gorman aggregation** — two economies with *different* endowment distributions but the
  same total produce the *same* aggregate excess demand. So the distribution is not
  identified from aggregates; the total is.
- **`guard_point_identified`** — a model's point claim is refused when an alternative
  parameter value produces the same aggregate (set-identified), and admitted only when no
  alternative exists (point-identified). This is the axis-2 falsifier: it goes red exactly
  when a model reports a point inside an unidentified region.
- **The better model** (`constraint_set_model`) — emits the *identified* quantity (the
  private balance S−I, forced by the identity) and the *identified set* for the rest (S vs I
  are a line), and refuses a point forecast inside an unidentified region.

Reproduce: `python3 scripts/validate_economics_identification.py` (5/5 exact).

## The empirical axis, built — forecast failure

`src/pacland/economics/forecast.py` makes the Meese–Rogoff point a check, not a citation:

- **`guard_forecast_is_extrapolation`** — compares a model's one-step-ahead forecast
  error against the no-change (random-walk) benchmark. It stays green while the model
  fails to beat the benchmark (the forecast is extrapolation, not verification), and goes
  **red** when a model has real out-of-sample skill (falsifying the axis-1 claim for that
  model) — the seeded-oracle mutation proves the check can fire.
- The real-data confirmation of axis 1 is the field's own record: Meese–Rogoff 1983, Rossi
  2013, Gürkaynak et al. — a structural model fails to beat a random walk out of sample.

Reproduce: `python3 scripts/validate_economics_forecast.py` (3/3).

## Honest limits

- **"validated" ≠ "validated out-of-sample."** It means "reproduces the measured series
  in-sample." A forecast is a different claim with no observation, and the deficit is the
  *statement of that gap* — the Meese–Rogoff failure is exactly where the `m = 4` stops.
- **`m = 4` is optimistic.** The field's own record (structural models fail to beat a
  random walk) shows even the retrospective tier is softer than it looks; tightening `m`
  makes the number worse.
- **The Lucas critique is the deeper wall.** A policy counterfactual is not merely
  unmeasured — it is *unmeasurable in principle*, because the model's parameters shift
  with the policy itself. The forecast is not just extrapolation; it is a moving target.
- **This is a characterisation, not a predictor.** It says "you are here," not "this
  forecast will work."

## Reproduce

```
cd pacland && PYTHONPATH=src python3 -m pacland.economics.deficit
PYTHONPATH=src python3 -m unittest tests.test_economics_deficit tests.test_economics_guards -v
```
