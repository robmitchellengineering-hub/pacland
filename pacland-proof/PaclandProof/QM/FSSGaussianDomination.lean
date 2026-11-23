import Mathlib

open scoped BigOperators

/-! The FSS Gaussian domination — the reflection-positivity input, done properly. -/

namespace FSSGaussianDomination

open Real

/-- **The Cauchy–Schwarz inequality**, via Mathlib's `real_inner_mul_inner_self_le` on the Euclidean
(ℓ²) space `EuclideanSpace ℝ (Fin n)`, whose inner product is the dot product. -/
theorem cauchy_schwarz {n : ℕ} (f g : Fin n → ℝ) :
    (∑ i : Fin n, f i * g i) ^ 2 ≤ (∑ i : Fin n, f i ^ 2) * (∑ i : Fin n, g i ^ 2) := by
  have h := real_inner_mul_inner_self_le (E := EuclideanSpace ℝ (Fin n)) (fun i => f i) (fun i => g i)
  simpa [EuclideanSpace.inner_apply, sq] using h

end FSSGaussianDomination
