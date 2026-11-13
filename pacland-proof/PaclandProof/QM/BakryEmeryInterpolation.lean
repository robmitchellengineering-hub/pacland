import Mathlib
import PaclandProof.QM.GronwallDecay

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Bakry–Émery interpolation: the Fisher-decay assembly

The core of the `Γ₂ ≥ κΓ ⟹ LSI` interpolation is the Fisher-information decay
`I'(t) ≤ -2κ I(t)`, from the Fisher derivative `I' = -2J` (the integrated Bochner–Lichnerowicz +
ou_invariant, both committed) and the curvature `κI ≤ J` (committed). This module proves the
assembly: the decay + Grönwall give the exponential bound `I t ≤ I 0 · e^{-2κ t}`.
-/

noncomputable section

namespace QM

/-- The pointwise Fisher decay: `I' = -2J` and `κI ≤ J` imply `I' ≤ -2κI`. -/
theorem fisher_decay_of_curvature {I J : ℝ → ℝ} (κ t : ℝ)
    (hderiv : deriv I t = -2 * J t)
    (hcurv : κ * I t ≤ J t) :
    deriv I t ≤ -2 * κ * I t := by
  rw [hderiv]
  nlinarith

/-- **The Fisher exponential decay** (the core of the interpolation): the Fisher derivative
`I' = -2J` and the curvature `κI ≤ J` imply `I t ≤ I 0 · e^{-2κt}` for `t ≥ 0`. This composes the
pointwise Fisher decay with the committed Grönwall decay. -/
theorem fisher_exponential_decay_of_curvature {I J : ℝ → ℝ} (κ : ℝ) (hκ : 0 ≤ κ)
    (hderiv : ∀ t ≥ 0, HasDerivAt I (deriv I t) t)
    (hI' : ∀ t ≥ 0, deriv I t = -2 * J t)
    (hcurv : ∀ t ≥ 0, κ * I t ≤ J t) (t : ℝ) (ht : 0 ≤ t) :
    I t ≤ I 0 * Real.exp (-2 * κ * t) := by
  have hdecay : ∀ s ≥ 0, deriv I s ≤ -(2 * κ) * I s := by
    intro s hs
    nlinarith [fisher_decay_of_curvature κ s (hI' s hs) (hcurv s hs)]
  convert gronwall_decay (2 * κ) I hderiv hdecay t ht using 1
  ring

end QM
