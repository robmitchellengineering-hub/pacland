import Mathlib
import PaclandProof.QM.Bessel
import PaclandProof.QM.FullLattice

noncomputable section

/-!
# The Bessel recurrence — algebraic heart (first sub-step of `bessel_ratio_mono`)

The modified Bessel functions satisfy `I₀(x) − I₂(x) = (2/x)·I₁(x)`. Its algebraic core is the
factorial identity `1/(k!)² − 1/((k−1)!(k+1)!) = 1/(k!(k+1)!)`, which makes the two series cancel
term-by-term. This file proves the identity and its term-wise corollary — the sub-steps that feed
the derivative `I₁′ = I₀ − I₁/x`, which feeds the monotonicity of `I₁/I₀` (the 1-link SU(2)
spectral gap in the coupling).
-/

namespace QM

/-- The factorial identity at the heart of the Bessel recurrence: for `k ≥ 1`,
`1/(k!)² − 1/((k−1)!(k+1)!) = 1/(k!(k+1)!)`. -/
lemma bessel_factorial_identity (k : ℕ) (hk : 1 ≤ k) :
    1 / ((k.factorial : ℝ)^2) - 1 / (((k - 1).factorial : ℝ) * (k + 1).factorial)
      = 1 / ((k.factorial : ℝ) * (k + 1).factorial) := by
  have h1 : ((k + 1).factorial : ℝ) = (k + 1 : ℝ) * (k.factorial : ℝ) := by
    rw [Nat.factorial_succ]
    norm_num
  have h2 : (k.factorial : ℝ) = (k : ℝ) * ((k - 1).factorial : ℝ) := by
    have hk' : k = (k - 1) + 1 := by omega
    rw [hk', Nat.factorial_succ]
    norm_num
  have hk0 : (k : ℝ) ≠ 0 := by
    exact_mod_cast (ne_of_gt (lt_of_lt_of_le zero_lt_one hk))
  have hk10 : (k + 1 : ℝ) ≠ 0 := by positivity
  rw [h1, h2]
  field_simp [hk0, hk10]
  ring

/-- The term-wise identity that telescopes the Bessel recurrence: for `k ≥ 1` and `x ≠ 0`,
`(x/2)^{2k}/(k!)² − (x/2)^{2k}/((k−1)!(k+1)!) = (2/x)·(x/2)^{2k+1}/(k!(k+1)!)`. -/
lemma bessel_term_identity (k : ℕ) (hk : 1 ≤ k) (x : ℝ) (hx : x ≠ 0) :
    (x / 2)^(2 * k) / ((k.factorial : ℝ)^2) - (x / 2)^(2 * k) / (((k - 1).factorial : ℝ) * (k + 1).factorial)
      = (2 / x) * ((x / 2)^(2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial)) := by
  have hfac := bessel_factorial_identity k hk
  have hscal : (2 / x) * (x / 2)^(2 * k + 1) = (x / 2)^(2 * k) := by
    rw [pow_succ]
    field_simp [hx]
  calc
    (x / 2)^(2 * k) / ((k.factorial : ℝ)^2) - (x / 2)^(2 * k) / (((k - 1).factorial : ℝ) * (k + 1).factorial)
        = (x / 2)^(2 * k) * (1 / ((k.factorial : ℝ)^2) - 1 / (((k - 1).factorial : ℝ) * (k + 1).factorial)) := by ring
    _ = (x / 2)^(2 * k) * (1 / ((k.factorial : ℝ) * (k + 1).factorial)) := by rw [hfac]
    _ = (2 / x) * ((x / 2)^(2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial)) := by
      rw [← hscal]
      ring

/-- **The telescoping sum** of the Bessel recurrence: the partial sums telescope term-by-term,
`Σ_{k<N} (A_{k+1} − B_k) = (2/x)·Σ_{k<N} C_{k+1}`, where each term is `bessel_term_identity`. This is
the sum-level identity that the finite recurrence `S₀ − S₂ = (2/x)·S₁ − E_N` assembles from. -/
lemma bessel_telescope_sum (N : ℕ) (x : ℝ) (hx : x ≠ 0) :
    Finset.sum (Finset.range N) (fun k =>
        (x / 2) ^ (2 * (k + 1)) / (((k + 1).factorial : ℝ)^2)
          - (x / 2) ^ (2 * k + 2) / ((k.factorial : ℝ) * (k + 2).factorial))
      = (2 / x) * Finset.sum (Finset.range N) (fun k =>
        (x / 2) ^ (2 * (k + 1) + 1) / (((k + 1).factorial : ℝ) * ((k + 1) + 1).factorial)) := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl ?_
    intro k _
    exact bessel_term_identity (k + 1) (by omega) x hx

/-- The partial sum of the modified Bessel series: `S_n(N, x) = Σ_{k=0}^N (x/2)^{2k+n}/(k!(k+n)!)`. -/
def besselPartial (n N : ℕ) (x : ℝ) : ℝ :=
  ∑ k ∈ Finset.range (N + 1), (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)

/-- **The finite Bessel recurrence**: `S₀(N) − S₂(N) = (2/x)·S₁(N) − (x/2)^{2N+2}/(N!(N+2)!)`.
The error term vanishes as N → ∞, giving `I₀ − I₂ = (2/x)·I₁`. -/
lemma bessel_recurrence_partial (N : ℕ) (x : ℝ) (hx : x ≠ 0) :
    besselPartial 0 N x - besselPartial 2 N x
      = (2 / x) * besselPartial 1 N x - (x / 2)^(2 * N + 2) / ((N.factorial : ℝ) * (N + 2).factorial) := by
  dsimp [besselPartial]
  rw [Finset.sum_range_succ', Finset.sum_range_succ, Finset.sum_range_succ']
  have hsub : Finset.sum (Finset.range N) (fun k => (x / 2) ^ (2 * (k + 1)) / (((k + 1).factorial : ℝ) * ((k + 1).factorial : ℝ)))
        - Finset.sum (Finset.range N) (fun k => (x / 2) ^ (2 * k + 2) / ((k.factorial : ℝ) * (k + 2).factorial))
      = (2 / x) * Finset.sum (Finset.range N) (fun k => (x / 2) ^ (2 * (k + 1) + 1) / (((k + 1).factorial : ℝ) * ((k + 1) + 1).factorial)) := by
    rw [← Finset.sum_sub_distrib]
    simpa only [pow_two] using bessel_telescope_sum N x hx
  have hA0 : (x / 2) ^ (2 * 0) / ((Nat.factorial 0 : ℝ) * (Nat.factorial 0 : ℝ)) = 1 := by norm_num
  have hC0 : (2 / x) * ((x / 2) ^ (2 * 0 + 1) / ((Nat.factorial 0 : ℝ) * (Nat.factorial 1 : ℝ))) = 1 := by
    field_simp [hx]
    ring
  rw [mul_add]
  nlinarith [hsub, hA0, hC0]

/-- The partial sums `besselPartial n N x` converge to the full Bessel function `besselI n x`
(for `x ≥ 0`, where the series is summable). This is the N → ∞ step that turns the finite
recurrence into the full recurrence. -/
lemma besselPartial_tendsto (n : ℕ) {x : ℝ} (hx : 0 ≤ x) :
    Filter.Tendsto (fun N : ℕ => besselPartial n N x) Filter.atTop (nhds (besselI n x)) := by
  dsimp [besselPartial]
  have hsum : Summable (fun k => (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)) :=
    besselI_summable_of_nonneg n hx
  have hhas : HasSum (fun k => (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)) (besselI n x) := by
    simpa [besselI] using (Summable.hasSum hsum)
  exact (HasSum.tendsto_sum_nat hhas).comp (Filter.tendsto_add_atTop_nat 1)

/-- **The full Bessel recurrence**: `I₀(x) − I₂(x) = (2/x)·I₁(x)` for `x > 0`. This is the N → ∞
limit of the finite recurrence `bessel_recurrence_partial`. -/
lemma bessel_recurrence {x : ℝ} (hx : 0 < x) :
    besselI 0 x - besselI 2 x = (2 / x) * besselI 1 x := by
  have hx0 : 0 ≤ x := le_of_lt hx
  have hconv0 : Filter.Tendsto (fun N : ℕ => besselPartial 0 N x) Filter.atTop (nhds (besselI 0 x)) :=
    besselPartial_tendsto 0 hx0
  have hconv2 : Filter.Tendsto (fun N : ℕ => besselPartial 2 N x) Filter.atTop (nhds (besselI 2 x)) :=
    besselPartial_tendsto 2 hx0
  have hconv1 : Filter.Tendsto (fun N : ℕ => besselPartial 1 N x) Filter.atTop (nhds (besselI 1 x)) :=
    besselPartial_tendsto 1 hx0
  have herr : Filter.Tendsto (fun N : ℕ => (x / 2)^(2 * N + 2) / ((N.factorial : ℝ) * (N + 2).factorial)) Filter.atTop (nhds 0) := by
    have hsum : Summable (fun k => (x / 2) ^ (2 * k + 2) / ((k.factorial : ℝ) * (k + 2).factorial)) :=
      besselI_summable_of_nonneg 2 hx0
    exact (Summable.tendsto_cofinite_zero hsum).mono_left Filter.atTop_le_cofinite
  have hlhs : Filter.Tendsto (fun N : ℕ => besselPartial 0 N x - besselPartial 2 N x) Filter.atTop (nhds (besselI 0 x - besselI 2 x)) :=
    hconv0.sub hconv2
  have hrhs : Filter.Tendsto (fun N : ℕ => besselPartial 0 N x - besselPartial 2 N x) Filter.atTop (nhds ((2 / x) * besselI 1 x)) := by
    have hxne : x ≠ 0 := ne_of_gt hx
    have hmul : Filter.Tendsto (fun N : ℕ => (2 / x) * besselPartial 1 N x) Filter.atTop (nhds ((2 / x) * besselI 1 x)) :=
      hconv1.const_mul (2 / x)
    have hsub : Filter.Tendsto (fun N : ℕ => (2 / x) * besselPartial 1 N x - (x / 2)^(2 * N + 2) / ((N.factorial : ℝ) * (N + 2).factorial)) Filter.atTop (nhds ((2 / x) * besselI 1 x - 0)) :=
      hmul.sub herr
    have hsub' : Filter.Tendsto (fun N : ℕ => (2 / x) * besselPartial 1 N x - (x / 2)^(2 * N + 2) / ((N.factorial : ℝ) * (N + 2).factorial)) Filter.atTop (nhds ((2 / x) * besselI 1 x)) := by
      simpa using hsub
    rw [show (fun N : ℕ => besselPartial 0 N x - besselPartial 2 N x)
          = (fun N : ℕ => (2 / x) * besselPartial 1 N x - (x / 2)^(2 * N + 2) / ((N.factorial : ℝ) * (N + 2).factorial)) by
      funext N
      exact bessel_recurrence_partial N x hxne]
    exact hsub'
  exact tendsto_nhds_unique hlhs hrhs

/-- **The modified Bessel functions are decreasing in order** (the ν = 1 case): `I₂(x) < I₀(x)`
for `x > 0`. Direct from the recurrence `I₀ − I₂ = (2/x)·I₁` and the positivity of `I₁`. This is the
non-triviality of the spectral gap: the next-to-leading eigenvalue `I₂` is strictly below the
leading `I₀`. -/
lemma besselI2_lt_besselI0 {x : ℝ} (hx : 0 < x) : besselI 2 x < besselI 0 x := by
  have hrec := bessel_recurrence hx
  have hI1 : 0 < besselI 1 x := besselI_pos hx
  have hpos : 0 < (2 / x) * besselI 1 x := mul_pos (div_pos two_pos hx) hI1
  rw [← hrec] at hpos
  linarith

/-- The derivative of the finite partial sum `besselPartial n N` at `x` — the term-by-term derivative
of the finite polynomial (derivative written with `(1/2)` last to match `HasDerivAt.pow`). This is the
finite step toward the derivative recurrence `I₀′ = I₁`, feeding the small-field activity bound. -/
lemma besselPartial_hasDerivAt (n N : ℕ) (x : ℝ) :
    HasDerivAt (fun y => besselPartial n N y)
      (∑ k ∈ Finset.range (N + 1), (2 * k + n : ℝ) * (x / 2)^(2 * k + n - 1) * (1 / 2) / ((k.factorial : ℝ) * (k + n).factorial)) x := by
  have hterm : ∀ k : ℕ, HasDerivAt (fun y : ℝ => (y / 2)^(2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial))
      ((2 * k + n : ℝ) * (x / 2)^(2 * k + n - 1) * (1 / 2) / ((k.factorial : ℝ) * (k + n).factorial)) x := by
    intro k
    have hlin : HasDerivAt (fun y : ℝ => y / 2) (1 / 2) x := by
      simpa using (hasDerivAt_id x).div_const 2
    have hpow : HasDerivAt (fun y : ℝ => (y / 2) ^ (2 * k + n)) ((2 * k + n : ℝ) * (x / 2) ^ (2 * k + n - 1) * (1 / 2)) x := by
      convert (hasDerivAt_pow (2 * k + n) (x / 2)).comp x hlin using 1
      · funext y
        rfl
      · norm_num
    exact hpow.div_const ((k.factorial : ℝ) * (k + n).factorial)
  induction N with
  | zero =>
      simp [besselPartial]
      simpa using hterm 0
  | succ N ih =>
      convert ih.add (hterm (N + 1)) using 1
      · ext y
        simp [besselPartial, Finset.sum_range_succ]
      · simp [Finset.sum_range_succ]

/-- **The order monotonicity for strong coupling**: `I₁ < I₀` when `β ≤ 2`. From `I₀ = I₂ + (2/β)I₁`
(the recurrence), `I₀ − I₁ = I₂ + (2/β − 1)I₁`, and for `β ≤ 2` the coefficient `2/β − 1 ≥ 0`, so the
difference is `≥ I₂ > 0`. Hence `I₁/I₀ < 1` and `E[z] = 1 − I₁/I₀ > 0` at strong coupling. The
weak-coupling (β > 2) half needs the Bessel asymptotics (the open Clay step). -/
lemma besselI1_lt_besselI0_of_le_two {β : ℝ} (hβ : 0 < β) (hβle : β ≤ 2) :
    besselI 1 β < besselI 0 β := by
  have hrec : besselI 0 β - besselI 2 β = (2 / β) * besselI 1 β := bessel_recurrence hβ
  have hI1 : 0 < besselI 1 β := besselI_pos hβ
  have hI2 : 0 < besselI 2 β := besselI_pos hβ
  have hcoef : 0 ≤ (2 / β) - 1 := by
    have h2β : 1 ≤ 2 / β := (one_le_div hβ).mpr hβle
    linarith
  have hdiff : 0 < besselI 0 β - besselI 1 β := by
    have hI0 : besselI 0 β = besselI 2 β + (2 / β) * besselI 1 β := by linarith
    have h : besselI 0 β - besselI 1 β = besselI 2 β + ((2 / β) - 1) * besselI 1 β := by
      rw [hI0]
      ring
    rw [h]
    have hnonneg : 0 ≤ ((2 / β) - 1) * besselI 1 β := mul_nonneg hcoef (le_of_lt hI1)
    linarith
  linarith

/-- **The SU(2) Weyl integral of the heat kernel**: `∫₀^π e^(x·cos θ)·sin²θ dθ = π·I₁(x)/x` (for `x > 0`).
This is the RG step's core identity — the block-spin average of the SU(2) weight at the trivial connection.
Derivation: `sin²θ = (1 − cos 2θ)/2`, so the integral is `(1/2)(∫ e^(x·cos) − ∫ e^(x·cos)·cos 2θ) =
(1/2)(π·I₀ − π·I₂)` (`integral_exp_cos_eq_pi_mul_besselI_zero`, `besselI_two_eq_integral`), and the recurrence
`I₀ − I₂ = 2I₁/x` gives `π·I₁/x`. -/
theorem su2_weyl_integral_heat_kernel (x : ℝ) (hx : 0 < x) :
    ∫ θ in (0 : ℝ)..Real.pi, Real.exp (x * Real.cos θ) * (Real.sin θ)^2 = Real.pi * besselI 1 x / x := by
  have hx' : 0 ≤ x := le_of_lt hx
  have hI0 := integral_exp_cos_eq_pi_mul_besselI_zero x hx'
  have hI2 := besselI_two_eq_integral x hx'
  have hI2int : ∫ θ in (0 : ℝ)..Real.pi, Real.exp (x * Real.cos θ) * Real.cos (2 * θ) = Real.pi * besselI 2 x := by
    have h := congrArg (fun t : ℝ => Real.pi * t) hI2
    field_simp [ne_of_gt Real.pi_pos] at h
    exact h.symm
  have hsin2 : ∀ θ : ℝ, (Real.sin θ)^2 = (1 - Real.cos (2 * θ)) / 2 := by
    intro θ
    rw [Real.sin_sq_eq_half_sub]
    ring_nf
  have hmain : ∫ θ in (0 : ℝ)..Real.pi, Real.exp (x * Real.cos θ) * (Real.sin θ)^2
      = (Real.pi * besselI 0 x - Real.pi * besselI 2 x) / 2 := by
    have hcongr : (fun θ : ℝ => Real.exp (x * Real.cos θ) * (Real.sin θ)^2)
        = fun θ : ℝ => (Real.exp (x * Real.cos θ) - Real.exp (x * Real.cos θ) * Real.cos (2 * θ)) / 2 := by
      funext θ
      rw [hsin2 θ]
      ring
    rw [hcongr]
    rw [intervalIntegral.integral_div]
    rw [intervalIntegral.integral_sub]
    · rw [hI0, hI2int]
    · exact (by continuity : Continuous (fun θ : ℝ => Real.exp (x * Real.cos θ))).intervalIntegrable 0 Real.pi
    · exact (by continuity : Continuous (fun θ : ℝ => Real.exp (x * Real.cos θ) * Real.cos (2 * θ))).intervalIntegrable 0 Real.pi
  rw [hmain]
  have hfactor : (Real.pi * besselI 0 x - Real.pi * besselI 2 x) / 2 = Real.pi * (besselI 0 x - besselI 2 x) / 2 := by ring
  rw [hfactor]
  rw [bessel_recurrence hx]
  field_simp [ne_of_gt hx]
  ring

/-- **The RG step's partition function is bounded below by `1`**: `1 ≤ 2·I₁(β)/β` for `β > 0`. The block-spin
average at the trivial connection is `π·I₁(β)/β` (`su2_weyl_integral_heat_kernel`), and its normalization by the
Weyl measure `π/2` gives the RG step's partition function `2·I₁(β)/β`, which is `≥ 1` by the leading-term bound
`β/2 ≤ I₁(β)` (`besselI_one_ge_half_mul`). So the block-spin RG step does not shrink the measure below unit mass. -/
theorem blockSpin_partition_ge_one (β : ℝ) (hβ : 0 < β) :
    1 ≤ 2 * besselI 1 β / β := by
  have hlb : β / 2 ≤ besselI 1 β := besselI_one_ge_half_mul β (le_of_lt hβ)
  rw [le_div_iff₀ hβ]
  nlinarith [hlb]

/-- **The `cos(2θ)` Weyl moment**: `∫₀^π cos(2θ)·sin²θ dθ = −π/4`. Building block of the block-spin average's
character convolution: `sin²θ = (1 − cos 2θ)/2` makes the moment `(1/2)(∫ cos 2θ − ∫ cos² 2θ) = (1/2)(0 − π/2)`. -/
theorem su2_cos_two_moment :
    ∫ θ in (0 : ℝ)..Real.pi, Real.cos (2 * θ) * (Real.sin θ)^2 = -(Real.pi / 4) := by
  have hsin2 : ∀ θ : ℝ, (Real.sin θ)^2 = (1 - Real.cos (2 * θ)) / 2 := by
    intro θ
    rw [Real.sin_sq_eq_half_sub]
    ring_nf
  have hcongr : (fun θ : ℝ => Real.cos (2 * θ) * (Real.sin θ)^2)
      = fun θ : ℝ => (Real.cos (2 * θ) - Real.cos (2 * θ) ^ 2) / 2 := by
    funext θ
    rw [hsin2 θ]
    ring
  have hcos2 : ∫ θ in (0 : ℝ)..Real.pi, Real.cos (2 * θ) = 0 := by
    rw [intervalIntegral.integral_congr (fun θ _ => by rw [show 2 * θ = ((2 : ℕ) : ℝ) * θ by norm_num])]
    exact integral_cos_of_ne_zero (by norm_num : (2 : ℕ) ≠ 0)
  have hcos2sq : ∫ θ in (0 : ℝ)..Real.pi, Real.cos (2 * θ) ^ 2 = Real.pi / 2 := by
    have hcos2sq_form : ∀ θ : ℝ, Real.cos (2 * θ) ^ 2 = (1 + Real.cos (4 * θ)) / 2 := by
      intro θ
      rw [Real.cos_sq_eq_half_add]
      ring_nf
    rw [intervalIntegral.integral_congr (fun θ _ => hcos2sq_form θ)]
    rw [intervalIntegral.integral_div]
    rw [intervalIntegral.integral_add]
    · rw [intervalIntegral.integral_const]
      have hcos4 : ∫ θ in (0 : ℝ)..Real.pi, Real.cos (4 * θ) = 0 := by
        rw [intervalIntegral.integral_congr (fun θ _ => by rw [show 4 * θ = ((4 : ℕ) : ℝ) * θ by norm_num])]
        exact integral_cos_of_ne_zero (by norm_num : (4 : ℕ) ≠ 0)
      rw [hcos4]
      norm_num
    · exact (by continuity : Continuous (fun _ : ℝ => (1 : ℝ))).intervalIntegrable 0 Real.pi
    · exact (by continuity : Continuous (fun θ : ℝ => Real.cos (4 * θ))).intervalIntegrable 0 Real.pi
  rw [hcongr]
  rw [intervalIntegral.integral_div]
  rw [intervalIntegral.integral_sub]
  · rw [hcos2, hcos2sq]
    norm_num
  · exact (by continuity : Continuous (fun θ : ℝ => Real.cos (2 * θ))).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ : ℝ => Real.cos (2 * θ) ^ 2)).intervalIntegrable 0 Real.pi

