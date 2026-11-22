import PaclandProof.QM.MassGapDiamond
import PaclandProof.QM.RefereeScalingLaw

/-! The two provable β-dependence sub-lemmas the churn loop grinds on.

These are the assembly steps between the (kernel-checked) transport bridge and the open
running-coupling rung — from `docs/PROOF-TARGETS.md`. The loop fills each `sorry` and the kernel
refuses it unless it is a real proof. -/

namespace ChurnTargets

open Real

/-- **The scaling-law bound is positive.** From `QM.refereeScalingLaw mGap` (a witness `A > 0` with
`A·e^{-(12π²/11)β} ≤ mGap β`), the mass gap `mGap β` is positive for every `β > 0`. This is the
positivity of the physical mass gap that the scaling law delivers. -/
theorem scaling_law_bound_positive {mGap : ℝ → ℝ} (h : QM.refereeScalingLaw mGap) (β : ℝ) (hβ : 0 < β) :
    0 < mGap β := by
  sorry

/-- **The running-coupling radius bound is positive.** The double exponential
`A·e^{-cβ}` is positive whenever `A > 0` — the `hpos` hypothesis the transport bridge
(`refereeScalingLaw_of_radius_bound`) needs to carry the radius bound to the scaling law. -/
theorem running_coupling_radius_positive {A c β : ℝ} (hA : 0 < A) :
    0 < A * Real.exp (-c * β) := by
  sorry

end ChurnTargets
