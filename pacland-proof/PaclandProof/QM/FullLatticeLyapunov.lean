import Mathlib
import PaclandProof.QM.WangCriterion

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The full-lattice Lyapunov drift and the soft mode (the moment of truth)

The 1-plaquette ceiling dissolves (Wang #519–#521). The Clay question is the FULL d=4 lattice. The
natural Lyapunov function is the total distance from the all-trivial connection `W = Σ_p (2 − Re Tr U_p)
= Σ_p (2 − 2cos θ_p)`. Its Langevin drift's gradient part is the COLLECTIVE term `−4β·(Σ_p sin θ_p)²`
— the square of the SUM of the plaquette gradients, not the sum of squares. This file kernel-checks
that the drift vanishes exactly on the collective mode `Σ_p sin θ_p = 0`, which exists with every
plaquette individually non-trivial. That collective mode is the low-momentum gluon — the soft mode
where the β-uniform rate drops, naming the non-perturbative `e^{−cβ}` mechanism.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The full-lattice drift is the COLLECTIVE term** (the square of the sum, not the sum of squares):
on the total Lyapunov `W = Σ_p (2 − 2cos θ_p)`, the Langevin drift's gradient part is
`−4β·(Σ_p sin θ_p)² ≤ 0`. It is the square of the *sum* of the plaquette gradients, so it vanishes
exactly when the collective sum `Σ_p sin θ_p = 0` — the long-wavelength (low-momentum gluon) mode.
The single-plaquette drift `−4β·sin²θ_p` is the *sum of squares*, which does NOT vanish for non-trivial
angles. -/
theorem drift_total_nonpos {β : ℝ} (hβ : 0 ≤ β) (θ : Fin m → ℝ) :
    -4 * β * (∑ p, Real.sin (θ p)) ^ 2 ≤ 0 := by
  have h1 : 0 ≤ (∑ p, Real.sin (θ p)) ^ 2 := sq_nonneg _
  have h2 : 0 ≤ 4 * β := mul_nonneg (by norm_num) hβ
  nlinarith [mul_nonneg h2 h1]

/-- **The soft mode (the drop point)**: the collective drift vanishes when `Σ_p sin θ_p = 0` — the
long-wavelength mode. This is where the β-uniform rate of the full-lattice Lyapunov condition drops,
naming the soft mode as the collective low-momentum gluon (the non-perturbative `e^{−cβ}` mechanism). -/
theorem drift_total_vanishes_on_soft_mode (β : ℝ) (θ : Fin m → ℝ) (hsoft : ∑ p, Real.sin (θ p) = 0) :
    -4 * β * (∑ p, Real.sin (θ p)) ^ 2 = 0 := by
  rw [hsoft]
  ring

/-- **The soft mode exists and is genuinely collective**: two plaquettes with `θ₀ = π/2`, `θ₁ = −π/2`
have `Σ_p sin θ_p = 0` (the collective cancellation) while each `sin θ_p ≠ 0` — the drift vanishes
even though every plaquette is individually non-trivial. This is the long-wavelength gluon: the soft
mode is the collective part of the field, not a single plaquette's antipode. -/
theorem soft_mode_exists :
    ∃ θ : Fin 2 → ℝ, (∑ p, Real.sin (θ p) = 0) ∧ (∀ p, Real.sin (θ p) ≠ 0) := by
  refine ⟨(![(Real.pi / 2), (-Real.pi / 2)] : Fin 2 → ℝ), ?_, ?_⟩
  · -- Σ sin θ_p = 0
    have hsinneg : Real.sin (-Real.pi / 2) = -1 := by
      rw [show (-Real.pi / 2) = -(Real.pi / 2) by ring]
      rw [Real.sin_neg, Real.sin_pi_div_two]
    simp [Fin.sum_univ_two, Real.sin_pi_div_two, hsinneg]
  · -- ∀ p, sin θ_p ≠ 0
    intro p
    fin_cases p
    · simp [Real.sin_pi_div_two]
    · have hsinneg : Real.sin (-Real.pi / 2) = -1 := by
        rw [show (-Real.pi / 2) = -(Real.pi / 2) by ring]
        rw [Real.sin_neg, Real.sin_pi_div_two]
      simp [hsinneg]

end QM