/-- **The basic sine integral**: `∫₀^π sin(n·θ) dθ = (1 − (−1)ⁿ)/n` for `n ≠ 0`. The antiderivative of
`sin(n·θ)` is `−cos(n·θ)/n` (the chain rule), so the FTC gives `(cos 0 − cos(nπ))/n = (1 − (−1)ⁿ)/n`.
Building block for the odd sine Weyl moments. -/
theorem integral_sin_nat {n : ℕ} (hn : n ≠ 0) :
    ∫ θ in (0 : ℝ)..Real.pi, Real.sin ((n : ℝ) * θ) = (1 - (-1 : ℝ) ^ n) / n := by
  let f : ℝ → ℝ := fun t => -Real.cos ((n : ℝ) * t) / (n : ℝ)
  have hderiv : ∀ θ : ℝ, HasDerivAt f (Real.sin ((n : ℝ) * θ)) θ := by
    intro θ
    have hcos : HasDerivAt (fun t : ℝ => Real.cos ((n : ℝ) * t)) (-((n : ℝ) * Real.sin ((n : ℝ) * θ))) θ := by
      simpa [mul_comm] using (Real.hasDerivAt_cos ((n : ℝ) * θ)).comp θ (hasDerivAt_const_mul (n : ℝ) θ (hasDerivAt_id θ))
    have hneg := hcos.const_mul (-(1 / (n : ℝ)))
    convert hneg using 1
    · ext t
      dsimp [f]
      ring
    · ring_nf
      rw [show (n : ℝ) ≠ 0 by exact_mod_cast hn]
      ring
  have hcont : ContinuousOn f (Set.Icc (0 : ℝ) Real.pi) := by
    exact (by continuity : Continuous f).continuousOn
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (le_of_lt Real.pi_pos) hcont (fun θ hθ => hderiv θ)]
  dsimp [f]
  have hcos0 : Real.cos ((n : ℝ) * 0) = 1 := by norm_num
  have hcospi : Real.cos ((n : ℝ) * Real.pi) = (-1 : ℝ) ^ n := by
    rw [Real.cos_nat_mul_pi]
  rw [hcos0, hcospi]
  field_simp [show (n : ℝ) ≠ 0 by exact_mod_cast hn]
  ring

/-- **The odd sine Weyl moment**: `∫₀^π sin((2m+1)θ)·sin²θ dθ = −4/((2m+1)(2m+3)(2m−1))` for `m ≥ 1`.
Building block of the block-spin average's character convolution: `sin² = (1 − cos 2θ)/2` and the product-to-sum
`sin·cos 2θ = (sin((2m+3)θ) + sin((2m−1)θ))/2` reduce it to the basic sine integrals (`integral_sin_nat`). -/
theorem su2_sin_odd_moment {m : ℕ} (hm : 1 ≤ m) :
    ∫ θ in (0 : ℝ)..Real.pi, Real.sin ((2 * m + 1 : ℝ) * θ) * (Real.sin θ)^2
      = -4 / ((2 * m + 1 : ℝ) * (2 * m + 3) * (2 * m - 1)) := by
  have hsin2 : ∀ θ : ℝ, (Real.sin θ)^2 = (1 - Real.cos (2 * θ)) / 2 := by
    intro θ
    rw [Real.sin_sq_eq_half_sub]
    ring_nf
  have hcongr : (fun θ : ℝ => Real.sin ((2 * m + 1 : ℝ) * θ) * (Real.sin θ)^2)
      = fun θ : ℝ => (Real.sin ((2 * m + 1 : ℝ) * θ) - Real.sin ((2 * m + 1 : ℝ) * θ) * Real.cos (2 * θ)) / 2 := by
    funext θ
    rw [hsin2 θ]
    ring
  have hsin1 : ∫ θ in (0 : ℝ)..Real.pi, Real.sin ((2 * m + 1 : ℝ) * θ) = 2 / (2 * m + 1 : ℝ) := by
    have h := integral_sin_nat (n := 2 * m + 1) (by omega)
    have hneg : (-1 : ℝ) ^ (2 * m + 1) = -1 := by
      exact neg_one_pow_eq_neg_one_iff.mpr (by omega : Odd (2 * m + 1))
    simpa [hneg] using h
  have hsincos : ∫ θ in (0 : ℝ)..Real.pi, Real.sin ((2 * m + 1 : ℝ) * θ) * Real.cos (2 * θ)
      = 1 / (2 * m + 3 : ℝ) + 1 / (2 * m - 1 : ℝ) := by
    have hprod : ∀ θ : ℝ, Real.sin ((2 * m + 1 : ℝ) * θ) * Real.cos (2 * θ)
        = (Real.sin ((2 * m + 3 : ℝ) * θ) + Real.sin ((2 * m - 1 : ℝ) * θ)) / 2 := by
      intro θ
      have hsum : Real.sin ((2 * m + 1 : ℝ) * θ + 2 * θ) + Real.sin ((2 * m + 1 : ℝ) * θ - 2 * θ)
          = 2 * (Real.sin ((2 * m + 1 : ℝ) * θ) * Real.cos (2 * θ)) := by
        nlinarith [Real.sin_add ((2 * m + 1 : ℝ) * θ) (2 * θ), Real.sin_sub ((2 * m + 1 : ℝ) * θ) (2 * θ)]
      have harg1 : (2 * m + 1 : ℝ) * θ + 2 * θ = (2 * m + 3 : ℝ) * θ := by ring
      have harg2 : (2 * m + 1 : ℝ) * θ - 2 * θ = (2 * m - 1 : ℝ) * θ := by ring
      rw [harg1, harg2] at hsum
      nlinarith [hsum]
    have h3 : ∫ θ in (0 : ℝ)..Real.pi, Real.sin ((2 * m + 3 : ℝ) * θ) = 2 / (2 * m + 3 : ℝ) := by
      have h := integral_sin_nat (n := 2 * m + 3) (by omega)
      have hneg : (-1 : ℝ) ^ (2 * m + 3) = -1 := by
        exact neg_one_pow_eq_neg_one_iff.mpr (by omega : Odd (2 * m + 3))
      simpa [hneg] using h
    have h1 : ∫ θ in (0 : ℝ)..Real.pi, Real.sin ((2 * m - 1 : ℝ) * θ) = 2 / (2 * m - 1 : ℝ) := by
      have h := integral_sin_nat (n := 2 * m - 1) (by omega : 2 * m - 1 ≠ 0)
      have hneg : (-1 : ℝ) ^ (2 * m - 1) = -1 := by
        exact neg_one_pow_eq_neg_one_iff.mpr (by omega : Odd (2 * m - 1))
      simpa [hneg] using h
    rw [intervalIntegral.integral_congr (fun θ _ => hprod θ)]
    rw [intervalIntegral.integral_div]
    rw [intervalIntegral.integral_add]
    · rw [h3, h1]
      ring
    · exact (by continuity : Continuous (fun θ : ℝ => Real.sin ((2 * m + 3 : ℝ) * θ))).intervalIntegrable 0 Real.pi
    · exact (by continuity : Continuous (fun θ : ℝ => Real.sin ((2 * m - 1 : ℝ) * θ))).intervalIntegrable 0 Real.pi
  rw [hcongr]
  rw [intervalIntegral.integral_div]
  rw [intervalIntegral.integral_sub]
  · rw [hsin1, hsincos]
    field_simp [show (2 * m + 1 : ℝ) ≠ 0 by positivity, show (2 * m + 3 : ℝ) ≠ 0 by positivity, show (2 * m - 1 : ℝ) ≠ 0 by nlinarith [hm]]
    ring
  · exact (by continuity : Continuous (fun θ : ℝ => Real.sin ((2 * m + 1 : ℝ) * θ))).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ : ℝ => Real.sin ((2 * m + 1 : ℝ) * θ) * Real.cos (2 * θ))).intervalIntegrable 0 Real.pi
