import Mathlib

/-!
# The Tsirelson bound — quantum mechanics saturates `S = 2√2` (the "yes" side of Bell)

The CHSH local bound is `S ≤ 2`; the quantum strategy reaches `S = 2√2 > 2`. For the Bell state
`|Φ⁺⟩ = (|00⟩+|11⟩)/√2` and measurements `A₀ = σ_z, A₁ = σ_x, B₀ = (σ_z+σ_x)/√2,
B₁ = (σ_z−σ_x)/√2`, the four expectation values are `1/√2, 1/√2, 1/√2, −1/√2`, summing to
`4/√2 = 2√2`. The expectation formula is `⟨Φ⁺|A⊗B|Φ⁺⟩ = (1/2)(A₀₀B₀₀ + A₀₁B₀₁ + A₁₀B₁₀ + A₁₁B₁₁)`.
Here we factor the `1/√2` out of `B₀, B₁`, so the four inner expectations are integers.
-/

namespace QM

noncomputable section

/-- The Pauli-X matrix. -/
def paulX : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 1, 0]

/-- The Pauli-Z matrix. -/
def paulZ : Matrix (Fin 2) (Fin 2) ℝ := !![1, 0; 0, -1]

/-- The Bell-state expectation `⟨Φ⁺| A⊗B |Φ⁺⟩ = (1/2)(A₀₀B₀₀ + A₀₁B₀₁ + A₁₀B₁₀ + A₁₁B₁₁)`. -/
def bell_expect (A B : Matrix (Fin 2) (Fin 2) ℝ) : ℝ :=
  (1/2 : ℝ) * (A 0 0 * B 0 0 + A 0 1 * B 0 1 + A 1 0 * B 1 0 + A 1 1 * B 1 1)

-- The four unnormalized (integer) expectation values.
lemma bell_paulZ_add : bell_expect paulZ (paulZ + paulX) = 1 := by
  norm_num [bell_expect, paulX, paulZ]

lemma bell_paulZ_sub : bell_expect paulZ (paulZ - paulX) = 1 := by
  norm_num [bell_expect, paulX, paulZ]

lemma bell_paulX_add : bell_expect paulX (paulZ + paulX) = 1 := by
  norm_num [bell_expect, paulX, paulZ]

lemma bell_paulX_sub : bell_expect paulX (paulZ - paulX) = -1 := by
  norm_num [bell_expect, paulX, paulZ]

/-- **Tsirelson bound.** The quantum CHSH value is `2√2`. -/
theorem tsirelson_bound :
    (1 / Real.sqrt 2) * (bell_expect paulZ (paulZ + paulX) + bell_expect paulZ (paulZ - paulX)
      + bell_expect paulX (paulZ + paulX) - bell_expect paulX (paulZ - paulX))
      = 2 * Real.sqrt 2 := by
  rw [bell_paulZ_add, bell_paulZ_sub, bell_paulX_add, bell_paulX_sub]
  norm_num
  -- (1/√2) * 4 = 2√2  →  clear the division, then √2² = 2
  field_simp [(Real.sqrt_pos.2 (by norm_num : 0 < (2:ℝ))).ne']
  nlinarith [Real.sq_sqrt (by norm_num : 0 ≤ (2:ℝ))]

/-- The quantum violation: the quantum CHSH value exceeds the local bound 2. -/
theorem chsh_quantum_violates_local :
    (2 : ℝ) < (1 / Real.sqrt 2) * (bell_expect paulZ (paulZ + paulX) + bell_expect paulZ (paulZ - paulX)
      + bell_expect paulX (paulZ + paulX) - bell_expect paulX (paulZ - paulX)) := by
  rw [tsirelson_bound]
  -- 2 < 2√2 since 1 < √2
  have hsqrt : 1 < Real.sqrt 2 := by
    have hsq : (1 : ℝ) ^ 2 < (Real.sqrt 2) ^ 2 := by
      rw [Real.sq_sqrt (by norm_num : 0 ≤ (2:ℝ))]
      norm_num
    have habs := (sq_lt_sq.mp hsq)
    simpa [abs_of_pos (by norm_num : 0 < (1:ℝ)), abs_of_nonneg (Real.sqrt_nonneg 2)] using habs
  nlinarith

end
end QM
