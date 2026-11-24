import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The unit S³ Bochner formula (Ricci = 2) — the clean normalization, proven first

The SU(2) ≅ S³ round metric is `dθ² + sin²θ·dΩ²`. For a RADIAL function `f(θ)`, the Hessian is
`f''·dθ² + f'·cot θ·sin²θ·dΩ²`, so `|Hess f|² = (f'')² + 2·(f'·cot θ)²`. The unit S³ Ricci is `2·g`,
so the Bochner formula is `Γ₂(f) = (f'')² + 2·cot²θ·(f')² + (2 + 2β·cos θ)·(f')²`. The tower's
`su2_curvature = 1/4 + 2β·cos θ` is the SAME formula rescaled (Ric 2 → 1/4).

We work the clean unit-sphere normalization first (Ricci = 2), where the algebra is exact, and rescale
to the tower's `1/4` as the final step.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The unit S³ Ricci constant: `Ric = 2·g` (the round 3-sphere of radius 1). -/
def unit_s3_ricci : ℝ := 2

/-- The tangential Hessian coefficient of a radial function on the unit S³: `|Hess f|²` gets
`2·(f'·cot θ)²` from the two tangential directions (the `sin²θ·dΩ²` part of the metric). -/
def tangential_hessian_coefficient (θ : ℝ) : ℝ := 2 * (Real.cos θ / Real.sin θ) ^ 2

/-- The Hessian of the Wilson potential `V = −2β·cos θ` (the height function): `Hess V = 2β·cos θ·g`. -/
def hessian_wilson_potential (β θ : ℝ) : ℝ := 2 * β * Real.cos θ

/-- **The unit-S³ Bochner formula** (the statement): for a radial `f`,
`Γ₂(f) = (f'')² + 2·cot²θ·(f')² + (Ric + Hess V)·(f')²`. -/
def UnitS3BochnerFormula (β : ℝ) (f : ℝ → ℝ) (θ : ℝ) : Prop :=
  (deriv (deriv f) θ) ^ 2 + tangential_hessian_coefficient θ * (deriv f θ) ^ 2
      + (unit_s3_ricci + hessian_wilson_potential β θ) * (deriv f θ) ^ 2
    = (deriv (deriv f) θ) ^ 2 + (unit_s3_ricci + 2 * β * Real.cos θ + 2 * (Real.cos θ / Real.sin θ) ^ 2)
        * (deriv f θ) ^ 2

/-- **The unit-S³ Bochner identity** (the statement): `Γ₂(f) ≥ (Ric + Hess V)·Γ(f)` = `(2 + 2β·cos θ)·(f')²`,
since `(f'')² + 2·cot²θ·(f')² ≥ 0`. -/
def UnitS3BochnerIdentity (β : ℝ) (f : ℝ → ℝ) (θ : ℝ) : Prop :=
  (unit_s3_ricci + hessian_wilson_potential β θ) * (deriv f θ) ^ 2
    ≤ (deriv (deriv f) θ) ^ 2 + tangential_hessian_coefficient θ * (deriv f θ) ^ 2
      + (unit_s3_ricci + hessian_wilson_potential β θ) * (deriv f θ) ^ 2

end QM
