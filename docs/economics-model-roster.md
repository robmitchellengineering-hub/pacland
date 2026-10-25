# The physics-level bar for a macro-finance model — and the roster

Status: **roster scored and audited** — `src/pacland/economics/model_roster.py`,
`tests/test_economics_model_roster.py`. Two of six models are at the bar; four are
**named but not built**, and the roster says so instead of implying otherwise.

The landscape core never argues for its claims: it publishes a command and the command
exits 0. Climate added the second idea — score **every named model** on hard axes rather
than average a crowd (`docs/climate-trust-board.md`: 53 CMIP6 models in, 14 trusted out).
This page is both machines pointed at macro-finance: a fixed bar, and six named models
scored against it.

## 1. What "physics level" means — eight slots

| slot | the landscape/climate artifact that sets the bar | what a *model* must show |
|---|---|---|
| `exact_structure` | `scripts/validate_all_theorems.py` (six machine-checked proofs) | an inventory of **constraints + labels**, proven symbolically, not asserted in prose |
| `deficit` | the Mitchell deficit, `m = 9` measured + computable + validated | `m` computed **two-tier** — backcast and forecast — with its certificate radius |
| `rule_of_three` | `docs/sm-rule-of-three.md` | three independent arms, distinct failure modes, agreeing |
| `guard_suite` | `src/pacland/economics/guards.py`, each mutation-tested | what the model **forbids**, each guard red on its seeded fault |
| `out_of_sample` | *(no physics analogue — this is the new axis)* | measured against a **real-time vintage**, benchmarked |
| `benchmark` | `src/pacland/economics/forecast.py` | the no-change null it must beat |
| `trust_entry` | `docs/climate-trust-board.md` | a per-model tier with named evidence, on the board |
| `falsifiable_prediction` | `docs/falsifiable-predictions.md` | a registered claim that could die |
| `reproduce` | every `scripts/validate_*.py` | one command, green |

A model's *kind* decides which slots it owes — an oracle owes no forecast, a benchmark
owes no model. The four kinds are `control`, `oracle`, `forecast`, `statistical`.

**The bar is enforced, not decorative.** `audit()` refuses three things: a claimed slot
with no evidence, a claimed slot whose evidence is a repo path that does not exist, and
an `out_of_sample` claim that names no real-time vintage source. Any model carrying one
is scored `broken` regardless of everything else it passes — overclaiming is worse than
not having started.

## 2. The roster, in build order

| # | model | kind | exact content | free | m | today |
|---|---|---|---|---|---|---|
| 0 | **random walk (no change)** | control | none — it asserts tomorrow equals today | none | — | **clean** |
| 1 | **Godley–Lavoie SFC (SIM/SIMEX)** | oracle | every sectoral + stock-flow identity, the budget constraint | behavioural propensities (α₁, α₂, θ) | — | **clean** |
| 2 | **New Keynesian 3-equation** (Taylor 1993; Clarida–Galí–Gertler) | forecast | Fisher exact; long-run Phillips slope (1−β)/κ; determinacy boundary; the zero-inflation domain | 5 (β, κ, σ, φπ, φy) | 3 | **weak — 3 owed** |
| 3 | **Smets–Wouters (2007) DSGE** | forecast | the 20-condition inventory: **13 established** at the steady state, 3 dynamic-only, 4 cited (Table 1a record + Calvo slope + policy rule check) | ~40 (published posterior) | **7** | weak — 5 owed |
| 4 | **VAR(1) (statistical benchmark)** | statistical | none — pure fit, no identity imposed | all coefficients | 3 | **clean** — real-time run done |
| 5 | **GDPNow (Atlanta Fed)** | forecast | national-accounts identities + the bridge equations | bridge coefficients, re-estimated quarterly | 1 | weak — 9 owed |

## 3. Why this order

