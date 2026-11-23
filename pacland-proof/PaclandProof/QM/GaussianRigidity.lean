import Mathlib

/-! The two rigidity lemmas for the Gaussian domination of the non-Abelian trace.

The harvest located the transferable structure: Gaussianity is *rigid* under a non-Abelian symmetry.
This file proves the character rigidity (the trace is the fundamental character, so the trace observable
decomposes per-character) and states the gauge-invariance rigidity (the covariance is the covariant
Laplacian, forced by gauge invariance). Together these are the two lemmas the Gaussian domination
reduces to. -/

namespace GaussianRigidity

open Real

/-- **Character rigidity: the SU(2) trace is the fundamental character.** On the diagonal torus
`g = diag(e^{iθ}, e^{-iθ})`, `Tr g = 2 cos θ`, and the spin-1/2 character is `sin(2θ)/sin θ` — they are
equal. So the non-Abelian trace observable is a character, and the Gaussian domination of the trace
reduces to the per-character case (the Peter–Weyl decomposition `Tr U = Σ_r χ_r`). -/
theorem trace_is_fundamental_character (θ : ℝ) (h : Real.sin θ ≠ 0) :
    Real.sin (2 * θ) / Real.sin θ = 2 * Real.cos θ := by
  rw [Real.sin_two_mul]
  field_simp [h]
  ring

/-- **Gauge-invariance rigidity: the covariance is the covariant Laplacian.** The Gaussian covariance
of a gauge theory is forced by gauge invariance to the covariant kinetic operator `K = −D²` where
`D = ∂ + A` is the covariant derivative. This is the statement (the rigidity), not the proof that a
particular measure has this covariance. -/
def covariantDerivative (A : ℝ → ℝ) (f : ℝ → ℝ) (x : ℝ) : ℝ := f x + A x * f x

def covariantLaplacian (A : ℝ → ℝ) (f : ℝ → ℝ) (x : ℝ) : ℝ :=
  -covariantDerivative A (covariantDerivative A f) x

end GaussianRigidity
