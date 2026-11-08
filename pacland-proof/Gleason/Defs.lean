import Mathlib

/-!
**FR.** # Définitions centrales

Objets de base pour la formalisation du théorème de Gleason (variante « projection
only », dimension finie) et du théorème de Busch (2003).

## Correction du défaut fatal de l'ancien développement

L'additivité de `ProjMeasure` est exigée pour l'ORTHOGONALITÉ (`Submodule.IsOrtho`),
et non pour la disjonction de treillis (`Disjoint`). Avec la disjonction de treillis,
le type des mesures est VIDE dès la dimension 2 (trois droites distinctes d'un plan
forcent 3/2 = 1). Chaque structure introduite ici doit être accompagnée, dans le même
commit, d'un test d'inhabitation dans `Gleason/Nonvacuity.lean`.

## Conventions

* `H n = EuclideanSpace ℂ (Fin n)` : espace de Hilbert complexe de dimension `n`.
* Produit scalaire Mathlib `⟪·,·⟫_ℂ` : linéaire en la SECONDE variable.
* Aucune déclaration `axiom` n'est autorisée dans ce dépôt (voir `scripts/guard.sh`).

**EN.** # Core definitions

Basic objects for the formalization of Gleason's theorem ("projections only"
variant, finite dimension) and of Busch's theorem (2003).

## Fixing the fatal flaw of the old development

The additivity of `ProjMeasure` is required for ORTHOGONALITY (`Submodule.IsOrtho`),
not for lattice disjointness (`Disjoint`). With lattice disjointness, the type of
measures is EMPTY as soon as dimension 2 (three distinct lines of a plane force
3/2 = 1). Every structure introduced here must be accompanied, in the same commit,
by an inhabitation test in `Gleason/Nonvacuity.lean`.

## Conventions

* `H n = EuclideanSpace ℂ (Fin n)`: complex Hilbert space of dimension `n`.
* Mathlib inner product `⟪·,·⟫_ℂ`: linear in the SECOND variable.
* No `axiom` declaration is allowed in this repository (see `scripts/guard.sh`).
-/

namespace Gleason

open scoped InnerProductSpace

noncomputable section

/-- Espace de Hilbert complexe de dimension finie `n`. -/
abbrev H (n : ℕ) := EuclideanSpace ℂ (Fin n)

variable {n : ℕ}

/--
**FR.** **Mesure de probabilité finiment additive sur les sous-espaces** d'un espace de
Hilbert complexe de dimension finie. L'additivité est exigée pour l'orthogonalité
au sens du produit scalaire (`Submodule.IsOrtho`, notation `A ⟂ B`).

**EN.** **Finitely additive probability measure on subspaces** of a finite-dimensional
complex Hilbert space. Additivity is required for orthogonality in the inner-product
sense (`Submodule.IsOrtho`, notation `A ⟂ B`).
-/
structure ProjMeasure (n : ℕ) where
  /--
**FR.** La valuation sur les sous-espaces.

**EN.** The valuation on subspaces.
-/
  μ : Submodule ℂ (H n) → ℝ
  nonneg : ∀ A, 0 ≤ μ A
  top_eq_one : μ ⊤ = 1
  /--
**FR.** Additivité sur les paires orthogonales (au sens du produit scalaire !).

**EN.** Additivity on orthogonal pairs (in the inner-product sense!).
-/
  add_isOrtho : ∀ A B : Submodule ℂ (H n), A ⟂ B → μ (A ⊔ B) = μ A + μ B

/--
**FR.** **Opérateur densité** : symétrique (auto-adjoint), positif, de trace 1.

**EN.** **Density operator**: symmetric (self-adjoint), positive, trace 1.
-/
structure IsDensityOperator (ρ : H n →ₗ[ℂ] H n) : Prop where
  symmetric : LinearMap.IsSymmetric ρ
  nonneg : ∀ x : H n, 0 ≤ (⟪ρ x, x⟫_ℂ).re
  trace_one : LinearMap.trace ℂ (H n) ρ = 1

