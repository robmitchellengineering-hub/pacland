# Climate gap analysis — does (ε,δ) certification exist in Earth-system modelling?

Status: **in progress** — 5-angle fan-out running; framework below is the durable spine,
results section fills in as agents return (2026-10-22).

---

## 1. Hypothesis under test

> PAC/Valiant-style (ε,δ) certification — and a single "verification deficit" number —
> do **not** exist as a category in climate modelling. Uncertainty is handled as
> ensemble spread / scenario spread, not as a formal certificate; and no one has
> computed, as one number, how many of a projection's driving quantities are *measured*
> vs *parameterized*.

This is the climate analogue of the finding that opened string-theory V2: the field
converges on verification from several sides but has no tool for the regime where
*ground truth is absent* — guard against known failure modes, not against "the wrong
answer."

## 2. Method — the five angles (running)

| # | angle | question |
|---|---|---|
| 1 | formal verification | any PAC/(ε,δ)/formal-methods/machine-checked work in climate science? |
| 2 | projection calibration | is projection uncertainty a formal guarantee, or a spread of models? |
| 3 | AI emulators | GraphCast/NeuralGCM/ClimSim — is there ANY guarantee over their predictions? |
| 4 | measured vs parameterized | has anyone counted measured vs tuned/assumed driving quantities? |
| 5 | constraint-first / falsification | emergent constraints as the closest analogue; is there a guard-suite? |

## 3. The deficit-transfer framework (how `m` generalises — the durable spine)

In pacland the **Mitchell Verification Deficit** `m` counts observables that are
simultaneously **measured + computable + validated**, and the certificate radius scales
as `1/√m`. Mapped onto climate:

**The prediction.** A projection `P(t)` of some quantity — global-mean surface
temperature, sea level, ice-sheet mass, precipitation pattern, crop yield, extreme-event
frequency — is the thing being verified.

**The verifier is imperfect — twice over.** The two-level certificate splits into:
- **candidate-vs-oracle** — model spread / emulator-vs-full-model error (estimable by
  sampling the ensemble);
- **oracle-vs-truth** — model-vs-observation error, estimable *only on the historical
  record*, the one place ground truth exists.

**The deficit `m` for climate** = the number of quantities that are simultaneously
*measured* (instrumental record, paleo proxies, reanalysis), *computable* (the model
outputs this quantity), and *validated* (the model reproduces it within tolerance on the
historical period). Every other quantity the model projects is **extrapolated** — no
measurement to validate against, hence no certificate term, hence it does not count
toward `m`. The honest sentence becomes: *the certificate on a 2100 projection is
bounded by how many of its driving quantities we can validate on the past — not by how
much we can compute.*

**Constraint-first maps cleanly.** A climate model's reliable content is:
- **constraints** — conservation laws (energy budget, water balance, carbon budget) and
  *emergent constraints* (observation-conditioned bounds, e.g. Hall & Qu 2006; Cox et
  al. 2018) — the "what it forbids";
- **labels** — the resolved/discretized structure (grid, resolved vs sub-grid, the model
  family);
- **parameters** — the sub-grid parameterizations and tuning constants — the free values.

**The four walls, in climate's terms:**
- **unmeasurable** → future projections have no ground truth → deliverable is the
  *deficit*, not the projection;
- **underdetermined** → many parameter sets fit history (equifinality) → deliverable is
  the *emergent constraints / invariants*, not "the right parameter set";
- **intractable** → full high-resolution coupled simulation → structure that shortcuts it
  (emulators, downscaling), or prove the cost;
- (no clean undecidable wall — note its absence honestly.)

## 4. Results (complete — 5/5 returned)

