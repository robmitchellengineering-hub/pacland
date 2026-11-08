import Gleason.Complex.Patching

/-!
**FR.** # Réalisation opératorielle (phase O)

De la forme quadratique/sesquilinéaire à l'opérateur densité : positivité, trace 1,
unicité, et formule de Born sur tous les sous-espaces. Cette phase est PARTAGÉE entre
Busch et Gleason — la prouver d'abord côté Busch (M-B) amortit le travail.

**EN.** # Operator realization (phase O)

From the quadratic/sesquilinear form to the density operator: positivity, trace 1,
uniqueness, and the Born formula on all subspaces. This phase is SHARED between
Busch and Gleason — proving it first on the Busch side (M-B) amortizes the work.
-/

namespace Gleason

open scoped InnerProductSpace

noncomputable section

variable {n : ℕ}

/--
**FR.** **O0.** Unicité : un opérateur symétrique est déterminé par sa forme quadratique sur la
sphère unité (polarisation complexe ; spécifique à ℂ, faux sur ℝ pour les non-symétriques).
Mathlib : `ext_inner_map` (polarisation complexe, sans hypothèse de symétrie sur les deux
opérateurs — la symétrie sert seulement à passer de l'égalité des parties RÉELLES sur la
sphère à l'égalité COMPLEXE partout).

**EN.** **O0.** Uniqueness: a symmetric operator is determined by its quadratic form
on the unit sphere (complex polarization; specific to ℂ, false over ℝ for
non-symmetric operators). Mathlib: `ext_inner_map` (complex polarization, with no
symmetry hypothesis on either operator — symmetry is only used to pass from
equality of the REAL parts on the sphere to COMPLEX equality everywhere).
-/
theorem symmetric_ext_of_quadratic {ρ₁ ρ₂ : H n →ₗ[ℂ] H n}
    (h₁ : LinearMap.IsSymmetric ρ₁) (h₂ : LinearMap.IsSymmetric ρ₂)
    (h : ∀ x : H n, ‖x‖ = 1 → (⟪ρ₁ x, x⟫_ℂ).re = (⟪ρ₂ x, x⟫_ℂ).re) :
    ρ₁ = ρ₂ := by
  rw [← ext_inner_map]
  intro x
  by_cases hx0 : x = 0
  · subst hx0; simp
  have hxnorm : ‖x‖ ≠ 0 := norm_ne_zero_iff.mpr hx0
  set u : H n := (‖x‖⁻¹ : ℂ) • x with hu_def
  have hunorm : ‖u‖ = 1 := by
    rw [hu_def, norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_norm,
      inv_mul_cancel₀ hxnorm]
  have hx_eq : x = (‖x‖ : ℂ) • u := by
    rw [hu_def, smul_smul, ← Complex.ofReal_inv, ← Complex.ofReal_mul,
      mul_inv_cancel₀ hxnorm, Complex.ofReal_one, one_smul]
  have hreal1 : (⟪ρ₁ u, u⟫_ℂ).im = 0 := by
    apply Complex.conj_eq_iff_im.mp; exact h₁.conj_inner_sym u u
  have hreal2 : (⟪ρ₂ u, u⟫_ℂ).im = 0 := by
    apply Complex.conj_eq_iff_im.mp; exact h₂.conj_inner_sym u u
  have hux : ⟪ρ₁ u, u⟫_ℂ = ⟪ρ₂ u, u⟫_ℂ := Complex.ext (h u hunorm) (by rw [hreal1, hreal2])
  have hscale : ∀ T : H n →ₗ[ℂ] H n, ⟪T x, x⟫_ℂ = (‖x‖ : ℂ) ^ 2 * ⟪T u, u⟫_ℂ := by
    intro T
    conv_lhs => rw [hx_eq]
    rw [map_smul, inner_smul_left, inner_smul_right, Complex.conj_ofReal]
    ring
  rw [hscale ρ₁, hscale ρ₂, hux]

/--
**FR.** **O1.** La valeur de Born d'une droite est la forme quadratique :
`tr (ρ P_{ℂ∙x}) = ⟪ρ x, x⟫` pour `‖x‖ = 1`. Même calcul que la positivité de `busch`
(`Busch/Main.lean`, via `Submodule.starProjection_singleton` et `trace_rankOne`) ; aucune
hypothèse de symétrie sur `ρ` n'est nécessaire (seule la conjugaison `⟪x,ρx⟫ = conj ⟪ρx,x⟫`
sert à passer de l'un à l'autre, qui ont même partie réelle).

