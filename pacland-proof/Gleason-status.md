# Gleason's theorem — formalization status

Machine-checked (Lean 4 + Mathlib, `lake build` green) proof of **Gleason's theorem** —
every nonnegative frame function on `ℝ³` is the Born rule. This is the quantum-foundations
arm, separate from the Mitchell/constraint-first arm documented in `README.md`.

## What is proven (all kernel-checked, no `sorry`)

- **Step 1 — algebraic core** (`PaclandProof/Foundations/Gleason.lean`, `Cauchy.lean`):
  `H + P + F ≥ 0 ⟹ F` is a quadratic form (Jordan–von Neumann via polarization +
  Cauchy–Schwarz); Cauchy's equation (bounded additive ⟹ ℝ-linear).
- **Step 3 — assembly** (`Gleason.lean`): a quadratic form `F` is `Tr(ρ·vvᵀ)` with `ρ` PSD,
  trace 1 (Born rule).
- **CKM functional-equation core** (`Cauchy.lean`): `triple_sum_additive`,
  `zero_of_triple_sum`, `affine_of_triple_sum` — a bounded `F` with `F(a)+F(b)+F(c)=W`
  for `a+b+c=1` is affine-linear.
- **Parseval / Binet–Cauchy** (`GleasonLemma.lean`): `(u·p)² + (v·p)² + ((u×v)·p)² = p·p`
  for orthonormal `u ⊥ v`.
- **Realizability** (`GleasonLemma.lean`): for `a+b+c=1` there is an orthonormal triple
  with squared projections `(a,b,c)` — the dim-≥-3 step.
- **The assembly** (`GleasonLemma.lean::gleason_assembly`): a nonnegative frame function
  that is *latitude-invariant* (`f t` depends only on `(t·p)²`) satisfies
  `f t = (f p − f q)·(t·p)² + f q` = `Tr(ρ·ttᵀ)` for the mixed state
  `ρ = (f p − f q)·ppᵀ + f q·I`.

## The one remaining rung

**Step 2 — continuity / latitude invariance** (Gleason's lemma): prove, *from the frame
property alone*, that `f t = f t'` whenever `unitVec3 t`, `unitVec3 t'`, and
`(t·p)² = (t'·p)²`. It is currently the single explicit hypothesis `hlat` in
`gleason_assembly`.

Precise target:

```lean
theorem latitude_invariant (p : Fin 3 → ℝ) (hp : unitVec3 p)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hpos : ∀ x, unitVec3 x → 0 ≤ f x) :
    ∀ t t', unitVec3 t → unitVec3 t' → (dotProduct t p)^2 = (dotProduct t' p)^2 → f t = f t'
```

Once this lands, `gleason_assembly` closes and the theorem is complete.

## What has been tried (and why it does not yet close)

- **2D additivity + boundedness**: `g(θ)+g(θ+π/2)=c` admits discontinuous step-function
  solutions, so these two alone do NOT force continuity.
- **Transport** (`GleasonLemma.lean::transport`): the longitude difference is invariant
  under the 90° rotation of its straddle axis — an invariance, not a contraction.
- **Two-frame functional equation** (`GleasonLemma.lean::two_frame_diff`):
  `f t − f t' = (f w' − f w) + (f z' − f z)` — at `a=0` it collapses to the evenness
  relation, so it is consistent with the step function and does not force `D=0`.
- The longitude difference `D(a,θ) = f(√a·p+√(1−a)·u(θ)) − f(√a·p+√(1−a)·u(θ+π/2))`
  satisfies `D(a,θ) = −D(1−a,θ+π) − D(0,θ+π/2)`; the bounded solution `D=0` needs a
  harmonic/density (cross-plane-consistency) argument that is not yet formalized.
  `polyrith` (the Groebner tactic that would dispatch the relevant polynomial
  identities) is no longer available.

The precise argument is in Richman–Bridges, *A Constructive Proof of Gleason's Theorem*
(CDMTCS-038, 1997) — Gleason's Lemma 2.8 "constant on latitudes" — but it is a PDF not
fetchable as text, and hand-reconstruction has repeatedly hit geometric sign errors.
