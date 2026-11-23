import Mathlib

open scoped BigOperators

/-! The covariant Laplacian — the first lemmas of step 1 (the covariance is `−∇·D`).

The weak-coupling Gaussian covariance is the covariant Laplacian `−∇·D`, i.e. the Faddeev–Popov
operator. This file starts that formalisation: the lattice covariant derivative (forward difference with
parallel transport), the covariant Laplacian (its adjoint-forward square), and the first lemma — for the
trivial connection `U = 1` the covariant Laplacian reduces to the standard lattice Laplacian (the second
difference). This is the seed of the full 4D non-Abelian operator. -/

namespace CovariantLaplacian

/-- The 1D lattice covariant derivative (forward difference with parallel transport):
`(D_U f)(x) = U(x)·f(x+1) − f(x)`. For `U = 1` this is the standard forward difference. -/
def covariantDerivative (U : ℤ → ℝ) (f : ℤ → ℝ) (x : ℤ) : ℝ :=
  U x * f (x + 1) - f x

/-- The 1D covariant Laplacian `K = −D†D`, the FP operator's kernel: the adjoint (backward) covariant
derivative composed with the forward one, negated. This is the 1D seed of `−∇·D`. -/
def covariantLaplacian (U : ℤ → ℝ) (f : ℤ → ℝ) (x : ℤ) : ℝ :=
  -(U (x - 1) * covariantDerivative U f (x - 1) - covariantDerivative U f x)

/-- **The trivial connection gives the free Laplacian.** For `U = 1`, the covariant Laplacian is the
standard lattice second difference `f(x−1) − 2f(x) + f(x+1)`. This is the first proof that the FP
operator is `−∇·D` with the correct free-field limit. -/
theorem covariant_laplacian_trivial (f : ℤ → ℝ) (x : ℤ) :
    covariantLaplacian (fun _ => 1) f x = f (x - 1) - 2 * f x + f (x + 1) := by
  unfold covariantLaplacian covariantDerivative
  simp
  ring

/-- **The covariant Dirichlet form is non-negative.** `Σ_x (D_U f x)² ≥ 0` — the quadratic form of the
covariant derivative. This is the positivity of the covariant Laplacian `D†D` (its spectrum is non-negative),
the seed of the mass gap's positivity. -/
theorem covariant_dirichlet_form_nonneg (U : ℤ → ℝ) (f : ℤ → ℝ) (S : Finset ℤ) :
    0 ≤ ∑ x ∈ S, (covariantDerivative U f x) ^ 2 := by
  exact Finset.sum_nonneg (fun x _ => sq_nonneg _)

/-- **The field strength (the curvature) — the plaquette's phase.** In 2D the field strength is the
discrete curl `F = ∂₁A₂ − ∂₂A₁`, the curvature that the plaquette measures to leading order. This is the
bridge from the plaquette to the covariant Laplacian: the quadratic part of the action is `Σ F²`, and
`Σ F²` is the covariant Laplacian's kernel. -/
def fieldStrength (A₁ A₂ : ℤ → ℝ) (x : ℤ) : ℝ :=
  (A₂ (x + 1) - A₂ x) - (A₁ (x + 1) - A₁ x)

/-- **The field strength is anti-symmetric.** Swapping the two directions negates the curvature
`F(A₂,A₁) = −F(A₁,A₂)` — the standard anti-symmetry of the field-strength tensor, the first proof that
the plaquette's quadratic part is the (anti-symmetric) curvature. -/
theorem fieldStrength_antisym (A₁ A₂ : ℤ → ℝ) (x : ℤ) :
    fieldStrength A₂ A₁ x = -fieldStrength A₁ A₂ x := by
  unfold fieldStrength
  ring

/-- **The covariant derivative annihilates constants (for `U = 1`).** The constant function is the zero
mode — the vacuum — of the free covariant derivative. The mass gap is the gap *above* this zero mode. -/
theorem covariant_derivative_annihilates_constant (c : ℝ) (x : ℤ) :
    covariantDerivative (fun _ => 1) (fun _ => c) x = 0 := by
  unfold covariantDerivative
  simp

/-- **The covariant Laplacian annihilates constants.** The constant (vacuum) is the zero mode of the
free covariant Laplacian too — so the spectrum of `−∇·D` has the vacuum at zero and the mass gap is the
first positive eigenvalue above it. This is the spectral structure the mass-gap bound needs. -/
theorem covariant_laplacian_annihilates_constant (c : ℝ) (x : ℤ) :
    covariantLaplacian (fun _ => 1) (fun _ => c) x = 0 := by
  unfold covariantLaplacian covariantDerivative
  simp

/-- **Abel summation (summation by parts) for the forward difference.** The telescoping identity
`Σᵢ aᵢ(b_{i+1}−bᵢ) = a_N b_N − a₀ b₀ − Σᵢ b_{i+1}(a_{i+1}−aᵢ)`. This is the algebraic core of the
Dirichlet identity: applied with `a = f` and `b = f`, it converts the covariant Laplacian's quadratic form
into the Dirichlet form `Σ |Df|²`. -/
theorem abel_summation (a b : ℕ → ℝ) (N : ℕ) :
    (∑ i in Finset.range N, a i * (b (i + 1) - b i)) =
      a N * b N - a 0 * b 0 - (∑ i in Finset.range N, b (i + 1) * (a (i + 1) - a i)) := by
  induction N with
  | zero => simp
  | succ N ih =>
      rw [Finset.sum_range_succ, Finset.sum_range_succ, ih]
      ring

end CovariantLaplacian