| angle | verdict | closest prior art | gap |
|---|---|---|---|
| 1 formal verification | **needs scoping** | formal *software* verification exists — KeYmaera X + CIVL proved the KPP ocean-mixing invariant (K>0) after finding a defect ([arXiv:2510.13425](https://arxiv.org/abs/2510.13425)); NCAR "Correctness and Reproducibility" workshop | verifies **program properties**, never a statistical (ε,δ) certificate on scientific verifiability; PAC/Valiant theory absent |
| 2 projection calibration | **hypothesis holds** | IPCC AR6 *calibrated language* (evidence×agreement + likelihood scale); UKCP18/CPDN Bayesian posteriors (no coverage guarantee); nearest formal art = **Harris & Sriver 2024 "conformal ensembles"** ([arXiv:2408.06642](https://arxiv.org/abs/2408.06642)); **Pendergrass 2026 "Could Climate Projections Be Verifiable?"** ([10.1002/met.70200](https://doi.org/10.1002/met.70200)) | linguistic/posterior/spread, not a certificate; conformal coverage is marginal + about prediction sets, not a PAC "correct within ε"; no deficit `m`, no `1/√m` radius |
| 3 AI emulators | **hypothesis holds** | skill = RMSE/ACC/CRPS, empirically assessed (GraphCast [2212.12794](https://arxiv.org/abs/2212.12794), Pangu [2211.02556](https://arxiv.org/abs/2211.02556), GenCast [2312.15796](https://arxiv.org/abs/2312.15796)); ACE "reproduces reference climate, >90% of tracked variables" ([2310.02074](https://arxiv.org/abs/2310.02074)) | "verification" is **fidelity-to-a-reference-GCM**, never reality-fidelity; conformal only in-sample; GeoCert certifies constraint feasibility, unvalidated; no (ε,δ), no deficit |
| 4 measured vs parameterized | **hypothesis holds** | Hourdin et al. 2017 — a GCM has "hundreds of free parameters, only a few tens tuned" ([BAMS](https://journals.ametsoc.org/view/journals/bams/98/3/bams-d-15-00135.1.xml)); Regayre et al. 2026 named-parameter aerosol PPE ([ACP 26:2487](https://acp.copernicus.org/articles/26/2487/2026/)); tuning *understates* uncertainty ([SciAdv](https://www.science.org/doi/10.1126/sciadv.adf2758)) | the split is named but **never aggregated to a number**; no `m`, no certificate; spread only |
| 5 constraint-first | **hypothesis holds** | Oreskes et al. 1994 ("earth models can never be verified, only *confirmed* by surviving falsification"); emergent constraints (Hall & Qu 2006; Cox et al. 2018, later shown non-robust; Hall et al. 2019); conservation-law *logs* (ClimaCoupler ConservationChecker; Irving et al. 2021 CMIP6 mass/energy drift) | no guard-suite a model must *pass*; conservation checks are drift logs, not certificates; no (ε,δ) guarantee, no deficit number |

---

## 5. Verdict

**Hypothesis confirmed — scoped.** Four of five angles hold outright; the fifth scopes
rather than refutes. The precise finding:

> **The PAC/Valiant object — a computable (ε,δ) certificate plus a single scalar
> "verification deficit" `m` — does not exist anywhere in climate science.** The field
> handles uncertainty as ensemble spread, Bayesian posteriors, or *calibrated language*.
> What formal machinery exists verifies the wrong thing (program correctness), or a
> weaker thing (marginal conformal coverage), and never a PAC-style "correct within ε"
> certificate with a `1/√m` radius.

**Conflations recorded (fan-out catches — the reason the fan-out was worth it):**

1. **"No formal verification in climate" is false as stated** (angle 1). A real
   machine-checked-*software* program exists (KeYmaera X / CIVL / the KPP invariant).
   The honest claim is "no *statistical* certificate", not "no formal verification."
2. **"Nothing formal exists" is false as stated** (angles 2–3). Distribution-free
   conformal coverage exists (Harris & Sriver 2024) — but it is a prediction-set
   coverage guarantee, not a certificate that the model is correct within ε, and it has
   no deficit number. Must be named and distinguished, not ignored.

**The field is converging on verification from several sides but has no tool for the
regime where ground truth is absent** — the exact pattern that opened string-theory V2:
formal software V&V, conformal coverage, emergent constraints, conservation diagnostics,
tuning inventories. None is a certificate; none is a deficit.

**The opening, stated precisely:**
- Oreskes et al. 1994 already holds the field's own thesis — *you cannot verify an
  open-system earth model, only falsify it* — and it has stood for 30 years without
  anyone making it quantitative.
- Pendergrass 2026 is literally titled "Could Climate Projections Be Verifiable?" and
  concludes they are "far less developed" than weather.
- The **deficit** is the missing quantitative bridge: *a 2100 projection is certifiable
  only to radius ~1/√m over the `m` observables validated on the historical record —
  everything else is extrapolation, not verification.*

## 6. Chosen target for the deficit report (next step)

**Two layers, one report:**

1. **The CMIP6 observable-set deficit** — score `docs/climate-observables.md` (GMST, EEI,
   OHC, GMSL, sea-ice, AMOC, ENSO, precip, ice sheets, extremes) for *measured +
   computable + validated* on the record, count `m`, and attach the `1/√m` radius to the
   2100 projection. Anchors already in hand: **Irving et al. 2021** (per-model mass/energy
   drift → the constraint side, already computed) and **Hourdin et al. 2017** (measured-vs-
   tuned split → the parameter side).
2. **The ACE worked example** (the sharpest single finding) — ACE's "verification" is
   *fidelity to a reference GCM, not to reality*; `m` is literally countable from its
   tracked-variable list, so the `1/√m` radius exposes reference-fidelity as the wrong
   certificate. This is the citable headline: *climate "verification" today certifies a
   model against another model, not against the Earth.*

The nearest formal boundary to *extend* (not duplicate) is Harris & Sriver 2024's
conformal ensembles — noted here so the deficit report cites it as adjacent, not as ours.
