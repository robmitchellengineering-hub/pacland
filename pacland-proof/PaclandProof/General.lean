import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Mitchell's Uniqueness Theorem — general-n machinery (machine-checked)

The D3 tadpole `Fᵀ J H` is the unique symplectic invariant bilinear form in the flux
pair, in **any** dimension. This file proves, for the abstract case (any finite index
type `l`, any field `R`), the machinery the uniqueness argument rests on:

1. the shear `fromBlocks 1 X 0 1` is symplectic for symmetric `X`;
2. the block-diagonal `fromBlocks U 0 0 V` is symplectic when `Uᵀ V = 1`;
3. the canonical pairing `(Sx)ᵀ J (Sy) = xᵀ J y` is invariant under every symplectic
   `S` (this is why the tadpole is *an* invariant).

The full uniqueness theorem (the *only* invariant is a scalar multiple of `J`) is
proven for `n = 1` in `Mitchell.lean`; the general-n statement is the next
formalization target, using these generators together with `J` itself (the swap).
-/

open Matrix

noncomputable section

namespace Mitchell

variable {l : Type*} [DecidableEq l] [Fintype l] {R : Type*} [Field R]

/-- The shear `fromBlocks 1 X 0 1` is symplectic for symmetric `X`. -/
theorem shear_mem (X : Matrix l l R) (hX : X.IsSymm) :
    fromBlocks (1 : Matrix l l R) X 0 1 ∈ symplecticGroup l R := by
  rw [SymplecticGroup.fromBlocks_mem_iff]
  exact ⟨by simp, by simpa [Matrix.IsSymm] using hX, by simp⟩

/-- The block-diagonal `fromBlocks U 0 0 V` is symplectic when `Uᵀ V = 1`. -/
theorem diag_mem (U V : Matrix l l R) (hUV : Uᵀ * V = 1) :
    fromBlocks U 0 0 V ∈ symplecticGroup l R := by
  rw [SymplecticGroup.fromBlocks_mem_iff]
  exact ⟨by simp, by simp, by simpa using hUV⟩

/-- The canonical symplectic matrix `J` itself is symplectic. (The "swap".) -/
theorem J_mem : (J l R) ∈ symplecticGroup l R :=
  SymplecticGroup.J_mem l R

