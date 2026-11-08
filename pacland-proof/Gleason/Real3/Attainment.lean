import Gleason.Real3.ExactPole

/-!
**FR.** # Attention des valeurs extrémales (CKM 1985 §6, PDF p. 125-126)

`frameFunction_attains_sup`/`frameFunction_attains_inf` : toute frame function
BORNÉE (pas nécessairement positive : le bloc H l'appliquera à des différences
`g - f`) atteint son sup et son inf sur la sphère. Preuve par ultrafiltre
(l'espace produit `[2m,2M]^S` n'est pas métrisable, donc pas de sous-suites) :
limite `p` d'une suite maximisante le long d'un ultrafiltre, symétrisation par
rotation 90°, recentrage par isométrie, passage à la limite le long de
l'ultrafiltre de la forme quadratique exacte (bloc F), puis descente radiale
à 2 pas pour contredire une éventuelle perte de masse en `p`.

**EN.** # Attainment of extremal values (CKM 1985 §6, project PDF p. 125-126)

`frameFunction_attains_sup`/`frameFunction_attains_inf`: every BOUNDED frame
function (not necessarily positive: block H will apply it to differences `g - f`)
attains its sup and inf on the sphere. Proof by ultrafilter (the product space
`[2m,2M]^S` is not metrizable, so no subsequences): limit `p` of a maximizing
sequence along an ultrafilter, symmetrization by 90° rotation, recentering by
isometry, passing to the limit along the ultrafilter of the exact quadratic form
(block F), then a 2-step radial descent to rule out a possible loss of mass at `p`.
-/

namespace Gleason

open scoped RealInnerProductSpace Real

noncomputable section

/- ═══════════════════════════════════════════════════════════════════
   G1. Boîte à outils isométries (réutilisable par le bloc H).
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **G1a.** Deux triplets orthonormés se correspondent par une isométrie
linéaire de `E3` : bases orthonormées prescrites (`exists_orthonormalBasis_of_triple'`)
des deux côtés, puis composition des représentations (`repr.trans repr.symm`),
même technique que dans `exists_frame_with_lat` (B7).

**EN.** **G1a.** Two orthonormal triples correspond to each other via a linear
isometry of `E3`: prescribed orthonormal bases on both sides
(`exists_orthonormalBasis_of_triple'`), then composing the representations
(`repr.trans repr.symm`), the same technique as in `exists_frame_with_lat` (B7).
-/
theorem isometry_of_orthonormal_triples {a0 a1 a2 b0 b1 b2 : E3}
    (ha0 : ‖a0‖ = 1) (ha1 : ‖a1‖ = 1) (ha2 : ‖a2‖ = 1)
    (ha01 : ⟪a0, a1⟫ = 0) (ha02 : ⟪a0, a2⟫ = 0) (ha12 : ⟪a1, a2⟫ = 0)
    (hb0 : ‖b0‖ = 1) (hb1 : ‖b1‖ = 1) (hb2 : ‖b2‖ = 1)
    (hb01 : ⟪b0, b1⟫ = 0) (hb02 : ⟪b0, b2⟫ = 0) (hb12 : ⟪b1, b2⟫ = 0) :
    ∃ ρ : E3 ≃ₗᵢ[ℝ] E3, ρ a0 = b0 ∧ ρ a1 = b1 ∧ ρ a2 = b2 := by
  obtain ⟨a, ha0', ha1', ha2'⟩ :=
    exists_orthonormalBasis_of_triple' a0 a1 a2 ha0 ha1 ha2 ha01 ha02 ha12
  obtain ⟨b, hb0', hb1', hb2'⟩ :=
    exists_orthonormalBasis_of_triple' b0 b1 b2 hb0 hb1 hb2 hb01 hb02 hb12
  set ρ : E3 ≃ₗᵢ[ℝ] E3 := a.repr.trans b.repr.symm with hρ_def
  have key : ∀ i : Fin 3, ρ (a i) = b i := by
    intro i
    have h1 : a.repr (a i) = EuclideanSpace.single i (1 : ℝ) := a.repr_self i
    have h2 : b.repr (b i) = EuclideanSpace.single i (1 : ℝ) := b.repr_self i
    rw [hρ_def, LinearIsometryEquiv.trans_apply, h1, ← h2, LinearIsometryEquiv.symm_apply_apply]
  exact ⟨ρ, by rw [← ha0', key 0, hb0'], by rw [← ha1', key 1, hb1'], by rw [← ha2', key 2, hb2']⟩

/--
**FR.** **G1a' (variante paire, outil interne).** Même énoncé pour une paire
orthonormée, via `exists_orthonormalBasis_pair`.

**EN.** **G1a' (pair variant, internal tool).** Same statement for an orthonormal
pair, via `exists_orthonormalBasis_pair`.
-/
theorem isometry_of_orthonormal_pair {a0 a1 b0 b1 : E3}
    (ha0 : ‖a0‖ = 1) (ha1 : ‖a1‖ = 1) (ha01 : ⟪a0, a1⟫ = 0)
    (hb0 : ‖b0‖ = 1) (hb1 : ‖b1‖ = 1) (hb01 : ⟪b0, b1⟫ = 0) :
    ∃ ρ : E3 ≃ₗᵢ[ℝ] E3, ρ a0 = b0 ∧ ρ a1 = b1 := by
  obtain ⟨a, ha0', ha1'⟩ := exists_orthonormalBasis_pair a0 a1 ha0 ha1 ha01
  obtain ⟨b, hb0', hb1'⟩ := exists_orthonormalBasis_pair b0 b1 hb0 hb1 hb01
  set ρ : E3 ≃ₗᵢ[ℝ] E3 := a.repr.trans b.repr.symm with hρ_def
  have key : ∀ i : Fin 3, ρ (a i) = b i := by
    intro i
    have h1 : a.repr (a i) = EuclideanSpace.single i (1 : ℝ) := a.repr_self i
    have h2 : b.repr (b i) = EuclideanSpace.single i (1 : ℝ) := b.repr_self i
    rw [hρ_def, LinearIsometryEquiv.trans_apply, h1, ← h2, LinearIsometryEquiv.symm_apply_apply]
  exact ⟨ρ, by rw [← ha0', key 0, hb0'], by rw [← ha1', key 1, hb1']⟩

/--
**FR.** **G1a'' (unitaire simple, outil interne).** Un seul vecteur : cas
dégénéré de G1a' (`exists_orthonormalBasis_fst` des deux côtés).

**EN.** **G1a'' (single unit vector, internal tool).** A single vector: degenerate
case of G1a' (`exists_orthonormalBasis_fst` on both sides).
-/
theorem exists_isometry_of_unit {x y : E3} (hx : ‖x‖ = 1) (hy : ‖y‖ = 1) :
    ∃ ρ : E3 ≃ₗᵢ[ℝ] E3, ρ x = y := by
  obtain ⟨a, ha0⟩ := exists_orthonormalBasis_fst x hx
  obtain ⟨b, hb0⟩ := exists_orthonormalBasis_fst y hy
  set ρ : E3 ≃ₗᵢ[ℝ] E3 := a.repr.trans b.repr.symm with hρ_def
  have h1 : a.repr (a 0) = EuclideanSpace.single 0 (1 : ℝ) := a.repr_self 0
  have h2 : b.repr (b 0) = EuclideanSpace.single 0 (1 : ℝ) := b.repr_self 0
  exact ⟨ρ, by rw [← ha0, hρ_def, LinearIsometryEquiv.trans_apply, h1, ← h2,
    LinearIsometryEquiv.symm_apply_apply, hb0]⟩

