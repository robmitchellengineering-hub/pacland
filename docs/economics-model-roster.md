# The physics-level bar for a macro-finance model — and the roster

Status: **roster scored and audited** — `src/pacland/economics/model_roster.py`,
`tests/test_economics_model_roster.py`. Two of six models are at the bar; four are
**named but not built**, and the roster says so instead of implying otherwise.

Method: [SOP — figuring a complex system out](SOP-FIGURING-SYSTEMS-OUT.md). This page is
that method's worked example.

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
| 2 | **New Keynesian 3-equation** (Taylor 1993; Clarida–Galí–Gertler) | forecast | Fisher exact; long-run Phillips slope (1−β)/κ; determinacy boundary; the zero-inflation domain; two-shock policy function | 7 (+ρ_r, ρ_u) | 3 | **weak — 0 owed, run lost** |
| 3 | **Smets–Wouters (2007) DSGE** | forecast | the 20-condition inventory: **16 proved** at the steady state, 4 specifications (inputs), 0 unresolved | ~40 (published posterior) | **7** | weak — 2 owed |
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
New Keynesian 3-equation                    forecast    weak   owes 0 — but its real-time run LOSES to the null
Smets–Wouters (2007) DSGE                   forecast    weak   owes 2  (out_of_sample, benchmark)
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

### The NK model, out of sample (slice 6): the null wins on inflation

The three-equation model is now fully specified — two AR(1) shocks (demand at ρ_r = 0.9,
cost-push at ρ_u = 0.8) solved by undetermined coefficients, so an observed state yields
a forecast. `scripts/economics_nk3_oos.py` runs it on the same vintage fixture, against
the null and an AR(1), on the two things it actually forecasts:

| | h=1 | h=2 | h=4 | ratio to the null |
|---|---|---|---|---|
| **inflation** no-change | 2.730 | 1.876 | 1.843 | 1.00 / 1.00 / 1.00 |
| inflation AR(1) | 2.235 | 1.549 | 2.070 | 0.82 / 0.83 / 1.12 |
| inflation **NK3** | 2.823 | 1.940 | 2.353 | **1.03 / 1.03 / 1.28** |
| **gap** no-change | 0.523 | 0.732 | 1.219 | 1.00 / 1.00 / 1.00 |
| gap **NK3** | 0.537 | 0.591 | 0.861 | 1.03 / 0.81 / **0.71** |

**The calibrated NK model loses to "no change" on inflation at every horizon** and wins
on the output gap only at 4 quarters (0.71x). Nine forecasts per cell — a direction, not
a verdict — and the calibration is *stated, not estimated*, so this measures the textbook
model rather than the best-fitted one. It is still the result the field's own debate
needs stated plainly: for a structural model, beating the null is not automatic.

**The board rule this forced.** NK3 now owes no slot, but a model that has taken the
test and *lost* must not be trusted more for having taken it. So `Model.outcome`
(`beats_null` / `loses_to_null`) is now part of the tier: every slot earned **and**
`loses_to_null` is still `weak`. VAR(1), which won (0.86x / 0.79x / 0.63x), is `clean`.
The contrast is exactly the point of a trust board.

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

### The three-way, as far as it goes (slice 8)

The objective asked for **SW vs BVAR vs the null**. SW's full model is 20 conditions and
~40 parameters; estimating it is a project. So the comparison is run at the level the
published record supports — SW's *published parameters* in a three-equation reduction,
named as such everywhere it appears:

| inflation, real-time | h=1 | h=2 | h=4 | ratio to the null |
|---|---|---|---|---|
| no-change | 2.730 | 1.876 | 1.843 | 1.00 / 1.00 / 1.00 |
| AR(1) | 2.235 | 1.549 | 2.070 | 0.82 / 0.83 / 1.12 |
| textbook NK3 | 2.823 | 1.940 | 2.353 | 1.03 / 1.03 / 1.28 |
| **SW subsystem** (κ = 0.178, φπ = 2.04, φy = 0.08) | 2.806 | 1.922 | 2.243 | **1.03 / 1.02 / 1.22** |

| output gap | h=1 | h=2 | h=4 |
|---|---|---|---|
| NK3 | 1.03x | 0.81x | **0.71x** |
| SW subsystem | 1.04x | 0.80x | **0.69x** |

**The finding worth keeping: SW's own parameters do not rescue the inflation forecast.**
Going from the textbook calibration (κ = 0.10, φπ = 1.5, φy = 0.5) to SW's published
values (κ = 0.178 from their Calvo estimate, φπ = 2.04, φy = 0.08) moves the
one-quarter ratio from 1.03x to 1.03x. The loss is not a parameter accident — it is the
mechanism, on this data, at these horizons. Meanwhile the VAR(1) — no structure at all —
beats the null by 0.86x / 0.79x / 0.63x.

