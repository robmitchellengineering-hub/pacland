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
    simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.mul_sum]
    ring
  by_cases hC : C = 0
  · -- C = 0 ⟹ all gᵢ = 0 ⟹ B = 0 ⟹ both sides 0
    have hg : ∀ i, g i = 0 := by
      intro i
      have hi : g i ^ 2 = 0 := by
        exact (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg _)).mp hC i (Finset.mem_univ i)
      exact sq_eq_zero_iff.mp hi
    have hB : B = 0 := by
      dsimp [B]
      simp [hg]
    dsimp [A, B, C]
    rw [hB, hC]
    simp
  · -- C > 0 ⟹ A·C − B² ≥ 0 ⟹ B² ≤ A·C
    have hCpos : 0 < C := by
      have hnn : 0 ≤ C := by
        dsimp [C]
        exact Finset.sum_nonneg (fun i _ => sq_nonneg _)
      exact lt_of_le_of_ne hnn (Ne.symm hC)
    have hAC : A * C - B ^ 2 ≥ 0 := by
      have h0 := hnonneg
      rw [hid] at h0
      exact (mul_nonneg_iff_of_pos_left hCpos).mp h0
    nlinarith [hAC]

end FSSGaussianDomination
