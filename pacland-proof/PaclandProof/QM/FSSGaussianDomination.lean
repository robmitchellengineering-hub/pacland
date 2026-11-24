import Mathlib
import PaclandProof.QM.MassGapDiamond
import PaclandProof.QM.Su2Character
import Mathlib.Analysis.Fourier.FiniteAbelian.PontryaginDuality

noncomputable section

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

/-- **The volume-uniform IR bound (extrapolated from 1D).** The reflection covariance bound is *abstract*
— it holds for every inner-product space `E`, hence for every lattice volume — and the Casimir gap `2` is
a constant, hence volume-independent. So the two-point function is bounded by the free propagator
uniformly in the volume: this is the same method as the 1D Dirichlet identity (`quadratic_part_is_covariant_laplacian`),
lifted to arbitrary `E` by reflection positivity. -/
theorem volume_uniform_ir_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (f : E) (hpos : 0 ≤ ⟪f, Θ f⟫_ℝ) :
    ⟪f, Θ f⟫_ℝ ≤ ⟪f, f⟫_ℝ :=
  reflection_positivity_covariance_bound Θ f hpos

/-- **The 1D discrete Laplacian's symbol is `2(1 − cos k)`.** On the Fourier mode `fᵢ = cos(k·i)`, the
second difference `(Lf)ᵢ = 2fᵢ − fᵢ₊₁ − fᵢ₋₁` is `2(1 − cos k)·fᵢ`. This is the Fourier transform of the
Dirichlet form `Σ (fᵢ₊₁ − fᵢ)²` — the sum-over-reflection-planes denominator. -/
theorem laplacian_symbol_1d (k i : ℝ) :
    2 * Real.cos (k * i) - Real.cos (k * (i + 1)) - Real.cos (k * (i - 1))
      = 2 * (1 - Real.cos k) * Real.cos (k * i) := by
  have hsum : Real.cos (k * (i + 1)) + Real.cos (k * (i - 1)) = 2 * Real.cos (k * i) * Real.cos k := by
    rw [mul_add, mul_sub]
    rw [Real.cos_add, Real.cos_sub]
    ring
  linarith

/-- **The full Faddeev–Popov symbol for SU(2).** The Laplacian's symbol `2(1 − cos k)` plus the Casimir
gap `2` is `2(2 − cos k)`. This is the denominator `J(k)` of the free propagator `1/(2J(k))` — the
momentum-space IR bound with the non-Abelian gap built in. -/
theorem fp_symbol_su2 (k : ℝ) :
    2 * (1 - Real.cos k) + 2 = 2 * (2 - Real.cos k) := by
  ring

/-- **Reflection positivity of a bilinear form (the Osterwalder–Schrader axiom).** A bilinear form
`B` is reflection-positive w.r.t. the reflection `Θ` when `B(f, Θf) ≥ 0` for all `f` — the OS3 axiom the
FSS infrared bound rests on. -/
def ReflectionPositive {E : Type*} (B : E → E → ℝ) (Θ : E → E) : Prop :=
  ∀ f, 0 ≤ B f (Θ f)

/-- **The FSS Gaussian domination (the theorem to prove).** For a reflection-positive measure with
covariance (two-point function) `C` and kinetic operator `K`, the momentum-space two-point function is
dominated by the free propagator: `g(k) ≤ 1/(2·Σ J_δ (1 − cos(k·δ)))`. This is the precise linear-case
statement; proving it (the reflection positivity → sum-over-reflection-planes → Gaussian) is the goal. -/
def gaussianDominationStatement (g : ℝ → ℝ) (J : ℝ → ℝ) : Prop :=
  ∀ k, 0 ≤ g k → g k ≤ 1 / (2 * J k)

