import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# M3 — the block-spin (coarse-graining) map

The second piece of the weak-coupling multiscale RG scaffolding. The block-spin map groups pairs of
fine links into a coarse link, and the key property is that it **preserves the total holonomy** — the
coarse field carries the same topological information as the fine field. This is the "decimation" step
that lets the multiscale RG integrate out the small-cell fluctuations while keeping the Wilson loop.
-/

open scoped BigOperators

noncomputable section

namespace QM

variable {G : Type*} [CommGroup G]

/-- The block-spin (decimation) map: the coarse link `j` is the product of the two fine links
`U (2j)` and `U (2j+1)`. This is the coarse-graining step of the multiscale RG. -/
def blockSpin (U : ℕ → G) (j : ℕ) : G := U (2 * j) * U (2 * j + 1)

/-- **The block-spin preserves the total holonomy**: the product of `2n` fine links equals the
product of `n` coarse links. The coarse field carries the same topological (holonomy) information. -/
theorem blockSpin_preserves_holonomy (U : ℕ → G) (n : ℕ) :
    (∏ i ∈ Finset.range (2 * n), U i) = (∏ j ∈ Finset.range n, blockSpin U j) := by
  induction' n with n ih
  · simp [blockSpin]
  · rw [Finset.prod_range_succ]
    rw [show 2 * (n + 1) = 2 * n + 2 by ring]
    rw [Finset.prod_range_succ, Finset.prod_range_succ]
    rw [ih]
    dsimp [blockSpin]
    group

/-- **The block-spin map is 1-Lipschitz in the metric group** — the distance between two coarse links is
bounded by the sum of the distances between the two fine links they are built from. This is the metric
input that a contraction estimate for the decimation map starts from. -/
theorem blockSpin_lipschitz {E : Type*} [SeminormedCommGroup E]
    (U V : ℕ → E) (j : ℕ) :
    dist (blockSpin U j) (blockSpin V j) ≤ dist (U (2 * j)) (V (2 * j)) + dist (U (2 * j + 1)) (V (2 * j + 1)) := by
  dsimp [blockSpin]
  exact dist_mul_mul_le (U (2 * j)) (U (2 * j + 1)) (V (2 * j)) (V (2 * j + 1))

/-- **The block-spin contracts a uniform fine-field distance by `2`** — if the two fine links are each
within `D` of each other, the coarse link is within `2D`. This is the coarse-graining contraction per
step (the `2` is the number of links per block); the exponential `e^(−cβ)` rate is the further measure-
concentration step, not this pointwise bound. -/
theorem blockSpin_contracts_two {E : Type*} [SeminormedCommGroup E]
    (U V : ℕ → E) (j : ℕ) (D : ℝ) (hU : dist (U (2 * j)) (V (2 * j)) ≤ D) (hV : dist (U (2 * j + 1)) (V (2 * j + 1)) ≤ D) :
    dist (blockSpin U j) (blockSpin V j) ≤ 2 * D := by
  exact (blockSpin_lipschitz U V j).trans (by linarith)

/-- **The block-spin RG average's weight is positive** — integrating the odd-link `θ₂` out of the
single-plaquette weight `e^(β·cos(θ₁+θ₂))` (the `Re Tr U(2j)·U(2j+1) = cos(θ₁+θ₂)` torus diagonal)
against the Weyl measure `sin²θ₂ dθ₂` stays strictly positive. This is the RG step's renormalised
density — the block-spin average of `μ_β` is a genuine positive weight for every coupling. -/
theorem blockSpin_average_pos (β θ₁ : ℝ) :
    0 < ∫ θ₂ in (0 : ℝ)..Real.pi, Real.exp (β * Real.cos (θ₁ + θ₂)) * (Real.sin θ₂)^2 := by
  refine intervalIntegral.integral_pos Real.pi_pos ?_ ?_ ?_
  · exact (by continuity : Continuous (fun θ₂ : ℝ => Real.exp (β * Real.cos (θ₁ + θ₂)) * (Real.sin θ₂)^2)).continuousOn
  · intro θ₂ hθ₂
    exact mul_nonneg (Real.exp_pos _).le (sq_nonneg (Real.sin θ₂))
  · refine ⟨Real.pi / 2, ?_, ?_⟩
    · exact ⟨by positivity, by linarith [Real.pi_pos]⟩
    · rw [Real.sin_pi_div_two]
      norm_num
      exact Real.exp_pos _

end QM
