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

end Mitchell

end
