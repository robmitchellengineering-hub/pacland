import Gleason.Defs
import Gleason.Busch.Effects

/-!
**FR.** # Tests d'inhabitation (non-vacuité)

**Discipline centrale du dépôt.** Chaque structure d'hypothèses doit posséder ici un
habitant CONCRET sur `ℂ³` (un vrai état quantique). C'est le test qui aurait détecté
dès le début les deux défauts fatals de l'ancien développement (types d'hypothèses
vides dès la dimension 2, axiome réfutable).

Règle : aucune structure nouvelle ne rentre dans `Defs.lean` sans son `example :
Nonempty (...)` ici, dans le même commit. Les `sorry` de ce fichier sont la
**première cible de preuve** du jalon M1.

**EN.** # Inhabitation tests (non-vacuity)

**Central discipline of this repository.** Every hypothesis structure must have a
CONCRETE inhabitant here on `ℂ³` (a real quantum state). This is the test that
would have caught, from the start, the two fatal flaws of the old development
(hypothesis types empty as soon as dimension 2, refutable axiom).

Rule: no new structure enters `Defs.lean` without its `example : Nonempty (...)`
here, in the same commit. The `sorry`s in this file are the **first proof target**
of milestone M1.
-/

namespace Gleason

open scoped InnerProductSpace

noncomputable section

/--
**FR.** **État pur** : un vecteur unitaire `ψ` induit la mesure `A ↦ ‖P_A ψ‖²`.
C'est la mesure de Born de l'état `|ψ⟩⟨ψ|`.

**EN.** **Pure state**: a unit vector `ψ` induces the measure `A ↦ ‖P_A ψ‖²`.
This is the Born measure of the state `|ψ⟩⟨ψ|`.
-/
noncomputable def pureState {n : ℕ} (ψ : H n) (hψ : ‖ψ‖ = 1) : ProjMeasure n where
  μ A := ‖(A.starProjection ψ : H n)‖ ^ 2
  nonneg A := by positivity
  top_eq_one := by
    simp [Submodule.starProjection_top, hψ]
  add_isOrtho A B hAB := by
    have hpA := Submodule.starProjection_apply_mem A ψ
    have hpB := Submodule.starProjection_apply_mem B ψ
    have hkey : (A ⊔ B).starProjection ψ = A.starProjection ψ + B.starProjection ψ := by
      have h : projL (A ⊔ B) ψ = (projL A + projL B) ψ := by
        rw [projL_sup_of_isOrtho hAB]
      simpa [projL] using h
    simp only [hkey, sq]
    exact norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _
      (Submodule.isOrtho_iff_inner_eq.mp hAB _ hpA _ hpB)

/--
**FR.** ℂ³ porte bien une mesure de projection : le type n'est PAS vide.

**EN.** ℂ³ does carry a projection measure: the type is NOT empty.
-/
example : Nonempty (ProjMeasure 3) :=
  ⟨pureState (EuclideanSpace.single 0 1) (by simp)⟩

/--
**FR.** Le même état pur induit une mesure d'effets (côté Busch) : `T ↦ Re ⟪T ψ, ψ⟫`.

**EN.** The same pure state induces an effect measure (Busch side):
`T ↦ Re ⟪T ψ, ψ⟫`.
-/
noncomputable def pureEffectMeasure {n : ℕ} (ψ : H n) (hψ : ‖ψ‖ = 1) : EffectMeasure n where
  f T := (⟪T ψ, ψ⟫_ℂ).re
  nonneg T hT := hT.1.2 ψ
  map_one := by
    simp [inner_self_eq_norm_sq_to_K, hψ]
  additive S T _ _ _ := by
    simp [LinearMap.add_apply]

/--
**FR.** ℂ³ porte bien une mesure d'effets : le type n'est PAS vide (et ℂ² aussi, cible Busch).

**EN.** ℂ³ does carry an effect measure: the type is NOT empty (and so does ℂ²,
Busch's target).
-/
example : Nonempty (EffectMeasure 3) :=
  ⟨pureEffectMeasure (EuclideanSpace.single 0 1) (by simp)⟩

example : Nonempty (EffectMeasure 2) :=
  ⟨pureEffectMeasure (EuclideanSpace.single 0 1) (by simp)⟩

end
end Gleason