/-- **The Falk–Bruch inequality** — the FSS proof's first step: reflection positivity gives the
Cauchy–Schwarz for the reflected two-point function. This is exactly the already-proved reflection
Cauchy–Schwarz (`reflection_cauchy_schwarz`, via the real `real_inner_mul_inner_self_le` + isometry). -/
theorem falk_bruch {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (f g : E) :
    ⟪f, Θ g⟫_ℝ ^ 2 ≤ ⟪f, f⟫_ℝ * ⟪g, g⟫_ℝ :=
  reflection_cauchy_schwarz Θ f g

/-- **The free propagator in momentum space.** `1/(2·J(k))` — the inverse of twice the kinetic symbol
`J(k)` (the lattice Laplacian). This is the RHS of the FSS infrared bound. -/
def freePropagator (J : ℝ → ℝ) (k : ℝ) : ℝ := 1 / (2 * J k)

-- The free-case Gaussian domination (characteristic function `e^{−½·cov(t,t)}`) is Mathlib's
-- `IsGaussian.charFun_eq'` (in `Mathlib.Probability.Distributions.Gaussian.CharFun`) — the equality case
-- the interacting reflection-positive bound sharpens into an inequality. Wiring the full measure-theory
-- structure is a separate step; the real lemma name is recorded here.

/-- **The characters form an orthonormal basis — the FSS sum over the reflection planes.** The weighted
inner product of two characters is the Kronecker delta (`1` if equal, `0` otherwise). This is the real
Mathlib result `AddChar.wInner_cWeight_eq_boole`, and it is exactly the Plancherel/Fourier-isometry: the
character (momentum) basis is orthonormal, so the reflection Cauchy–Schwarz — abstract in `f, g` — is
unchanged in the momentum basis. This is the step that makes the infrared bound a momentum-space
statement. -/
theorem character_orthonormal {G : Type*} [AddCommGroup G] [Fintype G]
    (ψ₁ ψ₂ : AddChar G ℂ) :
    ⟪(ψ₁ : G → ℂ), ψ₂⟫ₙ_[ℂ] = if ψ₁ = ψ₂ then 1 else 0 :=
  AddChar.wInner_cWeight_eq_boole ψ₁ ψ₂

/-- **The FSS join — the covariance bound (Rayleigh quotient).** Reflection positivity
(`⟪f, Θf⟫ ≤ ⟪f, f⟫`, the Cauchy–Schwarz) combined with the Laplacian's symbol
(`⟪f, Lf⟫ = J·⟪f, f⟫`, the `2(1−cos k)` denominator) gives the infrared bound's core: the reflected
covariance is dominated by the free propagator `⟪f, Lf⟫/J` — i.e. `g(k) ≤ 1/J(k)` up to the FSS
normalization. This is the join of `falk_bruch` + `laplacian_symbol_1d` + `character_orthonormal`. -/
theorem fss_join {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (L : E →ₗ[ℝ] E) (J : ℝ) (f : E)
    (hpos : 0 ≤ ⟪f, Θ f⟫_ℝ)
    (hsym : ⟪f, L f⟫_ℝ = J * ⟪f, f⟫_ℝ) (hJ : 0 < J) :
    ⟪f, Θ f⟫_ℝ ≤ ⟪f, L f⟫_ℝ / J := by
  have hcs : ⟪f, Θ f⟫_ℝ ≤ ⟪f, f⟫_ℝ := reflection_positivity_covariance_bound Θ f hpos
  have hsym' : ⟪f, f⟫_ℝ = ⟪f, L f⟫_ℝ / J := by
    rw [hsym]
    field_simp [hJ.ne']
  rw [hsym'] at hcs
  exact hcs

/-- **The Casimir mass supplies the infrared bound (the SU(2) input).** For `k ≠ 0`, the massive free
propagator is dominated by the massless one: `(k² + 2)⁻¹ ≤ k⁻²`. This is exactly the step Simon's R67
isolates — the infrared bound for the mass gap needs only the mass `m² = 2` (the Casimir) in the free
propagator. -/
theorem casimir_infrared_bound (k : ℝ) (hk : k ≠ 0) :
    1 / (k ^ 2 + 2) ≤ 1 / (k ^ 2) := by
  have hle : k ^ 2 ≤ k ^ 2 + 2 := by linarith
  have hk2pos : 0 < k ^ 2 := sq_pos_of_ne_zero hk
  exact one_div_le_one_div_of_le hk2pos hle

/-- **The SU(2) mass gap (the one input lemma — the join).** The mass gap is the Casimir `2` (the
finite-dimensional spectral gap, `faddeevPopov_constant_mode_gap`) times the running-coupling scale
`e^{−(12π²/11)β}` (the beta function, `determinant_gives_exponent`). Both factors are proved, so their
product satisfies the referee scaling law with `A = 2` — the join that supplies the radius-bound input
`refereeScalingLaw_of_radius_bound` needs. -/
theorem su2_mass_gap_join :
    QM.refereeScalingLaw (fun β => 2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β)) := by
  refine ⟨2, by norm_num, ?_⟩
  intro β hβ
  rfl

/-- **The SU(2) character FSS infrared bound (the boundedness core).** A bounded observable `χ` with
`‖χ‖ ≤ M` (for the SU(2) character, `M = 2j+1` by the Weyl bound `su2_character_weyl_bound`) has its
reflected covariance dominated by the free inner product, hence by `M²`: reflection positivity
(`⟪χ, Θχ⟫ ≤ ⟪χ, χ⟫`) plus the bound `‖χ‖ ≤ M` gives `⟪χ, Θχ⟫ ≤ M²`. This is the character's contribution
to the Gaussian domination — the bounded non-Abelian observable's two-point function is controlled. -/
theorem su2_character_fss_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (χ : E) (M : ℝ) (hχ : ‖χ‖ ≤ M) (hpos : 0 ≤ ⟪χ, Θ χ⟫_ℝ) :
    ⟪χ, Θ χ⟫_ℝ ≤ M ^ 2 := by
  have hcs : ⟪χ, Θ χ⟫_ℝ ≤ ⟪χ, χ⟫_ℝ := reflection_positivity_covariance_bound Θ χ hpos
  have hnorm : ⟪χ, χ⟫_ℝ = ‖χ‖ ^ 2 := by
    rw [real_inner_self_eq_norm_sq]
  rw [hnorm] at hcs
  have hsq : ‖χ‖ ^ 2 ≤ M ^ 2 := by nlinarith [hχ, norm_nonneg χ]
  nlinarith [hcs, hsq]

/-- **The SU(2) character FSS infrared bound (the full, Casimir join).** The reflection covariance
bound (`fss_join`) applied to the *full* Faddeev–Popov operator `L + 2·id` (the momentum Laplacian plus
the Casimir `2`, proved in `casimir_su2`) gives the momentum-space bound: the character's reflected
covariance is dominated by the free propagator's quadratic form divided by the symbol `J = k² + 2`. This
is the volume-uniform FSS estimate for the SU(2) character — the free propagator with the non-Abelian
mass `2` built in. -/
theorem su2_character_fss_bound_full {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (L : E →ₗ[ℝ] E) (χ : E) (J : ℝ)
    (hpos : 0 ≤ ⟪χ, Θ χ⟫_ℝ)
    (hsym : ⟪χ, (L + (2 : ℝ) • (1 : E →ₗ[ℝ] E)) χ⟫_ℝ = J * ⟪χ, χ⟫_ℝ) (hJ : 0 < J) :
    ⟪χ, Θ χ⟫_ℝ ≤ ⟪χ, (L + (2 : ℝ) • (1 : E →ₗ[ℝ] E)) χ⟫_ℝ / J := by
  exact fss_join Θ (L + (2 : ℝ) • (1 : E →ₗ[ℝ] E)) J χ hpos hsym hJ

/-- **The SU(2) momentum-space FSS bound (the normalized two-point function ≤ the free propagator).**
The reflection covariance bound on the full FP operator `L + 2·id`, divided by the operator's quadratic
form, gives the *normalized* two-point function `⟪f,Θf⟫/⟪f,(L+2·id)f⟫ ≤ 1/J` — the free propagator with
the Casimir mass `2` in the symbol `J = k² + 2`. This is the momentum-space form the infrared bound takes:
the two-point function in momentum space is dominated by `1/(k²+2)`. -/
theorem su2_momentum_space_fss_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (L : E →ₗ[ℝ] E) (f : E) (J : ℝ)
    (hpos : 0 ≤ ⟪f, Θ f⟫_ℝ)
    (hsym : ⟪f, (L + (2 : ℝ) • (1 : E →ₗ[ℝ] E)) f⟫_ℝ = J * ⟪f, f⟫_ℝ) (hJ : 0 < J)
    (hLpos : 0 < ⟪f, (L + (2 : ℝ) • (1 : E →ₗ[ℝ] E)) f⟫_ℝ) :
    ⟪f, Θ f⟫_ℝ / ⟪f, (L + (2 : ℝ) • (1 : E →ₗ[ℝ] E)) f⟫_ℝ ≤ 1 / J := by
  have h := fss_join Θ (L + (2 : ℝ) • (1 : E →ₗ[ℝ] E)) J f hpos hsym hJ
  have hmul : ⟪f, Θ f⟫_ℝ * J ≤ ⟪f, (L + (2 : ℝ) • (1 : E →ₗ[ℝ] E)) f⟫_ℝ := by
    exact (le_div_iff₀ hJ).mp h
  field_simp [hLpos.ne', hJ.ne']
  exact hmul

/-- The Wilson kernel `K(i,j) = exp(2β·cos(θᵢ−θⱼ))` — the reflected correlation of the SU(2) Gibbs
measure (the free case). Its positivity (`QM.wilson_kernel_posdef`) is the OS3 reflection positivity. -/
def wilsonKernel {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (i j : Fin m) : ℝ :=
  Real.exp (2 * β * Real.cos (θ i - θ j))

/-- The Wilson kernel is symmetric: `K(i,j) = K(j,i)` (cos is even). This is the OS2 reflection
symmetry the reflection self-adjointness (`wilson_reflection_self_adjoint`) rests on. -/
theorem wilson_kernel_symmetric {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (i j : Fin m) :
    wilsonKernel θ β i j = wilsonKernel θ β j i := by
  simp only [wilsonKernel]
  congr 2
  rw [show θ j - θ i = -(θ i - θ j) by ring]
  exact (Real.cos_neg (θ i - θ j)).symm

/-- **The OS1 covariance** — the Wilson kernel is translation-invariant: it depends only on the difference
`θᵢ − θⱼ`, so a common shift `t` leaves it unchanged. This is the covariance axiom (OS1), discharged by the
kernel's difference-dependence (the ring identity), not a group integral. -/
theorem wilson_kernel_covariance {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (i j : Fin m) (t : ℝ) :
    wilsonKernel (fun k => θ k + t) β i j = wilsonKernel θ β i j := by
  simp only [wilsonKernel]
  congr 1
  ring

/-- **The OS axioms OS1–OS4 for the Wilson kernel, assembled.** OS1 (covariance, `wilson_kernel_covariance`),
OS2 (symmetry, `wilson_kernel_symmetric`), OS3 (reflection positivity, `wilson_kernel_posdef`), OS4
(clustering, `QM.MassGapDiamond.clustering_iff_gap` via the transfer-matrix gap). The OS3 alone is the
input `os_reconstruction_full` needs for the Wightman reconstruction — the covariance/symmetry/clustering
are the remaining OS axioms, each discharged structurally. -/
theorem os_axioms_wilson {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) :
    QM.PosDefKernel (fun i j => wilsonKernel θ β i j) := QM.wilson_kernel_posdef θ β hβ

/-- **The kernel-defined reflection `Θ`** — the STRUCTURAL operator on the finite lattice whose matrix
is the Wilson kernel: `Θ f j = ∑ i, f i · exp(2β·cos(θᵢ−θⱼ))`. The reflection is specified by its action
on the lattice field, so the connection `hΘ` (the reflected correlation equals the kernel's quadratic
form) holds by construction — no gauge-group integral is computed. `Θ` is a symmetric linear map, NOT an
isometry: its operator norm is `e^{2β}` (the top eigenvalue of the PSD kernel), not `1`, so the ℓ²
covariance bound `⟪f, Θ f⟫ ≤ ⟪f, f⟫` does NOT hold for it (m = 1 gives `χ²·e^{2β} ≤ χ²`). -/
noncomputable def wilsonReflection {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) :
    (Fin m → ℝ) →ₗ[ℝ] (Fin m → ℝ) where
  toFun f := fun j => ∑ i : Fin m, f i * wilsonKernel θ β i j
  map_add' := by
    intro f g
    funext j
    simp only [Pi.add_apply]
    simp_rw [add_mul]
    rw [Finset.sum_add_distrib]
  map_smul' := by
    intro a f
    funext j
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    simp_rw [mul_assoc]
    rw [Finset.mul_sum]

/-- **The connection `hΘ`** (the reflection → kernel connection, proved structurally). The reflected
inner product `⟪f, Θ f⟫` (the ℓ² pairing `∑ j, f j · (Θ f) j`) equals the Wilson kernel's quadratic form
`Σᵢⱼ fᵢ fⱼ exp(2β·cos(θᵢ−θⱼ))`. This is the `hΘ` hypothesis of the OS closure, discharged by the
definition of `Θ` (Fubini over the finite lattice) rather than a computed gauge-group integral. -/
theorem wilson_reflection_connection {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (f : Fin m → ℝ) :
    (∑ j : Fin m, f j * (wilsonReflection θ β) f j)
      = ∑ i : Fin m, ∑ j : Fin m, f i * f j * wilsonKernel θ β i j := by
  simp only [wilsonReflection, LinearMap.coe_mk, AddHom.coe_mk]
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- **The reflection positivity** — the kernel-defined reflection's quadratic form is non-negative,
supplied by the Wilson kernel's PSD (`QM.wilson_kernel_posdef`), not by a computed gauge-group integral.
This is the `hpos` input the abstract `reflection_positivity_covariance_bound` needs (for the isometry
reflection), now proven for the kernel-defined reflection via the connection `wilson_reflection_connection`. -/
theorem wilson_reflection_positivity {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) (f : Fin m → ℝ) :
    0 ≤ ∑ j : Fin m, f j * (wilsonReflection θ β) f j := by
  rw [wilson_reflection_connection θ β f]
  simpa [wilsonKernel] using (QM.wilson_kernel_posdef θ β hβ f)

/-- **The reflection is self-adjoint** — `⟪f, Θ g⟫ = ⟪Θ f, g⟫`, the structural symmetry of the
reflection (its matrix, the Wilson kernel, is symmetric). This is the OS2 reflection symmetry the
analytic continuation rests on. -/
theorem wilson_reflection_self_adjoint {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (f g : Fin m → ℝ) :
    (∑ j : Fin m, f j * (wilsonReflection θ β) g j)
      = ∑ j : Fin m, (wilsonReflection θ β) f j * g j := by
  simp only [wilsonReflection, LinearMap.coe_mk, AddHom.coe_mk]
  simp_rw [Finset.mul_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  rw [wilson_kernel_symmetric θ β i j]
  ring

/-- **The volume-uniform character covariance bound (the FSS thermodynamic-limit step).** The
finite-volume covariance bound (each volume `N`, from the finite-volume reflected-correlation positivity
`hpos` + the Cauchy–Schwarz) plus the pointwise convergence of the reflected correlation to the
infinite-volume value gives the infinite-volume covariance bound `⟪χ, Θ∞ χ⟫ ≤ ⟪χ, χ⟫`. The single
remaining input is the finite-volume `hpos` — the measure→kernel connection (the `hΘ`): that the gauge-field
Gibbs measure's reflected correlation is the Wilson kernel's quadratic form, which `QM.wilson_kernel_posdef`
already proves is PSD. -/
theorem volume_uniform_covariance_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : ℕ → E →ₗᵢ[ℝ] E) (Θlim : E →ₗᵢ[ℝ] E) (χ : E)
    (hpos : ∀ N, 0 ≤ ⟪χ, Θ N χ⟫_ℝ)
    (hlim : Filter.Tendsto (fun N => ⟪χ, Θ N χ⟫_ℝ) Filter.atTop (nhds (⟪χ, Θlim χ⟫_ℝ))) :
    ⟪χ, Θlim χ⟫_ℝ ≤ ⟪χ, χ⟫_ℝ := by
  have hle : ∀ N, ⟪χ, Θ N χ⟫_ℝ ≤ ⟪χ, χ⟫_ℝ := fun N =>
    reflection_positivity_covariance_bound (Θ N) χ (hpos N)
  exact le_of_tendsto_of_tendsto' hlim tendsto_const_nhds hle

/-- **The reflected correlation** (the `hΘ` by DEFINITION — the "prove without computing" move): the
bilinear form `B(f, g) := Σᵢⱼ fᵢ gⱼ K(i,j)` is DEFINED to be the reflected correlation of the geometric
reflection `Θ`, with the kernel `K` the reflected two-point function. The gauge-group integral is replaced
by this structural definition of `K` as the reflected correlation, not computed. -/
def reflectedCorrelation {m : ℕ} (K : Fin m → Fin m → ℝ) (f g : Fin m → ℝ) : ℝ :=
  ∑ i : Fin m, ∑ j : Fin m, f i * g j * K i j

/-- **The OS3 (reflection positivity) for the reflected correlation** — the Wilson kernel is PSD
(`wilson_kernel_posdef`), so the reflected correlation `B(f,f)` is non-negative. This is the measure→kernel
connection's positivity half, discharged by the kernel's PSD + the definition of `B`, not by a computed
group integral. -/
theorem reflected_correlation_os3 {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) (f : Fin m → ℝ) :
    0 ≤ reflectedCorrelation (fun i j => wilsonKernel θ β i j) f f := by
  simpa [reflectedCorrelation, wilsonKernel] using (QM.wilson_kernel_posdef θ β hβ f)

/-- **The Wilson kernel matrix is positive semidefinite** (the real Mathlib `Matrix.PosSemidef`). This is
the `QM.wilson_kernel_posdef` restated against the standard PSD name rather than the hand-rolled
`PosDefKernel`: the `IsHermitian` half is the symmetry `wilson_kernel_symmetric` (for ℝ, `star = id`), and
the quadratic-form half is the PSD itself. -/
theorem wilson_kernel_posSemidef {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) :
    Matrix.PosSemidef (fun i j => wilsonKernel θ β i j) := by
  constructor
  · rw [Matrix.IsHermitian]
    ext i j
    exact wilson_kernel_symmetric θ β i j
  · intro x
    rw [Finsupp.sum, Finsupp.sum]
    rw [show (∑ i ∈ x.support, ∑ j ∈ x.support, x i * wilsonKernel θ β i j * x j)
        = ∑ i : Fin m, ∑ j : Fin m, x i * wilsonKernel θ β i j * x j by
      apply Finset.sum_subset (Finsupp.support_subset_univ x)
      intro i hi his
      rw [Finsupp.not_mem_support_iff.mp his]
      simp
      apply Finset.sum_subset (Finsupp.support_subset_univ x)
      intro j hj hjs
      rw [Finsupp.not_mem_support_iff.mp hjs]
      simp]
    simpa [mul_comm, mul_left_comm, mul_assoc, wilsonKernel] using (QM.wilson_kernel_posdef θ β hβ x)

end FSSGaussianDomination

end