/-- **The `cos(nθ)` Weyl moment vanishes for `n ≠ 0, 2`**: `∫₀^π cos(nθ)·sin²θ dθ = 0`. With `su2_cos_two_moment`
(the `n = 2` value `−π/4`), this isolates the only nonzero cos moment — the block-spin average's character
convolution has a single cosine term `−(π/2)·I₂(β)·cos(2θ₁)`. -/
theorem su2_cos_moment_ne_two {n : ℕ} (hn : n ≠ 0) (hn2 : n ≠ 2) :
    ∫ θ in (0 : ℝ)..Real.pi, Real.cos ((n : ℝ) * θ) * (Real.sin θ)^2 = 0 := by
  have hsin2 : ∀ θ : ℝ, (Real.sin θ)^2 = (1 - Real.cos (2 * θ)) / 2 := by
    intro θ
    rw [Real.sin_sq_eq_half_sub]
    ring_nf
  have hcongr : (fun θ : ℝ => Real.cos ((n : ℝ) * θ) * (Real.sin θ)^2)
      = fun θ : ℝ => (Real.cos ((n : ℝ) * θ) - Real.cos ((n : ℝ) * θ) * Real.cos (2 * θ)) / 2 := by
    funext θ
    rw [hsin2 θ]
    ring
  have hcosn : ∫ θ in (0 : ℝ)..Real.pi, Real.cos ((n : ℝ) * θ) = 0 :=
    integral_cos_of_ne_zero hn
  have hcosncos2 : ∫ θ in (0 : ℝ)..Real.pi, Real.cos ((n : ℝ) * θ) * Real.cos (2 * θ) = 0 := by
    have hprod : ∀ θ : ℝ, Real.cos ((n : ℝ) * θ) * Real.cos (2 * θ)
        = (Real.cos (((n + 2 : ℕ) : ℝ) * θ) + Real.cos (((n - 2 : ℕ) : ℝ) * θ)) / 2 := by
      intro θ
      have hsum : Real.cos ((n : ℝ) * θ + 2 * θ) + Real.cos ((n : ℝ) * θ - 2 * θ)
          = 2 * (Real.cos ((n : ℝ) * θ) * Real.cos (2 * θ)) := by
        nlinarith [Real.cos_add ((n : ℝ) * θ) (2 * θ), Real.cos_sub ((n : ℝ) * θ) (2 * θ)]
      have harg1 : (n : ℝ) * θ + 2 * θ = ((n + 2 : ℕ) : ℝ) * θ := by
        norm_num [Nat.cast_add]; ring
      have harg2 : (n : ℝ) * θ - 2 * θ = ((n - 2 : ℕ) : ℝ) * θ := by
        norm_num [Nat.cast_sub (by omega : 2 ≤ n)]; ring
      rw [harg1, harg2] at hsum
      nlinarith [hsum]
    rw [intervalIntegral.integral_congr (fun θ _ => hprod θ)]
    rw [intervalIntegral.integral_div]
    rw [intervalIntegral.integral_add]
    · have hn2' : n + 2 ≠ 0 := by omega
      have hn0' : n - 2 ≠ 0 := by omega
      rw [integral_cos_of_ne_zero hn2', integral_cos_of_ne_zero hn0']
      norm_num
    · exact (by continuity : Continuous (fun θ : ℝ => Real.cos (((n + 2 : ℕ) : ℝ) * θ))).intervalIntegrable 0 Real.pi
    · exact (by continuity : Continuous (fun θ : ℝ => Real.cos (((n - 2 : ℕ) : ℝ) * θ))).intervalIntegrable 0 Real.pi
  rw [hcongr]
  rw [intervalIntegral.integral_div]
  rw [intervalIntegral.integral_sub]
  · rw [hcosn, hcosncos2]
    norm_num
  · exact (by continuity : Continuous (fun θ : ℝ => Real.cos ((n : ℝ) * θ))).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ : ℝ => Real.cos ((n : ℝ) * θ) * Real.cos (2 * θ))).intervalIntegrable 0 Real.pi

/-- **The shifted `cos(2θ₁)` projection of a cosine mode**: `∫₀^π cos((n+1)(θ₁+θ₂))·cos(2θ₁) dθ₁ =
cos((n+1)θ₂)·(π/2 if n=1 else 0) − sin((n+1)θ₂)·(1/(2(n+3))·(1−(−1)^{n+3}) + 1/(2(n−1))·(1−(−1)^{n−1}))`.
The addition formula + `integral_cos_succ_mul_cos_two` (the cos part) + the product-to-sum + `integral_sin_nat`
(the sin part). This is the termwise-integration primitive for the block-spin average's cosine projection. -/
theorem integral_cos_succ_mul_cos_two_shift (n : ℕ) (θ₂ : ℝ) :
    ∫ θ₁ in (0 : ℝ)..Real.pi, Real.cos ((n + 1 : ℝ) * (θ₁ + θ₂)) * Real.cos (2 * θ₁)
      = Real.cos ((n + 1 : ℝ) * θ₂) * (if n = 1 then Real.pi / 2 else 0)
        - Real.sin ((n + 1 : ℝ) * θ₂) * ((1 - (-1 : ℝ) ^ (n + 3)) / (2 * (n + 3)) + (1 - (-1 : ℝ) ^ (n - 1)) / (2 * (n - 1))) := by
  have hadd : ∀ θ₁ : ℝ, Real.cos ((n + 1 : ℝ) * (θ₁ + θ₂))
      = Real.cos ((n + 1 : ℝ) * θ₁) * Real.cos ((n + 1 : ℝ) * θ₂) - Real.sin ((n + 1 : ℝ) * θ₁) * Real.sin ((n + 1 : ℝ) * θ₂) := by
    intro θ₁
    rw [mul_add]
    exact Real.cos_add ((n + 1 : ℝ) * θ₁) ((n + 1 : ℝ) * θ₂)
  have hcongr : (fun θ₁ : ℝ => Real.cos ((n + 1 : ℝ) * (θ₁ + θ₂)) * Real.cos (2 * θ₁))
      = fun θ₁ : ℝ => Real.cos ((n + 1 : ℝ) * θ₁) * Real.cos ((n + 1 : ℝ) * θ₂) * Real.cos (2 * θ₁)
          - Real.sin ((n + 1 : ℝ) * θ₁) * Real.sin ((n + 1 : ℝ) * θ₂) * Real.cos (2 * θ₁) := by
    funext θ₁
    rw [hadd θ₁]
    ring
  have hcos : ∫ θ₁ in (0 : ℝ)..Real.pi, Real.cos ((n + 1 : ℝ) * θ₁) * Real.cos ((n + 1 : ℝ) * θ₂) * Real.cos (2 * θ₁)
      = Real.cos ((n + 1 : ℝ) * θ₂) * (if n = 1 then Real.pi / 2 else 0) := by
    rw [intervalIntegral.integral_congr (fun θ₁ _ => by ring : ∀ θ₁, Real.cos ((n + 1 : ℝ) * θ₁) * Real.cos ((n + 1 : ℝ) * θ₂) * Real.cos (2 * θ₁) = Real.cos ((n + 1 : ℝ) * θ₂) * (Real.cos ((n + 1 : ℝ) * θ₁) * Real.cos (2 * θ₁)))]
    rw [intervalIntegral.integral_const_mul]
    rw [integral_cos_succ_mul_cos_two n]
  have hsin : ∫ θ₁ in (0 : ℝ)..Real.pi, Real.sin ((n + 1 : ℝ) * θ₁) * Real.sin ((n + 1 : ℝ) * θ₂) * Real.cos (2 * θ₁)
      = Real.sin ((n + 1 : ℝ) * θ₂) * ((1 - (-1 : ℝ) ^ (n + 3)) / (2 * (n + 3)) + (1 - (-1 : ℝ) ^ (n - 1)) / (2 * (n - 1))) := by
    rw [intervalIntegral.integral_congr (fun θ₁ _ => by ring : ∀ θ₁, Real.sin ((n + 1 : ℝ) * θ₁) * Real.sin ((n + 1 : ℝ) * θ₂) * Real.cos (2 * θ₁) = Real.sin ((n + 1 : ℝ) * θ₂) * (Real.sin ((n + 1 : ℝ) * θ₁) * Real.cos (2 * θ₁)))]
    rw [intervalIntegral.integral_const_mul]
    -- ∫ sin((n+1)θ)cos(2θ) = 1/2(∫sin((n+3)θ) + ∫sin((n−1)θ))
    have hprod : ∀ θ : ℝ, Real.sin ((n + 1 : ℝ) * θ) * Real.cos (2 * θ)
        = (Real.sin ((n + 3 : ℝ) * θ) + Real.sin ((n - 1 : ℝ) * θ)) / 2 := by
      intro θ
      have hsum : Real.sin ((n + 1 : ℝ) * θ + 2 * θ) + Real.sin ((n + 1 : ℝ) * θ - 2 * θ)
          = 2 * (Real.sin ((n + 1 : ℝ) * θ) * Real.cos (2 * θ)) := by
        nlinarith [Real.sin_add ((n + 1 : ℝ) * θ) (2 * θ), Real.sin_sub ((n + 1 : ℝ) * θ) (2 * θ)]
      have harg1 : (n + 1 : ℝ) * θ + 2 * θ = (n + 3 : ℝ) * θ := by ring
      have harg2 : (n + 1 : ℝ) * θ - 2 * θ = ((n : ℤ) - 1 : ℝ) * θ := by norm_num; ring
      rw [harg1] at hsum
      rw [show (n + 1 : ℝ) * θ - 2 * θ = ((n : ℝ) - 1) * θ by ring] at hsum
      nlinarith [hsum]
    rw [intervalIntegral.integral_congr (fun θ _ => hprod θ)]
    rw [intervalIntegral.integral_div, intervalIntegral.integral_add]
    · have h3 := integral_sin_nat (n := n + 3) (by omega)
      have hn1 := integral_sin_nat (n := n - 1) (by omega : n - 1 ≠ 0)
      rw [h3, hn1]
      ring
    · exact (by continuity : Continuous (fun θ : ℝ => Real.sin ((n + 3 : ℝ) * θ))).intervalIntegrable 0 Real.pi
    · exact (by continuity : Continuous (fun θ : ℝ => Real.sin (((n : ℝ) - 1) * θ))).intervalIntegrable 0 Real.pi
  rw [hcongr]
  rw [intervalIntegral.integral_sub]
  · rw [hcos, hsin]
    ring
  · exact (by continuity : Continuous (fun θ₁ : ℝ => Real.cos ((n + 1 : ℝ) * θ₁) * Real.cos ((n + 1 : ℝ) * θ₂) * Real.cos (2 * θ₁))).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ₁ : ℝ => Real.sin ((n + 1 : ℝ) * θ₁) * Real.sin ((n + 1 : ℝ) * θ₂) * Real.cos (2 * θ₁))).intervalIntegrable 0 Real.pi

/-- **The general Bessel factorial identity**: `1/(k!(k+n)!) − 1/((k−1)!(k+n+1)!) = (n+1)/(k!(k+n+1)!)`. The
coefficient identity behind the general recurrence `Iₙ − Iₙ₊₂ = 2(n+1)Iₙ₊₁/x`. -/
theorem bessel_factorial_identity_general (k n : ℕ) (hk : 1 ≤ k) :
    1 / ((k.factorial : ℝ) * (k + n).factorial) - 1 / (((k - 1).factorial : ℝ) * (k + n + 1).factorial)
      = (n + 1 : ℝ) / ((k.factorial : ℝ) * (k + n + 1).factorial) := by
  have hkfac : (k.factorial : ℝ) = k * (k - 1).factorial := by
    norm_num [Nat.factorial_succ]
  have hknn : ((k + n + 1).factorial : ℝ) = (k + n + 1) * (k + n).factorial := by
    norm_num [Nat.factorial_succ]
  have hden : (k.factorial : ℝ) * (k + n + 1).factorial ≠ 0 := by positivity
  have hden2 : ((k - 1).factorial : ℝ) * (k + n + 1).factorial ≠ 0 := by positivity
  field_simp [hden, hden2]
  rw [hkfac, hknn]
  nlinarith [show (0 : ℝ) < (k - 1).factorial by positivity, show (0 : ℝ) < (k + n).factorial by positivity]

