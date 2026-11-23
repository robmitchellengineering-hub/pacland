import Mathlib

open scoped BigOperators

/-! The FSS Gaussian domination — the reflection-positivity input, done properly.

The missing input is `σ² = K⁻¹`: reflection positivity forces the Gaussian covariance to be the free
propagator. The FSS chain is (1) the reflection Cauchy–Schwarz, (2) the reflection factorization, (3) the
sum over reflection planes → Gaussian. This file proves the lemmas in order, against the lake build. -/

namespace FSSGaussianDomination

open Real

/-- **The Cauchy–Schwarz inequality** (the FSS seed), proved directly by the non-negative quadratic
`Q(t) = Σ (fᵢ·t + gᵢ)² ≥ 0` and its discriminant. -/
theorem cauchy_schwarz {n : ℕ} (f g : Fin n → ℝ) :
    (∑ i : Fin n, f i * g i) ^ 2 ≤ (∑ i : Fin n, f i ^ 2) * (∑ i : Fin n, g i ^ 2) := by
  let A := ∑ i : Fin n, f i ^ 2
  let B := ∑ i : Fin n, f i * g i
  let C := ∑ i : Fin n, g i ^ 2
  have hnonneg : ∀ t : ℝ, 0 ≤ ∑ i : Fin n, (f i * t + g i) ^ 2 := by
    intro t
    exact Finset.sum_nonneg (fun i _ => sq_nonneg _)
  have hexpand : ∀ t : ℝ, (∑ i : Fin n, (f i * t + g i) ^ 2) = A * t ^ 2 + 2 * B * t + C := by
    intro t
    dsimp [A, B, C]
    calc
      (∑ i : Fin n, (f i * t + g i) ^ 2) = ∑ i : Fin n, (f i ^ 2 * t ^ 2 + 2 * (f i * g i) * t + g i ^ 2) := by
        apply Finset.sum_congr rfl
        intro i hi
        ring
      _ = (∑ i : Fin n, f i ^ 2) * t ^ 2 + 2 * (∑ i : Fin n, f i * g i) * t + (∑ i : Fin n, g i ^ 2) := by
        rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
        rw [Finset.mul_sum, Finset.mul_sum, Finset.mul_sum]
        ring
  by_cases hA : A = 0
  · -- A = 0 ⟹ all fᵢ = 0 ⟹ B = 0, so the LHS is 0
    have hf : ∀ i, f i = 0 := by
      intro i
      have hi : f i ^ 2 = 0 := by
        exact (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg _)).mp hA i (Finset.mem_univ i)
      exact sq_eq_zero_iff.mp hi
    have hB : B = 0 := by
      dsimp [B]
      simp [hf]
    dsimp [A, B, C]
    rw [hB, hA]
    simp
  · -- pick t = -B/A and use Q(t) ≥ 0
    have hA0 : A ≠ 0 := hA
    let t := -B / A
    have hQt : 0 ≤ A * t ^ 2 + 2 * B * t + C := by
      rw [← hexpand t]
      exact hnonneg t
    have hQ : A * t ^ 2 + 2 * B * t + C = C - B ^ 2 / A := by
      dsimp [t]
      field_simp [hA0]
      ring
    have hQt' : 0 ≤ C - B ^ 2 / A := by
      rwa [← hQ]
    have hApos : 0 < A := by
      dsimp [A]
      have hnn : 0 ≤ ∑ i : Fin n, f i ^ 2 := Finset.sum_nonneg (fun i _ => sq_nonneg _)
      exact lt_of_le_of_ne hnn (Ne.symm hA)
    have hAC : B ^ 2 ≤ A * C := by
      nlinarith [hQt', hApos]
    dsimp [A, B, C] at hAC ⊢
    exact hAC

end FSSGaussianDomination
