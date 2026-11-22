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
  have hf1' : Differentiable ℝ (deriv f) := ContDiff.differentiable_deriv_two hf
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
    change deriv ((fun y => 2 * f y) * deriv f) θ = 2 * (deriv f θ) ^ 2 + 2 * f θ * deriv (deriv f) θ
    rw [deriv_mul]
    · rw [deriv_const_mul (2 : ℝ) (hf1 θ)]
      ring
    · exact (hf1.const_smul (2 : ℝ)) θ
    · exact hf1' θ
  rw [h1, h2]
  ring

/-- **The general carré du champ**: `Γ(f, g) = f'·g'` for a diffusion generator. -/
theorem carre_du_champ_eq_mul (a f g : ℝ → ℝ) (θ : ℝ) (hf : ContDiff ℝ 2 f) (hg : ContDiff ℝ 2 g) :
    carreDuChamp (diffusion_generator a) f g θ = deriv f θ * deriv g θ := by
  dsimp [carreDuChamp, diffusion_generator]
  have hf1 : Differentiable ℝ f := hf.differentiable (by norm_num)
  have hg1 : Differentiable ℝ g := hg.differentiable (by norm_num)
  have hf1' : Differentiable ℝ (deriv f) := ContDiff.differentiable_deriv_two hf
  have hg1' : Differentiable ℝ (deriv g) := ContDiff.differentiable_deriv_two hg
  -- L(fg) − f·Lg − g·Lf = 2·f'·g'  (the diffusion identity)
  have hderiv_fg : deriv (f * g) = fun y => deriv f y * g y + f y * deriv g y := by
    funext y
    rw [deriv_mul (hf1 y) (hg1 y)]
  have hfg : deriv (fun t => f t * g t) θ = deriv f θ * g θ + f θ * deriv g θ := by
    rw [hderiv_fg]
  have hfg2 : deriv (deriv (fun t => f t * g t)) θ
      = deriv (deriv f) θ * g θ + 2 * (deriv f θ * deriv g θ) + f θ * deriv (deriv g) θ := by
    change deriv (deriv (f * g)) θ = _
    rw [hderiv_fg]
    rw [deriv_add]
    rw [deriv_mul (hf1' θ) (hg1 θ)]
    rw [deriv_mul (hf1 θ) (hg1' θ)]
    ring
  rw [hfg, hfg2]
  ring

/-- **The cross carré du champ is the product of derivatives**: `Γ(f, Lf) = f'·(Lf)'`. -/
theorem cross_carre_du_champ (a f : ℝ → ℝ) (θ : ℝ) (hf : ContDiff ℝ 3 f) :
    carreDuChamp (diffusion_generator a) f (diffusion_generator a f) θ
      = deriv f θ * deriv (diffusion_generator a f) θ := by
  sorry

/-- **The 1D Bochner formula**: `Γ₂(f) = (f'')² − a'(θ)·(f')²`. -/
theorem one_dimensional_bochner_formula (a f : ℝ → ℝ) (θ : ℝ) (hf : ContDiff ℝ 3 f) :
    Gamma2 (diffusion_generator a) f θ
      = (deriv (deriv f) θ) ^ 2 - deriv a θ * (deriv f θ) ^ 2 := by
  dsimp [Gamma2, diffusion_generator]
  sorry

end QM