/--
**FR.** Projection orthogonale sur `A`, vue comme endomorphisme linéaire de `H n`
(`Submodule.starProjection` ; en dimension finie, l'instance
`HasOrthogonalProjection` est automatique).

**EN.** Orthogonal projection onto `A`, viewed as a linear endomorphism of `H n`
(`Submodule.starProjection`; in finite dimension, the `HasOrthogonalProjection`
instance is automatic).
-/
def projL (A : Submodule ℂ (H n)) : H n →ₗ[ℂ] H n :=
  (A.starProjection : H n →L[ℂ] H n).toLinearMap

/--
**FR.** **Valeur de Born** : `Re (tr (ρ ∘ P_A))`. Pour `ρ` densité et `A` sous-espace,
cette trace est réelle ; on prend la partie réelle pour typer en `ℝ`.

**EN.** **Born value**: `Re (tr (ρ ∘ P_A))`. For `ρ` a density operator and `A` a
subspace, this trace is real; we take the real part to type it as `ℝ`.
-/
def bornValue (ρ : H n →ₗ[ℂ] H n) (A : Submodule ℂ (H n)) : ℝ :=
  (LinearMap.trace ℂ (H n) (ρ ∘ₗ projL A)).re

/--
**FR.** Additivité de la projection orthogonale sur une somme orthogonale directe :
`P_{A⊔B} = P_A + P_B` si `A ⟂ B`. Factorisé depuis les preuves inline de
`EffectMeasure.toProjMeasure` et `pureState` (mêmes calculs, réutilisés ici).

**EN.** Additivity of the orthogonal projection over an orthogonal direct sum:
`P_{A⊔B} = P_A + P_B` if `A ⟂ B`. Factored out from the inline proofs of
`EffectMeasure.toProjMeasure` and `pureState` (identical computations, reused here).
-/
theorem projL_sup_of_isOrtho {A B : Submodule ℂ (H n)} (hAB : A ⟂ B) :
    projL (A ⊔ B) = projL A + projL B := by
  apply LinearMap.ext; intro v
  show (A ⊔ B).starProjection v = A.starProjection v + B.starProjection v
  apply Submodule.eq_starProjection_of_mem_of_inner_eq_zero
  · exact Submodule.add_mem_sup
      (Submodule.starProjection_apply_mem A v)
      (Submodule.starProjection_apply_mem B v)
  · intro w hw
    obtain ⟨a, ha, b, hb, rfl⟩ := Submodule.mem_sup.mp hw
    rw [inner_add_right]
    have h1 : ⟪v - (A.starProjection v + B.starProjection v), a⟫_ℂ = 0 := by
      rw [show v - (A.starProjection v + B.starProjection v) =
          (v - A.starProjection v) - B.starProjection v from by abel,
          inner_sub_left,
          Submodule.starProjection_inner_eq_zero (K := A) v a ha,
          Submodule.isOrtho_iff_inner_eq.mp hAB.symm _
            (Submodule.starProjection_apply_mem B v) _ ha]
      simp
    have h2 : ⟪v - (A.starProjection v + B.starProjection v), b⟫_ℂ = 0 := by
      rw [show v - (A.starProjection v + B.starProjection v) =
          (v - B.starProjection v) - A.starProjection v from by abel,
          inner_sub_left,
          Submodule.starProjection_inner_eq_zero (K := B) v b hb,
          Submodule.isOrtho_iff_inner_eq.mp hAB _
            (Submodule.starProjection_apply_mem A v) _ hb]
      simp
    rw [h1, h2, add_zero]

/--
**FR.** **M4-2(c).** Un opérateur symétrique positif (`Re⟪ρz,z⟫ ≥ 0` partout) qui atteint 0 en
`y` (`⟪ρy,y⟫ = 0`) y est nul : `ρ y = 0`. N'existe pas tel quel dans Mathlib (le voisinage
`LinearMap.IsPositive` fournit la positivité mais pas ce cas d'égalité). Preuve autonome :
`0 ≤ Re⟪ρ(y+t•z),y+t•z⟫ = t²·Re⟪ρz,z⟫ + 2t·Re⟪ρy,z⟫` pour tout `t : ℝ` force le coefficient
linéaire `Re⟪ρy,z⟫` à s'annuler (témoin explicite `t₀ := -B/(K+1)` sinon) ; on refait
l'argument avec `I•z` pour la partie imaginaire, d'où `⟪ρy,z⟫ = 0` pour tout `z`, en
particulier `z := ρy`.

