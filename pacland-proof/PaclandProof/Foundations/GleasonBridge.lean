import Gleason
import PaclandProof.Foundations.GleasonLemma

/-!
# Bridge: our `FrameFunction3` (Fin 3 → ℝ, dotProduct) ⟹ the CKM Born rule

The vendored `Gleason` library (CKM descent-chain route) proves, in the encoding
`E3 = EuclideanSpace ℝ (Fin 3)` + `⟪·,·⟫` + `OrthonormalBasis`, that every positive frame
function is a quadratic form (`Gleason.frameFunction_regular`). This file bridges that to
our native encoding (`Fin 3 → ℝ` + `dotProduct` + `FrameFunction3`), so the Born rule is a
single theorem over our own definitions.
-/

open scoped RealInnerProductSpace

namespace GleasonBridge

noncomputable section

open Gleason

/-- The inner product on `EuclideanSpace ℝ (Fin 3)` equals Mathlib's `dotProduct`. -/
theorem inner_eq_dotProduct (x y : EuclideanSpace ℝ (Fin 3)) :
    ⟪x, y⟫ = dotProduct (x : Fin 3 → ℝ) (y : Fin 3 → ℝ) := by
  simp [dotProduct, Fin.sum_univ_three, PiLp.inner_apply, mul_comm]

/-- `‖x‖ = 1` implies our `unitVec3`. -/
theorem unitVec3_of_norm_eq_one (x : EuclideanSpace ℝ (Fin 3)) (h : ‖x‖ = 1) :
    GleasonLemma.unitVec3 (x : Fin 3 → ℝ) := by
  dsimp [GleasonLemma.unitVec3]
  have hsq : ‖x‖ ^ 2 = 1 := by rw [h]; norm_num
  rw [PiLp.norm_eq_of_L2] at hsq
  rw [Real.sq_sqrt] at hsq
  · simp [dotProduct, Fin.sum_univ_three] at hsq ⊢
    nlinarith [hsq]
  · positivity

/-- `⟪x, y⟫ = 0` implies our `orthVec3`. -/
theorem orthVec3_of_inner_zero (x y : EuclideanSpace ℝ (Fin 3)) (h : ⟪x, y⟫ = 0) :
    GleasonLemma.orthVec3 (x : Fin 3 → ℝ) (y : Fin 3 → ℝ) := by
  dsimp [GleasonLemma.orthVec3]
  rw [inner_eq_dotProduct x y] at h
  simpa using h

/-- Our `FrameFunction3` implies the CKM `IsFrameFunction` (weight 1), after coercing the
argument `E3 → Fin 3 → ℝ`. -/
theorem frameFunction3_to_isFrameFunction (f : (Fin 3 → ℝ) → ℝ)
    (hf : GleasonLemma.FrameFunction3 f) :
    IsFrameFunction (fun x : EuclideanSpace ℝ (Fin 3) => f (x : Fin 3 → ℝ)) 1 := by
  intro b
  have hu0 : GleasonLemma.unitVec3 (b 0 : Fin 3 → ℝ) :=
    unitVec3_of_norm_eq_one (b 0) (b.norm_eq_one 0)
  have hu1 : GleasonLemma.unitVec3 (b 1 : Fin 3 → ℝ) :=
    unitVec3_of_norm_eq_one (b 1) (b.norm_eq_one 1)
  have hu2 : GleasonLemma.unitVec3 (b 2 : Fin 3 → ℝ) :=
    unitVec3_of_norm_eq_one (b 2) (b.norm_eq_one 2)
  have h01 : GleasonLemma.orthVec3 (b 0 : Fin 3 → ℝ) (b 1 : Fin 3 → ℝ) :=
    orthVec3_of_inner_zero (b 0) (b 1) (b.inner_eq_zero (by decide))
  have h02 : GleasonLemma.orthVec3 (b 0 : Fin 3 → ℝ) (b 2 : Fin 3 → ℝ) :=
    orthVec3_of_inner_zero (b 0) (b 2) (b.inner_eq_zero (by decide))
  have h12 : GleasonLemma.orthVec3 (b 1 : Fin 3 → ℝ) (b 2 : Fin 3 → ℝ) :=
    orthVec3_of_inner_zero (b 1) (b 2) (b.inner_eq_zero (by decide))
  have hsum := hf (b 0 : Fin 3 → ℝ) (b 1 : Fin 3 → ℝ) (b 2 : Fin 3 → ℝ) hu0 hu1 hu2 h01 h02 h12
  simpa [Fin.sum_univ_three] using hsum

/-- **Born rule**: every nonnegative frame function on the sphere is a quadratic form
`x ↦ q x = Tr(ρ P_x)` (i.e. `Σ qᵢⱼ xᵢ xⱼ`). This is the CKM/Gleason assembly discharged for
our native `FrameFunction3`. -/
theorem gleason_born_rule (f : (Fin 3 → ℝ) → ℝ) (hf : GleasonLemma.FrameFunction3 f)
    (hnn : ∀ x, GleasonLemma.unitVec3 x → 0 ≤ f x) :
    ∃ q : QuadraticForm ℝ (EuclideanSpace ℝ (Fin 3)),
      ∀ x : EuclideanSpace ℝ (Fin 3), ‖x‖ = 1 → f (x : Fin 3 → ℝ) = q x := by
  let fE3 : EuclideanSpace ℝ (Fin 3) → ℝ := fun x => f (x : Fin 3 → ℝ)
  have hfE3 : IsFrameFunction fE3 1 := frameFunction3_to_isFrameFunction f hf
  have hnnE3 : ∀ x : EuclideanSpace ℝ (Fin 3), ‖x‖ = 1 → 0 ≤ fE3 x := by
    intro x hx
    exact hnn (x : Fin 3 → ℝ) (unitVec3_of_norm_eq_one x hx)
  obtain ⟨q, hq⟩ := Gleason.frameFunction_regular fE3 1 hfE3 hnnE3
  exact ⟨q, fun x hx => by simpa [fE3] using hq x hx⟩

end
end GleasonBridge
