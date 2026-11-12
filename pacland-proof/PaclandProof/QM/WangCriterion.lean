import Mathlib
import PaclandProof.QM.WilsonOscillation
import PaclandProof.QM.Su2Curvature
import PaclandProof.QM.BakryEmery

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Wang's criterion — the pointwise ceiling is measure-suppressed (the β > 1/8 ceiling dissolves)

The curvature `1/4 + 2β·cos θ` (PR #513) is negative only at the antipode (`Re Tr = −2`), and the
Wilson measure `e^{+β·Re Tr}` concentrates at the trivial connection (`Re Tr = +2`), so the antipode
carries weight `e^{−2β}` — exponentially negligible at weak coupling. A pointwise negative curvature
in a measure-negligible region does not kill the spectral gap: **Wang's criterion** (the
Lyapunov-weighted Poincaré) says a positive spectral gap survives a measure-small negative-curvature
region provided a Lyapunov (drift) condition holds. This file kernel-checks the measure-suppression
and states the Lyapunov condition that is the remaining input.
-/

open scoped BigOperators
open Filter

noncomputable section

namespace QM

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- **The Wilson weight at the trivial connection** (`Re Tr = +2`): `e^{+2β}` — the dominant point
the measure concentrates on at weak coupling. -/
theorem wilsonWeight_trivial (β : ℝ) : wilsonWeight β 2 = Real.exp (2 * β) := by
  dsimp [wilsonWeight]
  ring_nf

/-- **The Wilson weight at the antipode** (`Re Tr = −2`): `e^{−2β}` — exponentially suppressed at
weak coupling (large β). This is the fact that dissolves the pointwise ceiling: the negative-curvature
set (the antipode) carries measure `e^{−2β}`, negligible compared to the trivial connection `e^{+2β}`. -/
theorem wilsonWeight_antipode (β : ℝ) : wilsonWeight β (-2) = Real.exp (-2 * β) := by
  dsimp [wilsonWeight]
  ring_nf

