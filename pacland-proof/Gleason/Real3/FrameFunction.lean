import Mathlib

/-!
**FR.** # Frame functions sur ℝ³

Cœur analytique de Gleason, voie Cooke–Keane–Moran (1985) / Richman–Bridges (1999).
Une *frame function* de poids `W` sur la sphère unité de ℝ³ est une fonction dont la
somme sur toute base orthonormée vaut `W`. Le théorème dur (`Regular.lean`) : toute
frame function POSITIVE est la restriction d'une forme quadratique.

**EN.** # Frame functions on ℝ³

Analytic core of Gleason, via the Cooke–Keane–Moran (1985) / Richman–Bridges
(1999) route. A *frame function* of weight `W` on the unit sphere of ℝ³ is a
function whose sum over any orthonormal basis equals `W`. The hard theorem
(`Regular.lean`): every POSITIVE frame function is the restriction of a quadratic
form.
-/

namespace Gleason

open scoped RealInnerProductSpace

noncomputable section

/-- ℝ³ euclidien. -/
abbrev E3 := EuclideanSpace ℝ (Fin 3)

/--
**FR.** **Frame function de poids `W`** : la somme sur toute base orthonormée vaut `W`.
(Seules les valeurs sur la sphère unité comptent.)

**EN.** **Frame function of weight `W`**: the sum over any orthonormal basis
equals `W`. (Only the values on the unit sphere matter.)
-/
def IsFrameFunction (f : E3 → ℝ) (W : ℝ) : Prop :=
  ∀ b : OrthonormalBasis (Fin 3) ℝ E3, (∑ i, f (b i)) = W

-- `IsFrameFunction.le_of_nonneg` est dans `SphereGeometry.lean` : elle a besoin de
-- `exists_orthonormalBasis_fst` (complétion en base), et `SphereGeometry` importe
-- déjà `FrameFunction` (l'inverse créerait un cycle).

end
end Gleason
