import Mathlib

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

end QM
