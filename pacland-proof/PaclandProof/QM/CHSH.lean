import Mathlib

/-!
# Bell's theorem — the CHSH inequality (the locality no-go)

The falsification rung that excludes *local* hidden variables. Alice has two measurement
settings `a0, a1`, Bob two `b0, b1`, each with outcome ±1. A local hidden-variable theory
assigns a definite value to each, so the CHSH correlation

    S = a0·b0 + a0·b1 + a1·b0 − a1·b1

must satisfy `S ≤ 2`. Quantum mechanics saturates `S = 2√2` (the Tsirelson bound), so
locality is falsified. Here we kernel-check the forced half: **no local assignment can
exceed 2** — both the deterministic ±1 case (by case analysis, `S = ±2`) and the general
local-realism case `|a|, |b| ≤ 1` (by the sharp two-point bound `|x+y| + |x−y| ≤ 2`).
-/

namespace QM

/-- The CHSH correlation value. -/
def chsh (a0 a1 b0 b1 : ℝ) : ℝ := a0*b0 + a0*b1 + a1*b0 - a1*b1

/-- **CHSH inequality (local bound).** For deterministic ±1 local hidden variables, `S ≤ 2`. -/
theorem chsh_local_bound (a0 a1 b0 b1 : ℝ)
    (ha0 : a0 = 1 ∨ a0 = -1) (ha1 : a1 = 1 ∨ a1 = -1)
    (hb0 : b0 = 1 ∨ b0 = -1) (hb1 : b1 = 1 ∨ b1 = -1) :
    chsh a0 a1 b0 b1 ≤ 2 := by
  dsimp [chsh]
  rcases ha0 with ha0 | ha0 <;> rcases ha1 with ha1 | ha1 <;>
    rcases hb0 with hb0 | hb0 <;> rcases hb1 with hb1 | hb1 <;>
    subst a0 <;> subst a1 <;> subst b0 <;> subst b1 <;> norm_num

/-- `|x+y| + |x-y| ≤ 2` for `|x|, |y| ≤ 1` (the sharp two-point bound). -/
lemma abs_add_abs_sub_le_two {x y : ℝ} (hx : |x| ≤ 1) (hy : |y| ≤ 1) :
    |x + y| + |x - y| ≤ 2 := by
  have hx1 : x ≤ 1 := (abs_le.mp hx).2
  have hxm1 : -1 ≤ x := (abs_le.mp hx).1
  have hy1 : y ≤ 1 := (abs_le.mp hy).2
  have hym1 : -1 ≤ y := (abs_le.mp hy).1
  -- |x-y| ≤ 2 - x - y  and  |x-y| ≤ 2 + x + y
  have hsub_le : |x - y| ≤ 2 - x - y := by
    rw [abs_sub_le_iff]
    constructor <;> nlinarith [hx1, hy1]
  have hsub_le2 : |x - y| ≤ 2 + x + y := by
    rw [abs_sub_le_iff]
    constructor <;> nlinarith [hxm1, hym1]
  -- |x+y| ≤ 2 - |x-y|
  have hxy : |x + y| ≤ 2 - |x - y| := by
    rw [abs_le]
    constructor
    · nlinarith [hsub_le2]
    · nlinarith [hsub_le]
  nlinarith [hxy]

/-- **CHSH inequality (general / local-realism bound).** For `|a|, |b| ≤ 1`, `S ≤ 2`. -/
theorem chsh_local_bound_general (a0 a1 b0 b1 : ℝ)
    (ha0 : |a0| ≤ 1) (ha1 : |a1| ≤ 1) (hb0 : |b0| ≤ 1) (hb1 : |b1| ≤ 1) :
    chsh a0 a1 b0 b1 ≤ 2 := by
  -- S = a0*(b0+b1) + a1*(b0-b1); bound each cross term by the corresponding |b ± b'|.
  have h1 : a0 * (b0 + b1) ≤ |b0 + b1| := by
    calc
      a0 * (b0 + b1) ≤ |a0 * (b0 + b1)| := le_abs_self _
      _ = |a0| * |b0 + b1| := abs_mul _ _
      _ ≤ |b0 + b1| := mul_le_of_le_one_left (abs_nonneg (b0 + b1)) ha0
  have h2 : a1 * (b0 - b1) ≤ |b0 - b1| := by
    calc
      a1 * (b0 - b1) ≤ |a1 * (b0 - b1)| := le_abs_self _
      _ = |a1| * |b0 - b1| := abs_mul _ _
      _ ≤ |b0 - b1| := mul_le_of_le_one_left (abs_nonneg (b0 - b1)) ha1
  have hsum : |b0 + b1| + |b0 - b1| ≤ 2 := abs_add_abs_sub_le_two hb0 hb1
  have hS : chsh a0 a1 b0 b1 = a0 * (b0 + b1) + a1 * (b0 - b1) := by dsimp [chsh]; ring
  rw [hS]
  nlinarith [h1, h2, hsum]

end QM
