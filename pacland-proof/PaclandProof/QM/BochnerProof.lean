import Mathlib
import PaclandProof.QM.BakryEmery
import PaclandProof.QM.BochnerIdentity

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The 1D Bochner formula — the deriv-calculus identity Γ₂(f) = (f'')² − a'(θ)·(f')²

For a diffusion generator `Lf = f'' + a(θ)·f'`, the tower's algebraic `Gamma2` and `carreDuChamp` give
`Γ(f) = (f')²` and `Γ₂(f) = (f'')² − a'(θ)·(f')²`. For the full S³ generator this is the Bochner formula
(the tangential Hessian lives in the `cot θ` term of `a`). This is the proof target.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The diffusion generator `Lf = f'' + a·f'`. -/
def diffusion_generator (a : ℝ → ℝ) (f : ℝ → ℝ) : ℝ → ℝ :=
  fun θ => deriv (deriv f) θ + a θ * deriv f θ

/-- **The carré du champ is the squared derivative**: `Γ(f) = (f')²` for a diffusion generator. -/
theorem carre_du_champ_is_squared_deriv (a f : ℝ → ℝ) (θ : ℝ) (hf : ContDiff ℝ 2 f) :
    carreDuChamp (diffusion_generator a) f f θ = (deriv f θ) ^ 2 := by
  dsimp [carreDuChamp, diffusion_generator]
  have hf1 : Differentiable ℝ f := hf.differentiable (by norm_num)
  have hfun : deriv (f * f) = fun y => 2 * f y * deriv f y := by
    funext y
    rw [deriv_mul (hf1 y) (hf1 y)]
    ring
  have h1 : deriv (fun t => f t * f t) θ = 2 * f θ * deriv f θ := by
    change deriv (f * f) θ = 2 * f θ * deriv f θ
    rw [hfun]
  have h2 : deriv (deriv (fun t => f t * f t)) θ = 2 * (deriv f θ) ^ 2 + 2 * f θ * deriv (deriv f) θ := by
    change deriv (deriv (f * f)) θ = 2 * (deriv f θ) ^ 2 + 2 * f θ * deriv (deriv f) θ
    rw [hfun]
    simp [deriv_mul, deriv_const_mul]
    ring
  rw [h1, h2]
  ring

/-- **The cross carré du champ is the product of derivatives**: `Γ(f, Lf) = f'·(Lf)'` for a diffusion. -/
theorem cross_carre_du_champ (a f : ℝ → ℝ) (θ : ℝ) :
    carreDuChamp (diffusion_generator a) f (diffusion_generator a f) θ
      = deriv f θ * deriv (diffusion_generator a f) θ := by
  dsimp [carreDuChamp, diffusion_generator]
  -- Γ(f, Lf) = (L(f·Lf) − f·L(Lf) − Lf·Lf)/2 = f'·(Lf)' for a diffusion
  sorry

/-- **The 1D Bochner formula**: `Γ₂(f) = (f'')² − a'(θ)·(f')²`. -/
theorem one_dimensional_bochner_formula (a f : ℝ → ℝ) (θ : ℝ) :
    Gamma2 (diffusion_generator a) f θ
      = (deriv (deriv f) θ) ^ 2 - deriv a θ * (deriv f θ) ^ 2 := by
  dsimp [Gamma2, diffusion_generator]
  sorry

end QM