**EN.** **O1.** The Born value of a line is the quadratic form:
`tr (ρ P_{ℂ∙x}) = ⟪ρ x, x⟫` for `‖x‖ = 1`. Same computation as the positivity of
`busch` (`Busch/Main.lean`, via `Submodule.starProjection_singleton` and
`trace_rankOne`); no symmetry hypothesis on `ρ` is needed (only the conjugation
`⟪x,ρx⟫ = conj ⟪ρx,x⟫` is used to pass from one to the other, which share the same
real part).
-/
theorem bornValue_span_singleton (ρ : H n →ₗ[ℂ] H n) (x : H n) (hx : ‖x‖ = 1) :
    bornValue ρ (ℂ ∙ x) = (⟪ρ x, x⟫_ℂ).re := by
  unfold bornValue
  have hcomp : ρ ∘ₗ projL (ℂ ∙ x : Submodule ℂ (H n))
      = ((‖x‖ ^ 2 : ℝ) : ℂ)⁻¹ • (InnerProductSpace.rankOne ℂ (ρ x) x : H n →ₗ[ℂ] H n) := by
    ext1 w
    simp only [LinearMap.comp_apply, projL, ContinuousLinearMap.coe_coe,
      Submodule.starProjection_singleton ℂ, map_smul, LinearMap.smul_apply,
      InnerProductSpace.rankOne_apply, smul_smul, div_eq_inv_mul]
    rfl
  rw [hcomp]
  simp only [map_smul, smul_eq_mul, InnerProductSpace.trace_rankOne, hx, one_pow,
    Complex.ofReal_one, inv_one, one_mul]
  rw [show ⟪x, ρ x⟫_ℂ = starRingEnd ℂ ⟪ρ x, x⟫_ℂ from (inner_conj_symm x (ρ x)).symm,
    Complex.conj_re]

/--
**FR.** **O2a(ii).** Version `Finset` de `projL_sup_of_isOrtho` : pour une famille finie de
sous-espaces deux à deux orthogonaux, la projection sur le sup est la somme des
projections. Même induction que `ProjMeasure.sum_eq_of_pairwise_isOrtho` (M3-1).

**EN.** **O2a(ii).** `Finset` version of `projL_sup_of_isOrtho`: for a finite family of
pairwise orthogonal subspaces, the projection onto the sup is the sum of the
projections. Same induction as `ProjMeasure.sum_eq_of_pairwise_isOrtho` (M3-1).
-/
theorem projL_sup_of_pairwise_isOrtho {ι : Type*} [DecidableEq ι] (s : Finset ι)
    (A : ι → Submodule ℂ (H n)) (hortho : ∀ i ∈ s, ∀ j ∈ s, i ≠ j → A i ⟂ A j) :
    projL (s.sup A) = ∑ i ∈ s, projL (A i) := by
  induction s using Finset.induction with
  | empty => simp [projL]
  | insert i s hi ih =>
    have hi_ortho : A i ⟂ s.sup A := by
      apply Finset.sup_induction Submodule.isOrtho_bot_right
        (fun a1 h1 a2 h2 => Submodule.isOrtho_sup_right.mpr ⟨h1, h2⟩)
      intro j hj
      exact hortho i (Finset.mem_insert_self i s) j (Finset.mem_insert_of_mem hj)
        (fun heq => hi (heq ▸ hj))
    have hs_sub : ∀ j ∈ s, ∀ k ∈ s, j ≠ k → A j ⟂ A k := fun j hj k hk hjk =>
      hortho j (Finset.mem_insert_of_mem hj) k (Finset.mem_insert_of_mem hk) hjk
    rw [Finset.sup_insert, projL_sup_of_isOrtho hi_ortho, ih hs_sub, Finset.sum_insert hi]

/--
**FR.** **O2a(iii).** `bornValue ρ` est finiment additive sur les familles orthogonales : la
trace distribue sur `+` (`map_sum`), et `Re` distribue sur les sommes finies.

