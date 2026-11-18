import PaclandProof.QM.Committee.ChallengeSpec

/-!
# DRAFT mass-gap statement against the committee's `Hierarchy` / `WightmanTheory` API

STATUS
* Written against `yang-mills-group/OpenAI-YM-20261028` at commit 3456e5e75cf8 (Lean v4.32.0).
* NOT compiled: the committee build was not available when this was drafted. Expect small fixes
  (coercions, `Set` measurability side goals, namespace opens).
* It states the target ONLY. Nothing here claims a proof of a mass gap. Proofs marked `sorry` are routine
  lemmas whose only purpose is to sanity-check the statement; keep this file out of any no-`sorry` build.
* Meant as the artefact to hand to experts for fidelity review (see REVIEW QUESTIONS at the bottom).

HOW THE GAP IS EXPRESSED
The committee's `WightmanTheory` already carries a projection-valued joint energy-momentum measure
`energyMomentum`, axiom W0 gives positive energy (`projection forwardConeᶜ = 0`) and a unique
translation-invariant vacuum. So "mass gap" can be stated spectrally, with no new structures:
  no joint spectrum at nonzero momentum with energy below Δ.
The point p = 0 carries exactly the vacuum, by `uniqueVacuum`.
-/

set_option autoImplicit false
noncomputable section

namespace YangMills

open MeasureTheory Filter Set

section Gap

variable {H : HilbertSpace} {Labels : FieldLabels}

/-- Clay's literal formulation: for some Δ > 0 the joint spectrum has no point `p ≠ 0` with energy `time p < Δ`.
(Energy = time component of the four-momentum; with W0's positivity the spectrum lies in the forward cone.) -/
def HasEnergyGap (theory : WightmanTheory H Labels) : Prop :=
  ∃ Δ : ℝ, 0 < Δ ∧
    theory.energyMomentum.projection {p : Spacetime | p ≠ 0 ∧ time p < Δ} = 0

/-- Lorentz-scalar formulation: no joint spectrum in the forward cone with `0 < p² < m²`
(and none on the light cone except `p = 0`, so massless particles are excluded). -/
def HasMassGap (theory : WightmanTheory H Labels) : Prop :=
  ∃ m : ℝ, 0 < m ∧
    theory.energyMomentum.projection
      {p : Spacetime | p ∈ forwardCone ∧ p ≠ 0 ∧ minkowskiSquare p < m ^ 2} = 0

/-- The region used in `HasEnergyGap` is measurable (open ∩ open), so the projection axioms apply. -/
theorem measurableSet_energyGapRegion (Δ : ℝ) :
    MeasurableSet {p : Spacetime | p ≠ 0 ∧ time p < Δ} := by
  sorry

/-- Easy direction: the Lorentz-scalar gap implies Clay's energy gap with Δ = m.
Proof sketch: inside the forward cone `p² ≤ (time p)²`, so `{p ∈ cone, p ≠ 0, time p < m}` ⊆ the mass region;
the part outside the cone has projection 0 by W0 (`positiveEnergy`); use additivity/monotonicity of `projection`. -/
theorem hasEnergyGap_of_hasMassGap (theory : WightmanTheory H Labels) (hW0 : theory.W0)
    (h : HasMassGap theory) : HasEnergyGap theory := by
  sorry

/- The converse (energy gap ⇒ mass gap) needs Lorentz covariance of the joint spectrum (W2 + a spectral argument):
   left as a separate, harder lemma; Clay's statement only needs `HasEnergyGap`. -/

end Gap

/-! ## The joint target -/

/-- The committee's `JointExistence`, strengthened by a spectral gap for the constructed theory.
Same quantifier structure: one Wilson family per simple group, then (along a subsequence of any volume
sequence) a hierarchy with all four published properties AND an energy gap. -/
def JointExistenceWithGap : Prop :=
  ∀ g : GaugeGroup, g.IsSimple → ∃ C : WilsonFamily g,
    WilsonRegularity C ∧ ∀ p : ℕ → ℕ, StrictMono p → ∃ q : ℕ → ℕ, StrictMono q ∧
      ∃ T : Hierarchy C, T.Properties (p ∘ q) ∧ HasEnergyGap T.theory

/-- Sanity: the gap target strictly strengthens the committee's existence statement. -/
theorem jointExistenceWithGap_implies_jointExistence :
    JointExistenceWithGap → JointExistence := by
  intro h g hg
  obtain ⟨C, hreg, hC⟩ := h g hg
  refine ⟨C, hreg, fun p hp => ?_⟩
  obtain ⟨q, hq, T, hT, -⟩ := hC p hp
  exact ⟨q, hq, T, hT⟩

end YangMills

/-!
## REVIEW QUESTIONS (for experts, before any proof effort)

1. Energy vs mass. Is `HasEnergyGap` exactly the Clay condition "spectrum of H on the vacuum complement lies in
   [Δ, ∞)", given W0's unique vacuum? (Intended: yes; the p ≠ 0 punctured region excludes only the vacuum point.)
2. Non-triviality interplay. The gap is vacuous for a theory with only the vacuum. Here non-triviality comes from
   `Properties.nonfree` and `Reconstructed.acts`. Is that enough to make `HasEnergyGap` meaningful?
3. Subsequence quantifier. The committee statement gives a continuum limit along a subsequence of any volume
   sequence and does not assert uniqueness. Is a gap for "some limit along some subsequence" the right target,
   or should the statement quantify over all limit points (stronger)?
4. Selected phase. `T.theory` is the theory for the selected character/phase. Should the gap be required for
   every character in the phase measure, or only the selected one?
5. Sanity controls to build: (a) a trivial Hilbert space satisfies `HasEnergyGap` but fails `Properties`;
   (b) a massless free-field model has joint spectrum on the light cone and must FAIL `HasMassGap`.
6. Dependencies on `Classical`: the committee files `open scoped Classical`; check it does not change the meaning
   of `projection`-set equalities here.
-/

end
