# Drug-discovery gap analysis — does (ε,δ) certification exist in computational chemistry?

Status: **complete — 5/5 returned** (2026-10-22). Discipline #2, playbook item #2.
The same 5-angle method that produced `docs/climate-gap-analysis.md`.

## 1. Hypothesis under test

> PAC/Valiant-style (ε,δ) certification — and a single "verification deficit" number —
> do **not** exist as a category in drug discovery. "Verification" is benchmark error
> (RMSE/AUC) or per-prediction confidence (pLDDT), never a formal certificate; and no one
> collapses measured-vs-predicted into one number.

## 2. Method — the five angles

| # | angle | question |
|---|---|---|
| 1 | formal verification | any PAC/(ε,δ)/machine-checked work in cheminformatics / force fields / QSAR? |
| 2 | prediction calibration | is affinity/structure uncertainty a guarantee, or a confidence score? |
| 3 | AI/ML models | AlphaFold / docking / generative / MLIP — any certificate over their predictions? |
| 4 | measured vs predicted | has anyone counted measured vs predicted in a screening campaign? |
| 5 | constraint-first / falsification | are the rule-out filters already constraint-first? is there a certified guard-suite? |

## 3. The deficit-transfer framework (how `m` generalises — the durable spine)

Mapped from pacland onto drug discovery:

- **The prediction.** A hit/lead candidate's activity — binding affinity (Kd/Ki/IC50),
  an ADMET endpoint, or toxicity.
- **The verifier is imperfect twice over.** The two-level certificate splits into
  *candidate-vs-oracle* (the ML/docking model vs the benchmark) and *oracle-vs-truth*
  (the benchmark vs a **prospective** assay). Benchmarks are retrospective; the assay
  that matters is prospective.
- **`m`** = the number of observables simultaneously *measured* (an assay value exists),
  *computable* (the model predicts it), and *validated* (the prediction reproduces the
  measurement). On a benchmark (PDBbind, TDC, DUD-E) `m` is the measured set; for a
  **novel molecule there is no assay yet → `m = 0`**, and the prediction is extrapolation.
- **Constraint-first maps onto an already-mature practice.** A molecule's *forbidden*
  states — PAINS/Brenk/REOS substructures, Ro5 property bounds, valency/charge/tautomer
  inconsistency, un-synthesizability — are the reliable content ("rule out beats rank").
  The scaffold/assay is the label; the affinity/ADMET value is the free parameter.
- **The four walls, in drug-discovery terms:** *unmeasurable* → a novel molecule has no
  assay (the deficit) · *underdetermined* → many molecules fit the same SAR (the
  constraints) · *intractable* → FEP/MD cost (structure that shortcuts it) · no clean
  undecidable wall.

## 4. Results (complete)

| angle | verdict | closest prior art | gap |
|---|---|---|---|
| 1 formal verification | **needs scoping** | machine-checked proofs exist — **LeanLJ** (LJ energy vs NIST, [arXiv:2505.09095](https://ar5iv.labs.arxiv.org/html/2505.09095)); **Proof-Carrying Materials** (MLIP safety certs, [arXiv:2603.12183](https://ar5iv.labs.arxiv.org/html/2603.12183)); ASME V&V 40 = credibility framework | proves **code/derivation** correctness, never statistical error vs experiment; PAC (ε,δ) + deficit `m` absent |
| 2 prediction calibration | **holds (largely)** | pLDDT/PAE *not* calibrated (Vander Meersche et al. 2025 [Structure](https://hal.science/hal-05474189v1)); ensemble/Bayesian = score, not cert; conformal = closest (marginal coverage) | confidence scores uncalibrated; benchmark = population RMSE/AUC; no per-instance certificate |
| 3 AI/ML models | **holds** | TDC/MoleculeNet leaderboards; **TDC rankings themselves leaky** (2026 [JCIM](https://tdcommons.ai/) audit); MLIP uncertainty miscalibrated out-of-box | benchmark error, not a per-instance bound; breaks under scaffold/target shift; no deficit |
| 4 measured vs predicted | **holds** | **Zhu et al. 2013** ([doi:10.1021/jm301916b](https://doi.org/10.1021/jm301916b)): of 398 reported VS hits, **52% fail REOS, 18% PAINS, 17% direct-binding**; DUD-E/PDBbind = measured yardsticks | enrichment/ROC = retrospective ranking, not measured-vs-predicted; no per-pipeline deficit |
| 5 constraint-first | **holds** | PAINS/Brenk/REOS/Ro5/RDKit-sanitization *are* constraint-first, but as boolean heuristics; MOSES reports validity+filters | no certified guard-suite a model must *pass*; rule-out never wrapped as a bound |

## 5. Verdict

**Hypothesis confirmed — scoped.** Four of five hold outright; the fifth scopes rather
than refutes. The precise finding:

> **The PAC/Valiant object — a computable (ε,δ) certificate plus a single scalar
> "verification deficit" `m` — does not exist anywhere in drug discovery.** "Verification"
> is a benchmark average or a per-prediction confidence score, and even the benchmark
> numbers are not trustworthy (TDC leaderboard leakage; pLDDT uncalibrated). The
> measured-vs-predicted split is quantified only piecemeal, never as one number.

**Conflations recorded (fan-out catches):**

1. **"No formal verification in drug discovery" is false as stated** (angle 1).
   Machine-checked proofs (LeanLJ, Proof-Carrying Materials) and formal conformal
   coverage exist — but they certify code/derivation correctness or give per-prediction
   coverage, never a PAC certificate or a deficit.
2. **"Constraint-first is our idea" is false in spirit** (angle 5). The field has run
   constraint-first for 25 years — PAINS/Brenk/REOS/Lipinski/RDKit sanitization *are*
   "what the molecule forbids." What is missing is only the *certification*: nobody has
   wrapped them as a bound, and nobody has counted the failures as one number. That is
   the opening — formalise what the field already does, don't invent a new filter.

**The two anchors that make the headline:**
- **Zhu et al. 2013** — the field's own census: of 398 reported virtual-screening hits,
  52% fail REOS and 18% are PAINS, and only 17% got direct-binding validation. The
  "verified" hits were, in large part, artifacts.
- **Vander Meersche et al. 2025** — AlphaFold's pLDDT, the field's most-used confidence
  score, conflates flexibility with uncertainty and is *not* calibrated.

## 6. Chosen target for the deficit report (next step)

Two layers, one report (mirroring climate):

1. **The ADMET/affinity observable-set deficit** — `m` = the measured endpoints/complexes
   a model simultaneously predicts against measured labels. Benchmark: **TDC ADMET
   group** (~22 measured endpoints) or **PDBbind** (each complex = one measured +
   computable + validatable observable). Two tiers: retrospective benchmark (`m` = the
   measured set, weak) vs prospective novel chemical space (`m = 0`, total).
2. **The constraint guard-suite** — wrap the existing forbidden-state filters (RDKit/
   MolVS valency·charge·tautomer, PAINS/Brenk/REOS, RAScore synthesizability) as a
   *certified* guard-suite over **MOSES** validity + filters, mutation-tested.

The citable headline: *a virtual-screening hit is "verified" only retrospectively against
measured actives — its prospective novelty is extrapolation, and the field's own 2013
census shows the "verified" hits were ~18% PAINS and ~52% REOS-failing artifacts.*
