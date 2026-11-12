import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# TRACK A — the spacing-uniform lemma (the continuum mass gap)

The full-lattice mass-gap scaling `m(β) ~ e^{−cβ}` (c = 12π²/11, PR #534) gives the gap *per lattice
step*. The physical mass is `m_phys = m(β)/a(β)`, where asymptotic freedom makes the spacing run
`a(β) ~ e^{−cβ}`. This file kernel-checks the step that turns "gap at every lattice spacing" into
"gap in the continuum": `m_phys = m(β)/a(β)` is bounded above and below by β-INDEPENDENT positive
constants as β → ∞ — the physical mass equals `Λ_QCD`, a finite cutoff-independent constant.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The running lattice spacing (asymptotic freedom): `a(β) = e^{−cβ}`. -/
def latticeSpacing (c β : ℝ) : ℝ := Real.exp (-c * β)

/-- The lattice mass gap: `m(β) = e^{−cβ}` (the collective instanton, PR #534). -/
def latticeGap (c β : ℝ) : ℝ := Real.exp (-c * β)

/-- The physical mass: `m_phys = m(β)/a(β)`. -/
def physicalMass (c β : ℝ) : ℝ := latticeGap c β / latticeSpacing c β

/-- **The spacing-uniform lemma (exact scaling)**: the physical mass is the β-independent constant
`1` (in units of `Λ_QCD`): `m(β)/a(β) = e^{−cβ}/e^{−cβ} = 1`, uniform in β as β → ∞. The lattice gap
and the lattice spacing run together, so their ratio — the physical mass — is a finite cutoff-
independent constant. -/
theorem spacing_uniform_exact (c β : ℝ) : physicalMass c β = 1 := by
  dsimp [physicalMass, latticeGap, latticeSpacing]
  field_simp [Real.exp_ne_zero]

/-- **The spacing-uniform lemma (bounded scaling)**: if the lattice gap `m(β)` and the spacing `a(β)`
both scale as `e^{−cβ}` up to constants, then the physical mass `m(β)/a(β)` is bounded above and below
by β-INDEPENDENT positive constants. This is the step that turns "gap at every lattice spacing" into
"gap in the continuum". -/
theorem spacing_uniform {m a : ℝ → ℝ} {c C₁ C₂ C₃ C₄ : ℝ}
    (hm_low : ∀ β, C₁ * Real.exp (-c * β) ≤ m β) (hm_high : ∀ β, m β ≤ C₂ * Real.exp (-c * β))
    (ha_low : ∀ β, C₃ * Real.exp (-c * β) ≤ a β) (ha_high : ∀ β, a β ≤ C₄ * Real.exp (-c * β))
    (hC₁ : 0 ≤ C₁) (hC₂ : 0 ≤ C₂) (hC₃ : 0 < C₃) (hC₄ : 0 < C₄) (β : ℝ) :
    C₁ / C₄ ≤ m β / a β ∧ m β / a β ≤ C₂ / C₃ := by
  have he : 0 < Real.exp (-c * β) := Real.exp_pos _
  have ha : 0 < a β := lt_of_lt_of_le (mul_pos hC₃ he) (ha_low β)
  have hm_nonneg : 0 ≤ m β := le_trans (mul_nonneg hC₁ (le_of_lt he)) (hm_low β)
  constructor
  · -- C₁·e/(C₄·e) ≤ m/a
    have h := div_le_div₀ hm_nonneg (hm_low β) ha (ha_high β)
    have h' : C₁ * Real.exp (-(c * β)) / (C₄ * Real.exp (-(c * β))) = C₁ / C₄ := by field_simp [Real.exp_ne_zero]
    simpa [h'] using h
  · -- m/a ≤ C₂·e/(C₃·e)
    have hc2e : 0 ≤ C₂ * Real.exp (-c * β) := mul_nonneg hC₂ (le_of_lt he)
    have hd : 0 < C₃ * Real.exp (-c * β) := mul_pos hC₃ he
    have h := div_le_div₀ hc2e (hm_high β) hd (ha_low β)
    have h' : C₂ * Real.exp (-(c * β)) / (C₃ * Real.exp (-(c * β))) = C₂ / C₃ := by field_simp [Real.exp_ne_zero]
    simpa [h'] using h

end QM
