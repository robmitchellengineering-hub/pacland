import PaclandProof.QM.Committee.MassGapSpec

/-!
# Sanity controls — the non-vacuity tests for `HasEnergyGap` / `HasMassGap`

The two negative tests that pin down the mass-gap statement (review Q5 of `MassGapSpec.lean`):

1. **`hasEnergyGap_of_spectrum_at_zero`** — if the joint spectrum is supported at `{0}` (the
   vacuum-only theory), then `HasEnergyGap` holds VACUOUSLY (the punctured region `{p ≠ 0}` has
   projection 0). This is exactly why the gap clause is vacuous without non-triviality: the
   non-triviality (`Properties.nonfree` + `Reconstructed.acts`) is what makes the gap meaningful.

2. **`projection_subset_zero`** — the PVM monotonicity fact that powers #1: `A ⊆ B` and
   `projection B = 0` ⟹ `projection A = 0`. (No `sorry`; the core of the sanity control.)

The two `sorry` measurability side goals in #1 are routine (`{p | p ≠ 0}` is the complement of a closed
set; `{p | p ≠ 0 ∧ time p < Δ}` is an intersection of measurable sets). Draft-only, matching
`MassGapSpec.lean`'s convention.
-/

noncomputable section
open MeasureTheory Set
open scoped BigOperators

namespace YangMills
variable {H : HilbertSpace} {Labels : FieldLabels}

/-- **PVM monotonicity** (the core of the sanity control): if `A ⊆ B` and the projection of `B` is 0,
then the projection of `A` is 0. This is the PVM fact that makes the gap clause vacuous for a vacuum-only
theory. -/
theorem projection_subset_zero (theory : WightmanTheory H Labels) {A B : Set Spacetime}
    (hAB : A ⊆ B) (hA : MeasurableSet A) (hB : MeasurableSet B)
    (hB0 : theory.energyMomentum.projection B = 0) :
    theory.energyMomentum.projection A = 0 := by
  have hABeq : A ∩ B = A := by
    ext x; exact ⟨fun h => h.1, fun h => ⟨h, hAB h⟩⟩
  have hcomp := theory.energyMomentum.intersection hA hB
  calc
    theory.energyMomentum.projection A = theory.energyMomentum.projection (A ∩ B) := by rw [hABeq]
    _ = (theory.energyMomentum.projection A).comp (theory.energyMomentum.projection B) := by rw [hcomp]
    _ = (theory.energyMomentum.projection A).comp 0 := by rw [hB0]
    _ = 0 := by simp

/-- **SANITY CONTROL #1** (vacuousness): a vacuum-only theory (joint spectrum at `{0}`) satisfies
`HasEnergyGap` — the gap clause is vacuous unless the theory is non-trivial. The non-triviality
(`Properties.nonfree` + `Reconstructed.acts`) is what makes the gap meaningful. -/
theorem hasEnergyGap_of_spectrum_at_zero (theory : WightmanTheory H Labels)
    (h : theory.energyMomentum.projection {p : Spacetime | p ≠ 0} = 0) :
    HasEnergyGap theory := by
  refine ⟨1, by norm_num, ?_⟩
  exact projection_subset_zero theory (fun p hp => hp.1) (by sorry) (by sorry) h

end YangMills
