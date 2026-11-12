import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The asymptotic-freedom hypothesis — the open step, stated precisely

The arc has localized the mass-gap problem to one named object: the collective soft mode (the
low-momentum gluon, PR #524), where the full-lattice drift `−4β·(Σ sin θ_p)²` vanishes. The compactness
of that mode gives the β-UNIFORM strong-coupling scale `λ = 1` (PR #525). The physical mass gap runs to
0 through that mode with the asymptotic-freedom scaling `e^{−cβ}` — this is the "new math" that no
literature crosses. This file states that hypothesis precisely and records its falsifier.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The asymptotic-freedom hypothesis (the open step)**: the physical mass gap `m(β)` is positive for
every finite `β` and is bounded below by `e^{−cβ}` for some `c > 0` — it vanishes no faster than the
exponential, and the physical (weak-coupling) scale is strictly smaller than the β-uniform compactness
scale `λ = 1` (PR #525). This is the hypothesis the whole arc has localized; it is falsifiable by the
lattice Monte-Carlo mass gap `m/σ ≈ 7–8` (the computed value, not a derived one). -/
def AsymptoticFreedom (m : ℝ → ℝ) (c : ℝ) : Prop :=
  (∀ β, 0 < m β) ∧ (∀ β, 0 ≤ β → Real.exp (-c * β) ≤ m β)

/-- **The hypothesis is falsifiable**: it makes a definite claim about every finite `β` — a single
`β₀` with `m(β₀) ≤ 0`, or a single `β₀ ≥ 0` with `m(β₀) < e^{−cβ₀}`, refutes it. -/
theorem asymptotic_freedom_falsifiable {m : ℝ → ℝ} {c : ℝ} :
    (∃ β, m β ≤ 0) ∨ (∃ β, 0 ≤ β ∧ m β < Real.exp (-c * β)) → ¬ AsymptoticFreedom m c := by
  intro h
  rintro ⟨hpos, hbound⟩
  rcases h with (⟨β, hβ⟩ | ⟨β, hβ0, hβ⟩)
  · exact lt_irrefl 0 (lt_of_lt_of_le (hpos β) hβ)
  · exact not_le_of_gt hβ (hbound β hβ0)

end QM