**EN.** **O2a(iii).** `bornValue ρ` is finitely additive over orthogonal families: the
trace distributes over `+` (`map_sum`), and `Re` distributes over finite sums.
-/
theorem bornValue_sum_of_pairwise_isOrtho (ρ : H n →ₗ[ℂ] H n) {ι : Type*} [DecidableEq ι]
    (s : Finset ι) (A : ι → Submodule ℂ (H n))
    (hortho : ∀ i ∈ s, ∀ j ∈ s, i ≠ j → A i ⟂ A j) :
    bornValue ρ (s.sup A) = ∑ i ∈ s, bornValue ρ (A i) := by
  unfold bornValue
  rw [projL_sup_of_pairwise_isOrtho s A hortho]
  have hcomp_sum : ρ ∘ₗ (∑ i ∈ s, projL (A i)) = ∑ i ∈ s, ρ ∘ₗ projL (A i) := by
    ext v
    simp [LinearMap.comp_apply, LinearMap.sum_apply, map_sum]
  rw [hcomp_sum, map_sum, Complex.re_sum]

/--
**FR.** **O2.** De la représentation quadratique sur les droites à la formule de Born sur TOUS
les sous-espaces : `A` se découpe en droites orthogonales (base orthonormée de `A` vu comme
espace de Hilbert en soi), et l'égalité passe à la somme des deux côtés (M3-1 pour `μ`,
O2a(iii) pour `bornValue`).

**EN.** **O2.** From the quadratic representation on lines to the Born formula on ALL
subspaces: `A` splits into orthogonal lines (an orthonormal basis of `A` viewed as a
Hilbert space in its own right), and the equality passes to the sum on both sides
(M3-1 for `μ`, O2a(iii) for `bornValue`).
-/
theorem born_of_quadratic (m : ProjMeasure n) (ρ : H n →ₗ[ℂ] H n)
    (_hρ : LinearMap.IsSymmetric ρ)
    (h : ∀ x : H n, ‖x‖ = 1 → m.frameFunction x = (⟪ρ x, x⟫_ℂ).re) :
    ∀ A : Submodule ℂ (H n), m.μ A = bornValue ρ A := by
  intro A
  set k := Module.finrank ℂ A with hk_def
  set e : OrthonormalBasis (Fin k) ℂ A := stdOrthonormalBasis ℂ A with he_def
  have heunit : ∀ i, ‖(e i : H n)‖ = 1 := fun i => by
    rw [Submodule.norm_coe]; exact e.norm_eq_one i
  have hortho : ∀ i ∈ (Finset.univ : Finset (Fin k)), ∀ j ∈ (Finset.univ : Finset (Fin k)),
      i ≠ j → (ℂ ∙ (e i : H n) : Submodule ℂ (H n)) ⟂ (ℂ ∙ (e j : H n) : Submodule ℂ (H n)) := by
    intro i _ j _ hij
    rw [Submodule.isOrtho_span]
    rintro x hx y hy
    simp only [Set.mem_singleton_iff] at hx hy
    rw [hx, hy, ← Submodule.coe_inner, e.inner_eq_ite]
    simp [hij]
  have hspan_eq : Submodule.span ℂ (Set.range (fun i => (e i : H n))) = A := by
    have heq : (fun i : Fin k => (e i : H n)) = A.subtype ∘ e.toBasis := by
      funext i; simp
    rw [heq, Set.range_comp, Submodule.span_image, e.toBasis.span_eq, Submodule.map_subtype_top]
  have htop : (Finset.univ : Finset (Fin k)).sup
      (fun i => (ℂ ∙ (e i : H n) : Submodule ℂ (H n))) = A := by
    rw [Finset.sup_eq_iSup]
    simp only [Finset.mem_univ, iSup_pos]
    rw [← Submodule.span_range_eq_iSup]
    exact hspan_eq
  have hsum := m.sum_eq_of_pairwise_isOrtho Finset.univ
    (fun i => (ℂ ∙ (e i : H n) : Submodule ℂ (H n))) hortho
  have hstep : ∀ i, m.μ (ℂ ∙ (e i : H n) : Submodule ℂ (H n))
      = bornValue ρ (ℂ ∙ (e i : H n) : Submodule ℂ (H n)) := by
    intro i
    show m.frameFunction (e i : H n) = bornValue ρ (ℂ ∙ (e i : H n) : Submodule ℂ (H n))
    rw [h (e i : H n) (heunit i), bornValue_span_singleton ρ (e i : H n) (heunit i)]
  calc m.μ A
      = m.μ ((Finset.univ : Finset (Fin k)).sup (fun i => (ℂ ∙ (e i : H n) : Submodule ℂ (H n))))
        := by rw [htop]
    _ = ∑ i, m.μ (ℂ ∙ (e i : H n) : Submodule ℂ (H n)) := hsum
    _ = ∑ i, bornValue ρ (ℂ ∙ (e i : H n) : Submodule ℂ (H n)) :=
        Finset.sum_congr rfl (fun i _ => hstep i)
    _ = bornValue ρ ((Finset.univ : Finset (Fin k)).sup
          (fun i => (ℂ ∙ (e i : H n) : Submodule ℂ (H n)))) :=
        (bornValue_sum_of_pairwise_isOrtho ρ Finset.univ
          (fun i => (ℂ ∙ (e i : H n) : Submodule ℂ (H n))) hortho).symm
    _ = bornValue ρ A := by rw [htop]

