import Mathlib
import PaclandProof.QM.BakryEmery

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The 1D Ornstein-Uhlenbeck carré du champ (the Gaussian curvature input)

For the OU generator `L f = f'' − x·f'` (the generator of the standard Gaussian), the carré du champ
is `Γ(f) = (f')²`. This file proves that computation against mathlib's `deriv` rules — the first
derivative computation in the Gaussian-LSI chain.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The Ornstein–Uhlenbeck generator of the standard Gaussian: `L f = f'' − x·f'`. -/
def ouGenerator (f : ℝ → ℝ) (x : ℝ) : ℝ :=
  deriv (deriv f) x - x * deriv f x

/-- `(f·f)' = 2 f f'` (the product rule). -/
lemma deriv_sq (f : ℝ → ℝ) (hf : Differentiable ℝ f) (x : ℝ) :
    deriv (fun y => f y * f y) x = 2 * f x * deriv f x := by
  change deriv (f * f) x = 2 * f x * deriv f x
  rw [deriv_mul (hf x) (hf x)]
  ring

/-- `(f f')' = (f')² + f f''` (the product rule). -/
lemma deriv_mul_deriv (f : ℝ → ℝ) (hf : Differentiable ℝ f) (hf' : Differentiable ℝ (deriv f)) (x : ℝ) :
    deriv (fun y => f y * deriv f y) x = (deriv f x) ^ 2 + f x * deriv (deriv f) x := by
  change deriv (f * deriv f) x = (deriv f x) ^ 2 + f x * deriv (deriv f) x
  rw [deriv_mul (hf x) (hf' x)]
  ring

/-- **The carré du champ of the OU generator is `Γ(f) = (f')²`.**

Proof: `Γ(f) = (L(f²) − 2f·Lf)/2`. Compute `L(f²) = 2(f')² + 2f f'' − 2x f f'` and
`2f·Lf = 2f f'' − 2x f f'`, so the difference is `2(f')²`, and dividing by 2 gives `(f')²`. -/
theorem ou_carre_du_champ (f : ℝ → ℝ) (hf : Differentiable ℝ f) (hf' : Differentiable ℝ (deriv f)) (x : ℝ) :
    carreDuChamp ouGenerator f f x = (deriv f x) ^ 2 := by
  dsimp [carreDuChamp, ouGenerator]
  have hsq : deriv (fun y => f y * f y) x = 2 * f x * deriv f x := deriv_sq f hf x
  have h2f : Differentiable ℝ (fun y => 2 * f y) := fun y => (hf y).const_mul 2
  have hsq' : deriv (deriv (fun y => f y * f y)) x = 2 * (deriv f x) ^ 2 + 2 * f x * deriv (deriv f) x := by
    calc
      deriv (deriv (fun y => f y * f y)) x = deriv (fun y => 2 * f y * deriv f y) x := by
        congr 1
        funext y
        exact deriv_sq f hf y
      _ = deriv (fun y => 2 * f y) x * deriv f x + (2 * f x) * deriv (deriv f) x := by
        change deriv ((fun y => 2 * f y) * deriv f) x = deriv (fun y => 2 * f y) x * deriv f x + (2 * f x) * deriv (deriv f) x
        rw [deriv_mul (h2f x) (hf' x)]
      _ = (2 * deriv f x) * deriv f x + (2 * f x) * deriv (deriv f) x := by
        rw [deriv_const_mul (2 : ℝ) (hf x)]
      _ = 2 * (deriv f x) ^ 2 + 2 * f x * deriv (deriv f) x := by ring
  rw [hsq, hsq']
  ring

end QM