/-- **The general Bessel recurrence**: `Iₙ(x) − Iₙ₊₂(x) = (2(n+1)/x)·Iₙ₊₁(x)` for `x > 0`. The general
`I_{ν−1} − I_{ν+1} = (2ν/x)I_ν` at `ν = n+1`, via the coefficient identity `bessel_factorial_identity_general`.
This is the key identity for the SU(2) Weyl character formula. -/
theorem bessel_recurrence_general {n : ℕ} {x : ℝ} (hx : 0 < x) :
    besselI n x - besselI (n + 2) x = (2 * (n + 1 : ℝ) / x) * besselI (n + 1) x := by
  have hxne : x ≠ 0 := ne_of_gt hx
  let a : ℕ → ℝ := fun k => (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)
  let b : ℕ → ℝ := fun k => (x / 2) ^ (2 * k + n + 2) / ((k.factorial : ℝ) * (k + n + 2).factorial)
  have hIn : besselI n x = ∑' k, a k := by dsimp [besselI, a]
  have hIn2 : besselI (n + 2) x = ∑' k, b k := by dsimp [besselI, b]
  have ha : Summable a := by dsimp [a]; simpa using besselI_summable_of_nonneg n (le_of_lt hx)
  have hb : Summable b := by dsimp [b]; simpa using besselI_summable_of_nonneg (n + 2) (le_of_lt hx)
  rw [hIn, hIn2, ← tsum_sub]
  · -- the difference telescopes: a_k − b_k re-indexed
    have hreindex : (∑' k : ℕ, b k) = (∑' k : ℕ, (x / 2) ^ (2 * k + n) / (((k - 1).factorial : ℝ) * (k + n + 1).factorial)) := by
      -- shift b by 1: b_k = c_{k+1} where c_j = (x/2)^{2j+n}/((j−1)!(j+n+1)!)
      have hshift : (∑' k : ℕ, b k) = (∑' k : ℕ, (fun j : ℕ => (x / 2) ^ (2 * j + n) / (((j - 1).factorial : ℝ) * (j + n + 1).factorial)) (k + 1)) := by
        apply tsum_congr
        intro k
        dsimp [b]
        congr 1
        · rw [show 2 * (k + 1) + n = 2 * k + n + 2 by ring]
        · congr 1 <;> ring
      rw [hshift]
      -- re-index: sum over k of c_{k+1} = sum over j of c_j (with c_0 = 0)
      have hsum : (∑' k : ℕ, (fun j : ℕ => (x / 2) ^ (2 * j + n) / (((j - 1).factorial : ℝ) * (j + n + 1).factorial)) (k + 1))
          = (∑' k : ℕ, (if k = 0 then 0 else (x / 2) ^ (2 * k + n) / (((k - 1).factorial : ℝ) * (k + n + 1).factorial))) := by
        rw [← tsum_eq_add_tsum_ite (b := fun k : ℕ => (x / 2) ^ (2 * k + n) / (((k - 1).factorial : ℝ) * (k + n + 1).factorial)) (0 : ℕ)]
        · apply tsum_congr
          intro k
          by_cases hk : k = 0
          · subst k; norm_num
          · simp [hk]
        · -- summable of the shifted sequence
          exact hb.comp_injective (Nat.succ_injective)
      rw [hsum]
      -- the k=0 term of the if is 0, so the sum over k is the sum over k≥1 of c_k
      have hif0 : (fun k : ℕ => if k = 0 then 0 else (x / 2) ^ (2 * k + n) / (((k - 1).factorial : ℝ) * (k + n + 1).factorial)) 0 = 0 := by simp
      -- ∑' (if k=0 then 0 else c_k) = ∑' c_k (where c_0 is the if, but it equals 0 anyway)
      rfl
    -- now: ∑' a_k − ∑' b_k = ∑' (a_k − c_k)
    rw [hreindex]
    have hsumsub : (∑' k : ℕ, a k) - (∑' k : ℕ, (x / 2) ^ (2 * k + n) / (((k - 1).factorial : ℝ) * (k + n + 1).factorial))
        = ∑' k : ℕ, (a k - (x / 2) ^ (2 * k + n) / (((k - 1).factorial : ℝ) * (k + n + 1).factorial)) := by
      rw [← tsum_sub]
      rfl
      -- summable of the shifted sequence
      · exact hb.comp_injective (Nat.succ_injective)
    rw [hsumsub]
    -- a_k − c_k = (2(n+1)/x)·(x/2)^{2k+n+1}/(k!(k+n+1)!)
    have hterm : ∀ k, a k - (x / 2) ^ (2 * k + n) / (((k - 1).factorial : ℝ) * (k + n + 1).factorial)
        = (2 * (n + 1 : ℝ) / x) * ((x / 2) ^ (2 * k + n + 1) / ((k.factorial : ℝ) * (k + n + 1).factorial)) := by
      intro k
      dsimp [a]
      by_cases hk : k = 0
      · subst k
        norm_num
        ring
      · have hfac := bessel_factorial_identity_general k n (by omega : 1 ≤ k)
        -- a_k − c_k = (x/2)^{2k+n}·(1/(k!(k+n)!) − 1/((k−1)!(k+n+1)!))
        have hpow : (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)
            - (x / 2) ^ (2 * k + n) / (((k - 1).factorial : ℝ) * (k + n + 1).factorial)
            = (x / 2) ^ (2 * k + n) * ((n + 1 : ℝ) / ((k.factorial : ℝ) * (k + n + 1).factorial)) := by
          rw [← div_sub_div_same]
          rw [hfac]
        rw [hpow]
        -- (x/2)^{2k+n}·((n+1)/(k!(k+n+1)!)) = (2(n+1)/x)·(x/2)^{2k+n+1}/(k!(k+n+1)!)
        field_simp [hxne]
        rw [show (x / 2) ^ (2 * k + n + 1) = (x / 2) * (x / 2) ^ (2 * k + n) by rw [pow_succ]]
        ring
    simp_rw [hterm]
    -- (2(n+1)/x)·Σ (x/2)^{2k+n+1}/(k!(k+n+1)!) = (2(n+1)/x)·I_{n+1}
    rw [← tsum_mul_left]
    have hIn1 : (∑' k : ℕ, (x / 2) ^ (2 * k + n + 1) / ((k.factorial : ℝ) * (k + n + 1).factorial)) = besselI (n + 1) x := by
      dsimp [besselI]
      congr 1
      ext k
      congr 1 <;> ring
    rw [hIn1]
  · exact ha.sub hb

/-- **The general cosine orthogonality**: `∫₀^π cos((k+1)θ)·cos(nθ) dθ = π/2 if `k+1 = n` else 0`. The
product-to-sum `cos·cos = (cos(sum) + cos(diff))/2` with `integral_cos_of_ne_zero_int` (the signed difference).
This is the primitive for the general Jacobi–Anger moment `∫ e^(x·cos)·cos(n·) = π·Iₙ` and the Weyl character formula. -/
theorem integral_cos_succ_mul_cos_n (k n : ℕ) :
    ∫ θ in (0 : ℝ)..Real.pi, Real.cos ((k + 1 : ℝ) * θ) * Real.cos ((n : ℝ) * θ)
      = (if k + 1 = n then Real.pi / 2 else 0) := by
  have hprod : ∀ θ : ℝ, Real.cos ((k + 1 : ℝ) * θ) * Real.cos ((n : ℝ) * θ)
      = (Real.cos (((k + 1 + n : ℕ) : ℝ) * θ) + Real.cos (((k + 1 : ℤ) - n) * θ)) / 2 := by
    intro θ
    have hsum : Real.cos ((k + 1 : ℝ) * θ + (n : ℝ) * θ) + Real.cos ((k + 1 : ℝ) * θ - (n : ℝ) * θ)
        = 2 * (Real.cos ((k + 1 : ℝ) * θ) * Real.cos ((n : ℝ) * θ)) := by
      nlinarith [Real.cos_add ((k + 1 : ℝ) * θ) (n : ℝ) * θ, Real.cos_sub ((k + 1 : ℝ) * θ) ((n : ℝ) * θ)]
    have harg1 : (k + 1 : ℝ) * θ + (n : ℝ) * θ = ((k + 1 + n : ℕ) : ℝ) * θ := by
      norm_num [Nat.cast_add]; ring
    have harg2 : (k + 1 : ℝ) * θ - (n : ℝ) * θ = (((k + 1 : ℤ) - n) : ℝ) * θ := by
      norm_num [Int.cast_sub]; ring
    rw [harg1, harg2] at hsum
    nlinarith [hsum]
  rw [intervalIntegral.integral_congr (fun θ _ => hprod θ)]
  rw [intervalIntegral.integral_div, intervalIntegral.integral_add]
  · have hsumzero : ∫ θ in (0 : ℝ)..Real.pi, Real.cos (((k + 1 + n : ℕ) : ℝ) * θ) = 0 :=
      integral_cos_of_ne_zero (k + 1 + n) (by omega : k + 1 + n ≠ 0)
    have hdiff : ∫ θ in (0 : ℝ)..Real.pi, Real.cos (((k + 1 : ℤ) - n) * θ) = (if k + 1 = n then Real.pi else 0) := by
      by_cases hkn : (k : ℤ) + 1 = (n : ℤ)
      · have hkn_nat : k + 1 = n := by omega
        subst n
        rw [show (k + 1 : ℤ) - (k + 1) = 0 by omega]
        rw [intervalIntegral.integral_congr (fun θ _ => by norm_num)]
        rw [intervalIntegral.integral_const]
        norm_num
      · have hne : (k + 1 : ℤ) - n ≠ 0 := by omega
        rw [if_neg (by omega : k + 1 ≠ n)]
        simpa using integral_cos_of_ne_zero_int (k + 1 : ℤ) n hne
    rw [hsumzero, hdiff]
    by_cases hkn : k + 1 = n
    · simp [hkn]
    · simp [hkn]
  · exact (by continuity : Continuous (fun θ : ℝ => Real.cos (((k + 1 + n : ℕ) : ℝ) * θ))).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ : ℝ => Real.cos (((k + 1 : ℤ) - n) * θ))).intervalIntegrable 0 Real.pi

/-- **The general Jacobi–Anger moment**: `besselI n x = (1/π)·∫₀^π e^(x·cos θ)·cos(nθ) dθ` for `n ≥ 1`.
Mirrors `besselI_two_eq_integral` with `cos(nθ)` and the general orthogonality `integral_cos_succ_mul_cos_n`:
the Jacobi–Anger expansion termwise-integrated against `cos(nθ)` leaves only the `k+1 = n` term
(`tsum_eq_single (n−1)`), giving `π·Iₙ`. This is the moment identity that assembles the SU(2) Weyl character formula. -/
theorem besselI_eq_integral_general {n : ℕ} (x : ℝ) (hx : 0 ≤ x) (hn : 1 ≤ n) :
    besselI n x = (1 / Real.pi) * ∫ θ in (0 : ℝ)..Real.pi, Real.exp (x * Real.cos θ) * Real.cos ((n : ℝ) * θ) := by
  let g : ℕ → C(ℝ, ℝ) := fun k => ⟨fun θ => besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ) * Real.cos ((n : ℝ) * θ), by
    exact (continuous_const.mul (Real.continuous_cos.comp (continuous_const.mul continuous_id))).mul
      (Real.continuous_cos.comp (continuous_const.mul continuous_id))⟩
  have hg_sum : Summable (fun k => ‖(g k).restrict (⟨Set.uIcc (0 : ℝ) Real.pi, isCompact_uIcc⟩ : TopologicalSpace.Compacts ℝ)‖) := by
    refine Summable.of_nonneg_of_le (fun k => ?_) (fun k => ?_) (by simpa [Nat.succ_eq_add_one] using (besselI_summable hx).comp_injective Nat.succ_injective)
    · apply norm_nonneg
    · exact (ContinuousMap.norm_le ((g k).restrict (⟨Set.uIcc (0 : ℝ) Real.pi, isCompact_uIcc⟩ : TopologicalSpace.Compacts ℝ)) (C := besselI (k + 1) x) (besselI_nonneg (n := k + 1) hx)).mpr (fun θ => by
        dsimp [g]
        have h1 : ‖besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)‖ ≤ besselI (k + 1) x := by
          calc ‖besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)‖
              ≤ besselI (k + 1) x * ‖Real.cos ((k + 1 : ℝ) * θ)‖ := by
                  simpa [Real.norm_of_nonneg (besselI_nonneg (n := k + 1) hx)] using (norm_mul_le (besselI (k + 1) x) (Real.cos ((k + 1 : ℝ) * θ)))
              _ ≤ besselI (k + 1) x := by
                  rw [Real.norm_eq_abs]
                  exact (mul_le_mul_of_nonneg_left (Real.abs_cos_le_one ((k + 1 : ℝ) * θ)) (besselI_nonneg (n := k + 1) hx)).trans_eq (by ring)
        have h2 : ‖Real.cos ((n : ℝ) * θ)‖ ≤ 1 := by
          rw [Real.norm_eq_abs]
          exact Real.abs_cos_le_one ((n : ℝ) * θ)
        calc ‖besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ) * Real.cos ((n : ℝ) * θ)‖
            = ‖besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)‖ * ‖Real.cos ((n : ℝ) * θ)‖ := norm_mul _ _
            _ ≤ besselI (k + 1) x * 1 := mul_le_mul h1 h2 (norm_nonneg _) (besselI_nonneg (n := k + 1) hx)
            _ = besselI (k + 1) x := by ring)
  have hsumg : Summable g := by
    refine ContinuousMap.summable_of_locally_summable_norm (F := g) (fun K => ?_)
    refine Summable.of_nonneg_of_le (fun k => norm_nonneg _) (fun k => ?_) ((besselI_summable hx).comp_injective Nat.succ_injective)
    · exact (ContinuousMap.norm_le ((g k).restrict K) (C := besselI (k + 1) x) (besselI_nonneg (n := k + 1) hx)).mpr (fun θ => by
        dsimp [g]
        have h1 : ‖besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)‖ ≤ besselI (k + 1) x := by
          calc ‖besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)‖
              ≤ besselI (k + 1) x * ‖Real.cos ((k + 1 : ℝ) * θ)‖ := by
                  simpa [Real.norm_of_nonneg (besselI_nonneg (n := k + 1) hx)] using (norm_mul_le (besselI (k + 1) x) (Real.cos ((k + 1 : ℝ) * θ)))
              _ ≤ besselI (k + 1) x := by
                  rw [Real.norm_eq_abs]
                  exact (mul_le_mul_of_nonneg_left (Real.abs_cos_le_one ((k + 1 : ℝ) * θ)) (besselI_nonneg (n := k + 1) hx)).trans_eq (by ring)
        have h2 : ‖Real.cos ((n : ℝ) * θ)‖ ≤ 1 := by
          rw [Real.norm_eq_abs]
          exact Real.abs_cos_le_one ((n : ℝ) * θ)
        calc ‖besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ) * Real.cos ((n : ℝ) * θ)‖
            = ‖besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)‖ * ‖Real.cos ((n : ℝ) * θ)‖ := norm_mul _ _
            _ ≤ besselI (k + 1) x * 1 := mul_le_mul h1 h2 (norm_nonneg _) (besselI_nonneg (n := k + 1) hx)
            _ = besselI (k + 1) x := by ring)
  have hgtsum : ∀ θ : ℝ, (∑' k, g k) θ = ∑' k, (g k) θ := fun θ =>
    (hsumg.hasSum.map (g := @ContinuousMap.evalCLM ℝ _ ℝ ℝ _ _ _ _ _ _ θ) (hg := (@ContinuousMap.evalCLM ℝ _ ℝ ℝ _ _ _ _ _ _ θ).cont)).tsum_eq.symm
  have hgint : IntervalIntegrable (fun θ => (2 * ∑' k : ℕ, besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)) * Real.cos ((n : ℝ) * θ)) MeasureTheory.volume (0 : ℝ) Real.pi := by
    refine ⟨?_, ?_⟩
    · refine MeasureTheory.IntegrableOn.congr_fun (((2 : ℝ) • (∑' k, g k)).continuous.intervalIntegrable (μ := MeasureTheory.volume) (0 : ℝ) Real.pi).1 ?_ measurableSet_Ioc
      intro θ hθ
      rw [ContinuousMap.smul_apply, smul_eq_mul]
      rw [hgtsum θ]
      dsimp [g]
      conv_rhs => rw [mul_assoc]
      rw [← tsum_mul_right]
    · refine MeasureTheory.IntegrableOn.congr_fun (((2 : ℝ) • (∑' k, g k)).continuous.intervalIntegrable (μ := MeasureTheory.volume) (0 : ℝ) Real.pi).2 ?_ measurableSet_Ioc
      intro θ hθ
      rw [ContinuousMap.smul_apply, smul_eq_mul]
      rw [hgtsum θ]
      dsimp [g]
      conv_rhs => rw [mul_assoc]
      rw [← tsum_mul_right]
  have hmain : (∫ θ in (0 : ℝ)..Real.pi, Real.exp (x * Real.cos θ) * Real.cos ((n : ℝ) * θ)) = Real.pi * besselI n x := by
    simp_rw [jacobi_anger_real]
    simp_rw [show (∀ θ : ℝ, (besselI 0 x + 2 * ∑' k : ℕ, besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)) * Real.cos ((n : ℝ) * θ) =
        besselI 0 x * Real.cos ((n : ℝ) * θ) + (2 * ∑' k : ℕ, besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)) * Real.cos ((n : ℝ) * θ)) from fun θ => add_mul (a := besselI 0 x) (b := 2 * ∑' k : ℕ, besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)) (c := Real.cos ((n : ℝ) * θ))]
    rw [intervalIntegral.integral_add]
    · have hI0 : (∫ θ in (0 : ℝ)..Real.pi, besselI 0 x * Real.cos ((n : ℝ) * θ)) = 0 := by
        rw [intervalIntegral.integral_const_mul]
        rw [integral_cos_of_ne_zero n (by omega : n ≠ 0)]
        simp
      have htail : (∫ θ in (0 : ℝ)..Real.pi, (2 * ∑' k : ℕ, besselI (k + 1) x * Real.cos ((k + 1 : ℝ) * θ)) * Real.cos ((n : ℝ) * θ)) = Real.pi * besselI n x := by
        simp_rw [mul_assoc]
        simp_rw [← tsum_mul_right]
        change (∫ θ in (0 : ℝ)..Real.pi, (2 * ∑' k : ℕ, (g k) θ)) = Real.pi * besselI n x
        rw [intervalIntegral.integral_const_mul]
        have ht := @intervalIntegral.tsum_intervalIntegral_eq_of_summable_norm ℕ ℝ _ _ (0 : ℝ) Real.pi _ g hg_sum
        rw [← ht]
        have hterm : ∀ k : ℕ, (∫ θ in (0 : ℝ)..Real.pi, (g k) θ) = besselI (k + 1) x * (if k + 1 = n then Real.pi / 2 else 0) := by
          intro k
          dsimp [g]
          simp_rw [mul_assoc]
          rw [intervalIntegral.integral_const_mul]
          rw [integral_cos_succ_mul_cos_n k n]
        simp_rw [hterm]
        rw [tsum_eq_single (n - 1)]
        · rw [show (n - 1) + 1 = n by omega]
          rw [if_pos rfl]
          norm_num [Nat.cast_one]
          ring
        · intro b hb
          have hne : b + 1 ≠ n := by omega
          rw [if_neg hne]
          simp
      rw [hI0, htail, zero_add]
    · exact ((continuous_const : Continuous (fun _ : ℝ => besselI 0 x)).mul (Real.continuous_cos.comp (continuous_const.mul continuous_id))).intervalIntegrable (μ := MeasureTheory.volume) (0 : ℝ) Real.pi
    · exact hgint
  have hπ : Real.pi ≠ 0 := by exact_mod_cast Real.pi_ne_zero
  rw [hmain]
  field_simp [hπ]
/-- **The SU(2) Weyl character coefficient**: `(2/π)·∫₀^π e^(x·cos θ)·sin θ·sin((n+1)θ) dθ = 2(n+1)·Iₙ₊₁(x)/x`.
The coefficient `cₙ` of the Weyl character formula `e^(x·cos θ)·sin θ = Σ cₙ·sin((n+1)θ)`: `sin θ·sin((n+1)θ) =
(cos(nθ) − cos((n+2)θ))/2` + the general Jacobi–Anger moment (`besselI_eq_integral_general`) give `cₙ = Iₙ − Iₙ₊₂`,
and `bessel_recurrence_general` turns this into `2(n+1)Iₙ₊₁/x`. This is the clean coupling-advance identity. -/
theorem weyl_character_coefficient {n : ℕ} (x : ℝ) (hx : 0 < x) (hn : 1 ≤ n) :
    (2 / Real.pi) * ∫ θ in (0 : ℝ)..Real.pi, Real.exp (x * Real.cos θ) * Real.sin θ * Real.sin ((n + 1 : ℝ) * θ)
      = 2 * (n + 1 : ℝ) * besselI (n + 1) x / x := by
  have hprod : ∀ θ : ℝ, Real.sin θ * Real.sin ((n + 1 : ℝ) * θ)
      = (Real.cos ((n : ℝ) * θ) - Real.cos ((n + 2 : ℝ) * θ)) / 2 := by
    intro θ
    have hsub : Real.cos (θ - (n + 1 : ℝ) * θ) - Real.cos (θ + (n + 1 : ℝ) * θ)
        = 2 * (Real.sin θ * Real.sin ((n + 1 : ℝ) * θ)) := by
      nlinarith [Real.cos_sub θ ((n + 1 : ℝ) * θ), Real.cos_add θ ((n + 1 : ℝ) * θ)]
    have harg1 : θ - (n + 1 : ℝ) * θ = -((n : ℝ) * θ) := by ring
    have harg2 : θ + (n + 1 : ℝ) * θ = (n + 2 : ℝ) * θ := by ring
    rw [harg1, harg2] at hsub
    rw [Real.cos_neg ((n : ℝ) * θ)] at hsub
    nlinarith [hsub]
  have hcongr : (fun θ : ℝ => Real.exp (x * Real.cos θ) * Real.sin θ * Real.sin ((n + 1 : ℝ) * θ))
      = fun θ : ℝ => (Real.exp (x * Real.cos θ) * Real.cos ((n : ℝ) * θ) - Real.exp (x * Real.cos θ) * Real.cos ((n + 2 : ℝ) * θ)) / 2 := by
    funext θ
    rw [hprod θ]
    ring
  have hIn : ∫ θ in (0 : ℝ)..Real.pi, Real.exp (x * Real.cos θ) * Real.cos ((n : ℝ) * θ) = Real.pi * besselI n x := by
    have h := besselI_eq_integral_general (n := n) x (le_of_lt hx) hn
    have hπ : Real.pi ≠ 0 := by exact_mod_cast Real.pi_ne_zero
    field_simp [hπ] at h
    exact h.symm
  have hIn2 : ∫ θ in (0 : ℝ)..Real.pi, Real.exp (x * Real.cos θ) * Real.cos ((n + 2 : ℝ) * θ) = Real.pi * besselI (n + 2) x := by
    have h := besselI_eq_integral_general (n := n + 2) x (le_of_lt hx) (by omega)
    have hπ : Real.pi ≠ 0 := by exact_mod_cast Real.pi_ne_zero
    field_simp [hπ] at h
    exact h.symm
  rw [hcongr]
  rw [intervalIntegral.integral_div, intervalIntegral.integral_sub]
  · rw [hIn, hIn2]
    have hrec := bessel_recurrence_general (n := n) (x := x) hx
    rw [hrec]
    field_simp [ne_of_gt hx]
    ring
  · exact (by continuity : Continuous (fun θ : ℝ => Real.exp (x * Real.cos θ) * Real.cos ((n : ℝ) * θ))).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ : ℝ => Real.exp (x * Real.cos θ) * Real.cos ((n + 2 : ℝ) * θ))).intervalIntegrable 0 Real.pi

/-- **The derivative series is summable**: `Summable (fun n => (n+1)·Iₙ₊₁(x))` for `x ≥ 0`. From the recurrence
`(n+1)Iₙ₊₁ = (x/2)(Iₙ − Iₙ₊₂) ≤ (x/2)Iₙ` (since `Iₙ₊₂ ≥ 0`), so it is dominated by `(x/2)·Σ Iₙ`, which is summable
(`besselI_summable`). This is the summability hypothesis of `hasDerivAt_tsum` — the key input for the Weyl
character formula's termwise differentiation. -/
theorem besselI_mul_succ_summable (x : ℝ) (hx : 0 ≤ x) :
    Summable (fun n : ℕ => (n + 1 : ℝ) * besselI (n + 1) x) := by
  by_cases hx0 : x = 0
  · subst x
    have hzero : ∀ n, (n + 1 : ℝ) * besselI (n + 1) 0 = 0 := by
      intro n
      have hI : besselI (n + 1) 0 = 0 := by
        dsimp [besselI]
        have h : (fun m : ℕ => (0 / 2 : ℝ) ^ (2 * m + (n + 1)) / ((m.factorial : ℝ) * (m + (n + 1)).factorial)) = fun _ => 0 := by
          funext m
          rw [zero_div]
          rw [zero_pow (by omega : 2 * m + (n + 1) ≠ 0)]
          simp
        rw [h]
        exact tsum_zero
      rw [hI]
      ring
    simpa [hzero] using (summable_zero : Summable (fun _ : ℕ => (0 : ℝ)))
  · have hxpos : 0 < x := lt_of_le_of_ne hx (Ne.symm hx0)
    have hle : ∀ n, (n + 1 : ℝ) * besselI (n + 1) x ≤ (x / 2) * besselI n x := by
      intro n
      have hrec := bessel_recurrence_general (n := n) (x := x) hxpos
      have hnonneg : 0 ≤ besselI (n + 2) x := besselI_nonneg (n := n + 2) hx
      have hsub : besselI n x - besselI (n + 2) x ≤ besselI n x := by nlinarith [hnonneg]
      calc
        (n + 1 : ℝ) * besselI (n + 1) x = (x / 2) * (besselI n x - besselI (n + 2) x) := by
          rw [← hrec]
          ring
        _ ≤ (x / 2) * besselI n x := mul_le_mul_of_nonneg_left hsub (by positivity)
    exact Summable.of_nonneg_of_le (fun n => by positivity) hle ((besselI_summable hx).const_mul (x / 2))

/-- **The SU(2) Weyl character formula**: `e^(x·cos θ)·sin θ = Σₙ 2(n+1)Iₙ₊₁(x)/x · sin((n+1)θ)`. Termwise
differentiation of the Jacobi–Anger expansion (`hasDerivAt_tsum` with `besselI_mul_succ_summable`) gives
`−x·sin θ·e^(x·cos θ) = −2·Σ (n+1)Iₙ₊₁·sin((n+1)θ)`, so `sin θ·e^(x·cos θ) = (2/x)·Σ (n+1)Iₙ₊₁·sin((n+1)θ)`. This
is the symmetric (class-function) character expansion of the SU(2) heat kernel — the block-spin average's clean
coupling-advance identity. -/
theorem weyl_character_formula (x : ℝ) (hx : 0 < x) (θ : ℝ) :
    Real.exp (x * Real.cos θ) * Real.sin θ = ∑' n : ℕ, (2 * (n + 1 : ℝ) / x) * besselI (n + 1) x * Real.sin ((n + 1 : ℝ) * θ) := by
  have htsum : HasDerivAt (fun z : ℝ => ∑' n : ℕ, besselI (n + 1) x * Real.cos ((n + 1 : ℝ) * z))
      (∑' n : ℕ, -((n + 1 : ℝ) * besselI (n + 1) x) * Real.sin ((n + 1 : ℝ) * z)) θ := by
    refine hasDerivAt_tsum (u := fun n => (n + 1 : ℝ) * besselI (n + 1) x) (besselI_mul_succ_summable x (le_of_lt hx)) ?_ ?_ ?_ θ
    · intro n y
      have hcos : HasDerivAt (fun z : ℝ => Real.cos ((n + 1 : ℝ) * z)) (-((n + 1 : ℝ) * Real.sin ((n + 1 : ℝ) * y))) y := by
        simpa [mul_comm] using (Real.hasDerivAt_cos ((n + 1 : ℝ) * y)).comp y (hasDerivAt_const_mul (n + 1 : ℝ) y (hasDerivAt_id y))
      exact hcos.const_mul (besselI (n + 1) x)
    · intro n y
      have hnonneg : 0 ≤ (n + 1 : ℝ) * besselI (n + 1) x := mul_nonneg (by positivity) (besselI_nonneg (n := n + 1) (le_of_lt hx))
      rw [Real.norm_eq_abs]
      have h : |-(n + 1 : ℝ) * besselI (n + 1) x * Real.sin ((n + 1 : ℝ) * y)| ≤ (n + 1 : ℝ) * besselI (n + 1) x := by
        calc |-(n + 1 : ℝ) * besselI (n + 1) x * Real.sin ((n + 1 : ℝ) * y)|
            = |(n + 1 : ℝ) * besselI (n + 1) x| * |Real.sin ((n + 1 : ℝ) * y)| := by rw [abs_mul, abs_neg]
            _ ≤ (n + 1 : ℝ) * besselI (n + 1) x * 1 := mul_le_mul (le_of_eq (abs_of_nonneg hnonneg)) (Real.abs_sin_le_one ((n + 1 : ℝ) * y)) (abs_nonneg _) hnonneg
            _ = (n + 1 : ℝ) * besselI (n + 1) x := by ring
      exact h
    · exact (besselI_summable (le_of_lt hx)).comp_injective Nat.succ_injective
  have hexp : HasDerivAt (fun z : ℝ => Real.exp (x * Real.cos z)) (-(x * Real.sin θ) * Real.exp (x * Real.cos θ)) θ := by
    have hcos : HasDerivAt (fun z : ℝ => x * Real.cos z) (-(x * Real.sin θ)) θ := by
      simpa [mul_comm] using (Real.hasDerivAt_cos θ).const_mul x
    exact (Real.hasDerivAt_exp (x * Real.cos θ)).comp θ hcos
  have hderivR : HasDerivAt (fun z : ℝ => besselI 0 x + 2 * ∑' n : ℕ, besselI (n + 1) x * Real.cos ((n + 1 : ℝ) * z))
      (-2 * ∑' n : ℕ, (n + 1 : ℝ) * besselI (n + 1) x * Real.sin ((n + 1 : ℝ) * θ)) θ := by
    have hsum := htsum.const_mul 2
    have hconst : HasDerivAt (fun z : ℝ => besselI 0 x) 0 θ := hasDerivAt_const θ (besselI 0 x)
    have hsum' : HasDerivAt (fun z : ℝ => 2 * ∑' n : ℕ, besselI (n + 1) x * Real.cos ((n + 1 : ℝ) * z))
        (2 * ∑' n : ℕ, -((n + 1 : ℝ) * besselI (n + 1) x) * Real.sin ((n + 1 : ℝ) * z)) θ := by
      simpa using (htsum.const_mul 2)
    convert hconst.add hsum' using 1
    · ext z
      ring
    · rw [← tsum_mul_left, ← tsum_mul_left]
      congr 1
      ext n
      ring
  have hderiv_eq : -(x * Real.sin θ) * Real.exp (x * Real.cos θ) = -2 * ∑' n : ℕ, (n + 1 : ℝ) * besselI (n + 1) x * Real.sin ((n + 1 : ℝ) * θ) := by
    have hfuneq : (fun z : ℝ => Real.exp (x * Real.cos z)) = fun z : ℝ => besselI 0 x + 2 * ∑' n : ℕ, besselI (n + 1) x * Real.cos ((n + 1 : ℝ) * z) := by
      funext z
      exact jacobi_anger_real x z
    exact (hexp.congr_of_eventuallyEq (Filter.Eventually.of_forall (fun z => congr_fun hfuneq z))).deriv.trans hderivR.deriv.symm
  -- -(x sin θ) e^{x cos θ} = -2∑ (n+1)I_{n+1} sin((n+1)θ)
  have hpos : x * Real.sin θ * Real.exp (x * Real.cos θ) = 2 * ∑' n : ℕ, (n + 1 : ℝ) * besselI (n + 1) x * Real.sin ((n + 1 : ℝ) * θ) := by
    nlinarith [hderiv_eq]
  -- sin θ e^{x cos θ} = (2/x)∑ (n+1)I_{n+1} sin((n+1)θ) = ∑ (2(n+1)/x) I_{n+1} sin
  rw [← hpos]
  ring_nf
  rw [mul_comm (x * Real.sin θ) (Real.exp (x * Real.cos θ))]
  -- actually need: (x sin θ) e = x·(sin θ e), so sin θ e = (1/x)(x sin θ e)
  have hmain : Real.exp (x * Real.cos θ) * Real.sin θ = (2 / x) * ∑' n : ℕ, (n + 1 : ℝ) * besselI (n + 1) x * Real.sin ((n + 1 : ℝ) * θ) := by
    rw [mul_comm]
    have hxsin : x * Real.sin θ * Real.exp (x * Real.cos θ) = x * (Real.exp (x * Real.cos θ) * Real.sin θ) := by ring
    rw [hxsin] at hpos
    nlinarith [hpos]
  rw [hmain]
  rw [← tsum_mul_left]
  congr 1
  ext n
  ring

/-- **The torus-diagonal n=1 SU(2) character convolution**: `∫₀^π cos(θ_A+θ₂)·cos(θ_B+θ₂)·sin²θ₂ dθ₂ =
(π/4)·cos(θ_A−θ_B) − (π/8)·cos(θ_A+θ_B)`. This is the single-link building block of the two-plaquette block-spin
integration (the odd link's `cos` appears in two plaquettes); the `cos(θ_A+θ_B)` term is the torus-diagonal
artifact that the full SU(2) φ-integration cancels. -/
theorem su2_char_conv_one (θ_A θ_B : ℝ) :
    ∫ θ₂ in (0 : ℝ)..Real.pi, Real.cos (θ_A + θ₂) * Real.cos (θ_B + θ₂) * (Real.sin θ₂)^2
      = (Real.pi / 4) * Real.cos (θ_A - θ_B) - (Real.pi / 8) * Real.cos (θ_A + θ_B) := by
  have hprod : ∀ θ₂ : ℝ, Real.cos (θ_A + θ₂) * Real.cos (θ_B + θ₂)
      = (Real.cos (θ_A - θ_B) + Real.cos (θ_A + θ_B + 2 * θ₂)) / 2 := by
    intro θ₂
    have hsum : Real.cos ((θ_A + θ₂) + (θ_B + θ₂)) + Real.cos ((θ_A + θ₂) - (θ_B + θ₂))
        = 2 * (Real.cos (θ_A + θ₂) * Real.cos (θ_B + θ₂)) := by
      nlinarith [Real.cos_add (θ_A + θ₂) (θ_B + θ₂), Real.cos_sub (θ_A + θ₂) (θ_B + θ₂)]
    have harg1 : (θ_A + θ₂) + (θ_B + θ₂) = θ_A + θ_B + 2 * θ₂ := by ring
    have harg2 : (θ_A + θ₂) - (θ_B + θ₂) = θ_A - θ_B := by ring
    rw [harg1, harg2] at hsum
    nlinarith [hsum]
  have hcongr : (fun θ₂ : ℝ => Real.cos (θ_A + θ₂) * Real.cos (θ_B + θ₂) * (Real.sin θ₂)^2)
      = fun θ₂ : ℝ => (Real.cos (θ_A - θ_B) + Real.cos (θ_A + θ_B + 2 * θ₂)) / 2 * (Real.sin θ₂)^2 := by
    funext θ₂
    rw [hprod θ₂]
  rw [hcongr]
  rw [intervalIntegral.integral_congr (fun θ₂ _ => by ring : ∀ θ₂, (Real.cos (θ_A - θ_B) + Real.cos (θ_A + θ_B + 2 * θ₂)) / 2 * (Real.sin θ₂)^2 = (Real.cos (θ_A - θ_B) * (Real.sin θ₂)^2 + Real.cos (θ_A + θ_B + 2 * θ₂) * (Real.sin θ₂)^2) / 2)]
  rw [intervalIntegral.integral_div, intervalIntegral.integral_add]
  · have hconst : ∫ θ₂ in (0 : ℝ)..Real.pi, Real.cos (θ_A - θ_B) * (Real.sin θ₂)^2 = Real.cos (θ_A - θ_B) * (Real.pi / 2) := by
      rw [intervalIntegral.integral_const_mul]
      have hnorm : ∫ θ₂ in (0 : ℝ)..Real.pi, (Real.sin θ₂)^2 = Real.pi / 2 := by
        simpa using su2_character_orthogonality_diag (n := 0)
      rw [hnorm]
    have hcos2 : ∫ θ₂ in (0 : ℝ)..Real.pi, Real.cos (θ_A + θ_B + 2 * θ₂) * (Real.sin θ₂)^2
        = Real.cos (θ_A + θ_B) * (-(Real.pi / 4)) := by
      have hdecomp : ∀ θ₂, Real.cos (θ_A + θ_B + 2 * θ₂) = Real.cos (θ_A + θ_B) * Real.cos (2 * θ₂) - Real.sin (θ_A + θ_B) * Real.sin (2 * θ₂) := by
        intro θ₂
        exact Real.cos_add (θ_A + θ_B) (2 * θ₂)
      rw [intervalIntegral.integral_congr (fun θ₂ _ => hdecomp θ₂)]
      rw [intervalIntegral.integral_congr (fun θ₂ _ => by ring : ∀ θ₂, (Real.cos (θ_A + θ_B) * Real.cos (2 * θ₂) - Real.sin (θ_A + θ_B) * Real.sin (2 * θ₂)) * (Real.sin θ₂)^2 = Real.cos (θ_A + θ_B) * (Real.cos (2 * θ₂) * (Real.sin θ₂)^2) - Real.sin (θ_A + θ_B) * (Real.sin (2 * θ₂) * (Real.sin θ₂)^2))]
      rw [intervalIntegral.integral_sub]
      · rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
        rw [su2_cos_two_moment]
        have hsin2 : ∫ θ₂ in (0 : ℝ)..Real.pi, Real.sin (2 * θ₂) * (Real.sin θ₂)^2 = 0 := by
          -- ∫ sin(2θ) sin²θ = 0 (n=2 even)
          have hprod2 : ∀ θ₂, Real.sin (2 * θ₂) * (Real.sin θ₂)^2 = (Real.sin (2 * θ₂) - Real.sin (2 * θ₂) * Real.cos (2 * θ₂)) / 2 := by
            intro θ₂
            rw [Real.sin_sq_eq_half_sub]
            ring_nf
          rw [intervalIntegral.integral_congr (fun θ₂ _ => hprod2 θ₂)]
          rw [intervalIntegral.integral_div, intervalIntegral.integral_sub]
          · have hsin : ∫ θ₂ in (0 : ℝ)..Real.pi, Real.sin (2 * θ₂) = 0 := by
              simpa using integral_sin_nat (n := 2) (by norm_num)
            have hsincos : ∫ θ₂ in (0 : ℝ)..Real.pi, Real.sin (2 * θ₂) * Real.cos (2 * θ₂) = 0 := by
              rw [intervalIntegral.integral_congr (fun θ₂ _ => by rw [Real.sin_mul_cos_eq_half_sin_two_mul])]
              -- ∫ sin(4θ)/2 = 0
              rw [intervalIntegral.integral_div]
              have h4 : ∫ θ₂ in (0 : ℝ)..Real.pi, Real.sin (4 * θ₂) = 0 := by
                simpa using integral_sin_nat (n := 4) (by norm_num)
              rw [h4]; norm_num
            rw [hsin, hsincos]; norm_num
          · exact (by continuity : Continuous (fun θ₂ : ℝ => Real.sin (2 * θ₂))).intervalIntegrable 0 Real.pi
          · exact (by continuity : Continuous (fun θ₂ : ℝ => Real.sin (2 * θ₂) * Real.cos (2 * θ₂))).intervalIntegrable 0 Real.pi
        rw [hsin2]
        ring
      · exact (by continuity : Continuous (fun θ₂ : ℝ => Real.cos (θ_A + θ_B) * (Real.cos (2 * θ₂) * (Real.sin θ₂)^2))).intervalIntegrable 0 Real.pi
      · exact (by continuity : Continuous (fun θ₂ : ℝ => Real.sin (θ_A + θ_B) * (Real.sin (2 * θ₂) * (Real.sin θ₂)^2))).intervalIntegrable 0 Real.pi
    rw [hconst, hcos2]
    ring
  · exact (by continuity : Continuous (fun θ₂ : ℝ => Real.cos (θ_A - θ_B) * (Real.sin θ₂)^2)).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ₂ : ℝ => Real.cos (θ_A + θ_B + 2 * θ₂) * (Real.sin θ₂)^2)).intervalIntegrable 0 Real.pi

/-- **The φ-angle cosine orthogonality**: `∫₀^{2π} cos(φ−φ_A)·cos(φ−φ_B) dφ = π·cos(φ_A−φ_B)`. The product-to-sum
`cos·cos = (cos(φ_A−φ_B) + cos(2φ−φ_A−φ_B))/2`, the constant integrates to `2π·cos(φ_A−φ_B)` and the full-period
cosine vanishes. This is the φ-integration primitive for the full SU(2) character convolution (which cancels the
torus-diagonal artifact). -/
theorem cos_phi_orthogonality (φ_A φ_B : ℝ) :
    ∫ φ in (0 : ℝ)..(2 * Real.pi), Real.cos (φ - φ_A) * Real.cos (φ - φ_B) = Real.pi * Real.cos (φ_A - φ_B) := by
  have hprod : ∀ φ : ℝ, Real.cos (φ - φ_A) * Real.cos (φ - φ_B)
      = (Real.cos (φ_A - φ_B) + Real.cos (2 * φ - φ_A - φ_B)) / 2 := by
    intro φ
    have hsum : Real.cos ((φ - φ_A) + (φ - φ_B)) + Real.cos ((φ - φ_A) - (φ - φ_B))
        = 2 * (Real.cos (φ - φ_A) * Real.cos (φ - φ_B)) := by
      nlinarith [Real.cos_add (φ - φ_A) (φ - φ_B), Real.cos_sub (φ - φ_A) (φ - φ_B)]
    have harg1 : (φ - φ_A) + (φ - φ_B) = 2 * φ - φ_A - φ_B := by ring
    have harg2 : (φ - φ_A) - (φ - φ_B) = φ_B - φ_A := by ring
    rw [harg1, harg2] at hsum
    rw [Real.cos_neg (φ_A - φ_B)] at hsum
    have hneg : φ_B - φ_A = -(φ_A - φ_B) := by ring
    rw [hneg, Real.cos_neg] at hsum
    nlinarith [hsum]
  rw [intervalIntegral.integral_congr (fun φ _ => hprod φ)]
  rw [intervalIntegral.integral_div, intervalIntegral.integral_add]
  · have hconst : ∫ φ in (0 : ℝ)..(2 * Real.pi), Real.cos (φ_A - φ_B) = 2 * Real.pi * Real.cos (φ_A - φ_B) := by
      rw [intervalIntegral.integral_const]
      ring
    have hcos2 : ∫ φ in (0 : ℝ)..(2 * Real.pi), Real.cos (2 * φ - φ_A - φ_B) = 0 := by
      -- full-period cosine: antiderivative sin(2φ−φ_A−φ_B)/2
      have hderiv : ∀ φ : ℝ, HasDerivAt (fun t : ℝ => Real.sin (2 * t - φ_A - φ_B) / 2) (Real.cos (2 * φ - φ_A - φ_B)) φ := by
        intro φ
        have hsin : HasDerivAt (fun t : ℝ => Real.sin (2 * t - φ_A - φ_B)) (2 * Real.cos (2 * φ - φ_A - φ_B)) φ := by
          have hlin : HasDerivAt (fun t : ℝ => 2 * t - φ_A - φ_B) 2 φ := by
            simpa using ((hasDerivAt_const_mul 2 φ (hasDerivAt_id φ)).sub (hasDerivAt_const φ (φ_A + φ_B)))
          exact (Real.hasDerivAt_sin (2 * φ - φ_A - φ_B)).comp φ hlin
        simpa using hsin.const_mul (1 / 2)
      rw [intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (by nlinarith [Real.pi_pos]) (by continuity) (fun φ hφ => hderiv φ)]
      have hπ : Real.sin (2 * (2 * Real.pi) - φ_A - φ_B) = Real.sin (2 * 0 - φ_A - φ_B) := by
        -- sin(4π − c) = sin(−c), since sin is 2π-periodic
        rw [show 2 * (2 * Real.pi) - φ_A - φ_B = (-φ_A - φ_B) + 4 * Real.pi by ring]
        rw [Real.sin_add_int_mul_two_pi 2]
        rw [show 2 * 0 - φ_A - φ_B = -φ_A - φ_B by ring]
      field_simp
      ring_nf
      exact sub_eq_zero.mpr (congrArg (fun x => x / 2) hπ)
    rw [hconst, hcos2]
    field_simp [show (2 : ℝ) ≠ 0 by norm_num]
    ring
  · exact (by continuity : Continuous (fun _ : ℝ => Real.cos (φ_A - φ_B))).intervalIntegrable 0 (2 * Real.pi)
  · exact (by continuity : Continuous (fun φ : ℝ => Real.cos (2 * φ - φ_A - φ_B))).intervalIntegrable 0 (2 * Real.pi)

/-- **The SU(2) pseudoreality scalar**: `(2/π)·∫₀^π cos(2θ)·sin²θ dθ = −1/2`. This is the coefficient of the
SU(2) identity `∫ V² dV = −I/2` (the fundamental rep's pseudoreality), since `Tr(V²) = 2cos(2θ)` and
`∫ Tr(V²) dV = (2/π)∫ 2cos(2θ)sin²θ = −1`. The key ingredient for the n=1 character convolution
`∫ χ₁(U₂A)χ₁(U₂B) dU₂ = χ₁(A⁻¹B)/2`. -/
theorem su2_pseudoreality_scalar :
    (2 / Real.pi) * ∫ θ in (0 : ℝ)..Real.pi, Real.cos (2 * θ) * (Real.sin θ)^2 = -(1 / 2) := by
  rw [su2_cos_two_moment]
  field_simp [Real.pi_ne_zero]
  ring

/-- **The trace form of the SU(2) pseudoreality**: `∫ Tr(V²) dV = −1` — the normalized Weyl integral of
`Tr(V²) = 2cos(2θ)` is `(2/π)·2·∫₀^π cos(2θ)sin²θ = −1`. The scalar half of `∫ V² dV = −I/2` (the Schur lemma
then gives the matrix form from this trace). -/
theorem su2_trace_sq_weyl_eq_neg_one :
    (2 / Real.pi) * ∫ θ in (0 : ℝ)..Real.pi, (2 * Real.cos (2 * θ)) * (Real.sin θ)^2 = -1 := by
  rw [su2_cos_two_moment]
  field_simp [Real.pi_ne_zero]
  ring

/-- **The scalar `∫ Tr(U₂) = 0`** (the `∫ U₂ dU₂ = 0` orthogonality's trace form): `(2/π)·∫₀^π cos θ·sin²θ = 0`.
`Tr(U₂) = 2cos θ`, and the `cos θ` Weyl moment vanishes (`su2_cos_moment_ne_two n=1`). The scalar half of the
Haar orthogonality `∫ U₂ dU₂ = 0` (the Schur lemma then gives the matrix form). -/
theorem su2_trace_weyl_eq_zero :
    (2 / Real.pi) * ∫ θ in (0 : ℝ)..Real.pi, Real.cos θ * (Real.sin θ)^2 = 0 := by
  rw [su2_cos_moment_ne_two (n := 1) (by norm_num) (by norm_num)]
  norm_num

/-- **The S³ moment `∫ x₀² = 1/4` in the Weyl form**: `(2/π)·∫₀^π cos²θ·sin²θ dθ = 1/4`. Via the product-to-sum
`cos²·sin² = (1−cos(4θ))/8` and `∫ cos(4θ) = 0`. The key S³ moment that (with `∫ x₀xᵢ = 0`) gives the matrix
pseudoreality `∫ V² dV = −I/2`. -/
theorem su2_cos_sq_weyl_moment :
    (2 / Real.pi) * ∫ θ in (0 : ℝ)..Real.pi, (Real.cos θ)^2 * (Real.sin θ)^2 = 1 / 4 := by
  have hprod : ∀ θ : ℝ, (Real.cos θ)^2 * (Real.sin θ)^2 = (1 - Real.cos (4 * θ)) / 8 := by
    intro θ
    rw [Real.cos_sq_eq_half_add, Real.sin_sq_eq_half_sub]
    rw [show 4 * θ = 2 * (2 * θ) by ring]
    rw [Real.cos_two_mul]
    ring
  rw [intervalIntegral.integral_congr (fun θ _ => hprod θ)]
  rw [intervalIntegral.integral_div]
  rw [intervalIntegral.integral_const, intervalIntegral.integral_sub]
  · have hcos4 : ∫ θ in (0 : ℝ)..Real.pi, Real.cos (4 * θ) = 0 := by
      simpa using integral_cos_of_ne_zero (n := 4) (by norm_num)
    rw [hcos4]
    field_simp [Real.pi_ne_zero]
    ring
  · exact (by continuity : Continuous (fun _ : ℝ => (1 : ℝ))).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ : ℝ => Real.cos (4 * θ))).intervalIntegrable 0 Real.pi

/-- **The full-period cosine integral**: `∫₀^{2π} cos φ dφ = 0` (the φ-integration primitive for the S³ odd
moment `∫ x₀xᵢ = 0`, which kills the trace-zero part of the quaternion square). -/
theorem integral_cos_full_period_zero : ∫ φ in (0 : ℝ)..(2 * Real.pi), Real.cos φ = 0 := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (by nlinarith [Real.pi_pos]) (by continuity)
    (fun φ _ => Real.hasDerivAt_sin φ)]
  rw [Real.sin_periodic 1]
  ring

/-- **The full-period sine integral**: `∫₀^{2π} sin φ dφ = 0` (the φ-integration primitive for the S³ odd
moment `∫ x₀xᵢ = 0`). -/
theorem integral_sin_full_period_zero : ∫ φ in (0 : ℝ)..(2 * Real.pi), Real.sin φ = 0 := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (by nlinarith [Real.pi_pos]) (by continuity)
    (fun φ _ => (Real.hasDerivAt_cos φ).neg)]
  rw [Real.cos_periodic 1]
  ring

/-- **The θ₂ odd moment**: `∫₀^π cos θ·sin θ dθ = 0` (the odd-function FTC `[sin²θ/2]₀^π`). The θ₂-direction
primitive for the S³ odd moment `∫ x₀xᵢ = 0` (which kills the trace-zero part `2ix₀(x⃗·σ⃗)` of the quaternion
square). -/
theorem integral_cos_mul_sin_zero : ∫ θ in (0 : ℝ)..Real.pi, Real.cos θ * Real.sin θ = 0 := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (le_of_lt Real.pi_pos) (by continuity)
    (fun θ _ => by
      -- d/dθ (sin²θ/2) = cos θ · sin θ
      have h : HasDerivAt (fun t : ℝ => (Real.sin t)^2 / 2) (Real.cos θ * Real.sin θ) θ := by
        have hsin : HasDerivAt (fun t : ℝ => (Real.sin t)^2) (2 * Real.sin θ * Real.cos θ) θ := by
          simpa [pow_two] using (Real.hasDerivAt_sin θ).mul (Real.hasDerivAt_sin θ)
        simpa [pow_two, mul_assoc, mul_comm, mul_left_comm] using hsin.const_mul (1 / 2)
      exact h)]
  rw [Real.sin_pi, Real.sin_zero]
  ring

/-- **The scalar part of the pseudoreality**: `(2/π)·∫₀^π (cos²θ − sin²θ)·sin²θ dθ = −1/2` — the Weyl integral of
the quaternion square's scalar coefficient `x₀²−|x⃗|² = cos²θ−sin²θ = cos(2θ)`. This is the scalar coefficient of
`∫ V² dV = −I/2` (the trace-zero part integrates to zero via the odd moments). -/
theorem su2_sq_scalar_weyl :
    (2 / Real.pi) * ∫ θ in (0 : ℝ)..Real.pi, ((Real.cos θ)^2 - (Real.sin θ)^2) * (Real.sin θ)^2 = -(1 / 2) := by
  rw [intervalIntegral.integral_congr (fun θ _ => by rw [Real.cos_sq_sub_sin_sq])]
  rw [su2_cos_two_moment]
  field_simp [Real.pi_ne_zero]
  ring

/-- **The S² area factor**: `∫₀^π sin θ dθ = 2` — the θ₂-direction normalization in the S³ spherical-coordinate
round measure `dV = (2/π)·sin²θ₁·sin θ₂ dθ₁ dθ₂ dφ`. -/
theorem integral_sin_eq_two : ∫ θ in (0 : ℝ)..Real.pi, Real.sin θ = 2 := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (le_of_lt Real.pi_pos) (by continuity)
    (fun θ _ => (Real.hasDerivAt_cos θ).neg)]
  rw [Real.cos_pi, Real.cos_zero]
  norm_num

/-- **The S² direction moment `∫ u₁ = 0`**: the u₁ = cos θ₂ direction function integrates to zero over S² (the
θ₂ odd moment `∫ cos θ·sin θ = 0`, times the φ-period). The primitive for the S³ odd moment `∫ x₀xᵢ = 0`. -/
theorem su2_direction_moment_u1 : ∫ φ in (0 : ℝ)..(2 * Real.pi), ∫ θ in (0 : ℝ)..Real.pi, Real.cos θ * Real.sin θ = 0 := by
  rw [intervalIntegral.integral_congr (fun φ _ => integral_cos_mul_sin_zero)]
  simp

/-- **The S² direction moment `∫ u₂ = 0`**: the u₂ = sin θ₂·cos φ direction function integrates to zero (the
full-period cos φ). The primitive for the S³ odd moment `∫ x₀xᵢ = 0`. -/
theorem su2_direction_moment_u2 : ∫ φ in (0 : ℝ)..(2 * Real.pi), ∫ θ in (0 : ℝ)..Real.pi, (Real.sin θ)^2 * Real.cos φ = 0 := by
  rw [intervalIntegral.integral_congr (fun φ _ => by rw [intervalIntegral.integral_const_mul]; simp)]
  rw [intervalIntegral.integral_congr (fun φ _ => by rw [integral_cos_full_period_zero]; norm_num)]
  simp

/-- **The S² direction moment `∫ u₃ = 0`**: the u₃ = sin θ₂·sin φ direction function integrates to zero (the
full-period sin φ). The primitive for the S³ odd moment `∫ x₀xᵢ = 0`. -/
theorem su2_direction_moment_u3 : ∫ φ in (0 : ℝ)..(2 * Real.pi), ∫ θ in (0 : ℝ)..Real.pi, (Real.sin θ)^2 * Real.sin φ = 0 := by
  rw [intervalIntegral.integral_congr (fun φ _ => by rw [intervalIntegral.integral_const_mul]; simp)]
  rw [intervalIntegral.integral_congr (fun φ _ => by rw [integral_sin_full_period_zero]; norm_num)]
  simp

/-- **The scalar part of the pseudoreality (nested)**: `∫₀^π∫₀^π∫₀^{2π} (cos²θ₁−sin²θ₁)·sin²θ₁·sin θ₂ dθ₁ dθ₂ dφ = −π²`.
The θ₁ Weyl moment `−π/4` (`su2_sq_scalar_weyl`) × the θ₂ factor `2` (`integral_sin_eq_two`) × the φ factor `2π`.
The scalar coefficient of the unnormalized matrix pseudoreality `∫ V² = −π²·I` (normalized: `−I/2`). -/
theorem su2_sq_scalar_nested :
    ∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        ((Real.cos θ₁)^2 - (Real.sin θ₁)^2) * (Real.sin θ₁)^2 * Real.sin θ₂ = -Real.pi ^ 2 := by
  -- the φ-integral is constant: ∫_0^{2π} dφ = 2π
  have hφ : ∀ θ₁ θ₂, ∫ φ in (0 : ℝ)..(2 * Real.pi),
      ((Real.cos θ₁)^2 - (Real.sin θ₁)^2) * (Real.sin θ₁)^2 * Real.sin θ₂
        = ((Real.cos θ₁)^2 - (Real.sin θ₁)^2) * (Real.sin θ₁)^2 * Real.sin θ₂ * (2 * Real.pi) := by
    intro θ₁ θ₂
    rw [intervalIntegral.integral_const_mul]
    rw [intervalIntegral.integral_const]
    ring
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => hφ θ₁ θ₂))]
  -- ∫ θ₂, (cos²−sin²)sin² sin θ₂ · 2π = (cos²−sin²)sin² · 2π · 2
  have hθ₂ : ∀ θ₁, ∫ θ₂ in (0 : ℝ)..Real.pi,
      ((Real.cos θ₁)^2 - (Real.sin θ₁)^2) * (Real.sin θ₁)^2 * Real.sin θ₂ * (2 * Real.pi)
        = ((Real.cos θ₁)^2 - (Real.sin θ₁)^2) * (Real.sin θ₁)^2 * (4 * Real.pi) := by
    intro θ₁
    rw [intervalIntegral.integral_const_mul]
    rw [intervalIntegral.integral_const_mul]
    rw [integral_sin_eq_two]
    ring
  rw [intervalIntegral.integral_congr (fun θ₁ _ => hθ₂ θ₁)]
  -- ∫ θ₁, (cos²−sin²)sin² · 4π = 4π · (−π/4) = −π²
  rw [intervalIntegral.integral_const_mul]
  rw [show ∫ θ₁ in (0 : ℝ)..Real.pi, ((Real.cos θ₁)^2 - (Real.sin θ₁)^2) * (Real.sin θ₁)^2 = -(Real.pi / 4) by
    -- (2/π)∫ = −1/2, so ∫ = −π/4
    have h := su2_sq_scalar_weyl
    -- h : (2/π) · ∫ = −1/2
    field_simp at h
    linarith]
  ring

/-- **The trace-zero odd moment (u₁, nested)**: `∫∫∫ cos θ₁·sin θ₁·cos θ₂·sin²θ₁·sin θ₂ = 0` — the θ₂ odd moment
kills the u₁ direction of the quaternion square's trace-zero part. -/
theorem su2_odd_moment_u1_nested :
    ∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        Real.cos θ₁ * Real.sin θ₁ * Real.cos θ₂ * (Real.sin θ₁)^2 * Real.sin θ₂ = 0 := by
  have hφ : ∀ θ₁ θ₂, ∫ φ in (0 : ℝ)..(2 * Real.pi),
      Real.cos θ₁ * Real.sin θ₁ * Real.cos θ₂ * (Real.sin θ₁)^2 * Real.sin θ₂
        = Real.cos θ₁ * Real.sin θ₁ * Real.cos θ₂ * (Real.sin θ₁)^2 * Real.sin θ₂ * (2 * Real.pi) := by
    intro θ₁ θ₂
    rw [intervalIntegral.integral_const]
    ring
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => hφ θ₁ θ₂))]
  have hθ₂ : ∀ θ₁, ∫ θ₂ in (0 : ℝ)..Real.pi,
      Real.cos θ₁ * Real.sin θ₁ * Real.cos θ₂ * (Real.sin θ₁)^2 * Real.sin θ₂ * (2 * Real.pi) = 0 := by
    intro θ₁
    rw [intervalIntegral.integral_const_mul]
    rw [show ∫ θ₂ in (0 : ℝ)..Real.pi, Real.cos θ₂ * Real.sin θ₂ = 0 by exact integral_cos_mul_sin_zero]
    ring
  rw [intervalIntegral.integral_congr (fun θ₁ _ => hθ₂ θ₁)]
  simp

/-- **The trace-zero odd moment (u₂, nested)**: `∫∫∫ cos θ₁·sin θ₁·sin θ₂·cos φ·sin²θ₁·sin θ₂ = 0` — the full-period
cos φ kills the u₂ direction. -/
theorem su2_odd_moment_u2_nested :
    ∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        Real.cos θ₁ * Real.sin θ₁ * Real.sin θ₂ * Real.cos φ * (Real.sin θ₁)^2 * Real.sin θ₂ = 0 := by
  have hφ : ∀ θ₁ θ₂, ∫ φ in (0 : ℝ)..(2 * Real.pi),
      Real.cos θ₁ * Real.sin θ₁ * Real.sin θ₂ * Real.cos φ * (Real.sin θ₁)^2 * Real.sin θ₂
        = Real.cos θ₁ * Real.sin θ₁ * (Real.sin θ₂)^2 * (Real.sin θ₁)^2 * ∫ φ in (0 : ℝ)..(2 * Real.pi), Real.cos φ := by
    intro θ₁ θ₂
    rw [intervalIntegral.integral_const_mul]
    ring_nf
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => hφ θ₁ θ₂))]
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => by rw [integral_cos_full_period_zero]; simp))]
  simp

