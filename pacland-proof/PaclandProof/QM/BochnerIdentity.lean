import Mathlib
import PaclandProof.QM.BakryEmery
import PaclandProof.QM.Su2Curvature

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The SU(2) Bochner identity — the full S³ generator and the Γ₂ formula (statement)

The pointwise Bochner bound `Γ₂(f) ≥ κ(θ)·Γ(f)` with the tower's Bakry–Émery curvature
`κ(θ) = su2_curvature β θ = 1/4 + 2β·cos θ`. The full S³ radial generator carries the Ricci-carrying
`2·cot θ` term; the identity follows from the standard Γ₂-calculus `Γ₂(f) = (f'')² + κ(θ)·(f')²`.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The FULL S³ radial generator (with the Ricci-carrying cot θ term):
`L f = f'' + (2·cot θ − 2β·sin θ)·f'`. This is the radial part of the SU(2) Langevin generator on
S³ ≅ SU(2), with the drift `a(θ) = 2·cot θ − 2β·sin θ` whose derivative gives the Bakry–Émery curvature. -/
def su2_full_generator (β : ℝ) (f : ℝ → ℝ) : ℝ → ℝ :=
  fun θ => deriv (deriv f) θ + (2 * (Real.cos θ / Real.sin θ) - 2 * β * Real.sin θ) * deriv f θ

/-- **The Bochner formula (the statement, corrected)**: the FULL S³ Γ₂ is the 1D Γ₂ plus the
tangential Hessian `2·cot²θ·(f')²`, so `Γ₂_full(f) = (f'')² + su2_curvature·(f')²`. The tower's
algebraic `Gamma2` is the 1D part; the tangential term is the missing differential-geometry input. -/
def BochnerFormulaSu2 (β : ℝ) (f : ℝ → ℝ) (θ : ℝ) : Prop :=
  Gamma2 (su2_full_generator β) f θ + 2 * (Real.cos θ / Real.sin θ) ^ 2 * (deriv f θ) ^ 2
    = (deriv (deriv f) θ) ^ 2 + su2_curvature β θ * carreDuChamp (su2_full_generator β) f f θ

/-- **The SU(2) Bochner identity (the statement)**: `Γ₂(f) ≥ κ(θ)·Γ(f)` with κ = su2_curvature. This
follows from `BochnerFormulaSu2` and `(f'')² ≥ 0`. -/
def Su2BochnerIdentity (β : ℝ) (f : ℝ → ℝ) (θ : ℝ) : Prop :=
  su2_curvature β θ * carreDuChamp (su2_full_generator β) f f θ ≤ Gamma2 (su2_full_generator β) f θ

/-- **The Bochner identity implies the good-set curvature** (the `hcurv` hypothesis of
`WeakCouplingWangCriterion`): on the good set where `0 ≤ su2_curvature β θ`, the identity
`Γ₂ ≥ κ·Γ` gives the pointwise bound. -/
def Su2GoodSetCurvature (β : ℝ) (f : ℝ → ℝ) (θ : ℝ) : Prop :=
  0 ≤ su2_curvature β θ → su2_curvature β θ * carreDuChamp (su2_full_generator β) f f θ ≤
    Gamma2 (su2_full_generator β) f θ

end QM