/--
**FR.** **G1b.** Deux paires de vecteurs unitaires de même produit scalaire se
correspondent par une isométrie. Cas `c² = 1` (colinéaire) : `u2 = c•u1` et
`v2 = c•v1` par annulation de `norm_sq_sub_inner_smul` (égalité de
Cauchy-Schwarz, dérivée directement plutôt que via un lemme Mathlib nommé),
toute isométrie envoyant `u1` sur `v1` convient (linéarité). Cas `c² < 1` :
résidus de Gram-Schmidt `u2' := ‖u2-c•u1‖⁻¹•(u2-c•u1)`, `v2'` idem,
`isometry_of_orthonormal_pair` sur `(u1,u2')`/`(v1,v2')`, puis
`ρu2 = ρ(c•u1+√(1-c²)•u2') = c•v1+√(1-c²)•v2' = v2` par linéarité de `ρ`.

**EN.** **G1b.** Two pairs of unit vectors with the same inner product correspond to
each other via an isometry. Case `c² = 1` (collinear): `u2 = c•u1` and
`v2 = c•v1` from the vanishing of `norm_sq_sub_inner_smul` (Cauchy-Schwarz
equality case, derived directly rather than via a named Mathlib lemma), any
isometry sending `u1` to `v1` works (linearity). Case `c² < 1`: Gram-Schmidt
residues `u2' := ‖u2-c•u1‖⁻¹•(u2-c•u1)`, `v2'` likewise,
`isometry_of_orthonormal_pair` on `(u1,u2')`/`(v1,v2')`, then
`ρu2 = ρ(c•u1+√(1-c²)•u2') = c•v1+√(1-c²)•v2' = v2` by linearity of `ρ`.
-/
theorem exists_isometry_pair {u1 u2 v1 v2 : E3}
    (hu1 : ‖u1‖ = 1) (hu2 : ‖u2‖ = 1) (hv1 : ‖v1‖ = 1) (hv2 : ‖v2‖ = 1)
    (hc : ⟪u1, u2⟫ = ⟪v1, v2⟫) :
    ∃ ρ : E3 ≃ₗᵢ[ℝ] E3, ρ u1 = v1 ∧ ρ u2 = v2 := by
  set c : ℝ := ⟪u1, u2⟫ with hc_def
  have hcv : c = ⟪v1, v2⟫ := hc_def.trans hc
  have hc2le1 : c ^ 2 ≤ 1 := by
    have h := abs_real_inner_le_norm u1 u2
    rw [hu1, hu2, mul_one] at h
    nlinarith [abs_le.mp h]
  have collinear : ∀ {x y : E3}, ‖x‖ = 1 → ‖y‖ = 1 → ⟪x, y⟫ ^ 2 = 1 → y = ⟪x, y⟫ • x := by
    intro x y hx hy hxy2
    have hnormsq : ‖y - ⟪x, y⟫ • x‖ ^ 2 = 0 := by rw [norm_sq_sub_inner_smul hx hy, hxy2]; ring
    exact sub_eq_zero.mp (norm_eq_zero.mp (sq_eq_zero_iff.mp hnormsq))
  rcases hc2le1.eq_or_lt with hc2eq | hc2lt
  · have hu2eq : u2 = ⟪u1, u2⟫ • u1 := collinear hu1 hu2 (hc_def ▸ hc2eq)
    have hv2eq : v2 = ⟪v1, v2⟫ • v1 := collinear hv1 hv2 (hcv ▸ hc2eq)
    obtain ⟨ρ, hρ⟩ := exists_isometry_of_unit hu1 hv1
    refine ⟨ρ, hρ, ?_⟩
    rw [hu2eq, ρ.map_smul, hρ, ← hc_def, hc, ← hv2eq]
  · set r : ℝ := ‖u2 - c • u1‖ with hr_def
    have hnormsq_u : r ^ 2 = 1 - c ^ 2 := by rw [hr_def]; exact norm_sq_sub_inner_smul hu1 hu2
    have hrpos : 0 < r := by
      have hr2pos : 0 < r ^ 2 := by rw [hnormsq_u]; linarith
      have hrnn : 0 ≤ r := hr_def ▸ norm_nonneg _
      rcases hrnn.eq_or_lt with h | h
      · exfalso; rw [← h] at hr2pos; norm_num at hr2pos
      · exact h
    set u2' : E3 := r⁻¹ • (u2 - c • u1) with hu2'_def
    have hu2'norm : ‖u2'‖ = 1 := by
      rw [hu2'_def, norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos hrpos, ← hr_def]
      exact inv_mul_cancel₀ hrpos.ne'
    have hu1u2'_orth : ⟪u1, u2'⟫ = 0 := by
      rw [hu2'_def, real_inner_smul_right, inner_sub_right, real_inner_smul_right,
        real_inner_self_eq_norm_sq, hu1, ← hc_def]
      ring
    have hu2_decomp : u2 = c • u1 + r • u2' := by
      rw [hu2'_def, smul_smul, mul_inv_cancel₀ hrpos.ne', one_smul]
      abel
    set r' : ℝ := ‖v2 - c • v1‖ with hr'_def
    have hnormsq_v : r' ^ 2 = 1 - c ^ 2 := by
      have h := norm_sq_sub_inner_smul hv1 hv2
      rw [← hcv] at h
      rw [hr'_def]; exact h
    have hr'r : r' = r := by
      have heq2 : r' ^ 2 = r ^ 2 := by rw [hnormsq_v, hnormsq_u]
      have hr'nn : 0 ≤ r' := norm_nonneg _
      have hrnn : 0 ≤ r := norm_nonneg _
      nlinarith [heq2, hr'nn, hrnn]
    have hr'pos : 0 < r' := hr'r ▸ hrpos
    set v2' : E3 := r'⁻¹ • (v2 - c • v1) with hv2'_def
    have hv2'norm : ‖v2'‖ = 1 := by
      rw [hv2'_def, norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos hr'pos, ← hr'_def]
      exact inv_mul_cancel₀ hr'pos.ne'
    have hv1v2'_orth : ⟪v1, v2'⟫ = 0 := by
      rw [hv2'_def, real_inner_smul_right, inner_sub_right, real_inner_smul_right,
        real_inner_self_eq_norm_sq, hv1, ← hcv]
      ring
    have hv2_decomp : v2 = c • v1 + r' • v2' := by
      rw [hv2'_def, smul_smul, mul_inv_cancel₀ hr'pos.ne', one_smul]
      abel
    obtain ⟨ρ, hρ1, hρ2⟩ := isometry_of_orthonormal_pair hu1 hu2'norm hu1u2'_orth
      hv1 hv2'norm hv1v2'_orth
    refine ⟨ρ, hρ1, ?_⟩
    rw [hu2_decomp, ρ.map_add, ρ.map_smul, ρ.map_smul, hρ1, hρ2, ← hr'r, ← hv2_decomp]

/--
**FR.** **G1c.** `f ∘ ρ` (pour `ρ` une isométrie linéaire) est une frame function
du même poids : l'image d'une base orthonormée par `ρ` en est une
(`OrthonormalBasis.map`).

**EN.** **G1c.** `f ∘ ρ` (for `ρ` a linear isometry) is a frame function of the same
weight: the image of an orthonormal basis under `ρ` is one (`OrthonormalBasis.map`).
-/
theorem IsFrameFunction.comp_isometry {f : E3 → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (ρ : E3 ≃ₗᵢ[ℝ] E3) : IsFrameFunction (f ∘ ρ) W := by
  intro b
  have h := hf (b.map ρ)
  simpa [Function.comp, OrthonormalBasis.map_apply] using h

/--
**FR.** **G1d.** Somme, négation et constante de frame functions.

**EN.** **G1d.** Sum, negation, and constant of frame functions.
-/
theorem IsFrameFunction.add {f g : E3 → ℝ} {Wf Wg : ℝ}
    (hf : IsFrameFunction f Wf) (hg : IsFrameFunction g Wg) :
    IsFrameFunction (fun x => f x + g x) (Wf + Wg) := by
  intro b
  have h1 := hf b
  have h2 := hg b
  rw [Fin.sum_univ_three] at h1 h2 ⊢
  linarith

theorem IsFrameFunction.neg {f : E3 → ℝ} {W : ℝ} (hf : IsFrameFunction f W) :
    IsFrameFunction (fun x => -f x) (-W) := by
  intro b
  have h := hf b
  rw [Fin.sum_univ_three] at h ⊢
  linarith

theorem IsFrameFunction.const (c : ℝ) : IsFrameFunction (fun _ => c) (3 * c) := by
  intro b
  rw [Fin.sum_univ_three]
  ring

theorem IsFrameFunction.sub {f g : E3 → ℝ} {Wf Wg : ℝ}
    (hf : IsFrameFunction f Wf) (hg : IsFrameFunction g Wg) :
    IsFrameFunction (fun x => f x - g x) (Wf - Wg) := by
  have := hf.add hg.neg
  simpa [sub_eq_add_neg] using this

/- ═══════════════════════════════════════════════════════════════════
   G2. Rotation de 90° autour du pôle.
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **G2.** Isométrie de rotation de 90° autour de `p` : complète `p` en base
`(p,u1,u2)`, envoie `(p,u1,u2) ↦ (p,u2,-u1)` (G1a). Fixe `p` ; envoie
l'équateur de `p` dans lui-même ; pour `s` sur l'équateur, `s` et son image
sont orthogonaux (décomposition `s = ⟪u1,s⟫•u1+⟪u2,s⟫•u2`, image
`⟪u1,s⟫•u2-⟪u2,s⟫•u1`, produit scalaire croisé nul par `⟪u1,u2⟫=0` et
normes unitaires). `u1` (renommé `e0` par G3) est exposé pour que le
recentrage de G3 et la descente de G8/G9 travaillent dans le même plan
méridien que la rotation.

**EN.** **G2.** 90° rotation isometry about `p`: completes `p` into a basis
`(p,u1,u2)`, sends `(p,u1,u2) ↦ (p,u2,-u1)` (G1a). Fixes `p`; sends `p`'s equator
into itself; for `s` on the equator, `s` and its image are orthogonal
(decomposition `s = ⟪u1,s⟫•u1+⟪u2,s⟫•u2`, image `⟪u1,s⟫•u2-⟪u2,s⟫•u1`, cross
inner product zero by `⟪u1,u2⟫=0` and unit norms). `u1` (renamed `e0` by G3) is
exposed so that the recentering of G3 and the descent of G8/G9 work in the same
meridian plane as the rotation.
-/
theorem exists_rotate90 {p : E3} (hp : ‖p‖ = 1) :
    ∃ (phat : E3 ≃ₗᵢ[ℝ] E3) (u1 u2 : E3), ‖u1‖ = 1 ∧ ‖u2‖ = 1 ∧
      ⟪p, u1⟫ = 0 ∧ ⟪p, u2⟫ = 0 ∧ ⟪u1, u2⟫ = 0 ∧
      phat p = p ∧ phat u1 = u2 ∧ phat u2 = -u1 ∧
      ∀ s ∈ equator p, phat s ∈ equator p ∧ ⟪s, phat s⟫ = 0 := by
  obtain ⟨b, hb0⟩ := exists_orthonormalBasis_fst p hp
  set u1 : E3 := b 1 with hu1_def
  set u2 : E3 := b 2 with hu2_def
  have hu1 : ‖u1‖ = 1 := b.norm_eq_one 1
  have hu2 : ‖u2‖ = 1 := b.norm_eq_one 2
  have hpu1 : ⟪p, u1⟫ = 0 := by rw [← hb0]; exact b.inner_eq_zero (by decide)
  have hpu2 : ⟪p, u2⟫ = 0 := by rw [← hb0]; exact b.inner_eq_zero (by decide)
  have hu1u2 : ⟪u1, u2⟫ = 0 := b.inner_eq_zero (by decide)
  have hu2u1 : ⟪u2, u1⟫ = 0 := by rw [real_inner_comm]; exact hu1u2
  have hpu1_neg : ⟪p, -u1⟫ = 0 := by rw [inner_neg_right, hpu1, neg_zero]
  have hu2u1_neg : ⟪u2, -u1⟫ = 0 := by rw [inner_neg_right, hu2u1, neg_zero]
  have hnegu1 : ‖(-u1 : E3)‖ = 1 := by rw [norm_neg]; exact hu1
  obtain ⟨ρ, hρp, hρu1, hρu2⟩ := isometry_of_orthonormal_triples hp hu1 hu2 hpu1 hpu2 hu1u2
    hp hu2 hnegu1 hpu2 hpu1_neg hu2u1_neg
  refine ⟨ρ, u1, u2, hu1, hu2, hpu1, hpu2, hu1u2, hρp, hρu1, hρu2, ?_⟩
  intro s hs
  have hsu : ‖s‖ = 1 := hs.1
  have hsp : ⟪p, s⟫ = 0 := hs.2
  have hpsnorm : ‖ρ s‖ = 1 := by rw [ρ.norm_map]; exact hsu
  have hpsp : ⟪p, ρ s⟫ = 0 := by rw [← hρp, ρ.inner_map_map]; exact hsp
  refine ⟨⟨hpsnorm, hpsp⟩, ?_⟩
  have hdecomp : ⟪u1, s⟫ • u1 + ⟪u2, s⟫ • u2 = s := by
    have h := b.sum_repr' s
    rw [Fin.sum_univ_three, hb0, hsp, zero_smul, zero_add, ← hu1_def, ← hu2_def] at h
    exact h
  set a : ℝ := ⟪u1, s⟫ with ha_def
  set d : ℝ := ⟪u2, s⟫ with hd_def
  have hrhos : ρ s = a • u2 - d • u1 := by
    rw [← hdecomp, ρ.map_add, ρ.map_smul, ρ.map_smul, hρu1, hρu2, smul_neg]
    abel
  rw [hrhos, ← hdecomp]
  simp only [inner_add_left, inner_sub_right, real_inner_smul_left, real_inner_smul_right,
    real_inner_self_eq_norm_sq, hu1, hu2, hu1u2, hu2u1]
  ring

/- ═══════════════════════════════════════════════════════════════════
   G3. Recentrage.
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **G3 (définition).** Point du méridien `(p,e0)` de latitude (signée) `c'`.

**EN.** **G3 (definition).** Point of the meridian `(p,e0)` of (signed) latitude `c'`.
-/
def recenter (p e0 : E3) (c' : ℝ) : E3 := c' • p + Real.sqrt (1 - c' ^ 2) • e0

/--
**FR.** **G3.** `recenter p e0 c'` est unitaire, de produit scalaire `c'` avec `p`,
pour `c' ∈ [0,1]` (le radicande `1-c'²` est alors `≥ 0`).

**EN.** **G3.** `recenter p e0 c'` is a unit vector, with inner product `c'` with `p`,
for `c' ∈ [0,1]` (the radicand `1-c'²` is then `≥ 0`).
-/
theorem recenter_prop {p e0 : E3} (hp : ‖p‖ = 1) (he0 : ‖e0‖ = 1) (hpe0 : ⟪p, e0⟫ = 0)
    {c' : ℝ} (hc'0 : 0 ≤ c') (hc'1 : c' ≤ 1) :
    ‖recenter p e0 c'‖ = 1 ∧ ⟪p, recenter p e0 c'⟫ = c' := by
  have hnn : (0 : ℝ) ≤ 1 - c' ^ 2 := by nlinarith
  have hinner : ⟪p, recenter p e0 c'⟫ = c' := by
    unfold recenter
    rw [inner_add_right, real_inner_smul_right, real_inner_smul_right, hpe0, mul_zero, add_zero,
      real_inner_self_eq_norm_sq, hp]
    ring
  refine ⟨?_, hinner⟩
  have hsq : ‖recenter p e0 c'‖ ^ 2 = 1 := by
    unfold recenter
    rw [norm_add_sq_real, real_inner_smul_left, real_inner_smul_right, hpe0, mul_zero, mul_zero]
    have h1 : ‖c' • p‖ ^ 2 = c' ^ 2 := by
      rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, hp]; ring
    have h2 : ‖Real.sqrt (1 - c' ^ 2) • e0‖ ^ 2 = 1 - c' ^ 2 := by
      rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, he0, Real.sq_sqrt hnn]; ring
    rw [h1, h2]
    ring
  have heq0 : (‖recenter p e0 c'‖ - 1) * (‖recenter p e0 c'‖ + 1) = 0 := by
    linear_combination hsq
  rcases mul_eq_zero.mp heq0 with h | h
  · linarith
  · linarith [norm_nonneg (recenter p e0 c')]

/--
**FR.** **G3.** `recenter p e0 c'` est dans `northern p`, de latitude `c'²`.

**EN.** **G3.** `recenter p e0 c'` lies in `northern p`, with latitude `c'²`.
-/
theorem recenter_northern {p e0 : E3} (hp : ‖p‖ = 1) (he0 : ‖e0‖ = 1) (hpe0 : ⟪p, e0⟫ = 0)
    {c' : ℝ} (hc'0 : 0 ≤ c') (hc'1 : c' ≤ 1) :
    recenter p e0 c' ∈ northern p ∧ lat p (recenter p e0 c') = c' ^ 2 := by
  obtain ⟨hn, hi⟩ := recenter_prop hp he0 hpe0 hc'0 hc'1
  refine ⟨⟨hn, by rw [hi]; exact hc'0⟩, ?_⟩
  unfold lat; rw [hi]

/--
**FR.** **G3 (assemblage).** Pour `q` unitaire avec `⟪p,q⟫ ∈ [0,1]`, il existe une
isométrie envoyant `recenter p e0 ⟪p,q⟫` sur `p` et `p` sur `q` :
`⟪recenter c', p⟫ = c' = ⟪p,q⟫` (G3, `real_inner_comm`), puis G1b.

**EN.** **G3 (assembly).** For `q` a unit vector with `⟪p,q⟫ ∈ [0,1]`, there exists an
isometry sending `recenter p e0 ⟪p,q⟫` to `p` and `p` to `q`:
`⟪recenter c', p⟫ = c' = ⟪p,q⟫` (G3, `real_inner_comm`), then G1b.
-/
theorem exists_recenter_isometry {p e0 q : E3} (hp : ‖p‖ = 1) (he0 : ‖e0‖ = 1)
    (hpe0 : ⟪p, e0⟫ = 0) (hq : ‖q‖ = 1) (hc'0 : 0 ≤ ⟪p, q⟫) :
    ∃ ρ : E3 ≃ₗᵢ[ℝ] E3, ρ (recenter p e0 ⟪p, q⟫) = p ∧ ρ p = q := by
  have hc'1 : ⟪p, q⟫ ≤ 1 := by
    have h := abs_real_inner_le_norm p q
    rw [hp, hq, mul_one] at h
    exact (abs_le.mp h).2
  obtain ⟨hrn, hri⟩ := recenter_prop hp he0 hpe0 hc'0 hc'1
  have hcomm : ⟪recenter p e0 ⟪p, q⟫, p⟫ = ⟪p, q⟫ := by rw [real_inner_comm]; exact hri
  exact exists_isometry_pair hrn hp hp hq hcomm

/- ═══════════════════════════════════════════════════════════════════
   G4. Symétrisation par la rotation de 90°.
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **G4a.** `g + g∘phat` est une frame function de poids `2W` (G1c + G1d).

**EN.** **G4a.** `g + g∘phat` is a frame function of weight `2W` (G1c + G1d).
-/
theorem symmetrize_frame {g : E3 → ℝ} {W : ℝ} (hg : IsFrameFunction g W)
    (phat : E3 ≃ₗᵢ[ℝ] E3) : IsFrameFunction (fun x => g x + g (phat x)) (2 * W) := by
  have h2 : IsFrameFunction (fun x => g x + (g ∘ phat) x) (W + W) :=
    hg.add (hg.comp_isometry phat)
  have hWW : (2 : ℝ) * W = W + W := by ring
  rwa [hWW]

/--
**FR.** **G4b.** Bornes héritées : `phat` préserve la norme.

**EN.** **G4b.** Inherited bounds: `phat` preserves the norm.
-/
theorem symmetrize_bounds {g : E3 → ℝ} {m M : ℝ} (phat : E3 ≃ₗᵢ[ℝ] E3)
    (hgm : ∀ t : E3, ‖t‖ = 1 → m ≤ g t) (hgM : ∀ t : E3, ‖t‖ = 1 → g t ≤ M)
    {t : E3} (ht : ‖t‖ = 1) :
    2 * m ≤ g t + g (phat t) ∧ g t + g (phat t) ≤ 2 * M := by
  have hphatt : ‖phat t‖ = 1 := by rw [phat.norm_map]; exact ht
  exact ⟨by linarith [hgm t ht, hgm (phat t) hphatt], by linarith [hgM t ht, hgM (phat t) hphatt]⟩

/--
**FR.** **G4c.** Sur l'équateur de `p`, `g + g∘phat` vaut la constante `W - g p` :
`(p,s,phat s)` est un triplet orthonormé (G2), donc `g p + g s + g(phat s) = W`
(somme de trame).

**EN.** **G4c.** On `p`'s equator, `g + g∘phat` equals the constant `W - g p`:
`(p,s,phat s)` is an orthonormal triple (G2), so `g p + g s + g(phat s) = W`
(frame sum).
-/
theorem symmetrize_equator {g : E3 → ℝ} {W : ℝ} (hg : IsFrameFunction g W)
    {phat : E3 ≃ₗᵢ[ℝ] E3} {p : E3} (hp : ‖p‖ = 1)
    (hphat_equator : ∀ s ∈ equator p, phat s ∈ equator p ∧ ⟪s, phat s⟫ = 0)
    {s : E3} (hs : s ∈ equator p) :
    g s + g (phat s) = W - g p := by
  obtain ⟨hpsE, hspd⟩ := hphat_equator s hs
  have hsu : ‖s‖ = 1 := hs.1
  have hsp : ⟪p, s⟫ = 0 := hs.2
  have hpsu : ‖phat s‖ = 1 := hpsE.1
  have hpsp : ⟪p, phat s⟫ = 0 := hpsE.2
  obtain ⟨b, hb0, hb1, hb2⟩ := exists_orthonormalBasis_of_triple' p s (phat s) hp hsu hpsu
    hsp hpsp hspd
  have h := hg b
  rw [Fin.sum_univ_three, hb0, hb1, hb2] at h
  linarith

/- ═══════════════════════════════════════════════════════════════════
   G5 (préliminaires). Limites le long d'un ultrafiltre dans un compact
   (l'espace produit `[2m,2M]^S` n'étant pas métrisable, pas de
   sous-suites : Gleason/CKM §6 utilise un ultrafiltre).
   ═══════════════════════════════════════════════════════════════════ -/

open Filter Topology

/--
**FR.** **G5a.** Toute suite de vecteurs unitaires admet, le long de l'ultrafiltre
`Ultrafilter.of atTop`, une limite unitaire (compacité de la sphère).

**EN.** **G5a.** Every sequence of unit vectors admits, along the ultrafilter
`Ultrafilter.of atTop`, a unit-vector limit (compactness of the sphere).
-/
theorem exists_ultrafilter_tendsto_sphere (u : ℕ → E3) (hu : ∀ n, ‖u n‖ = 1) :
    ∃ p : E3, ‖p‖ = 1 ∧
      Tendsto u (Ultrafilter.of (atTop : Filter ℕ) : Filter ℕ) (𝓝 p) := by
  set 𝒰 : Ultrafilter ℕ := Ultrafilter.of atTop with h𝒰_def
  have hmem : (Ultrafilter.map u 𝒰 : Filter E3) ≤ 𝓟 (Metric.sphere (0 : E3) 1) := by
    rw [Ultrafilter.coe_map, le_principal_iff, mem_map]
    filter_upwards [univ_mem] with n _
    simpa using hu n
  obtain ⟨p, hpmem, hp⟩ := (isCompact_sphere (0 : E3) 1).ultrafilter_le_nhds (Ultrafilter.map u 𝒰)
    hmem
  refine ⟨p, ?_, hp⟩
  simpa using hpmem

/--
**FR.** **G5a' (variante réelle).** Toute suite réelle à valeurs dans `[m,M]`
admet, le long de l'ultrafiltre, une limite dans `[m,M]` (compacité de
`Icc m M`).

**EN.** **G5a' (real variant).** Every real sequence with values in `[m,M]`
admits, along the ultrafilter, a limit in `[m,M]` (compactness of `Icc m M`).
-/
theorem exists_ultrafilter_tendsto_Icc {m M : ℝ} (u : ℕ → ℝ) (hu : ∀ n, u n ∈ Set.Icc m M) :
    ∃ L : ℝ, L ∈ Set.Icc m M ∧
      Tendsto u (Ultrafilter.of (atTop : Filter ℕ) : Filter ℕ) (𝓝 L) := by
  set 𝒰 : Ultrafilter ℕ := Ultrafilter.of atTop with h𝒰_def
  have hmem : (Ultrafilter.map u 𝒰 : Filter ℝ) ≤ 𝓟 (Set.Icc m M) := by
    rw [Ultrafilter.coe_map, le_principal_iff, mem_map]
    filter_upwards [univ_mem] with n _ using hu n
  exact isCompact_Icc.ultrafilter_le_nhds (Ultrafilter.map u 𝒰) hmem

/--
**FR.** **G9 (préliminaire).** Variante de F1b (`exists_inf_approx`) : dérive
`(m₀, hmlb, hm)` à partir d'une borne supérieure GÉNÉRALE `M` (pas
nécessairement `f p` pour un pôle) — c'est tout ce qu'il faut pour la borne
inférieure grossière ; réutilisé pour chaque `hₙ` en G9.

**EN.** **G9 (preliminary).** Variant of F1b (`exists_inf_approx`): derives
`(m₀, hmlb, hm)` from a GENERAL upper bound `M` (not necessarily `f p` for a pole)
— exactly what is needed for the crude lower bound; reused for each `hₙ` in G9.
-/
theorem exists_inf_approx_of_le {f : E3 → ℝ} {W M : ℝ} (hf : IsFrameFunction f W)
    (hM : ∀ t : E3, ‖t‖ = 1 → f t ≤ M) (p0 : E3) (hp0 : ‖p0‖ = 1) :
    ∃ m₀ : ℝ, (∀ t : E3, ‖t‖ = 1 → m₀ ≤ f t) ∧
      (∀ ε > 0, ∃ x : E3, ‖x‖ = 1 ∧ f x < m₀ + ε) := by
  set S : Set ℝ := f '' {x : E3 | ‖x‖ = 1} with hS_def
  have hSne : S.Nonempty := ⟨f p0, p0, hp0, rfl⟩
  have hSbdd : BddBelow S := by
    refine ⟨W - 2 * M, ?_⟩
    rintro y ⟨x, hx, rfl⟩
    obtain ⟨b, hb0⟩ := exists_orthonormalBasis_fst x hx
    have hsum := hf b
    rw [Fin.sum_univ_three, hb0] at hsum
    have h1 : f (b 1) ≤ M := hM (b 1) (b.norm_eq_one 1)
    have h2 : f (b 2) ≤ M := hM (b 2) (b.norm_eq_one 2)
    linarith
  refine ⟨sInf S, ?_, ?_⟩
  · intro t ht
    exact csInf_le hSbdd ⟨t, ht, rfl⟩
  · intro ε hε
    obtain ⟨y, hyS, hylt⟩ := exists_lt_of_csInf_lt hSne (show sInf S < sInf S + ε by linarith)
    obtain ⟨x, hx, rfl⟩ := hyS
    exact ⟨x, hx, hylt⟩

/- ═══════════════════════════════════════════════════════════════════
   G5-G9. Assemblage : attention du sup d'une frame function bornée.
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **G5-G9 (théorème principal).** Toute frame function bornée (au sens
`∀t unitaire, f t ≤ M`) atteint son sup sur la sphère. Preuve CKM §6 par
ultrafiltre : limite `p` d'une suite maximisante (G5), symétrisation par
rotation de 90° et recentrage par isométrie (G3-G4), passage à la limite le
long de l'ultrafiltre de la forme quadratique exacte (G6, bloc F), puis
descente radiale à 2 pas (G8) pour exclure une perte de masse en `p` (G9).

**EN.** **G5-G9 (main theorem).** Every bounded frame function (in the sense
`∀ unit t, f t ≤ M`) attains its sup on the sphere. Proof, CKM §6, by ultrafilter:
limit `p` of a maximizing sequence (G5), symmetrization by 90° rotation and
recentering by isometry (G3-G4), passing to the limit along the ultrafilter of the
exact quadratic form (G6, block F), then a 2-step radial descent (G8) to rule out a
loss of mass at `p` (G9).
-/
theorem frameFunction_attains_sup {f : E3 → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    {M : ℝ} (hM : ∀ t : E3, ‖t‖ = 1 → f t ≤ M) :
    ∃ p₀ : E3, ‖p₀‖ = 1 ∧ ∀ t : E3, ‖t‖ = 1 → f t ≤ f p₀ := by
  set p0 : E3 := (EuclideanSpace.basisFun (Fin 3) ℝ) 0 with hp0_def
  have hp0 : ‖p0‖ = 1 := (EuclideanSpace.basisFun (Fin 3) ℝ).norm_eq_one 0
  have hm_lb : ∀ t : E3, ‖t‖ = 1 → W - 2 * M ≤ f t := by
    intro t ht
    obtain ⟨b, hb0⟩ := exists_orthonormalBasis_fst t ht
    have hsum := hf b
    rw [Fin.sum_univ_three, hb0] at hsum
    have h1 : f (b 1) ≤ M := hM (b 1) (b.norm_eq_one 1)
    have h2 : f (b 2) ≤ M := hM (b 2) (b.norm_eq_one 2)
    linarith
  set m : ℝ := W - 2 * M with hm_def
  -- G5 : suite maximisante et limite le long de l'ultrafiltre
  set S : Set ℝ := f '' {x : E3 | ‖x‖ = 1} with hS_def
  have hSne : S.Nonempty := ⟨f p0, p0, hp0, rfl⟩
  have hSbdd : BddAbove S := ⟨M, by rintro y ⟨x, hx, rfl⟩; exact hM x hx⟩
  set M₀ : ℝ := sSup S with hM₀_def
  have hM₀_ub : ∀ t : E3, ‖t‖ = 1 → f t ≤ M₀ := fun t ht => le_csSup hSbdd ⟨t, ht, rfl⟩
  obtain ⟨useq, -, hu_tendsto, hu_mem⟩ := exists_seq_tendsto_sSup hSne hSbdd
  choose p_seq hp_seq_unit hp_seq_eq using hu_mem
  have hfp_tendsto : Tendsto (fun n => f (p_seq n)) atTop (𝓝 M₀) := by
    have heq : (fun n => f (p_seq n)) = useq := funext hp_seq_eq
    rw [heq]; exact hu_tendsto
  obtain ⟨p, hp, hp_tendsto⟩ := exists_ultrafilter_tendsto_sphere p_seq hp_seq_unit
  set 𝒰 : Ultrafilter ℕ := Ultrafilter.of atTop with h𝒰_def
  have hp_tendsto' : Tendsto p_seq (𝒰 : Filter ℕ) (𝓝 p) := by rw [h𝒰_def]; exact hp_tendsto
  have h𝒰_le : (𝒰 : Filter ℕ) ≤ atTop := by rw [h𝒰_def]; exact Ultrafilter.of_le atTop
  have hfp_tendsto' : Tendsto (fun n => f (p_seq n)) (𝒰 : Filter ℕ) (𝓝 M₀) :=
    hfp_tendsto.mono_left h𝒰_le
  -- q_seq : représentant nord de p_seq (même valeur de f, par parité)
  set q_seq : ℕ → E3 := fun n => if 0 ≤ ⟪p, p_seq n⟫ then p_seq n else -(p_seq n) with hq_seq_def
  have hq_seq_unit : ∀ n, ‖q_seq n‖ = 1 := by
    intro n
    simp only [hq_seq_def]
    split_ifs with h
    · exact hp_seq_unit n
    · rw [norm_neg]; exact hp_seq_unit n
  have hfq_seq_eq : ∀ n, f (q_seq n) = f (p_seq n) := by
    intro n
    simp only [hq_seq_def]
    split_ifs with h
    · rfl
    · exact frameFunction_even hf (p_seq n) (hp_seq_unit n)
  have hq_seq_nonneg : ∀ n, 0 ≤ ⟪p, q_seq n⟫ := by
    intro n
    simp only [hq_seq_def]
    split_ifs with h
    · exact h
    · rw [inner_neg_right]; linarith [not_le.mp h]
  set c'_seq : ℕ → ℝ := fun n => ⟪p, q_seq n⟫ with hc'_seq_def
  have hc'_seq_eq_abs : ∀ n, c'_seq n = |⟪p, p_seq n⟫| := by
    intro n
    simp only [hc'_seq_def, hq_seq_def]
    split_ifs with h
    · exact (abs_of_nonneg h).symm
    · rw [inner_neg_right, abs_of_neg (not_le.mp h)]
  have hc'_seq_mem : ∀ n, c'_seq n ∈ Set.Icc (0 : ℝ) 1 := by
    intro n
    rw [hc'_seq_eq_abs]
    refine ⟨abs_nonneg _, ?_⟩
    have h := abs_real_inner_le_norm p (p_seq n)
    rwa [hp, hp_seq_unit n, mul_one] at h
  have hpp_eq_one : (⟪p, p⟫ : ℝ) = 1 := by rw [real_inner_self_eq_norm_sq, hp]; norm_num
  have hcont : Continuous (fun x : E3 => (⟪p, x⟫ : ℝ)) := continuous_const.inner continuous_id
  have hpp_seq_tendsto : Tendsto (fun n => (⟪p, p_seq n⟫ : ℝ)) (𝒰 : Filter ℕ) (𝓝 (1 : ℝ)) := by
    have := (hcont.tendsto p).comp hp_tendsto'
    rwa [hpp_eq_one] at this
  have hc'_tendsto : Tendsto c'_seq (𝒰 : Filter ℕ) (𝓝 (1 : ℝ)) := by
    have heq : c'_seq = fun n => |⟪p, p_seq n⟫| := funext hc'_seq_eq_abs
    rw [heq]
    have := (continuous_abs.tendsto (1 : ℝ)).comp hpp_seq_tendsto
    rwa [abs_one] at this
  -- rotation de 90° (fixée une fois pour toutes) et recentrage par isométrie
  obtain ⟨phat, u1, u2, hu1, hu2, hpu1, hpu2, hu1u2, hphatp, hphatu1, hphatu2, hphat_equator⟩ :=
    exists_rotate90 hp
  set e0 : E3 := u1 with he0_def
  have hρ_exists : ∀ n, ∃ ρ : E3 ≃ₗᵢ[ℝ] E3, ρ (recenter p e0 (c'_seq n)) = p ∧ ρ p = q_seq n :=
    fun n => exists_recenter_isometry hp hu1 hpu1 (hq_seq_unit n) (hq_seq_nonneg n)
  choose ρ_seq hρ_seq1 hρ_seq2 using hρ_exists
  set g_seq : ℕ → E3 → ℝ := fun n => f ∘ (ρ_seq n) with hg_seq_def
  have hg_seq_frame : ∀ n, IsFrameFunction (g_seq n) W := fun n => hf.comp_isometry (ρ_seq n)
  set h_seq : ℕ → E3 → ℝ := fun n s => g_seq n s + g_seq n (phat s) with hh_seq_def
  have hh_seq_frame : ∀ n, IsFrameFunction (h_seq n) (2 * W) := by
    intro n
    have := symmetrize_frame (hg_seq_frame n) phat
    simpa only [hh_seq_def] using this
  have hh_seq_p : ∀ n, h_seq n p = 2 * f (q_seq n) := by
    intro n
    have h1 : h_seq n p = g_seq n p + g_seq n p := by simp only [hh_seq_def, hphatp]
    rw [h1, hg_seq_def]
    simp only [Function.comp_apply]
    rw [hρ_seq2 n]; ring
  have hh_seq_equator : ∀ n, ∀ e ∈ equator p, h_seq n e = W - f (q_seq n) := by
    intro n e he
    have h1 := symmetrize_equator (hg_seq_frame n) hp hphat_equator he
    have h2 : g_seq n p = f (q_seq n) := by
      rw [hg_seq_def]; simp only [Function.comp_apply]; rw [hρ_seq2 n]
    rw [h2] at h1
    simpa only [hh_seq_def] using h1
  have hg_bound : ∀ (n : ℕ) (t : E3), ‖t‖ = 1 → m ≤ g_seq n t ∧ g_seq n t ≤ M₀ := by
    intro n t ht
    rw [hg_seq_def]
    simp only [Function.comp_apply]
    have htu : ‖(ρ_seq n) t‖ = 1 := by rw [(ρ_seq n).norm_map]; exact ht
    exact ⟨hm_lb ((ρ_seq n) t) htu, hM₀_ub ((ρ_seq n) t) htu⟩
  have hh_seq_bounds : ∀ n s, ‖s‖ = 1 → 2 * m ≤ h_seq n s ∧ h_seq n s ≤ 2 * M₀ := by
    intro n s hs
    have h1 := hg_bound n s hs
    have h2 : ‖phat s‖ = 1 := by rw [phat.norm_map]; exact hs
    have h3 := hg_bound n (phat s) h2
    rw [hh_seq_def]
    exact ⟨by linarith [h1.1, h3.1], by linarith [h1.2, h3.2]⟩
  -- G6 : limite ponctuelle h le long de l'ultrafiltre
  have hh_exists : ∀ s : E3, ∃ L : ℝ, ‖s‖ = 1 →
      Tendsto (fun n => h_seq n s) (𝒰 : Filter ℕ) (𝓝 L) := by
    intro s
    by_cases hs : ‖s‖ = 1
    · obtain ⟨L, -, hL⟩ := exists_ultrafilter_tendsto_Icc (m := 2 * m) (M := 2 * M₀)
        (fun n => h_seq n s) (fun n => ⟨(hh_seq_bounds n s hs).1, (hh_seq_bounds n s hs).2⟩)
      exact ⟨L, fun _ => hL⟩
    · exact ⟨0, fun hcon => absurd hcon hs⟩
  choose h hh_tendsto using hh_exists
  have hh_frame : IsFrameFunction h (2 * W) := by
    intro b
    rw [Fin.sum_univ_three]
    have h0 := hh_tendsto (b 0) (b.norm_eq_one 0)
    have h1 := hh_tendsto (b 1) (b.norm_eq_one 1)
    have h2 := hh_tendsto (b 2) (b.norm_eq_one 2)
    have hsum_tendsto : Tendsto (fun n => h_seq n (b 0) + h_seq n (b 1) + h_seq n (b 2))
        (𝒰 : Filter ℕ) (𝓝 (h (b 0) + h (b 1) + h (b 2))) := (h0.add h1).add h2
    have hsum_const : ∀ n, h_seq n (b 0) + h_seq n (b 1) + h_seq n (b 2) = 2 * W := by
      intro n
      have hb := hh_seq_frame n b
      rwa [Fin.sum_univ_three] at hb
    have hsum_tendsto' : Tendsto (fun n => h_seq n (b 0) + h_seq n (b 1) + h_seq n (b 2))
        (𝒰 : Filter ℕ) (𝓝 (2 * W)) := by
      have heq : (fun n => h_seq n (b 0) + h_seq n (b 1) + h_seq n (b 2)) = fun _ => 2 * W :=
        funext hsum_const
      rw [heq]; exact tendsto_const_nhds
    exact tendsto_nhds_unique hsum_tendsto hsum_tendsto'
  have hh_bounds : ∀ t : E3, ‖t‖ = 1 → 2 * m ≤ h t ∧ h t ≤ 2 * M₀ := by
    intro t ht
    have htend := hh_tendsto t ht
    exact ⟨ge_of_tendsto' htend (fun n => (hh_seq_bounds n t ht).1),
      le_of_tendsto' htend (fun n => (hh_seq_bounds n t ht).2)⟩
  have hfq_tendsto : Tendsto (fun n => f (q_seq n)) (𝒰 : Filter ℕ) (𝓝 M₀) := by
    have heq2 : (fun n => f (q_seq n)) = fun n => f (p_seq n) := funext hfq_seq_eq
    rw [heq2]; exact hfp_tendsto'
  have hhp : h p = 2 * M₀ := by
    have htend1 : Tendsto (fun n => h_seq n p) (𝒰 : Filter ℕ) (𝓝 (h p)) := hh_tendsto p hp
    have htend2 : Tendsto (fun n => h_seq n p) (𝒰 : Filter ℕ) (𝓝 (2 * M₀)) := by
      have heq : (fun n => h_seq n p) = fun n => 2 * f (q_seq n) := funext hh_seq_p
      rw [heq]
      exact hfq_tendsto.const_mul 2
    exact tendsto_nhds_unique htend1 htend2
  have hh_equator : ∀ e ∈ equator p, h e = W - M₀ := by
    intro e he
    have htend1 : Tendsto (fun n => h_seq n e) (𝒰 : Filter ℕ) (𝓝 (h e)) := hh_tendsto e he.1
    have htend2 : Tendsto (fun n => h_seq n e) (𝒰 : Filter ℕ) (𝓝 (W - M₀)) := by
      have heq : (fun n => h_seq n e) = fun n => W - f (q_seq n) :=
        funext (fun n => hh_seq_equator n e he)
      rw [heq]
      exact tendsto_const_nhds.sub hfq_tendsto
    exact tendsto_nhds_unique htend1 htend2
  have hh_max : ∀ t : E3, ‖t‖ = 1 → h t ≤ h p := by
    intro t ht; rw [hhp]; exact (hh_bounds t ht).2
  -- G7 : forme exacte via F
  have hh_exact := frameFunction_exact_pole hh_frame hp hh_max hh_equator
  obtain ⟨e_eq, he_eq⟩ := equator_nonempty' hp
  have hK_nn : 0 ≤ 3 * M₀ - W := by
    have h1 : h e_eq ≤ h p := hh_max e_eq he_eq.1
    rw [hh_equator e_eq he_eq, hhp] at h1
    linarith
  -- G9 : assemblage final (descente à 2 pas pour exclure toute perte de masse en p)
  have hfp_eq : f p = M₀ := by
    apply le_antisymm (hM₀_ub p hp)
    apply le_of_forall_pos_lt_add
    intro ε hε
    set K : ℝ := 3 * M₀ - W with hK_def
    set δ : ℝ := min 1 (ε / (4 * (K + 1))) with hδ_def
    have hδpos : 0 < δ := lt_min (by norm_num) (by positivity)
    have hδle1 : δ ≤ 1 := min_le_left _ _
    have hKδ_lt : K * δ < ε / 4 := by
      have h1 : δ ≤ ε / (4 * (K + 1)) := min_le_right _ _
      have h2 : K * δ ≤ K * (ε / (4 * (K + 1))) := mul_le_mul_of_nonneg_left h1 hK_nn
      have h3 : K * (ε / (4 * (K + 1))) < ε / 4 := by
        rw [show K * (ε / (4 * (K + 1))) = (K * ε) / (4 * (K + 1)) from by ring,
          div_lt_div_iff₀ (by positivity : (0 : ℝ) < 4 * (K + 1)) (by norm_num : (0 : ℝ) < 4)]
        nlinarith [hK_nn, hε]
      linarith [h2, h3]
    set τ : ℝ := Real.sqrt (1 - δ) with hτ_def
    have hτnn : 0 ≤ τ := Real.sqrt_nonneg _
    have hτsq : τ ^ 2 = 1 - δ := Real.sq_sqrt (by linarith)
    have hτlt1 : τ < 1 := (sq_lt_sq₀ hτnn zero_le_one).mp (by rw [one_pow, hτsq]; linarith)
    set c : E3 := recenter p e0 τ with hc_def
    have hc_unfold : c = τ • p + Real.sqrt (1 - τ ^ 2) • e0 := hc_def
    have hc_prop := recenter_prop hp hu1 hpu1 hτnn hτlt1.le
    have hc_northern := recenter_northern hp hu1 hpu1 hτnn hτlt1.le
    have hc_unit : ‖c‖ = 1 := hc_prop.1
    have hc_lat : lat p c = τ ^ 2 := hc_northern.2
    have hh_c_eq : h c = 2 * M₀ - K * δ := by
      have heq := hh_exact c hc_unit
      rw [hc_lat, hτsq, hhp] at heq
      rw [heq, hK_def]; ring
    have hhc_gt : h c > 2 * M₀ - ε / 4 := by rw [hh_c_eq]; linarith [hKδ_lt]
    have hev1 : ∀ᶠ n in (𝒰 : Filter ℕ), 2 * M₀ - ε / 8 < h_seq n p := by
      have htend : Tendsto (fun n => h_seq n p) (𝒰 : Filter ℕ) (𝓝 (2 * M₀)) := hhp ▸ hh_tendsto p hp
      exact (tendsto_order.mp htend).1 (2 * M₀ - ε / 8) (by linarith)
    have hev2 : ∀ᶠ n in (𝒰 : Filter ℕ), h c - ε / 8 < h_seq n c := by
      exact (tendsto_order.mp (hh_tendsto c hc_unit)).1 (h c - ε / 8) (by linarith)
    have hev3 : ∀ᶠ n in (𝒰 : Filter ℕ), τ < c'_seq n :=
      (tendsto_order.mp hc'_tendsto).1 τ hτlt1
    obtain ⟨n, ⟨hn1, hn2⟩, hn3⟩ := ((hev1.and hev2).and hev3).exists
    set cn : E3 := recenter p e0 (c'_seq n) with hcn_def
    have hcn_unfold : cn = c'_seq n • p + Real.sqrt (1 - (c'_seq n) ^ 2) • e0 := hcn_def
    have hcn_prop := recenter_prop hp hu1 hpu1 (hc'_seq_mem n).1 (hc'_seq_mem n).2
    have hcn_northern := recenter_northern hp hu1 hpu1 (hc'_seq_mem n).1 (hc'_seq_mem n).2
    have hcn_unit : ‖cn‖ = 1 := hcn_prop.1
    have hρn_cn : (ρ_seq n) cn = p := hρ_seq1 n
    have hgn_cn : g_seq n cn = f p := by
      rw [hg_seq_def]; simp only [Function.comp_apply]; rw [hρn_cn]
    have hphat_cn_unit : ‖phat cn‖ = 1 := by rw [phat.norm_map]; exact hcn_unit
    have hhn_cn_le : h_seq n cn ≤ f p + M₀ := by
      rw [hh_seq_def]
      simp only
      rw [hgn_cn]
      linarith [(hg_bound n (phat cn) hphat_cn_unit).2]
    have hhn_cn_gt : h_seq n cn > 2 * M₀ - 3 * ε / 4 := by
      rcases (hc'_seq_mem n).2.eq_or_lt with hc'eq | hc'lt
      · have hcn_eq_p : cn = p := by
          rw [hcn_unfold, hc'eq]; simp
        rw [hcn_eq_p]
        linarith [hn1]
      · have hcn_ne_p : cn ≠ p := by
          intro heq
          have h1 : lat p cn = 1 := by rw [heq]; exact lat_self p hp
          rw [hcn_northern.2] at h1
          nlinarith [hc'lt, (hc'_seq_mem n).1]
        obtain ⟨s1, hs1N, hs1p, hs1_desc_cn, hc_desc_s1⟩ :=
          exists_two_step_descent hp hu1 hpu1 hτnn hn3 hc'lt
        rw [← hcn_unfold] at hs1_desc_cn
        rw [← hc_unfold] at hc_desc_s1
        obtain ⟨m₀n, hmlb_n, hm_n⟩ :=
          exists_inf_approx_of_le (hh_seq_frame n) (fun t ht => (hh_seq_bounds n t ht).2) p hp
        set ξ : ℝ := (2 * M₀ - h_seq n p) + ε / 16 with hξ_def
        have hfp_bound : 2 * M₀ - ξ < h_seq n p := by rw [hξ_def]; linarith
        have hs1_unit : ‖s1‖ = 1 := hs1N.1
        have hC3_1 := basic_lemma_approx (hh_seq_frame n) hp
          (fun t ht => (hh_seq_bounds n t ht).2) hmlb_n hm_n (hh_seq_equator n) hfp_bound
          hcn_unit hcn_northern.1 hcn_ne_p hs1_desc_cn
        have hC3_2 := basic_lemma_approx (hh_seq_frame n) hp
          (fun t ht => (hh_seq_bounds n t ht).2) hmlb_n hm_n (hh_seq_equator n) hfp_bound
          hs1_unit hs1N hs1p hc_desc_s1
        have hξ_small : ξ < ε / 8 + ε / 16 := by rw [hξ_def]; linarith [hn1]
        linarith [hC3_1, hC3_2, hn2, hhc_gt, hξ_small]
    linarith [hhn_cn_le, hhn_cn_gt]
  refine ⟨p, hp, fun t ht => ?_⟩
  rw [hfp_eq]; exact hM₀_ub t ht

/--
**FR.** **G9 (corollaire).** Attention de l'inf, via `frameFunction_attains_sup`
appliqué à `-f` (G1d, `IsFrameFunction.neg`).

**EN.** **G9 (corollary).** Attainment of the inf, via `frameFunction_attains_sup`
applied to `-f` (G1d, `IsFrameFunction.neg`).
-/
theorem frameFunction_attains_inf {f : E3 → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    {m : ℝ} (hm : ∀ t : E3, ‖t‖ = 1 → m ≤ f t) :
    ∃ r₀ : E3, ‖r₀‖ = 1 ∧ ∀ t : E3, ‖t‖ = 1 → f r₀ ≤ f t := by
  have hnegM : ∀ t : E3, ‖t‖ = 1 → (fun x => -f x) t ≤ -m := by
    intro t ht; simp only; linarith [hm t ht]
  obtain ⟨p₀, hp₀, hp₀max⟩ := frameFunction_attains_sup hf.neg hnegM
  refine ⟨p₀, hp₀, fun t ht => ?_⟩
  have h := hp₀max t ht
  linarith

end
end Gleason
