import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The modified Bessel function (the coefficient in the SU(2) heat-kernel character expansion)

The physics input to the gauge-theory EKR certificate. The SU(2) Wilson heat kernel expands in
characters `exp(β·Tr U) = Σ_j (2j+1)·I_{2j+1}(2β)/β · χ_j(U)`, and the "small oscillation" /
positive-definiteness of the effective weight comes from the coefficients being non-negative. This
file defines the modified Bessel function `I_n` and proves the non-negativity.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The modified Bessel function of the first kind, integer order `n ≥ 0`:
`I_n(x) = Σ_k (x/2)^(2k+n) / (k! · (k+n)!)`. This is the coefficient function in the SU(2)
heat-kernel character expansion. -/
noncomputable def besselI (n : ℕ) (x : ℝ) : ℝ :=
  ∑' k : ℕ, (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)

/-- **Non-negativity of the modified Bessel function**: for `x ≥ 0`, every term in the series is
non-negative, so `I_n(x) ≥ 0`. This is the key positivity input to the character expansion — the
coefficients `(2j+1)·I_{2j+1}(2β)/β` are non-negative. -/
theorem besselI_nonneg {n : ℕ} {x : ℝ} (hx : 0 ≤ x) : 0 ≤ besselI n x := by
  dsimp [besselI]
  exact tsum_nonneg (by
    intro k
    exact div_nonneg (pow_nonneg (div_nonneg hx (by norm_num : 0 ≤ (2 : ℝ))) _)
      (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)))

/-- **The SU(2) character-expansion coefficient is non-negative**: `(2j+1)·I_{2j+1}(2β)/β ≥ 0` for
`β > 0`. This is the "positive-definite" / small-oscillation input that makes the Wilson heat kernel
a non-negative combination of characters. -/
theorem su2_coefficient_nonneg {j : ℕ} {β : ℝ} (hβ : 0 < β) :
    0 ≤ (2 * (j : ℝ) + 1) * besselI (2 * j + 1) (2 * β) / β := by
  have hI : 0 ≤ besselI (2 * j + 1) (2 * β) := besselI_nonneg (by nlinarith [hβ] : 0 ≤ 2 * β)
  have hnum : 0 ≤ (2 * (j : ℝ) + 1) * besselI (2 * j + 1) (2 * β) := by
    exact mul_nonneg (by nlinarith : 0 ≤ 2 * (j : ℝ) + 1) hI
  exact div_nonneg hnum (le_of_lt hβ)

/-- The Bessel series is summable for `x ≥ 0`: dominated by `(x/2)^n · exp((x/2)²)`. -/
theorem besselI_summable_of_nonneg (n : ℕ) {x : ℝ} (hx : 0 ≤ x) :
    Summable (fun k : ℕ => (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)) := by
  have hf : Summable (fun k : ℕ => (x / 2) ^ n * (((x / 2) ^ 2) ^ k / (k.factorial : ℝ))) := by
    exact (Real.summable_pow_div_factorial ((x / 2) ^ 2)).mul_left ((x / 2) ^ n)
  refine Summable.of_nonneg_of_le (fun k => ?_) (fun k => ?_) hf
  · exact div_nonneg (pow_nonneg (div_nonneg hx (by norm_num)) _)
      (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _))
  · have h1 : (k.factorial : ℝ) ≤ (k.factorial : ℝ) * (k + n).factorial := by
      have hfact : (1 : ℝ) ≤ (k + n).factorial := by exact_mod_cast (Nat.factorial_pos (k + n))
      nlinarith [mul_le_mul_of_nonneg_left hfact (Nat.cast_nonneg (k.factorial))]
    calc
      (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)
          ≤ (x / 2) ^ (2 * k + n) / (k.factorial : ℝ) := by
        exact div_le_div_of_nonneg_left (pow_nonneg (div_nonneg hx (by norm_num)) _) (Nat.cast_pos.mpr (Nat.factorial_pos k)) h1
      _ = (x / 2) ^ n * (((x / 2) ^ 2) ^ k / (k.factorial : ℝ)) := by
        rw [← pow_mul, pow_add]
        ring

