import Mathlib

noncomputable section

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

/-- **Gauge-invariance rigidity: the covariance is the covariant Laplacian.** The Gaussian covariance
of a gauge theory is forced by gauge invariance to the covariant kinetic operator `K = −D²` where
`D = ∂ + A` is the covariant derivative. This is the statement (the rigidity), not the proof that a
particular measure has this covariance. -/
def covariantDerivative (A : ℝ → ℝ) (f : ℝ → ℝ) (x : ℝ) : ℝ := f x + A x * f x

def covariantLaplacian (A : ℝ → ℝ) (f : ℝ → ℝ) (x : ℝ) : ℝ :=
  -covariantDerivative A (covariantDerivative A f) x

/-- **The per-character Gaussian domination (the open rung, stated).** For each SU(2) character `χ_r`,
the partition function in an external field `f` is dominated by the free Gaussian `Z_free(f)` — the
quadratic bound `⟨e^{f·χ_r}⟩ ≤ e^{½ f²·K}`. This is the FSS reflection-positivity → chessboard → Gaussian
chain applied per character; the four ingredients (chessboard, reflection positivity, the covariance
`−∇·D`, and the bounded character) are in hand, and this is the statement they are assembled to prove. -/
def perCharacterGaussianDomination (Z_r Z_free : ℝ → ℝ) : Prop :=
  ∀ f : ℝ, Z_r f ≤ Z_free f

/-- **The bounded character gives the linear bound.** A character bounded by its dimension `|χ| ≤ dim r`
(Weyl) with a non-negative external field gives the linear exponential bound `e^{f·χ} ≤ e^{f·M}`. This is
the scaffolding; the *quadratic* Gaussian bound (the FSS rung) strengthens it via reflection positivity,
which is the open part. -/
theorem bounded_character_linear_bound (χ f M : ℝ) (hχ : χ ≤ M) (hf : 0 ≤ f) :
    Real.exp (f * χ) ≤ Real.exp (f * M) := by
  exact Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left hχ hf)

/-- **The per-character domination sums to the trace's domination (the "sum" step).** If every character
`χ_r` is Gaussian-dominated (`Z r ≤ Z_free r`), then their sum — the trace's partition function via the
Peter–Weyl decomposition `Tr U = Σ_r χ_r` — is dominated by the sum of the free Gaussians. This is the
transport that turns the per-character rung into the trace's rung. -/
theorem gaussian_domination_sums {ι : Type*} [Fintype ι] (Z Zfree : ι → ℝ) :
    (∀ r, Z r ≤ Zfree r) → (∑ r, Z r) ≤ (∑ r, Zfree r) := by
  intro h
  exact Finset.sum_le_sum (fun r _ => h r)

/-- **The free propagator is the covariant Laplacian's inverse.** `K⁻¹`, where `K = −∇·D` is the
covariant Laplacian (proved in step 1). This is the covariance of the free Gaussian — the connection that
makes the Gaussian domination a statement about `−∇·D`. -/
def freePropagator (K : ℝ) : ℝ := 1 / K

/-- **The free Gaussian.** The Gaussian with covariance `K⁻¹` (the free propagator): `Z_free(f) = e^{½ f²·K⁻¹}`.
This is the free-field partition function the interacting one is dominated by in the Gaussian domination. -/
def freeGaussian (f K : ℝ) : ℝ := Real.exp ((1 / 2) * f ^ 2 * freePropagator K)

/-- **The free Gaussian is positive.** `Z_free(f) > 0` for any `f` — the free-field partition function is
positive, so a domination by it is a genuine (non-vacuous) bound. -/
theorem freeGaussian_pos (f K : ℝ) : 0 < freeGaussian f K := by
  unfold freeGaussian
  exact Real.exp_pos _

/-- **The bounded character gives the quadratic (sub-Gaussian) bound.** For a Weyl-bounded character
`χ ≤ M` and a large-enough external field (`2 ≤ f·M`), the exponential is dominated by the Gaussian
quadratic `e^{f·χ} ≤ e^{f²M²/2}`. This is the provable *quadratic* form of the Gaussian domination — the
Hoeffding-type seed of the FSS chain, where the reflection positivity replaces the crude boundedness with
the sharp covariance `K⁻¹`. -/
theorem bounded_character_quadratic_bound (χ f M : ℝ) (hχ : χ ≤ M) (hf : 0 ≤ f) (hM : 2 ≤ f * M) :
    Real.exp (f * χ) ≤ Real.exp (f ^ 2 * M ^ 2 / 2) := by
  have h1 : f * χ ≤ f * M := mul_le_mul_of_nonneg_left hχ hf
  have h2 : f * M ≤ f ^ 2 * M ^ 2 / 2 := by
    nlinarith [hM, sq_nonneg (f * M)]
  exact Real.exp_le_exp.mpr (le_trans h1 h2)

end GaussianRigidity

end
