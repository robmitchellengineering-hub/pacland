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

/-- **The diffusion identity: `Γ(f,g) = f'·g'`** for the OU generator.

A second-order diffusion `L f = a f'' + b f'` has carré du champ `Γ(f,g) = a f'·g'`; for the OU
generator `a = 1`, so `Γ(f,g) = f'·g'`. Proof: `Γ = (L(fg) − f Lg − g Lf)/2`, and the second-derivative
cross terms cancel, leaving `2 f' g'`. -/
theorem ou_carre_du_champ_general (f g : ℝ → ℝ) (hf : Differentiable ℝ f) (hg : Differentiable ℝ g)
    (hf' : Differentiable ℝ (deriv f)) (hg' : Differentiable ℝ (deriv g)) (x : ℝ) :
    carreDuChamp ouGenerator f g x = deriv f x * deriv g x := by
  dsimp [carreDuChamp, ouGenerator]
  have hfg : deriv (fun y => f y * g y) x = deriv f x * g x + f x * deriv g x := by
    change deriv (f * g) x = deriv f x * g x + f x * deriv g x
    rw [deriv_mul (hf x) (hg x)]
  have hfg2 : deriv (deriv (fun y => f y * g y)) x = deriv (deriv f) x * g x + 2 * deriv f x * deriv g x + f x * deriv (deriv g) x := by
    calc
      deriv (deriv (fun y => f y * g y)) x = deriv (fun y => deriv f y * g y + f y * deriv g y) x := by
        congr 1
        funext y
        change deriv (f * g) y = deriv f y * g y + f y * deriv g y
        rw [deriv_mul (hf y) (hg y)]
      _ = deriv (fun y => deriv f y * g y) x + deriv (fun y => f y * deriv g y) x := by
        change deriv (deriv f * g + f * deriv g) x = deriv (deriv f * g) x + deriv (f * deriv g) x
        rw [deriv_add ((hf'.mul hg) x) ((hf.mul hg') x)]
      _ = (deriv (deriv f) x * g x + deriv f x * deriv g x) + (deriv f x * deriv g x + f x * deriv (deriv g) x) := by
        change deriv (deriv f * g) x + deriv (f * deriv g) x = (deriv (deriv f) x * g x + deriv f x * deriv g x) + (deriv f x * deriv g x + f x * deriv (deriv g) x)
        rw [deriv_mul (hf' x) (hg x)]
        rw [deriv_mul (hf x) (hg' x)]
      _ = deriv (deriv f) x * g x + 2 * deriv f x * deriv g x + f x * deriv (deriv g) x := by ring
  rw [hfg, hfg2]
  ring

/-- `(Lf)' = f''' − f' − x f''` — the derivative of the OU generator. -/
lemma deriv_ou (f : ℝ → ℝ) (hf' : Differentiable ℝ (deriv f)) (hf'' : Differentiable ℝ (deriv (deriv f))) (x : ℝ) :
    deriv (ouGenerator f) x = deriv (deriv (deriv f)) x - deriv f x - x * deriv (deriv f) x := by
  rw [show ouGenerator f = deriv (deriv f) - id * deriv f by rfl]
  rw [deriv_sub (hf'' x) ((differentiable_id.mul hf') x)]
  rw [deriv_mul (differentiable_id x) (hf' x)]
  rw [deriv_id']
  rw [show id x = x by rfl]
  ring

/-- `((f')²)' = 2 f' f''` — the derivative of the squared derivative. -/
lemma deriv_deriv_sq (f : ℝ → ℝ) (hf' : Differentiable ℝ (deriv f)) (x : ℝ) :
    deriv (fun y => (deriv f y) ^ 2) x = 2 * deriv f x * deriv (deriv f) x := by
  change deriv ((deriv f) ^ 2) x = 2 * deriv f x * deriv (deriv f) x
  simpa using (deriv_pow (hf' x) 2)

/-- **The iterated carré du champ is `Γ₂(f) = (f'')² + (f')²`** (the Bochner formula, curvature 1). -/
theorem ou_gamma2 (f : ℝ → ℝ) (hf : Differentiable ℝ f) (hf' : Differentiable ℝ (deriv f))
    (hf'' : Differentiable ℝ (deriv (deriv f))) (hf''' : Differentiable ℝ (deriv (deriv (deriv f)))) (x : ℝ) :
    Gamma2 ouGenerator f x = (deriv (deriv f) x) ^ 2 + (deriv f x) ^ 2 := by
  dsimp [Gamma2]
  have hΓ : carreDuChamp ouGenerator f f = fun y => (deriv f y) ^ 2 := by
    funext y
    exact ou_carre_du_champ f hf hf' y
  have hg : Differentiable ℝ (ouGenerator f) := by
    intro y
    change DifferentiableAt ℝ (fun z => deriv (deriv f) z - z * deriv f z) y
    exact (hf'' y).sub ((differentiable_id.mul hf') y)
  have hg' : Differentiable ℝ (deriv (ouGenerator f)) := by
    have hderiv : deriv (ouGenerator f) = fun y => deriv (deriv (deriv f)) y - deriv f y - y * deriv (deriv f) y := by
      funext y
      exact deriv_ou f hf' hf'' y
    rw [hderiv]
    intro y
    exact ((hf''' y).sub (hf' y)).sub ((differentiable_id.mul hf'') y)
  have hΓgen : carreDuChamp ouGenerator f (ouGenerator f) x = deriv f x * deriv (ouGenerator f) x :=
    ou_carre_du_champ_general f (ouGenerator f) hf hg hf' hg' x
  have h1 : deriv (ouGenerator f) x = deriv (deriv (deriv f)) x - deriv f x - x * deriv (deriv f) x :=
    deriv_ou f hf' hf'' x
  have h2 : deriv (fun y => (deriv f y) ^ 2) x = 2 * deriv f x * deriv (deriv f) x :=
    deriv_deriv_sq f hf' x
  have h3 : deriv (deriv (fun y => (deriv f y) ^ 2)) x = 2 * (deriv (deriv f) x) ^ 2 + 2 * deriv f x * deriv (deriv (deriv f)) x := by
    calc
      deriv (deriv (fun y => (deriv f y) ^ 2)) x = deriv (fun y => 2 * deriv f y * deriv (deriv f) y) x := by
        congr 1
        funext y
        exact deriv_deriv_sq f hf' y
      _ = 2 * (deriv (deriv f) x) ^ 2 + 2 * deriv f x * deriv (deriv (deriv f)) x := by
        rw [show (fun y => 2 * deriv f y * deriv (deriv f) y) = fun y => (2 * deriv f y) * deriv (deriv f) y by rfl]
        rw [show (fun y => (2 * deriv f y) * deriv (deriv f) y) = (fun y => 2 * deriv f y) * deriv (deriv f) by rfl]
        rw [deriv_mul ((fun y => (hf' y).const_mul 2) x) (hf'' x)]
        rw [deriv_const_mul (2 : ℝ) (hf' x)]
        ring
  rw [hΓ]
  rw [hΓgen]
  rw [h1]
  dsimp [ouGenerator]
  rw [h2, h3]
  ring_nf

/-- **The OU generator has Bakry–Émery curvature 1** (`Γ₂ ≥ Γ`), from the Bochner formula
`Γ₂ = (f'')² + (f')² ≥ (f')²`. This is the curvature input that gives the Gaussian LSI. -/
theorem ou_bakry_emery (f : ℝ → ℝ) (hf : Differentiable ℝ f) (hf' : Differentiable ℝ (deriv f))
    (hf'' : Differentiable ℝ (deriv (deriv f))) (hf''' : Differentiable ℝ (deriv (deriv (deriv f)))) (x : ℝ) :
    carreDuChamp ouGenerator f f x ≤ Gamma2 ouGenerator f x := by
  rw [ou_gamma2 f hf hf' hf'' hf''' x]
  rw [ou_carre_du_champ f hf hf' x]
  nlinarith [sq_nonneg (deriv (deriv f) x)]

end QM