**What this is not.** It is not SW. No capital, no Calvo wages, no partial indexation, no
seven shocks; ρ_r and ρ_u are borrowed from the textbook run and labelled as borrowed.
SW itself still owes `out_of_sample` and `benchmark`, and the registered prediction
(§9) says what it will find when it is estimated.

### The constraint set — plural, by design (slice 9)

Physics gave the *shape* of the machine, not a licence to insist on one constraint. The
landscape has a single invariant because it has a duality group and a finite-generation
theorem; macro-finance has neither, and forcing the analogy would have been the overclaim.
What macro-finance has is a **set** — and a set has to be measured, not asserted.

`src/pacland/economics/constraint_set.py` holds **11 constraints**, each with a kind, a
statement, a source and a residual function:

| kind | count | examples |
|---|---|---|
| **identity** (true by construction) | 4 | circular flow · sectoral balances · stock-flow · the budget constraint |
| **model** (true of the model's solution) | 5 | Fisher · Taylor principle · long-run Phillips · resource shares · capital–output relation |
| **domain** (where the model is defined) | 2 | non-negative prices · the zero-inflation domain |

Two numbers matter, and neither is "how many we wrote down":

- **Independent rank = 8 of 8 equalities**, measured as the rank of the constraint
  Jacobian at a *generic* point. A dependent constraint is one constraint wearing two
  hats, and the test proves the detector works: duplicating Fisher as `2·(i − r* − π)`
  lifts the count to 9 and leaves the rank at 8.
- **Slack ordering** — which constraints actually bind. A constraint the data never
  approaches is decoration; the one with the smallest slack is doing the work.

The reference state is **derived**, not hand-tuned: it is the model's own steady state
(Fisher at `r* + π`, the long-run Phillips gap, the capital–output ratio at the rental
rate) joined to a closed set of accounts, so the set is consistent at a point that no one
picked. `guard_default_state_is_admissible` fails if a constraint and a model ever drift
apart.

### The estimation (slice 10): what the data will and will not identify

Rob funded the estimation the roster's last two SW slots need. It ran, and its answer is a
**refusal, twice over** — which is the useful kind of answer.

**What the data identifies: the policy rule.** A linear regression of the federal funds
rate on inflation and the trend gap, on 338 real-time observations from the vintage paths:

```
static   i = +3.444 +0.461*pi -0.449*x     SEs 0.061 / 0.067 · R² 0.287
smoothed i = rho 0.900, long-run phi_pi 0.985, long-run phi_y 1.365 · R² 0.796
```

The fitted rule is **passive** — `φπ = 0.46` static, long-run `0.99` once smoothing is
included — where SW's *structural* estimate is `φπ = 2.04`. That gap is not a mistake in
either: the regression has no expectations, a crude trend gap, and smoothing the model does
not carry (which biases `φπ` down hard — the classic result). It is exactly why
structural estimation exists. The estimator is validated on synthetic data with a known
rule before its real-data numbers are believed.

**What the data does not identify: the Phillips slope.** Running the moment-matching
estimator on the model's own simulated data at a known `κ = 0.18` recovers **1.00** — a
bound. The four-parameter fit is rank-deficient (3 of 4). With two shocks and their
variances free, `κ` mostly rescales responses that the variances absorb. This is the
classic weak-identification problem in the NKPC, reproduced on our own machinery rather
than cited — and it means no `κ` estimated from this sample would mean anything.

**What the constraint set does with the fitted rule: refuses it.** A passive rule admits
sunspots, so `taylor_principle` fails and `estimate.estimated_calibration()` raises
`InadmissibleFit` instead of handing out a forecast. The eight independent constraints are
now doing real work: they are the reason an unusable fit cannot be laundered into an
out-of-sample table.

**So SW's last two slots stay open, and the reason is now measured.** Not "we ran out of
time": the sample cannot identify the slope, and the identifiable part (the rule) violates
the discipline's own constraint. Taking the slots would require a full-information
estimation of the 20-condition model — the project this slice has now scoped and priced
rather than guessed.

### GDPNow (slice 11): a published nowcast, and a real result

The Atlanta Fed's GDPNow is the cleanest test of what "verified" may mean: a model run by
professionals, published, updated through the quarter, targeting a number that appears
about four weeks after the quarter ends. The record is real-time (ALFRED vintages,
keyless), 37 quarters, 2016Q2–2025Q4.

| model | MAE | RMSE | ratio to the null |
|---|---|---|---|
| no-change | 5.055 | 13.200 | 1.00x |
| **GDPNow** | **1.262** | **1.906** | **0.25x MAE · 0.14x RMSE** |

28/37 paired wins. **Excluding 2020 — whose collapse dominates the null's RMSE — the edge
survives: 24/33 wins, 0.51x MAE.** That robustness line is the result; the headline 0.25x
is a number COVID made.

**Four guards, because this test could lie three ways.** The nowcast vintage must
*strictly* predate the vintage carrying its target (else the "forecast" reads the answer);
the null must be built from the **same vintage** as the nowcast (else the model gets data
the benchmark never had); the target must be the **first published** value; and both series
must be growth rates, not levels. All four are checked per quarter, and each has a seeded
fault in the tests. The second one actually fired on the first fetch — the benchmark had
drifted a release — which is why it exists.

**The advance-estimate claim, and the prediction it survived.** GDPNow beats "last
quarter's growth" at nowcasting the **advance estimate** — a number built from the same
monthly source data. That invited the obvious objection: is the edge just an artifact of
targeting the first print? Prediction §11 said the edge would shrink below half when
scored against the **revised** value. **It was falsified in the same slice that registered
it:**

| target | MAE ratio | edge | paired wins |
|---|---|---|---|
| advance | 0.25x | 0.75 | 28/37 |
| **revised** | **0.31x** | **0.69** | **24/37** |

The edge survives revision with most of its force, so the caution was too cautious and is
retracted. What stays true: the nowcast is built from the same source data as the advance
estimate, so this measures a good reconstruction — not a year-ahead forecast.

**And the deficit does its job:** `m = 1`. One observable buys a certificate radius of
**1.36** at 5%. However well the model does, a single series cannot certify anything
narrowly — the deficit is a property of the observable set, not of the model's skill.

### GDPNow's exact half — the national accounts (slice 12)

The last slot GDPNow owed was `exact_structure`. It is an **accounting bridge**: monthly
source data are mapped onto the expenditure components, and the components are added up.
So its exact content is the national-accounts identity, and its specification is the
bridge. Both are now named, and the first is proved on 32 quarters of real BEA data
(2018Q1–2025Q4, `src/pacland/economics/national_accounts.py`):

| condition | status | measured |
|---|---|---|
| `GDP = C + I + G + NX` | **proved** | max residual 0.038 bn = **1.2 × 10⁻⁴ % of GDP** |
| nominal contributions sum to nominal growth | **proved** | worst gap **2.7 × 10⁻⁴ pp** |
| nominal shares sum to 1 | **proved** | worst gap **1.8 × 10⁻⁶** |
| the **real** decomposition closes | **specification** | chain-link residual mean **−1.77 pp**, max **24.9 pp** |
| the bridge equations | **specification** | the Atlanta Fed's engineering, not re-derived |
| BEA's chained aggregation | **specification** | the source of the leak above |

**Tolerances are publication rounding, not floating point.** BEA publishes components to
0.001 bn, so the identity closes to ~10⁻⁴ of a percentage point — a thousand times smaller
than any economic effect. Demanding 10⁻¹² would have been a claim about BEA's rounding,
not about the accounts, and the guards say which gap they measured.

**The real side does not close, and that is the finding.** Chained-dollar components are
not additive — real GDP is a chain aggregate — so summing real component changes divided
by real GDP leaves a residual that averages −1.8 pp and reaches **−24.9 pp** in 2020.
Excluding 2020 it still averages −2.2 pp with a 5.2 pp worst case. That residual is the
*measured deficit* of the real decomposition; no arithmetic removes it, and a page that
presented `GDP = C + I + G + NX` as exact for *real* GDP would be wrong.

**Board effect: GDPNow is the first model from outside this repo to go `clean`** — all nine
slots, outcome `beats_null` (0.25x MAE on the advance estimate, 0.31x on the revised
value). Two of six roster rows now pass the bar on their own merits; three are clean
overall.

### The linearised model, from the authors' own file (slice 13)

The objective asked for **the ~20 linearised equilibrium conditions machine-checked**. The
paper's technical appendix is not openly posted — but the **authors' own Dynare
implementation** of the linearised model is, maintained by Johannes Pfeifer in the
`DSGE_mod` replication library. That file *is* the linearised system, machine-readable, and
it is a better source than any transcription of mine.

`scripts/verify_sw_mod.py` fetches it (pinned URL, **sha256
`662d1e82…1ffddb`**, never committed — it is GPL and this repo is MIT), parses the model
block, and checks the two things that can be settled mechanically:

| check | result |
|---|---|
| the model block parses into statements | **40 equations = 34 equilibrium + 6 measurement** |
| every equilibrium condition vanishes at the steady state | **34/34** |
| every measurement equation carries its steady-state constant | **6/6** |
| the implied real rate vs the paper's "about 3%" | **3.02 %/yr** |
| the implied nominal rate vs the paper's "about 6%" | **6.16 %/yr** |
| agreement with this repo's independent derivation | **6.16 vs 6.14 %/yr** (the Fisher cross term) |
| the expenditure shares sum to one | **0.649 + 0.171 + 0.18 = 1.000** |

**Why "vanishes at the steady state" is a real test, not a formality.** A linearised model
is an expansion about a point where every deviation is zero, so each behavioural equation
must reduce to `0 = 0` there. If a steady-state ratio and an equation disagree, the residual
is non-zero and the transcription is wrong — caught without knowing any economics, which is
the point. The six that do *not* vanish are the measurement equations (`dy`, `dc`, `dinve`,
`dw`, `pinfobs`, `robs`): they carry `ctrend`, `constepinf` and `conster` because they map
deviations to observables. Separating them is part of the check, not an exemption from it.

**Two sources agreeing is the Rule of Three on the derivation:** the nonlinear appendix
derived by hand (`validate_sw_structure.py`, 12/12), the authors' linearised file
(34/34 here), and the paper's own reported rates. All three land on 3.0 and 6.1–6.2 %.

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
6. ~~**NK3 out of sample**~~ — **done**: two-shock policy function, real-time run on the
   fixture, and the loss recorded in the tier rather than hidden.
7. ~~**SW inventory closed**~~ — **done**: 16/20 proved, 4 specifications, 0 unresolved;
   `exact_structure`, `trust_entry` and a registered falsifiable prediction claimed.
8. ~~**Three-way at the supportable level**~~ — **done**: SW's published parameters in a
   three-equation reduction, four arms, one null, and the label honest.
9. **SW out of sample** — estimate the model itself (or a defensible reduced form) and
   run it against the null on the vintage fixture, completing the literal three-way. The registered
   prediction (falsifiable-predictions §9) says it beats the VAR(1) but not the null on
   inflation at h ≤ 2.
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

Or from the CLI — three views, each rendering what the modules have already verified:

```
pacland economics              # the verification deficit (unchanged)
pacland economics --models     # the roster, scored, with what each row owes
pacland economics --constraints # the constraint set and its measured independent rank
pacland economics --realtime   # every model against its null, on data as it was published
```

## What the first print is worth — replicated on 239 quarters

A real result, measured twice: first on 37 quarters of BEA advances, then on the Philadelphia Fed's
own **First/Second/Third/Most-Recent** release ladder back to 1965 — a different assembly, 6.5× the
history.

| question | 37 quarters (BEA) | **239 quarters (Fed ladder)** |
|---|---|---|
| biased upward? | +0.565 pp, t = 2.39 (***sensitive*** — see below) | **+0.469 pp, t = 3.68, 62% upward** |
| memory in revisions? | AR(1) = 0.017 | **AR(1) = −0.066** |
| exploitable? | 1.22× worse out of sample | **1.02× — a wash** |
| beats the print? | no: print 0.92 pp vs nowcast 1.54 pp | — |

Per release step, on the ladder: first→second **+0.115 pp** (t = 2.89), second→third **+0.057 pp**
(t = 2.39), first→most recent **+0.469 pp** (t = 3.68). The bias arrives in pieces, not one jump.

**The 37-quarter number is not stable, and a cross-source check is how we know.** Comparing the Fed's
First Release against the `advance` we had recorded for the 36 overlapping quarters: **34 agree within
0.5 pp**, and two do not — **2020Q2 at −7.00 pp** and 2020Q3 at −4.50 pp. Those are not noise; one of
the two records is not the first print. The 37-quarter mean revision moves **+0.565 → +0.357**
(excluding those quarters) or **+0.254** (using the Fed's values) — a **0.311 pp swing**. So the
37-quarter figure is quoted as a cross-check, not as the headline. **The 239-quarter ladder is the
headline**, because it never depends on our advance column.

Reproduce: `python3 scripts/economics_release_archive.py` and
`python3 scripts/economics_release_cross.py`.

**"GDPNow beats the no-change null 4:1" stays true.** What it does not license is "GDPNow is the
best estimate of GDP": against the final number the official first print is closer, and the first
print's own upward bias cannot be traded — no memory (AR(1) = −0.07) and a fitted correction is a
wash out of sample.

Reproduce: `python3 scripts/economics_revisions.py` (37 quarters) and
`python3 scripts/economics_release_archive.py` (239 quarters).
