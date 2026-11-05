import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Cauchy's equation — the additive map, step by step

The Jordan–von Neumann ℝ-linearity step reduces to: an **additive** map
`ℝ → ℝ` that is **bounded on `[-1,1]`** is **ℝ-linear** (`a x = x · a 1`).
This file kernel-checks the clean first half: additivity alone forces
`a 0 = 0`, `a(-x) = -a x`, and `a n = n · a 1` for naturals — the ℕ/ℤ
homogeneity that the continuity/density half then extends to `ℝ`.
-/

noncomputable section

namespace Cauchy

/-- Additivity forces `a 0 = 0`. -/
theorem additive_zero (a : ℝ → ℝ) (hadd : ∀ x y, a (x + y) = a x + a y) :
    a 0 = 0 := by
  have h := hadd 0 0
  rw [show (0 : ℝ) + 0 = 0 by norm_num] at h
  linarith

/-- Additivity forces `a(-x) = -a x`. -/
theorem additive_neg (a : ℝ → ℝ) (hadd : ∀ x y, a (x + y) = a x + a y) :
    ∀ x, a (-x) = -a x := by
  intro x
  have h := hadd x (-x)
  have h0 : a 0 = 0 := additive_zero a hadd
  rw [show x + (-x) = 0 by ring] at h
  rw [h0] at h
  linarith

/-- Additivity forces `a n = n · a 1` for naturals. -/
theorem additive_nat (a : ℝ → ℝ) (hadd : ∀ x y, a (x + y) = a x + a y) :
    ∀ n : ℕ, a (n : ℝ) = (n : ℝ) * a 1 := by
  intro n
  induction n with
  | zero => simp [additive_zero a hadd]
  | succ n ih =>
      have hcast : (n : ℝ) + 1 = ((n + 1 : ℕ) : ℝ) := by norm_num
      calc
        a ((n + 1 : ℕ) : ℝ) = a ((n : ℝ) + 1) := by rw [hcast]
        _ = a (n : ℝ) + a 1 := hadd (n : ℝ) 1
        _ = (n : ℝ) * a 1 + a 1 := by rw [ih]
        _ = ((n + 1 : ℕ) : ℝ) * a 1 := by rw [← hcast]; ring

/-- Additivity forces `a(n • x) = n · a x` for naturals (the general form the
continuity proof needs, not just `x = 1`). -/
theorem additive_nsmul (a : ℝ → ℝ) (hadd : ∀ x y, a (x + y) = a x + a y) :
    ∀ n : ℕ, ∀ x, a (n • x) = (n : ℝ) * a x := by
  intro n
  induction n with
  | zero => intro x; simp [additive_zero a hadd]
  | succ n ih =>
      intro x
      have hcast : (n : ℝ) + 1 = ((n + 1 : ℕ) : ℝ) := by norm_num
      calc
        a ((n + 1 : ℕ) • x) = a (n • x + x) := by rfl
        _ = a (n • x) + a x := hadd (n • x) x
        _ = (n : ℝ) * a x + a x := by rw [ih x]
        _ = ((n + 1 : ℕ) : ℝ) * a x := by rw [← hcast]; ring

/-- Additivity + bounded on `[-1,1]` forces continuity at `0`. -/
theorem additive_continuousAt_zero_of_bounded (a : ℝ → ℝ)
    (hadd : ∀ x y, a (x + y) = a x + a y)
    (hbounded : ∃ M : ℝ, ∀ x, |x| ≤ 1 → |a x| ≤ M) :
    ContinuousAt a 0 := by
  rcases hbounded with ⟨M, hM⟩
  rw [Metric.continuousAt_iff]
  intro ε hε
  obtain ⟨n, hnpos, hn⟩ : ∃ n : ℕ, (0 : ℝ) < (n : ℝ) ∧ M / (n : ℝ) < ε := by
    by_cases hMle : M ≤ 0
    · refine ⟨1, by norm_num, ?_⟩
      simpa using lt_of_le_of_lt hMle hε
    · have hMpos : 0 < M := lt_of_not_ge hMle
      obtain ⟨n, hn⟩ := exists_nat_gt (M / ε)
      have hn0 : n ≠ 0 := by
        intro h0
        have hn' : M / ε < (0 : ℝ) := by simpa [h0] using hn
        linarith [div_pos hMpos hε]
      have hnpos' : (0 : ℝ) < (n : ℝ) := by
        exact_mod_cast (Nat.pos_of_ne_zero hn0)
      refine ⟨n, hnpos', ?_⟩
      rw [div_lt_iff₀ hε] at hn
      rw [div_lt_iff₀ hnpos']
      rw [mul_comm ε (n : ℝ)]
      exact hn
  refine ⟨1 / (n : ℝ), by positivity, ?_⟩
  intro x hx
  have hx' : |x| < 1 / (n : ℝ) := by
    simpa [Real.dist_eq] using hx
  have hnx : |(n : ℝ) * x| ≤ 1 := by
    calc
      |(n : ℝ) * x| = (n : ℝ) * |x| := by rw [abs_mul, abs_of_pos hnpos]
      _ ≤ (n : ℝ) * (1 / (n : ℝ)) := by
        exact mul_le_mul_of_nonneg_left (le_of_lt hx') (le_of_lt hnpos)
      _ = 1 := by field_simp [ne_of_gt hnpos]
  have hax : |a x| ≤ M / (n : ℝ) := by
    have h := additive_nsmul a hadd n x
    have hb : |a (n • x)| ≤ M := hM (n • x) (by simpa [nsmul_eq_mul] using hnx)
    rw [h] at hb
    rw [abs_mul, abs_of_pos hnpos] at hb
    have hb' : |a x| * (n : ℝ) ≤ M := by
      have hmc : (n : ℝ) * |a x| = |a x| * (n : ℝ) := mul_comm _ _
      rwa [hmc] at hb
    exact (le_div_iff₀ hnpos).2 hb'
  have haxlt : |a x| < ε := lt_of_le_of_lt hax hn
  simpa [Real.dist_eq, additive_zero a hadd] using haxlt

/-- Additivity + continuity at `0` forces continuity everywhere
(`a y − a x = a (y − x)` translates the neighbourhood). -/
theorem additive_continuous_of_continuousAt_zero (a : ℝ → ℝ)
    (hadd : ∀ x y, a (x + y) = a x + a y)
    (hcont0 : ContinuousAt a 0) :
    Continuous a := by
  rw [continuous_iff_continuousAt]
  intro x
  rw [Metric.continuousAt_iff]
  intro ε hε
  rcases (Metric.continuousAt_iff.mp hcont0) ε hε with ⟨δ, hδpos, hδ⟩
  refine ⟨δ, hδpos, ?_⟩
  intro y hy
  have hyx : |y - x| < δ := by
    simpa [Real.dist_eq] using hy
  have hay : |a (y - x)| < ε := by
    have hd : dist (y - x) 0 < δ := by simpa [Real.dist_eq] using hyx
    have h' := hδ hd
    simpa [Real.dist_eq, additive_zero a hadd] using h'
  have hdiff : a y - a x = a (y - x) := by
    have h := hadd x (y - x)
    have hxy : x + (y - x) = y := by ring
    rw [hxy] at h
    linarith
  simpa [Real.dist_eq, hdiff] using hay

end Cauchy

end
