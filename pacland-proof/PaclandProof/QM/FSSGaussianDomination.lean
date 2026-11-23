import Mathlib

open scoped BigOperators

/-! The FSS Gaussian domination — the reflection-positivity input, done properly. -/

namespace FSSGaussianDomination

open Real

/-- **The Cauchy–Schwarz inequality**, via the inner-product Cauchy–Schwarz `norm_inner_le_norm` and the
explicit form of the Pi inner product and ℓ² norm. -/
theorem cauchy_schwarz {n : ℕ} (f g : Fin n → ℝ) :
    (∑ i : Fin n, f i * g i) ^ 2 ≤ (∑ i : Fin n, f i ^ 2) * (∑ i : Fin n, g i ^ 2) := by
  have h := norm_inner_le_norm (E := Fin n → ℝ) f g
  have hsq : ‖⟪f, g⟫_ℝ‖ ^ 2 ≤ ‖f‖ ^ 2 * ‖g‖ ^ 2 := by
    nlinarith [h, norm_nonneg ⟪f, g⟫_ℝ, norm_nonneg f, norm_nonneg g]
  simpa using hsq

end FSSGaussianDomination
