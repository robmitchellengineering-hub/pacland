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

/-- **The truncated Wilson heat kernel is positive-definite** (the OS3 reflection positivity, first
three terms): `1 + 2β·cos + 2β²·cos²` is PSD for `β ≥ 0`, as a non-negative combination of the
positive-definite constant, cosine, and cosine-squared kernels. -/
theorem heat_kernel_truncated_posdef {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) :
    PosDefKernel (fun i j => (1 : ℝ) + (2 * β) * Real.cos (θ i - θ j) + ((2 * β)^2 / 2) * (Real.cos (θ i - θ j))^2) := by
  let K₁ : Fin m → Fin m → ℝ := fun _ _ => (1 : ℝ)
  let K₂ : Fin m → Fin m → ℝ := fun i j => Real.cos (θ i - θ j)
  let K₃ : Fin m → Fin m → ℝ := fun i j => (Real.cos (θ i - θ j))^2
  have hK₁ : PosDefKernel K₁ := by dsimp [K₁]; exact const_kernel_posdef
  have hK₂ : PosDefKernel K₂ := by dsimp [K₂]; exact cos_kernel_posdef θ
  have hK₃ : PosDefKernel K₃ := by dsimp [K₃]; exact cos_sq_posdef θ
  have h1 : PosDefKernel (fun i j => (1 : ℝ) + (2 * β) * K₂ i j) := by
    exact posdef_add K₁ (fun i j => (2 * β) * K₂ i j) hK₁ (posdef_smul K₂ (2 * β) (by nlinarith [hβ]) hK₂)
  have h2 : PosDefKernel (fun i j => (1 : ℝ) + (2 * β) * K₂ i j + ((2 * β)^2 / 2) * K₃ i j) := by
    exact posdef_add (fun i j => (1 : ℝ) + (2 * β) * K₂ i j) (fun i j => ((2 * β)^2 / 2) * K₃ i j) h1
      (posdef_smul K₃ ((2 * β)^2 / 2) (by positivity) hK₃)
  simpa [K₁, K₂, K₃] using h2
