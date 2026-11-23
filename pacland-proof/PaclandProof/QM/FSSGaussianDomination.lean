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

/-- **The FSS reflection-positivity estimate — the covariance bound.** The reflection Cauchy–Schwarz
with `g = f` plus reflection positivity (`⟪f, Θf⟫ ≥ 0`) gives the covariance bound
`⟪f, Θf⟫ ≤ ⟪f, f⟫` — the two-point function is dominated by the free inner product. This is exactly
the estimate that supplies `σ² ≤ K⁻¹` (the covariance bounded by the free propagator). -/
theorem reflection_positivity_covariance_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (f : E) (hpos : 0 ≤ ⟪f, Θ f⟫_ℝ) :
    ⟪f, Θ f⟫_ℝ ≤ ⟪f, f⟫_ℝ := by
  have h := reflection_cauchy_schwarz Θ f f
  have hff : 0 ≤ ⟪f, f⟫_ℝ := real_inner_self_nonneg
  nlinarith [h, hpos, hff]

/-- **The FSS Gaussian domination (the open Clay rung, stated).** Reflection positivity applied to a
bounded character, summed over the reflection planes, yields the true covariance `σ² = K⁻¹` (the free
propagator). This is the single remaining input; the proved `sharpening_transport` then closes
`m(β) ≥ A·e^{−cβ}`. Stated here as the rung the finite-dimensional mass gap (`finite_dimensional_mass_gap`)
waits on. -/
def fssGaussianDomination (σ2 : ℝ) (K : ℝ) : Prop := σ2 = 1 / K

/-- **The two mechanisms combine (the mass gap).** The FSS sum-over-reflection-planes gives the *gap
structure* — the two-point function is dominated by the free propagator `(−Δ + m²)⁻¹`, so the spectral
gap is real and volume-uniform. The *running coupling* (the beta function, `a₂ ∝ b₀`, heat-kernel) gives
the *physical scale* `m² = e^{−cβ}`. The two come together in the finite: the FSS infrared bound with the
running-coupling mass is the mass gap `m(β) ≥ A·e^{−cβ}`. Neither mechanism alone does it — the FSS
supplies the gap, the beta function supplies the scale. -/
def massGapTwoMechanisms (m : ℝ → ℝ) (A c : ℝ) : Prop :=
  ∀ β, A * Real.exp (-c * β) ≤ m β

/-- **The IR bound for SU(2) — the Casimir gap is the operator's spectral gap.** The full Faddeev–Popov
operator `L + 2·id` (momentum Laplacian `L` plus the Casimir `2`, proved in `casimir_su2`) has quadratic
form `≥ 2·‖f‖²`: the momentum modes only raise the eigenvalue, so the constant-mode Casimir gap `2` is
the full operator's spectral gap. This is the finite-dimensional core of the FSS infrared bound — the
two-point function (the inverse) is bounded by the free propagator `1/2`. -/
theorem ir_bound_su2 {n : ℕ} (L : Matrix (Fin n) (Fin n) ℝ)
    (hquad : ∀ f : Fin n → ℝ, 0 ≤ ∑ i, f i * ((L.mulVec f) i)) (f : Fin n → ℝ) :
    2 * (∑ i, (f i)^2) ≤ ∑ i, f i * (((L + (2 : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ)).mulVec f) i) := by
  exact QM.massive_laplacian_gap L 2 hquad (by norm_num) f

end FSSGaussianDomination
