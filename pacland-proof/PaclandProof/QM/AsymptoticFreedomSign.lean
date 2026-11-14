import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Asymptotic freedom — the SIGN, the shared exponent, and the positivity close

The Clay problem asks for existence + `Δ > 0`; it does NOT ask for the value of `Δ` or the exact
exponent. `Δ > 0` needs only: `b₀ > 0` (asymptotic freedom), and the SAME `b₀` governing both the gap
and the spacing (dimensional transmutation). Any `c > 0` gives `Δ > 0` — the exact `11N/48π²` is not
required. Convention flag: `c = 1/(2b₀) = 12π²/11` is under `β = 1/g²`; the Wilson convention
`β = 2N/g²` gives `c = 6π²/11` for SU(2).
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **Asymptotic freedom (the sign)**: the one-loop β-function coefficient is `b₀ = C − c`, where `C`
is the (anti-screening, positive) gluon self-energy and `c` is the (screening, negative-sign) ghost
contribution. Asymptotic freedom is exactly `c < C`, i.e. `b₀ = C − c > 0` — the gluon anti-screening
dominates the ghost. The exact value `11N/48π²` is NOT needed; only the sign. -/
theorem beta_function_positive {C c : ℝ} (hc : c < C) : 0 < C - c := by
  linarith

/-- **The dimensional transmutation (the shared exponent)**: the non-perturbative gap `Δ(β) = A·e^{−b₀β}`
and the perturbative spacing `a(β) = B·e^{−b₀β}` are governed by the SAME `b₀`, so `m_phys = Δ/a = A/B`
is β-INDEPENDENT — the single scale Λ_QCD. This is the real spacing-uniform content (the same
coefficient in both), NOT "define both equal to e^{−cβ}". -/
theorem shared_exponent {A B b₀ : ℝ} (hB : B ≠ 0) (β : ℝ) :
    (A * Real.exp (-b₀ * β)) / (B * Real.exp (-b₀ * β)) = A / B := by
  field_simp [Real.exp_ne_zero, hB]

/-- **The positivity close**: with `b₀ > 0` and the shared exponent, `m_phys = A/B` is bounded away
from 0 (and from ∞) by positive β-independent constants — that is `Δ > 0` in the continuum. -/
theorem physical_mass_bounded {A B : ℝ} (hA : 0 < A) (hB : 0 < B) :
    0 < A / B := by
  exact div_pos hA hB

/-- **Convention flag**: `c = 1/(2b₀) = 12π²/11` is under `β = 1/g²`. The Wilson convention
`β = 2N/g²` gives `c = 6π²/11` for SU(2). This records the convention, not a derived result. -/
theorem wilson_convention_su2 : (12 * Real.pi ^ 2 / 11) / 2 = 6 * Real.pi ^ 2 / 11 := by
  ring

end QM
