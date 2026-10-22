# PACLAND expansion map — where the method applies next

Catch-up question: *"what other areas of science can we apply this method to, where it
will be of most benefit to the world?"*

This is the answer, as a ranked map. It extends the seed already in the explainer
("climate models, fusion simulations, AI systems — anywhere the verifier is itself
imperfect") into a criterion-driven list with a recommendation. Nothing here is a
physics claim; it is a *where next* analysis for the verification discipline.

---

## The recipe — the expandable methodology (how to add a discipline)

Eight steps, distilled from climate and drugs. Run them in order; a result does not
count as *grounded* until steps 2–3 (its own oracle + Rule of Three) are done.

1. **Gap analysis (5-angle fan-out).** Confirm no (ε,δ) certificate / verification
   deficit exists in the field (`docs/research-fanout.md`).
2. **Name the oracle.** The always-true answer — what *must* hold. (climate: `piControl`
   → zero drift; drugs: chemical validity.)
3. **Name the Rule of Three.** Three independent ways a wrong answer shows.
   (climate: energy + mass + salt ledgers; drugs: validity + drug-likeness +
   synthesizability.)
4. **Build the deficit.** measured + computable + validated → `m` → radius `1/√m`.
5. **Build the guards.** The constraints, each mutation-tested (must be able to fire).
6. **Run on real data.** The discipline's own dataset (climate: Irving 2021; drugs: MOSES).
7. **Write the explainer.** Headlines + the finding, auto-generated from the modules.
8. **Drop into the trust board.** A ranked entry, tiered by how many checks fail.

---

## Playbook status

| # | Field | Status |
|---|---|---|
| 1 | **Climate / Earth-system modelling** | **built + grounded** (oracle + 3 ledgers, real data) |
| 2 | **Drug discovery / protein science** | **built + grounded** (oracle + 3 checks; real-data run pending) |
| 3 | Epidemiology / disease modelling | queued |
| 4 | Valiant Verification (software & AI) | the verified-badge lane |
| 5 | Materials discovery | queued |
| 6 | Quantum-computation verification | queued |
| 7–10 | condensed matter, genomics, neuroscience, economics | queued (foundational) |

---

## 1. What actually transfers (the reusable spine)

Not the string-theory theorems — the *method*. Five field-agnostic components:

1. **The two-level (ε,δ) certificate with an imperfect verifier.** Replace "it is
   correct" with "it is correct within ε with confidence δ", where the verifier itself
   has bounded error. This is the single most portable piece: it applies anywhere the
   *model* is the only "oracle" and ground truth is scarce or absent.
2. **The verification deficit `m`.** The count of observables simultaneously measured +
   computable + validated, and the certificate radius that scales as `1/√m`. It turns
   "this field is untestable" into a number with a denominator — and the number tells
   you *where* effort pays (more measured points, not more compute).
3. **Constraint-first decomposition.** Split a theory's exact content into *constraints*
   (what it forbids), *labels* (topology / handed data), and *parameters* (free values).
   The falsifiable claim: **a model predicts relations/invariants, never values.**
4. **The four-walls map.** intractable → prove intractability or find structure ·
   unmeasurable → compute the deficit · underdetermined → compute the invariants ·
   undecidable → prove undecidability. "Use the wall, don't hit it."
5. **Verification where ground truth is absent** — mutation-tested guards over known
   failure modes (symmetries, invariants, bounds), the Rule of Three, free validation
   targets from symmetry, machine-checked proofs (Lean), and adversarial fan-out.

The first four are the spine; #5 is the engineering that makes them honest.

---

## 2. The fit criteria (the shape that makes a field worth the effort)

A field is a strong target when it has **several** of these:

- a **landscape** — a combinatorial space of candidate models/parameters, not one model;
- **ground truth absent or expensive** — the "unmeasurable" wall, so verification
  against known failure modes is the only verification available;
- **expensive or disputed computation** — predictions that cost money to make and are
  argued about because no one can check them;
- **overclaimed predictions** — a theory that asserts *values* it cannot derive;
- **symmetries / invariants / conservation laws** — free known-answer targets;
- a place where **"forbidden vs allowed" is itself the actionable answer** (constraints
  are the deliverable, not a stepping stone).

Every field below is scored against these, then ranked by **benefit to the world**.

---

## 3. The ranked map

Ranked by world benefit. For each: *why it fits, what transfers, first artifact, benefit.*

### Tier 1 — the two that change the most lives

**1. Climate / Earth-system modelling** *(highest technical fit + highest policy leverage)*
- **Why it fits:** the ensemble of models *is* a landscape; century-scale projections
  have **no ground truth until it is too late** (the unmeasurable wall in its purest
  form); the two-level certificate's "imperfect verifier" is *literally* the model-vs-
  reality gap the IPCC already struggles to state honestly. Constraint-first maps
  cleanly: conservation laws / the energy budget are the *constraints*, the sub-grid
  parameterizations are the *free parameters*.
- **What transfers:** all five components, no adaptation needed. The headline number —
  "the verification deficit of a climate projection" — is a publishable, citable,
  policy-legible quantity that does not exist today as a single figure.
- **First artifact:** a deficit report on one benchmark (e.g. CMIP-style ensemble →
  "how many of the fields driving the projection are measured + computable + validated
  vs parameterized"), with the (ε,δ) radius attached.
- **Benefit:** feeds decisions worth trillions and affects everyone; this is where
  overclaiming currently costs the most.

**2. Drug discovery / protein & molecular science**
- **Why it fits:** chemical space (~10⁶⁰) is the largest *named* landscape; expensive
  compute (docking, folding, simulation); ground truth = scarce assay/clinical data.
  AlphaFold ships a per-residue confidence (pLDDT) but there is **no (ε,δ) certificate
  across a screening campaign** — a model is "right" per-prediction, never per-decision.
- **What transfers:** the two-level certificate (oracle = the surrogate model), the
  deficit (`m` = validated binders vs predicted), and *constraint-first* — a molecule's
  forbidden states (instability, un-synthesizability, toxicity) are far more reliable
  than its predicted *affinity*, so "rule out" beats "rank".
- **First artifact:** a falsification guard-suite over a docking/folding output — does a
  candidate violate a known constraint — with mutation tests proving the guards fire.
- **Benefit:** population-scale health, and the one field where the money to fund it
  already exists.

### Tier 2 — lives at scale, plus the highest-leverage target of all

**3. Epidemiology / infectious-disease modelling**
- **Why it fits:** the identifiability problem is the **underdetermined** wall exactly —
  many parameter sets fit the same data, so "which parameters did the model actually
  earn?" is the question. 2020 is the case study in overclaimed predictions eroding
  trust and costing lives.
- **What transfers:** the deficit (measured vs *assumed* parameters), constraint-first
  (the next-generation matrix, conservation structure), and the four-walls map.
- **First artifact:** a per-model deficit: "of N parameters, M are measured, the rest
  are assumed — here is the certificate radius on the headline projection."
- **Benefit:** pandemic preparedness; a number like this is politically legible.

**4. AI-safety / capability verification** *(highest leverage, and home turf)*
- **Why it fits:** the method is *already* the discipline that built the SDK — guards,
  mutation testing, adversarial review, machine-checked properties, (ε,δ) certificates.
  "What can this model be guaranteed to do / not do" is verification-where-ground-truth-
  is-absent by definition.
- **What transfers:** all five, unchanged. The one genuinely new move is pointing the
  already-built machine at the *thing Rob is building* (Morpheus/MorpheOS) rather than
  at string theory.
- **First artifact:** a constraint-first guard-suite over one concrete claim (e.g.
  "this model never emits X under conditions Y"), mutation-tested.
- **Benefit:** downside risk at civilisation scale; and it is the only target where the
  tooling is already built and just needs re-aiming.

### Tier 3 — concrete, energy-adjacent

**5. Materials discovery (batteries, catalysts, superconductors)**
- **Why it fits:** "stable vs metastable" and "synthesizable vs not" are **constraint**
  questions; DFT is the expensive-oracle wall; the deficit = validated vs *predicted*
  materials. Feeds climate mitigation directly.
- **First artifact:** a stability/synthesizability falsification suite over a structure-
  prediction output, mutation-tested.

**6. Quantum-computation verification**
- **Why it fits:** "certify a computation you cannot directly observe" is the two-level
  bound's native habitat (interactive proofs, self-testing). Deep and clean.
- **Benefit:** trust in the next generation of compute; high, but further out.

### Tier 4 — deeper science, lower immediate world-benefit (foundational)

**7. Condensed matter / strongly-correlated systems** — the natural *next physics*
(same math: many-body Hilbert space = landscape; the QMC sign problem = the intractable
wall). Foundational, and it feeds #5.

**8. Genomics / polygenic prediction** — "how much of a phenotype is learnable
(heritability) vs noise" is a PAC question; "missing heritability" is a deficit number.

**9. Neuroscience** — "does this model explain the data?" is underdetermined (many
models fit the same data); connectome-scale compute is expensive.

**10. Economics / policy evaluation** — causal identifiability is the underdetermined
wall; high policy benefit but no clean symmetries, so the guard-suite half transfers
better than the constraint-first half.

---

## 4. Recommendation

**Start with climate, and re-aim the already-built machine at AI in parallel.**

- **Climate is the flagship** because it is the cleanest technical transfer (the
  imperfect-verifier bound is literally the model-vs-reality gap) *and* the highest
  policy leverage: a "verification deficit of a climate projection" is a single,
  defensible, citable number the field does not currently have.
- **AI is the cheap second lane** because the tooling already exists — it is the SDK the
  mesh is already running — so the marginal cost is one gap-analysis pass, not a build.

Both share the same first step, which we already know how to do because it is exactly
what V2's plan did for string theory: **run the gap analysis** — confirm (or refute) the
"no (ε,δ) certification exists here" hypothesis per field, before committing build time.

## 5. Honest limits (so this never overclaims)

- **Constraint-first needs a symmetry/duality group to be *provable*.** The flux theorem
  was provable only because Sp + the First Fundamental Theorem existed. Fields without a
  clean symmetry group (economics, neuroscience) get the *heuristic* version — useful,
  not a theorem. Say so.
- **The deficit number is a characterisation, not a prediction.** It says "you are here,"
  not "here is the answer." It is the same honesty rule v1 carried.
- **This map is an analysis, not a verified gap study.** Each field's "no certificate
  exists" claim is a hypothesis to be confirmed with the same research fan-out that
  produced `string-landscape-ML-gap-analysis.md`, before any code is written.
