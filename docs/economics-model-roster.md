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
| 3 | **Smets–Wouters (2007) DSGE** | forecast | ~20 linearized equilibrium conditions (Euler, NKPC, Taylor, Fisher, capital accumulation, resource constraint, AR shocks) | ~40 (published posterior) | **7** | weak — 9 slots owed |
| 4 | **Bayesian VAR** | statistical | none — pure fit, no identity imposed | all coefficients + prior | 3–7 | weak — 3 owed |
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
Smets–Wouters (2007) DSGE                   forecast    weak   owes 9
Bayesian VAR                                statistical weak   owes 3
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

## 5. The one hard precondition: real-time vintages

- **Current-vintage data is keyless and verified.** All seven Smets–Wouters observables
  pull from FRED's `fredgraph.csv` endpoint with no API key (checked 2026-10-25).
- **Out-of-sample needs vintages**, and that is a different dataset: the value of GDP
  *as first published*, not as revised. ALFRED requires a free FRED API key; the
  Philadelphia Fed's Real-Time Data Set for Macroeconomists (Croushore–Stark) is the
  keyless alternative and its landing page is up.
- **Until a vintage source is connected, every "beats the benchmark" number here is a
  backtest.** That is why the audit refuses the `out_of_sample` slot without a named
  vintage source: the refusal is the protection against shipping exactly the error the
  discipline exists to name.

## 6. The slices, and what each leaves behind

1. **This slice** — the bar, the roster, the honesty gate, and per-model board rows.
2. ~~**NK 3-equation**~~ — **done** (this round): 8/8 sympy proofs, the deficit ceiling,
   five mutation-tested guards, two registered falsifications, one-command reproduce.
   Still owes out-of-sample, benchmark and a clean row.
3. **Smets–Wouters** — the ~20-condition inventory machine-checked, `m = 7` computed
   two-tier, a determinacy guard. The workhorse scored where policy acts.
4. **Vintages** — connect ALFRED (or RTDSM) and run the real Meese–Rogoff test:
   SW vs BVAR vs the null, on data as it was known at the time.
5. **The asset-pricing arm** *(only if "finance" means markets rather than macro)* —
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