**EN.** **M4-2(c).** A positive symmetric operator (`Re⟪ρz,z⟫ ≥ 0` everywhere) that
attains 0 at `y` (`⟪ρy,y⟫ = 0`) vanishes there: `ρ y = 0`. Not available as such in
Mathlib (the neighboring `LinearMap.IsPositive` gives positivity but not this
equality case). Self-contained proof: `0 ≤ Re⟪ρ(y+t•z),y+t•z⟫ =
t²·Re⟪ρz,z⟫ + 2t·Re⟪ρy,z⟫` for all `t : ℝ` forces the linear coefficient
`Re⟪ρy,z⟫` to vanish (explicit witness `t₀ := -B/(K+1)` otherwise); the same
argument is redone with `I•z` for the imaginary part, giving `⟪ρy,z⟫ = 0` for all
`z`, in particular `z := ρy`.
-/
theorem positive_inner_self_eq_zero {ρ : H n →ₗ[ℂ] H n} (hρ : LinearMap.IsSymmetric ρ)
    (hnn : ∀ z : H n, 0 ≤ (⟪ρ z, z⟫_ℂ).re) {y : H n} (hy : ⟪ρ y, y⟫_ℂ = 0) :
    ρ y = 0 := by
  have hy_re : (⟪ρ y, y⟫_ℂ).re = 0 := by rw [hy]; simp
  have hlin_re : ∀ z : H n, (⟪ρ y, z⟫_ℂ).re = 0 := by
    intro z
    have hzy_conj : ⟪ρ z, y⟫_ℂ = starRingEnd ℂ ⟪ρ y, z⟫_ℂ := by
      rw [hρ z y, ← inner_conj_symm z (ρ y)]
    have hquad : ∀ t : ℝ, 0 ≤ t * (⟪ρ y, z⟫_ℂ).re + t * (⟪ρ y, z⟫_ℂ).re
        + t * t * (⟪ρ z, z⟫_ℂ).re := by
      intro t
      have hpos := hnn (y + (t : ℂ) • z)
      have hexpand : ⟪ρ (y + (t : ℂ) • z), y + (t : ℂ) • z⟫_ℂ
          = ⟪ρ y, y⟫_ℂ + (t : ℂ) * ⟪ρ y, z⟫_ℂ + (t : ℂ) * (starRingEnd ℂ ⟪ρ y, z⟫_ℂ)
            + ((t * t : ℝ) : ℂ) * ⟪ρ z, z⟫_ℂ := by
        rw [map_add, map_smul, inner_add_left, inner_add_right, inner_add_right,
          inner_smul_left, inner_smul_right, inner_smul_left, inner_smul_right,
          Complex.conj_ofReal, hzy_conj]
        push_cast
        ring
      rw [hexpand] at hpos
      simp only [Complex.add_re, Complex.re_ofReal_mul, Complex.conj_re, hy_re, zero_add]
        at hpos
      linarith [hpos]
    set K : ℝ := (⟪ρ z, z⟫_ℂ).re with hK_def
    set B : ℝ := (⟪ρ y, z⟫_ℂ).re with hB_def
    have hquad' : ∀ t : ℝ, 0 ≤ t ^ 2 * K + 2 * t * B := by
      intro t; have := hquad t; nlinarith [this]
    have hK_nonneg : 0 ≤ K := hnn z
    by_contra hBne
    set t0 : ℝ := -B / (K + 1) with ht0_def
    have hden_pos : 0 < K + 1 := by linarith
    have hcontra : t0 ^ 2 * K + 2 * t0 * B = B ^ 2 * (-K - 2) / (K + 1) ^ 2 := by
      rw [ht0_def]; field_simp; ring
    have hBsq_pos : 0 < B ^ 2 := by positivity
    have hneg : B ^ 2 * (-K - 2) / (K + 1) ^ 2 < 0 := by
      apply div_neg_of_neg_of_pos
      · nlinarith [hBsq_pos, hK_nonneg]
      · positivity
    linarith [hquad' t0, hcontra, hneg]
  have hall_zero : ∀ z : H n, ⟪ρ y, z⟫_ℂ = 0 := by
    intro z
    have h1 : (⟪ρ y, z⟫_ℂ).re = 0 := hlin_re z
    have h3 : (⟪ρ y, z⟫_ℂ).im = 0 := by
      have h2' := hlin_re (Complex.I • z)
      rw [inner_smul_right, Complex.mul_re, Complex.I_re, Complex.I_im] at h2'
      linarith [h2']
    exact Complex.ext h1 h3
  have hfinal := hall_zero (ρ y)
  rwa [inner_self_eq_zero] at hfinal

namespace ProjMeasure

variable (m : ProjMeasure n)

/--
**FR.** Premier exercice de preuve (M1) : `μ ⊥ = 0`.
Indication : `⊥ ⟂ ⊥` et `⊥ ⊔ ⊥ = ⊥`, donc `μ ⊥ = 2 * μ ⊥`.

**EN.** First proof exercise (M1): `μ ⊥ = 0`.
Hint: `⊥ ⟂ ⊥` and `⊥ ⊔ ⊥ = ⊥`, so `μ ⊥ = 2 * μ ⊥`.
-/
theorem bot_eq_zero : m.μ ⊥ = 0 := by
  have h := m.add_isOrtho ⊥ ⊥ (Submodule.IsOrtho.symm (Submodule.isOrtho_bot_left))
  simp at h
  linarith

/--
**FR.** Additivité avec le complément orthogonal : `μ A + μ Aᗮ = 1`.
Indication : en dimension finie, `A ⊔ Aᗮ = ⊤` et `A ⟂ Aᗮ`.

**EN.** Additivity with the orthogonal complement: `μ A + μ Aᗮ = 1`.
Hint: in finite dimension, `A ⊔ Aᗮ = ⊤` and `A ⟂ Aᗮ`.
-/
theorem add_orthogonal_compl (A : Submodule ℂ (H n)) : m.μ A + m.μ Aᗮ = 1 := by
  rw [← m.top_eq_one, ← Submodule.sup_orthogonal_of_hasOrthogonalProjection (K := A)]
  exact (m.add_isOrtho A Aᗮ (Submodule.isOrtho_orthogonal_right A)).symm

/--
**FR.** Toute valeur est ≤ 1. Conséquence de `add_orthogonal_compl` et `nonneg`.

**EN.** Every value is ≤ 1. Consequence of `add_orthogonal_compl` and `nonneg`.
-/
theorem le_one (A : Submodule ℂ (H n)) : m.μ A ≤ 1 := by
  linarith [m.add_orthogonal_compl A, m.nonneg Aᗮ]

/--
**FR.** Monotonie : si `A ≤ B` alors `μ A ≤ μ B`.
Indication : `B = A ⊔ (B ⊓ Aᗮ)` en dimension finie, et les deux morceaux sont orthogonaux.

**EN.** Monotonicity: if `A ≤ B` then `μ A ≤ μ B`.
Hint: `B = A ⊔ (B ⊓ Aᗮ)` in finite dimension, and the two pieces are orthogonal.
-/
theorem mono {A B : Submodule ℂ (H n)} (h : A ≤ B) : m.μ A ≤ m.μ B := by
  have hdecomp := Submodule.sup_orthogonal_inf_of_hasOrthogonalProjection h
  have hortho : A ⟂ (Aᗮ ⊓ B) :=
    (Submodule.isOrtho_orthogonal_right A).mono_right inf_le_left
  rw [← hdecomp, m.add_isOrtho _ _ hortho]
  linarith [m.nonneg (Aᗮ ⊓ B)]

end ProjMeasure

end
end Gleason
