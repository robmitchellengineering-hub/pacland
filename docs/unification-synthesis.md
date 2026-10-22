# The unification synthesis — fan-out results (2026-10-22)

A four-pass research fan-out asked: *is the flux tadpole the same object as the SM
anomaly cancellation?* It returned a **sharpened claim, not a flat yes/no** — and the
disagreement between two passes is itself the next check.

## The claim, before and after

- **Before:** "the tadpole and the anomaly are the same object — a vanishing
  topological index."
- **After:** three precise parts (below), one of which is still open.

## 1. Same object — Atiyah–Singer, with torsion on both sides (mostly settled)

- **Constructive pass (21d99b05):** both are literally *"a Dirac index / (twisted)
  K-theory class vanishes."* The single theorem is **Atiyah–Singer + Chern
  character**: `index(D) = 0 ⇔ [D] = 0 ∈ K(X)`. The index *is* the rational image of
  a K-class under `ch: K(X)⊗ℚ → H^even(X;ℚ)`. They differ only in *which* Dirac
  operator and *which* K-group.
- **Structural pass (9cfec47b):** objected that the tadpole is natively K-theoretic
  (ℤ₂ torsion, Freed–Witten) while the anomaly is natively its rational image —
  "same only over ℚ." Its own "precise condition for same-object" is the `ch` square
  + Green–Schwarz inflow.
- **Resolution offered by the constructive pass:** the structural pass missed that
  the anomaly *also* has torsion — Witten's ℤ₂ **global** anomaly (detected by KO),
  symmetric with the tadpole's Freed–Witten ℤ₂. If correct, they are the same object
  at full strength, not only rationally.

**Update 2026-10-22 — the check refined "which index."** A sympy expansion of the
Â-genus to degree 6 found it has **no c₃ term** (coefficient 0), so the constructive
pass's literal "O3 charge `−χ/24` = `∫Â(TX)`" is wrong. The tadpole's index is the
**Euler** index (`χ = ∫c₃`, Gauss–Bonnet–Chern), the anomaly's is the **Dirac** index
(`[Â·ch]₆`, Atiyah–Singer). So "same object" sharpens to: **same K-theory *kind*
(both a class whose shadow is a vanishing index), different *index* (Euler vs Dirac).**
The ℤ₂ torsion correspondence is still the open check.

## 2. Three types, not two (refutes the two-type decomposition)

- **Completeness pass (1e89ec43):** a **third kind** of exact structure exists —
  **counting**: exact integer-valued invariants derived by theorem from the
  representation content + symmetry. The concrete instance is the **19 =
  orbit-space dimension** (Molien–Weyl / Hilbert–Serre / Jacobian rank): it forbids
  nothing (not `=0`/`≤L`), and it is not read off geometry (algebraic, a function *of*
  the labels). Same kind in the flux sector: the Ashok–Denef–Douglas signed index,
  Morse bounds.
- This resolves a real internal contradiction: `complete-exact-structure.md` counts
  the 19 as an exact rung, `sm-frontier.md` calls it a free parameter. Both are
  right: **the count is exact; the values are free.**
- `five-pillars.md` already separated "counting" from "labels"; `complete-exact-structure.md`
  folded it away. The three-type decomposition is: **constraint + label + counting.**

## 3. Constraint ↔ label entangled (refutes their independence)

- **Labels pass (2bc75c5f):** a conifold transition moves `h¹¹` → the tadpole bound
  `L` → `N_gen` together through one variable. Neither is landscape-invariant; they
  are the same object viewed twice through `h¹¹`. `N_gen=3` is a label (anomaly
  cancellation is per-generation, blind to the count; `|χ|/2` is integral for free).

## The frontier data backs the constraint (same day)

| h12 | model | critical points | SUSY | tadpole `N_flux` | bound `L` | all ≤ L |
|---|---|---|---|---|---|---|
| 3 | m3 | 40 | **16** | [5, 103], med 48 | 104 | ✅ |
| 4 | m1 | 40 | **2** | [2, 75], med 20 | 76 | ✅ |

Every one of the 80 vacua satisfies `N_flux ≤ L`. The SUSY fraction falls 40% → 5%
as h12 approaches the flat-tower cliff at h12=5 — the constraint holds, the selection
thins.

## The next check (the fan-out's disagreement, made concrete)

Verify the **torsion correspondence**: does `ch: K → H` reproduce both sides *in full*
— the O3/Dirac-index charge `∫Â(TX) = −χ/24` **and** the anomaly polynomial
`P₆ = [Â·ch(F)]₆`, **including the ℤ₂ torsion on each** (Freed–Witten on flux,
Witten global anomaly on SM)?

- Both match → "same object" (constructive pass wins).
- Torsion fails to match → "same only over ℚ" (structural pass wins).

Per the verification config (`docs/verification-config.md`), this is failure mode 1
("structurally different") mapped to its check — and it is the cheapest covering
check, so it runs first.
