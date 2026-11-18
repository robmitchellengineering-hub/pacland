# The discovery process — jump taxonomy + jump-seeking loop

Distilled from the history of scientific breakthroughs, so the SEXTANT falsifier-before-believe machinery
can hunt for *jumps* (new ideas), not just falsify known candidates. The goal is a process that maximizes
the odds of a discovery and makes failure informative — for the Yang–Mills mass gap today, for any real
science after.

## The five jump types (with the canonical physics examples)

| # | Type | Historical example | The move |
|---|---|---|---|
| 1 | **Anomaly** | Galileo's moons; the photoelectric effect; the blackbody | find the contradiction the field is ignoring |
| 2 | **Inversion / reframe** | Copernicus (Sun fixed, not Earth); Einstein SR (light's speed fixed, not time) | flip an assumption |
| 3 | **Unification** | Newton (celestial = terrestrial); Maxwell (electricity = magnetism) | two "different" things are one |
| 4 | **Analogy** | Einstein GR (gravity ≈ acceleration); Yang–Mills (local symmetry from general covariance) | a structure from another domain maps over |
| 5 | **New principle** | least action; gauge invariance; the equivalence principle | a postulate that reorganizes the field |

## The jump-seeking loop (five questions, each feeding the falsifier)

```
1. ANOMALY   — what contradiction is the field quietly ignoring?
2. INVERSION — list every assumption; flip each one.
3. UNIFY     — which two "different" objects are secretly the same?
4. ANALOGY   — what structure from another domain maps here?
5. PRINCIPLE — what single postulate would reorganize everything?
   ↓  each answer is a HYPOTHESIS
   ↓  SEXTANT falsifier kills the wrong ones (referee + kernel-check + non-vacuity + U(1) gate)
   ↓  a survivor is a JUMP-CANDIDATE
```

The system cannot guarantee the jump — the jump is the rare "aha" that survives falsification — but it can
*enumerate and falsify the candidate jumps*, which is exactly what the historical jumps were: a candidate
that cleared the falsifier.

## Applied to the Yang–Mills mass gap (the working example)

**Rung A — the crossover (Polchinski–Bakry–Émery for gauge).**
- ANOMALY: the single-scale BE curvature is β-dependent and *negative* at the antipode, yet the theory
  still has a gap — the contradiction is "negative curvature ⟹ no gap" is the wrong sufficient condition.
- INVERSION: instead of "the bare action's curvature must be positive", ask "must the *effective* action's
  curvature at each scale be positive?" (this is exactly the multiscale BE — the inversion we already
  started).
- UNIFY: the sine-Gordon β < 6π criterion and the gauge-theory UV hypotheses are secretly one — a single
  multiscale-BE inequality, just in different groups.
- ANALOGY: the Polchinski flow's convexification of the potential = the same "softening" as gradient flow
  on the Ricci curvature (our `GradientFlow.lean` seed).
- PRINCIPLE: "scale-wise curvature positivity" (Γ₂ ≥ κ_Λ Γ at every scale) replaces "bare curvature > 0".

**Rung B — the mass gap itself.**
- ANOMALY: LGT proves the gap at strong coupling; the committee's construction reaches the continuum;
  nothing connects them — the missing object *is* the anomaly.
- INVERSION: instead of "prove Δ > 0", ask "what must be FALSE for Δ = 0?" (a gapless spectrum is a
  massless particle on the light cone — invert to *exclude* it, which `HasMassGap` already states).
- UNIFY: the transfer-matrix gap (our finite-β theorem) and the spectral gap (the Wightman PVM) are one —
  the missing link is `clustering ⟺ gap` at the continuum (the `Semigroup.descent` in the committee repo).
- ANALOGY: the 2D/3D exactly-solvable mass gaps are the template; the 4D obstruction is the *marginal*
  coupling, so the analogy to exploit is "what 3D argument survives when the coupling is dimensionless?"
- PRINCIPLE: "confinement ⟹ mass gap" as a single spectral theorem (the temporal–spatial duality we
  already formalized as `string_tension_iff_gap`).

## The honest boundary

The taxonomy + loop are buildable and are built here. The *jump* — the candidate that survives all five
questions and the falsifier — is still the rare, unguaranteed event. What this process does is make the
search *systematic* and the failures *informative*, which is the highest-leverage thing a discovery system
can do.
