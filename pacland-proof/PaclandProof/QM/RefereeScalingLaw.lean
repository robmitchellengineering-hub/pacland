import PaclandProof.QM.MassGapDiamond

/-! # The transport bridge: spectral radius → `refereeScalingLaw`

The mass gap is `m = -log ρ` where `ρ` is the transfer-matrix spectral radius. `refereeScalingLaw`
(the Milestone-3 target, `QM.refereeScalingLaw`) asks for `∃ A > 0, ∀ β > 0, A·e^{-(12π²/11)β} ≤ m(β)`.
These lemmas are the *provable* log/exp transport that turns a bound on the spectral radius into that
scaling law. The bridge is closed here; the open physics is the radius bound itself (the
running-coupling structure `ρ(β) ≤ e^{-A·e^{-(12π²/11)β}}`), which sits one rung above these lemmas.
-/

namespace RefereeScalingLaw

open Real

/-- **`m = -log ρ` and `ρ ≤ e^{-B}` give `B ≤ m`.** The log is antitone on `(0, ∞)`, so a radius
bound transfers to a mass-gap bound. This is the single transport step behind the scaling law. -/
theorem mass_gap_of_radius_bound {ρ m B : ℝ} (hm : m = -Real.log ρ)
    (hρ : ρ ≤ Real.exp (-B)) (hρ0 : 0 < ρ) : B ≤ m := by
  rw [hm]
  have hlog : Real.log ρ ≤ -B := by
    have hle : Real.log ρ ≤ Real.log (Real.exp (-B)) :=
      (Real.log_le_log_iff hρ0 (Real.exp_pos (-B))).2 hρ
    simpa [Real.log_exp] using hle
  linarith

/-- **The radius bound `ρ ≤ e^{-A·e^{-cβ}}` implies `A·e^{-cβ} ≤ m(β)`.** The mass gap inherits the
exponential lower bound from the spectral radius — the double exponential in the radius is the single
exponential in the gap. -/
theorem mass_gap_of_radius_exponential {ρ m A c β : ℝ} (hm : m = -Real.log ρ)
    (hρ : ρ ≤ Real.exp (-(A * Real.exp (-c * β)))) (hρ0 : 0 < ρ) :
    A * Real.exp (-c * β) ≤ m := by
  exact mass_gap_of_radius_bound hm hρ hρ0

/-- **The scaling law from a radius bound.** If for every `β > 0` the transfer-matrix spectral
radius satisfies `ρ(β) ≤ e^{-A·e^{-(12π²/11)β}}`, then the mass gap `m(β) = -log ρ(β)` satisfies
`QM.refereeScalingLaw`. This is the closed bridge: the *radius* bound carries the running-coupling
exponential, and the mass gap inherits it. -/
theorem refereeScalingLaw_of_radius_bound {ρ : ℝ → ℝ} {A : ℝ} (hA0 : 0 < A)
    (hρ : ∀ β : ℝ, 0 < β → ρ β ≤ Real.exp (-(A * Real.exp (-(12 * Real.pi ^ 2 / 11) * β))))
    (hρ0 : ∀ β : ℝ, 0 < β → 0 < ρ β) :
    QM.refereeScalingLaw (fun β => -Real.log (ρ β)) := by
  refine ⟨A, hA0, ?_⟩
  intro β hβ
  exact mass_gap_of_radius_exponential rfl (hρ β hβ) (hρ0 β hβ)

end RefereeScalingLaw
