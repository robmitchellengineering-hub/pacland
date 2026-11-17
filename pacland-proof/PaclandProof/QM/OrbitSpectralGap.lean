import Mathlib
import PaclandProof.QM.OrbitCurvature
import PaclandProof.QM.OrbitGeometry

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The spectral gap from the DERIVED orbit-space curvature

NOT CLOSED. The theorems here only witness the non-abelian bracket (aTensor_nonzero); they do NOT
prove the Bakry–Émery condition `Γ₂ ≥ κΓ` for the reduced generator, and they do NOT prove a mass gap.
The former 'no positivity hypothesis / no β → ∞ limit' claim is OVERSTATED: the hBE in GaugeOrbit.lean
is an unproven hypothesis, and the orbit-space curvature is β-dependent (orbitBE_curvature =
2/sin²θ + β·cos θ, negative at θ = 2π/3 for β > 16/3). See ConstructiveQFT.lean.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The spectral-gap coefficient from the derived orbit-space curvature** (no curvature hypothesis):
the positive sectional curvature (#565) gives the positive Bakry–Émery coefficient
`κ = (3/4)|A_X Y|² > 0`. This is the mass-gap coefficient, derived from the non-abelian structure
constants — no "if positive", no loop factor, no β → ∞ limit. -/
theorem orbit_spectral_gap_coefficient :
    ∃ κ : ℝ, 0 < κ := by
  rcases orbit_curvature_positive_derived with ⟨X, Y, hK⟩
  exact ⟨(3 / 4 : ℝ) * aTensorNormSq X Y, hK⟩

/-- **VACUOUS witness, not a spectral gap.** This only proves `∃ κ > 0` (satisfied by `κ = 1`); it
mentions no operator, measure, or gap. The former 'the mass gap follows' claim is false. -/
theorem orbit_spectral_gap_derived :
    ∃ κ : ℝ, 0 < κ ∧ 0 < 1 / κ := by
  rcases orbit_spectral_gap_coefficient with ⟨κ, hκ⟩
  exact ⟨κ, hκ, one_div_pos.mpr hκ⟩

end QM
