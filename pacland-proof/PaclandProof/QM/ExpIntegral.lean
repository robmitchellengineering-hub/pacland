import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The exponential integral `∫₀^b e^{-c x} dx = (1 - e^{-c b}) / c`

The definite integral behind the final step of the Bakry–Émery interpolation: integrating the
Fisher exponential bound `I t ≤ I 0 · e^{-2κt}` over `[0,∞)` gives `I 0 / (2κ)`.
-/

noncomputable section

namespace QM

/-- The derivative of `x ↦ -c⁻¹ e^{-c x}` is `x ↦ e^{-c x}`. -/
private lemma deriv_exp_neg_mul (c : ℝ) (x : ℝ) (hc : c ≠ 0) :
    HasDerivAt (fun y => -c⁻¹ * Real.exp (-c * y)) (Real.exp (-c * x)) x := by
  have hcomp : HasDerivAt (fun y => -c * y) (-c) x := by
    simpa using (hasDerivAt_id x).const_mul (-c)
  have hexp := (Real.hasDerivAt_exp (x := -c * x)).comp x hcomp
  have hconst := hexp.const_mul (-c⁻¹)
  have hder : -c⁻¹ * (Real.exp (-c * x) * -c) = Real.exp (-c * x) := by
    field_simp [hc]
  rwa [hder] at hconst

/-- **The definite exponential integral**: `∫₀^b e^{-c x} dx = (1 - e^{-c b}) / c` for `c ≠ 0`. -/
theorem integral_exp_neg_mul_Ioc (c b : ℝ) (hc : c ≠ 0) :
    ∫ x in (0 : ℝ)..b, Real.exp (-c * x) = (1 - Real.exp (-c * b)) / c := by
  let F : ℝ → ℝ := fun y => -c⁻¹ * Real.exp (-c * y)
  have hder : ∀ x ∈ Set.uIcc 0 b, HasDerivAt F (Real.exp (-c * x)) x := by
    intro x hx
    exact deriv_exp_neg_mul c x hc
  have hcont : ContinuousOn (fun x => Real.exp (-c * x)) (Set.uIcc 0 b) := by
    exact (Real.continuous_exp.comp (continuous_const.mul continuous_id)).continuousOn
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt (f := F) (f' := fun x => Real.exp (-c * x)) hder
    (hcont.intervalIntegrable)
  dsimp [F] at h
  have hR : -c⁻¹ * Real.exp (-c * b) - -c⁻¹ * Real.exp (-c * 0) = (1 + -Real.exp (-c * b)) * c⁻¹ := by
    have hz : -c * 0 = 0 := by ring
    rw [hz, Real.exp_zero]
    ring
  rw [hR] at h
  simpa [div_eq_mul_inv, sub_eq_add_neg] using h

end QM
