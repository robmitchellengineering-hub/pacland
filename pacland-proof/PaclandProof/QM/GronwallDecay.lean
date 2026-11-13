import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Grönwall decay: `u' ≤ -c·u ⟹ u t ≤ u 0 · e^{-c t}`

The comparison argument `v s = u s · e^{c s}` (so `v' ≤ 0`, hence `v` nonincreasing) gives the
exponential decay. This is the `hgronwall` input to the Bakry–Émery interpolation.
-/

noncomputable section

namespace QM

private lemma exp_mul_hasDerivAt (c : ℝ) (s : ℝ) :
    HasDerivAt (fun s => Real.exp (c * s)) (Real.exp (c * s) * c) s :=
  (Real.hasDerivAt_exp (x := c * s)).comp s (hasDerivAt_const_mul c)

/-- **The Grönwall decay** (scalar form): if `u` is differentiable and `u' ≤ -c·u` for all `t ≥ 0`,
then `u t ≤ u 0 · e^{-c·t}` for `t ≥ 0`. -/
theorem gronwall_decay (c : ℝ) (u : ℝ → ℝ)
    (hu : ∀ t ≥ 0, HasDerivAt u (deriv u t) t)
    (hder : ∀ t ≥ 0, deriv u t ≤ -c * u t) (t : ℝ) (ht : 0 ≤ t) :
    u t ≤ u 0 * Real.exp (-c * t) := by
  let v : ℝ → ℝ := fun s => u s * Real.exp (c * s)
  have hv' : ∀ s ∈ Set.Ioo 0 t, deriv v s ≤ 0 := by
    intro s hs
    have hvs : HasDerivAt v (deriv u s * Real.exp (c * s) + u s * (Real.exp (c * s) * c)) s :=
      (hu s (le_of_lt hs.1)).mul (exp_mul_hasDerivAt c s)
    rw [hvs.deriv]
    have he : 0 < Real.exp (c * s) := Real.exp_pos _
    nlinarith [hder s (le_of_lt hs.1), he]
  have hvmono : AntitoneOn v (Set.Icc 0 t) := by
    refine antitoneOn_of_deriv_nonpos (convex_Icc 0 t) ?hf ?hf' ?hnonpos
    · intro s hs
      exact ((hu s hs.1).continuousAt.mul (exp_mul_hasDerivAt c s).continuousAt).continuousWithinAt
    · intro s hs
      rw [interior_Icc] at hs
      exact ((hu s (le_of_lt hs.1)).differentiableAt.mul (exp_mul_hasDerivAt c s).differentiableAt).differentiableWithinAt
    · intro s hs
      rw [interior_Icc] at hs
      exact hv' s hs
  have hvle : v t ≤ v 0 := by
    have h0t : 0 ∈ Set.Icc 0 t := ⟨le_rfl, ht⟩
    have htt : t ∈ Set.Icc 0 t := ⟨ht, le_rfl⟩
    exact hvmono h0t htt ht
  dsimp [v] at hvle
  have huineq : u t * Real.exp (c * t) ≤ u 0 := by
    simpa using hvle
  have hle : (u t * Real.exp (c * t)) * Real.exp (-c * t) ≤ u 0 * Real.exp (-c * t) :=
    mul_le_mul_of_nonneg_right huineq (Real.exp_nonneg _)
  rw [mul_assoc] at hle
  have he : Real.exp (c * t) * Real.exp (-c * t) = 1 := by
    rw [← Real.exp_add]
    simp
  rw [he] at hle
  simpa using hle

end QM