/-- The scaled cosine kernel `cos(k·(θ_i−θ_j))` is positive-definite (via #500). -/
theorem cos_scaled_posdef {m : ℕ} (θ : Fin m → ℝ) (k : ℕ) :
    PosDefKernel (fun i j => Real.cos ((k : ℝ) * (θ i - θ j))) := by
  intro c
  have h : (∑ i, ∑ j, c i * c j * Real.cos ((k : ℝ) * (θ i - θ j))) = ∑ i, ∑ j, c i * c j * Real.cos (((k : ℝ) * θ i) - ((k : ℝ) * θ j)) := by
    simp_rw [mul_sub]
  rw [h]
  exact cos_kernel_posdef (fun i => (k : ℝ) * θ i) c

/-- The triple-angle expansion: `cos³(θ) = (3cos θ + cos 3θ)/4`. -/
theorem cos_cube_expansion (θ : ℝ) : (Real.cos θ)^3 = (3 * Real.cos θ + Real.cos (3 * θ)) / 4 := by
  have h := Real.cos_three_mul θ
  linarith

/-- **The cube of the cosine kernel is positive-definite** — the triple-angle turns `cos³` into
the positive combination `(3cos θ + cos 3θ)/4`. -/
theorem cos_cube_posdef {m : ℕ} (θ : Fin m → ℝ) : PosDefKernel (fun i j => (Real.cos (θ i - θ j))^3) := by
  have heq : (fun i j => (Real.cos (θ i - θ j))^3) = fun i j => (3 / 4) * Real.cos (θ i - θ j) + (1 / 4) * Real.cos (3 * (θ i - θ j)) := by
    funext i j
    rw [cos_cube_expansion]
    ring
  rw [heq]
  exact posdef_add (fun i j => (3 / 4) * Real.cos (θ i - θ j)) (fun i j => (1 / 4) * Real.cos (3 * (θ i - θ j)))
    (posdef_smul (fun i j => Real.cos (θ i - θ j)) (3 / 4) (by norm_num) (cos_kernel_posdef θ))
    (posdef_smul (fun i j => Real.cos (3 * (θ i - θ j))) (1 / 4) (by norm_num) (cos_scaled_posdef θ 3))
/-- The quadruple-angle expansion: `cos⁴(θ) = (3 + 4cos 2θ + cos 4θ)/8`. -/
theorem cos_four_expansion (θ : ℝ) : (Real.cos θ)^4 = (3 + 4 * Real.cos (2 * θ) + Real.cos (4 * θ)) / 8 := by
  have h1 : (Real.cos θ)^4 = ((Real.cos θ)^2)^2 := by ring
  rw [h1, Real.cos_sq]
  -- ((1 + cos 2θ)/2)² = (1 + 2cos 2θ + cos² 2θ)/4
  have h2 : (1 / 2 + Real.cos (2 * θ) / 2)^2 = (1 + 2 * Real.cos (2 * θ) + (Real.cos (2 * θ))^2) / 4 := by
    ring_nf
  rw [h2]
  have h3 : (Real.cos (2 * θ))^2 = 1 / 2 + Real.cos (4 * θ) / 2 := by
    have h := Real.cos_sq (2 * θ)
    rw [show 2 * (2 * θ) = 4 * θ by ring] at h
    exact h
  rw [h3]
  ring_nf

/-- **The fourth power of the cosine kernel is positive-definite** — the quadruple-angle turns
`cos⁴` into the positive combination `(3 + 4cos 2θ + cos 4θ)/8`. -/
theorem cos_four_posdef {m : ℕ} (θ : Fin m → ℝ) : PosDefKernel (fun i j => (Real.cos (θ i - θ j))^4) := by
  have heq : (fun i j => (Real.cos (θ i - θ j))^4) = fun i j => (3 / 8) * (1 : ℝ) + (4 / 8) * Real.cos (2 * (θ i - θ j)) + (1 / 8) * Real.cos (4 * (θ i - θ j)) := by
    funext i j
    rw [cos_four_expansion]
    ring
  rw [heq]
  exact posdef_add (fun i j => (3 / 8) * (1 : ℝ) + (4 / 8) * Real.cos (2 * (θ i - θ j)))
      (fun i j => (1 / 8) * Real.cos (4 * (θ i - θ j)))
    (posdef_add (fun _ _ : Fin m => (3 / 8) * (1 : ℝ)) (fun i j => (4 / 8) * Real.cos (2 * (θ i - θ j)))
      (posdef_smul (fun _ _ : Fin m => (1 : ℝ)) (3 / 8) (by norm_num) const_kernel_posdef)
      (posdef_smul (fun i j => Real.cos (2 * (θ i - θ j))) (4 / 8) (by norm_num) (cos_double_posdef θ)))
    (posdef_smul (fun i j => Real.cos (4 * (θ i - θ j))) (1 / 8) (by norm_num) (cos_scaled_posdef θ 4))
set_option maxHeartbeats 400000 in
/-- **The general truncated Wilson heat kernel is positive-definite** (first N+1 terms):
`Σ_{n=0}^{N} (2β)^n/n!·cos^n` is PSD for `β ≥ 0`, a non-negative combination of the PSD `cos^n`. -/
theorem heat_kernel_truncated_posdef_gen {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) (N : ℕ)
    (hcos : ∀ n, PosDefKernel (fun i j => (Real.cos (θ i - θ j))^n)) :
    PosDefKernel (fun i j => ∑ n : Fin (N+1), ((2 * β)^(n.1) / (n.1.factorial : ℝ)) * (Real.cos (θ i - θ j))^(n.1)) := by
  let Kcos : ℕ → Fin m → Fin m → ℝ := fun n i j => (Real.cos (θ i - θ j))^n
  let w : Fin (N+1) → ℝ := fun n => (2 * β)^(n.1) / (n.1.factorial : ℝ)
  have hw : ∀ n : Fin (N+1), 0 ≤ w n := fun n => div_nonneg (pow_nonneg (mul_nonneg (by norm_num : 0 ≤ (2 : ℝ)) hβ) (n.1)) (Nat.cast_nonneg (n.1.factorial))
  have hK : ∀ n : Fin (N+1), PosDefKernel (fun i j => w n * Kcos n.1 i j) := fun n =>
    posdef_smul (Kcos n.1) (w n) (hw n) (hcos n.1)
  simpa [Kcos, w] using (posdef_sum (fun n => fun i j => w n * Kcos n.1 i j) hK)
end QM
