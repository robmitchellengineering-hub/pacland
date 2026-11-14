import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The modified Bessel function (the coefficient in the SU(2) heat-kernel character expansion)

The physics input to the gauge-theory EKR certificate. The SU(2) Wilson heat kernel expands in
characters `exp(β·Tr U) = Σ_j (2j+1)·I_{2j+1}(2β)/β · χ_j(U)`, and the "small oscillation" /
positive-definiteness of the effective weight comes from the coefficients being non-negative. This
file defines the modified Bessel function `I_n` and proves the non-negativity.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The modified Bessel function of the first kind, integer order `n ≥ 0`:
`I_n(x) = Σ_k (x/2)^(2k+n) / (k! · (k+n)!)`. This is the coefficient function in the SU(2)
heat-kernel character expansion. -/
noncomputable def besselI (n : ℕ) (x : ℝ) : ℝ :=
  ∑' k : ℕ, (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)

/-- **Non-negativity of the modified Bessel function**: for `x ≥ 0`, every term in the series is
non-negative, so `I_n(x) ≥ 0`. This is the key positivity input to the character expansion — the
coefficients `(2j+1)·I_{2j+1}(2β)/β` are non-negative. -/
theorem besselI_nonneg {n : ℕ} {x : ℝ} (hx : 0 ≤ x) : 0 ≤ besselI n x := by
  dsimp [besselI]
  exact tsum_nonneg (by
    intro k
    exact div_nonneg (pow_nonneg (div_nonneg hx (by norm_num : 0 ≤ (2 : ℝ))) _)
      (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)))

/-- **The SU(2) character-expansion coefficient is non-negative**: `(2j+1)·I_{2j+1}(2β)/β ≥ 0` for
`β > 0`. This is the "positive-definite" / small-oscillation input that makes the Wilson heat kernel
a non-negative combination of characters. -/
theorem su2_coefficient_nonneg {j : ℕ} {β : ℝ} (hβ : 0 < β) :
    0 ≤ (2 * (j : ℝ) + 1) * besselI (2 * j + 1) (2 * β) / β := by
  have hI : 0 ≤ besselI (2 * j + 1) (2 * β) := besselI_nonneg (by nlinarith [hβ] : 0 ≤ 2 * β)
  have hnum : 0 ≤ (2 * (j : ℝ) + 1) * besselI (2 * j + 1) (2 * β) := by
    exact mul_nonneg (by nlinarith : 0 ≤ 2 * (j : ℝ) + 1) hI
  exact div_nonneg hnum (le_of_lt hβ)

/-- The Bessel series is summable for `x ≥ 0`: dominated by `(x/2)^n · exp((x/2)²)`. -/
theorem besselI_summable_of_nonneg (n : ℕ) {x : ℝ} (hx : 0 ≤ x) :
    Summable (fun k : ℕ => (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)) := by
  have hf : Summable (fun k : ℕ => (x / 2) ^ n * (((x / 2) ^ 2) ^ k / (k.factorial : ℝ))) := by
    exact (Real.summable_pow_div_factorial ((x / 2) ^ 2)).mul_left ((x / 2) ^ n)
  refine Summable.of_nonneg_of_le (fun k => ?_) (fun k => ?_) hf
  · exact div_nonneg (pow_nonneg (div_nonneg hx (by norm_num)) _)
      (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _))
  · have h1 : (k.factorial : ℝ) ≤ (k.factorial : ℝ) * (k + n).factorial := by
      have hfact : (1 : ℝ) ≤ (k + n).factorial := by exact_mod_cast (Nat.factorial_pos (k + n))
      nlinarith [mul_le_mul_of_nonneg_left hfact (Nat.cast_nonneg (k.factorial))]
    calc
      (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)
          ≤ (x / 2) ^ (2 * k + n) / (k.factorial : ℝ) := by
        exact div_le_div_of_nonneg_left (pow_nonneg (div_nonneg hx (by norm_num)) _) (Nat.cast_pos.mpr (Nat.factorial_pos k)) h1
      _ = (x / 2) ^ n * (((x / 2) ^ 2) ^ k / (k.factorial : ℝ)) := by
        rw [← pow_mul, pow_add]
        ring

/-- **Strict positivity of the modified Bessel function**: `I_n(x) > 0` for `x > 0` — the first
term `(x/2)^n/n!` is positive and the tail is non-negative. This is the strict positivity that makes
the SU(2) character coefficients genuinely positive (not just non-negative). -/
theorem besselI_pos {n : ℕ} {x : ℝ} (hx : 0 < x) : 0 < besselI n x := by
  dsimp [besselI]
  let a : ℕ → ℝ := fun k => (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)
  have hsum : Summable a := by
    dsimp [a]
    exact besselI_summable_of_nonneg n (le_of_lt hx)
  have hdecomp : (∑' k : ℕ, a k) = a 0 + ∑' k : ℕ, ite (k = 0) (0 : ℝ) (a k) :=
    Summable.tsum_eq_add_tsum_ite hsum (0 : ℕ)
  rw [hdecomp]
  have hfirst : 0 < a 0 := by
    dsimp [a]
    norm_num [Nat.factorial]
    exact div_pos (pow_pos (div_pos hx (by norm_num)) n) (Nat.cast_pos.mpr (Nat.factorial_pos n))
  have htail : 0 ≤ ∑' k : ℕ, ite (k = 0) (0 : ℝ) (a k) := by
    apply tsum_nonneg
    intro k
    split_ifs with hk
    · simp
    · dsimp [a]
      exact div_nonneg (pow_nonneg (div_nonneg (le_of_lt hx) (by norm_num)) _)
        (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _))
  exact add_pos_of_pos_of_nonneg hfirst htail
end QM
