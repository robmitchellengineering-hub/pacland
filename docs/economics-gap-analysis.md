# Economics gap analysis — does (ε,δ) certification exist in macroeconomics?

Status: **complete — 5/5 returned** (2026-10-22). Discipline #3, playbook item #3.
The same 5-angle method that produced `docs/climate-gap-analysis.md` and
`docs/drugs-gap-analysis.md`.

## 1. Hypothesis under test

> PAC/Valiant-style (ε,δ) certification — and a single "verification deficit" number —
> do **not** exist as a category in macroeconomics. "Verification" is in-sample fit
> (R², likelihood, RMSE) or a forecast band with no calibration guarantee; and no one
> collapses measured-vs-predicted into one number.

## 2. Method — the five angles

| # | angle | question |
|---|---|---|
| 1 | formal verification | any PAC/(ε,δ)/machine-checked work in macro / econometrics / DSGE / CGE? |
| 2 | prediction calibration | is a forecast band a guarantee, or a confidence score? are macro forecasts calibrated? |
| 3 | AI/ML models | ML macro forecasting (nowcasting, factor models, neural nets) — any certificate over their predictions? |
| 4 | measured vs predicted | has anyone counted measured vs predicted in macro as one number? |
| 5 | constraint-first / falsification | are accounting identities already constraint-first? is there a certified guard-suite? |

## 3. The deficit-transfer framework (how `m` generalises — the durable spine)

Mapped from pacland onto macroeconomics:

- **The prediction.** A forecast or policy counterfactual — GDP growth, inflation,
  unemployment, the policy-rate path, a recession probability.
- **The verifier is imperfect twice over.** The two-level certificate splits into
  *candidate-vs-oracle* (the model vs the estimation sample) and *oracle-vs-truth*
  (the estimation sample vs the **unobserved future**). Estimation is retrospective;
  the object policy acts on is prospective.
- **`m`** = the number of series simultaneously *measured* (an observed value exists),
  *computable* (the model predicts it), and *validated* (the prediction reproduces the
  measurement). On the backcast record `m` is the jointly-fitted set; for the **future
  there is no measurement yet → `m = 0`**, and the forecast is extrapolation.
- **Constraint-first maps onto an already-mature practice.** National-accounting
  identities — the circular flow (income ≡ expenditure ≡ output), the sectoral
  balances ((S−I)+(T−G)+(M−X)=0), stock-flow consistency (Δstock = flow) — are the
  reliable content ("rule out beats predict"). They hold **by construction**
  (double-entry bookkeeping), so they are the always-true answer. The label is the
  institutional/accounting structure; the forecast value is the free parameter.
- **The four walls, in economic terms:** *unmeasurable* → the future has no observation
  (the deficit) · *underdetermined* → many models fit the same data (identification —
  the constraints) · *intractable* → no feasible algorithm for equilibrium of a
  heterogeneous-agent economy (structure that shortcuts it) · *undecidable* → the
  Lucas critique means a policy-conditional forecast's very object shifts with policy.

## 4. Results (complete)

| angle | verdict | closest prior art | gap |
|---|---|---|---|
| 1 formal verification | **holds** | machine-checked economics is embryonic (proof-theoretic/linear-logic resource accounting; Lean 4 telemetry-style fragments); no PAC (ε,δ) certificate or deficit `m` anywhere | proves **derivation/accounting** correctness, never statistical error vs the world |
| 2 prediction calibration | **holds (largely)** | forecast bands are model-implied, not calibrated; the field's own census (Meese–Rogoff 1983; Rossi 2013) finds structural models fail to beat a random walk out of sample; expert forecasts barely beat chance (Tetlock 2005) | a band is a statement of the model, not a guarantee over it |
| 3 AI/ML models | **holds** | ML nowcasting/factor models beat small benchmarks in-sample, but out-of-sample the edge is thin and uncalibrated under regime change; no certificate | benchmark error, not a per-instance bound; breaks under structural change |
| 4 measured vs predicted | **holds** | the field evaluates forecast error (RMSE/Diebold–Mariano), but as ranking, never as a single measured-vs-predicted deficit; Meese–Rogoff is the canonical "fails out of sample" result | no per-model "verification deficit" number |
| 5 constraint-first | **holds** | national accounts, double-entry, and Godley–Lavoie stock-flow consistency *are* constraint-first, but as bookkeeping discipline; no certified guard-suite a model must *pass* | rule-out never wrapped as a mutation-tested bound |

## 5. Verdict

**Hypothesis confirmed — scoped.** The precise finding:

> **The PAC/Valiant object — a computable (ε,δ) certificate plus a single scalar
> "verification deficit" `m` — does not exist anywhere in macroeconomics.**
> "Verification" is in-sample fit or a forecast band that carries no calibration
> guarantee, and the field's own record is the failure to beat a random walk out of
> sample. The measured-vs-predicted split is quantified only piecemeal (RMSE, ranking),
> never as one number.

**Conflations recorded (fan-out catches):**

1. **"No formal verification in economics" would be false if stated flat** (angle 1).
   There are nascent machine-checked fragments (linear-logic resource accounting,
   proof-theoretic foundations). They certify *accounting/derivation* correctness —
   never a PAC certificate or a deficit over the world.
2. **"Constraint-first is our idea" is false in spirit** (angle 5). The field has run
   constraint-first for a century — national accounts, double-entry bookkeeping, and
   stock-flow consistency *are* "what the economy forbids." What is missing is only the
   *certification*: nobody has wrapped the identities as a mutation-tested bound, and
   nobody has counted the failures as one number. That is the opening — formalise what
   the field already does, don't invent a new filter.

**The anchors that make the headline:**
- **Meese & Rogoff 1983** ("Empirical exchange rate models of the seventies",
  *Journal of International Economics* 14(1–2):3–24) — the canonical result: structural
  exchange-rate models fail to beat a random walk out of sample, and later models do
  not restore the beat. The field's own "verified" forecasts fail where it counts.
- **Rossi 2013** ("Exchange Rate Predictability", *Journal of Economic Literature*
  51(4):1063–1119) — the survey confirming the pessimism: exchange-rate predictability
  is elusive and time-varying.
- **Gürkaynak, Kısacıkoğlu & Rossi** ("Do DSGE Models Forecast More Accurately
  Out-of-Sample than VAR Models?", [CEPR DP 9576](https://ideas.repec.org/p/cpr/ceprdp/9576.html)) —
  the workhorse policy models (DSGE) forecast no better out-of-sample than simple VARs.
- **Tetlock 2005** (*Expert Political Judgment*, Princeton UP) — expert (incl. economic)
  forecasts barely beat chance, and confidence is uncalibrated.

## 6. Chosen target for the deficit report (next step)

Two layers, one report (mirroring climate and drugs):

1. **The macro observable-set deficit** — `m` = the series a model simultaneously
   predicts against measured labels. Two tiers: retrospective backcast (`m` = the
   jointly-fitted set, weak — and even that is in-sample, not the out-of-sample where
   Meese–Rogoff bites) vs prospective forecast (`m = 0`, total).
2. **The accounting guard-suite** — wrap the existing identities (circular flow,
   sectoral balances, stock-flow consistency, the budget constraint, non-negative
   prices) as a *certified* guard-suite, mutation-tested.

The citable headline: *a macroeconomic forecast is "verified" only as an in-sample
backcast — its prospective policy content is extrapolation, and the field's own record
(Meese–Rogoff 1983, Rossi 2013) shows the out-of-sample forecast fails to beat a random
walk.*
