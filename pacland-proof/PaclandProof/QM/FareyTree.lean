import Mathlib
import PaclandProof.QM.SternBrocot

/-!
# The Farey tree — the corrected map of the binary tree into H²

The Stern-Brocot encoding (`SternBrocot.lean`) proves the tree's boundary is the **circle** (the
positive rationals ∪ {∞}), not the Cantor set — this is the fix for the binary-expansion angle's
`0.0111… = 0.1000…` collapse. This file defines the corresponding map: the tree maps to the upper
half-plane ℍ by the PSL(2,ℤ) **Möbius orbit** of `i` under the word `L`/`R` — the Farey
tessellation's dual graph. The full quasi-isometry `tree ≃ H²` is the **Švarc–Milnor lemma**
(PSL(2,ℤ) acts cocompactly on ℍ), cited here, not re-proven — like Weyl's FFT.
-/

namespace Farey

/-- The left mediant generator `L(z) = z/(z+1)`. -/
noncomputable def L (z : ℂ) : ℂ := z / (z + 1)

/-- The right mediant generator `R(z) = z + 1`. -/
noncomputable def R (z : ℂ) : ℂ := z + 1

/-- The generator of the path step: `false ↦ L`, `true ↦ R`. -/
noncomputable def gen : Bool → (ℂ → ℂ)
  | false => L
  | true => R

/-- The word action: the path's Möbius map, first bit applied first (foldl). -/
noncomputable def word : List Bool → (ℂ → ℂ) :=
  List.foldl (fun acc b => gen b ∘ acc) id

/-- The Farey point of a path: the orbit of `i` under the word. -/
noncomputable def fareyPoint (s : List Bool) : ℂ := word s Complex.I

/-- The base point is the root's image. -/
theorem fareyPoint_nil : fareyPoint [] = Complex.I := by
  rfl

end Farey
