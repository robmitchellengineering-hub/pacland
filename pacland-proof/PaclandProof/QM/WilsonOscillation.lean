import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The small oscillation of the Wilson heat-kernel weight

The physics input to the Dobrushin/EKR influence bound (the "small oscillation" certificate). For a
compact gauge group the plaquette trace `Re Tr(U_p)` lies in `[-n, n]`, so the Wilson weight
`exp(β·Re Tr)` has log-oscillation bounded by `2nβ`. This is the exact quantity the tensor-RG
certificate (`weightOscillation` / `influenceBoundTensor` in lgt) needs: at small β (strong coupling)
the oscillation is small, which is why the Dobrushin method works there and fails as β grows.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The Wilson heat-kernel weight `exp(β·x)` for a real trace `x` (the `Re Tr(U_p)` of a plaquette). -/
def wilsonWeight (β x : ℝ) : ℝ := Real.exp (β * x)

/-- **The small oscillation of the Wilson weight**: for traces in `[-n, n]`, the log-ratio of the
weight at two points is bounded by `2nβ` — the "small oscillation" certificate that feeds the
Dobrushin/EKR influence bound. At small β (strong coupling) this oscillation is small. -/
theorem wilsonWeight_log_oscillation {β n x y : ℝ} (hβ : 0 ≤ β)
    (hx : |x| ≤ n) (hy : |y| ≤ n) :
    |Real.log (wilsonWeight β x / wilsonWeight β y)| ≤ 2 * n * β := by
  dsimp [wilsonWeight]
  have hxpos : Real.exp (β * x) ≠ 0 := ne_of_gt (Real.exp_pos _)
  have hypos : Real.exp (β * y) ≠ 0 := ne_of_gt (Real.exp_pos _)
  rw [Real.log_div hxpos hypos]
  rw [Real.log_exp, Real.log_exp]
  have hxy : |x - y| ≤ 2 * n := by
    have habs : |x + (-y)| ≤ |x| + |-y| := abs_add_le x (-y)
    have habs' : |x - y| ≤ |x| + |y| := by simpa [sub_eq_add_neg, abs_neg] using habs
    nlinarith [habs', hx, hy]
  have hmain : |β * x - β * y| ≤ 2 * n * β := by
    rw [← mul_sub]
    rw [abs_mul]
    rw [abs_of_nonneg hβ]
    nlinarith [mul_le_mul_of_nonneg_left hxy hβ]
  simpa [sub_eq_add_neg, mul_comm, mul_left_comm, mul_assoc] using hmain

end QM
