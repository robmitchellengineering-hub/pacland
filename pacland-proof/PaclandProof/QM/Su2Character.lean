import Mathlib
import PaclandProof.QM.Bessel

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The SU(2) character and its Weyl bound

The character `χ_j` of the spin-j representation of SU(2), evaluated on the diagonal torus, is
`χ_j(θ) = sin((2j+1)θ)/sin θ`. Its Weyl bound `|sin((2j+1)θ)| ≤ (2j+1)·|sin θ|` (the character is
bounded by its dimension) is the "small oscillation" of the character — the input that makes the
heat-kernel character expansion `exp(β·Tr U) = Σ (2j+1)·I_{2j+1}(2β)/β·χ_j(U)` converge.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The SU(2) character of the spin-j representation, evaluated on the diagonal torus
`g = diag(e^{iθ}, e^{-iθ})`: `χ_j(θ) = sin((2j+1)θ)/sin θ` (the Weyl character formula). -/
def su2_character (j : ℕ) (θ : ℝ) : ℝ :=
  Real.sin ((2 * (j : ℝ) + 1) * θ) / Real.sin θ

/-- **The Weyl bound**: the SU(2) character is bounded by its dimension `2j+1` —
`|sin((2j+1)θ)| ≤ (2j+1)·|sin θ|`. This is the "small oscillation" of the character, the input
that makes the heat-kernel character expansion well-behaved. -/
theorem su2_character_weyl_bound (j : ℕ) (θ : ℝ) :
    |Real.sin ((2 * (j : ℝ) + 1) * θ)| ≤ (2 * (j : ℝ) + 1) * |Real.sin θ| := by
  induction' j with j ih
  · simp
  · have htrig : Real.sin ((2 * (j : ℝ) + 3) * θ) = Real.sin ((2 * (j : ℝ) + 1) * θ) + 2 * Real.cos ((2 * (j : ℝ) + 2) * θ) * Real.sin θ := by
      have h : Real.sin ((2 * (j : ℝ) + 3) * θ) - Real.sin ((2 * (j : ℝ) + 1) * θ) = 2 * Real.cos ((2 * (j : ℝ) + 2) * θ) * Real.sin θ := by
        rw [Real.sin_sub_sin]
        ring_nf
      linarith
    have habs : |Real.sin ((2 * (j : ℝ) + 3) * θ)| ≤ |Real.sin ((2 * (j : ℝ) + 1) * θ)| + 2 * |Real.sin θ| := by
      rw [htrig]
      have hcos : |Real.cos ((2 * (j : ℝ) + 2) * θ)| ≤ 1 := Real.abs_cos_le_one _
      calc
        |Real.sin ((2 * (j : ℝ) + 1) * θ) + 2 * Real.cos ((2 * (j : ℝ) + 2) * θ) * Real.sin θ|
            ≤ |Real.sin ((2 * (j : ℝ) + 1) * θ)| + |2 * Real.cos ((2 * (j : ℝ) + 2) * θ) * Real.sin θ| := abs_add_le _ _
        _ ≤ |Real.sin ((2 * (j : ℝ) + 1) * θ)| + 2 * |Real.sin θ| := by
          rw [abs_mul, abs_mul, abs_of_nonneg (by norm_num : 0 ≤ (2 : ℝ))]
          nlinarith [mul_le_mul_of_nonneg_left hcos (abs_nonneg (Real.sin θ))]
    have hfinal : |Real.sin ((2 * (j : ℝ) + 3) * θ)| ≤ (2 * (j : ℝ) + 3) * |Real.sin θ| := by
      nlinarith [habs, ih]
    norm_num
    ring_nf at hfinal ⊢
    exact hfinal

end QM
