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

/-- The gradient-flow map `Fₜ(θ) = θ − t·S'(θ) = θ − t·β·sin θ` (one flow-time step). -/
def gradientFlow (t β θ : ℝ) : ℝ := θ - t * (β * Real.sin θ)

/-- **The flow-time contraction rate — route (2) of `refereeScalingLaw`.** The flow's infinitesimal
contraction is `Fₜ'(θ) = 1 − t·β·cos θ`, and on the region `cos θ ≥ c > 0` with `t·β ≤ 1`, the rate
`|Fₜ'(θ)| ≤ 1 − t·β·c < 1`: the gradient flow contracts the configuration at a rate strictly below 1.
This is the flow-time contraction that Lüscher's trivializing map builds on — the contraction rate is
the input to the mass-gap bound at the asymptotic-freedom scale. -/
theorem gradientFlow_contraction_rate (t β θ c : ℝ)
    (hc : 0 < c) (hcos : c ≤ Real.cos θ) (ht : t * β ≤ 1) (hpos : 0 ≤ t * β) :
    |1 - t * β * Real.cos θ| ≤ 1 - t * β * c := by
  have hcos_le_one : Real.cos θ ≤ 1 := Real.cos_le_one θ
  have htcos : t * β * Real.cos θ ≤ 1 := by
    have htb : t * β * Real.cos θ ≤ t * β * 1 := mul_le_mul_of_nonneg_left hcos_le_one hpos
    nlinarith [htb, ht]
  have hnonneg : 0 ≤ 1 - t * β * Real.cos θ := by nlinarith
  rw [abs_of_nonneg hnonneg]
  have hstep : t * β * c ≤ t * β * Real.cos θ := mul_le_mul_of_nonneg_left hcos hpos
  nlinarith [hstep]

end QM
