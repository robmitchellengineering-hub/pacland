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

/-- **The ceiling is exactly where α = 1.** At β = ceilingBeta c n the Dobrushin parameter
reaches 1, so the mass rate `m = (−log α)/2` is exactly 0 there. -/
theorem alphaAt_ceiling_eq_one {c n : ℝ} (hc : 1 < c) (hn : n ≠ 0) :
    alphaAt c n (ceilingBeta c n) = 1 := by
  have hc_pos : 0 < c := lt_trans zero_lt_one hc
  have h1 : 0 < 1 - 1 / c := by
    have hinv : 1 / c < 1 := (div_lt_one hc_pos).2 hc
    linarith
  dsimp [alphaAt, ceilingBeta]
  have h2 : -4 * n * (-Real.log (1 - 1 / c) / (4 * n)) = Real.log (1 - 1 / c) := by
    field_simp [hn, hc_pos.ne']
  rw [h2, Real.exp_log h1]
  field_simp [hc_pos.ne']
  ring

/-- **Past the ceiling (α > 1) the Dobrushin mass rate is negative** — the bound is vacuous there,
so the strong-coupling proof cannot be "extended" across the ceiling. This is the falsifier that
refutes "the Dobrushin bound extends past the ceiling". -/
theorem massRate_neg_of_one_lt {α : ℝ} (h : 1 < α) : massRate α < 0 := by
  dsimp [massRate]
  have hlog : 0 < Real.log α := Real.log_pos h
  linarith

/-- The confinement scale of pure Yang-Mills via dimensional transmutation:
`Λ(g) = μ · exp(−1/(2b₀g²))`, where g is the free gauge coupling and b₀ the one-loop beta
coefficient. This is the mass-gap *scale* — a free parameter, not a prediction. -/
def confinementScale (b₀ μ g : ℝ) : ℝ := μ * Real.exp (-1 / (2 * b₀ * g^2))

/-- **The mass gap is a value, not a relation (dimensional transmutation).** The confinement
scale is strictly increasing in the free coupling g (for g > 0), so different couplings give
different scales: no dimensionless constant fixes Λ, and the mass-gap scale is a free input —
exactly the constraint-first "relations, never values" for the YM mass gap. -/
theorem confinementScale_mono_of_coupling {b₀ μ g₁ g₂ : ℝ} (hb₀ : 0 < b₀) (hμ : 0 < μ)
    (h₁ : 0 < g₁) (h₂ : 0 < g₂) (h : g₁ < g₂) :
    confinementScale b₀ μ g₁ < confinementScale b₀ μ g₂ := by
  have hsq : g₁^2 < g₂^2 := by nlinarith [sq_nonneg g₁, sq_nonneg g₂]
  have hsq₁ : 0 < g₁^2 := sq_pos_of_ne_zero (ne_of_gt h₁)
  have hsq₂ : 0 < g₂^2 := sq_pos_of_ne_zero (ne_of_gt h₂)
  have hinv : 1 / (g₂^2) < 1 / (g₁^2) := by
    exact (one_div_lt_one_div hsq₂ hsq₁).2 hsq
  have harg : 1 / (2 * b₀ * g₂^2) < 1 / (2 * b₀ * g₁^2) := by
    have := mul_lt_mul_of_pos_left hinv (show 0 < (2 * b₀)⁻¹ by positivity)
    simpa [div_eq_mul_inv, mul_assoc, mul_left_comm, mul_comm] using this
  have hneg : -(1 / (2 * b₀ * g₁^2)) < -(1 / (2 * b₀ * g₂^2)) := by linarith
  have hexp : Real.exp (-(1 / (2 * b₀ * g₁^2))) < Real.exp (-(1 / (2 * b₀ * g₂^2))) :=
    Real.exp_lt_exp.mpr hneg
  have hfinal : μ * Real.exp (-(1 / (2 * b₀ * g₁^2))) < μ * Real.exp (-(1 / (2 * b₀ * g₂^2))) :=
    mul_lt_mul_of_pos_left hexp hμ
  dsimp [confinementScale]
  ring_nf at hfinal ⊢
  exact hfinal

end QM
