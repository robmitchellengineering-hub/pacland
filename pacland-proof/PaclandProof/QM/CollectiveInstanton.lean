import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The explicit full-lattice collective instanton (rung A)

The full-lattice generalization of the two-vacua instanton: the zero-momentum (uniform) winding
`θ_p = θ` over all m plaquettes — the long-wavelength collective mode, the soft mode named in #524.
Its Wilson action is `β·Σ_p (1 − cos θ_p) = β·m·(1 − cos θ)`, with the collective coefficient `m`
(the lattice volume). This file kernel-checks that the collective action is the sum over plaquettes.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The zero-momentum winding (the uniform configuration): `θ_p = θ` for all plaquettes — the
long-wavelength (collective) mode, i.e. the soft mode that the drift vanishes on (PR #524). -/
def zeroMomentumWinding {m : ℕ} (θ : ℝ) : Fin m → ℝ := fun _ => θ

/-- **The collective (zero-momentum) action**: for the uniform winding `θ_p = θ`, the Wilson action is
`β·Σ_p (1 − cos θ_p) = β·m·(1 − cos θ)`. The collective coefficient is `m` — the lattice volume (the
number of plaquettes). This is the full-lattice generalization of the single-plaquette action. -/
theorem collective_action {m : ℕ} (β θ : ℝ) :
    β * ∑ p : Fin m, (1 - Real.cos (zeroMomentumWinding θ p)) = β * (m : ℝ) * (1 - Real.cos θ) := by
  dsimp [zeroMomentumWinding]
  rw [Finset.sum_const]
  simp
  ring

/-- The collective (zero-momentum) action as a clean function: `S_m(β, θ) = β·m·(1 − cos θ)`. -/
def collectiveAction (β θ : ℝ) (m : ℕ) : ℝ := β * (m : ℝ) * (1 - Real.cos θ)

/-- The collective action agrees with the sum-over-plaquettes definition. -/
theorem collectiveAction_eq_sum {m : ℕ} (β θ : ℝ) :
    collectiveAction β θ m = β * ∑ p : Fin m, (1 - Real.cos (zeroMomentumWinding θ p)) := by
  dsimp [collectiveAction]
  rw [collective_action]

end QM
