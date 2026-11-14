import Mathlib

/-!
# The transfer-matrix spectral gap is monotone (the toy pattern the mass-gap proof needs)
-/

noncomputable section

namespace QM

/-- The mass gap of the 1D Ising transfer matrix: `m(β) = -log (tanh β)`. -/
def isingGap (β : ℝ) : ℝ := -Real.log (Real.tanh β)

/-- `tanh` is monotone increasing. -/
lemma tanh_mono {a b : ℝ} (hab : a ≤ b) : Real.tanh a ≤ Real.tanh b := by
  rw [Real.tanh_eq, Real.tanh_eq]
  have hden_a : 0 < Real.exp a + Real.exp (-a) := by positivity
  have hden_b : 0 < Real.exp b + Real.exp (-b) := by positivity
  rw [div_le_div_iff₀ hden_a hden_b]
  have hkey : (Real.exp a - Real.exp (-a)) * (Real.exp b + Real.exp (-b))
        - (Real.exp b - Real.exp (-b)) * (Real.exp a + Real.exp (-a))
        = 2 * (Real.exp (a - b) - Real.exp (b - a)) := by
    simp only [Real.exp_neg]
    simp only [Real.exp_sub]
    field_simp
    ring
  have h : Real.exp (a - b) ≤ Real.exp (b - a) := by
    rw [Real.exp_le_exp]
    linarith
  nlinarith [hkey, h]

/-- `tanh a > 0` for `a > 0`. -/
lemma tanh_pos {a : ℝ} (ha : 0 < a) : 0 < Real.tanh a := by
  rw [Real.tanh_eq]
  have h : Real.exp (-a) < Real.exp a := by
    rw [Real.exp_lt_exp]
    linarith
  have hden : 0 < Real.exp a + Real.exp (-a) := by positivity
  positivity

/-- **The transfer-matrix mass gap is monotone decreasing**: `0 < a ≤ b ⟹ m(b) ≤ m(a)`. -/
theorem isingGap_antitone {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) :
    isingGap b ≤ isingGap a := by
  dsimp [isingGap]
  apply neg_le_neg
  apply Real.log_le_log
  · exact tanh_pos ha
  · exact tanh_mono hab

end QM
