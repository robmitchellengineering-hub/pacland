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

end QM