/-- **The trace-zero odd moment (u₃, nested)**: `∫∫∫ cos θ₁·sin θ₁·sin θ₂·sin φ·sin²θ₁·sin θ₂ = 0` — the full-period
sin φ kills the u₃ direction. -/
theorem su2_odd_moment_u3_nested :
    ∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        Real.cos θ₁ * Real.sin θ₁ * Real.sin θ₂ * Real.sin φ * (Real.sin θ₁)^2 * Real.sin θ₂ = 0 := by
  have hφ : ∀ θ₁ θ₂, ∫ φ in (0 : ℝ)..(2 * Real.pi),
      Real.cos θ₁ * Real.sin θ₁ * Real.sin θ₂ * Real.sin φ * (Real.sin θ₁)^2 * Real.sin θ₂
        = Real.cos θ₁ * Real.sin θ₁ * (Real.sin θ₂)^2 * (Real.sin θ₁)^2 * ∫ φ in (0 : ℝ)..(2 * Real.pi), Real.sin φ := by
    intro θ₁ θ₂
    rw [intervalIntegral.integral_const_mul]
    ring_nf
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => hφ θ₁ θ₂))]
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => by rw [integral_sin_full_period_zero]; simp))]
  simp

/-- **The φ-period helper**: `∫₀^{2π} (A + B·sin φ) dφ = A·2π` for constants `A B : ℂ` (the sin term's full-period
integral vanishes). The clean φ-level linearity for the matrix pseudoreality's entry integral. -/
theorem integral_add_const_sin_period (A B : ℂ) :
    ∫ φ in (0 : ℝ)..(2 * Real.pi), (A + B * (Real.sin φ : ℂ)) = A * (2 * Real.pi : ℂ) := by
  rw [intervalIntegral.integral_add]
  · rw [intervalIntegral.integral_const]
    rw [intervalIntegral.integral_const_mul]
    rw [intervalIntegral.integral_ofReal]
    rw [integral_sin_full_period_zero]
    simp
  · exact (by continuity : Continuous (fun _ : ℝ => A)).intervalIntegrable 0 (2 * Real.pi)
  · exact (by continuity : Continuous (fun φ : ℝ => B * (Real.sin φ : ℂ))).intervalIntegrable 0 (2 * Real.pi)

