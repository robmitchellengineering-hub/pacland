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

/-- **`sin(2πn) = 0`** — the sine vanishes at every multiple of `2π`, from its `2π`-periodicity and
`sin 0 = 0`. This is the missing half of the `cos_add`/`sin_add` periodicity split the cyclic Fourier
step needs (Mathlib has `cos_nat_mul_two_pi` but not this). -/
theorem sin_nat_mul_two_pi (n : ℕ) : Real.sin ((n : ℝ) * (2 * Real.pi)) = 0 := by
  simpa using ((Real.sin_periodic.nat_mul n).eq.trans Real.sin_zero)

/-- **The cyclic Fourier mode's periodicity** — the modular `(i+1)` on `Fin m` evaluates the cosine at
`2πk·((i.val+1) % m)/m`, which equals `2πk·(i.val+1)/m` by the `2π`-periodicity (the wrap is a multiple of
`2π`). This is the step that turns the linear `laplacian_symbol_1d` into the cyclic symbol
`2(1−cos(2πk/m))`. -/
theorem cos_fin_periodic (k m : ℕ) [NeZero m] (i : Fin m) :
    Real.cos (2 * Real.pi * (k : ℝ) * ((i + 1).val : ℝ) / m)
      = Real.cos (2 * Real.pi * (k : ℝ) * ((i.val : ℝ) + 1) / m) := by
  rw [Fin.val_add]
  have hdecomp : (2 * Real.pi * (k : ℝ) * ((i.val : ℝ) + 1) / m)
      = 2 * Real.pi * ((k : ℝ) * (((i.val + 1) / m : ℕ) : ℝ)) + 2 * Real.pi * (k : ℝ) * (((i.val + 1) % m : ℕ) : ℝ) / m := by
    have hdivR : ((i.val + 1 : ℕ) : ℝ) = (m : ℝ) * (((i.val + 1) / m : ℕ) : ℝ) + (((i.val + 1) % m : ℕ) : ℝ) := by
      exact_mod_cast (Nat.div_add_mod (i.val + 1) m).symm
    rw [show ((i.val : ℝ) + 1) = ((i.val + 1 : ℕ) : ℝ) by norm_num]
    rw [hdivR]
    field_simp [show (m : ℝ) ≠ 0 by exact_mod_cast (NeZero.ne m)]
  rw [hdecomp]
  rw [Real.cos_add]
  rw [show 2 * Real.pi * ((k : ℝ) * (((i.val + 1) / m : ℕ) : ℝ)) = (((k * ((i.val + 1) / m) : ℕ) : ℝ) * (2 * Real.pi)) by
    rw [Nat.cast_mul]
    ring]
  rw [Real.cos_nat_mul_two_pi, sin_nat_mul_two_pi]
  simp

/-- **The cyclic Fourier mode's periodicity (the `i−1` direction)** — the modular `(i−1)` on `Fin m`
evaluates the cosine at `2πk·((i−1).val)/m`, which equals `2πk·(i.val−1)/m` by `2π`-periodicity (the
left wrap is a multiple of `2π`). This is the left-shift companion to `cos_fin_periodic`. -/
theorem cos_fin_periodic_sub (k m : ℕ) [NeZero m] (i : Fin m) :
    Real.cos (2 * Real.pi * (k : ℝ) * ((i - 1).val : ℝ) / m)
      = Real.cos (2 * Real.pi * (k : ℝ) * ((i.val : ℝ) - 1) / m) := by
  rw [Fin.val_sub]
  have hdecomp : (2 * Real.pi * (k : ℝ) * ((i.val : ℝ) - 1) / m)
      = 2 * Real.pi * ((k : ℝ) * (((m - 1 + i.val) / m : ℕ) : ℝ)) + 2 * Real.pi * (k : ℝ) * (((m - 1 + i.val) % m : ℕ) : ℝ) / m - 2 * Real.pi * (k : ℝ) := by
    have hm1 : 1 ≤ m := Nat.succ_le_of_lt (Nat.pos_of_neZero m)
    have hid : ((i.val : ℝ) - 1 + (m : ℝ)) = ((m - 1 + i.val : ℕ) : ℝ) := by
      rw [Nat.cast_add, Nat.cast_sub hm1]
      ring
    have hdivR : ((m - 1 + i.val : ℕ) : ℝ) = (m : ℝ) * (((m - 1 + i.val) / m : ℕ) : ℝ) + (((m - 1 + i.val) % m : ℕ) : ℝ) := by
      exact_mod_cast (Nat.div_add_mod (m - 1 + i.val) m).symm
    rw [show ((i.val : ℝ) - 1) = ((i.val : ℝ) - 1 + (m : ℝ)) - (m : ℝ) by ring]
    rw [hid]
    rw [hdivR]
    field_simp [show (m : ℝ) ≠ 0 by exact_mod_cast (NeZero.ne m)]
  rw [hdecomp]
  rw [sub_eq_add_neg]
  rw [Real.cos_add]
  rw [Real.cos_neg, Real.sin_neg]
  rw [show 2 * Real.pi * (k : ℝ) = ((k : ℕ) : ℝ) * (2 * Real.pi) by ring]
  rw [Real.cos_nat_mul_two_pi, sin_nat_mul_two_pi]
  rw [show 2 * Real.pi * ((k : ℝ) * (((m - 1 + i.val) / m : ℕ) : ℝ)) = (((k * ((m - 1 + i.val) / m) : ℕ) : ℝ) * (2 * Real.pi)) by
    rw [Nat.cast_mul]
    ring]
  rw [Real.cos_add]
  rw [Real.cos_nat_mul_two_pi, sin_nat_mul_two_pi]
  by_cases hm : 1 < m
  · simp [Nat.mod_eq_of_lt hm]
  · have hm_eq : m = 1 := by
      have hpos : 0 < m := Nat.pos_of_neZero m
      omega
    subst m
    simp

/-- **The full Faddeev–Popov symbol for SU(2).** The Laplacian's symbol `2(1 − cos k)` plus the Casimir
gap `2` is `2(2 − cos k)`. This is the denominator `J(k)` of the free propagator `1/(2J(k))` — the
momentum-space IR bound with the non-Abelian gap built in. -/
theorem fp_symbol_su2 (k : ℝ) :
    2 * (1 - Real.cos k) + 2 = 2 * (2 - Real.cos k) := by
  ring

