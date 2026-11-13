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
open scoped MeasureTheory
open Filter

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

/-- `(e^{-x²/2})' = -x e^{-x²/2}` — the derivative of the Gaussian density. -/
lemma gaussian_density_deriv (x : ℝ) :
    deriv (fun y => Real.exp (-y ^ 2 / 2)) x = -x * Real.exp (-x ^ 2 / 2) := by
  have hg : DifferentiableAt ℝ (fun y => -y ^ 2 / 2) x := by
    rw [show (fun y => -y ^ 2 / 2) = fun y => ((-1 : ℝ) / 2) * y ^ 2 by funext y; ring]
    exact (differentiableAt_id.pow 2).const_mul ((-1 : ℝ) / 2)
  rw [deriv_exp hg]
  have h : deriv (fun y => -y ^ 2 / 2) x = -x := by
    rw [show (fun y => -y ^ 2 / 2) = fun y => ((-1 : ℝ) / 2) * y ^ 2 by funext y; ring]
    rw [deriv_const_mul]
    · have hpow : deriv (fun y => y ^ 2) x = 2 * x := by
        rw [show (fun y => y ^ 2) = id ^ 2 by rfl]
        simp [id, deriv_id', deriv_pow]
      rw [hpow]
      ring
    · exact differentiableAt_id.pow 2
  rw [h]
  ring

/-- `HasDerivAt` form of the Gaussian density derivative, for the integration-by-parts input. -/
lemma gaussian_density_hasDerivAt (x : ℝ) :
    HasDerivAt (fun y => Real.exp (-y ^ 2 / 2)) (-x * Real.exp (-x ^ 2 / 2)) x := by
  have hg : HasDerivAt (fun y => -y ^ 2 / 2) (-x) x := by
    have hpow : HasDerivAt (fun y => y ^ 2) (2 * x) x := by
      simpa using (hasDerivAt_pow 2 x)
    have h := hpow.const_mul ((-1 : ℝ) / 2)
    rw [show (fun y => ((-1 : ℝ) / 2) * y ^ 2) = fun y => -y ^ 2 / 2 by funext y; ring] at h
    convert h using 1
    ring
  have h := (Real.hasDerivAt_exp (x := -x ^ 2 / 2)).comp x hg
  rw [mul_comm]
  exact h

/-- **The Gaussian integration by parts**: `∫ e^{-x²/2} f' = ∫ e^{-x²/2} x f`.

From `integral_deriv_mul_eq_sub` with `u = f`, `v = e^{-x²/2}` (derivative `-x e^{-x²/2}`), boundary
terms vanishing. This is the Dirichlet-form identity feeding the direct Bakry-Émery route. -/
theorem gaussian_ibp (f : ℝ → ℝ)
    (hfd : ∀ x, HasDerivAt f (deriv f x) x)
    (hint1 : MeasureTheory.Integrable (fun x => deriv f x * Real.exp (-x^2/2)) MeasureTheory.volume)
    (hint2 : MeasureTheory.Integrable (fun x => f x * (-x * Real.exp (-x^2/2))) MeasureTheory.volume)
    (hbot : Tendsto (fun x => f x * Real.exp (-x^2/2)) atBot (nhds 0))
    (htop : Tendsto (fun x => f x * Real.exp (-x^2/2)) atTop (nhds 0)) :
    ∫ x, deriv f x * Real.exp (-x^2/2) = ∫ x, f x * x * Real.exp (-x^2/2) := by
  have hv : ∀ x ∈ tsupport f, HasDerivAt (fun y => Real.exp (-y^2/2)) (-x * Real.exp (-x^2/2)) x := by
    intro x hx
    exact gaussian_density_hasDerivAt x
  have h := MeasureTheory.integral_deriv_mul_eq_sub
    (u := f) (v := fun x => Real.exp (-x^2/2))
    (u' := deriv f) (v' := fun x => -x * Real.exp (-x^2/2))
    (hu := by intro x hx; exact hfd x) (hv := hv) (huv := hint1.add hint2) (h_bot := hbot) (h_top := htop)
  have hsplit : (∫ x, deriv f x * Real.exp (-x^2/2)) + (∫ x, f x * (-x * Real.exp (-x^2/2))) = 0 := by
    rw [← MeasureTheory.integral_add hint1 hint2]
    simpa using h
  have hneg : (∫ x, f x * (-x * Real.exp (-x^2/2))) = -(∫ x, f x * (x * Real.exp (-x^2/2))) := by
    have hcongr : (∫ x, f x * (-x * Real.exp (-x^2/2))) = (∫ x, -(f x * (x * Real.exp (-x^2/2)))) := by
      apply MeasureTheory.integral_congr_ae
      filter_upwards with x
      ring
    rw [hcongr]
    rw [MeasureTheory.integral_neg]
  rw [hneg] at hsplit
  have hC : (∫ x, f x * x * Real.exp (-x^2/2)) = (∫ x, f x * (x * Real.exp (-x^2/2))) := by
    apply MeasureTheory.integral_congr_ae
    filter_upwards with x
    ring
  rw [hC]
  nlinarith

/-- **The Bochner–Lichnerowicz formula (OU case)**: `L(Γ f) = 2Γ(f, Lf) + 2Γ₂(f)`, pointwise.

This is the identity behind the Fisher decay `I' ≤ -2κI` in the Bakry–Émery interpolation: integrated
against `γ`, the `Γ₂` term is bounded below by `κΓ` (the committed curvature), giving the decay. -/
theorem bochner_lichnerowicz (f : ℝ → ℝ)
    (hf : Differentiable ℝ f) (hf' : Differentiable ℝ (deriv f)) (hf'' : Differentiable ℝ (deriv (deriv f)))
    (hf''' : Differentiable ℝ (deriv (deriv (deriv f)))) :
    ouGenerator (fun x => carreDuChamp ouGenerator f f x) =
      fun x => 2 * carreDuChamp ouGenerator f (ouGenerator f) x + 2 * Gamma2 ouGenerator f x := by
  have hLf : Differentiable ℝ (ouGenerator f) := hf''.sub (differentiable_id.mul hf')
  have hLf' : Differentiable ℝ (deriv (ouGenerator f)) := by
    rw [show deriv (ouGenerator f) = fun y => deriv (deriv (deriv f)) y - deriv f y - (fun y => y) y * deriv (deriv f) y by
      funext y; rw [deriv_ou f hf' hf'' y]]
    exact (hf'''.sub hf').sub (differentiable_id.mul hf'')
  funext x
  have hd1 : deriv (fun y => (deriv f y) ^ 2) x = 2 * deriv f x * deriv (deriv f) x := deriv_deriv_sq f hf' x
  have hd2 : deriv (deriv (fun y => (deriv f y) ^ 2)) x = 2 * (deriv (deriv f) x) ^ 2 + 2 * deriv f x * deriv (deriv (deriv f)) x := by
    rw [show deriv (fun y => (deriv f y) ^ 2) = fun y => 2 * (deriv f y * deriv (deriv f) y) by
      funext y; rw [deriv_deriv_sq f hf' y]; ring]
    rw [deriv_const_mul]
    · change 2 * deriv (deriv f * deriv (deriv f)) x = 2 * (deriv (deriv f) x) ^ 2 + 2 * deriv f x * deriv (deriv (deriv f)) x
      rw [deriv_mul (hf' x) (hf'' x)]
      ring
    · exact (hf' x).mul (hf'' x)
  rw [show ouGenerator (fun x => carreDuChamp ouGenerator f f x) = fun y => deriv (deriv (fun z => (deriv f z) ^ 2)) y - (fun y => y) y * deriv (fun z => (deriv f z) ^ 2) y by
    funext y
    have h : carreDuChamp ouGenerator f f = fun z => (deriv f z) ^ 2 := by
      funext z; rw [ou_carre_du_champ_general f f hf hf hf' hf' z]; ring
    simp [h]
    rfl]
  change deriv (deriv (fun z => deriv f z ^ 2)) x - x * deriv (fun z => deriv f z ^ 2) x = 2 * carreDuChamp ouGenerator f (ouGenerator f) x + 2 * Gamma2 ouGenerator f x
  rw [hd2, hd1]
  rw [show carreDuChamp ouGenerator f (ouGenerator f) x = deriv f x * deriv (ouGenerator f) x by
    exact ou_carre_du_champ_general f (ouGenerator f) hf hLf hf' hLf' x]
  rw [show Gamma2 ouGenerator f x = (deriv (deriv f) x) ^ 2 + (deriv f x) ^ 2 by
    exact ou_gamma2 f hf hf' hf'' hf''' x]
  rw [deriv_ou f hf' hf'' x]
  ring

/-- **The OU generator has mean zero against the Gaussian** (the invariant measure):
`∫ e^{-x²/2} · Lg = 0`. From the committed integration-by-parts `∫ γ g'' = ∫ γ x g'`, the two
terms in `Lg = g'' - x g'` cancel. This is the divergence form that turns the Bochner–Lichnerowicz
formula into the Fisher decay `I' = -2∫γ Γ₂`. -/
theorem ou_invariant (g : ℝ → ℝ)
    (hgd' : ∀ x, HasDerivAt (deriv g) (deriv (deriv g) x) x)
    (hint1 : MeasureTheory.Integrable (fun x => deriv (deriv g) x * Real.exp (-x^2/2)) MeasureTheory.volume)
    (hint2 : MeasureTheory.Integrable (fun x => (deriv g x) * (-x * Real.exp (-x^2/2))) MeasureTheory.volume)
    (hbot : Tendsto (fun x => deriv g x * Real.exp (-x^2/2)) atBot (nhds 0))
    (htop : Tendsto (fun x => deriv g x * Real.exp (-x^2/2)) atTop (nhds 0)) :
    ∫ x, Real.exp (-x^2/2) * ouGenerator g x = 0 := by
  have hibp := gaussian_ibp (deriv g) hgd' hint1 hint2 hbot htop
  rw [show ouGenerator g = fun x => deriv (deriv g) x - x * deriv g x by rfl]
  have hsplit : (∫ x, Real.exp (-x^2/2) * (deriv (deriv g) x - x * deriv g x)) =
      (∫ x, Real.exp (-x^2/2) * deriv (deriv g) x) - (∫ x, Real.exp (-x^2/2) * (x * deriv g x)) := by
    rw [show (fun x => Real.exp (-x^2/2) * (deriv (deriv g) x - x * deriv g x)) = fun x => Real.exp (-x^2/2) * deriv (deriv g) x - Real.exp (-x^2/2) * (x * deriv g x) by funext x; ring]
    rw [MeasureTheory.integral_sub]
    · exact (by simpa [mul_comm] using hint1)
    · exact (by simpa [mul_comm, mul_left_comm, mul_assoc] using hint2.neg)
  rw [hsplit]
  rw [show (∫ x, Real.exp (-x^2/2) * deriv (deriv g) x) = (∫ x, Real.exp (-x^2/2) * (x * deriv g x)) by
    simpa [mul_comm, mul_left_comm, mul_assoc] using hibp]
  ring

/-- **The Dirichlet form (self-adjointness of the OU generator)**: `∫ e^{-x²/2} f·Lg = -∫ e^{-x²/2} f'·g'`. -/
theorem gaussian_dirichlet (f g : ℝ → ℝ)
    (hfg : ∀ x, HasDerivAt (fun y => f y * deriv g y) (deriv (fun y => f y * deriv g y) x) x)
    (hprod : deriv (fun y => f y * deriv g y) = fun x => deriv f x * deriv g x + f x * deriv (deriv g) x)
    (hint1 : MeasureTheory.Integrable (fun x => deriv (fun y => f y * deriv g y) x * Real.exp (-x^2/2)) MeasureTheory.volume)
    (hint2 : MeasureTheory.Integrable (fun x => (f x * deriv g x) * (-x * Real.exp (-x^2/2))) MeasureTheory.volume)
    (hint3 : MeasureTheory.Integrable (fun x => Real.exp (-x^2/2) * (deriv f x * deriv g x)) MeasureTheory.volume)
    (hint4 : MeasureTheory.Integrable (fun x => Real.exp (-x^2/2) * (f x * deriv (deriv g) x)) MeasureTheory.volume)
    (hint5 : MeasureTheory.Integrable (fun x => Real.exp (-x^2/2) * (f x * (x * deriv g x))) MeasureTheory.volume)
    (hbot : Tendsto (fun x => Real.exp (-x^2/2) * (f x * deriv g x)) atBot (nhds 0))
    (htop : Tendsto (fun x => Real.exp (-x^2/2) * (f x * deriv g x)) atTop (nhds 0)) :
    ∫ x, Real.exp (-x^2/2) * f x * ouGenerator g x = -∫ x, Real.exp (-x^2/2) * deriv f x * deriv g x := by
  have hibp := gaussian_ibp (fun y => f y * deriv g y) hfg hint1 hint2 (by simpa [mul_comm] using hbot) (by simpa [mul_comm] using htop)
  rw [hprod] at hibp
  have hsplit : (∫ x, Real.exp (-x^2/2) * (deriv f x * deriv g x)) + (∫ x, Real.exp (-x^2/2) * (f x * deriv (deriv g) x)) = (∫ x, Real.exp (-x^2/2) * (f x * deriv g x) * x) := by
    have hsum : (∫ x, Real.exp (-x^2/2) * (deriv f x * deriv g x) + Real.exp (-x^2/2) * (f x * deriv (deriv g) x)) = (∫ x, Real.exp (-x^2/2) * (deriv f x * deriv g x + f x * deriv (deriv g) x)) := by
      apply MeasureTheory.integral_congr_ae
      filter_upwards with x
      ring
    rw [← MeasureTheory.integral_add hint3 hint4]
    rw [hsum]
    simpa [mul_assoc, mul_comm, mul_left_comm] using hibp
  have hfg2 : (∫ x, Real.exp (-x^2/2) * (f x * deriv (deriv g) x)) = (∫ x, Real.exp (-x^2/2) * (f x * deriv g x) * x) - (∫ x, Real.exp (-x^2/2) * (deriv f x * deriv g x)) := by
    linarith
  rw [show ouGenerator g = fun x => deriv (deriv g) x - x * deriv g x by rfl]
  have hdist : (∫ x, Real.exp (-x^2/2) * f x * (deriv (deriv g) x - x * deriv g x)) = (∫ x, Real.exp (-x^2/2) * (f x * deriv (deriv g) x)) - (∫ x, Real.exp (-x^2/2) * (f x * (x * deriv g x))) := by
    have hf : (fun x => Real.exp (-x^2/2) * f x * (deriv (deriv g) x - x * deriv g x)) = fun x => Real.exp (-x^2/2) * (f x * deriv (deriv g) x) - Real.exp (-x^2/2) * (f x * (x * deriv g x)) := by
      funext x; ring
    rw [hf]
    rw [MeasureTheory.integral_sub hint4 hint5]
  rw [hdist]
  have hcongr : (∫ x, Real.exp (-x^2/2) * (f x * (x * deriv g x))) = (∫ x, Real.exp (-x^2/2) * (f x * deriv g x) * x) := by
    apply MeasureTheory.integral_congr_ae
    filter_upwards with x
    ring
  rw [hcongr]
  rw [hfg2]
  ring

end QM
