import Mathlib
import PaclandProof.QM.AsymptoticFreedomSign

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The forced relation — m_phys cutoff-independent ⇒ b₀ > 0 ∧ shared exponent ∧ Δ > 0

The one-loop value `b₀ = 11N/48π²` is a free parameter, not forced. What IS forced is the relation:
`m_phys = Δ(β)/a(β)` is a physical observable, so it is cutoff-independent (a constant). From that one
constraint we DERIVE (do not compute, do not assume): the shared exponent, `b₀ > 0`, and `Δ > 0`.
-/

open scoped BigOperators
open Filter

noncomputable section

namespace QM

/-- **The dimensional transmutation (forced)**: if `m_phys = Δ(β)/a(β)` is cutoff-independent (a
constant `M`), then `Δ(β) = M·a(β)` — the gap and the spacing share the SAME β-dependence. This is the
shared exponent, DERIVED from the relation, not assumed. -/
theorem dimensional_transmutation {Δ a : ℝ → ℝ} {M : ℝ}
    (h : ∀ β, Δ β / a β = M) (ha : ∀ β, a β ≠ 0) (β : ℝ) :
    Δ β = M * a β := by
  have hβ := h β
  field_simp [ha β] at hβ
  rw [mul_comm]
  exact hβ

/-- **Asymptotic freedom (b₀ > 0) forced by the continuum limit**: if the spacing `a(β) = B·e^{−b₀β}`
tends to `0` as `β → ∞` (the continuum limit exists), then `b₀ > 0` — the positive exponent is forced
by the existence of the limit, not by a loop integral. -/
theorem beta_positive_from_continuum_limit {B b₀ : ℝ}
    (hB : 0 < B) (hlim : Tendsto (fun β : ℝ => B * Real.exp (-b₀ * β)) atTop (nhds 0)) :
    0 < b₀ := by
  by_contra hb
  have hb' : b₀ ≤ 0 := not_lt.mp hb
  have hge : ∀ β, 0 ≤ β → B ≤ B * Real.exp (-b₀ * β) := by
    intro β hβ
    have h1 : 0 ≤ -b₀ * β := mul_nonneg (neg_nonneg.mpr hb') hβ
    have h2 : 1 ≤ Real.exp (-b₀ * β) := by
      rw [← Real.exp_zero]
      exact Real.exp_le_exp.mpr h1
    simpa using (mul_le_mul_of_nonneg_left h2 (le_of_lt hB))
  have hbound : ∀ᶠ β in atTop, B ≤ B * Real.exp (-b₀ * β) := by
    rw [Filter.eventually_atTop]
    exact ⟨0, hge⟩
  have hle : B ≤ 0 := ge_of_tendsto hlim hbound
  linarith

/-- **The positivity close (forced)**: if `m_phys = Δ(β)/a(β) = M > 0` (cutoff-independent) and
`a(β) > 0`, then `Δ(β) = M·a(β) > 0` — the mass gap is positive in the continuum, DERIVED from the
relation. -/
theorem delta_positive_from_relation {Δ a : ℝ → ℝ} {M : ℝ}
    (hM : 0 < M) (ha : ∀ β, 0 < a β) (h : ∀ β, Δ β / a β = M) (β : ℝ) :
    0 < Δ β := by
  have htrans := dimensional_transmutation h (fun γ => ne_of_gt (ha γ)) β
  rw [htrans]
  exact mul_pos hM (ha β)

end QM