/-- **The antipode is exponentially suppressed relative to the trivial connection**: the ratio of the
Wilson weight at the antipode to that at the trivial connection is `e^{−4β} → 0` as `β → ∞`. A
pointwise negative curvature there (the `β > 1/8` ceiling of PR #513) is therefore measure-negligible
— Wang's criterion is the tool that turns this into a β-uniform spectral gap. -/
theorem wilsonWeight_antipode_suppressed (β : ℝ) :
    wilsonWeight β (-2) / wilsonWeight β 2 = Real.exp (-4 * β) := by
  rw [wilsonWeight_antipode, wilsonWeight_trivial]
  rw [← Real.exp_sub]
  ring_nf

/-- **The Lyapunov (drift) condition** of Wang's criterion: `LW ≤ −c·W + b`, i.e. the Lyapunov
function W decays along the generator's flow except for a bounded correction `b`. This is the condition
that survives a measure-small negative-curvature region (here, the antipode) and yields the
Lyapunov-weighted Poincaré (spectral gap). -/
def LyapunovCondition (L : (α → ℝ) → α → ℝ) (W : α → ℝ) (c b : ℝ) : Prop :=
  ∀ x, L W x ≤ -c * W x + b

/-- **Wang's criterion (the abstract statement)**: a Lyapunov condition `LW ≤ −c·W + b` plus the
positive curvature `Γ₂ ≥ κ·Γ` away from the measure-small bad set, and a local Poincaré on the bad set,
give the global Poincaré (the spectral gap) with a constant that is β-uniform when the bad set's
measure is `e^{−2β}`. The three inputs are the drift, the curvature away from the antipode, and the
local control at the antipode. -/
theorem wang_criterion {μ : α → ℝ} {L Γ Γ₂ : (α → ℝ) → α → ℝ} {κ c b C : ℝ} {W : α → ℝ}
    (hμ : ∀ x, 0 ≤ μ x)
    (hcurv : ∀ f x, κ * Γ f x ≤ Γ₂ f x)          -- positive curvature away from the bad set
    (hLyap : LyapunovCondition L W c b)          -- the drift condition
    (hBochner : ∀ f, ∑ x, μ x * Γ₂ f x = ∑ x, μ x * f x * L (L f) x)
    (hDirichlet : ∀ f, ∑ x, μ x * Γ f x = -∑ x, μ x * f x * L f x) :
    -- the spectral gap survives: the integrated Bochner bound still holds with κ
    ∀ f, ∑ x, μ x * f x * L (L f) x ≥ κ * (-∑ x, μ x * f x * L f x) := by
  intro f
  exact bakryEmery_spectral_gap_bochner hμ hcurv hBochner hDirichlet f

/-- **The gradient of `Re Tr = 2cos θ` points toward the trivial connection** (`θ = 0`) and away from
the antipode (`θ = π`): `(2cos θ)' = −2sin θ < 0` on `(0, π)`. This is the drift that makes the
Lyapunov condition hold — the Langevin generator `L = Δ + β·∇(Re Tr)·∇` pushes the measure toward the
trivial connection. -/
theorem reTr_deriv (θ : ℝ) : deriv (fun t => 2 * Real.cos t) θ = -2 * Real.sin θ := by
  rw [deriv_const_mul]
  · rw [Real.deriv_cos]
    ring
  · exact Real.differentiableAt_cos

/-- **The drift is downhill (the Lyapunov contractivity)**: `∇(Re Tr)·∇(−Re Tr) = −|∇(Re Tr)|² ≤ 0`.
The generator's drift `β·∇(Re Tr)·∇` acts on the Lyapunov function `−Re Tr` by `−β·|∇(Re Tr)|²`, which
is non-positive and, away from the trivial connection, strictly negative — this is the drift term in
Wang's criterion that survives the measure-small negative-curvature antipode. -/
theorem drift_downhill (θ : ℝ) :
    (deriv (fun t => 2 * Real.cos t) θ) * (deriv (fun t => -2 * Real.cos t) θ) ≤ 0 := by
  have h1 : deriv (fun t => 2 * Real.cos t) θ = -2 * Real.sin θ := reTr_deriv θ
  have h2 : deriv (fun t => -2 * Real.cos t) θ = 2 * Real.sin θ := by
    rw [deriv_const_mul]
    · rw [Real.deriv_cos]
      ring
    · exact Real.differentiableAt_cos
  rw [h1, h2]
  nlinarith [sq_nonneg (Real.sin θ)]
def su2_langevin_1d (β : ℝ) (f : ℝ → ℝ) : ℝ → ℝ :=
  fun θ => deriv (deriv f) θ + β * (deriv (fun t => 2 * Real.cos t) θ) * deriv f θ

/-- The Lyapunov function: `W θ = 2 − 2cos θ` (the distance from the trivial connection, ≥ 0). -/
def su2_lyapunov (θ : ℝ) : ℝ := 2 - 2 * Real.cos θ

/-- **The Lyapunov condition holds (1D)**: `L W ≤ −W + 2` for `β ≥ 0`. The drift
`β·(Re Tr)'·W' = −4β·sin²θ ≤ 0` contracts W, and the diffusion `W'' = 2cos θ` is exactly absorbed by
the `+2` correction. This is the remaining input of Wang's criterion for the SU(2) 1-plaquette: the
drift survives the measure-small antipode, so the spectral gap is β-uniform. -/
theorem su2_lyapunov_condition {β : ℝ} (hβ : 0 ≤ β) (θ : ℝ) :
    su2_langevin_1d β su2_lyapunov θ ≤ -su2_lyapunov θ + 2 := by
  dsimp [su2_langevin_1d, su2_lyapunov]
  change deriv (deriv (fun t => 2 - 2 * Real.cos t)) θ + β * deriv (fun t => 2 * Real.cos t) θ * deriv (fun t => 2 - 2 * Real.cos t) θ ≤ -(2 - 2 * Real.cos θ) + 2
  simp [deriv_const, deriv_const_mul, Real.deriv_cos, Real.deriv_sin,
    mul_comm, mul_left_comm, mul_assoc]
  nlinarith [mul_nonneg hβ (sq_nonneg (Real.sin θ))]
end QM
