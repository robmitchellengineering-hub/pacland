import Mathlib
import PaclandProof.QM.Bessel

/-!
# The integral representation's foundation — the orthogonality of cos on [0, π]

The derivative-free route to the small-field activity bound `1 − I₁/I₀ ≤ C/β` goes through the
integral representation `I_n(x) = (1/π)∫₀^π e^{x cos θ} cos(nθ) dθ`. Its foundation is the
orthogonality of the cosine family on [0, π]: the first harmonic integrates to zero and the squared
cosine normalizes to π/2. These are the first concrete steps of that route (the Jacobi–Anger
expansion and the concentration bound build on them).
-/

open Real intervalIntegral
open scoped BigOperators

namespace QM

/-- `∫₀^π cos θ dθ = 0` — the first harmonic integrates to zero (orthogonality to the constant). -/
theorem integral_cos_zero_pi : (∫ θ in (0 : ℝ)..π, Real.cos θ) = 0 := by
  have hderiv : ∀ x ∈ Set.uIcc (0 : ℝ) π, HasDerivAt (fun y : ℝ => Real.sin y) (Real.cos x) x := by
    intro x hx
    exact Real.hasDerivAt_sin x
  have hint : IntervalIntegrable (fun y : ℝ => Real.cos y) MeasureTheory.volume (0 : ℝ) π :=
    Real.continuous_cos.intervalIntegrable _ _
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint]
  simp [Real.sin_pi, Real.sin_zero]

/-- `∫₀^π cos² θ dθ = π/2` — the squared-cosine normalization. -/
theorem integral_cos_sq_pi : (∫ θ in (0 : ℝ)..π, Real.cos θ ^ 2) = π / 2 := by
  rw [integral_cos_sq]
  norm_num [Real.sin_pi, Real.sin_zero, Real.cos_pi, Real.cos_zero]

/-- **The Wallis recurrence**: `∫₀^π cos^{2m+2} θ = ((2m+1)/(2m+2))·∫₀^π cos^{2m} θ`. This is mathlib's
`integral_cos_pow` (the reduction formula) specialized to `[0, π]`, where the boundary term vanishes
(`sin π = sin 0 = 0`). The key input to the Jacobi–Anger expansion. -/
theorem wallis_recurrence (m : ℕ) :
    (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*m+2)) =
      ((2*m+1 : ℝ)/(2*m+2)) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*m)) := by
  rw [integral_cos_pow (a := (0 : ℝ)) (b := π) (n := 2*m)]
  simp [Real.sin_pi, Real.sin_zero]

end QM
