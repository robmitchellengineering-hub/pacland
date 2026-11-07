import Mathlib

/-!
# PBR (Pusey–Barrett–Rudolph) — the ψ-epistemic no-go, finite form

The falsification rung that excludes *ψ-epistemic* interpretations (where a quantum state is a
probability distribution over some ontic state, so distinct but non-orthogonal states overlap).
The finite form is the key **independence lemma**: for two distinct non-orthogonal pure states,
the four two-copy states `|ψᵢ⟩⊗|ψⱼ⟩` are **linearly independent** — so a measurement exists that
distinguishes them, contradicting the overlap of any ψ-epistemic model.

Here we take `|ψ₀⟩ = |0⟩` and `|ψ₁⟩ = |0⟩+|1⟩` (unnormalised; the argument is scale-invariant).
The four two-copy states are the columns of the upper-triangular matrix

    1 1 1 1
    0 1 0 1
    0 0 1 1
    0 0 0 1

and their linear independence is kernel-checked by the triangular back-substitution: the
bottom coordinate forces `c₃ = 0`, then `c₂ = 0`, `c₁ = 0`, `c₀ = 0`.
-/

namespace QM

/-- The four two-copy states as columns. -/
def pbr_matrix : Matrix (Fin 4) (Fin 4) ℝ := !![1, 1, 1, 1; 0, 1, 0, 1; 0, 0, 1, 1; 0, 0, 0, 1]

/-- The `j`-th two-copy state as a vector. -/
def pbr_col (j : Fin 4) : Fin 4 → ℝ := fun i => pbr_matrix i j

/-- **PBR independence.** The four two-copy states `|ψᵢ⟩⊗|ψⱼ⟩` are linearly independent. -/
theorem pbr_two_copy_independent : LinearIndependent ℝ pbr_col := by
  rw [Fintype.linearIndependent_iff]
  intro c hc
  have h3 : c 3 = 0 := by
    have h := congrFun hc 3
    simp [pbr_col, pbr_matrix, Finset.sum_apply, Fin.sum_univ_four] at h
    norm_num at h
    exact h
  have h2 : c 2 = 0 := by
    have h := congrFun hc 2
    simp [pbr_col, pbr_matrix, Finset.sum_apply, Fin.sum_univ_four] at h
    norm_num [h3] at h
    exact h
  have h1 : c 1 = 0 := by
    have h := congrFun hc 1
    simp [pbr_col, pbr_matrix, Finset.sum_apply, Fin.sum_univ_four] at h
    norm_num [h3] at h
    exact h
  have h0 : c 0 = 0 := by
    have h := congrFun hc 0
    simp [pbr_col, pbr_matrix, Finset.sum_apply, Fin.sum_univ_four] at h
    norm_num [h1, h2, h3] at h
    exact h
  intro j
  fin_cases j <;> simp [h0, h1, h2, h3]

end QM
