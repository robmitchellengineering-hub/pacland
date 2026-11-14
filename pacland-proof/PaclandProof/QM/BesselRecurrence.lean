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

end QM
