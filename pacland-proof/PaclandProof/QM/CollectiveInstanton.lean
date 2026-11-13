import Mathlib
import PaclandProof.QM.AsymptoticFreedom

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

/-- The collective instanton weight (the Boltzmann weight of the zero-momentum winding). -/
def collectiveInstantonWeightRaw (β θ : ℝ) (m : ℕ) : ℝ := Real.exp (-collectiveAction β θ m)

/-- **The renormalization hypothesis (the RG input)**: the collective coefficient `m·(1−cos θ)` of the
zero-momentum instanton renormalizes to the one-loop exponent `c = 1/(2b₀) = 12π²/11` at the instanton
saddle. This is the renormalization-group statement that turns the collective action `β·m·(1−cos θ)`
into the physical renormalized action `c·β`. -/
def CollectiveRenormalization (m : ℕ) (θ : ℝ) : Prop :=
  (m : ℝ) * (1 - Real.cos θ) = asymptoticFreedomExponent 2

/-- **The renormalized collective instanton weight**: under the renormalization hypothesis, the
collective instanton weight `e^{−β·m·(1−cos θ)}` equals the physical `e^{−cβ}` with `c = 12π²/11`
(PR #531). This is step 2 of rung A: the collective coefficient renormalizes to the one-loop β-function
exponent, so the full-lattice instanton weight carries the physical scale. -/
theorem collective_weight_renormalized {m : ℕ} {θ β : ℝ} (hren : CollectiveRenormalization m θ) :
    collectiveInstantonWeightRaw β θ m = collectiveInstantonWeight β := by
  dsimp [collectiveInstantonWeightRaw, collectiveInstantonWeight, collectiveAction]
  rw [show β * (m : ℝ) * (1 - Real.cos θ) = β * ((m : ℝ) * (1 - Real.cos θ)) by ring]
  rw [hren]
  rw [su2_exponent]
  ring_nf
end QM