/-- **Strict positivity of the modified Bessel function**: `I_n(x) > 0` for `x > 0` — the first
term `(x/2)^n/n!` is positive and the tail is non-negative. This is the strict positivity that makes
the SU(2) character coefficients genuinely positive (not just non-negative). -/
theorem besselI_pos {n : ℕ} {x : ℝ} (hx : 0 < x) : 0 < besselI n x := by
  dsimp [besselI]
  let a : ℕ → ℝ := fun k => (x / 2) ^ (2 * k + n) / ((k.factorial : ℝ) * (k + n).factorial)
  have hsum : Summable a := by
    dsimp [a]
    exact besselI_summable_of_nonneg n (le_of_lt hx)
  have hdecomp : (∑' k : ℕ, a k) = a 0 + ∑' k : ℕ, ite (k = 0) (0 : ℝ) (a k) :=
    Summable.tsum_eq_add_tsum_ite hsum (0 : ℕ)
  rw [hdecomp]
  have hfirst : 0 < a 0 := by
    dsimp [a]
    norm_num [Nat.factorial]
    exact div_pos (pow_pos (div_pos hx (by norm_num)) n) (Nat.cast_pos.mpr (Nat.factorial_pos n))
  have htail : 0 ≤ ∑' k : ℕ, ite (k = 0) (0 : ℝ) (a k) := by
    apply tsum_nonneg
    intro k
    split_ifs with hk
    · simp
    · dsimp [a]
      exact div_nonneg (pow_nonneg (div_nonneg (le_of_lt hx) (by norm_num)) _)
        (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _))
  exact add_pos_of_pos_of_nonneg hfirst htail

lemma complex_exp_eq_tsum_div (z : ℂ) :
    Complex.exp z = ∑' k : ℕ, z ^ k / (k.factorial : ℂ) := by
  rw [Complex.exp_eq_exp_ℂ, NormedSpace.exp_eq_tsum_div]

def diagInl (p : ℕ × ℕ) : ℕ × ℕ := (p.2 + p.1, p.2)
def diagInr (p : ℕ × ℕ) : ℕ × ℕ := (p.2, p.2 + p.1 + 1)

def diagEquiv : (ℕ × ℕ) ⊕ (ℕ × ℕ) ≃ ℕ × ℕ where
  toFun := Sum.elim diagInl diagInr
  invFun p := if p.2 ≤ p.1 then Sum.inl (p.1 - p.2, p.2) else Sum.inr (p.2 - p.1 - 1, p.1)
  left_inv := by
    intro s
    rcases s with ⟨n, l⟩ | ⟨m, k⟩
    · simp [diagInl]
    · simp [diagInr]
      omega
  right_inv := by
    intro p
    by_cases h : p.2 ≤ p.1
    · simp [h, diagInl]
    · have hp : p.1 < p.2 := Nat.lt_of_not_ge h
      simp [h, diagInr]
      ext <;> omega

lemma diagEquiv_inl (p : ℕ × ℕ) : diagEquiv (Sum.inl p) = diagInl p := rfl
lemma diagEquiv_inr (p : ℕ × ℕ) : diagEquiv (Sum.inr p) = diagInr p := rfl

