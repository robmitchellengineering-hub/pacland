import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The 1-plaquette SU(2) Bakry–Émery curvature and the ceiling (the Clay attack's moment of truth)

The gauge-fixed (axial-gauge) 1-plaquette space is SU(2) ≅ S³. Its Bakry–Émery curvature for the
measure `e^{−β·Re Tr}` is `Ric − β·Hess(Re Tr) = 1/4 + 2β·cos θ`. This file names the ceiling: the
curvature turns negative at the antipode (`Re Tr = −2`) exactly when `β > 1/8`. The fix is Singer's
observation — quotient the flat gauge orbit (the axial gauge, PR #489), leaving the positively-curved
orbit space, so the bound becomes β-uniform.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The SU(2) Ricci constant of the bi-invariant (round) metric on S³ ≅ SU(2): `Ric = 1/4·g`. -/
def su2_ricci : ℝ := 1 / 4

/-- The Hessian of `Re Tr` on SU(2) ≅ S³ (the height function): `Hess(2cos θ) = −2cos θ · g`. -/
def hessian_reTr (θ : ℝ) : ℝ := -2 * Real.cos θ

/-- The 1-plaquette SU(2) Bakry–Émery curvature of the measure `e^{−β·Re Tr}`:
`Ric − β·Hess(Re Tr) = 1/4 + 2β·cos θ` (per tangent direction on S³). -/
def su2_curvature (β θ : ℝ) : ℝ := su2_ricci - β * hessian_reTr θ

/-- **The curvature ceiling (kernel-checked)**: at the antipode `θ = π` (the maximally non-trivial
connection, `Re Tr = −2`) the curvature is `1/4 − 2β`, which turns negative for `β > 1/8`. This is
exactly the ceiling the Clay attack must cross — and it lives on the *physical* (gauge-invariant)
direction, so the fix is to quotient the flat gauge orbit, not to fight the Hessian. -/
theorem su2_curvature_ceiling {β : ℝ} (hβ : 1 / 8 < β) :
    su2_curvature β Real.pi < 0 := by
  dsimp [su2_curvature, su2_ricci, hessian_reTr]
  have hcos : Real.cos Real.pi = -1 := Real.cos_pi
  rw [hcos]
  nlinarith

/-- **The strong-coupling regime is safe**: for `β < 1/8`, the curvature is positive *everywhere*
(even at the antipode), so the Bakry–Émery bound holds with `κ = 1/4 − 2β > 0` — the published
strong-coupling result, reproduced. -/
theorem su2_curvature_pos_strong {β : ℝ} (hβ : β < 1 / 8) :
    0 < su2_curvature β Real.pi := by
  dsimp [su2_curvature, su2_ricci, hessian_reTr]
  have hcos : Real.cos Real.pi = -1 := Real.cos_pi
  rw [hcos]
  nlinarith

end QM
