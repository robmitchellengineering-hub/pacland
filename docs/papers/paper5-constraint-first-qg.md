# Constraint-First Quantum Gravity, machine-checked

**The unification of quantum mechanics and gravity is the constraint algebra**

*Authors: the pacland proof arm · Date: 2026-11-07 · Repository: `pacland-proof/`*

**DOI:** https://doi.org/10.5281/zenodo.24042472

**Abstract.** We machine-check (Lean 4 / Mathlib) a constraint-first theory of quantum gravity and
state what it contributes. The forced content of QG is the *union* of the two forced halves — the
Born rule (Gleason) and the Einstein equation (Lovelock) — joined by a single constraint `∇·T = 0`,
whose quantum promotion is the Wheeler–DeWitt equation `Ĥ|ψ⟩ = 0` and whose closure is the Dirac
algebra. The coupling is *quantum* (a classical coupling is ruled out) and *free* (its value is a
label, not a prediction). We report three sharpened statements and the machine-checked chain that
produces them, with an honest accounting of what is new versus what is textbook.

## What this contributes (honestly)

**New physics statements (sharpened, falsifiable):**

1. **SM minimality selects `π₁ ≠ 0`.** Scanning the Kreuzer–Skarke list: the famous three-generation
   `(1,4)/(4,1)` manifold has fundamental group `π₁ = Z₁₂` (Braun–Candelas–Davies) and is **not** a
   toric hypersurface; the smallest *toric* `χ = ±6` manifolds have `h¹¹ + h²¹ = 29`, and there are
   `>200,000` of each sign. So three generations is an *abundant* topological label, and the SM's
   *minimality* (small `h¹¹`) is what forces the non-simply-connected quotient. Falsifiable: a
   simply-connected CY with `h¹¹ = 4`, `|χ| = 6`.

2. **The gravitational coupling is free.** `∇·G = 0` involves no coupling, so `G = κT` is consistent
   for every `κ ≠ 0`; `G` (and `Λ`) are labels, like `N_gen` and the 19. A unification that *derives*
   `G` is provably impossible. Falsifiable: a derivation of `G` from the forced halves.

3. **The BMV entangling phase oscillates.** For two `10⁻¹⁴ kg` masses, `100 µm` apart, superposition
   width `10 µm`: the concurrence is `C(t) = |sin(π t / T)|` with `T = 496 s`, reaching `C = 1` at
   `248 s`. The experiment must run below `0.1 K` (thermal photons kill it above). This is a
   specific, lab-confirmable curve, not a monotonic growth.

**New formalization (the machine-checked chain):**

- Gleason (Born rule) → Lovelock (Einstein form) → Bianchi `∇·G = 0` → WdW `Ĥ|ψ⟩ = 0`
  (physical states = `ker Ĥ`) → ADM `{Ĥ = G·ππ − R, Ĥ_a = ∇·π}` → Dirac algebra (structure
  function `q^ab`, antisymmetric). This chain — *the unification is the constraint algebra* — has
  not been machine-checked before, to our knowledge.
- The LOCC-cannot-create-entanglement theorem (`Φ⊗Ψ` preserves product and separable states), the
  algebraic core of the Bose–Marletto–Vedral "gravity must be quantum" test.

**Framing (conceptual):** the four classic QG obstacles — spacetime incompatibility,
non-renormalizability, weakness, singularities/information — are **one free label** (`G`) appearing
in four places, delimited not dissolved.

## What is *not* new (textbook, cited not derived)

Lovelock's theorem, the Wheeler–DeWitt equation, the Dirac algebra, Atiyah–Singer `N_gen = |χ|/2`,
and the BMV phase formula are all established. We did not build string theory or LQG, did not resolve
the information paradox, and did not predict `G`. The contribution is the *certified* constraint-first
assembly of these, plus the three sharpened statements above.

## The theory, in one sentence

**Quantum mechanics and gravity are one constrained system — state space from Gleason, geometry from
Lovelock, the join a single constraint `∇·T = 0`, its quantization `Ĥ|ψ⟩ = 0`, its closure the Dirac
algebra — whose coupling is quantum and free, and whose tabletop signature is the `T = 496 s`
entangling phase.**

## Reproducibility

```
cd pacland-proof && lake build      # green, 9100 jobs; #print axioms = propext, Classical.choice, Quot.sound
python3 scripts/bmv_sim.py          # the BMV phase, oscillation period, decoherence threshold
```
Sources: `PaclandProof/Foundations/GleasonBridge.lean`, `Gravity/{Bianchi,Lovelock,QG,
WheelerDeWitt,ADM,ADMConstraints,Dirac}.lean`, `QM/{NoCloning,Entanglement}.lean`, `SM/{Hypercharge,
Anomaly,Generation}.lean`; `docs/chi-6-scan.md`, `docs/qg-answers.md`, `docs/bmv-number.md`.
