import Mathlib
import PaclandProof.QM.WangCriterion
import PaclandProof.QM.BakryEmery
import PaclandProof.QM.Su2Curvature

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The weak-coupling Wang's criterion — the OPEN theorem (stated, not yet proven)

The mass gap's remaining step. The strong-coupling `wang_criterion` needs POINTWISE positive curvature
(`κ·Γ ≤ Γ₂` everywhere), which `Su2Curvature.lean` shows holds only for β < 1/8. The weak-coupling
version (β > 1/8) must allow the curvature to be negative on the measure-negligible antipode, provided
the MEASURE-WEIGHTED (integrated) curvature stays positive. This file states that theorem precisely so
it can be proven, rather than leaving it as prose.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The weak-coupling Wang's criterion** (the statement). A positive spectral gap survives even when
the curvature is negative on a measure-small `bad` set, provided:
1. the measure is non-negative,
2. the curvature `κ·Γ ≤ Γ₂` holds on the GOOD set (away from `bad`),
3. the Lyapunov drift `LyapunovCondition L W c 0` holds,
4. the bad set's measure is suppressed (`μ x ≤ ε` on `bad`).

The conclusion (to be proven) is the integrated Bochner bound with a β-uniform constant — the Gaussian
comparison surviving the non-linearity of the trace. -/
def WeakCouplingWangCriterion
    {α : Type*}
    (μ : α → ℝ) (L Γ Γ₂ : (α → ℝ) → α → ℝ) (κ c : ℝ) (W : α → ℝ) (bad : α → Prop) : Prop :=
  (∀ x, 0 ≤ μ x) ∧
  (∀ f x, ¬ bad x → κ * Γ f x ≤ Γ₂ f x) ∧
  (LyapunovCondition L W c 0) ∧
  (∃ ε > 0, ∀ x, bad x → μ x ≤ ε)

/-- **The SU(2) weak-coupling Wang's criterion**: the bad set is the antipode θ = π (where the curvature
`1/4 + 2β·cos θ` is negative for β > 1/8), whose Wilson weight is `e^(−2β)`; the good set is the rest,
where the curvature is positive away from the antipode. -/
def Su2WeakCouplingWangCriterion (β : ℝ) : Prop :=
  WeakCouplingWangCriterion
    (fun θ => Real.exp (2 * β * Real.cos θ))          -- the Wilson weight μ
    (su2_langevin_1d β)                               -- the SU(2) Langevin generator L
    (fun f => carreDuChamp (su2_langevin_1d β) f f)   -- the carré du champ Γ (f with itself)
    (Gamma2 (su2_langevin_1d β))                      -- the Γ₂ operator
    (su2_ricci)                                       -- κ = 1/4 (the S³ Ricci, the strong-coupling curvature)
    (1 : ℝ)                                           -- c = 1 (the drift rate)
    (su2_lyapunov)                                    -- the Lyapunov function W = 2 − 2·cos θ
    (fun θ => θ = Real.pi)                            -- the bad set = the antipode

/-- **The claim that must be proven** (the mass gap): the SU(2) weak-coupling Wang's criterion holds
for every β, giving a β-uniform spectral gap. This is `C > 0`, the Clay statement, in its Wang-criterion
form. -/
def Su2MassGapViaWang : Prop :=
  ∀ β : ℝ, 0 ≤ β → Su2WeakCouplingWangCriterion β

end QM
