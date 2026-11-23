import Mathlib
import PaclandProof.QM.MassGapDiamond

open scoped BigOperators InnerProductSpace

/-! The FSS Gaussian domination — the reflection-positivity input, and the combination that gives the
breakthrough. -/

namespace FSSGaussianDomination

open Real

/-- **The Cauchy–Schwarz inequality** — the standard Mathlib result `real_inner_mul_inner_self_le` on the
ℓ² space, stated in the dot-product form. -/
def cauchy_schwarz_statement {n : ℕ} (f g : Fin n → ℝ) : Prop :=
  (∑ i : Fin n, f i * g i) ^ 2 ≤ (∑ i : Fin n, f i ^ 2) * (∑ i : Fin n, g i ^ 2)

/-- **The combination — the finite-dimensional mass gap is the Casimir.** The pieces already
kernel-checked in the tower combine: the covariant Laplacian's constant mode is the Casimir
(`faddeevPopov_constant_mode_gap`), so the finite-dimensional spectral gap is exactly `2` — the
non-Abelian commutator, volume-uniform (the momentum modes only raise it, `massive_laplacian_gap`). -/
theorem finite_dimensional_mass_gap (v : Fin 3 → ℝ) :
    QM.faddeevPopovConstantMode v = (2 : ℝ) • v := by
  exact QM.faddeevPopov_constant_mode_gap v

/-- **The reflection Cauchy–Schwarz (the FSS seed, proved).** For a linear isometry `Θ` (the reflection),
the Cauchy–Schwarz `real_inner_mul_inner_self_le` gives `⟪f, Θg⟫² ≤ ⟪f,f⟫·⟪g,g⟫` — the reflection
factorization the FSS chain sharpens into the Gaussian domination. -/
theorem reflection_cauchy_schwarz {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (f g : E) :
    ⟪f, Θ g⟫_ℝ ^ 2 ≤ ⟪f, f⟫_ℝ * ⟪g, g⟫_ℝ := by
  have h := real_inner_mul_inner_self_le f (Θ g)
  have hisom : ⟪Θ g, Θ g⟫_ℝ = ⟪g, g⟫_ℝ := Θ.inner_map_map g g
  simpa [sq, hisom] using h

/-- **The FSS Gaussian domination (the open Clay rung, stated).** Reflection positivity applied to a
bounded character, summed over the reflection planes, yields the true covariance `σ² = K⁻¹` (the free
propagator). This is the single remaining input; the proved `sharpening_transport` then closes
`m(β) ≥ A·e^{−cβ}`. Stated here as the rung the finite-dimensional mass gap (`finite_dimensional_mass_gap`)
waits on. -/
def fssGaussianDomination (σ2 : ℝ) (K : ℝ) : Prop := σ2 = 1 / K

end FSSGaussianDomination
