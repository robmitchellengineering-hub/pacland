# CKM descent-chain route for Gleason's theorem (the correct closure)

**Reference Lean 4 mechanization:** https://github.com/Bobart0/gleason-theorem-lean (tag `v1.0.3-gleason`, ~7,500 lines). It mechanizes Gleason's theorem via **Cooke–Keane–Moran (1985)**, which **does NOT use continuity**.

## Why continuity was the wrong target

The continuity closure I was grinding is unnecessary. CKM prove `hlat` (f constant on each latitude) via **finite descent chains**, all algebraic/finite (spherical coordinates + a trig estimate), no analytic closure.

## The CKM chain (mapping to our file)

Notation: `E3 := Fin 3 → ℝ`, `⟪x,y⟫ := dotProduct x y`, `‖x‖ := √(dotProduct x x)`, `unitVec3 x := ‖x‖ = 1`.

Definitions (to add):
- `lat p s := (dotProduct s p)^2`
- `northern p := {t | unitVec3 t ∧ 0 ≤ dotProduct t p}`
- `equator p := {t | unitVec3 t ∧ dotProduct t p = 0}`
- `sperp p s := √(1−(dotProduct p s)²) • p − (dotProduct p s) • ((s − (dotProduct p s)•p) / ‖s − (dotProduct p s)•p‖)` — unit, ⊥ s, in plane (p,s)
- `descent p s := {t | t ∈ northern p ∧ dotProduct (sperp p s) t = 0}`

Key lemmas (CKM §2–§6):
- **P3** `frameFunction_pair_swap`: for orthonormal triples `(u,s,t)` and `(u,s',t')` sharing `u`, `f s + f t = f s' + f t'`. (We can derive it from our `two_dim_sum_eq_one_minus_z` + `even_of_frame` + `cross s t = ±u`.)
- **P4** `frameFunction_P4`: if `f s > M − ξ` then `∃ t ⊥ s, f t < m + ξ`. (Uses P3 + a unit vector ⊥ both `s` and `t'` = our `cross`/`exists_perp`.)
- **C2/C3/C4** `basic_lemma` (CKM §4): if `f` attains its sup at `p` (`hmax : ∀ t, f t ≤ f p`), is bounded below by `m₀`, and is constant `= c` on `p`'s equator, then **f decreases along descents**: `s' ∈ descent p s ⟹ f s' ≤ f s`.
- **E2/E4** `piron_chain` (CKM §5): if `lat p t < lat p s` (t closer to equator), there's a **finite chain** `s = c 0 → c 1 → … → c n = t` with each `c (i+1) ∈ descent p (c i)`. Built via spherical coordinates (`spherePoint`) + the trig estimate `spiral_amplification` (Taylor `cos x ≥ 1 − x²/2` + Bernoulli), NO IVT/continuity.
- **E5** `frameFunction_le_of_lat_lt`: `lat p t < lat p s ⟹ f t ≤ f s` (compose piron_chain + chain_decreasing).
- **F block** `frameFunction_exact_pole` (ExactPole.lean): if `f` sup at `p` + constant on equator, then `f s = c + (f p − c)·lat p s` for every unit `s`. Uses `latSup`/`latInf` envelopes + the bounded-additive ⟹ affine lemma.
- **bounded-additive ⟹ affine** (Simplex.lean `bounded_additive_affine`): this is OUR `Cauchy.affine_of_triple_sum`.
- **Attainment** (Attainment.lean): the extremal pole exists (compactness/ultrafilter; we have `unit_sphere_compact`).

## Our existing machinery that maps directly

- `two_dim_sum_eq_one_minus_z` ≈ P3's ingredient (`f x + f y = 1 − f(x×y)`).
- `monotonicity_bound` ≈ a g-weight-2 analogue of `basic_lemma`.
- `Cauchy.affine_of_triple_sum` ≈ `bounded_additive_affine`.
- `symm_latitude_affine` + recover-f (f_minus_Q_antisymm etc.) ≈ the CKM §6 "remove constant-on-equator via symmetrization".
- `gleason_assembly` (hlat ⟹ Born rule) is the final assembly.

## Plan (what to formalize next, in order)

1. Pole geometry: `lat`, `northern`, `equator`, `sperp`, `descent` + `sperp` ⊥ s / unit.
2. `frameFunction_pair_swap` (P3) + `frameFunction_P4` (P4).
3. `basic_lemma` (f decreases along descents).
4. `piron_chain` (finite chains; the hard geometric step).
5. `frameFunction_le_of_lat_lt` ⟹ `hlat` (f constant on each latitude).
6. Close: `gleason_assembly` with `hlat` discharged.

All of this is **finite/algebraic** — no `ContinuousOn`/`UniformContinuousOn`/compactness closure needed for the Born rule itself.

## STATUS: DONE (rounds 92–94)

The CKM route is **vendored, ported, and bridged** — Gleason's theorem is now machine-checked in
pacland-proof, green, committed (branch `foundations/qf0-hinge-ledger`):

- `Gleason/` (17 files, Apache 2.0, from Bobart0/gleason-theorem-lean v1.0.3) — the full proof:
  real-3D core (`frameFunction_regular` = Born rule) + complex n≥3 (`Gleason.gleason`) + Busch.
  Ported to Mathlib v4.35 (6 trivial `Set.restrict`→`Set.domRestrict` deprecation fixes).
  `#print axioms` on `Gleason.gleason` = **propext + Classical.choice + Quot.sound only**; 0 sorries.
- `PaclandProof/Foundations/GleasonBridge.lean` — bridges our native encoding
  (`Fin 3 → ℝ` + `dotProduct` + `FrameFunction3`) to theirs:
  `inner_eq_dotProduct`, `unitVec3_of_norm_eq_one`, `orthVec3_of_inner_zero`,
  `frameFunction3_to_isFrameFunction`, and the final
  **`gleason_born_rule`**: every nonnegative `FrameFunction3 f` is a quadratic form (Born rule).

Full `lake build` green (9081 jobs). The "continuity" step (objective's step 2) is superseded by
the CKM descent-chain proof, which is strictly more elementary (no continuity/compactness needed).