/-- The canonical pairing is invariant under symplectic transformations:
`(Sx)ᵀ J (Sy) = xᵀ J y`. -/
theorem pairing_invariant (S : Matrix (l ⊕ l) (l ⊕ l) R)
    (hS : S ∈ symplecticGroup l R) (x y : (l ⊕ l) → R) :
    dotProduct (S.mulVec x) ((J l R).mulVec (S.mulVec y)) = dotProduct x ((J l R).mulVec y) := by
  have hS' : Sᵀ * (J l R) * S = J l R := (SymplecticGroup.mem_iff' (l := l) (R := R)).1 hS
  calc
    dotProduct (S.mulVec x) ((J l R).mulVec (S.mulVec y))
        = dotProduct x (Sᵀ.mulVec ((J l R).mulVec (S.mulVec y))) := by
            simpa [Matrix.vecMul_transpose] using
              (Matrix.dotProduct_mulVec x Sᵀ ((J l R).mulVec (S.mulVec y))).symm
    _ = dotProduct x ((Sᵀ * (J l R) * S).mulVec y) := by
            rw [Matrix.mulVec_mulVec, Matrix.mulVec_mulVec]
    _ = dotProduct x ((J l R).mulVec y) := by rw [hS']

/-- A matrix that commutes with every symmetric matrix is a scalar multiple of the
identity. -/
theorem scalar_of_commute_all_symm (Q : Matrix l l R)
    (h : ∀ X : Matrix l l R, X.IsSymm → X * Q = Q * X) :
    ∃ c : R, Q = c • (1 : Matrix l l R) := by
  -- `Q` is diagonal: off-diagonal entries vanish.
  have hd : ∀ ⦃i j : l⦄, i ≠ j → Q i j = 0 := by
    intro i j hij
    have hc : Commute (Matrix.single i i (1 : R)) Q :=
      h (Matrix.single i i (1 : R)) (by simp [IsSymm, transpose_single])
    exact Matrix.row_eq_zero_of_commute_single hc (Ne.symm hij)
  -- The diagonal entries all agree.
  have hdiag : ∀ i j : l, Q i i = Q j j := by
    intro i j
    by_cases hij : i = j
    · subst hij
      rfl
    · have hc : (Matrix.single i j (1 : R) + Matrix.single j i (1 : R)) * Q =
            Q * (Matrix.single i j (1 : R) + Matrix.single j i (1 : R)) :=
        h (Matrix.single i j (1 : R) + Matrix.single j i (1 : R))
          (by simp [IsSymm, transpose_single, add_comm])
      have e : ((Matrix.single i j (1 : R) + Matrix.single j i (1 : R)) * Q) i j =
          (Q * (Matrix.single i j (1 : R) + Matrix.single j i (1 : R))) i j :=
        congr_fun (congr_fun hc i) j
      have hL : ((Matrix.single i j (1 : R) + Matrix.single j i (1 : R)) * Q) i j = Q j j := by
        simp [Matrix.add_mul, hij]
      have hR : (Q * (Matrix.single i j (1 : R) + Matrix.single j i (1 : R))) i j = Q i i := by
        simp [Matrix.mul_add, Ne.symm hij]
      simpa [hL, hR] using e.symm
  -- Assemble.
  rcases isEmpty_or_nonempty l with hE | hNE
  · refine ⟨0, ?_⟩
    ext i j
    exact False.elim (hE.false i)
  · obtain ⟨d⟩ := hNE
    refine ⟨Q d d, ?_⟩
    ext i j
    by_cases hij : i = j
    · rw [hij]
      simpa using (hdiag j d)
    · simpa [hij] using (hd hij)

/-- **Mitchell's Uniqueness Theorem (general n).**
The only matrices preserved by every symplectic transformation `Sᵀ M S = M` are the
scalar multiples of the canonical symplectic form `J`. -/
theorem mitchell_uniqueness (M : Matrix (l ⊕ l) (l ⊕ l) R)
    (h : ∀ S, S ∈ symplecticGroup l R → Sᵀ * M * S = M) :
    ∃ c : R, M = c • (J l R) := by
  set P := M.toBlocks₁₁
  set Q := M.toBlocks₁₂
  set Rm := M.toBlocks₂₁
  set T := M.toBlocks₂₂
  have hM : M = fromBlocks P Q Rm T := by
    dsimp [P, Q, Rm, T]
    exact (fromBlocks_toBlocks M).symm
  -- Step 1: the shear with `X = 1` forces `P = 0` and `Rm = -Q`.
  have hsh := h (fromBlocks (1 : Matrix l l R) 1 0 1) (shear_mem (1 : Matrix l l R) (by simp))
  have hsh' : fromBlocks P (P + Q) (P + Rm) ((P + Rm) + (Q + T)) = fromBlocks P Q Rm T := by
    simpa [hM, fromBlocks_transpose, fromBlocks_multiply] using hsh
  obtain ⟨_, h12, _, h22⟩ := (fromBlocks_inj.mp hsh')
  have hP0 : P = 0 := by
    have := congrArg (fun x : Matrix l l R => x - Q) h12
    simpa using this
  have hRm : Rm = -Q := by
    have h22a : Rm + Q + T = T := by simpa [hP0, add_assoc] using h22
    have := congrArg (fun x : Matrix l l R => x - T) h22a
    have h22b : Rm + Q = 0 := by simpa using this
    exact eq_neg_of_add_eq_zero_left h22b
  -- Step 2: `Q` commutes with every symmetric matrix.
  have hQcomm : ∀ X : Matrix l l R, X.IsSymm → X * Q = Q * X := by
    intro X hX
    have hshX := h (fromBlocks (1 : Matrix l l R) X 0 1) (shear_mem X hX)
    have hshX' : fromBlocks P (P * X + Q) (X * P + Rm) ((X * P + Rm) * X + (X * Q + T))
        = fromBlocks P Q Rm T := by
      simpa [hM, fromBlocks_transpose, fromBlocks_multiply, hX.eq] using hshX
    obtain ⟨_, _, _, h22X⟩ := (fromBlocks_inj.mp hshX')
    have h22X'' : (X * P + Rm) * X + X * Q = 0 := by
      have hsub := congrArg (fun y : Matrix l l R => y - T) h22X
      rw [← add_assoc, add_sub_cancel_right, sub_self] at hsub
      exact hsub
    have h22X''' : -(Q * X) + X * Q = 0 := by
      simpa [hP0, hRm, Matrix.neg_mul] using h22X''
    have hQX : X * Q = -(-(Q * X)) := eq_neg_of_add_eq_zero_right h22X'''
    simpa using hQX
  -- Step 3: `Q` is a scalar matrix.
  obtain ⟨c₀, hQ⟩ := scalar_of_commute_all_symm Q hQcomm
  -- Step 4: the swap `J` forces `T = P = 0`.
  have hJ := h (J l R) (J_mem (l := l) (R := R))
  have hJ' : fromBlocks T (-Rm) (-Q) P = fromBlocks P Q Rm T := by
    simpa [hM, J, fromBlocks_neg, fromBlocks_transpose, fromBlocks_multiply] using hJ
  obtain ⟨hT, _, _, _⟩ := (fromBlocks_inj.mp hJ')
  have hT0 : T = 0 := by simpa [hP0] using hT
  -- Step 5: assemble.
  refine ⟨-c₀, ?_⟩
  calc
    M = fromBlocks P Q Rm T := hM
    _ = fromBlocks 0 (c₀ • 1) (-(c₀ • 1)) 0 := by simp [hP0, hQ, hRm, hT0]
    _ = (-c₀) • (J l R) := by simp [J, fromBlocks_smul, fromBlocks_neg, neg_smul, smul_neg]

end Mitchell

end
