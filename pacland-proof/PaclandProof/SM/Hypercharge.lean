import Mathlib

/-!
# Standard-Model hypercharge uniqueness — the gauge-sector analog of Mitchell's Uniqueness

Mitchell's Uniqueness (flux): the tadpole `FᵀJH` is the *unique* bilinear symplectic
invariant — the constraint is the only exact structure. This file machine-checks the
gauge-sector analog, one sector up: given the SM matter content (gauge reps +
chirality), the **anomaly-cancellation conditions force the hypercharge assignment
uniquely**, up to overall normalization and the `u ↔ d` flavor swap — among solutions
with `Y_Q ≠ 0` (the physical electric-charge assignment; `Y_Q = 0` is an unphysical
anomaly-free branch `(0, t, −t, 0, 0)`, excluded).

The five hypercharges are `Y_Q, Y_u, Y_d, Y_L, Y_e` (per generation). The four
chirality-signed anomaly conditions are:

```
[grav]²U(1) :  6Y_Q − 3Y_u − 3Y_d + 2Y_L − Y_e = 0
[SU(2)]²U(1):  3Y_Q + Y_L = 0
[SU(3)]²U(1):  2Y_Q − Y_u − Y_d = 0
[U(1)]³     :  6Y_Q³ − 3Y_u³ − 3Y_d³ + 2Y_L³ − Y_e³ = 0
```

The three *linear* conditions leave a 2-dim family `(Y_L = −3Y_Q, Y_e = −6Y_Q,
Y_d = 2Y_Q − Y_u)`; the cubic `[U(1)]³` restricted to it factors as
`−18·Y_Q·(Y_u − 4Y_Q)(Y_u + 2Y_Q)`, so (with `Y_Q ≠ 0`) either `Y_u = 4Y_Q` (the SM,
`(1/6, 2/3, −1/3, −1/2, −1)`) or `Y_u = −2Y_Q` (the `u↔d` swap). QED.
-/

namespace SM

/-- The cubic `[U(1)]³` restricted to the linear-solution family factors as
`−18·Y_Q·(Y_u − 4Y_Q)(Y_u + 2Y_Q)`. -/
lemma cubic_reduced_factorization (YQ Yu : ℝ) :
    6*YQ^3 - 3*Yu^3 - 3*(2*YQ - Yu)^3 + 2*(-3*YQ)^3 - (-6*YQ)^3
      = -18 * YQ * ((Yu - 4*YQ) * (Yu + 2*YQ)) := by
  ring

/-- **SM hypercharge uniqueness.** The four anomaly-cancellation conditions determine the
hypercharge assignment uniquely up to overall scale (`Y_Q`) and the `u↔d` swap, among
solutions with `Y_Q ≠ 0`. -/
theorem hypercharge_uniqueness (YQ Yu Yd YL Ye : ℝ)
    (hgrav : 6*YQ - 3*Yu - 3*Yd + 2*YL - Ye = 0)
    (hsu2 : 3*YQ + YL = 0)
    (hsu3 : 2*YQ - Yu - Yd = 0)
    (hcubic : 6*YQ^3 - 3*Yu^3 - 3*Yd^3 + 2*YL^3 - Ye^3 = 0)
    (hYQ : YQ ≠ 0) :
    (Yu = 4*YQ ∧ Yd = -2*YQ ∧ YL = -3*YQ ∧ Ye = -6*YQ) ∨
    (Yu = -2*YQ ∧ Yd = 4*YQ ∧ YL = -3*YQ ∧ Ye = -6*YQ) := by
  -- Step 1: the three linear conditions solve for Y_L, Y_d, Y_e.
  have hYL : YL = -3*YQ := by nlinarith
  have hYd : Yd = 2*YQ - Yu := by nlinarith
  have hYe : Ye = -6*YQ := by nlinarith
  -- Step 2: the cubic restricted to the family factors.
  have hcubic' : -18 * YQ * ((Yu - 4*YQ) * (Yu + 2*YQ)) = 0 := by
    have hsub : 6*YQ^3 - 3*Yu^3 - 3*(2*YQ - Yu)^3 + 2*(-3*YQ)^3 - (-6*YQ)^3 = 0 := by
      rw [hYL, hYd, hYe] at hcubic
      exact hcubic
    rw [cubic_reduced_factorization YQ Yu] at hsub
    exact hsub
  -- Step 3: Y_Q ≠ 0 and −18 ≠ 0 leave the product of the two factors zero.
  have hprod : (Yu - 4*YQ) * (Yu + 2*YQ) = 0 := by
    have h18YQ : (-18 : ℝ) * YQ ≠ 0 := mul_ne_zero (by norm_num) hYQ
    have h := mul_eq_zero.mp hcubic'
    rcases h with h1 | h2
    · exfalso; exact h18YQ h1
    · exact h2
  rcases mul_eq_zero.mp hprod with h1 | h2
  · -- Yu = 4 Y_Q  →  the SM assignment
    have hYu : Yu = 4*YQ := by nlinarith
    left
    have hYd' : Yd = -2*YQ := by nlinarith [hYd, hYu]
    exact ⟨hYu, hYd', hYL, hYe⟩
  · -- Yu = −2 Y_Q  →  the u↔d swap
    have hYu : Yu = -2*YQ := by nlinarith
    right
    have hYd' : Yd = 4*YQ := by nlinarith [hYd, hYu]
    exact ⟨hYu, hYd', hYL, hYe⟩

end SM
