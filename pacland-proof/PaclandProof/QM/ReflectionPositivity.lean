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

/-- **The `1 + cos(2·)` kernel is positive-definite** — the sum of the constant kernel `(Σ c)²` and the
`cos(2·)` kernel `(Σ c cos 2θ)² + (Σ c sin 2θ)²`, both non-negative. No division, so the double-sum
normalisation is cheap (it mirrors `cos_kernel_posdef`). -/
theorem one_plus_cos_two_posdef {m : ℕ} (θ : Fin m → ℝ) (c : Fin m → ℝ) :
    0 ≤ ∑ i : Fin m, ∑ j : Fin m, c i * c j * (1 + Real.cos (2 * (θ i - θ j))) := by
  have h : (∑ i : Fin m, ∑ j : Fin m, c i * c j * (1 + Real.cos (2 * (θ i - θ j))))
      = (∑ i : Fin m, c i) ^ 2 + (∑ i : Fin m, c i * Real.cos (2 * θ i)) ^ 2
          + (∑ i : Fin m, c i * Real.sin (2 * θ i)) ^ 2 := by
    simp_rw [mul_add, mul_one]
    simp_rw [Finset.sum_add_distrib]
    simp_rw [mul_sub]
    simp_rw [Real.cos_sub]
    simp_rw [mul_add]
    simp_rw [Finset.sum_add_distrib]
    rw [pow_two, pow_two, pow_two]
    simp_rw [Finset.sum_mul_sum]
    ac_rfl
  rw [h]
  nlinarith [sq_nonneg (∑ i : Fin m, c i),
    sq_nonneg (∑ i : Fin m, c i * Real.cos (2 * θ i)),
    sq_nonneg (∑ i : Fin m, c i * Real.sin (2 * θ i))]

/-- **cos² is positive-definite** — `cos²x = (1 + cos 2x)/2`, half of the already-proved
`1 + cos(2·)` kernel. -/
theorem cos_sq_posdef {m : ℕ} (θ : Fin m → ℝ) (c : Fin m → ℝ) :
    0 ≤ ∑ i : Fin m, ∑ j : Fin m, c i * c j * (Real.cos (θ i - θ j)) ^ 2 := by
  have h2cos : 0 ≤ ∑ i : Fin m, ∑ j : Fin m, c i * c j * (2 * Real.cos (θ i - θ j) ^ 2) := by
    rw [show ∑ i : Fin m, ∑ j : Fin m, c i * c j * (2 * Real.cos (θ i - θ j) ^ 2)
        = ∑ i : Fin m, ∑ j : Fin m, c i * c j * (1 + Real.cos (2 * (θ i - θ j))) by
        apply Finset.sum_congr rfl
        intro i hi
        apply Finset.sum_congr rfl
        intro j hj
        have hcos : 2 * Real.cos (θ i - θ j) ^ 2 = 1 + Real.cos (2 * (θ i - θ j)) := by
          have h2 : Real.cos (2 * (θ i - θ j)) = 2 * Real.cos (θ i - θ j) ^ 2 - 1 :=
            Real.cos_two_mul (θ i - θ j)
          linarith
        rw [hcos]]
    exact one_plus_cos_two_posdef θ c
  have hpull : ∑ i : Fin m, ∑ j : Fin m, c i * c j * (2 * Real.cos (θ i - θ j) ^ 2)
      = 2 * (∑ i : Fin m, ∑ j : Fin m, c i * c j * (Real.cos (θ i - θ j)) ^ 2) := by
    ring_nf
    simp_rw [Finset.sum_mul]
  rw [hpull] at h2cos
  exact (mul_nonneg_iff_of_pos_left (by norm_num : 0 < (2 : ℝ))).mp h2cos

/-- **The product-to-sum identity** (real angle `n`, no `ℕ`-smul coercion): `cos θ · cos(nθ) =
(cos((n+1)θ) + cos((n−1)θ))/2` — the building block of the Chebyshev recursion that expresses `cos^m`
as a non-negative sum of `cos(k·)` kernels. -/
theorem cos_mul_cos_n (θ : ℝ) (n : ℝ) :
    Real.cos θ * Real.cos (n * θ) = (Real.cos ((n + 1) * θ) + Real.cos ((n - 1) * θ)) / 2 := by
  have hsum : Real.cos ((n + 1) * θ) + Real.cos ((n - 1) * θ)
      = Real.cos (θ + n * θ) + Real.cos (θ - n * θ) := by
    rw [show (n + 1) * θ = θ + n * θ by ring]
    rw [show (n - 1) * θ = n * θ - θ by ring]
    rw [show Real.cos (n * θ - θ) = Real.cos (θ - n * θ) by
      rw [show θ - n * θ = -(n * θ - θ) by ring]
      rw [Real.cos_neg]]
  rw [hsum]
  rw [Real.cos_add, Real.cos_sub]
  ring

/-- **cos³ = (3·cos θ + cos 3θ)/4** — the Chebyshev reduction for `n = 3`, from the product-to-sum. -/
theorem cos_cube_eq (θ : ℝ) :
    Real.cos θ ^ 3 = (3 * Real.cos θ + Real.cos (3 * θ)) / 4 := by
  have hcos2 : Real.cos θ ^ 2 = (1 + Real.cos (2 * θ)) / 2 := by
    have h := Real.cos_two_mul θ
    linarith
  have hmul : Real.cos θ * Real.cos (2 * θ) = (Real.cos (3 * θ) + Real.cos θ) / 2 := by
    have h := cos_mul_cos_n θ (2 : ℝ)
    norm_num at h
    exact h
  have hmul' : Real.cos (θ * 2) * Real.cos θ = (Real.cos (3 * θ) + Real.cos θ) / 2 := by
    simpa [mul_comm, mul_left_comm, mul_assoc] using hmul
  rw [pow_succ, hcos2]
  ring_nf
  rw [hmul']
  ring_nf

end QM
