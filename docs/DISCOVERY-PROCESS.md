# The discovery process — jump taxonomy + jump-seeking loop

**Status: HYPOTHESIS, untested.** The five-type taxonomy is a post-hoc reading of history; nothing yet
shows that naming the types produces better hypotheses than an untyped baseline. That is exactly what
`RETRODICTION-TEST.md` is for. Read this doc as a *proposal to be tested*, not an established method.

## The five jump types (candidate taxonomy)

| # | Type | Historical example (corrected) | The move |
|---|---|---|---|
| 1 | **Anomaly** | Galilean moons; the photoelectric effect; the blackbody | find the contradiction the *established* framework cannot absorb |
| 2 | **Inversion / reframe** | Copernicus (Sun fixed, not Earth); Einstein SR (light's speed fixed, not time) | flip an assumption |
| 3 | **Unification** | Newton (celestial = terrestrial); Maxwell (electricity = magnetism) | two "different" things are one |
| 4 | **Analogy** | Einstein GR (gravity ≈ acceleration, the equivalence principle) | a structure from another domain maps over |
| 5 | **New principle** | least action; gauge invariance; the equivalence principle | a postulate that reorganizes the field |

**Corrections to the first draft:**
- **Yang–Mills is NOT "analogy from general covariance."** Yang–Mills came from *extending isospin and
  QED's gauge idea* to a local non-abelian symmetry — a **unification/generalization** of known gauge
  invariance, not an import of a structure from GR. (Mislabelled; fixed.)
- **"Anomaly" is mislabelled in the mass-gap application.** The field already knows Bakry–Émery is only
  *sufficient*, so the single-scale failure is not an ignored contradiction. Drop the "anomaly" framing
  there; it is a *known sufficient-condition mismatch*, not a Kuhnian anomaly.

## The jump-seeking loop (five questions, each feeding the falsifier)

```
1. ANOMALY   — what contradiction is the field quietly ignoring?
2. INVERSION — list every assumption; flip each one.
3. UNIFY     — which two "different" objects are secretly the same?
4. ANALOGY   — what structure from another domain maps here?
5. PRINCIPLE — what single postulate would reorganize everything?
   ↓  each answer is a HYPOTHESIS (a candidate)
   ↓  SEXTANT falsifier kills the wrong ones
   ↓  a survivor is a JUMP-CANDIDATE
```

**Caveat (added):** prompting a model with these five questions is NOT a candidate-production mechanism
by itself. The questions are a *search structure*; the candidate production must be logged and scored in
`CANDIDATE-LEDGER.md`, and the whole thing must beat a baseline in `RETRODICTION-TEST.md` before the
taxonomy earns any claim to "help".

## Applied to the Yang–Mills mass gap

**Rung A — the crossover (Polchinski–Bakry–Émery for gauge).**
- INVERSION: instead of "the bare action's curvature must be positive", ask "must the *effective* action's
  curvature at each scale be positive?" (the multiscale BE — already started).
- UNIFY: the sine-Gordon β < 6π criterion and the gauge-theory UV hypotheses are secretly one — a single
  multiscale-BE inequality in different groups.
- ANALOGY: the Polchinski flow's convexification of the potential ≈ the "softening" in gradient flow on
  curvature. **Not in our files**: `GradientFlow.lean` is only the SU(2) single-plaquette energy
  monotonicity (`θ' = −β·sin θ`, `gradient_flow_monotone`), with no Ricci-flow link. The analogy is a
  *direction*, not a result.
- PRINCIPLE: "scale-wise curvature positivity" (Γ₂ ≥ κ_Λ Γ at every scale) replaces "bare curvature > 0".

**Rung B — the mass gap itself.**
- INVERSION (corrected): "no massless particle" is NOT enough — a continuous spectrum can reach down to 0
  with no massless particle. The real inversion is: *exclude spectrum in (0, Δ) on the vacuum complement*,
  i.e. `projection {0 < time p < Δ} = 0` — which is exactly `HasMassGap` and is as hard as the gap.
- UNIFY: the transfer-matrix gap (finite-β) and the spectral gap (Wightman PVM) are one, via
  `clustering ⟺ gap` at the continuum. **Caveat**: `string_tension_iff_gap` (`MassGapDiamond.lean:91`) is
  a statement about a real number `lam1 > 0`, NOT the lattice measure — the lattice-measure version is
  still open.
- ANALOGY: 2D/3D exactly-solvable gaps as template; the 4D obstruction is the *marginal* coupling, so the
  question is "what 3D argument survives a dimensionless coupling?"
- PRINCIPLE: "confinement ⟹ mass gap" as a single spectral theorem.

**Locations (corrected):** `HasMassGap` lives in `PaclandProof/QM/Committee/MassGapSpec.lean`, with the
sanity controls in `PaclandProof/QM/Committee/SanityControls.lean`. `Semigroup.descent` exists in the
committee repo (`YM/…`), as stated.

## The honest boundary

The taxonomy + loop are a **proposal**, not a result. "Maximizes the odds of a discovery" is **untested**
— there is no benchmark showing it beats a baseline. The three things that make it testable are:
`RETRODICTION-TEST.md` (does it beat baseline, blind, no hindsight), `CANDIDATE-LEDGER.md` (log every
hypothesis with jump type / falsifier / cost / status, fed into the belief layer), and `KILL-CRITERIA.md`
(a budget and a stop rule per rung).