/-- **The matrix pseudoreality's `(0,0)` entry**: `∫∫∫ (V²)₀₀·sin²θ₁·sin θ₂ = −π²`. The trace-zero u₃ term's
φ-integral vanishes (`integral_add_const_sin_period`), leaving the scalar coefficient (`su2_sq_scalar_nested`). -/
theorem su2_sphere_sq_entry_00_integral :
    ∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        ((su2SphereQuaternion θ₁ θ₂ φ)^2) 0 0 * (Real.sin θ₁)^2 * Real.sin θ₂ = -(Real.pi ^ 2 : ℂ) := by
  have hφ : ∀ θ₁ θ₂, ∫ φ in (0 : ℝ)..(2 * Real.pi),
      ((su2SphereQuaternion θ₁ θ₂ φ)^2) 0 0 * (Real.sin θ₁)^2 * Real.sin θ₂
        = (((Real.cos θ₁)^2 - (Real.sin θ₁)^2 : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂ * (2 * Real.pi) := by
    intro θ₁ θ₂
    have hpoint : ∀ φ ∈ Set.uIcc (0 : ℝ) (2 * Real.pi),
        ((su2SphereQuaternion θ₁ θ₂ φ)^2) 0 0 * (Real.sin θ₁)^2 * Real.sin θ₂
          = ((((Real.cos θ₁)^2 - (Real.sin θ₁)^2 : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂)
            + ((2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * (Real.sin θ₁ : ℂ) * (Real.sin θ₂ : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂) * (Real.sin φ : ℂ) := by
      intro φ hφin
      rw [su2_sphere_sq_entry_00 θ₁ θ₂ φ]
      ring_nf
      simp [Complex.ofReal_mul]
      ring
    rw [intervalIntegral.integral_congr hpoint]
    rw [integral_add_const_sin_period]
    ring
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => hφ θ₁ θ₂))]
  rw [intervalIntegral.integral_congr (fun θ₁ _ => by
    rw [intervalIntegral.integral_congr (fun θ₂ _ => by
      rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
      rw [integral_sin_eq_two]
      ring)]
    rw [intervalIntegral.integral_const_mul]
    rw [su2_sq_scalar_nested]
    ring)]

/-- **The φ-period helper (cosine)**: `∫₀^{2π} (A + B·cos φ) dφ = A·2π` for `A B : ℂ`. -/
theorem integral_add_const_cos_period (A B : ℂ) :
    ∫ φ in (0 : ℝ)..(2 * Real.pi), (A + B * (Real.cos φ : ℂ)) = A * (2 * Real.pi : ℂ) := by
  rw [intervalIntegral.integral_add]
  · rw [intervalIntegral.integral_const]
    rw [intervalIntegral.integral_const_mul]
    rw [intervalIntegral.integral_ofReal]
    rw [integral_cos_full_period_zero]
    simp
  · exact (by continuity : Continuous (fun _ : ℝ => A)).intervalIntegrable 0 (2 * Real.pi)
  · exact (by continuity : Continuous (fun φ : ℝ => B * (Real.cos φ : ℂ))).intervalIntegrable 0 (2 * Real.pi)

/-- **The matrix pseudoreality's `(1,1)` entry**: `∫∫∫ (V²)₁₁·sin²θ₁·sin θ₂ = −π²` (symmetric to the `(0,0)` entry). -/
theorem su2_sphere_sq_entry_11_integral :
    ∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        ((su2SphereQuaternion θ₁ θ₂ φ)^2) 1 1 * (Real.sin θ₁)^2 * Real.sin θ₂ = -(Real.pi ^ 2 : ℂ) := by
  have hφ : ∀ θ₁ θ₂, ∫ φ in (0 : ℝ)..(2 * Real.pi),
      ((su2SphereQuaternion θ₁ θ₂ φ)^2) 1 1 * (Real.sin θ₁)^2 * Real.sin θ₂
        = (((Real.cos θ₁)^2 - (Real.sin θ₁)^2 : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂ * (2 * Real.pi) := by
    intro θ₁ θ₂
    have hpoint : ∀ φ ∈ Set.uIcc (0 : ℝ) (2 * Real.pi),
        ((su2SphereQuaternion θ₁ θ₂ φ)^2) 1 1 * (Real.sin θ₁)^2 * Real.sin θ₂
          = ((((Real.cos θ₁)^2 - (Real.sin θ₁)^2 : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂)
            + (-(2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * (Real.sin θ₁ : ℂ) * (Real.sin θ₂ : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂) * (Real.sin φ : ℂ) := by
      intro φ hφin
      rw [su2_sphere_sq_entry_11 θ₁ θ₂ φ]
      ring_nf
      simp [Complex.ofReal_mul]
      ring
    rw [intervalIntegral.integral_congr hpoint]
    rw [integral_add_const_sin_period]
    ring
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => hφ θ₁ θ₂))]
  rw [intervalIntegral.integral_congr (fun θ₁ _ => by
    rw [intervalIntegral.integral_congr (fun θ₂ _ => by
      rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
      rw [integral_sin_eq_two]
      ring)]
    rw [intervalIntegral.integral_const_mul]
    rw [su2_sq_scalar_nested]
    ring)]

/-- **The matrix pseudoreality's `(0,1)` entry**: `∫∫∫ (V²)₀₁·sin²θ₁·sin θ₂ = 0` (the `cos φ` full-period and the
`cos θ₂·sin θ₂` odd moment both vanish). -/
theorem su2_sphere_sq_entry_01_integral :
    ∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        ((su2SphereQuaternion θ₁ θ₂ φ)^2) 0 1 * (Real.sin θ₁)^2 * Real.sin θ₂ = 0 := by
  have hφ : ∀ θ₁ θ₂, ∫ φ in (0 : ℝ)..(2 * Real.pi),
      ((su2SphereQuaternion θ₁ θ₂ φ)^2) 0 1 * (Real.sin θ₁)^2 * Real.sin θ₂
        = (2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.cos θ₂ : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂ * (2 * Real.pi) := by
    intro θ₁ θ₂
    have hpoint : ∀ φ ∈ Set.uIcc (0 : ℝ) (2 * Real.pi),
        ((su2SphereQuaternion θ₁ θ₂ φ)^2) 0 1 * (Real.sin θ₁)^2 * Real.sin θ₂
          = ((2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.cos θ₂ : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂)
            + ((2 : ℂ) * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.sin θ₂ : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂) * (Real.cos φ : ℂ) := by
      intro φ hφin
      rw [su2_sphere_sq_entry_01 θ₁ θ₂ φ]
      ring_nf
      simp [Complex.ofReal_mul]
      ring
    rw [intervalIntegral.integral_congr hpoint]
    rw [integral_add_const_cos_period]
    ring
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => hφ θ₁ θ₂))]
  rw [intervalIntegral.integral_congr (fun θ₁ _ => by
    rw [intervalIntegral.integral_congr (fun θ₂ _ => by
      rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
      rw [integral_cos_mul_sin_zero]
      ring)]
    simp)]

/-- **The matrix pseudoreality's `(1,0)` entry**: `∫∫∫ (V²)₁₀·sin²θ₁·sin θ₂ = 0` (symmetric to `(0,1)`). -/
theorem su2_sphere_sq_entry_10_integral :
    ∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        ((su2SphereQuaternion θ₁ θ₂ φ)^2) 1 0 * (Real.sin θ₁)^2 * Real.sin θ₂ = 0 := by
  have hφ : ∀ θ₁ θ₂, ∫ φ in (0 : ℝ)..(2 * Real.pi),
      ((su2SphereQuaternion θ₁ θ₂ φ)^2) 1 0 * (Real.sin θ₁)^2 * Real.sin θ₂
        = (2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.cos θ₂ : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂ * (2 * Real.pi) := by
    intro θ₁ θ₂
    have hpoint : ∀ φ ∈ Set.uIcc (0 : ℝ) (2 * Real.pi),
        ((su2SphereQuaternion θ₁ θ₂ φ)^2) 1 0 * (Real.sin θ₁)^2 * Real.sin θ₂
          = ((2 : ℂ) * Complex.I * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.cos θ₂ : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂)
            + (-(2 : ℂ) * (Real.cos θ₁ : ℂ) * ((Real.sin θ₁ * Real.sin θ₂ : ℝ) : ℂ) * (Real.sin θ₁)^2 * Real.sin θ₂) * (Real.cos φ : ℂ) := by
      intro φ hφin
      rw [su2_sphere_sq_entry_10 θ₁ θ₂ φ]
      ring_nf
      simp [Complex.ofReal_mul]
      ring
    rw [intervalIntegral.integral_congr hpoint]
    rw [integral_add_const_cos_period]
    ring
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => hφ θ₁ θ₂))]
  rw [intervalIntegral.integral_congr (fun θ₁ _ => by
    rw [intervalIntegral.integral_congr (fun θ₂ _ => by
      rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
      rw [integral_cos_mul_sin_zero]
      ring)]
    simp)]

/-- **The SU(2) matrix pseudoreality (unnormalized)**: `∫∫∫ V²·sin²θ₁·sin θ₂ = −π²·I`. Since the normalized round
measure is `(1/(2π²))·sin²θ₁·sin θ₂ dθ₁ dθ₂ dφ`, this is `∫ V² dV = −I/2`. All four entries assembled. -/
theorem su2_sphere_sq_integral :
    (∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        (su2SphereQuaternion θ₁ θ₂ φ)^2 * (Real.sin θ₁)^2 * Real.sin θ₂)
      = -(Real.pi ^ 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [intervalIntegral.integral_apply, smul_eq_mul, Matrix.one_apply_eq]
  · exact su2_sphere_sq_entry_00_integral
  · exact su2_sphere_sq_entry_01_integral
  · exact su2_sphere_sq_entry_10_integral
  · exact su2_sphere_sq_entry_11_integral

/-- **The direction moment `∫ cos²θ·sin θ = 2/3`**: the θ₂-integral for the S³ direction moment `∫ x₁² = 1/4`
(FTC `[−cos³θ/3]₀^π`). -/
theorem integral_cos_sq_sin : ∫ θ in (0 : ℝ)..Real.pi, (Real.cos θ)^2 * Real.sin θ = 2 / 3 := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (le_of_lt Real.pi_pos) (by continuity)
    (fun θ _ => by
      have h : HasDerivAt (fun t : ℝ => -(Real.cos t)^3 / 3) ((Real.cos θ)^2 * Real.sin θ) θ := by
        have hcos : HasDerivAt (fun t : ℝ => (Real.cos t)^3) (3 * (Real.cos θ)^2 * (-Real.sin θ)) θ := by
          simpa [pow_two] using (Real.hasDerivAt_cos θ).pow 3
        simpa [pow_two, pow_succ, mul_assoc, mul_comm, mul_left_comm] using hcos.const_mul (-(1 / 3))
      exact h)]
  rw [Real.cos_pi, Real.cos_zero]
  norm_num

/-- **The θ₁ moment `∫ sin⁴θ = 3π/8`**: the θ₁-integral for the S³ direction moment (via `sin² = (1−cos 2θ)/2`). -/
theorem integral_sin_four : ∫ θ in (0 : ℝ)..Real.pi, (Real.sin θ)^4 = 3 * Real.pi / 8 := by
  rw [intervalIntegral.integral_congr (fun θ _ => by rw [Real.sin_sq_eq_half_sub]; ring_nf)]
  rw [intervalIntegral.integral_congr (fun θ _ => by
    rw [show (1 - Real.cos (2 * θ)) ^ 2 / 4 = (1 / 4) - (1 / 2) * Real.cos (2 * θ) + (1 / 4) * (Real.cos (2 * θ))^2 by ring_nf])]
  rw [intervalIntegral.integral_congr (fun θ _ => by rw [Real.cos_sq_eq_half_add]; ring_nf)]
  rw [intervalIntegral.integral_add, intervalIntegral.integral_add, intervalIntegral.integral_sub]
  · rw [intervalIntegral.integral_const]
    rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
    have hcos2 : ∫ θ in (0 : ℝ)..Real.pi, Real.cos (2 * θ) = 0 := by
      simpa using integral_cos_of_ne_zero (n := 2) (by norm_num)
    have hcos4 : ∫ θ in (0 : ℝ)..Real.pi, Real.cos (4 * θ) = 0 := by
      simpa using integral_cos_of_ne_zero (n := 4) (by norm_num)
    rw [hcos2, hcos4]
    field_simp [Real.pi_ne_zero]
    ring
  · exact (by continuity : Continuous (fun _ : ℝ => (1 / 4 : ℝ))).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ : ℝ => (1 / 4 : ℝ) * Real.cos (4 * θ))).intervalIntegrable 0 Real.pi
  · exact (by continuity : Continuous (fun θ : ℝ => (1 / 2 : ℝ) * Real.cos (2 * θ))).intervalIntegrable 0 Real.pi

