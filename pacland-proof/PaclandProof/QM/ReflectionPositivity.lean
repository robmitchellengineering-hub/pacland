import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The cosine kernel is positive-definite (the reflection-positivity input)

The SU(2) Wilson heat kernel is `exp(2β·cos θ)` on the diagonal torus `g = diag(e^{iθ}, e^{-iθ})`.
Its reflection positivity (OS3) is the statement that this kernel is positive-definite, and the
underlying fact is that the **cosine kernel** `cos(θ_i − θ_j)` is positive-definite (the rank-one
factorization `|Σ c_i e^{iθ_i}|² ≥ 0`). This file proves that real-form identity.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The cosine kernel is positive-definite** (the reflection-positivity input): for any finite
set of angles and real coefficients, `Σ_{i,j} c_i c_j · cos(θ_i − θ_j) ≥ 0`. This is the rank-one
factorization `|Σ c_i e^{iθ_i}|² ≥ 0`, written in real form. It is the kernel whose exponential is
the SU(2) Wilson heat kernel. -/
theorem cos_kernel_posdef {m : ℕ} (θ : Fin m → ℝ) (c : Fin m → ℝ) :
    0 ≤ ∑ i : Fin m, ∑ j : Fin m, c i * c j * Real.cos (θ i - θ j) := by
  have h : (∑ i : Fin m, ∑ j : Fin m, c i * c j * Real.cos (θ i - θ j))
      = (∑ i : Fin m, c i * Real.cos (θ i))^2 + (∑ i : Fin m, c i * Real.sin (θ i))^2 := by
    simp_rw [Real.cos_sub]
    rw [pow_two, pow_two]
    simp_rw [Finset.sum_mul_sum]
    simp_rw [mul_add]
    simp_rw [Finset.sum_add_distrib]
    simp [mul_assoc, mul_left_comm, mul_comm]
  rw [h]
  exact add_nonneg (sq_nonneg _) (sq_nonneg _)

/-- **cos² is positive-definite** — the base case of the power-reduction that makes the Wilson heat
kernel `exp(2β·cos)` positive-definite. `cos²x = (1 + cos 2x)/2`, the average of the constant kernel and
the `cos` kernel, both positive-definite. -/
theorem cos_sq_posdef {m : ℕ} (θ : Fin m → ℝ) (c : Fin m → ℝ) :
    0 ≤ ∑ i : Fin m, ∑ j : Fin m, c i * c j * (Real.cos (θ i - θ j)) ^ 2 := by
  have hcos : ∀ x, Real.cos x ^ 2 = (1 + Real.cos (2 * x)) / 2 := by
    intro x
    rw [Real.cos_two_mul]
    have h1 : Real.cos x ^ 2 + Real.sin x ^ 2 = 1 := Real.cos_sq_add_sin_sq x
    linarith
  calc
    ∑ i : Fin m, ∑ j : Fin m, c i * c j * (Real.cos (θ i - θ j)) ^ 2
        = ∑ i : Fin m, ∑ j : Fin m, c i * c j * ((1 + Real.cos (2 * (θ i - θ j))) / 2) := by
          apply Finset.sum_congr rfl
          intro i hi
          apply Finset.sum_congr rfl
          intro j hj
          rw [hcos (θ i - θ j)]
    _ = (1 / 2) * (∑ i : Fin m, ∑ j : Fin m, c i * c j)
          + (1 / 2) * (∑ i : Fin m, ∑ j : Fin m, c i * c j * Real.cos (2 * (θ i - θ j))) := by
          rw [Finset.sum_mul]
          simp_rw [mul_add]
          rw [Finset.sum_add_distrib]
          ring
    _ ≥ 0 := by
          have hconst : 0 ≤ ∑ i : Fin m, ∑ j : Fin m, c i * c j := by
            rw [Finset.sum_mul, Finset.sum_mul]
            simpa [mul_comm] using sq_nonneg (∑ i : Fin m, c i)
          have hcos2 : 0 ≤ ∑ i : Fin m, ∑ j : Fin m, c i * c j * Real.cos (2 * (θ i - θ j)) := by
            simpa using cos_kernel_posdef (fun i => 2 * θ i) c
          nlinarith [mul_nonneg (by norm_num : 0 ≤ (1 / 2 : ℝ)) hconst,
            mul_nonneg (by norm_num : 0 ≤ (1 / 2 : ℝ)) hcos2]

end QM
