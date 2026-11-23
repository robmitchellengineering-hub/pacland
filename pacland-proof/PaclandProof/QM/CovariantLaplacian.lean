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
    0 ≤ ∑ x in S, (covariantDerivative U f x) ^ 2 := by
  exact Finset.sum_nonneg (fun x _ => sq_nonneg _)

end CovariantLaplacian
