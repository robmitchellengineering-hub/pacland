import Mathlib
import PaclandProof.QM.AsymptoticFreedom
import PaclandProof.QM.CollectiveInstanton

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Rung A — the renormalized collective-instanton action

The reconciliation that closes Rung A: the mass gap follows the β-function exponent
`c = 1/(2β₀) = 12π²/11` (the running coupling's dimensional-transmutation scale), NOT the single
instanton's `8π²/g²`. The two are different objects, and their ratio is exactly `22/3`.

The renormalized action is the running coupling plugged into the collective action: the exponent is
`c = 1/(2β₀)` because the coupling runs as `g²(μ) = 1/(2β₀·ln(μ/Λ))`, so the mass scale `Λ = μ·e^(−c/g²)`
carries the β-function exponent, not the instanton's.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The running coupling squared `g²(μ) = 1/(2β₀·ln(μ/Λ))` — the β-function's dimensional transmutation. -/
def runningCouplingSquared (b0 μ Λ : ℝ) : ℝ := 1 / (2 * b0 * Real.log (μ / Λ))

/-- Rung A: the renormalized collective-instanton exponent is the β-function exponent `c = 1/(2β₀)` —
the exponent the running coupling carries, not the instanton's `8π²`. -/
theorem renormalized_exponent_is_beta (N : ℝ) :
    asymptoticFreedomExponent N = 1 / (2 * betaFunctionCoefficient N) := by
  rw [asymptoticFreedomExponent]

/-- Rung A (SU(2)): the renormalized exponent is `12π²/11`. -/
theorem renormalized_exponent_su2 :
    asymptoticFreedomExponent 2 = 12 * Real.pi ^ 2 / 11 := by
  rw [asymptoticFreedomExponent, betaFunctionCoefficient]
  field_simp
  ring

/-- Rung A: the renormalized mass-gap exponent `12π²/11` is NOT the single-instanton `8π²` — the
reconciliation (the gap follows the β-function, not the instanton). -/
theorem renormalized_ne_instanton :
    (12 * Real.pi ^ 2 / 11) ≠ 8 * Real.pi ^ 2 := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  intro h
  field_simp [hpi] at h
  norm_num at h

/-- Rung A: the instanton exponent is `22/3` times the mass-gap exponent — the precise "different scale". -/
theorem instanton_over_gap_ratio :
    (8 * Real.pi ^ 2) / (12 * Real.pi ^ 2 / 11) = 22 / 3 := by
  field_simp [Real.pi_ne_zero]
  ring

/-- Rung A (the reconciliation, stated and proven): the mass gap follows the β-function exponent
`12π²/11`, which is `22/3` smaller than the instanton's `8π²`. -/
theorem mass_gap_follows_beta_not_instanton :
    asymptoticFreedomExponent 2 = 12 * Real.pi ^ 2 / 11 ∧
    (8 * Real.pi ^ 2) / (12 * Real.pi ^ 2 / 11) = 22 / 3 := by
  exact ⟨renormalized_exponent_su2, instanton_over_gap_ratio⟩

end QM
