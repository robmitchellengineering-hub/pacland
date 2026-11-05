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

end Cauchy

end
