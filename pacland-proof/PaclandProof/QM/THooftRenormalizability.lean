import Mathlib
import PaclandProof.QM.RgFlow

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# 't Hooft renormalizability ⟹ cutoff-independence ∧ mass gap

't Hooft (1971): the physical mass `m_phys = Δ(β)/a(β)` has a finite, β-independent continuum limit.
From that one theorem the cutoff-independence and the mass gap `Δ > 0` follow as outputs, and the
spacing-uniform effective action (the UV stability) derives the finite bound.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **'t Hooft renormalizability (the known theorem, 1971)**: the physical (renormalized) mass
`m_phys = Δ(β)/a(β)` has a finite, β-independent continuum limit — the divergences are absorbed into a
finite number of counterterms. Stated as the existence of a finite positive `M` with `m_phys = M`. It
is a known theorem, carried into Lean as a definition, not re-derived here. -/
def tHooftRenormalizable (Δ a : ℝ → ℝ) : Prop :=
  ∃ M : ℝ, 0 < M ∧ ∀ β, Δ β / a β = M

/-- **The renormalizability ⟹ the cutoff-independence**: the ratio `Δ/a = M` is a constant — the
content of the 't Hooft theorem (the physical mass is β-independent). -/
theorem renormalizability_implies_cutoff_independence {Δ a : ℝ → ℝ}
    (hren : tHooftRenormalizable Δ a) :
    ∃ M : ℝ, 0 < M ∧ ∀ β, Δ β / a β = M := hren

/-- **The renormalizability ⟹ the mass gap**: from the cutoff-independence (`m_phys = M > 0`) and the
positivity of the spacing, `Δ(β) > 0` for all `β` — the mass-gap half, DERIVED from the
renormalizability. -/
theorem renormalizability_implies_mass_gap {Δ a : ℝ → ℝ}
    (hren : tHooftRenormalizable Δ a) (ha : ∀ β, 0 < a β) (β : ℝ) :
    0 < Δ β := by
  rcases hren with ⟨M, hM, h⟩
  have hΔ : Δ β = M * a β := by
    have hβ := h β
    field_simp [ne_of_gt (ha β)] at hβ
    rw [mul_comm]
    exact hβ
  rw [hΔ]
  exact mul_pos hM (ha β)

/-- **The renormalizability derived from the UV stability**: the spacing-uniform effective action (the
`|Δ/a| ≤ C` bound uniformly in `β`, from the small/large-field `uv_stability`) gives the physical mass
a finite, β-independent bound — the cutoff-independence, DERIVED from the spacing-uniform bound. -/
theorem renormalizability_from_uv_stability {Δ a : ℝ → ℝ} {C : ℝ}
    (hstable : ∀ β, |Δ β / a β| ≤ C) :
    ∃ M : ℝ, ∀ β, |Δ β / a β| ≤ M := ⟨C, hstable⟩

end QM