def diagInlEquiv : ℕ × ℕ ≃ {z : ℕ × ℕ // z.2 ≤ z.1} where
  toFun p := ⟨diagInl p, by simp [diagInl]⟩
  invFun z := ⟨z.1.1 - z.1.2, z.1.2⟩
  left_inv := by
    intro p
    apply Prod.ext
    · simp [diagInl]
    · simp [diagInl]
  right_inv := by
    intro z
    apply Subtype.ext
    simp [diagInl]
    apply Prod.ext
    · exact Nat.add_sub_of_le z.2
    · rfl

def diagInrEquiv : ℕ × ℕ ≃ {z : ℕ × ℕ // z.1 < z.2} where
  toFun p := ⟨diagInr p, by simp [diagInr]⟩
  invFun z := ⟨z.1.2 - z.1.1 - 1, z.1.1⟩
  left_inv := by
    intro p
    apply Prod.ext
    · simp [diagInr]
      omega
    · simp [diagInr]
  right_inv := by
    intro z
    apply Subtype.ext
    simp [diagInr]
    apply Prod.ext
    · rfl
    · calc
        z.1.1 + (z.1.2 - z.1.1 - 1) + 1 = z.1.1 + (z.1.2 - (z.1.1 + 1)) + 1 := by rw [Nat.sub_sub]
        _ = (z.1.1 + 1) + (z.1.2 - (z.1.1 + 1)) := by omega
        _ = z.1.2 := Nat.add_sub_of_le (Nat.succ_le_of_lt z.2)

lemma tsum_mul_tsum_eq_diagonal (a b : ℕ → ℂ) (ha : Summable a) (hb : Summable b)
    (hfg : Summable (fun z : ℕ × ℕ => a z.1 * b z.2)) :
    (∑' k, a k) * (∑' l, b l) =
      (∑' n, ∑' l, a (l + n) * b l) + (∑' m, ∑' k, a k * b (k + m + 1)) := by
  rw [ha.tsum_mul_tsum hb hfg]
  rw [← diagEquiv.tsum_eq (fun z : ℕ × ℕ => a z.1 * b z.2)]
  have hsub1 : Summable (fun z : {z : ℕ × ℕ // z.2 ≤ z.1} => a z.1.1 * b z.1.2) :=
    hfg.subtype (fun z => z.2 ≤ z.1)
  have hsub2 : Summable (fun z : {z : ℕ × ℕ // z.1 < z.2} => a z.1.1 * b z.1.2) :=
    hfg.subtype (fun z => z.1 < z.2)
  have h1 : Summable (fun p : ℕ × ℕ => a (p.2 + p.1) * b p.2) := by
    have h := (diagInlEquiv.summable_iff (f := fun z : {z : ℕ × ℕ // z.2 ≤ z.1} => a z.1.1 * b z.1.2)).mpr hsub1
    convert h using 1
    funext p
    simp [diagInlEquiv, diagInl]
  have h2 : Summable (fun p : ℕ × ℕ => a p.2 * b (p.2 + p.1 + 1)) := by
    have h := (diagInrEquiv.summable_iff (f := fun z : {z : ℕ × ℕ // z.1 < z.2} => a z.1.1 * b z.1.2)).mpr hsub2
    convert h using 1
    funext p
    simp [diagInrEquiv, diagInr]
  calc
    (∑' c : (ℕ × ℕ) ⊕ (ℕ × ℕ), a (diagEquiv c).1 * b (diagEquiv c).2)
        = ∑' c : (ℕ × ℕ) ⊕ (ℕ × ℕ),
            Sum.elim (fun p : ℕ × ℕ => a (p.2 + p.1) * b p.2)
              (fun p : ℕ × ℕ => a p.2 * b (p.2 + p.1 + 1)) c := by
          apply tsum_congr
          intro c
          rcases c with p | p <;> simp [diagEquiv_inl, diagEquiv_inr, diagInl, diagInr]
        _ = (∑' p : ℕ × ℕ, a (p.2 + p.1) * b p.2) + (∑' p : ℕ × ℕ, a p.2 * b (p.2 + p.1 + 1)) := by
          exact (Summable.tsum_sum (f := Sum.elim (fun p : ℕ × ℕ => a (p.2 + p.1) * b p.2)
              (fun p : ℕ × ℕ => a p.2 * b (p.2 + p.1 + 1))) h1 h2)
        _ = (∑' n, ∑' l, a (l + n) * b l) + (∑' m, ∑' k, a k * b (k + m + 1)) := by
          rw [Summable.tsum_prod h1, Summable.tsum_prod h2]

lemma besselI_eq_tsum_cx (n : ℕ) (x : ℝ) :
    (besselI n x : ℂ) = ∑' l : ℕ, (x / 2 : ℂ) ^ (2 * l + n) / ((l.factorial : ℂ) * ((l + n).factorial : ℂ)) := by
  dsimp [besselI]
  rw [Complex.ofReal_tsum]
  apply tsum_congr
  intro l
  simp only [Complex.ofReal_div, Complex.ofReal_pow, Complex.ofReal_mul, Complex.ofReal_natCast]
  norm_num

lemma coeff_eq_left (x : ℝ) (z : ℂ) (n l : ℕ) (hz : z ≠ 0) :
    (((x / 2 : ℂ) * z) ^ (l + n) / ((l + n).factorial : ℂ)) *
        (((x / 2 : ℂ) * z⁻¹) ^ l / (l.factorial : ℂ)) =
      ((x / 2 : ℂ) ^ (2 * l + n) / ((l.factorial : ℂ) * ((l + n).factorial : ℂ))) * z ^ n := by
  rw [mul_pow, mul_pow]
  have hzpow : z ^ (l + n) * (z⁻¹) ^ l = z ^ n := by
    calc
      z ^ (l + n) * (z⁻¹) ^ l = z ^ l * z ^ n * (z⁻¹) ^ l := by rw [pow_add]
      _ = z ^ n * (z ^ l * (z⁻¹) ^ l) := by ring
      _ = z ^ n * (z * z⁻¹) ^ l := by rw [mul_pow]
      _ = z ^ n := by simp [mul_inv_cancel₀ hz]
  have hpowx : (x / 2 : ℂ) ^ (l + n) * (x / 2 : ℂ) ^ l = (x / 2 : ℂ) ^ (2 * l + n) := by
    rw [← pow_add]
    congr 1
    omega
  calc
    (x / 2 : ℂ) ^ (l + n) * z ^ (l + n) / ((l + n).factorial : ℂ) *
        ((x / 2 : ℂ) ^ l * (z⁻¹) ^ l / (l.factorial : ℂ))
        = ((x / 2 : ℂ) ^ (l + n) * (x / 2 : ℂ) ^ l) * (z ^ (l + n) * (z⁻¹) ^ l) /
            (((l + n).factorial : ℂ) * (l.factorial : ℂ)) := by ring
    _ = (x / 2 : ℂ) ^ (2 * l + n) * z ^ n / (((l + n).factorial : ℂ) * (l.factorial : ℂ)) := by
        rw [hpowx, hzpow]
    _ = (x / 2 : ℂ) ^ (2 * l + n) / ((l.factorial : ℂ) * ((l + n).factorial : ℂ)) * z ^ n := by ring

lemma coeff_eq_right (x : ℝ) (z : ℂ) (m k : ℕ) (hz : z ≠ 0) :
    (((x / 2 : ℂ) * z) ^ k / (k.factorial : ℂ)) *
        (((x / 2 : ℂ) * z⁻¹) ^ (k + m + 1) / ((k + m + 1).factorial : ℂ)) =
      ((x / 2 : ℂ) ^ (2 * k + (m + 1)) / ((k.factorial : ℂ) * ((k + (m + 1)).factorial : ℂ))) * z⁻¹ ^ (m + 1) := by
  rw [mul_pow, mul_pow]
  have hzpow : z ^ k * (z⁻¹) ^ (k + m + 1) = (z⁻¹) ^ (m + 1) := by
    calc
      z ^ k * (z⁻¹) ^ (k + m + 1) = z ^ k * ((z⁻¹) ^ k * (z⁻¹) ^ (m + 1)) := by
        rw [show k + m + 1 = k + (m + 1) by omega]
        rw [pow_add]
      _ = (z ^ k * (z⁻¹) ^ k) * (z⁻¹) ^ (m + 1) := by ring
      _ = (z * z⁻¹) ^ k * (z⁻¹) ^ (m + 1) := by rw [mul_pow]
      _ = (z⁻¹) ^ (m + 1) := by simp [mul_inv_cancel₀ hz]
  have hpowx : (x / 2 : ℂ) ^ k * (x / 2 : ℂ) ^ (k + m + 1) = (x / 2 : ℂ) ^ (2 * k + (m + 1)) := by
    rw [← pow_add]
    congr 1
    omega
  calc
    (x / 2 : ℂ) ^ k * z ^ k / (k.factorial : ℂ) *
        ((x / 2 : ℂ) ^ (k + m + 1) * (z⁻¹) ^ (k + m + 1) / ((k + m + 1).factorial : ℂ))
        = ((x / 2 : ℂ) ^ k * (x / 2 : ℂ) ^ (k + m + 1)) * (z ^ k * (z⁻¹) ^ (k + m + 1)) /
            ((k.factorial : ℂ) * ((k + m + 1).factorial : ℂ)) := by ring
    _ = (x / 2 : ℂ) ^ (2 * k + (m + 1)) * (z⁻¹) ^ (m + 1) /
            ((k.factorial : ℂ) * ((k + (m + 1)).factorial : ℂ)) := by
        rw [hpowx, hzpow]
        congr 1
    _ = (x / 2 : ℂ) ^ (2 * k + (m + 1)) / ((k.factorial : ℂ) * ((k + (m + 1)).factorial : ℂ)) * z⁻¹ ^ (m + 1) := by ring



lemma coeff_sum_left (x : ℝ) (z : ℂ) (n : ℕ) (hz : z ≠ 0) :
    ∑' l : ℕ, (((x / 2 : ℂ) * z) ^ (l + n) / ((l + n).factorial : ℂ)) *
        (((x / 2 : ℂ) * z⁻¹) ^ l / (l.factorial : ℂ)) =
      (besselI n x : ℂ) * z ^ n := by
  rw [tsum_congr (fun l => coeff_eq_left x z n l hz)]
  rw [tsum_mul_right]
  rw [← besselI_eq_tsum_cx n x]

lemma coeff_sum_right (x : ℝ) (z : ℂ) (m : ℕ) (hz : z ≠ 0) :
    ∑' k : ℕ, (((x / 2 : ℂ) * z) ^ k / (k.factorial : ℂ)) *
        (((x / 2 : ℂ) * z⁻¹) ^ (k + m + 1) / ((k + m + 1).factorial : ℂ)) =
      (besselI (m + 1) x : ℂ) * z⁻¹ ^ (m + 1) := by
  rw [tsum_congr (fun k => coeff_eq_right x z m k hz)]
  rw [tsum_mul_right]
  rw [← besselI_eq_tsum_cx (m + 1) x]

lemma besselI_generating (x : ℝ) (z : ℂ) (hz : z ≠ 0) :
    Complex.exp ((x / 2 : ℂ) * (z + z⁻¹)) =
      (besselI 0 x : ℂ) + ∑' n : ℕ, (besselI (n + 1) x : ℂ) * (z ^ (n + 1) + z⁻¹ ^ (n + 1)) := by
  let a : ℕ → ℂ := fun k => ((x / 2 : ℂ) * z) ^ k / (k.factorial : ℂ)
  let b : ℕ → ℂ := fun l => ((x / 2 : ℂ) * z⁻¹) ^ l / (l.factorial : ℂ)
  have ha : Summable a := by
    dsimp [a]
    exact NormedSpace.expSeries_div_summable ((x / 2 : ℂ) * z)
  have hb : Summable b := by
    dsimp [b]
    exact NormedSpace.expSeries_div_summable ((x / 2 : ℂ) * z⁻¹)
  have hfg : Summable (fun p : ℕ × ℕ => a p.1 * b p.2) := by
    apply summable_mul_of_summable_norm (f := a) (g := b)
    · dsimp [a]
      exact NormedSpace.norm_expSeries_div_summable ((x / 2 : ℂ) * z)
    · dsimp [b]
      exact NormedSpace.norm_expSeries_div_summable ((x / 2 : ℂ) * z⁻¹)
  have hc : Summable (fun n : ℕ => (besselI n x : ℂ) * z ^ n) := by
    have hG1 : Summable (fun p : ℕ × ℕ => a (p.2 + p.1) * b p.2) := by
      have hsub := hfg.subtype (fun q => q.2 ≤ q.1)
      have h := (diagInlEquiv.summable_iff (f := fun q : {q : ℕ × ℕ // q.2 ≤ q.1} => a q.1.1 * b q.1.2)).mpr hsub
      convert h using 1
      funext p
      simp [diagInlEquiv, diagInl]
    have houter := hG1.prod
    refine houter.congr ?_
    intro n
    dsimp [a, b]
    exact coeff_sum_left x z n hz
  have hd : Summable (fun n : ℕ => (besselI (n + 1) x : ℂ) * z⁻¹ ^ (n + 1)) := by
    have hG2 : Summable (fun p : ℕ × ℕ => a p.2 * b (p.2 + p.1 + 1)) := by
      have hsub := hfg.subtype (fun q => q.1 < q.2)
      have h := (diagInrEquiv.summable_iff (f := fun q : {q : ℕ × ℕ // q.1 < q.2} => a q.1.1 * b q.1.2)).mpr hsub
      convert h using 1
      funext p
      simp [diagInrEquiv, diagInr]
    have houter := hG2.prod
    refine houter.congr ?_
    intro n
    dsimp [a, b]
    exact coeff_sum_right x z n hz
  have hcsucc : Summable (fun n : ℕ => (besselI (n + 1) x : ℂ) * z ^ (n + 1)) :=
    (summable_nat_add_iff 1).mpr hc
  calc
    Complex.exp ((x / 2 : ℂ) * (z + z⁻¹))
        = Complex.exp ((x / 2 : ℂ) * z + (x / 2 : ℂ) * z⁻¹) := by rw [mul_add]
        _ = Complex.exp ((x / 2 : ℂ) * z) * Complex.exp ((x / 2 : ℂ) * z⁻¹) := Complex.exp_add _ _
        _ = (∑' k : ℕ, ((x / 2 : ℂ) * z) ^ k / (k.factorial : ℂ)) *
              (∑' l : ℕ, ((x / 2 : ℂ) * z⁻¹) ^ l / (l.factorial : ℂ)) := by
            rw [complex_exp_eq_tsum_div, complex_exp_eq_tsum_div]
        _ = (∑' n : ℕ, (besselI n x : ℂ) * z ^ n) + (∑' n : ℕ, (besselI (n + 1) x : ℂ) * z⁻¹ ^ (n + 1)) := by
            rw [tsum_mul_tsum_eq_diagonal a b ha hb hfg]
            congr 1
            · dsimp [a, b]; apply tsum_congr; intro n; exact coeff_sum_left x z n hz
            · dsimp [a, b]; apply tsum_congr; intro m; exact coeff_sum_right x z m hz
        _ = (besselI 0 x : ℂ) + ∑' n : ℕ, (besselI (n + 1) x : ℂ) * (z ^ (n + 1) + z⁻¹ ^ (n + 1)) := by
            rw [Summable.tsum_eq_zero_add hc]
            rw [add_assoc]
            rw [← Summable.tsum_add hcsucc hd]
            congr 1
            · simp
            · apply tsum_congr; intro n; ring



lemma exp_I_add_neg_eq_two_cos (u : ℂ) :
    Complex.exp (Complex.I * u) + Complex.exp (-(Complex.I * u)) = 2 * Complex.cos u := by
  rw [Complex.cos]
  have h1 : Complex.I * u = u * Complex.I := by ring
  have h2 : -(Complex.I * u) = -u * Complex.I := by ring
  rw [h2, h1]
  ring

lemma x_mul_cos_eq_ofReal (x θ : ℝ) :
    ((x * Real.cos θ : ℝ) : ℂ) = (x : ℂ) * Complex.cos (θ : ℂ) := by
  rw [Complex.ofReal_mul]
  rw [Complex.ofReal_cos θ]

lemma exp_nat_add_neg_eq_two_cos (θ : ℝ) (n : ℕ) :
    (Complex.exp (Complex.I * θ)) ^ (n + 1) + (Complex.exp (Complex.I * θ))⁻¹ ^ (n + 1) =
      2 * (Real.cos ((n + 1) * θ) : ℂ) := by
  rw [← Complex.exp_neg (Complex.I * θ)]
  rw [← Complex.exp_nat_mul (Complex.I * θ) (n + 1)]
  rw [← Complex.exp_nat_mul (-(Complex.I * θ)) (n + 1)]
  calc
    Complex.exp (((n + 1 : ℕ) : ℂ) * (Complex.I * (θ : ℂ))) + Complex.exp (((n + 1 : ℕ) : ℂ) * (-(Complex.I * (θ : ℂ))))
        = Complex.exp (Complex.I * (((n + 1 : ℕ) : ℂ) * (θ : ℂ))) + Complex.exp (-(Complex.I * (((n + 1 : ℕ) : ℂ) * (θ : ℂ)))) := by
            congr 2 <;> ring
        _ = 2 * Complex.cos (((n + 1 : ℕ) : ℂ) * (θ : ℂ)) := by
            exact exp_I_add_neg_eq_two_cos (((n + 1 : ℕ) : ℂ) * (θ : ℂ))
        _ = 2 * (Real.cos ((n + 1) * θ) : ℂ) := by
            norm_num [Complex.ofReal_cos, Complex.ofReal_mul, Complex.ofReal_natCast]



lemma jacobi_anger_complex_cos (x θ : ℝ) :
    Complex.exp ((x * Real.cos θ : ℝ) : ℂ) =
      (besselI 0 x : ℂ) + 2 * ∑' n : ℕ, (besselI (n + 1) x : ℂ) * (Real.cos ((n + 1) * θ) : ℂ) := by
  have hw : Complex.exp (Complex.I * θ) ≠ 0 := Complex.exp_ne_zero _
  have hgf := besselI_generating x (Complex.exp (Complex.I * θ)) hw
  have harg : ((x * Real.cos θ : ℝ) : ℂ) = (x / 2 : ℂ) * (Complex.exp (Complex.I * θ) + Complex.exp (-(Complex.I * θ))) := by
    calc
      ((x * Real.cos θ : ℝ) : ℂ) = (x : ℂ) * Complex.cos (θ : ℂ) := x_mul_cos_eq_ofReal x θ
      _ = (x / 2 : ℂ) * (2 * Complex.cos (θ : ℂ)) := by ring
      _ = (x / 2 : ℂ) * (Complex.exp (Complex.I * θ) + Complex.exp (-(Complex.I * θ))) := by
          rw [show 2 * Complex.cos (θ : ℂ) = Complex.exp (Complex.I * θ) + Complex.exp (-(Complex.I * θ)) by
            exact (exp_I_add_neg_eq_two_cos (θ : ℂ)).symm]
  calc
    Complex.exp ((x * Real.cos θ : ℝ) : ℂ)
        = Complex.exp ((x / 2 : ℂ) * (Complex.exp (Complex.I * θ) + Complex.exp (-(Complex.I * θ)))) := by rw [harg]
        _ = Complex.exp ((x / 2 : ℂ) * (Complex.exp (Complex.I * θ) + (Complex.exp (Complex.I * θ))⁻¹)) := by
            rw [Complex.exp_neg (Complex.I * θ)]
        _ = (besselI 0 x : ℂ) + ∑' n : ℕ, (besselI (n + 1) x : ℂ) * ((Complex.exp (Complex.I * θ)) ^ (n + 1) + (Complex.exp (Complex.I * θ))⁻¹ ^ (n + 1)) := by
            simpa using hgf
        _ = (besselI 0 x : ℂ) + 2 * ∑' n : ℕ, (besselI (n + 1) x : ℂ) * (Real.cos ((n + 1) * θ) : ℂ) := by
            congr 1
            calc
              ∑' n : ℕ, (besselI (n + 1) x : ℂ) * ((Complex.exp (Complex.I * θ)) ^ (n + 1) + (Complex.exp (Complex.I * θ))⁻¹ ^ (n + 1))
                  = ∑' n : ℕ, (besselI (n + 1) x : ℂ) * (2 * (Real.cos ((n + 1) * θ) : ℂ)) := by
                      apply tsum_congr; intro n; rw [exp_nat_add_neg_eq_two_cos θ n]
                  _ = ∑' n : ℕ, 2 * ((besselI (n + 1) x : ℂ) * (Real.cos ((n + 1) * θ) : ℂ)) := by
                      apply tsum_congr; intro n; ring
                  _ = 2 * ∑' n : ℕ, (besselI (n + 1) x : ℂ) * (Real.cos ((n + 1) * θ) : ℂ) := by
                      rw [tsum_mul_left]


/-- **Jacobi–Anger expansion (real form)** for the modified Bessel functions `Iₙ`:
`exp(x·cos θ) = I₀(x) + 2·Σₙ I_{n+1}(x)·cos((n+1)θ)`. Proved via the generating function
`exp((x/2)(t + t⁻¹)) = Σₙ Iₙ(x)(tⁿ + t⁻ⁿ)`: expand `exp(x·cos θ) = exp((x/2)e^{iθ})·exp((x/2)e^{-iθ})`,
take the Cauchy product of the two exponential series, and collect the coefficient of `e^{inθ}`. -/
theorem jacobi_anger_real (x θ : ℝ) :
    Real.exp (x * Real.cos θ) = besselI 0 x + 2 * ∑' n : ℕ, besselI (n + 1) x * Real.cos ((n + 1) * θ) := by
  apply Complex.ofReal_injective
  rw [Complex.ofReal_exp]
  rw [jacobi_anger_complex_cos x θ]
  simp only [Complex.ofReal_add, Complex.ofReal_mul, Complex.ofReal_tsum]
  norm_num

/-- **The Wilson heat kernel's Chebyshev expansion** — the Jacobi–Anger identity restated in the SU(2)/SO(3)
character basis: `exp(2β·cos θ) = Σₙ (2−δₙ₀)·Iₙ(2β)·Tₙ(cos θ)`, using `Tₙ(cos θ) = cos(nθ)` (Mathlib's
`Polynomial.Chebyshev.T_real_cos`). This is the representation-theory half of the `hΘ` measure→kernel
connection: the heat kernel is the reflected correlation of the all-mode Chebyshev observable
`W = Σₙ √((2−δₙ₀)·Iₙ(2β))·Tₙ`, whose positivity is the Chebyshev orthogonality (Mathlib) + `besselI_pos`. -/
theorem wilson_heat_kernel_chebyshev (β θ : ℝ) :
    Real.exp (2 * β * Real.cos θ)
      = besselI 0 (2 * β) * (Polynomial.Chebyshev.T ℝ 0).eval (Real.cos θ)
        + 2 * ∑' n : ℕ, besselI (n + 1) (2 * β) * (Polynomial.Chebyshev.T ℝ (n + 1)).eval (Real.cos θ) := by
  rw [jacobi_anger_real (2 * β) θ]
  congr 1
  · simp
  · congr 1
    apply tsum_congr
    intro n
    rw [Polynomial.Chebyshev.T_real_cos]
    norm_num

/-- **The `hΘ` character orthogonality (the real-name Peter–Weyl for the SU(2)/SO(3) trace)** — the
Chebyshev modes `Tₙ` are orthogonal under the Haar measure `measureT`: `∫ Tₙ·Tₘ ∂measureT = 0` for
`n ≠ m`. This is the *structured* Haar integral the measure→kernel connection reduces to, taken from
Mathlib's `Polynomial.Chebyshev` orthogonality rather than hand-rolled. -/
theorem hTheta_character_orthogonality_ne {n m : ℕ} (h : n ≠ m) :
    ∫ x, (Polynomial.Chebyshev.T ℝ n).eval x * (Polynomial.Chebyshev.T ℝ m).eval x
      ∂Polynomial.Chebyshev.measureT = 0 :=
  Polynomial.Chebyshev.integral_eval_T_real_mul_eval_T_real_measureT_of_ne h

/-- **The `hΘ` character norm** — `∫ Tₙ² ∂measureT = π/2` for `n ≠ 0` (the Chebyshev modes are normalized
up to `π/2` under the Haar measure). The second half of the orthogonality relation. -/
theorem hTheta_character_norm {n : ℕ} (hn : n ≠ 0) :
    ∫ x, (Polynomial.Chebyshev.T ℝ n).eval x * (Polynomial.Chebyshev.T ℝ n).eval x
      ∂Polynomial.Chebyshev.measureT = Real.pi / 2 :=
  Polynomial.Chebyshev.integral_T_real_mul_self_measureT_of_ne_zero hn

/-- **The `hΘ` character mean** — `∫ Tₙ ∂measureT = 0` for `n ≠ 0` (the non-constant Chebyshev modes have
zero Haar mean), the ingredient the von-Mises normalization integrates against. -/
theorem hTheta_character_mean {n : ℕ} (hn : n ≠ 0) :
    ∫ x, (Polynomial.Chebyshev.T ℝ n).eval x ∂Polynomial.Chebyshev.measureT = 0 :=
  Polynomial.Chebyshev.integral_eval_T_real_measureT_of_ne_zero (by omega : (n : ℤ) ≠ 0)

/-- **The `hΘ` two-variable rank-one decomposition** — the Wilson heat kernel factors into the positive
rank-one character modes: `exp(2β·cos(θᵢ−θⱼ)) = I₀(2β) + 2Σₙ Iₙ₊₁(2β)·(cos((n+1)θᵢ)cos((n+1)θⱼ) + sin((n+1)θᵢ)sin((n+1)θⱼ))`,
the Jacobi–Anger identity plus the cosine addition formula `cos(a−b) = cos a cos b + sin a sin b`. This is
the measure→kernel connection's concrete kernel — the all-mode observable's reflected correlation. -/
theorem wilson_heat_kernel_rank_one (β θi θj : ℝ) :
    Real.exp (2 * β * Real.cos (θi - θj)) =
      besselI 0 (2 * β) + 2 * ∑' n : ℕ, besselI (n + 1) (2 * β) *
        (Real.cos ((n + 1) * θi) * Real.cos ((n + 1) * θj) + Real.sin ((n + 1) * θi) * Real.sin ((n + 1) * θj)) := by
  rw [jacobi_anger_real (2 * β) (θi - θj)]
  congr 2
  apply tsum_congr
  intro n
  rw [show (n + 1 : ℝ) * (θi - θj) = (n + 1 : ℝ) * θi - (n + 1 : ℝ) * θj by ring]
  rw [Real.cos_sub]

/-- **The Fourier ingredient `∫₀^π cos(kθ) dθ = 0`** for `k ≠ 0` — via Mathlib's Chebyshev orthogonality
(the `integral_measureT_eq_integral_cos` change of variables plus `Tₖ(cos θ) = cos(kθ)`). -/
theorem integral_cos_of_ne_zero {k : ℕ} (hk : k ≠ 0) :
    ∫ θ in 0..Real.pi, Real.cos (k * θ) = 0 := by
  have h := Polynomial.Chebyshev.integral_eval_T_real_measureT_of_ne_zero (by omega : (k : ℤ) ≠ 0)
  rw [Polynomial.Chebyshev.integral_measureT_eq_integral_cos] at h
  simpa [Polynomial.Chebyshev.T_real_cos] using h

/-- **The ℤ Fourier ingredient `∫₀^π cos(kθ) dθ = 0`** for `k : ℤ ≠ 0` — the cosine's even symmetry
(`cos(−x) = cos x`) reduces the negative case to the ℕ case. -/
theorem integral_cos_of_ne_zero_int {k : ℤ} (hk : k ≠ 0) :
    ∫ θ in 0..Real.pi, Real.cos (k * θ) = 0 := by
  by_cases hkpos : 0 ≤ k
  · have hk' : Int.toNat k ≠ 0 := by
      rw [Int.toNat_eq_zero]
      omega
    have h := integral_cos_of_ne_zero hk'
    simpa [Int.toNat_of_nonneg hkpos] using h
  · have hkneg : k < 0 := by omega
    have hk' : Int.toNat (-k) ≠ 0 := by
      rw [Int.toNat_eq_zero]
      omega
    have h := integral_cos_of_ne_zero hk'
    rw [show (k : ℝ) * θ = -((-k : ℝ) * θ) by ring]
    rw [Real.cos_neg]
    simpa [Int.toNat_of_nonneg (by omega : 0 ≤ -k)] using h

end QM
