import Mathlib

open scoped BigOperators

/-! The FSS Gaussian domination — the reflection-positivity input, done properly. -/

namespace FSSGaussianDomination

open Real

/-- **The Cauchy–Schwarz inequality**, proved by the non-negative sum of squares
`Σ (fᵢ·C − gᵢ·B)² = C·(A·C − B²) ≥ 0` with `A = Σ f²`, `B = Σ f·g`, `C = Σ g²`. -/
theorem cauchy_schwarz {n : ℕ} (f g : Fin n → ℝ) :
    (∑ i : Fin n, f i * g i) ^ 2 ≤ (∑ i : Fin n, f i ^ 2) * (∑ i : Fin n, g i ^ 2) := by
  let A := ∑ i : Fin n, f i ^ 2
  let B := ∑ i : Fin n, f i * g i
  let C := ∑ i : Fin n, g i ^ 2
  have hnonneg : 0 ≤ ∑ i : Fin n, (f i * C - g i * B) ^ 2 := by
    exact Finset.sum_nonneg (fun i _ => sq_nonneg _)
  have hid : (∑ i : Fin n, (f i * C - g i * B) ^ 2) = C * (A * C - B ^ 2) := by
    dsimp [A, B, C]
    calc
      (∑ i : Fin n, (f i * (∑ j : Fin n, g j ^ 2) - g i * (∑ j : Fin n, f j * g j)) ^ 2)
          = ∑ i : Fin n, (f i ^ 2 * (∑ j : Fin n, g j ^ 2) ^ 2
              - 2 * (f i * g i) * ((∑ j : Fin n, g j ^ 2) * (∑ j : Fin n, f j * g j))
              + g i ^ 2 * (∑ j : Fin n, f j * g j) ^ 2) := by
        apply Finset.sum_congr rfl
        intro i hi
        ring
      _ = (∑ i : Fin n, f i ^ 2) * (∑ j : Fin n, g j ^ 2) ^ 2
          - 2 * (∑ i : Fin n, f i * g i) * ((∑ j : Fin n, g j ^ 2) * (∑ j : Fin n, f j * g j))
          + (∑ i : Fin n, g i ^ 2) * (∑ j : Fin n, f j * g j) ^ 2 := by
        rw [Finset.sum_sub_distrib, Finset.sum_add_distrib]
        rw [Finset.mul_sum, Finset.mul_sum, Finset.mul_sum]
        ring
      _ = (∑ j : Fin n, g j ^ 2) * ((∑ i : Fin n, f i ^ 2) * (∑ j : Fin n, g j ^ 2) - (∑ i : Fin n, f i * g i) ^ 2) := by
        ring
  by_cases hC : C = 0
  · -- C = 0 ⟹ all gᵢ = 0 ⟹ B = 0 ⟹ RHS = 0 ≥ LHS = 0
    have hg : ∀ i, g i = 0 := by
      intro i
      have hi : g i ^ 2 = 0 := by
        exact (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg _)).mp hC i (Finset.mem_univ i)
      exact sq_eq_zero_iff.mp hi
    have hB : B = 0 := by
      dsimp [B]
      simp [hg]
    dsimp [A, B, C]
    rw [hB]
    simp
  · -- C ≠ 0 ⟹ C > 0 (C ≥ 0) ⟹ A·C − B² ≥ 0 ⟹ B² ≤ A·C
    have hCpos : 0 < C := by
      dsimp [C]
      have hnn : 0 ≤ ∑ i : Fin n, g i ^ 2 := Finset.sum_nonneg (fun i _ => sq_nonneg _)
      exact lt_of_le_of_ne hnn (Ne.symm hC)
    have hAC : A * C - B ^ 2 ≥ 0 := by
      have h0 := hnonneg
      rw [hid] at h0
      exact (mul_nonneg_iff_of_pos_left hCpos).mp h0
    nlinarith [hAC]

end FSSGaussianDomination