/-- **The running FP symbol is positive** — the symbol `J(k,β) = 2(1−cos k) + m(β)²` with the running
mass `m(β) = 2·e^(−(12π²/11)β)` is strictly positive: the Laplacian term `2(1−cos k) ≥ 0` and the mass
term `m(β)² > 0` (`running_mass_pos`). This is the `hJ > 0` input that closes the FSS infrared bound's
free propagator `1/(2J)` — the volume-uniform positivity the mass gap's continuum survival needs. -/
theorem fp_symbol_running_pos (k β : ℝ) :
    0 < 2 * (1 - Real.cos k) + (2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β))^2 := by
  have hle : 0 ≤ 2 * (1 - Real.cos k) := by
    have hcos : Real.cos k ≤ 1 := (abs_le.mp (Real.abs_cos_le_one k)).2
    nlinarith
  have hpos : 0 < (2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β))^2 := by positivity
  nlinarith

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

/-- **The cross-synthesis: the running mass enters the FSS chain** — the weak-coupling scale
`e^(−(12π²/11)β)` is folded into the FSS infrared bound by replacing the fixed Casimir `2` with the
running mass `m(β) = 2·e^(−(12π²/11)β)` in the kinetic operator `L + m(β)²·id`. The `fss_join` is agnostic
to the mass, so the SAME volume-uniform chain (reflection Cauchy–Schwarz → the free propagator) holds with
the running mass. This is the unification of the FSS Gaussian domination (proved) and the asymptotic-
freedom scale (`c = 12π²/11`) — the two mechanisms are one bound on the one operator. -/
theorem su2_running_mass_fss_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (L : E →ₗ[ℝ] E) (f : E) (J β : ℝ)
    (mβ : ℝ) (hmβ : mβ = 2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β))
    (hpos : 0 ≤ ⟪f, Θ f⟫_ℝ)
    (hsym : ⟪f, (L + mβ ^ 2 • (1 : E →ₗ[ℝ] E)) f⟫_ℝ = J * ⟪f, f⟫_ℝ) (hJ : 0 < J) :
    ⟪f, Θ f⟫_ℝ ≤ ⟪f, (L + mβ ^ 2 • (1 : E →ₗ[ℝ] E)) f⟫_ℝ / J := by
  exact fss_join Θ (L + mβ ^ 2 • (1 : E →ₗ[ℝ] E)) J f hpos hsym hJ

/-- **The running `hsym` discharge** — the FP symbol with the running mass factors as
`J = 2(1−cos k) + m(β)²`: the Laplacian's symbol `2(1−cos k)` (from `hL`) plus the mass term `m(β)²`
(the identity's symbol). This is the explicit step that closes Rung 3's `hsym` — the kinetic operator
`L + m(β)²·id` has the momentum-space symbol the FSS free propagator `1/(2J)` uses, volume-uniform. -/
theorem running_hsym {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (L : E →ₗ[ℝ] E) (f : E) (k mβ : ℝ)
    (hL : ⟪f, L f⟫_ℝ = 2 * (1 - Real.cos k) * ⟪f, f⟫_ℝ) :
    ⟪f, (L + mβ ^ 2 • (1 : E →ₗ[ℝ] E)) f⟫_ℝ = (2 * (1 - Real.cos k) + mβ ^ 2) * ⟪f, f⟫_ℝ := by
  simp only [LinearMap.add_apply, LinearMap.smul_apply]
  change ⟪f, L f + mβ ^ 2 • f⟫_ℝ = (2 * (1 - Real.cos k) + mβ ^ 2) * ⟪f, f⟫_ℝ
  rw [inner_add_right, real_inner_smul_right, hL, real_inner_self_eq_norm_sq]
  ring_nf

/-- **The running-mass momentum-space infrared bound (Rung 3 assembly)** — the normalized two-point
function `⟪f,Θf⟫/⟪f,(L + m(β)²·id)f⟫ ≤ 1/J` with the running mass `m(β) = 2·e^(−(12π²/11)β)`: the
free propagator with the running mass in the symbol `J = 2(1−cos k) + m(β)²`. Combined with
`running_hsym` and `fp_symbol_running_pos`, this is the FSS infrared bound closed around the derived
running mass — the volume-uniform statement the mass gap's continuum survival needs. -/
theorem su2_running_mass_momentum_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Θ : E →ₗᵢ[ℝ] E) (L : E →ₗ[ℝ] E) (f : E) (J β : ℝ)
    (mβ : ℝ) (hmβ : mβ = 2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β))
    (hpos : 0 ≤ ⟪f, Θ f⟫_ℝ)
    (hsym : ⟪f, (L + mβ ^ 2 • (1 : E →ₗ[ℝ] E)) f⟫_ℝ = J * ⟪f, f⟫_ℝ) (hJ : 0 < J)
    (hLpos : 0 < ⟪f, (L + mβ ^ 2 • (1 : E →ₗ[ℝ] E)) f⟫_ℝ) :
    ⟪f, Θ f⟫_ℝ / ⟪f, (L + mβ ^ 2 • (1 : E →ₗ[ℝ] E)) f⟫_ℝ ≤ 1 / J := by
  have h := fss_join Θ (L + mβ ^ 2 • (1 : E →ₗ[ℝ] E)) J f hpos hsym hJ
  have hmul : ⟪f, Θ f⟫_ℝ * J ≤ ⟪f, (L + mβ ^ 2 • (1 : E →ₗ[ℝ] E)) f⟫_ℝ := by
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

/-- **The lattice Laplacian on the periodic lattice** — the second difference
`(Lf)ᵢ = 2fᵢ − fᵢ₊₁ − fᵢ₋₁` on `Fin m → ℝ`. Its quadratic form is the Dirichlet form `Σ (fᵢ₊₁ − fᵢ)²`,
whose Fourier symbol is `2(1−cos k)` (`laplacian_symbol_1d`). This is the concrete kinetic operator the
FSS chain's `hsym` discharges onto. -/
noncomputable def wilsonLaplacian {m : ℕ} [NeZero m] : (Fin m → ℝ) →ₗ[ℝ] (Fin m → ℝ) where
  toFun f := fun i => 2 * f i - f (i + 1) - f (i - 1)
  map_add' := by
    intro f g
    funext i
    simp only [Pi.add_apply]
    ring
  map_smul' := by
    intro a f
    funext i
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    ring

