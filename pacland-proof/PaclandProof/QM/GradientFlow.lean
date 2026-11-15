import Mathlib

/-!
# The gradient flow (Lüscher's Wilson flow) — the trivializing-map route

The first rung of the gradient-flow attack on the mass gap (the second un-falsified candidate of
the sharper-bound search): the **energy monotonicity**. For the SU(2) single-plaquette Wilson action
`S(θ) = β·(1 − cos θ)`, the gradient flow `θₜ' = −S'(θ) = −β·sin θ` is a *descent direction* —
the action decreases along the flow: `d/dt S(θₜ) = −(S'(θ))² ≤ 0`.

This is the "flow smooths" statement that Lüscher's trivializing map builds on: the flow removes UV
fluctuations and contracts the configuration space, and the contraction rate is the input to the
mass-gap bound. The energy monotonicity is the first, kernel-checked rung; the full trivializing map
(a measure-preserving flow to a Gaussian) is the open conjecture.
-/

noncomputable section

open scoped Real

namespace QM

/-- The SU(2) single-plaquette Wilson action `S(θ) = β·(1 − cos θ)`, where `θ` is the plaquette
angle (the argument of the holonomy). -/
def onePlaquetteAction (β θ : ℝ) : ℝ := β * (1 - Real.cos θ)

/-- The action derivative: `S'(θ) = β·sin θ` — the Wilson (link) gradient of the 1-plaquette
action. -/
lemma onePlaquetteAction_deriv (β θ : ℝ) :
    deriv (fun x : ℝ => onePlaquetteAction β x) θ = β * Real.sin θ := by
  simp [onePlaquetteAction]

/-- **The gradient flow decreases the action.** For the flow `θₜ = θ − t·S'(θ)` (so `θₜ' = −S'(θ)`),
the action's derivative at `t = 0` is `−(S'(θ))²`: the flow is a descent direction. -/
theorem gradient_flow_monotone (β θ : ℝ) :
    deriv (fun t : ℝ => onePlaquetteAction β (θ - t * (β * Real.sin θ))) 0
      = -(β * Real.sin θ)^2 := by
  simp [onePlaquetteAction]
  ring_nf

/-- **The flow is a descent direction**: the action's derivative along the flow is non-positive.
This is the energy-monotonicity rung of Lüscher's trivializing-map argument. -/
theorem gradient_flow_decreases (β θ : ℝ) :
    deriv (fun t : ℝ => onePlaquetteAction β (θ - t * (β * Real.sin θ))) 0 ≤ 0 := by
  rw [gradient_flow_monotone]
  nlinarith [sq_nonneg (β * Real.sin θ)]

end QM