/-- **The S³ direction moment `∫ x₁² = 1/4`**: the normalized S³ round-measure integral of `x₁² = sin²θ₁·cos²θ₂`.
Via the product-separable Fubini: `(1/(2π²))·2π·(2/3)·(3π/8) = 1/4`. The diagonal direction moment for the general
pseudoreality `∫U₂BU₂ = (B−Tr(B)I)/2`. -/
theorem su2_direction_moment_x1_sq :
    (1 / (2 * Real.pi ^ 2)) * ∫ θ₁ in (0 : ℝ)..Real.pi, ∫ θ₂ in (0 : ℝ)..Real.pi, ∫ φ in (0 : ℝ)..(2 * Real.pi),
        (Real.sin θ₁)^2 * (Real.cos θ₂)^2 * (Real.sin θ₁)^2 * Real.sin θ₂ = 1 / 4 := by
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ =>
    intervalIntegral.integral_const_mul))]
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ =>
    intervalIntegral.integral_const))]
  rw [intervalIntegral.integral_congr (fun θ₁ _ => intervalIntegral.integral_congr (fun θ₂ _ => by ring))]
  rw [intervalIntegral.integral_congr (fun θ₁ _ => by
    rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
    rw [integral_cos_sq_sin]
    ring)]
  rw [intervalIntegral.integral_const_mul]
  rw [integral_sin_four]
  field_simp [Real.pi_ne_zero]
  ring


