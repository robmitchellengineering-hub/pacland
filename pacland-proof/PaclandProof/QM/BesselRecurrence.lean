import Mathlib
import PaclandProof.QM.Bessel

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


