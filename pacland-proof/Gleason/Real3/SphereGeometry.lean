import Gleason.Real3.FrameFunction

/-!
**FR.** # Mini-bibliothèque de géométrie sphérique

Lemmes de géométrie sur S² nécessaires à la descente CKM. Stratégie : tout exprimer
par des TRIPLETS ORTHONORMÉS (extension de bases orthonormées, Gram–Schmidt), en
évitant SO(3) et les angles d'Euler, mal couverts par Mathlib.

**EN.** # Spherical geometry mini-library

Geometric lemmas on S² needed for the CKM descent. Strategy: express everything
via ORTHONORMAL TRIPLES (extension of orthonormal bases, Gram–Schmidt), avoiding
SO(3) and Euler angles, which Mathlib covers poorly.
-/

namespace Gleason

open scoped RealInnerProductSpace Real

noncomputable section

/--
**FR.** Tout vecteur unitaire se complète en base orthonormée de ℝ³.
Mathlib : chercher l'extension d'une famille orthonormée en `OrthonormalBasis`
(`Orthonormal` + `exists_orthonormalBasis_extension` ou équivalent).

**EN.** Every unit vector extends to an orthonormal basis of ℝ³.
Mathlib: look for the extension of an orthonormal family to an
`OrthonormalBasis` (`Orthonormal` + `exists_orthonormalBasis_extension` or
equivalent).
-/
theorem exists_orthonormalBasis_fst (x : E3) (hx : ‖x‖ = 1) :
    ∃ b : OrthonormalBasis (Fin 3) ℝ E3, b 0 = x := by
  have hcard : Module.finrank ℝ E3 = Fintype.card (Fin 3) := by simp
  have hv : Orthonormal ℝ (({0} : Set (Fin 3)).restrict (fun _ : Fin 3 => x)) := by
    constructor
    · rintro ⟨i, hi⟩
      simpa [Set.restrict, Set.restrict_apply] using hx
    · rintro ⟨i, hi⟩ ⟨j, hj⟩ hij
      simp only [Set.mem_singleton_iff] at hi hj
      exact absurd (Subtype.ext (hi.trans hj.symm)) hij
  obtain ⟨b, hb⟩ := hv.exists_orthonormalBasis_extension_of_card_eq hcard
  exact ⟨b, hb 0 rfl⟩

/--
**FR.** Toute paire orthonormée se complète en base orthonormée de ℝ³.

**EN.** Every orthonormal pair extends to an orthonormal basis of ℝ³.
-/
theorem exists_orthonormalBasis_pair (x y : E3) (hx : ‖x‖ = 1) (hy : ‖y‖ = 1)
    (hxy : ⟪x, y⟫ = 0) :
    ∃ b : OrthonormalBasis (Fin 3) ℝ E3, b 0 = x ∧ b 1 = y := by
  have hcard : Module.finrank ℝ E3 = Fintype.card (Fin 3) := by simp
  have hyx : ⟪y, x⟫ = 0 := by rw [real_inner_comm]; exact hxy
  have hv : Orthonormal ℝ (({0, 1} : Set (Fin 3)).restrict ![x, y, 0]) := by
    constructor
    · rintro ⟨i, hi⟩
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hi
      rcases hi with hi | hi <;> subst hi
      · simpa [Set.restrict, Set.restrict_apply] using hx
      · simpa [Set.restrict, Set.restrict_apply] using hy
    · rintro ⟨i, hi⟩ ⟨j, hj⟩ hij
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hi hj
      simp only [ne_eq, Subtype.mk.injEq] at hij
      rcases hi with hi | hi <;> rcases hj with hj | hj <;> subst hi <;> subst hj
      · exact absurd rfl hij
      · simpa [Set.restrict, Set.restrict_apply] using hxy
      · simpa [Set.restrict, Set.restrict_apply] using hyx
      · exact absurd rfl hij
  obtain ⟨b, hb⟩ := hv.exists_orthonormalBasis_extension_of_card_eq hcard
  refine ⟨b, ?_, ?_⟩
  · have := hb 0 (by simp)
    simpa using this
  · have := hb 1 (by simp)
    simpa using this

