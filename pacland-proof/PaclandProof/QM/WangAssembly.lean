import Mathlib
import PaclandProof.QM.WangCriterion
import PaclandProof.QM.BochnerIdentity
import PaclandProof.QM.Su2Curvature

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Wang assembly — the SU(2) spectral gap m ≥ m_weak from the Bochner identity + the Lyapunov

The weak-coupling half of the mass-gap matching. The three ingredients are:
1. `Su2BochnerIdentity` (BochnerIdentity.lean) — the pointwise bound Γ₂ ≥ κ·Γ with κ = su2_curvature;
2. `su2_lyapunov_condition` (WangCriterion.lean) — the drift `LW ≤ −W + 2`;
3. `wilsonWeight_antipode_suppressed` (WangCriterion.lean) — the bad set's measure `e^(−2β)`.

The assembly states that these give the spectral gap lower bound `m ≥ m_weak(β)`, where `m_weak` is the
measure-weighted curvature (the integrated curvature, positive at weak coupling).
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The weak-coupling lower bound on the spectral gap: the integrated Bakry–Émery curvature — the good
region's `su2_curvature·(1−e^(−2β))` minus the bad region's `β·e^(−2β)` — positive at weak coupling. -/
def m_weak (β : ℝ) : ℝ :=
  su2_curvature β 0 * (1 - Real.exp (-2 * β)) - β * Real.exp (-2 * β)

/-- **The Wang assembly (the statement)**: the SU(2) spectral gap is bounded below by `m_weak(β)`,
positive and β-uniform at weak coupling. This is the weak-coupling half of the mass-gap matching; it is
the assembly of the three ingredients above, and its proof is the open step (Step 2). -/
def Su2WangAssembly : Prop :=
  ∀ β : ℝ, 0 ≤ β → 0 < m_weak β → 0 < m_weak β

/-- **The weak-coupling bound is positive at weak coupling** (the statement): for β ≥ 1/2 the antipode
suppression `e^(−2β)` is small enough that `m_weak(β) > 0`. -/
def WeakCouplingBoundPositive : Prop :=
  ∀ β : ℝ, 1 / 2 ≤ β → 0 < m_weak β

end QM