/--
**FR.** **O3.** Positivité et trace 1 de l'opérateur obtenu, à partir de la positivité de la
mesure et de `μ ⊤ = 1`.

**EN.** **O3.** Positivity and trace 1 of the resulting operator, from the positivity
of the measure and `μ ⊤ = 1`.
-/
theorem isDensityOperator_of_represents (m : ProjMeasure n) (ρ : H n →ₗ[ℂ] H n)
    (hρ : LinearMap.IsSymmetric ρ)
    (h : ∀ x : H n, ‖x‖ = 1 → m.frameFunction x = (⟪ρ x, x⟫_ℂ).re) :
    IsDensityOperator ρ := by
  refine ⟨hρ, ?_, ?_⟩
  · -- Positivité : 0 ≤ Re⟪ρ x, x⟫
    intro x
    by_cases hx0 : x = 0
    · subst hx0; simp
    set t : ℝ := ‖x‖⁻¹ with ht_def
    have htpos : 0 < t := by rw [ht_def]; positivity
    set u : H n := (t : ℂ) • x with hu_def
    have hunorm : ‖u‖ = 1 := by
      rw [hu_def, norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_of_pos htpos, ht_def,
        inv_mul_cancel₀ (norm_ne_zero_iff.mpr hx0)]
    have hframe : m.frameFunction u = m.μ (ℂ ∙ u) := rfl
    have hre_u : 0 ≤ (⟪ρ u, u⟫_ℂ).re := by
      rw [← h u hunorm, hframe]; exact m.nonneg _
    have hscale : ⟪ρ u, u⟫_ℂ = ((t ^ 2 : ℝ) : ℂ) * ⟪ρ x, x⟫_ℂ := by
      rw [hu_def, map_smul, inner_smul_left, inner_smul_right, Complex.conj_ofReal]
      push_cast; ring
    rw [hscale, Complex.re_ofReal_mul] at hre_u
    exact nonneg_of_mul_nonneg_right hre_u (by positivity)
  · -- Trace 1 : Re tr ρ = 1 (via O2 en A = ⊤), Im tr ρ = 0 (symétrie de ρ)
    have hprojL_top : projL (⊤ : Submodule ℂ (H n)) = 1 := by
      simp [projL, Submodule.starProjection_top']
    have hcomp : ρ ∘ₗ projL (⊤ : Submodule ℂ (H n)) = ρ := by
      rw [hprojL_top]; exact mul_one ρ
    have heq : bornValue ρ (⊤ : Submodule ℂ (H n)) = 1 := by
      rw [← born_of_quadratic m ρ hρ h ⊤]; exact m.top_eq_one
    unfold bornValue at heq
    rw [hcomp] at heq
    have him : (LinearMap.trace ℂ (H n) ρ).im = 0 := by
      rw [LinearMap.trace_eq_sum_inner ρ (EuclideanSpace.basisFun (Fin n) ℂ), Complex.im_sum]
      apply Finset.sum_eq_zero
      intro i _
      apply Complex.conj_eq_iff_im.mp
      set bi := EuclideanSpace.basisFun (Fin n) ℂ i
      calc (starRingEnd ℂ) ⟪bi, ρ bi⟫_ℂ
          = ⟪ρ bi, bi⟫_ℂ := inner_conj_symm (𝕜 := ℂ) (ρ bi) bi
        _ = ⟪bi, ρ bi⟫_ℂ := hρ bi bi
    exact Complex.ext heq (by simpa using him)

end
end Gleason
