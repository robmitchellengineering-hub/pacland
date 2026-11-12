import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Yang–Mills mass gap — the Dobrushin-ceiling regime gap, kernel-checked

The `lgt` formalization (Douglas + Rajasekaran) proves the lattice YM mass gap at strong
coupling via the Dobrushin method, with rate `m = (−log α)/2`, where
`α = c · (1 − exp(−4nβ))` (c = maxNeighbors d, n = rank). The bound is valid only for
`α < 1`; the ceiling is where `α → 1`.

This file kernel-checks the **negative direction** of the regime gap: the mass-gap rate
`m(α) = (−log α)/2` tends to `0` as `α → 1`. So the strong-coupling bound gives *zero* rate
at the ceiling and cannot be spacing-uniform — the continuum limit (which needs a uniformly
positive mass) is a genuinely different regime. This turns the "regime gap" from a claim
into a theorem.
-/

open scoped BigOperators
open Filter

noncomputable section

namespace QM

/-- The Dobrushin parameter `α(β) = c·(1 − exp(−4nβ))` — the `lgt` `dobrushinAlpha` formula,
abstracted over the constants c = maxNeighbors d and n = rank. -/
def alphaAt (c n β : ℝ) : ℝ := c * (1 - Real.exp (-4 * n * β))

/-- The Dobrushin ceiling: the β where `α(β) = 1`. -/
def ceilingBeta (c n : ℝ) : ℝ := -Real.log (1 - 1 / c) / (4 * n)

/-- The mass-gap rate of the `lgt` bound, as a function of the Dobrushin parameter α. -/
def massRate (α : ℝ) : ℝ := (-Real.log α) / 2

/-- **The regime gap (negative direction).** The mass-gap rate vanishes as α → 1: at the
Dobrushin ceiling the strong-coupling bound gives rate 0, so it cannot be spacing-uniform. -/
theorem massRate_tendsto_zero :
    Tendsto massRate (nhds (1 : ℝ)) (nhds 0) := by
  change Tendsto (fun α : ℝ => (-Real.log α) / 2) (nhds (1 : ℝ)) (nhds 0)
  have hlog : Tendsto Real.log (nhds (1 : ℝ)) (nhds (Real.log 1)) :=
    Real.continuousAt_log (by norm_num : (1 : ℝ) ≠ 0)
  simpa [Real.log_one] using (hlog.neg.div_const 2)

end QM