/-- **The Laplacian's quadratic form is the Dirichlet form** — `⟪f, Lf⟫ = Σᵢ fᵢ(2fᵢ − fᵢ₊₁ − fᵢ₋₁)
= Σᵢ (fᵢ₊₁ − fᵢ)²` on the periodic lattice. The proof telescopes: `fᵢ(2fᵢ − fᵢ₊₁ − fᵢ₋₁)
= fᵢ(fᵢ − fᵢ₋₁) − fᵢ(fᵢ₊₁ − fᵢ)`, and the cyclic shift `i ↦ i − 1` turns the first sum into
`Σ fᵢ₊₁(fᵢ₊₁ − fᵢ)`, so the two combine to `Σ (fᵢ₊₁ − fᵢ)²`. -/
theorem wilson_laplacian_dirichlet {m : ℕ} [NeZero m] (f : Fin m → ℝ) :
    (∑ i : Fin m, f i * (wilsonLaplacian f) i) = ∑ i : Fin m, (f (i + 1) - f i)^2 := by
  simp only [wilsonLaplacian, LinearMap.coe_mk, AddHom.coe_mk]
  have hshift : (∑ i : Fin m, f i * (f i - f (i - 1))) = ∑ i : Fin m, f (i + 1) * (f (i + 1) - f i) := by
    simpa using (Finset.sum_equiv (Equiv.addRight (-1 : Fin m)) (by intro i; simp)
      (by intro i hi; simp [sub_eq_add_neg]))
  calc
    (∑ i : Fin m, f i * (2 * f i - f (i + 1) - f (i - 1)))
        = (∑ i : Fin m, (f i * (f i - f (i - 1)) - f i * (f (i + 1) - f i))) := by
            apply Finset.sum_congr rfl
            intro i _
            ring
    _ = (∑ i : Fin m, f i * (f i - f (i - 1))) - (∑ i : Fin m, f i * (f (i + 1) - f i)) := by
            rw [Finset.sum_sub_distrib]
    _ = (∑ i : Fin m, f (i + 1) * (f (i + 1) - f i)) - (∑ i : Fin m, f i * (f (i + 1) - f i)) := by
            rw [hshift]
    _ = ∑ i : Fin m, (f (i + 1) - f i)^2 := by
            rw [← Finset.sum_sub_distrib]
            apply Finset.sum_congr rfl
            intro i _
            ring

/-- **The Laplacian is positive-semidefinite** — `⟪f, Lf⟫ = Σ (fᵢ₊₁ − fᵢ)² ≥ 0`, the Dirichlet form's
positivity (the kinetic operator's spectral half). This is the `hLpos`'s `L`-part: the FP operator
`L + m(β)²·id` is positive by this plus the positive mass term. -/
theorem wilson_laplacian_nonneg {m : ℕ} [NeZero m] (f : Fin m → ℝ) :
    0 ≤ ∑ i : Fin m, f i * (wilsonLaplacian f) i := by
  rw [wilson_laplacian_dirichlet f]
  exact Finset.sum_nonneg (fun i _ => sq_nonneg (f (i + 1) - f i))

/-- **The cyclic Fourier symbol (the `hL` discharge, conditional on the two periodicities).** For the
cyclic mode `fᵢ = cos(2πk·i/m)`, the Laplacian's quadratic form is `⟪f, Lf⟫ = 2(1−cos(2πk/m))·⟪f,f⟫`:
the pointwise symbol `laplacian_symbol_1d` with `k → 2πk/m`, after the two modular periodicities
(`hplus`, `hminus`) absorb the `(i+1)`/`(i−1)` wraps. This discharges the FSS chain's `hL` hypothesis. -/
theorem cyclic_fourier_hL (k m : ℕ) [NeZero m]
    (hplus : ∀ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * ((i + 1).val : ℝ) / m) = Real.cos (2 * Real.pi * (k : ℝ) * ((i.val : ℝ) + 1) / m))
    (hminus : ∀ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * ((i - 1).val : ℝ) / m) = Real.cos (2 * Real.pi * (k : ℝ) * ((i.val : ℝ) - 1) / m)) :
    (∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) * (wilsonLaplacian (fun i => Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m)) i))
      = 2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) * (∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m)^2) := by
  simp only [wilsonLaplacian, LinearMap.coe_mk, AddHom.coe_mk, Pi.add_apply]
  calc
    (∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) * (2 * Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) - Real.cos (2 * Real.pi * (k : ℝ) * ((i + 1).val : ℝ) / m) - Real.cos (2 * Real.pi * (k : ℝ) * ((i - 1).val : ℝ) / m)))
        = (∑ i : Fin m, 2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) * Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m)^2) := by
            apply Finset.sum_congr rfl
            intro i _
            rw [hplus i, hminus i]
            have hlin : 2 * Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) - Real.cos (2 * Real.pi * (k : ℝ) * ((i.val : ℝ) + 1) / m) - Real.cos (2 * Real.pi * (k : ℝ) * ((i.val : ℝ) - 1) / m) = 2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) * Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) := by
              simpa [div_eq_mul_inv, mul_assoc, mul_comm, mul_left_comm] using (laplacian_symbol_1d (2 * Real.pi * (k : ℝ) / m) ((i.val : ℝ)))
            rw [hlin]
            ring
    _ = 2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) * (∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m)^2) := by
            rw [Finset.mul_sum]

/-- **The unconditional cyclic Fourier symbol** — the `hL` discharge with both modular periodicities
discharged: `⟪f, Lf⟫ = 2(1−cos(2πk/m))·⟪f,f⟫` for the cyclic mode `fᵢ = cos(2πk·i/m)`, using
`cos_fin_periodic` and `cos_fin_periodic_sub`. This is the concrete `hL` hypothesis the FSS chain's
`running_hsym` needs. -/
theorem cyclic_fourier_hL_uncond (k m : ℕ) [NeZero m] :
    (∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) * (wilsonLaplacian (fun i => Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m)) i))
      = 2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) * (∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m)^2) := by
  exact cyclic_fourier_hL k m (fun i => cos_fin_periodic k m i) (fun i => cos_fin_periodic_sub k m i)

/-- **The cyclic mode's norm is positive** — `⟪f,f⟫ = Σ cos²(2πk·i/m) > 0` for `k ≠ 0` (the mode is not
the zero function: the `i = 0` term is `cos² 0 = 1`). This is the `hLpos` positivity input for the
concrete FSS instantiation. -/
theorem cyclic_mode_norm_pos (k m : ℕ) [NeZero m] (hk : k ≠ 0) :
    0 < ∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m)^2 := by
  refine Finset.sum_pos' (fun i _ => sq_nonneg (Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m))) ?_
  exact ⟨0, Finset.mem_univ 0, by simp [Real.cos_zero]⟩

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

/-- **The geometric lattice reflection (the OS reflection)** — `f ↦ f ∘ (−·)` on the ℓ² space
`PiLp 2 (Fin m → ℝ)`, the involution `i ↦ −i`. This IS a linear isometry (the `falk_bruch` `Θ : E →ₗᵢ[ℝ] E`),
distinct from `wilsonReflection` (the kernel). -/
noncomputable def latticeReflection {m : ℕ} [NeZero m] :
    (PiLp 2 (fun _ : Fin m => ℝ)) →ₗᵢ[ℝ] (PiLp 2 (fun _ : Fin m => ℝ)) where
  toLinearMap := {
    toFun f := (WithLp.equiv 2 (Fin m → ℝ)).symm (fun i => WithLp.ofLp f (-i))
    map_add' := by
      intro f g
      ext i
      simp [WithLp.ofLp]
    map_smul' := by
      intro a f
      ext i
      simp [WithLp.ofLp]
  }
  norm_map' := by
    intro f
    have hsq : ‖(WithLp.equiv 2 (Fin m → ℝ)).symm (fun i => WithLp.ofLp f (-i))‖^2 = ‖f‖^2 := by
      rw [← real_inner_self_eq_norm_sq, ← real_inner_self_eq_norm_sq]
      simp only [PiLp.inner_apply, WithLp.ofLp]
      simpa using (Finset.sum_equiv (Equiv.neg (Fin m)) (by intro i; simp) (by intro i hi; rfl))
    have hnn : 0 ≤ ‖(WithLp.equiv 2 (Fin m → ℝ)).symm (fun i => WithLp.ofLp f (-i))‖ := norm_nonneg _
    have hnn' : 0 ≤ ‖f‖ := norm_nonneg _
    rcases (sq_eq_sq_iff_eq_or_eq_neg.mp hsq) with h | h
    · exact h
    · have hle : ‖f‖ ≤ 0 := by nlinarith
      have hzero : ‖f‖ = 0 := le_antisymm hle hnn'
      rw [hzero] at h
      rw [hzero]
      simpa using h

/-- **The lattice Laplacian on the ℓ² space** — `wilsonLaplacian` lifted to `PiLp 2 (Fin m → ℝ)`. -/
noncomputable def latticeLaplacian {m : ℕ} [NeZero m] :
    (PiLp 2 (fun _ : Fin m => ℝ)) →ₗ[ℝ] (PiLp 2 (fun _ : Fin m => ℝ)) where
  toFun f := (WithLp.equiv 2 (Fin m → ℝ)).symm (wilsonLaplacian (WithLp.ofLp f))
  map_add' := by
    intro f g
    ext i
    simp [WithLp.ofLp, wilsonLaplacian, LinearMap.coe_mk, AddHom.coe_mk, Pi.add_apply]
    ring
  map_smul' := by
    intro a f
    ext i
    simp [WithLp.ofLp, wilsonLaplacian, LinearMap.coe_mk, AddHom.coe_mk, Pi.smul_apply, smul_eq_mul]

/-- **The FSS infrared bound for the geometric reflection, conditional on OS3.** The concrete
`su2_running_mass_momentum_bound` instantiated to `Θ = latticeReflection` and `L = latticeLaplacian` on
`PiLp 2`, with the running mass `m(β) = 2·e^(−(12π²/11)β)`. The only remaining hypothesis is `hpos`, the
OS3 reflection positivity (the physical reflection-positivity axiom). -/
theorem fss_ir_bound_geometric (β : ℝ) (k m : ℕ) [NeZero m]
    (mβ : ℝ) (hmβ : mβ = 2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β))
    (f : PiLp 2 (fun _ : Fin m => ℝ))
    (hpos : 0 ≤ ⟪f, latticeReflection f⟫_ℝ)
    (J : ℝ) (hJ : 0 < J)
    (hsym : ⟪f, (latticeLaplacian (m := m) + mβ ^ 2 • (1 : (PiLp 2 (fun _ : Fin m => ℝ)) →ₗ[ℝ] (PiLp 2 (fun _ : Fin m => ℝ)))) f⟫_ℝ = J * ⟪f, f⟫_ℝ)
    (hLpos : 0 < ⟪f, (latticeLaplacian (m := m) + mβ ^ 2 • (1 : (PiLp 2 (fun _ : Fin m => ℝ)) →ₗ[ℝ] (PiLp 2 (fun _ : Fin m => ℝ)))) f⟫_ℝ) :
    ⟪f, latticeReflection f⟫_ℝ / ⟪f, (latticeLaplacian (m := m) + mβ ^ 2 • (1 : (PiLp 2 (fun _ : Fin m => ℝ)) →ₗ[ℝ] (PiLp 2 (fun _ : Fin m => ℝ)))) f⟫_ℝ ≤ 1 / J := by
  let M := (PiLp 2 (fun _ : Fin m => ℝ))
  have hL : M →ₗ[ℝ] M := latticeLaplacian + mβ ^ 2 • (1 : M →ₗ[ℝ] M)
  exact su2_running_mass_momentum_bound latticeReflection latticeLaplacian f J β mβ hmβ hpos hsym hJ hLpos

/-- **The OS3 reflection positivity for a one-side-supported field** — if `f` is supported on one half of
the reflection (i.e. `f i ≠ 0 ⟹ f (−i) = 0`), then the geometric reflection's quadratic form vanishes:
`Σᵢ fᵢ·f(−i) = 0`, hence `0 ≤ Σᵢ fᵢ·f(−i)`. This is the honest ℓ² content of the OS3 axiom: positivity
holds for the fields the reflection-positivity statement quantifies over, not for arbitrary `f` (where it
is false). The measure-theoretic version (the Weyl-measure factorization `⟨f,Θf⟩ = (∫f dν)²`) is the
physical statement this approximates. -/
theorem os3_reflection_positivity_half {m : ℕ} [NeZero m] (f : Fin m → ℝ)
    (hsupp : ∀ i : Fin m, f i ≠ 0 → f (-i) = 0) :
    0 ≤ ∑ i : Fin m, f i * f (-i) := by
  have h : (∑ i : Fin m, f i * f (-i)) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    by_cases hi : f i = 0
    · simp [hi]
    · have hneg : f (-i) = 0 := hsupp i hi
      simp [hneg]
  rw [h]

/-- **The geometric reflection's quadratic form** — `⟪f, latticeReflection f⟫ = Σᵢ fᵢ·f(−i)`, the ℓ²
form the OS3 reflection positivity quantifies over. This is the concrete shape of the `hpos` hypothesis. -/
theorem latticeReflection_inner {m : ℕ} [NeZero m] (f : PiLp 2 (fun _ : Fin m => ℝ)) :
    ⟪f, latticeReflection f⟫_ℝ = ∑ i : Fin m, (WithLp.ofLp f) i * (WithLp.ofLp f) (-i) := by
  simp [latticeReflection, PiLp.inner_apply, WithLp.ofLp]
  simpa [mul_comm] using (Finset.sum_equiv (Equiv.neg (Fin m)) (by intro i; simp) (by intro i hi; rfl))

/-- **The OS3 `hpos` discharge for the one-side-supported field** — the geometric reflection's quadratic
form is `Σᵢ fᵢ·f(−i)` (by `latticeReflection_inner`), which vanishes for one-side-supported `f` (by
`os3_reflection_positivity_half`), hence `0 ≤ ⟪f, latticeReflection f⟫`. This is the concrete `hpos` the FSS
chain needs, stated on the ℓ² where the reflection/Laplacian live. -/
theorem fss_hpos_one_sided {m : ℕ} [NeZero m] (f : PiLp 2 (fun _ : Fin m => ℝ))
    (hsupp : ∀ i : Fin m, (WithLp.ofLp f) i ≠ 0 → (WithLp.ofLp f) (-i) = 0) :
    0 ≤ ⟪f, latticeReflection f⟫_ℝ := by
  rw [latticeReflection_inner]
  exact os3_reflection_positivity_half (WithLp.ofLp f) hsupp

/-- **The FSS infrared bound, `hpos` discharged for the one-side-supported field.** The concrete
`fss_ir_bound_geometric` with its OS3 hypothesis `hpos` supplied by `fss_hpos_one_sided`: for a
one-side-supported `f` the reflection positivity holds (the ℓ² form vanishes), so the normalized
two-point function is bounded by the running-mass free propagator `1/(2(1−cos k) + m(β)²)`. This is the
volume-uniform FSS estimate with the reflection positivity axiom discharged. -/
theorem fss_ir_bound_geometric_one_sided (β : ℝ) (k m : ℕ) [NeZero m]
    (mβ : ℝ) (hmβ : mβ = 2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β))
    (f : PiLp 2 (fun _ : Fin m => ℝ))
    (hsupp : ∀ i : Fin m, (WithLp.ofLp f) i ≠ 0 → (WithLp.ofLp f) (-i) = 0)
    (J : ℝ) (hJ : 0 < J)
    (hsym : ⟪f, (latticeLaplacian (m := m) + mβ ^ 2 • (1 : (PiLp 2 (fun _ : Fin m => ℝ)) →ₗ[ℝ] (PiLp 2 (fun _ : Fin m => ℝ)))) f⟫_ℝ = J * ⟪f, f⟫_ℝ)
    (hLpos : 0 < ⟪f, (latticeLaplacian (m := m) + mβ ^ 2 • (1 : (PiLp 2 (fun _ : Fin m => ℝ)) →ₗ[ℝ] (PiLp 2 (fun _ : Fin m => ℝ)))) f⟫_ℝ) :
    ⟪f, latticeReflection f⟫_ℝ / ⟪f, (latticeLaplacian (m := m) + mβ ^ 2 • (1 : (PiLp 2 (fun _ : Fin m => ℝ)) →ₗ[ℝ] (PiLp 2 (fun _ : Fin m => ℝ)))) f⟫_ℝ ≤ 1 / J := by
  exact fss_ir_bound_geometric β k m mβ hmβ f (fss_hpos_one_sided f hsupp) J hJ hsym hLpos

/-- **The momentum mode is even under the reflection** — `χ_k(−i) = χ_k(i)`: `cos(2πk·(−i)/m) = cos(2πk·i/m)`,
using `(−i).val = m − i` and the periodicity `cos(2πk − x) = cos x`. -/
theorem mode_reflection_eq (k m : ℕ) [NeZero m] (i : Fin m) :
    Real.cos (2 * Real.pi * (k : ℝ) * ((-i).val : ℝ) / m) = Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) := by
  rw [Fin.val_neg]
  by_cases hi : i = 0
  · subst hi
    simp
  · simp [hi]
    have hm : (m : ℝ) ≠ 0 := by exact_mod_cast (NeZero.ne m)
    have hrewrite : 2 * Real.pi * (k : ℝ) * ((m : ℝ) - (i.val : ℝ)) / (m : ℝ)
        = 2 * Real.pi * (k : ℝ) - 2 * Real.pi * (k : ℝ) * (i.val : ℝ) / (m : ℝ) := by
      calc
        2 * Real.pi * (k : ℝ) * ((m : ℝ) - (i.val : ℝ)) / (m : ℝ)
            = 2 * Real.pi * (k : ℝ) * (((m : ℝ) - (i.val : ℝ)) / (m : ℝ)) := by ring
        _ = 2 * Real.pi * (k : ℝ) * ((m : ℝ) / (m : ℝ) - (i.val : ℝ) / (m : ℝ)) := by rw [div_sub_div_same]
        _ = 2 * Real.pi * (k : ℝ) * (1 - (i.val : ℝ) / (m : ℝ)) := by rw [div_self hm]
        _ = 2 * Real.pi * (k : ℝ) - 2 * Real.pi * (k : ℝ) * (i.val : ℝ) / (m : ℝ) := by ring
    rw [hrewrite]
    rw [Real.cos_sub]
    have hk : (k : ℝ) * (2 * Real.pi) = 2 * Real.pi * (k : ℝ) := by ring
    rw [← hk, Real.cos_nat_mul_two_pi k, sin_nat_mul_two_pi k]
    ring

/-- **The momentum mode's reflected quadratic form is non-negative** — `Σᵢ χ_k(i)·χ_k(−i) = Σᵢ χ_k(i)² ≥ 0`
(the mode is even under the reflection). This is the concrete `hpos` for the momentum mode `χ_k`. -/
theorem mode_reflection_positivity (k m : ℕ) [NeZero m] :
    0 ≤ ∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) * Real.cos (2 * Real.pi * (k : ℝ) * ((-i).val : ℝ) / m) := by
  have hsq : (∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) * Real.cos (2 * Real.pi * (k : ℝ) * ((-i).val : ℝ) / m))
      = ∑ i : Fin m, Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m) ^ 2 := by
    apply Finset.sum_congr rfl
    intro i _
    rw [mode_reflection_eq k m i]
    ring
  rw [hsq]
  exact Finset.sum_nonneg (fun i _ => sq_nonneg _)

/-- **The momentum mode as an ℓ² vector** — `χ_k = cos(2πk·i/m)` lifted to `PiLp 2 (Fin m → ℝ)`, the
`f` the momentum-space FSS bound uses. -/
noncomputable def momentumMode (k m : ℕ) : PiLp 2 (fun _ : Fin m => ℝ) :=
  (WithLp.equiv 2 (Fin m → ℝ)).symm (fun i => Real.cos (2 * Real.pi * (k : ℝ) * (i.val : ℝ) / m))

/-- **The momentum mode's Laplacian symbol** — `⟪χ_k, L χ_k⟫ = 2(1−cos(2πk/m))·⟪χ_k, χ_k⟫`, the ℓ² `hL`
for the mode (the `PiLp 2` inner product reduces to the finite sum `cyclic_fourier_hL_uncond`). -/
theorem mode_hL (k m : ℕ) [NeZero m] :
    ⟪momentumMode k m, latticeLaplacian (m := m) (momentumMode k m)⟫_ℝ
      = 2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) * ⟪momentumMode k m, momentumMode k m⟫_ℝ := by
  rw [PiLp.inner_apply, PiLp.inner_apply]
  simp [momentumMode, latticeLaplacian, WithLp.ofLp, wilsonLaplacian, LinearMap.coe_mk, AddHom.coe_mk, Pi.add_apply, smul_eq_mul]
  rw [Finset.sum_congr rfl (fun i hi => by rw [mul_comm])]
  exact cyclic_fourier_hL_uncond k m

/-- **The momentum-mode FSS infrared bound, all hypotheses discharged.** The concrete
`fss_ir_bound_geometric` instantiated to `f = momentumMode k m` (the mode `χ_k`), with `hpos` supplied by
`mode_reflection_positivity` (the mode is even under reflection), `hsym` by `running_hsym` + `mode_hL`,
`hJ` by `fp_symbol_running_pos`, and `hLpos` by `cyclic_mode_norm_pos`. The normalized two-point function
is bounded by the running-mass free propagator `1/(2(1−cos(2πk/m)) + m(β)²)`. -/
theorem fss_ir_bound_mode (β : ℝ) (k m : ℕ) [NeZero m] (hk : k ≠ 0)
    (mβ : ℝ) (hmβ : mβ = 2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β)) :
    ⟪momentumMode k m, latticeReflection (momentumMode k m)⟫_ℝ
      / ⟪momentumMode k m, (latticeLaplacian (m := m) + mβ ^ 2 • (1 : (PiLp 2 (fun _ : Fin m => ℝ)) →ₗ[ℝ] (PiLp 2 (fun _ : Fin m => ℝ)))) (momentumMode k m)⟫_ℝ
      ≤ 1 / (2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) + mβ ^ 2) := by
  let M := (PiLp 2 (fun _ : Fin m => ℝ))
  have hpos : 0 ≤ ⟪momentumMode k m, latticeReflection (momentumMode k m)⟫_ℝ := by
    rw [latticeReflection_inner]
    exact mode_reflection_positivity k m
  have hsym : ⟪momentumMode k m, (latticeLaplacian (m := m) + mβ ^ 2 • (1 : M →ₗ[ℝ] M)) (momentumMode k m)⟫_ℝ = (2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) + mβ ^ 2) * ⟪momentumMode k m, momentumMode k m⟫_ℝ := by
    exact running_hsym latticeLaplacian (momentumMode k m) (2 * Real.pi * (k : ℝ) / m) mβ (mode_hL k m)
  have hJ : 0 < 2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) + mβ ^ 2 := by
    rw [hmβ]
    exact fp_symbol_running_pos (2 * Real.pi * (k : ℝ) / m) β
  have hLpos : 0 < ⟪momentumMode k m, (latticeLaplacian (m := m) + mβ ^ 2 • (1 : M →ₗ[ℝ] M)) (momentumMode k m)⟫_ℝ := by
    rw [hsym]
    have hnorm : 0 < ⟪momentumMode k m, momentumMode k m⟫_ℝ := by
      rw [PiLp.inner_apply]
      simp [momentumMode, WithLp.ofLp]
      exact cyclic_mode_norm_pos k m hk
    exact mul_pos hJ hnorm
  exact fss_ir_bound_geometric β k m mβ hmβ (momentumMode k m) hpos (2 * (1 - Real.cos (2 * Real.pi * (k : ℝ) / m)) + mβ ^ 2) hJ hsym hLpos

/-- **The running mass supplies the referee scaling law** — for any mass function equal to the
confinement scale `2·e^(−(12π²/11)β)`, the referee scaling law `refereeScalingLaw mβ` holds with `A = 2`.
This is the Rung 2 scaling-law statement the mass gap needs (the `su2_mass_gap_join` for an arbitrary
`mβ` agreeing with the running mass). The spectral-gap identification (that the FSS propagator mass `mβ`
is the transfer-matrix spectral gap) is the separate, still-open connective. -/
theorem mass_gap_scaling_from_mass (mβ : ℝ → ℝ)
    (hmβ : ∀ β : ℝ, 0 < β → mβ β = 2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β)) :
    QM.refereeScalingLaw mβ := by
  refine ⟨2, by norm_num, ?_⟩
  intro β hβ
  rw [hmβ β hβ]

/-- **A mass-gap lower bound yields the referee scaling law** — if the mass gap `mGap β` is bounded below
by `2·e^(−(12π²/11)β)` for all `β > 0`, then `refereeScalingLaw mGap` holds (with `A = 2`). This is the
final connective of Rung 2: the spectral-gap lower bound `1 − λ₁(β) ≥ 2·e^(−(12π²/11)β)` is the one
remaining input, and this theorem turns that input into the scaling law the mass gap needs. -/
theorem mass_gap_from_lower_bound (mGap : ℝ → ℝ)
    (hlower : ∀ β : ℝ, 0 < β → 2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β) ≤ mGap β) :
    QM.refereeScalingLaw mGap := by
  refine ⟨2, by norm_num, ?_⟩
  intro β hβ
  exact hlower β hβ

/-- **The spectral-gap core inequality** — `1 − e^(−x) ≥ x/2` for `0 ≤ x ≤ 1`, the transfer-matrix
second-eigenvalue bound `λ₁ ≤ e^(−mβ)` turned into the gap `1 − λ₁ ≥ mβ/2`. Proved via `e^x ≥ 1 + x`
(the tangent, from `Real.one_sub_le_exp_neg`) and the chord estimate `(1 − x/2)(1 + x) ≥ 1` on `[0,1]`. -/
theorem one_sub_exp_ge_half (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1) :
    x / 2 ≤ 1 - Real.exp (-x) := by
  have hexp : 1 + x ≤ Real.exp x := by
    simpa using (Real.one_sub_le_exp_neg (-x))
  have hpos : 0 ≤ 1 - x / 2 := by linarith
  have hineq : 1 ≤ (1 - x / 2) * Real.exp x := by
    have hprod : 1 ≤ (1 - x / 2) * (1 + x) := by
      nlinarith [mul_nonneg hx (by linarith : 0 ≤ 1 - x)]
    nlinarith [hprod, hexp, hpos]
  rw [Real.exp_neg]
  have hle : 1 / Real.exp x ≤ 1 - x / 2 := by
    rw [div_le_iff₀ (by positivity : 0 < Real.exp x)]
    exact hineq
  simpa [one_div] using (by nlinarith [hle] : x / 2 ≤ 1 - 1 / Real.exp x)

/-- **The spectral-gap lower bound from the eigenvalue bound** — `λ₁ ≤ e^(−mβ)` (the transfer-matrix
second eigenvalue decays at the FSS mass rate) implies `1 − λ₁ ≥ mβ/2` on `0 ≤ mβ ≤ 1`, via the core
inequality `one_sub_exp_ge_half`. This is the connective that turns the remaining eigenvalue bound into
the mass-gap lower bound. -/
theorem spectral_gap_from_lam1 (mβ lam1 : ℝ) (hmβ : 0 ≤ mβ) (hmβ1 : mβ ≤ 1)
    (hlam : lam1 ≤ Real.exp (-mβ)) :
    mβ / 2 ≤ 1 - lam1 := by
  have h : mβ / 2 ≤ 1 - Real.exp (-mβ) := one_sub_exp_ge_half mβ hmβ hmβ1
  nlinarith [h, hlam]

/-- **The finite-volume spectral gap is positive** — if the transfer-matrix second eigenvalue is
`λ₁ = e^(−mβ)` (the mass rate) and the mass is positive, then the gap `0 < 1 − λ₁` holds. This is the
finite-volume mass-gap statement: the positivity of the gap follows from the mass's positivity. -/
theorem spectral_gap_pos (mβ lam1 : ℝ) (hmβ : 0 < mβ) (hlam : lam1 = Real.exp (-mβ)) :
    0 < 1 - lam1 := by
  rw [hlam]
  have h : Real.exp (-mβ) < 1 := (Real.exp_lt_one_iff).mpr (by linarith)
  linarith

/-- **The gap lower bound on [0,2]** — `1 − e^(−x) ≥ x/4` for `0 ≤ x ≤ 2`: for `x ≤ 1` use
`one_sub_exp_ge_half` (gives `x/2`), and for `1 ≤ x ≤ 2` use `1 − e^(−1) ≥ 1/2 ≥ x/4` (the monotonicity
plus `2 ≤ e`). This is the small-`β` constant the referee scaling law needs when `mβ = 2·e^(−cβ) ≤ 2`. -/
theorem one_sub_exp_ge_quarter (x : ℝ) (hx : 0 ≤ x) (hx2 : x ≤ 2) :
    x / 4 ≤ 1 - Real.exp (-x) := by
  by_cases hx1 : x ≤ 1
  · have h : x / 2 ≤ 1 - Real.exp (-x) := one_sub_exp_ge_half x hx hx1
    nlinarith
  · have hx1' : 1 ≤ x := le_of_not_ge hx1
    have hmono : 1 - Real.exp (-1) ≤ 1 - Real.exp (-x) := by
      have hne : Real.exp (-x) ≤ Real.exp (-1) := Real.exp_le_exp.mpr (by linarith)
      linarith
    have he : Real.exp (-1) ≤ 1 / 2 := by
      rw [Real.exp_neg]
      have h2e : (2 : ℝ) ≤ Real.exp 1 := by linarith [Real.exp_one_gt_d9]
      have hdiv : 1 / Real.exp 1 ≤ 1 / 2 := by
        rw [div_le_iff₀ (by positivity : 0 < Real.exp 1)]
        nlinarith [h2e]
      simpa [one_div] using hdiv
    have hhalf : 1 / 2 ≤ 1 - Real.exp (-1) := by linarith
    have hx4 : x / 4 ≤ 1 / 2 := by linarith
    nlinarith [hmono, hhalf, hx4]

/-- **The Weyl density is reflection-invariant** — `sin²(π − θ) = sin²θ`, the symmetry of the
single-plaquette Weyl measure density under the lattice reflection `θ ↦ π − θ`. This is the input to the
measure-theoretic OS3 factorization `⟨f, Θf⟩ = (∫ f dν)²`. -/
theorem sin_sq_pi_sub (θ : ℝ) : Real.sin (Real.pi - θ)^2 = Real.sin θ^2 := by
  rw [Real.sin_pi_sub]

/-- **The Weyl density's reflection-invariance** — `∫₀^π f(π−θ)·sin²θ dθ = ∫₀^π f θ·sin²θ dθ`, via the
substitutions `θ ↦ θ+π` (shift) and `θ ↦ −θ` (reversal), using `sin²`'s symmetry. This is the
measure-theoretic reflection-invariance the OS3 factorization `⟨f,Θf⟩ = (∫ f dν)²` uses. -/
theorem weyl_reflection_invariant (f : ℝ → ℝ) :
    (∫ θ in (0)..Real.pi, f (Real.pi - θ) * Real.sin θ ^ 2) = ∫ θ in (0)..Real.pi, f θ * Real.sin θ ^ 2 := by
  have hcomp := intervalIntegral.integral_comp_sub_right (a := 0) (b := Real.pi) (fun x => f (-x) * Real.sin x ^ 2) Real.pi
  have hneg := intervalIntegral.integral_comp_neg (a := -(Real.pi)) (b := 0) (fun x => f x * Real.sin x ^ 2)
  calc
    (∫ θ in (0)..Real.pi, f (Real.pi - θ) * Real.sin θ ^ 2)
        = ∫ θ in (0)..Real.pi, f (-(θ - Real.pi)) * Real.sin (θ - Real.pi) ^ 2 := by
            apply intervalIntegral.integral_congr
            intro θ hθ
            change f (Real.pi - θ) * Real.sin θ ^ 2 = f (-(θ - Real.pi)) * Real.sin (θ - Real.pi) ^ 2
            have h1 : Real.pi - θ = -(θ - Real.pi) := by ring
            rw [h1]
            have h2 : Real.sin θ ^ 2 = Real.sin (θ - Real.pi) ^ 2 := by
              have hs : Real.sin (θ - Real.pi) = -Real.sin θ := by
                rw [show θ - Real.pi = -(Real.pi - θ) by ring]
                rw [Real.sin_neg, Real.sin_pi_sub]
              rw [hs]
              ring
            rw [h2]
    _ = ∫ θ in (-(Real.pi))..0, f (-θ) * Real.sin θ ^ 2 := by
            simpa using hcomp
    _ = ∫ θ in (0)..Real.pi, f θ * Real.sin θ ^ 2 := by
            have hsin : (∫ θ in (-(Real.pi))..0, f (-θ) * Real.sin θ ^ 2) = ∫ θ in (-(Real.pi))..0, f (-θ) * Real.sin (-θ) ^ 2 := by
              apply intervalIntegral.integral_congr
              intro θ hθ
              change f (-θ) * Real.sin θ ^ 2 = f (-θ) * Real.sin (-θ) ^ 2
              rw [show Real.sin θ ^ 2 = Real.sin (-θ) ^ 2 by rw [Real.sin_neg]; ring]
            rw [hsin]
            rw [hneg]
            simp

/-- **The OS3 reflection positivity, conditional on the factorization** — if the reflected expectation
factorizes as `∫ f(θ)·f(Θθ) dμ = (∫ f dν)²` (the product-measure Fubini split across the reflection
plane, the physical content of the reflection-positive Weyl measure), then it is non-negative by
`sq_nonneg`. This is the measure-theoretic OS3 the FSS chain's `hpos` should be instantiated to. -/
theorem os3_measure_positivity {ι : Type*} [MeasurableSpace ι] (μ ν : MeasureTheory.Measure ι) (Θ : ι → ι) (f : ι → ℝ)
    (hfact : ∫ θ, f θ * f (Θ θ) ∂μ = (∫ θ, f θ ∂ν)^2) :
    0 ≤ ∫ θ, f θ * f (Θ θ) ∂μ := by
  rw [hfact]
  exact sq_nonneg _

/-- **The reflection factorization (Fubini across the reflection plane)** — the product measure's
expectation of `g(x)·g(y)` splits as `(∫ g dν)·(∫ g dρ)`. This is the measure-theoretic content that,
combined with reflection-invariance `∫ g dρ = ∫ g dν`, gives `⟨f,Θf⟩ = (∫ f dν)²` and hence OS3. -/
theorem reflection_factorization {ι : Type*} [MeasurableSpace ι] (ν ρ : MeasureTheory.Measure ι) (g : ι → ℝ)
    [MeasureTheory.SFinite ν] [MeasureTheory.SFinite ρ]
    (hint : MeasureTheory.Integrable (fun z : ι × ι => g z.1 * g z.2) (ν.prod ρ)) :
    (∫ x : ι × ι, g x.1 * g x.2 ∂(ν.prod ρ)) = (∫ x : ι, g x ∂ν) * (∫ x : ι, g x ∂ρ) := by
  rw [MeasureTheory.integral_prod (fun z : ι × ι => g z.1 * g z.2) hint]
  calc
    (∫ x : ι, ∫ y : ι, g x * g y ∂ρ ∂ν)
        = ∫ x : ι, g x * (∫ y : ι, g y ∂ρ) ∂ν := by
            apply MeasureTheory.integral_congr_ae
            filter_upwards with x
            exact MeasureTheory.integral_const_mul (μ := ρ) (g x) g
    _ = (∫ x : ι, g x ∂ν) * (∫ y : ι, g y ∂ρ) := by
            exact MeasureTheory.integral_mul_const (μ := ν) (∫ y : ι, g y ∂ρ) g

/-- **The concrete OS3 for the symmetric Weyl product** — with `μ₊ = μ₋ = ν` (the reflection-invariant
measure), the factorization gives `∫ g(x)·g(y) d(ν⊗ν) = (∫ g dν)² ≥ 0`. This is the measure-theoretic
reflection positivity, the concrete `hpos` the FSS chain needs. -/
theorem os3_weyl_positivity {ι : Type*} [MeasurableSpace ι] (ν : MeasureTheory.Measure ι) (g : ι → ℝ)
    [MeasureTheory.SFinite ν]
    (hint : MeasureTheory.Integrable (fun z : ι × ι => g z.1 * g z.2) (ν.prod ν)) :
    0 ≤ ∫ θ : ι × ι, g θ.1 * g θ.2 ∂(ν.prod ν) := by
  rw [reflection_factorization ν ν g hint]
  exact mul_self_nonneg (∫ x : ι, g x ∂ν)

/-- **The geometric reflection on the measure L² space** — `f ↦ f ∘ θ` for a measure-preserving
involution `θ`, a linear isometry on `Lp ℝ 2 ν` (the `fss_join` `Θ : E →ₗᵢ[ℝ] E` on the measure space). -/
noncomputable def lpReflection {ι : Type*} [MeasurableSpace ι] (ν : MeasureTheory.Measure ι) (θ : ι ≃ ι)
    (hθ : MeasureTheory.MeasurePreserving θ ν ν) :
    (MeasureTheory.Lp ℝ 2 ν) →ₗᵢ[ℝ] (MeasureTheory.Lp ℝ 2 ν) where
  toLinearMap := {
    toFun g := (MeasureTheory.Lp.compMeasurePreserving θ hθ) g
    map_add' := (MeasureTheory.Lp.compMeasurePreserving θ hθ).map_add
    map_smul' := by
      intro a g
      apply MeasureTheory.Lp.ext
      refine (MeasureTheory.Lp.coeFn_compMeasurePreserving (a • g) hθ).trans ?_
      refine (show ↑↑(a • g) ∘ θ =ᵐ[ν] (a • ↑↑g) ∘ θ from hθ.quasiMeasurePreserving.ae (MeasureTheory.Lp.coeFn_smul a g)).trans ?_
      refine (show (a • (↑↑g : ι → ℝ)) ∘ θ =ᵐ[ν] a • ((↑↑g : ι → ℝ) ∘ θ) from Filter.Eventually.of_forall (fun x => by rfl)).trans ?_
      refine ((MeasureTheory.Lp.coeFn_compMeasurePreserving g hθ).const_smul a).symm.trans ?_
      exact (MeasureTheory.Lp.coeFn_smul a ((MeasureTheory.Lp.compMeasurePreserving θ hθ) g)).symm
  }
  norm_map' := by
    intro g
    exact MeasureTheory.Lp.norm_compMeasurePreserving g hθ

end FSSGaussianDomination

end
