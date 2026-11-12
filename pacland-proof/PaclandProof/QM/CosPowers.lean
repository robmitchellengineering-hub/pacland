import Mathlib
import PaclandProof.QM.PosDefKernel
import PaclandProof.QM.ReflectionPositivity

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Powers of the cosine kernel are positive-definite (the multi-angle input)

The Wilson heat kernel `exp(2β·cos θ)` is a power series in the cosine kernel. This file proves the
building blocks: the constant kernel, the doubled-angle cosine kernel, the square, and the product of
two cosine kernels are all positive-definite. Together with the closure facts (#501), this lifts the
cosine-kernel positivity (#500) toward the full heat kernel.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The product-to-sum identity: `cos a · cos b = (cos(a+b) + cos(a−b))/2`. -/
theorem cos_mul_cos (a b : ℝ) : Real.cos a * Real.cos b = (Real.cos (a + b) + Real.cos (a - b)) / 2 := by
  have h1 := Real.cos_add a b
  have h2 := Real.cos_sub a b
  linarith

/-- The constant kernel is positive-definite: `Σ c_i c_j = (Σ c_i)² ≥ 0`. -/
theorem const_kernel_posdef {α : Type*} [Fintype α] : PosDefKernel (fun _ _ : α => (1 : ℝ)) := by
  intro c
  have h : (∑ i : α, ∑ j : α, c i * c j * (1 : ℝ)) = (∑ i : α, c i)^2 := by
    rw [pow_two]
    rw [Finset.sum_mul_sum]
    simp
  rw [h]
  exact sq_nonneg _

/-- The cosine kernel with a doubled angle is positive-definite (via #500). -/
theorem cos_double_posdef {m : ℕ} (θ : Fin m → ℝ) : PosDefKernel (fun i j => Real.cos (2 * (θ i - θ j))) := by
  intro c
  have h : (∑ i, ∑ j, c i * c j * Real.cos (2 * (θ i - θ j))) = ∑ i, ∑ j, c i * c j * Real.cos ((2 * θ i) - (2 * θ j)) := by
    simp_rw [mul_sub]
  rw [h]
  exact cos_kernel_posdef (fun i => 2 * θ i) c

/-- **The square of the cosine kernel is positive-definite** — the double-angle turns `cos²` into
the positive combination `(1 + cos(2θ))/2`. -/
theorem cos_sq_posdef {m : ℕ} (θ : Fin m → ℝ) : PosDefKernel (fun i j => (Real.cos (θ i - θ j))^2) := by
  have heq : (fun i j => (Real.cos (θ i - θ j))^2) = fun i j => (1 / 2) * ((1 : ℝ) + Real.cos (2 * (θ i - θ j))) := by
    funext i j
    rw [Real.cos_sq]
    ring
  rw [heq]
  exact posdef_smul (fun i j => (1 : ℝ) + Real.cos (2 * (θ i - θ j))) (1 / 2) (by norm_num)
    (posdef_add (fun _ _ : Fin m => (1 : ℝ)) (fun i j => Real.cos (2 * (θ i - θ j))) const_kernel_posdef (cos_double_posdef θ))

/-- **The pointwise product of two cosine kernels is positive-definite**: the product-to-sum turns
`cos(θ_i−θ_j)·cos(φ_i−φ_j)` into the positive combination of two cosine kernels. -/
theorem cos_product_posdef {m : ℕ} (θ φ : Fin m → ℝ) :
    PosDefKernel (fun i j => Real.cos (θ i - θ j) * Real.cos (φ i - φ j)) := by
  have hsum : PosDefKernel (fun i j => Real.cos ((θ i + φ i) - (θ j + φ j)) + Real.cos ((θ i - φ i) - (θ j - φ j))) := by
    exact posdef_add (fun i j => Real.cos ((θ i + φ i) - (θ j + φ j))) (fun i j => Real.cos ((θ i - φ i) - (θ j - φ j)))
      (cos_kernel_posdef (fun i => θ i + φ i))
      (cos_kernel_posdef (fun i => θ i - φ i))
  have heq : (fun i j => Real.cos (θ i - θ j) * Real.cos (φ i - φ j)) = fun i j => (1 / 2) * (Real.cos ((θ i + φ i) - (θ j + φ j)) + Real.cos ((θ i - φ i) - (θ j - φ j))) := by
    funext i j
    rw [cos_mul_cos]
    ring
  rw [heq]
  exact posdef_smul (fun i j => Real.cos ((θ i + φ i) - (θ j + φ j)) + Real.cos ((θ i - φ i) - (θ j - φ j))) (1 / 2) (by norm_num) hsum

end QM