/--
**FR.** **C1.** Étant donné une paire orthonormée, il existe un troisième vecteur
unitaire orthogonal aux deux (le 3ᵉ vecteur d'une base les complétant).

**EN.** **C1.** Given an orthonormal pair, there exists a third unit vector
orthogonal to both (the 3rd vector of a basis completing them).
-/
theorem exists_third_orthogonal (x y : E3) (hx : ‖x‖ = 1) (hy : ‖y‖ = 1) (hxy : ⟪x, y⟫ = 0) :
    ∃ z, ‖z‖ = 1 ∧ ⟪x, z⟫ = 0 ∧ ⟪y, z⟫ = 0 := by
  obtain ⟨b, hb0, hb1⟩ := exists_orthonormalBasis_pair x y hx hy hxy
  refine ⟨b 2, b.norm_eq_one 2, ?_, ?_⟩
  · rw [← hb0]; exact b.inner_eq_zero (by decide)
  · rw [← hb1]; exact b.inner_eq_zero (by decide)

/--
**FR.** Un triplet EXPLICITEMENT prescrit (les trois vecteurs, pas seulement deux) qui
est orthonormé coïncide avec une base orthonormée — cas `s = univ` de l'extension.
Outil de base pour construire des bases par manipulation directe de triplets
(retournement de signe, produit vectoriel, etc.), utilisé dans toute la suite.

**EN.** An EXPLICITLY prescribed triple (all three vectors, not just two) that is
orthonormal coincides with an orthonormal basis — the `s = univ` case of the
extension. Basic tool for building bases by direct manipulation of triples
(sign flip, cross product, etc.), used throughout the rest of the file.
-/
theorem exists_orthonormalBasis_of_triple (v : Fin 3 → E3)
    (hnorm : ∀ i, ‖v i‖ = 1) (hperp : Pairwise (fun i j => ⟪v i, v j⟫ = 0)) :
    ∃ b : OrthonormalBasis (Fin 3) ℝ E3, ∀ i, b i = v i := by
  have hcard : Module.finrank ℝ E3 = Fintype.card (Fin 3) := by simp
  have hv : Orthonormal ℝ ((Set.univ : Set (Fin 3)).restrict v) :=
    ⟨fun i => hnorm i.1, fun i j hij => hperp (fun h => hij (Subtype.ext h))⟩
  obtain ⟨b, hb⟩ := hv.exists_orthonormalBasis_extension_of_card_eq hcard
  exact ⟨b, fun i => hb i (Set.mem_univ i)⟩

/--
**FR.** Variante « symétrique » de `exists_orthonormalBasis_of_triple` : au lieu d'une
`Pairwise`, les 3 produits scalaires deux-à-deux sont donnés explicitement (plus
commode à fournir à chaque site d'appel).

**EN.** Symmetric variant of `exists_orthonormalBasis_of_triple`: instead of a
`Pairwise`, the 3 pairwise inner products are given explicitly (more convenient
to supply at each call site).
-/
theorem exists_orthonormalBasis_of_triple' (v0 v1 v2 : E3)
    (h0 : ‖v0‖ = 1) (h1 : ‖v1‖ = 1) (h2 : ‖v2‖ = 1)
    (h01 : ⟪v0, v1⟫ = 0) (h02 : ⟪v0, v2⟫ = 0) (h12 : ⟪v1, v2⟫ = 0) :
    ∃ b : OrthonormalBasis (Fin 3) ℝ E3, b 0 = v0 ∧ b 1 = v1 ∧ b 2 = v2 := by
  have h10 : ⟪v1, v0⟫ = 0 := by rw [real_inner_comm]; exact h01
  have h20 : ⟪v2, v0⟫ = 0 := by rw [real_inner_comm]; exact h02
  have h21 : ⟪v2, v1⟫ = 0 := by rw [real_inner_comm]; exact h12
  have hnorm : ∀ i, ‖(![v0, v1, v2] : Fin 3 → E3) i‖ = 1 := by
    intro i; fin_cases i <;> simp_all
  have hperp : Pairwise (fun i j =>
      ⟪(![v0, v1, v2] : Fin 3 → E3) i, (![v0, v1, v2] : Fin 3 → E3) j⟫ = 0) := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> first | exact absurd rfl hij | simp_all
  obtain ⟨b, hb⟩ := exists_orthonormalBasis_of_triple _ hnorm hperp
  exact ⟨b, by simpa using hb 0, by simpa using hb 1, by simpa using hb 2⟩

/--
**FR.** Il existe un vecteur unitaire orthogonal à deux vecteurs donnés : l'orthogonal
d'un sous-espace engendré par 2 vecteurs, dans un espace de dimension 3, est de
dimension ≥ 1 (comptage de dimension). Remplace le produit vectoriel : couvre
uniformément le cas dégénéré où les deux vecteurs sont colinéaires, sans
disjonction de cas.

**EN.** There exists a unit vector orthogonal to two given vectors: the
orthogonal complement of a subspace spanned by 2 vectors, in a
dimension-3 space, has dimension ≥ 1 (dimension counting). Replaces the cross
product: uniformly covers the degenerate case where the two vectors are
collinear, with no case split.
-/
theorem exists_unit_orthogonal_to_pair (a b : E3) :
    ∃ u : E3, ‖u‖ = 1 ∧ ⟪u, a⟫ = 0 ∧ ⟪u, b⟫ = 0 := by
  classical
  set K : Submodule ℝ E3 := Submodule.span ℝ ({a, b} : Set E3) with hK_def
  have hKfin : Module.finrank ℝ K ≤ 2 := by
    refine le_trans (finrank_span_le_card ({a, b} : Set E3)) ?_
    simp only [Set.toFinset_insert, Set.toFinset_singleton]
    exact (Finset.card_insert_le _ _).trans (by simp)
  have hE3 : Module.finrank ℝ E3 = 3 := by simp
  have hsum : Module.finrank ℝ K + Module.finrank ℝ Kᗮ = Module.finrank ℝ E3 :=
    Submodule.finrank_add_finrank_orthogonal K
  have hKperp : 1 ≤ Module.finrank ℝ Kᗮ := by omega
  have hne : Kᗮ ≠ ⊥ := by
    intro h
    rw [h, finrank_bot] at hKperp
    omega
  obtain ⟨w, hwK, hw0⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hne
  have haK : a ∈ K := Submodule.subset_span (by simp)
  have hbK : b ∈ K := Submodule.subset_span (by simp)
  have hwa : ⟪w, a⟫ = 0 := Submodule.inner_left_of_mem_orthogonal haK hwK
  have hwb : ⟪w, b⟫ = 0 := Submodule.inner_left_of_mem_orthogonal hbK hwK
  refine ⟨(‖w‖⁻¹ : ℝ) • w, ?_, ?_, ?_⟩
  · rw [norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos (norm_pos_iff.mpr hw0)]
    exact inv_mul_cancel₀ (norm_ne_zero_iff.mpr hw0)
  · rw [real_inner_smul_left, hwa, mul_zero]
  · rw [real_inner_smul_left, hwb, mul_zero]

/--
**FR.** **Unicité (à signe près) de l'orthogonal d'une paire indépendante.**
Si `a,b` sont indépendants (`a ≠ 0`, `b` non multiple de `a`), l'orthogonal de
`span{a,b}` est de rang 1 (`finrank_add_finrank_orthogonal` + rang 2 du span,
via l'indépendance linéaire) : deux vecteurs unitaires qui y vivent sont égaux
ou opposés. Complète `exists_unit_orthogonal_to_pair` (existence) : nécessaire
en bloc H (Regular.lean) pour montrer que deux grands cercles distincts se
coupent en EXACTEMENT une paire antipodale (pas plus).

**EN.** **Uniqueness (up to sign) of the orthogonal of an independent pair.**
If `a,b` are independent (`a ≠ 0`, `b` not a multiple of `a`), the orthogonal
complement of `span{a,b}` has rank 1 (`finrank_add_finrank_orthogonal` + rank 2
of the span, via linear independence): two unit vectors living there are equal
or opposite. Completes `exists_unit_orthogonal_to_pair` (existence): needed in
block H (Regular.lean) to show that two distinct great circles meet in EXACTLY
one antipodal pair (no more).
-/
theorem unique_unit_orthogonal_to_pair {a b u v : E3} (ha0 : a ≠ 0)
    (hindep : ∀ c : ℝ, c • a ≠ b)
    (hua : ⟪u, a⟫ = 0) (hub : ⟪u, b⟫ = 0) (hu : ‖u‖ = 1)
    (hva : ⟪v, a⟫ = 0) (hvb : ⟪v, b⟫ = 0) (hv : ‖v‖ = 1) :
    v = u ∨ v = -u := by
  classical
  set K : Submodule ℝ E3 := Submodule.span ℝ ({a, b} : Set E3) with hK_def
  have hindepv : LinearIndependent ℝ ![a, b] := (LinearIndependent.pair_iff' ha0).mpr hindep
  have hrange : ({a, b} : Set E3) = Set.range ![a, b] := by
    ext x
    simp [eq_comm, or_comm]
  have hKfin : Module.finrank ℝ K = 2 := by
    rw [hK_def, hrange]
    have h := finrank_span_eq_card hindepv
    simpa using h
  have hE3 : Module.finrank ℝ E3 = 3 := by simp
  have hsum : Module.finrank ℝ K + Module.finrank ℝ Kᗮ = Module.finrank ℝ E3 :=
    Submodule.finrank_add_finrank_orthogonal K
  have hKperp1 : Module.finrank ℝ Kᗮ = 1 := by omega
  have huK : u ∈ Kᗮ := by
    have hiso : (Submodule.span ℝ ({u} : Set E3)) ⟂ K := by
      rw [hK_def, Submodule.isOrtho_span]
      intro x hx y hy
      simp only [Set.mem_singleton_iff] at hx
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hy
      subst hx
      rcases hy with hy | hy <;> subst hy
      · exact hua
      · exact hub
    exact Submodule.isOrtho_iff_le.mp hiso (Submodule.mem_span_singleton_self u)
  have hvK : v ∈ Kᗮ := by
    have hiso : (Submodule.span ℝ ({v} : Set E3)) ⟂ K := by
      rw [hK_def, Submodule.isOrtho_span]
      intro x hx y hy
      simp only [Set.mem_singleton_iff] at hx
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hy
      subst hx
      rcases hy with hy | hy <;> subst hy
      · exact hva
      · exact hvb
    exact Submodule.isOrtho_iff_le.mp hiso (Submodule.mem_span_singleton_self v)
  have hu0 : u ≠ 0 := by
    intro h; rw [h, norm_zero] at hu; exact absurd hu (by norm_num)
  have hspan : Kᗮ = Submodule.span ℝ ({u} : Set E3) :=
    eq_span_singleton_of_mem_of_finrank_eq_one hKperp1 huK hu0
  rw [hspan] at hvK
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hvK
  have hcabs : |c| = 1 := by
    have hnorm : ‖c • u‖ = 1 := by rw [hc]; exact hv
    rwa [norm_smul, Real.norm_eq_abs, hu, mul_one] at hnorm
  rcases (abs_eq (by norm_num : (0:ℝ) ≤ 1)).mp hcabs with h1 | h1
  · left; rw [← hc, h1, one_smul]
  · right; rw [← hc, h1, neg_one_smul]

/--
**FR.** Deux bases partageant un vecteur : la somme de `f` sur les deux autres vecteurs
est la même (conséquence directe de la définition de frame function ; utilisé
partout dans la descente).

**EN.** Two bases sharing a vector: the sum of `f` over the other two vectors is
the same (direct consequence of the definition of frame function; used
throughout the descent).
-/
theorem frame_pair_sum_eq {f : E3 → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (b b' : OrthonormalBasis (Fin 3) ℝ E3) (h : b 0 = b' 0) :
    f (b 1) + f (b 2) = f (b' 1) + f (b' 2) := by
  have h1 := hf b
  have h2 := hf b'
  rw [Fin.sum_univ_three] at h1 h2
  rw [h] at h1
  linarith

/--
**FR.** Une frame function positive est bornée par `W` sur la sphère
(compléter tout vecteur unitaire en base orthonormée, les deux autres termes sont ≥ 0).

**EN.** A positive frame function is bounded by `W` on the sphere (complete any
unit vector into an orthonormal basis, the other two terms are ≥ 0).
-/
theorem IsFrameFunction.le_of_nonneg {f : E3 → ℝ} {W : ℝ}
    (hf : IsFrameFunction f W) (hnn : ∀ x, ‖x‖ = 1 → 0 ≤ f x)
    {x : E3} (hx : ‖x‖ = 1) : f x ≤ W := by
  obtain ⟨b, hb0⟩ := exists_orthonormalBasis_fst x hx
  have hsum := hf b
  rw [Fin.sum_univ_three, hb0] at hsum
  have hn1 : 0 ≤ f (b 1) := hnn (b 1) (b.norm_eq_one 1)
  have hn2 : 0 ≤ f (b 2) := hnn (b 2) (b.norm_eq_one 2)
  linarith

/--
**FR.** **P2 (parité).** `f(-s) = f(s)` : on remplace `b 0` par `-(b 0)` dans une base
contenant `s`, les deux triplets sont orthonormés (retournement de signe préserve
normes et orthogonalité).

**EN.** **P2 (parity).** `f(-s) = f(s)`: replace `b 0` by `-(b 0)` in a basis
containing `s`; both triples are orthonormal (sign flip preserves norms and
orthogonality).
-/
theorem frameFunction_even {f : E3 → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (s : E3) (hs : ‖s‖ = 1) : f (-s) = f s := by
  obtain ⟨b, hb0⟩ := exists_orthonormalBasis_fst s hs
  have hnorm : ∀ i, ‖(![-(b 0), b 1, b 2] : Fin 3 → E3) i‖ = 1 := by
    intro i; fin_cases i <;> simp [b.norm_eq_one]
  have hperp : Pairwise (fun i j =>
      ⟪(![-(b 0), b 1, b 2] : Fin 3 → E3) i, (![-(b 0), b 1, b 2] : Fin 3 → E3) j⟫ = 0) := by
    intro i j hij
    fin_cases i <;> fin_cases j <;>
      first
        | exact absurd rfl hij
        | simp [inner_neg_left, inner_neg_right, b.inner_eq_ite]
  obtain ⟨b', hb'⟩ := exists_orthonormalBasis_of_triple _ hnorm hperp
  have h1 := hf b
  have h2 := hf b'
  rw [Fin.sum_univ_three] at h1 h2
  rw [hb' 0, hb' 1, hb' 2] at h2
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
             Matrix.cons_val_two, Matrix.tail_cons] at h2
  rw [hb0] at h1 h2
  linarith

/--
**FR.** **P3.** Si `(u,s,t)` et `(u,s',t')` sont deux triplets orthonormés partageant
`u`, alors `f s + f t = f s' + f t'` — corollaire direct de `frame_pair_sum_eq`
appliqué aux bases construites sur `(u,s,t)` et `(u,s',t')`.

**EN.** **P3.** If `(u,s,t)` and `(u,s',t')` are two orthonormal triples sharing
`u`, then `f s + f t = f s' + f t'` — a direct corollary of
`frame_pair_sum_eq` applied to the bases built on `(u,s,t)` and `(u,s',t')`.
-/
theorem frameFunction_pair_swap {f : E3 → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    {u s t s' t' : E3}
    (hu : ‖u‖ = 1) (hs : ‖s‖ = 1) (ht : ‖t‖ = 1) (hs' : ‖s'‖ = 1) (ht' : ‖t'‖ = 1)
    (hus : ⟪u, s⟫ = 0) (hut : ⟪u, t⟫ = 0) (hst : ⟪s, t⟫ = 0)
    (hus' : ⟪u, s'⟫ = 0) (hut' : ⟪u, t'⟫ = 0) (hs't' : ⟪s', t'⟫ = 0) :
    f s + f t = f s' + f t' := by
  obtain ⟨b, hb0, hb1, hb2⟩ := exists_orthonormalBasis_of_triple' u s t hu hs ht hus hut hst
  obtain ⟨b', hb0', hb1', hb2'⟩ :=
    exists_orthonormalBasis_of_triple' u s' t' hu hs' ht' hus' hut' hs't'
  have h := frame_pair_sum_eq hf b b' (by rw [hb0, hb0'])
  rwa [hb1, hb2, hb1', hb2'] at h

/--
**FR.** **P4.** Si `f(s) > M - ξ` (proche du sup) alors il existe `t ⊥ s` avec
`f(t) < m + ξ` (proche de l'inf). Preuve CKM §2 : on choisit `t'` avec
`f(t') < m + δ` où `δ = ξ - (M - f s) > 0`, un vecteur `u` orthogonal à `s`
et `t'` (`exists_unit_orthogonal_to_pair`, remplace le produit vectoriel —
couvre le cas dégénéré `t' = ±s` sans disjonction de cas), puis on complète
en `t ⊥ (s,u)` et `s' ⊥ (t',u)`. `frameFunction_pair_swap` sur `(u,s,t)` et
`(u,s',t')` donne `f s + f t = f s' + f t'`, d'où `f t < m + ξ` en
combinant `f s' ≤ M` et `f t' < m + δ`.

**EN.** **P4.** If `f(s) > M - ξ` (close to the sup) then there exists `t ⊥ s`
with `f(t) < m + ξ` (close to the inf). Proof, CKM §2: choose `t'` with
`f(t') < m + δ` where `δ = ξ - (M - f s) > 0`, a vector `u` orthogonal to `s`
and `t'` (`exists_unit_orthogonal_to_pair`, replaces the cross product —
covers the degenerate case `t' = ±s` with no case split), then complete into
`t ⊥ (s,u)` and `s' ⊥ (t',u)`. `frameFunction_pair_swap` on `(u,s,t)` and
`(u,s',t')` gives `f s + f t = f s' + f t'`, hence `f t < m + ξ` by combining
`f s' ≤ M` and `f t' < m + δ`.
-/
theorem frameFunction_P4 {f : E3 → ℝ} {W M m : ℝ} (hf : IsFrameFunction f W)
    (hMub : ∀ x : E3, ‖x‖ = 1 → f x ≤ M)
    (hm : ∀ ε > 0, ∃ x : E3, ‖x‖ = 1 ∧ f x < m + ε)
    {s : E3} (hs : ‖s‖ = 1) {ξ : ℝ} (hfs : M - ξ < f s) :
    ∃ t : E3, ‖t‖ = 1 ∧ ⟪s, t⟫ = 0 ∧ f t < m + ξ := by
  set δ : ℝ := ξ - (M - f s) with hδ_def
  have hδpos : 0 < δ := by rw [hδ_def]; linarith
  obtain ⟨t', ht'unit, ht'lt⟩ := hm δ hδpos
  obtain ⟨u, huunit, hus, hut'⟩ := exists_unit_orthogonal_to_pair s t'
  obtain ⟨t, htunit, hts, htu⟩ := exists_unit_orthogonal_to_pair s u
  obtain ⟨s', hs'unit, hs't', hs'u⟩ := exists_unit_orthogonal_to_pair t' u
  have hut : ⟪u, t⟫ = 0 := by rw [real_inner_comm]; exact htu
  have hst : ⟪s, t⟫ = 0 := by rw [real_inner_comm]; exact hts
  have hus' : ⟪u, s'⟫ = 0 := by rw [real_inner_comm]; exact hs'u
  have h := frameFunction_pair_swap hf huunit hs htunit hs'unit ht'unit
    hus hut hst hus' hut' hs't'
  have hs'M : f s' ≤ M := hMub s' hs'unit
  refine ⟨t, htunit, hst, ?_⟩
  rw [hδ_def] at ht'lt
  linarith

/- ═══════════════════════════════════════════════════════════════════
   Géométrie du pôle (CKM 1985 §4). Le pôle `p` reste un ARGUMENT
   EXPLICITE de chaque définition (pas de `variable` fixée globalement au
   sens mathématique) : le §7 utilisera trois pôles différents.
   ═══════════════════════════════════════════════════════════════════ -/

section PoleGeometry

variable (p : E3)

/--
**FR.** **Latitude** de `s` relative au pôle `p` : `⟪p,s⟫²`.

**EN.** **Latitude** of `s` relative to pole `p`: `⟪p,s⟫²`.
-/
def lat (s : E3) : ℝ := ⟪p, s⟫ ^ 2

/--
**FR.** **Hémisphère nord** : vecteurs unitaires du côté du pôle (`⟪p,·⟫ ≥ 0`).

**EN.** **Northern hemisphere**: unit vectors on the pole's side
(`⟪p,·⟫ ≥ 0`).
-/
def northern : Set E3 := {t : E3 | ‖t‖ = 1 ∧ 0 ≤ ⟪p, t⟫}

/--
**FR.** **Équateur** : vecteurs unitaires orthogonaux au pôle.

**EN.** **Equator**: unit vectors orthogonal to the pole.
-/
def equator : Set E3 := {t : E3 | ‖t‖ = 1 ∧ ⟪p, t⟫ = 0}

/--
**FR.** Point de l'équateur (à normalisation près) déterminé par `p` et `s` : la
projection de `s` sur `pᗮ`, complétée par la composante `√(1-⟪p,s⟫²)` sur `p`
pour former un vecteur unitaire orthogonal à `s` dans le plan `(p,s)`.
Valeur poubelle en `s = p` (jamais utilisée : voir les hypothèses de B2).

**EN.** Equatorial point (up to normalization) determined by `p` and `s`: the
projection of `s` onto `pᗮ`, completed by the component `√(1-⟪p,s⟫²)` on `p` to
form a unit vector orthogonal to `s` in the plane `(p,s)`. Junk value at
`s = p` (never used: see B2's hypotheses).
-/
noncomputable def sperp (s : E3) : E3 :=
  Real.sqrt (1 - ⟪p, s⟫ ^ 2) • p - ⟪p, s⟫ • (‖s - ⟪p, s⟫ • p‖⁻¹ • (s - ⟪p, s⟫ • p))

/--
**FR.** **Cercle de descente** de `s` relatif au pôle `p` : les points de
l'hémisphère nord orthogonaux à `sperp p s`.

**EN.** **Descent circle** of `s` relative to pole `p`: the points of the
northern hemisphere orthogonal to `sperp p s`.
-/
def descent (s : E3) : Set E3 := {t : E3 | t ∈ northern p ∧ ⟪sperp p s, t⟫ = 0}

@[simp] theorem mem_northern_iff {t : E3} : t ∈ northern p ↔ ‖t‖ = 1 ∧ 0 ≤ ⟪p, t⟫ := Iff.rfl

@[simp] theorem mem_equator_iff {t : E3} : t ∈ equator p ↔ ‖t‖ = 1 ∧ ⟪p, t⟫ = 0 := Iff.rfl

@[simp] theorem mem_descent_iff {s t : E3} :
    t ∈ descent p s ↔ t ∈ northern p ∧ ⟪sperp p s, t⟫ = 0 := Iff.rfl

/-- **B1.** Faits basiques sur `lat`, `northern`, `equator`. -/
theorem lat_nonneg (s : E3) : 0 ≤ lat p s := sq_nonneg _

theorem lat_le_one {s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) : lat p s ≤ 1 := by
  have h := abs_real_inner_le_norm p s
  rw [hp, hs, mul_one] at h
  have h' := abs_le.mp h
  have h2 : ⟪p, s⟫ ^ 2 ≤ 1 ^ 2 := sq_le_sq' h'.1 h'.2
  simpa [lat] using h2

theorem lat_self (hp : ‖p‖ = 1) : lat p p = 1 := by
  unfold lat
  rw [real_inner_self_eq_norm_sq, hp]
  norm_num

theorem equator_subset_northern : equator p ⊆ northern p := by
  intro t ht
  exact ⟨ht.1, le_of_eq ht.2.symm⟩

theorem mem_equator_iff_lat_eq_zero (t : E3) : t ∈ equator p ↔ ‖t‖ = 1 ∧ lat p t = 0 := by
  simp [equator, lat]

/--
**FR.** **F0.** `lat` est paire (`⟪p,-s⟫ = -⟪p,s⟫`, mis au carré).

**EN.** **F0.** `lat` is even (`⟪p,-s⟫ = -⟪p,s⟫`, squared).
-/
theorem lat_neg (s : E3) : lat p (-s) = lat p s := by
  unfold lat
  rw [inner_neg_right]
  ring

end PoleGeometry

/--
**FR.** **B2 (préliminaire).** `‖s - ⟪p,s⟫•p‖² = 1 - ⟪p,s⟫²`, par développement de
l'inner product (algèbre pure, aucune hypothèse `s ≠ p`).

**EN.** **B2 (preliminary).** `‖s - ⟪p,s⟫•p‖² = 1 - ⟪p,s⟫²`, by expanding the
inner product (pure algebra, no hypothesis `s ≠ p`).
-/
theorem norm_sq_sub_inner_smul {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) :
    ‖s - ⟪p, s⟫ • p‖ ^ 2 = 1 - ⟪p, s⟫ ^ 2 := by
  set c : ℝ := ⟪p, s⟫ with hc_def
  rw [norm_sub_sq_real, real_inner_smul_right, real_inner_comm p s, ← hc_def,
      norm_smul, hp, mul_one, Real.norm_eq_abs, sq_abs, hs]
  ring

/--
**FR.** **F0.** Latitude maximale ⇒ pôle : `s ∈ northern p`, `lat p s = 1` force
`⟪p,s⟫ = 1` (racine positive), d'où `‖s-p‖ = 0` via le préliminaire ci-dessus.

**EN.** **F0.** Maximal latitude ⇒ pole: `s ∈ northern p`, `lat p s = 1` forces
`⟪p,s⟫ = 1` (positive root), hence `‖s-p‖ = 0` via the preliminary above.
-/
theorem eq_pole_of_lat_eq_one {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1)
    (hsN : s ∈ northern p) (hl : lat p s = 1) : s = p := by
  have hc0 : 0 ≤ ⟪p, s⟫ := hsN.2
  have hc1 : ⟪p, s⟫ = 1 := by
    have heq0 : (⟪p, s⟫ - 1) * (⟪p, s⟫ + 1) = 0 := by
      have : ⟪p, s⟫ ^ 2 = 1 := hl
      linear_combination this
    rcases mul_eq_zero.mp heq0 with h | h
    · linarith
    · linarith
  have hnorm : ‖s - ⟪p, s⟫ • p‖ ^ 2 = 1 - ⟪p, s⟫ ^ 2 := norm_sq_sub_inner_smul hp hs
  rw [hc1, one_smul] at hnorm
  norm_num at hnorm
  exact sub_eq_zero.mp hnorm

/--
**FR.** **F0.** Tout vecteur unitaire admet un représentant dans `northern p` de
même latitude, égal à lui-même ou à son opposé (`⟪p,·⟫ ≥ 0` ou `< 0`).

**EN.** **F0.** Every unit vector admits a representative in `northern p` of the
same latitude, equal to itself or to its opposite (`⟪p,·⟫ ≥ 0` or `< 0`).
-/
theorem exists_northern_rep {p t : E3} (ht : ‖t‖ = 1) :
    ∃ s : E3, s ∈ northern p ∧ lat p s = lat p t ∧ (s = t ∨ s = -t) := by
  by_cases h : 0 ≤ (⟪p, t⟫ : ℝ)
  · exact ⟨t, ⟨ht, h⟩, rfl, Or.inl rfl⟩
  · push Not at h
    refine ⟨-t, ⟨by rwa [norm_neg], ?_⟩, lat_neg p t, Or.inr rfl⟩
    rw [inner_neg_right]; linarith

/--
**FR.** **B2 (préliminaire).** `⟪p,s⟫ < 1` pour `p,s` unitaires, `s ≠ p` : `⟪p,s⟫ = 1`
forcerait `‖s-p‖ = 0` (via le préliminaire ci-dessus), donc `s = p`.

**EN.** **B2 (preliminary).** `⟪p,s⟫ < 1` for `p,s` unit vectors, `s ≠ p`:
`⟪p,s⟫ = 1` would force `‖s-p‖ = 0` (via the preliminary above), hence `s = p`.
-/
theorem sperp_c_lt_one {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsp : s ≠ p) :
    ⟪p, s⟫ < 1 := by
  have hle : ⟪p, s⟫ ≤ 1 := by
    have h := abs_real_inner_le_norm p s
    rw [hp, hs, mul_one] at h
    exact (abs_le.mp h).2
  rcases hle.lt_or_eq with h | h
  · exact h
  · exfalso
    apply hsp
    have hnorm : ‖s - ⟪p, s⟫ • p‖ ^ 2 = 1 - ⟪p, s⟫ ^ 2 := norm_sq_sub_inner_smul hp hs
    rw [h, one_smul] at hnorm
    norm_num at hnorm
    have h0 : s - p = 0 := hnorm
    exact sub_eq_zero.mp h0

/--
**FR.** **B2 (cœur, groupé).** Les trois faits sur `sperp p s` (norme, orthogonalité
à `s`, produit scalaire avec `p`), établis ensemble car ils partagent la même
construction intermédiaire (`e`, le vecteur unitaire de `pᗮ` dans le plan
`(p,s)`).

**EN.** **B2 (core, grouped).** The three facts about `sperp p s` (norm,
orthogonality to `s`, inner product with `p`), established together since they
share the same intermediate construction (`e`, the unit vector of `pᗮ` in the
plane `(p,s)`).
-/
private theorem sperp_core {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsN : s ∈ northern p)
    (hsp : s ≠ p) :
    ‖sperp p s‖ = 1 ∧ ⟪s, sperp p s⟫ = 0 ∧ ⟪p, sperp p s⟫ = Real.sqrt (1 - ⟪p, s⟫ ^ 2) := by
  set c : ℝ := ⟪p, s⟫ with hc_def
  have hc0 : 0 ≤ c := hsN.2
  have hc1 : c < 1 := sperp_c_lt_one hp hs hsp
  have hc2lt1 : c ^ 2 < 1 := by nlinarith
  have hpos : (0 : ℝ) < 1 - c ^ 2 := by linarith
  have hnormsq : ‖s - c • p‖ ^ 2 = 1 - c ^ 2 := norm_sq_sub_inner_smul hp hs
  have hvne : s - c • p ≠ 0 := by
    intro h
    rw [h] at hnormsq
    simp at hnormsq
    linarith
  have hvnormpos : 0 < ‖s - c • p‖ := norm_pos_iff.mpr hvne
  have hvnorm_eq : ‖s - c • p‖ = Real.sqrt (1 - c ^ 2) := by
    rw [← hnormsq, Real.sqrt_sq (norm_nonneg _)]
  set e : E3 := ‖s - c • p‖⁻¹ • (s - c • p) with he_def
  have hpp : ⟪p, p⟫ = 1 := by rw [real_inner_self_eq_norm_sq, hp]; norm_num
  have hss : ⟪s, s⟫ = 1 := by rw [real_inner_self_eq_norm_sq, hs]; norm_num
  have hpv : ⟪p, s - c • p⟫ = 0 := by
    rw [inner_sub_right, real_inner_smul_right, hpp, ← hc_def]
    ring
  have hpe : ⟪p, e⟫ = 0 := by rw [he_def, real_inner_smul_right, hpv, mul_zero]
  have hsv : ⟪s, s - c • p⟫ = 1 - c ^ 2 := by
    rw [inner_sub_right, real_inner_smul_right, real_inner_comm p s, ← hc_def, hss]
    ring
  have hse : ⟪s, e⟫ = Real.sqrt (1 - c ^ 2) := by
    rw [he_def, real_inner_smul_right, hsv, ← hnormsq, Real.sqrt_sq (norm_nonneg _)]
    field_simp
  have he_norm : ‖e‖ = 1 := by
    rw [he_def, norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hvnormpos)]
    field_simp
  have hnormsq1 : ‖Real.sqrt (1 - c ^ 2) • p‖ ^ 2 = 1 - c ^ 2 := by
    rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, Real.sq_sqrt hpos.le, hp]
    ring
  have hnormsq2 : ‖c • e‖ ^ 2 = c ^ 2 := by
    rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, he_norm]
    ring
  have hcross : ⟪Real.sqrt (1 - c ^ 2) • p, c • e⟫ = 0 := by
    rw [real_inner_smul_left, real_inner_smul_right, hpe, mul_zero, mul_zero]
  have hnormsq_sperp : ‖sperp p s‖ ^ 2 = 1 := by
    unfold sperp
    rw [← hc_def, ← he_def, norm_sub_sq_real, hcross, hnormsq1, hnormsq2]
    ring
  have hnorm_sperp : ‖sperp p s‖ = 1 := by
    have h1 : (‖sperp p s‖ - 1) * (‖sperp p s‖ + 1) = 0 := by linear_combination hnormsq_sperp
    rcases mul_eq_zero.mp h1 with h | h
    · linarith
    · linarith [norm_nonneg (sperp p s)]
  have step3 : ⟪s, sperp p s⟫ = 0 := by
    unfold sperp
    rw [← hc_def, ← he_def, inner_sub_right, real_inner_smul_right, real_inner_smul_right,
        real_inner_comm p s, ← hc_def, hse]
    ring
  have step4 : ⟪p, sperp p s⟫ = Real.sqrt (1 - c ^ 2) := by
    unfold sperp
    rw [← hc_def, ← he_def, inner_sub_right, real_inner_smul_right, real_inner_smul_right,
        hpp, hpe]
    ring
  exact ⟨hnorm_sperp, step3, step4⟩

theorem norm_sperp {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsN : s ∈ northern p)
    (hsp : s ≠ p) : ‖sperp p s‖ = 1 := (sperp_core hp hs hsN hsp).1

theorem inner_sperp_self {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsN : s ∈ northern p)
    (hsp : s ≠ p) : ⟪s, sperp p s⟫ = 0 := (sperp_core hp hs hsN hsp).2.1

theorem inner_p_sperp {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsN : s ∈ northern p)
    (hsp : s ≠ p) : ⟪p, sperp p s⟫ = Real.sqrt (1 - ⟪p, s⟫ ^ 2) := (sperp_core hp hs hsN hsp).2.2

theorem sperp_mem_northern {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsN : s ∈ northern p)
    (hsp : s ≠ p) : sperp p s ∈ northern p := by
  refine ⟨norm_sperp hp hs hsN hsp, ?_⟩
  rw [inner_p_sperp hp hs hsN hsp]
  exact Real.sqrt_nonneg _

theorem lat_sperp {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsN : s ∈ northern p) (hsp : s ≠ p) :
    lat p (sperp p s) = 1 - lat p s := by
  have hnn : (0 : ℝ) ≤ 1 - ⟪p, s⟫ ^ 2 := by
    have := lat_le_one p hp hs
    unfold lat at this
    linarith
  unfold lat
  rw [inner_p_sperp hp hs hsN hsp, Real.sq_sqrt hnn]

/--
**FR.** Cas particulier de vérification : quand `⟪p,s⟫ = 0`, `sperp p s` se réduit à
`p` (le point de l'équateur "évident").

**EN.** Special-case check: when `⟪p,s⟫ = 0`, `sperp p s` reduces to `p` (the
"obvious" equatorial point).
-/
example (p s : E3) (hc : ⟪p, s⟫ = 0) : sperp p s = p := by
  unfold sperp
  rw [hc]
  simp

/--
**FR.** **B3.** La somme des latitudes sur une base orthonormée vaut `1` (Parseval,
`x = y = p`, puis `real_inner_comm` pour recoller `⟪p,b i⟫²`).

**EN.** **B3.** The sum of latitudes over an orthonormal basis equals `1`
(Parseval, `x = y = p`, then `real_inner_comm` to reassemble `⟪p,b i⟫²`).
-/
theorem sum_lat_eq_one {p : E3} (hp : ‖p‖ = 1) (b : OrthonormalBasis (Fin 3) ℝ E3) :
    ∑ i, lat p (b i) = 1 := by
  have h := b.sum_inner_mul_inner p p
  rw [real_inner_self_eq_norm_sq, hp] at h
  norm_num at h
  unfold lat
  rw [← h]
  apply Finset.sum_congr rfl
  intro i _
  rw [real_inner_comm p (b i)]
  ring

/--
**FR.** **B4a (lemme-outil).** Complète `sperp p s` et `s` en base orthonormée dont
le 3ᵉ vecteur est sur l'équateur : par B3, `lat(b 0) + lat(b 1) + lat(b 2) = 1`
avec `lat(b 0) = 1 - lat s` (B2) et `lat(b 1) = lat s`, donc `lat(b 2) = 0`.

**EN.** **B4a (tool lemma).** Completes `sperp p s` and `s` into an orthonormal
basis whose 3rd vector is on the equator: by B3,
`lat(b 0) + lat(b 1) + lat(b 2) = 1` with `lat(b 0) = 1 - lat s` (B2) and
`lat(b 1) = lat s`, hence `lat(b 2) = 0`.
-/
theorem exists_descent_basis {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsN : s ∈ northern p)
    (hsp : s ≠ p) :
    ∃ b : OrthonormalBasis (Fin 3) ℝ E3, b 0 = sperp p s ∧ b 1 = s ∧ b 2 ∈ equator p := by
  have hortho : ⟪sperp p s, s⟫ = 0 := by
    have h := inner_sperp_self hp hs hsN hsp
    rwa [real_inner_comm (sperp p s) s] at h
  obtain ⟨b, hb0, hb1⟩ :=
    exists_orthonormalBasis_pair (sperp p s) s (norm_sperp hp hs hsN hsp) hs hortho
  have hsum := sum_lat_eq_one hp b
  rw [Fin.sum_univ_three, hb0, hb1, lat_sperp hp hs hsN hsp] at hsum
  have hlat2 : lat p (b 2) = 0 := by linarith
  exact ⟨b, hb0, hb1, (mem_equator_iff_lat_eq_zero p (b 2)).mpr ⟨b.norm_eq_one 2, hlat2⟩⟩

/--
**FR.** **B4b (corollaire).** Le 3ᵉ vecteur de la base de B4a est à la fois dans le
cercle de descente et sur l'équateur, et orthogonal à `s`.

**EN.** **B4b (corollary).** The 3rd vector of B4a's basis lies both in the
descent circle and on the equator, and is orthogonal to `s`.
-/
theorem exists_equator_orthogonal {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1)
    (hsN : s ∈ northern p) (hsp : s ≠ p) :
    ∃ u, u ∈ descent p s ∩ equator p ∧ ⟪s, u⟫ = 0 := by
  obtain ⟨b, hb0, hb1, hb2⟩ := exists_descent_basis hp hs hsN hsp
  have hd : ⟪sperp p s, b 2⟫ = 0 := by rw [← hb0]; exact b.inner_eq_zero (by decide)
  have hse : ⟪s, b 2⟫ = 0 := by rw [← hb1]; exact b.inner_eq_zero (by decide)
  exact ⟨b 2, ⟨⟨equator_subset_northern p hb2, hd⟩, hb2⟩, hse⟩

/--
**FR.** **B5.** `s` est toujours dans son propre cercle de descente.

**EN.** **B5.** `s` always lies in its own descent circle.
-/
theorem self_mem_descent {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsN : s ∈ northern p)
    (hsp : s ≠ p) : s ∈ descent p s := by
  refine ⟨hsN, ?_⟩
  have h := inner_sperp_self hp hs hsN hsp
  rwa [real_inner_comm (sperp p s) s] at h

/--
**FR.** **B6.** Le sommet du cercle de descente est le point de latitude maximale :
`t ∈ descent p s → lat p t ≤ lat p s`. Preuve : Parseval polarisé
(`x=p,y=t`) sur la base de B4a donne `⟪p,t⟫ = ⟪p,s⟫·⟪s,t⟫` (les deux autres
termes s'annulent : `⟪sperp,t⟫=0` par définition de la descente,
`⟪p,b 2⟫=0` par B4a) ; Parseval `x=y=t` donne `⟪s,t⟫² ≤ 1`.

**EN.** **B6.** The apex of the descent circle is the point of maximal latitude:
`t ∈ descent p s → lat p t ≤ lat p s`. Proof: polarized Parseval (`x=p,y=t`) on
B4a's basis gives `⟪p,t⟫ = ⟪p,s⟫·⟪s,t⟫` (the other two terms vanish:
`⟪sperp,t⟫=0` by definition of descent, `⟪p,b 2⟫=0` by B4a); Parseval
`x=y=t` gives `⟪s,t⟫² ≤ 1`.
-/
theorem lat_le_of_mem_descent {p s t : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1) (hsN : s ∈ northern p)
    (hsp : s ≠ p) (ht : t ∈ descent p s) : lat p t ≤ lat p s := by
  obtain ⟨b, hb0, hb1, hb2⟩ := exists_descent_basis hp hs hsN hsp
  have htd : ⟪sperp p s, t⟫ = 0 := ht.2
  have htN : t ∈ northern p := ht.1
  have hpol := b.sum_inner_mul_inner p t
  rw [Fin.sum_univ_three, hb0, hb1, htd, hb2.2, mul_zero, zero_mul, add_zero, zero_add] at hpol
  have hlat_eq : lat p t = lat p s * ⟪s, t⟫ ^ 2 := by
    unfold lat
    rw [← hpol]
    ring
  have hsum_t := b.sum_sq_inner_right t
  rw [htN.1] at hsum_t
  norm_num at hsum_t
  rw [Fin.sum_univ_three, hb1] at hsum_t
  have hββ : ⟪s, t⟫ ^ 2 ≤ 1 := by
    nlinarith [sq_nonneg (⟪b 0, t⟫ : ℝ), sq_nonneg (⟪b 2, t⟫ : ℝ), hsum_t]
  rw [hlat_eq]
  exact mul_le_of_le_one_right (lat_nonneg p s) hββ

/--
**FR.** **B7.** Réalisabilité des latitudes : pour tout triplet de latitudes
positives sommant à 1, il existe une base orthonormée les réalisant.
Construction sans matrices : `v := √l₁•E0+√l₂•E1+√l₃•E2` (`E` = base standard)
est unitaire ; on transporte `E` par l'isométrie envoyant `v` sur `p`
(composée des représentations de deux bases étendant `v` et `p`).

**EN.** **B7.** Realizability of latitudes: for any triple of positive latitudes
summing to 1, there exists an orthonormal basis realizing them. Matrix-free
construction: `v := √l₁•E0+√l₂•E1+√l₃•E2` (`E` = standard basis) is a unit
vector; transport `E` via the isometry sending `v` to `p` (composition of the
representations of two bases extending `v` and `p`).
-/
theorem exists_frame_with_lat {p : E3} (hp : ‖p‖ = 1) {l₁ l₂ l₃ : ℝ}
    (h₁ : 0 ≤ l₁) (h₂ : 0 ≤ l₂) (h₃ : 0 ≤ l₃) (hsum : l₁ + l₂ + l₃ = 1) :
    ∃ b : OrthonormalBasis (Fin 3) ℝ E3,
      lat p (b 0) = l₁ ∧ lat p (b 1) = l₂ ∧ lat p (b 2) = l₃ := by
  set E := EuclideanSpace.basisFun (Fin 3) ℝ with hE_def
  set v : E3 := Real.sqrt l₁ • E 0 + Real.sqrt l₂ • E 1 + Real.sqrt l₃ • E 2 with hv_def
  have hE01 : (⟪E 0, E 1⟫ : ℝ) = 0 := E.inner_eq_zero (by decide)
  have hE11 : (⟪E 1, E 1⟫ : ℝ) = 1 := E.inner_eq_one 1
  have hE21 : (⟪E 2, E 1⟫ : ℝ) = 0 := E.inner_eq_zero (by decide)
  have hE00 : (⟪E 0, E 0⟫ : ℝ) = 1 := E.inner_eq_one 0
  have hE10 : (⟪E 1, E 0⟫ : ℝ) = 0 := E.inner_eq_zero (by decide)
  have hE20 : (⟪E 2, E 0⟫ : ℝ) = 0 := E.inner_eq_zero (by decide)
  have hE02 : (⟪E 0, E 2⟫ : ℝ) = 0 := E.inner_eq_zero (by decide)
  have hE12 : (⟪E 1, E 2⟫ : ℝ) = 0 := E.inner_eq_zero (by decide)
  have hE22 : (⟪E 2, E 2⟫ : ℝ) = 1 := E.inner_eq_one 2
  have hv0 : ⟪v, E 0⟫ = Real.sqrt l₁ := by
    rw [hv_def, inner_add_left, inner_add_left, real_inner_smul_left, real_inner_smul_left,
        real_inner_smul_left, hE00, hE10, hE20]
    ring
  have hv1 : ⟪v, E 1⟫ = Real.sqrt l₂ := by
    rw [hv_def, inner_add_left, inner_add_left, real_inner_smul_left, real_inner_smul_left,
        real_inner_smul_left, hE01, hE11, hE21]
    ring
  have hv2 : ⟪v, E 2⟫ = Real.sqrt l₃ := by
    rw [hv_def, inner_add_left, inner_add_left, real_inner_smul_left, real_inner_smul_left,
        real_inner_smul_left, hE02, hE12, hE22]
    ring
  have hvv : ⟪v, v⟫ = l₁ + l₂ + l₃ := by
    nth_rewrite 2 [hv_def]
    rw [inner_add_right, inner_add_right, real_inner_smul_right, real_inner_smul_right,
        real_inner_smul_right, hv0, hv1, hv2, Real.mul_self_sqrt h₁, Real.mul_self_sqrt h₂,
        Real.mul_self_sqrt h₃]
  have hvnorm : ‖v‖ = 1 := by
    have hsq : ‖v‖ ^ 2 = 1 := by rw [← real_inner_self_eq_norm_sq, hvv, hsum]
    nlinarith [norm_nonneg v, hsq]
  obtain ⟨bᵥ, hbᵥ0⟩ := exists_orthonormalBasis_fst v hvnorm
  obtain ⟨c_p, hc_p0⟩ := exists_orthonormalBasis_fst p hp
  set U : E3 ≃ₗᵢ[ℝ] E3 := bᵥ.repr.trans c_p.repr.symm with hU_def
  have hUv : U v = p := by
    have h1 : bᵥ.repr v = EuclideanSpace.single 0 (1 : ℝ) := by
      conv_lhs => rw [← hbᵥ0]
      exact bᵥ.repr_self 0
    have h2 : c_p.repr (c_p 0) = EuclideanSpace.single 0 (1 : ℝ) := c_p.repr_self 0
    rw [hU_def, LinearIsometryEquiv.trans_apply, h1, ← h2, LinearIsometryEquiv.symm_apply_apply,
        hc_p0]
  set b := E.map U with hb_def
  have hinner : ∀ j, ⟪p, b j⟫ = ⟪v, E j⟫ := by
    intro j
    rw [hb_def, OrthonormalBasis.map_apply, ← hUv, U.inner_map_map]
  refine ⟨b, ?_, ?_, ?_⟩
  · unfold lat; rw [hinner 0, hv0, Real.sq_sqrt h₁]
  · unfold lat; rw [hinner 1, hv1, Real.sq_sqrt h₂]
  · unfold lat; rw [hinner 2, hv2, Real.sq_sqrt h₃]

end
end Gleason