- **The null (#0) first.** Without the no-change benchmark every other number is
  uninterpretable — Meese–Rogoff is not a critique of a model, it is the unit the model
  is measured in. It is already the guard's benchmark, so it costs nothing to score.
- **The oracle (#1) second.** The SFC model is exact *by construction*: double-entry
  bookkeeping makes every identity hold, so it defines what "the model must not violate"
  means before any forecast is scored. It is already at the bar — the real-data closure
  reproduces on FRED (`docs/economics-accounting-closure.md`).
- **The small forecast model (#2) third.** The positive control: three equations, five
  parameters, every constraint and every free parameter enumerable in closed form. The
  machinery gets proven here, at a size where a disagreement is a bug and not a
  judgement call — the landscape's tadpole, for macro.
- **The workhorse (#3) fourth.** Smets–Wouters is the model central banks actually
  forecast with, and it publishes its observation set: **seven series**. That is its `m`
  by construction — output growth, consumption growth, investment growth, hours, real
  wage growth, inflation, policy rate — which is exactly the shape of the PACLAND
  deficit. (All seven pull keyless from FRED; see §5.)
- **The baselines last (#4, #5).** A BVAR has no exact content to inventory, so its
  verdict is a single number: does it beat the null where the structural model cannot.
  GDPNow is a real published nowcast — the cleanest test of what "verified" is allowed
  to mean — but it needs vintages to be scored honestly.

## 4. The honest state

```
random walk (no change)                     control     clean
Godley–Lavoie SFC (SIM/SIMEX)               oracle      clean
New Keynesian 3-equation                    forecast    weak   owes 3  (out_of_sample, benchmark, trust_entry)
Smets–Wouters (2007) DSGE                   forecast    weak   owes 5  (exact_structure, out_of_sample, benchmark, trust_entry, prediction)
VAR(1) (statistical benchmark)              statistical clean
GDPNow (Atlanta Fed)                        forecast    weak   owes 9
```

The NK three-equation model now earns six of the nine slots: exact structure (8/8
sympy), the deficit and its ceiling, the Rule of Three on determinacy, five
mutation-tested guards, a registered falsifiable prediction, and a one-command
reproduce. It still owes the out-of-sample run, the benchmark comparison and a clean
board row — so it prints `weak`, which is what it is.

The other `weak` rows are named-but-not-built: their exact content is known, their data
is reachable, and their deficits are **not computed**. The roster would rather print
that than a tier it has not earned.

### What the NK model actually established (slice 2)

- **Exact:** `x = (1−β)/κ · π` from the NKPC; `i = r* + π` (Fisher); `d(i−π)/dπ = 0`
  (superneutrality); the long-run Phillips slope `(1−β)/κ`; the determinacy boundary
  `φπ > 1 − (1−β)/κ · φy`, which is **σ-free**.
- **Uncomfortable, and the reason it was worth building:** with `β < 1` and `φy > 0`
  the three equations have **no jointly consistent steady state at a non-zero inflation
  target** — the NKPC puts the gap at `(1−β)/κ · π*`, the IS curve and the Taylor rule
  put it at zero, and the contradiction is exactly `φy · (1−β)/κ · π*`. The model's
  domain is zero net inflation; a 2% target is outside it. `guard_steady_state_admissible`
  refuses the out-of-domain use instead of averaging it in.
- **A ceiling, not a gap:** three observables, so the best the model can ever score is
  `m = 3` → a 78% certificate at δ = 0.025. A 1% certificate would need m ≈ 18,000.

### What the SW record established (slice 3)

Source **fetched, not recalled**: Smets & Wouters (2007), ECB Working Paper 722 — Tables
1a/1b (pp. 34–35), Table 3 (p. 37), policy rule eq. 23 (p. 52). The published posterior
means are recorded verbatim in `src/pacland/economics/sw2007.py`; the risk with a
published model is transcription, not algebra, so every derived quantity is checked
against what the paper says in prose:

| derived | from | paper says | check |
|---|---|---|---|
| β = 0.99840 | `100(1/β − 1) = 0.16` %/q | — | exact |
| β̃ = 0.99251 | `β · γ^(−σ_c)`, γ = 0.43%, σ_c = 1.38 | — | exact |
| real rate **3.02%**/yr | `1/β̃ − 1` | "about 3%" | 0.02pp |
| inflation **3.12%**/yr | π̄ = 0.78 %/q | "about 3%" | 0.12pp |
| nominal **6.14%**/yr | Fisher | "about 6%" | 0.14pp |
| Calvo slope κ = **0.1777** | ξ_p = 0.66 | — | exact |

Eleven checks, `scripts/validate_economics_sw.py`, 11/11. The Taylor boundary at the
published output response is **0.9966**; their published inflation response is
**2.04**, so the rule is comfortably determinate — with the caveat that smoothing
(ρ = 0.81) leaves the *contemporaneous* response at only **0.39** while the long-run
response stays 2.04. Two things sit outside the three-equation reduction and are named
rather than buried: the r_Δy = 0.22 growth term, and the smoothing itself.

**The correction this slice forced on our own narrative.** The roster said the
workhorse "fails to beat a VAR out of sample" (Gürkaynak–Kısacıkoğlu–Rossi). SW's own
Table 3 says otherwise for *their* model: against a VAR(1) over 1990:1–2004:4 the DSGE
gains **+3.06 (1q) … +13.51 (12q)** on the overall measure. The claim was wrong as
stated and is retracted here.

What that table does **not** contain is the no-change (random-walk) null — so the
Meese–Rogoff question is genuinely open, and it is exactly what slice 4 runs. The
correction sharpens the plan instead of weakening it: the field's best-known
out-of-sample table benchmarks a VAR(1), not "tomorrow equals today".

### What the conditions inventory established (slice 5)

The objective was to machine-check the model's ~20 linearised conditions. The honest way
to do that without transcribing a technical appendix is to go the other way: take the
paper's **nonlinear** decision problems (appendix 1, pp. 47–53) and *derive* the steady
state in sympy, then record verdicts. `src/pacland/economics/sw_structure.py` carries the
inventory; `scripts/validate_sw_structure.py` derives it, **9/9**.

| derivation | result |
|---|---|
| Euler → Fisher | `R = π̄/β̃` → **1.5407 %/q = 6.16 %/yr** |
| Tobin's Q = 1 | `R^k = 1/β̃ − 1 + δ` → **3.25 %/q** |
| capital accumulation | `i = δk` |
| production + FOCs | `y+φ = k^α(ΓL)^{1−α}`, `k/L = α/(1−α)·w/R^k` |
| cost identity | eq. (6) reproduces `mc` from the FOCs — true because production is CRS (Euler's theorem) |
| resource constraint | `k/(y+φ) = α·mc/R^k`, so `i/y = δk/y = 0.122`, `c/y = 0.698` |
| policy rule | satisfied by `R = R*` at **any** target |

**The result worth keeping:** SW's rule is written in deviations from *its own* steady
state, so `π = π*`, `R = R*` satisfies it identically for any target. The NK three-equation
model has no steady state at a non-zero target (`nk3.guard_steady_state_admissible`); SW
does not inherit that bug — it is designed out. That is the model-design lesson the two
slices now carry together.

**Scope, stated not implied:** 13 of 20 conditions are established, 3 are dynamic-only by
construction (the Calvo reset-price and wage recursions, and the utilisation FOC — their
content is the recursion, not a steady-state number), and 4 are cited as given (the
Kimball aggregator, the demand curve, the government-spending and shock processes). The
`exact_structure` slot therefore stays **unclaimed**, and a roster test asserts that:
coverage is not total, so the model does not get the tick.

δ = 0.025 is a **calibration**, not a Table 1a estimate, and is labelled as such wherever
it appears.

### The real-time run (slice 4): does anything beat "no change"?

Slice 3 found that the field's best-known out-of-sample table (SW 2007, Table 3)
benchmarks a **VAR(1)**, never the no-change null. This slice asks the missing question
on data *as it was published* — ALFRED's graph endpoint takes an explicit
`vintage_date` and needs **no API key** (verified 2026-10-26), so
`scripts/fetch_economics_vintages.py` commits a fixture of 10 vintages × 4 series and
the suite runs offline.

| model | h=1 | h=2 | h=4 | ratio to the null (1,2,4) | paired wins |
|---|---|---|---|---|---|
| no-change | 0.0208 | 0.0292 | 0.0574 | 1.00x / 1.00x / 1.00x | — |
| AR(1) | 0.0191 | 0.0256 | 0.0399 | 0.92x / 0.88x / 0.69x | 20/27 · 22/27 · 22/24 |
| **VAR(1)** | **0.0179** | **0.0230** | **0.0364** | **0.86x / 0.79x / 0.63x** | **21/27 · 23/27 · 22/24** |

Errors are log-growth (rebasing-invariant), scored against today's revised values. The
VAR beats the null at every horizon and wins more paired comparisons than it loses.

**Two caveats, and they matter.** The sample is 26 forecasts from 9 usable vintages — a
direction, not a verdict. And this is *not* the three-way test: SW's own model is not
estimated here (that is the next slice), so what is established today is that the null
is beatable on these three series at these horizons by a plain VAR — which makes the
SW-vs-null comparison the interesting one, not a formality.

**The trap this slice hit, and the guard that now exists.** The first run reported
RMSE ≈ 0.50 — a 50% error on a one-quarter forecast. The cause was not the models: an
old vintage is not on today's base (GDPC1 reads ~10,493 in the 2003 vintage and ~15,163
today — a *rebasing*, not a revision), so level errors measure the rebasing. Growth — a
log difference taken within one vintage for the forecast and within today's vintage for
the truth — cancels it. `guard_growth_not_levels` now refuses a table whose error scale
is level-sized, so that mistake cannot be published quietly.

## 5. The one hard precondition: real-time vintages — **met**

- **Current-vintage data is keyless.** All seven Smets–Wouters observables pull from
  FRED's `fredgraph.csv` endpoint with no API key.
- **Real-time vintages are keyless too.** ALFRED's graph endpoint
  (`alfredgraph.csv?vintage_date=…`) returns a series *as published on a date*, with no
  key — so the Meese–Rogoff test needs no credential, no scrape, and no RTDSM
  spreadsheet. Fixture: `data/economics/vintages.json`; fetcher:
  `scripts/fetch_economics_vintages.py`.
- **Vintage coverage is series-specific.** GDPC1, PCECC96, GPDIC1 and CPIAUCSL have
  usable vintages; FEDFUNDS, HOANBS and COMPRNFB returned nothing at the dates tried,
  so the real-time panel is three quarterly series until that is chased.
- **The audit still refuses the `out_of_sample` slot without a named vintage source** —
  that is the protection against shipping a current-vintage backtest as if it were a
  forecast.

## 6. The slices, and what each leaves behind

1. **This slice** — the bar, the roster, the honesty gate, and per-model board rows.
2. ~~**NK 3-equation**~~ — **done** (this round): 8/8 sympy proofs, the deficit ceiling,
   five mutation-tested guards, two registered falsifications, one-command reproduce.
   Still owes out-of-sample, benchmark and a clean row.
3. **Smets–Wouters** — the ~20-condition inventory machine-checked, `m = 7` computed
   two-tier, a determinacy guard. The workhorse scored where policy acts.
4. ~~**Vintages**~~ — **done**: keyless ALFRED vintages, the fixture, the no-look-ahead
   and no-target-leak guards, and the null-vs-AR(1)-vs-VAR(1) run. Still open from the
   original wording: **SW's own model is not estimated**, so the three-way is
   null/AR/VAR today and null/SW next.
5. ~~**SW conditions inventory**~~ — **done**: 13/20 established symbolically, 7
   scoped out with reasons, and the model-design contrast with NK3 recorded.
6. **SW out of sample** — estimate the model (or a defensible reduced form) and run it
   against the null on the vintage fixture, completing the three-way.
7. **The asset-pricing arm** *(only if "finance" means markets rather than macro)* —
   put–call parity, the Hansen–Jagannathan bound, Black–Scholes. Their exact content is
   stronger than macro's (no-arbitrage is a theorem), so they may belong first if that is
   the intended meaning; they are held back until the roster's macro half is green.

## 7. Honest limits

- **The bar is a checklist, not a proof of correctness.** A model can pass every slot and
  still be wrong about the world — that is precisely what the deficit reports, and why
  the deficit is a slot rather than the verdict.
- **`m = 7` for Smets–Wouters is its published observation set**, not a validated count.
  Their own paper validates it in-sample; the seven series being *observable* is not the
  same as seven being *validated*, and the deficit is the number that separates them.
- **Only two rows are evidence-backed today.** The other four are a plan with names.

## Reproduce

```
cd pacland && PYTHONPATH=src python3 -m unittest tests.test_economics_model_roster -v
PYTHONPATH=src python3 -c "from pacland.economics.model_roster import summary; [print(r) for r in summary()]"
```
