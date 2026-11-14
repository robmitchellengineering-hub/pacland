import PaclandProof.Foundations.GleasonLemma

/-! Scratch verification for the final `hlat` reduction. NOT part of the proof; delete before commit. -/

noncomputable section
open Matrix BigOperators
namespace GleasonLemma

/-- **Signed-to-unsigned latitude invariance.** The antipodal map `t ↦ −t` carries the
latitude `t·p = a` to `t·p = −a` and, because a frame function is even (`even_of_frame`),
preserves `f`. So once `f` is constant on each *signed* latitude `{t : t·p = a}` (which is
what invariance under rotations about `p` delivers — they preserve `t·p`), it is constant on
each *unsigned* latitude `{t : (t·p)² = a²}`. This is the exact hypothesis `gleason_assembly`
needs. -/
theorem latitude_invariant_of_signed (p : Fin 3 → ℝ)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hsigned : ∀ t t', unitVec3 t → unitVec3 t' → dotProduct t p = dotProduct t' p → f t = f t') :
    ∀ t t', unitVec3 t → unitVec3 t' → (dotProduct t p) ^ 2 = (dotProduct t' p) ^ 2 → f t = f t' := by
  intro t t' ht ht' hsq
  by_cases h : dotProduct t p = dotProduct t' p
  · exact hsigned t t' ht ht' h
  · have hneg : dotProduct t p = -dotProduct t' p := by
      have hfactor : (dotProduct t p - dotProduct t' p) * (dotProduct t p + dotProduct t' p) = 0 := by
        nlinarith [hsq]
      rcases mul_eq_zero.mp hfactor with h1 | h2
      · have : dotProduct t p = dotProduct t' p := by linarith
        exact False.elim (h this)
      · linarith
    have hneg_unit : unitVec3 (-t') := by
      simpa [unitVec3, dotProduct, Fin.sum_univ_three] using ht'
    have hneg_dot : dotProduct (-t') p = -dotProduct t' p := by
      simp [dotProduct, Fin.sum_univ_three]
    have hft_neg : f t = f (-t') := by
      apply hsigned t (-t') ht hneg_unit
      rw [hneg, hneg_dot]
    rcases exists_perp t' ht' with ⟨v, hv, horth⟩
    have heven : f (-t') = f t' := even_of_frame f hf t' v ht' hv horth
    rw [hft_neg, heven]

end GleasonLemma
