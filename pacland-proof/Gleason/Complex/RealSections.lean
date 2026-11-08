import Gleason.Defs
import Gleason.Real3.Regular

/-!
**FR.** # Réduction complexe par sections réelles (Dvurečenskij, ch. 3)

Passage de ℝ³ (cœur analytique de `Real3/`) au cas complexe ℂⁿ, `n ≥ 3` :

1. une frame function complexe, restreinte à un sous-espace RÉEL complètement réel
   de dimension 3 (une « section réelle »), est une frame function réelle sur ℝ³ ;
2. `Real3.frameFunction_regular` donne une forme quadratique sur chaque section ;
3. le recollement des sections (`Patching.lean`) produit une forme sesquilinéaire
   globale — c'est exactement là que l'ancienne « obligation G » (sesquilinéarité du
   noyau de polarisation) devient un THÉORÈME, démontré par la géométrie des sections
   et l'hypothèse `dim ≥ 3`, et non par l'algèbre seule.

Jalon M3 complet (voir `SORRIES.md`) : `realSection` est le plongement ℝ-linéaire
`E3 → H n` associé à un triplet orthonormé complexe (isométrique, préserve les phases),
et `cFrameFunction_regular` (`Patching.lean`) est l'aboutissement de ce fichier.

**EN.** # Complex reduction via real sections (Dvurečenskij, ch. 3)

Passage from ℝ³ (analytic core of `Real3/`) to the complex case ℂⁿ, `n ≥ 3`:

1. a complex frame function, restricted to a completely real REAL subspace of
   dimension 3 (a "real section"), is a real frame function on ℝ³;
2. `Real3.frameFunction_regular` gives a quadratic form on each section;
3. patching the sections together (`Patching.lean`) produces a global sesquilinear
   form — this is exactly where the old "obligation G" (sesquilinearity of the
   polarization kernel) becomes a THEOREM, proved via the geometry of the sections
   and the hypothesis `dim ≥ 3`, rather than by algebra alone.

Milestone M3 complete (see `SORRIES.md`): `realSection` is the ℝ-linear embedding
`E3 → H n` associated with a complex orthonormal triple (isometric, phase-preserving),
and `cFrameFunction_regular` (`Patching.lean`) is the culmination of this file.
-/

namespace Gleason

open scoped InnerProductSpace

noncomputable section

variable {n : ℕ}

/- ═══════════════════════════════════════════════════════════════════
   M3-0. Extension d'une famille orthonormée complexe, à positions
   prescrites (via `Fin.castLE`), en base orthonormée de `H n`. Généralise
   `exists_orthonormalBasis_of_triple'` (bloc A, `Real3/SphereGeometry.lean`,
   hardcodé `ℝ`/`Fin 3`) : ici `k` est arbitraire (`k ≤ n`) et le corps est
   `ℂ`. Le lemme Mathlib sous-jacent
   (`Orthonormal.exists_orthonormalBasis_extension_of_card_eq`) est déjà
   générique en `𝕜`.
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** Toute famille orthonormée `v : Fin k → H n` (`k ≤ n`) se complète en une base
orthonormée de `H n` qui coïncide avec `v` sur les `k` premières positions
(`Fin.castLE`).

**EN.** Every orthonormal family `v : Fin k → H n` (`k ≤ n`) extends to an orthonormal
basis of `H n` that agrees with `v` on the first `k` positions (`Fin.castLE`).
-/
theorem exists_orthonormalBasis_extension_complex {k : ℕ} (hk : k ≤ n) (v : Fin k → H n)
    (hv : Orthonormal ℂ v) :
    ∃ b : OrthonormalBasis (Fin n) ℂ (H n), ∀ i : Fin k, b (Fin.castLE hk i) = v i := by
  have hinj : Function.Injective (Fin.castLE hk : Fin k → Fin n) := Fin.castLE_injective hk
  set V : Fin n → H n := Function.extend (Fin.castLE hk) v (fun _ => 0) with hV_def
  have hVv : ∀ i : Fin k, V (Fin.castLE hk i) = v i := fun i =>
    hinj.extend_apply v (fun _ => (0 : H n)) i
  set e : Fin k ≃ Set.range (Fin.castLE hk) := Equiv.ofInjective (Fin.castLE hk) hinj with he_def
  have hcomp : (Fin.castLE hk : Fin k → Fin n) ∘ e.symm = Subtype.val :=
    Equiv.self_comp_ofInjective_symm hinj
  have hrestrict : (Set.range (Fin.castLE hk)).restrict V = v ∘ e.symm := by
    funext x
    have hx1 : Fin.castLE hk (e.symm x) = (x : Fin n) := congrFun hcomp x
    show V (x : Fin n) = v (e.symm x)
    rw [← hx1, hVv]
  have hOrtho : Orthonormal ℂ ((Set.range (Fin.castLE hk)).restrict V) := by
    rw [hrestrict]; exact hv.comp e.symm e.symm.injective
  have hcard : Module.finrank ℂ (H n) = Fintype.card (Fin n) := by simp
  obtain ⟨b, hb⟩ := hOrtho.exists_orthonormalBasis_extension_of_card_eq hcard
  exact ⟨b, fun i => by rw [hb (Fin.castLE hk i) ⟨i, rfl⟩, hVv]⟩

/-- **Frame function complexe de poids `W`** sur `ℂⁿ`. -/
def IsCFrameFunction (g : H n → ℝ) (W : ℝ) : Prop :=
  ∀ b : OrthonormalBasis (Fin n) ℂ (H n), (∑ i, g (b i)) = W

/--
**FR.** La frame function d'une mesure de projection : `x ↦ μ (ℂ ∙ x)`.

**EN.** The frame function of a projection measure: `x ↦ μ (ℂ ∙ x)`.
-/
def ProjMeasure.frameFunction (m : ProjMeasure n) : H n → ℝ :=
  fun x => m.μ (ℂ ∙ x)

/--
**FR.** **M3-1(b) préliminaire.** Additivité finie sur une famille deux à deux orthogonale
(indexée par un `Finset`) : généralise `add_isOrtho` par récurrence sur le `Finset`.
`i ∈ s` orthogonal à `s.sup A` s'obtient de `i ⊥ A j` pour tout `j ∈ s` via
`Submodule.isOrtho_iSup_right` (le sup fini est un cas particulier du sup indexé).

**EN.** **M3-1(b) preliminary.** Finite additivity on a pairwise orthogonal family
(indexed by a `Finset`): generalizes `add_isOrtho` by induction on the `Finset`.
`i ∈ s` orthogonal to `s.sup A` follows from `i ⊥ A j` for all `j ∈ s` via
`Submodule.isOrtho_iSup_right` (the finite sup is a special case of the indexed sup).
-/
theorem ProjMeasure.sum_eq_of_pairwise_isOrtho (m : ProjMeasure n) {ι : Type*} [DecidableEq ι]
    (s : Finset ι) (A : ι → Submodule ℂ (H n))
    (hortho : ∀ i ∈ s, ∀ j ∈ s, i ≠ j → A i ⟂ A j) :
    m.μ (s.sup A) = ∑ i ∈ s, m.μ (A i) := by
  induction s using Finset.induction with
  | empty => simp [m.bot_eq_zero]
  | insert i s hi ih =>
    have hi_ortho : A i ⟂ s.sup A := by
      apply Finset.sup_induction Submodule.isOrtho_bot_right
        (fun a1 h1 a2 h2 => Submodule.isOrtho_sup_right.mpr ⟨h1, h2⟩)
      intro j hj
      exact hortho i (Finset.mem_insert_self i s) j (Finset.mem_insert_of_mem hj)
        (fun heq => hi (heq ▸ hj))
    have hs_sub : ∀ j ∈ s, ∀ k ∈ s, j ≠ k → A j ⟂ A k := fun j hj k hk hjk =>
      hortho j (Finset.mem_insert_of_mem hj) k (Finset.mem_insert_of_mem hk) hjk
    rw [Finset.sup_insert, m.add_isOrtho _ _ hi_ortho, ih hs_sub, Finset.sum_insert hi]

/--
**FR.** (Phase M) La frame function d'une mesure de projection est une frame function
complexe de poids 1. Indication : une base orthonormée découpe `⊤` en droites deux à
deux orthogonales ; itérer `add_isOrtho` (via `sum_eq_of_pairwise_isOrtho`).

**EN.** (Phase M) The frame function of a projection measure is a complex frame
function of weight 1. Hint: an orthonormal basis splits `⊤` into pairwise orthogonal
lines; iterate `add_isOrtho` (via `sum_eq_of_pairwise_isOrtho`).
-/
theorem ProjMeasure.isCFrameFunction (m : ProjMeasure n) :
    IsCFrameFunction m.frameFunction 1 := by
  intro b
  have hortho : ∀ i ∈ (Finset.univ : Finset (Fin n)), ∀ j ∈ (Finset.univ : Finset (Fin n)),
      i ≠ j → (ℂ ∙ b i) ⟂ (ℂ ∙ b j) := by
    intro i _ j _ hij
    rw [Submodule.isOrtho_span]
    rintro x hx y hy
    simp only [Set.mem_singleton_iff] at hx hy
    rw [hx, hy, b.inner_eq_ite]
    simp [hij]
  have hsum := m.sum_eq_of_pairwise_isOrtho Finset.univ (fun i => ℂ ∙ b i) hortho
  have htop : (Finset.univ : Finset (Fin n)).sup (fun i => ℂ ∙ b i) = ⊤ := by
    rw [Finset.sup_eq_iSup]
    simp only [Finset.mem_univ, iSup_pos]
    rw [← Submodule.span_range_eq_iSup]
    exact b.toBasis.span_eq
  rw [htop, m.top_eq_one] at hsum
  unfold ProjMeasure.frameFunction
  exact hsum.symm

/--
**FR.** Invariance de phase : `g (c • x) = g x` pour `‖c‖ = 1` — automatique pour les
frame functions issues de mesures, car `ℂ ∙ (c • x) = ℂ ∙ x`.

**EN.** Phase invariance: `g (c • x) = g x` for `‖c‖ = 1` — automatic for frame
functions arising from measures, since `ℂ ∙ (c • x) = ℂ ∙ x`.
-/
theorem ProjMeasure.frameFunction_phase (m : ProjMeasure n) (c : ℂ) (x : H n)
    (hc : ‖c‖ = 1) : m.frameFunction (c • x) = m.frameFunction x := by
  have hc0 : c ≠ 0 := by
    intro h; rw [h, norm_zero] at hc; norm_num at hc
  unfold ProjMeasure.frameFunction
  rw [Submodule.span_singleton_smul_eq hc0.isUnit]

/- ═══════════════════════════════════════════════════════════════════
   M3-2. Invariance de `∑ g(v i)` par changement de base orthonormée
   d'un même sous-espace (engendré par `v` ou par `v'`).
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **M3-2.** Si `v, v' : Fin k → H n` sont orthonormées et engendrent le même
sous-espace, les sommes `∑ g(v i)` et `∑ g(v' i)` coïncident, pour `g` frame
function complexe de poids `W`. Preuve : étend `v` en base `b` de `H n`
(`exists_orthonormalBasis_extension_complex`) ; la famille hybride `w`
(`v'` sur les `k` premières positions, la queue de `b` ensuite) est
orthonormée — la queue de `b` est orthogonale à `span(range v) = span(range v')`
donc à chaque `v' i` — donc base ; les deux sommes valent `W` (`hg`), la
queue commune s'annule par soustraction.

**EN.** **M3-2.** If `v, v' : Fin k → H n` are orthonormal and span the same
subspace, the sums `∑ g(v i)` and `∑ g(v' i)` coincide, for `g` a complex frame
function of weight `W`. Proof: extend `v` to a basis `b` of `H n`
(`exists_orthonormalBasis_extension_complex`); the hybrid family `w`
(`v'` on the first `k` positions, then the tail of `b`) is orthonormal — the tail
of `b` is orthogonal to `span(range v) = span(range v')` and hence to each `v' i` —
so it is a basis; both sums equal `W` (`hg`), and the common tail cancels by
subtraction.
-/
theorem cframe_sum_invariant {g : H n → ℝ} {W : ℝ} (hg : IsCFrameFunction g W)
    {k : ℕ} (hk : k ≤ n) (v v' : Fin k → H n) (hv : Orthonormal ℂ v) (hv' : Orthonormal ℂ v')
    (hspan : Submodule.span ℂ (Set.range v) = Submodule.span ℂ (Set.range v')) :
    ∑ i, g (v i) = ∑ i, g (v' i) := by
  have hzero_symm : ∀ x y : H n, ⟪x, y⟫_ℂ = 0 → ⟪y, x⟫_ℂ = 0 := by
    intro x y hxy
    have h := congrArg (starRingEnd ℂ) hxy
    rwa [inner_conj_symm, map_zero] at h
  obtain ⟨b, hb⟩ := exists_orthonormalBasis_extension_complex hk v hv
  set w : Fin n → H n := fun j => if h : j.1 < k then v' ⟨j.1, h⟩ else b j with hw_def
  have hw_lt : ∀ j : Fin n, ∀ h : j.1 < k, w j = v' ⟨j.1, h⟩ := fun j h => by simp [hw_def, h]
  have hw_ge : ∀ j : Fin n, ¬ j.1 < k → w j = b j := fun j h => by simp [hw_def, h]
  have hw_castLE : ∀ i : Fin k, w (Fin.castLE hk i) = v' i := by
    intro i
    rw [hw_lt (Fin.castLE hk i) (by simp)]
    exact congrArg v' (Fin.ext rfl)
  have hb_tail_orth : ∀ j : Fin n, ¬ j.1 < k → ∀ x ∈ Submodule.span ℂ (Set.range v),
      ⟪b j, x⟫_ℂ = 0 := by
    intro j hj x hx
    refine Submodule.span_induction ?_ ?_ ?_ ?_ hx
    · rintro y ⟨i, rfl⟩
      rw [← hb i]
      have hij : j ≠ Fin.castLE hk i := by
        intro heq; apply hj; rw [heq]; simp
      exact b.orthonormal.2 hij
    · simp
    · intro y z _ _ hy hz; rw [inner_add_right, hy, hz, add_zero]
    · intro c y _ hy; rw [inner_smul_right, hy, mul_zero]
  have hw_orth : Orthonormal ℂ w := by
    constructor
    · intro j
      by_cases hj : j.1 < k
      · rw [hw_lt j hj]; exact hv'.1 _
      · rw [hw_ge j hj]; exact b.orthonormal.1 j
    · intro i j hij
      by_cases hi : i.1 < k <;> by_cases hj : j.1 < k
      · rw [hw_lt i hi, hw_lt j hj]
        have hij' : (⟨i.1, hi⟩ : Fin k) ≠ ⟨j.1, hj⟩ := by
          simp only [ne_eq, Fin.mk.injEq]
          intro heq; exact hij (Fin.ext heq)
        exact hv'.2 hij'
      · rw [hw_lt i hi, hw_ge j hj]
        have hvi : v' ⟨i.1, hi⟩ ∈ Submodule.span ℂ (Set.range v) := by
          rw [hspan]; exact Submodule.subset_span ⟨⟨i.1, hi⟩, rfl⟩
        exact hzero_symm _ _ (hb_tail_orth j hj (v' ⟨i.1, hi⟩) hvi)
      · rw [hw_ge i hi, hw_lt j hj]
        have hvj : v' ⟨j.1, hj⟩ ∈ Submodule.span ℂ (Set.range v) := by
          rw [hspan]; exact Submodule.subset_span ⟨⟨j.1, hj⟩, rfl⟩
        exact hb_tail_orth i hi (v' ⟨j.1, hj⟩) hvj
      · rw [hw_ge i hi, hw_ge j hj]; exact b.orthonormal.2 hij
  have hcard : Module.finrank ℂ (H n) = Fintype.card (Fin n) := by simp
  have hw_univ : Orthonormal ℂ ((Set.univ : Set (Fin n)).restrict w) :=
    ⟨fun i => hw_orth.1 i.1, fun i j hij => hw_orth.2 (fun h => hij (Subtype.ext h))⟩
  obtain ⟨bw, hbw⟩ := hw_univ.exists_orthonormalBasis_extension_of_card_eq hcard
  have hbw' : ∀ i, bw i = w i := fun i => hbw i (Set.mem_univ i)
  have hsumb := hg b
  have hsumbw := hg bw
  have hD_zero_outside : ∀ i : Fin n, (∀ j : Fin k, Fin.castLE hk j ≠ i) →
      g (b i) - g (bw i) = 0 := by
    intro i hi
    have hnotlt : ¬ i.1 < k := fun hlt => hi ⟨i.1, hlt⟩ (Fin.ext rfl)
    rw [hbw' i, hw_ge i hnotlt]; ring
  have hsum_eq : ∑ i : Fin n, (g (b i) - g (bw i)) = ∑ j : Fin k, (g (v j) - g (v' j)) := by
    have hstep1 : ∑ i : Fin n, (g (b i) - g (bw i))
        = ∑ i ∈ Finset.univ.image (Fin.castLE hk), (g (b i) - g (bw i)) := by
      symm
      apply Finset.sum_subset (Finset.subset_univ _)
      intro i _ hi
      apply hD_zero_outside i
      intro j hji
      exact hi (Finset.mem_image.mpr ⟨j, Finset.mem_univ j, hji⟩)
    rw [hstep1, Finset.sum_image (fun a _ b _ hab => Fin.castLE_injective hk hab)]
    apply Finset.sum_congr rfl
    intro j _
    rw [hb j, hbw' (Fin.castLE hk j), hw_castLE j]
  have hsum0 : ∑ i : Fin n, (g (b i) - g (bw i)) = 0 := by
    rw [Finset.sum_sub_distrib, hsumb, hsumbw, sub_self]
  rw [hsum0] at hsum_eq
  have hfinal := hsum_eq.symm
  rw [Finset.sum_sub_distrib] at hfinal
  linarith [hfinal]

/--
**FR.** **M3-2 (corollaire).** Une frame function complexe positive est bornée par son poids :
complète `x` en base (`k := 1`) et compare au terme isolé, les autres étant `≥ 0` (`hnn`).

**EN.** **M3-2 (corollary).** A positive complex frame function is bounded by its
weight: complete `x` into a basis (`k := 1`) and compare with the isolated term,
the others being `≥ 0` (`hnn`).
-/
theorem cframe_le_weight {g : H n → ℝ} {W : ℝ} (hg : IsCFrameFunction g W)
    (hnn : ∀ x, ‖x‖ = 1 → 0 ≤ g x) (hn1 : 1 ≤ n) {x : H n} (hx : ‖x‖ = 1) : g x ≤ W := by
  have hvx : Orthonormal ℂ (fun _ : Fin 1 => x) :=
    ⟨fun _ => hx, fun i j hij => absurd (Subsingleton.elim i j) hij⟩
  obtain ⟨b, hb⟩ := exists_orthonormalBasis_extension_complex hn1 (fun _ : Fin 1 => x) hvx
  have hsum := hg b
  have h0 : b (Fin.castLE hn1 0) = x := hb 0
  rw [← h0, ← hsum]
  exact Finset.single_le_sum (fun i _ => hnn (b i) (b.norm_eq_one i)) (Finset.mem_univ _)

/- ═══════════════════════════════════════════════════════════════════
   M3-7. Infrastructure de sous-espaces pour l'induction d'épluchage
   (M3-8) : pour `x` unitaire dans `U`, `U' := U ⊓ (ℂ∙x)ᗮ` est le
   complément orthogonal de `x` DANS `U`.
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **M3-7(a).** Pour `x` unitaire dans `U`, la projection `w - ⟪x,w⟫•x` de tout
`w ∈ U` reste dans `U` (différence de deux éléments de `U`) et est orthogonale à `x`.

**EN.** **M3-7(a).** For `x` a unit vector in `U`, the projection `w - ⟪x,w⟫•x` of any
`w ∈ U` remains in `U` (difference of two elements of `U`) and is orthogonal to `x`.
-/
theorem sub_proj_mem_inf_orthogonal {U : Submodule ℂ (H n)} {x : H n} (hxU : x ∈ U)
    (hxnorm : ‖x‖ = 1) {w : H n} (hw : w ∈ U) :
    w - ⟪x, w⟫_ℂ • x ∈ U ⊓ (Submodule.span ℂ ({x} : Set (H n)))ᗮ := by
  rw [Submodule.mem_inf]
  refine ⟨Submodule.sub_mem _ hw (Submodule.smul_mem _ _ hxU), ?_⟩
  rw [Submodule.mem_orthogonal_singleton_iff_inner_right, inner_sub_right, inner_smul_right,
    inner_self_eq_norm_sq_to_K, hxnorm]
  simp

/--
**FR.** **M3-7(b).** Décomposition orthogonale interne : pour `x` unitaire dans `U`, le complément
orthogonal `U ⊓ (ℂ∙x)ᗮ` a une dimension de moins que `U`.

**EN.** **M3-7(b).** Internal orthogonal decomposition: for `x` a unit vector in `U`,
the orthogonal complement `U ⊓ (ℂ∙x)ᗮ` has dimension one less than `U`.
-/
theorem finrank_inf_orthogonal_add_one {U : Submodule ℂ (H n)} {x : H n} (hxU : x ∈ U)
    (hxnorm : ‖x‖ = 1) :
    Module.finrank ℂ (U ⊓ (Submodule.span ℂ ({x} : Set (H n)))ᗮ : Submodule ℂ (H n))
      + 1 = Module.finrank ℂ U := by
  have hx0 : x ≠ 0 := by intro h; rw [h, norm_zero] at hxnorm; norm_num at hxnorm
  have hle : Submodule.span ℂ ({x} : Set (H n)) ≤ U := by
    rw [Submodule.span_le, Set.singleton_subset_iff]; exact hxU
  have hfin1 : Module.finrank ℂ (Submodule.span ℂ ({x} : Set (H n))) = 1 :=
    finrank_span_singleton hx0
  have h := Submodule.finrank_add_inf_finrank_orthogonal hle
  rw [hfin1, inf_comm] at h
  omega

/--
**FR.** **M3-7(c).** Le plan complexe engendré par deux éléments d'un sous-espace `U` reste
dans `U`.

**EN.** **M3-7(c).** The complex plane spanned by two elements of a subspace `U`
remains in `U`.
-/
theorem span_pair_le_of_mem {U : Submodule ℂ (H n)} {x y : H n} (hx : x ∈ U) (hy : y ∈ U) :
    Submodule.span ℂ ({x, y} : Set (H n)) ≤ U := by
  rw [Submodule.span_le, Set.insert_subset_iff, Set.singleton_subset_iff]
  exact ⟨hx, hy⟩

/- ═══════════════════════════════════════════════════════════════════
   M3-3 à M3-9 : hypothèses de section communes. `g` frame function
   complexe positive et invariante de phase, `n ≥ 3`.
   ═══════════════════════════════════════════════════════════════════ -/

section CFrameSections

variable {g : H n → ℝ} {W : ℝ} (hg : IsCFrameFunction g W) (hnn : ∀ x, ‖x‖ = 1 → 0 ≤ g x)
  (hphase : ∀ (c : ℂ) (x : H n), ‖c‖ = 1 → g (c • x) = g x) (hn : 3 ≤ n)

/--
**FR.** **M3-3.** Extension homogène de degré 2 de `g` (nulle en `0`, `g` sur la sphère unité
sinon, prolongée par `q(c • z) = ‖c‖² q z`).

**EN.** **M3-3.** Degree-2 homogeneous extension of `g` (zero at `0`, equal to `g` on
the unit sphere otherwise, extended by `q(c • z) = ‖c‖² q z`).
-/
noncomputable def homogExt (g : H n → ℝ) (z : H n) : ℝ :=
  if z = 0 then 0 else ‖z‖ ^ 2 * g ((‖z‖⁻¹ : ℂ) • z)

theorem homogExt_of_unit {z : H n} (hz : ‖z‖ = 1) : homogExt g z = g z := by
  have hz0 : z ≠ 0 := by intro h; rw [h, norm_zero] at hz; norm_num at hz
  unfold homogExt
  rw [if_neg hz0, hz]
  norm_num

include hphase in
theorem homogExt_smul (c : ℂ) (z : H n) :
    homogExt g (c • z) = ‖c‖ ^ 2 * homogExt g z := by
  by_cases hz0 : z = 0
  · subst hz0; simp [homogExt]
  by_cases hc0 : c = 0
  · subst hc0; simp [homogExt]
  have hcz0 : c • z ≠ 0 := smul_ne_zero hc0 hz0
  have hcnorm : ‖c‖ ≠ 0 := norm_ne_zero_iff.mpr hc0
  have hznorm : ‖z‖ ≠ 0 := norm_ne_zero_iff.mpr hz0
  have hcC : (‖c‖ : ℂ) ≠ 0 := by exact_mod_cast hcnorm
  have hzC : (‖z‖ : ℂ) ≠ 0 := by exact_mod_cast hznorm
  unfold homogExt
  rw [if_neg hcz0, if_neg hz0]
  have harg : (‖c • z‖⁻¹ : ℂ) • (c • z) = (c / (‖c‖ : ℂ)) • ((‖z‖⁻¹ : ℂ) • z) := by
    rw [norm_smul, smul_smul, smul_smul]
    congr 1
    push_cast
    field_simp
  rw [harg, hphase (c / (‖c‖ : ℂ)) ((‖z‖⁻¹ : ℂ) • z) (by
    rw [norm_div, Complex.norm_real, Real.norm_eq_abs, abs_norm, div_self hcnorm])]
  rw [norm_smul]
  ring

include hnn in
theorem homogExt_nonneg (z : H n) : 0 ≤ homogExt g z := by
  by_cases hz0 : z = 0
  · subst hz0; simp [homogExt]
  unfold homogExt
  rw [if_neg hz0]
  have hunit : ‖(‖z‖⁻¹ : ℂ) • z‖ = 1 := by
    rw [norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_norm,
      inv_mul_cancel₀ (norm_ne_zero_iff.mpr hz0)]
  exact mul_nonneg (by positivity) (hnn _ hunit)

include hg hnn hn in
theorem homogExt_le (z : H n) : homogExt g z ≤ W * ‖z‖ ^ 2 := by
  by_cases hz0 : z = 0
  · subst hz0; simp [homogExt]
  unfold homogExt
  rw [if_neg hz0]
  have hunit : ‖(‖z‖⁻¹ : ℂ) • z‖ = 1 := by
    rw [norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_norm,
      inv_mul_cancel₀ (norm_ne_zero_iff.mpr hz0)]
  have hle := cframe_le_weight hg hnn (by omega) hunit
  nlinarith [sq_nonneg ‖z‖, hle]

/- ═══════════════════════════════════════════════════════════════════
   M3-4. Sections réelles : plongement `ι_v` de `E3` dans `H n` associé
   à un triplet orthonormé complexe `v`, isométrique (préserve le
   produit scalaire réel), fournissant une frame function réelle
   `f_v := g ∘ ι_v` dont `frameFunction_regular` (M2) donne la forme
   quadratique `Q_v`.
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** Section réelle associée à un triplet orthonormé complexe `v : Fin 3 → H n` :
plongement ℝ-linéaire (fonction nue, pas de bundling `LinearIsometry`) de `E3`
dans `H n`.

**EN.** Real section associated with a complex orthonormal triple `v : Fin 3 → H n`:
the (bare-function, not `LinearIsometry`-bundled) ℝ-linear embedding of `E3` into
`H n`.
-/
noncomputable def realSection (v : Fin 3 → H n) (x : E3) : H n := ∑ i, (x i : ℂ) • v i

theorem realSection_inner (v : Fin 3 → H n) (hv : Orthonormal ℂ v) (x y : E3) :
    ⟪realSection v x, realSection v y⟫_ℂ = (⟪x, y⟫_ℝ : ℂ) := by
  have hvite := orthonormal_iff_ite.mp hv
  have hstar_real : ∀ r : ℝ, star (r : ℂ) = (r : ℂ) := fun r => by
    rw [← starRingEnd_apply, Complex.conj_ofReal]
  unfold realSection
  rw [Fin.sum_univ_three, Fin.sum_univ_three]
  simp only [inner_add_left, inner_add_right, inner_smul_left, inner_smul_right, hvite]
  simp only [PiLp.inner_apply, RCLike.inner_apply, Fin.sum_univ_three,
    starRingEnd_apply, star_trivial, hstar_real]
  push_cast
  ring

theorem realSection_norm (v : Fin 3 → H n) (hv : Orthonormal ℂ v) (x : E3) :
    ‖realSection v x‖ = ‖x‖ := by
  have hkey := realSection_inner v hv x x
  rw [inner_self_eq_norm_sq_to_K, real_inner_self_eq_norm_sq] at hkey
  have h2 : ‖realSection v x‖ ^ 2 = ‖x‖ ^ 2 := by
    apply Complex.ofReal_inj.mp; push_cast at hkey ⊢; exact hkey
  have hh := Real.sqrt_sq (norm_nonneg (realSection v x))
  rw [h2, Real.sqrt_sq (norm_nonneg x)] at hh
  exact hh.symm

theorem realSection_orthonormal (v : Fin 3 → H n) (hv : Orthonormal ℂ v)
    (b : OrthonormalBasis (Fin 3) ℝ E3) : Orthonormal ℂ (fun i => realSection v (b i)) := by
  rw [orthonormal_iff_ite]
  intro i j
  rw [realSection_inner v hv, b.inner_eq_ite]
  split_ifs <;> simp

theorem realSection_span (v : Fin 3 → H n) (hv : Orthonormal ℂ v)
    (b : OrthonormalBasis (Fin 3) ℝ E3) : Submodule.span ℂ (Set.range (fun i => realSection v (b i)))
    = Submodule.span ℂ (Set.range v) := by
  have hle : Submodule.span ℂ (Set.range (fun i => realSection v (b i)))
      ≤ Submodule.span ℂ (Set.range v) := by
    rw [Submodule.span_le]
    rintro y ⟨i, rfl⟩
    unfold realSection
    exact Submodule.sum_mem _ (fun j _ => Submodule.smul_mem _ _ (Submodule.subset_span ⟨j, rfl⟩))
  have hfin_v : Module.finrank ℂ (Submodule.span ℂ (Set.range v)) = 3 := by
    have h := finrank_span_eq_card hv.linearIndependent
    simpa using h
  have hfin_b : Module.finrank ℂ (Submodule.span ℂ (Set.range (fun i => realSection v (b i))))
      = 3 := by
    have h := finrank_span_eq_card (realSection_orthonormal v hv b).linearIndependent
    simpa using h
  exact Submodule.eq_of_le_of_finrank_eq hle (by rw [hfin_b, hfin_v])

include hg hn in
theorem realSection_isFrameFunction (v : Fin 3 → H n) (hv : Orthonormal ℂ v) :
    IsFrameFunction (fun x => g (realSection v x)) (∑ i, g (v i)) := by
  intro b
  exact (cframe_sum_invariant hg hn v (fun i => realSection v (b i)) hv
    (realSection_orthonormal v hv b) (realSection_span v hv b).symm).symm

include hnn in
theorem realSection_nonneg (v : Fin 3 → H n) (hv : Orthonormal ℂ v) {x : E3} (hx : ‖x‖ = 1) :
    0 ≤ g (realSection v x) := by
  rw [← realSection_norm v hv x] at hx; exact hnn _ hx

include hg hnn hn in
theorem exists_Qv (v : Fin 3 → H n) (hv : Orthonormal ℂ v) :
    ∃ Q : QuadraticForm ℝ E3, ∀ x : E3, ‖x‖ = 1 → g (realSection v x) = Q x :=
  frameFunction_regular (fun x => g (realSection v x)) (∑ i, g (v i))
    (realSection_isFrameFunction hg hn v hv) (fun _ hx => realSection_nonneg hnn v hv hx)

include hg hnn hphase hn in
/--
**FR.** **M3-4 (assemblage).** Extension homogène de `g` composée avec la section réelle : c'est
la forme quadratique `Q_v` donnée par `frameFunction_regular` (M2), prolongée à `E3` entier par
homogénéité (`homogExt_smul` et `QuadraticMap.map_smul` des deux côtés).

**EN.** **M3-4 (assembly).** The homogeneous extension of `g` composed with the real
section: this is exactly the quadratic form `Q_v` given by `frameFunction_regular`
(M2), extended to all of `E3` by homogeneity (`homogExt_smul` and
`QuadraticMap.map_smul` on both sides).
-/
theorem homogExt_realSection (v : Fin 3 → H n) (hv : Orthonormal ℂ v) :
    ∃ Q : QuadraticForm ℝ E3, ∀ x : E3, homogExt g (realSection v x) = Q x := by
  obtain ⟨Q, hQ⟩ := exists_Qv hg hnn hn v hv
  refine ⟨Q, fun x => ?_⟩
  by_cases hx0 : x = 0
  · subst hx0; simp [homogExt, realSection, map_zero]
  have hxnorm : ‖x‖ ≠ 0 := norm_ne_zero_iff.mpr hx0
  have hunit : ‖(‖x‖⁻¹ : ℝ) • x‖ = 1 := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos (by positivity), inv_mul_cancel₀ hxnorm]
  have hcomp : realSection v x = (‖x‖ : ℂ) • realSection v ((‖x‖⁻¹ : ℝ) • x) := by
    unfold realSection
    rw [Finset.smul_sum]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    rw [smul_smul]
    congr 1
    simp only [PiLp.smul_apply, smul_eq_mul]
    push_cast
    field_simp [show (‖x‖ : ℂ) ≠ 0 from by exact_mod_cast hxnorm]
  have hunit' : ‖realSection v ((‖x‖⁻¹ : ℝ) • x)‖ = 1 := by
    rw [realSection_norm v hv]; exact hunit
  have hgoal : ‖x‖ ^ 2 * homogExt g (realSection v ((‖x‖⁻¹ : ℝ) • x)) = Q x := by
    rw [homogExt_of_unit hunit', hQ _ hunit, QuadraticMap.map_smul, smul_eq_mul]
    field_simp
  calc homogExt g (realSection v x)
      = homogExt g ((‖x‖ : ℂ) • realSection v ((‖x‖⁻¹ : ℝ) • x)) := by rw [hcomp]
    _ = ‖(‖x‖ : ℂ)‖ ^ 2 * homogExt g (realSection v ((‖x‖⁻¹ : ℝ) • x)) :=
        homogExt_smul hphase (‖x‖ : ℂ) (realSection v ((‖x‖⁻¹ : ℝ) • x))
    _ = ‖x‖ ^ 2 * homogExt g (realSection v ((‖x‖⁻¹ : ℝ) • x)) := by
        rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (norm_pos_iff.mpr hx0)]
    _ = Q x := hgoal

/- ═══════════════════════════════════════════════════════════════════
   M3-5. Continuité Lipschitz de `g` (via un ajustement de phase et la
   borne polaire de `Q_v`) puis existence d'un maximum sur toute
   sous-espace non nul (compacité).
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **M3-5(a).** Ajustement de phase : pour deux vecteurs unitaires `u, w`, il existe une
phase `c` (`‖c‖ = 1`) qui aligne `⟪u, c•w⟫` sur le réel positif `‖⟪u,w⟫‖`, et rapproche
`c•w` de `u` (au sens large) par rapport à `w`.

**EN.** **M3-5(a).** Phase adjustment: for two unit vectors `u, w`, there exists a
phase `c` (`‖c‖ = 1`) that aligns `⟪u, c•w⟫` with the nonnegative real number
`‖⟪u,w⟫‖`, and brings `c•w` (weakly) closer to `u` than `w` was.
-/
theorem exists_phase_adjust (u w : H n) (hu : ‖u‖ = 1) (hw : ‖w‖ = 1) :
    ∃ c : ℂ, ‖c‖ = 1 ∧ ⟪u, c • w⟫_ℂ = (‖⟪u, w⟫_ℂ‖ : ℂ) ∧ ‖u - c • w‖ ≤ ‖u - w‖ := by
  by_cases hz : ⟪u, w⟫_ℂ = 0
  · exact ⟨1, by norm_num, by rw [one_smul, hz]; simp, by rw [one_smul]⟩
  · set z : ℂ := ⟪u, w⟫_ℂ with hz_def
    set c : ℂ := (starRingEnd ℂ z) / (‖z‖ : ℂ) with hc_def
    have hznorm : ‖z‖ ≠ 0 := norm_ne_zero_iff.mpr hz
    have hznormC : (‖z‖ : ℂ) ≠ 0 := by exact_mod_cast hznorm
    have hnormz_castnorm : ‖(‖z‖ : ℂ)‖ = ‖z‖ := by simp
    have hre_castz : RCLike.re ((‖z‖ : ℝ) : ℂ) = ‖z‖ := by simp
    have hcnorm : ‖c‖ = 1 := by
      rw [hc_def, norm_div, RCLike.norm_conj, hnormz_castnorm, div_self hznorm]
    have hinner : ⟪u, c • w⟫_ℂ = (‖z‖ : ℂ) := by
      rw [inner_smul_right, hc_def, div_mul_eq_mul_div, RCLike.conj_mul, sq]
      field_simp
      norm_cast
    refine ⟨c, hcnorm, hinner, ?_⟩
    have hcw_norm : ‖c • w‖ = 1 := by rw [norm_smul, hcnorm, hw, one_mul]
    have h1 : ‖u - c • w‖ ^ 2 = 2 - 2 * ‖z‖ := by
      rw [norm_sub_sq (𝕜 := ℂ), hu, hcw_norm, hinner, hre_castz]; ring
    have h2 : ‖u - w‖ ^ 2 = 2 - 2 * RCLike.re (⟪u, w⟫_ℂ) := by
      rw [norm_sub_sq (𝕜 := ℂ), hu, hw]; ring
    have h3 : RCLike.re (⟪u, w⟫_ℂ) ≤ ‖z‖ := RCLike.re_le_norm z
    have h4 : ‖u - c • w‖ ^ 2 ≤ ‖u - w‖ ^ 2 := by rw [h1, h2]; linarith [h3]
    have h5 := Real.sqrt_le_sqrt h4
    rwa [Real.sqrt_sq (norm_nonneg _), Real.sqrt_sq (norm_nonneg _)] at h5

/--
**FR.** **M3-5(b).** Version COMPLEXE de `exists_unit_orthogonal_to_pair` (`Real3/SphereGeometry.lean`,
bloc A) : l'orthogonal (complexe) d'un span engendré par deux vecteurs, de dimension complexe
`≤ 2`, est non nul dès que `dim_ℂ (H n) ≥ 3`. C'est ICI, et seulement ici, que l'hypothèse
`n ≥ 3` intervient dans tout le bloc M3 : c'est le théorème qui remplace l'axiome analytique de
l'ancien développement (comptage de dimension complexe, pas de produit vectoriel en dimension
`n` quelconque).

**EN.** **M3-5(b).** COMPLEX version of `exists_unit_orthogonal_to_pair`
(`Real3/SphereGeometry.lean`, block A): the (complex) orthogonal complement of a span
generated by two vectors, of complex dimension `≤ 2`, is nonzero as soon as
`dim_ℂ (H n) ≥ 3`. This is HERE, and only here, that the hypothesis `n ≥ 3` enters
the whole M3 block: it is the theorem that replaces the analytic postulate of the
old development (complex dimension counting, no cross product in arbitrary
dimension `n`).
-/
theorem exists_unit_orthogonal_to_pair_complex (hn : 3 ≤ n) (a b : H n) :
    ∃ u : H n, ‖u‖ = 1 ∧ ⟪u, a⟫_ℂ = 0 ∧ ⟪u, b⟫_ℂ = 0 := by
  classical
  set K : Submodule ℂ (H n) := Submodule.span ℂ ({a, b} : Set (H n)) with hK_def
  have hKfin : Module.finrank ℂ K ≤ 2 := by
    refine le_trans (finrank_span_le_card ({a, b} : Set (H n))) ?_
    simp only [Set.toFinset_insert, Set.toFinset_singleton]
    exact (Finset.card_insert_le _ _).trans (by simp)
  have hHn : Module.finrank ℂ (H n) = n := by simp
  have hsum : Module.finrank ℂ K + Module.finrank ℂ Kᗮ = Module.finrank ℂ (H n) :=
    Submodule.finrank_add_finrank_orthogonal K
  have hKperp : 1 ≤ Module.finrank ℂ Kᗮ := by omega
  have hne : Kᗮ ≠ ⊥ := by
    intro h; rw [h, finrank_bot] at hKperp; omega
  obtain ⟨w, hwK, hw0⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hne
  have haK : a ∈ K := Submodule.subset_span (by simp)
  have hbK : b ∈ K := Submodule.subset_span (by simp)
  have hwa : ⟪w, a⟫_ℂ = 0 := Submodule.inner_left_of_mem_orthogonal haK hwK
  have hwb : ⟪w, b⟫_ℂ = 0 := Submodule.inner_left_of_mem_orthogonal hbK hwK
  have hwnorm : ‖w‖ ≠ 0 := norm_ne_zero_iff.mpr hw0
  have hwnormC : (‖w‖ : ℂ) ≠ 0 := by exact_mod_cast hwnorm
  refine ⟨(‖w‖⁻¹ : ℂ) • w, ?_, ?_, ?_⟩
  · rw [norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_norm,
      inv_mul_cancel₀ hwnorm]
  · rw [inner_smul_left, hwa, mul_zero]
  · rw [inner_smul_left, hwb, mul_zero]

/--
**FR.** **M3-5(c) (générique, réel).** Si `0 ≤ Q ≤ W‖·‖²` sur `E3`, la forme polaire de `Q` est
bornée : `|Q.polar a b| ≤ 2W‖a‖‖b‖`. Preuve : rééchelonnage `t := √(‖b‖/‖a‖)` dans
`0 ≤ Q(t•a ± t⁻¹•b) = t²Q(a) + t⁻²Q(b) ± Q.polar a b`, puis `Q(a) ≤ W‖a‖²` etc. et
`t²‖a‖² = t⁻²‖b‖² = ‖a‖‖b‖` par le choix de `t`.

**EN.** **M3-5(c) (generic, real).** If `0 ≤ Q ≤ W‖·‖²` on `E3`, the polar form of `Q`
is bounded: `|Q.polar a b| ≤ 2W‖a‖‖b‖`. Proof: rescaling `t := √(‖b‖/‖a‖)` in
`0 ≤ Q(t•a ± t⁻¹•b) = t²Q(a) + t⁻²Q(b) ± Q.polar a b`, then `Q(a) ≤ W‖a‖²` etc. and
`t²‖a‖² = t⁻²‖b‖² = ‖a‖‖b‖` by the choice of `t`.
-/
theorem quadratic_polar_bound {Q : QuadraticForm ℝ E3} {W : ℝ}
    (hQ_nonneg : ∀ x : E3, 0 ≤ Q x) (hQ_le : ∀ x : E3, Q x ≤ W * ‖x‖ ^ 2) (a b : E3) :
    |QuadraticMap.polar Q a b| ≤ 2 * W * ‖a‖ * ‖b‖ := by
  by_cases ha0 : a = 0
  · simp [ha0, QuadraticMap.polar]
  by_cases hb0 : b = 0
  · simp [hb0, QuadraticMap.polar]
  have hanorm : (0 : ℝ) < ‖a‖ := norm_pos_iff.mpr ha0
  have hbnorm : (0 : ℝ) < ‖b‖ := norm_pos_iff.mpr hb0
  have hWnonneg : 0 ≤ W := by
    by_contra hW
    exact absurd ((hQ_nonneg a).trans (hQ_le a))
      (not_le.mpr (mul_neg_of_neg_of_pos (not_le.mp hW) (by positivity)))
  set t : ℝ := Real.sqrt (‖b‖ / ‖a‖) with ht_def
  have ht_pos : 0 < t := Real.sqrt_pos.mpr (div_pos hbnorm hanorm)
  have ht_ne : t ≠ 0 := ht_pos.ne'
  have htsq : t ^ 2 = ‖b‖ / ‖a‖ := Real.sq_sqrt (by positivity)
  have hexpand_plus : Q (t • a + t⁻¹ • b)
      = t ^ 2 * Q a + t⁻¹ ^ 2 * Q b + QuadraticMap.polar Q a b := by
    have hpolar_eq : QuadraticMap.polar Q (t • a) (t⁻¹ • b) = QuadraticMap.polar Q a b := by
      rw [QuadraticMap.polar_smul_left, QuadraticMap.polar_smul_right, smul_smul,
        mul_inv_cancel₀ ht_ne, one_smul]
    have hQsum : Q (t • a + t⁻¹ • b)
        = Q (t • a) + Q (t⁻¹ • b) + QuadraticMap.polar Q (t • a) (t⁻¹ • b) := by
      rw [QuadraticMap.polar]; ring
    rw [hQsum, hpolar_eq, QuadraticMap.map_smul, QuadraticMap.map_smul, smul_eq_mul, smul_eq_mul]
    ring
  have hexpand_minus : Q (t • a - t⁻¹ • b)
      = t ^ 2 * Q a + t⁻¹ ^ 2 * Q b - QuadraticMap.polar Q a b := by
    have heq : t • a - t⁻¹ • b = t • a + (-1 : ℝ) • (t⁻¹ • b) := by
      rw [neg_one_smul]; abel
    have hpolar_eq : QuadraticMap.polar Q (t • a) ((-1 : ℝ) • (t⁻¹ • b))
        = -QuadraticMap.polar Q a b := by
      rw [QuadraticMap.polar_smul_right, QuadraticMap.polar_smul_left,
        QuadraticMap.polar_smul_right, smul_smul, smul_smul,
        show (-1 : ℝ) * t * t⁻¹ = -1 from by field_simp, neg_one_smul]
    have hQneg : Q ((-1 : ℝ) • (t⁻¹ • b)) = Q (t⁻¹ • b) := by
      rw [QuadraticMap.map_smul]; ring
    rw [heq]
    have hQsum : Q (t • a + (-1 : ℝ) • (t⁻¹ • b)) = Q (t • a) + Q ((-1 : ℝ) • (t⁻¹ • b)) +
        QuadraticMap.polar Q (t • a) ((-1 : ℝ) • (t⁻¹ • b)) := by
      rw [QuadraticMap.polar]; ring
    rw [hQsum, hpolar_eq, hQneg, QuadraticMap.map_smul, QuadraticMap.map_smul, smul_eq_mul,
      smul_eq_mul]
    ring
  have h1 : 0 ≤ t ^ 2 * Q a + t⁻¹ ^ 2 * Q b + QuadraticMap.polar Q a b := by
    rw [← hexpand_plus]; exact hQ_nonneg _
  have h2 : 0 ≤ t ^ 2 * Q a + t⁻¹ ^ 2 * Q b - QuadraticMap.polar Q a b := by
    rw [← hexpand_minus]; exact hQ_nonneg _
  have h3 : t ^ 2 * Q a + t⁻¹ ^ 2 * Q b ≤ t ^ 2 * (W * ‖a‖ ^ 2) + t⁻¹ ^ 2 * (W * ‖b‖ ^ 2) := by
    gcongr
    · exact hQ_le a
    · exact hQ_le b
  have hval : t ^ 2 * (W * ‖a‖ ^ 2) + t⁻¹ ^ 2 * (W * ‖b‖ ^ 2) = 2 * W * ‖a‖ * ‖b‖ := by
    rw [htsq, inv_pow, htsq]
    field_simp
    ring
  rw [abs_le]
  constructor <;> nlinarith [h1, h2, h3, hval]

/--
**FR.** **M3-5(c) (corollaire).** Si `0 ≤ Q ≤ W‖·‖²`, `Q` est `2W`-lipschitzienne sur la sphère
unité. Preuve : `Q.polar (a+b) (a-b) = 2(Q a - Q b)` (identités de polarisation), borné par
`2W‖a+b‖‖a-b‖ ≤ 4W‖a-b‖` via `quadratic_polar_bound` et `‖a+b‖ ≤ 2`.

**EN.** **M3-5(c) (corollary).** If `0 ≤ Q ≤ W‖·‖²`, `Q` is `2W`-Lipschitz on the unit
sphere. Proof: `Q.polar (a+b) (a-b) = 2(Q a - Q b)` (polarization identities),
bounded by `2W‖a+b‖‖a-b‖ ≤ 4W‖a-b‖` via `quadratic_polar_bound` and `‖a+b‖ ≤ 2`.
-/
theorem quadratic_lipschitz {Q : QuadraticForm ℝ E3} {W : ℝ}
    (hQ_nonneg : ∀ x : E3, 0 ≤ Q x) (hQ_le : ∀ x : E3, Q x ≤ W * ‖x‖ ^ 2)
    {a b : E3} (ha : ‖a‖ = 1) (hb : ‖b‖ = 1) :
    |Q a - Q b| ≤ 2 * W * ‖a - b‖ := by
  have hWnonneg : 0 ≤ W := by
    by_contra hW
    exact absurd ((hQ_nonneg a).trans (hQ_le a))
      (not_le.mpr (mul_neg_of_neg_of_pos (not_le.mp hW) (by rw [ha]; norm_num)))
  have hQa_neg : Q (-b) = Q b := by
    rw [show (-b : E3) = (-1 : ℝ) • b from (neg_one_smul ℝ b).symm, QuadraticMap.map_smul]; ring
  have hpolar_ab_neg : QuadraticMap.polar Q a (-b) = -QuadraticMap.polar Q a b := by
    rw [show (-b : E3) = (-1 : ℝ) • b from (neg_one_smul ℝ b).symm, QuadraticMap.polar_smul_right,
      neg_one_smul]
  have h1 : Q (a + b) = Q a + Q b + QuadraticMap.polar Q a b := by rw [QuadraticMap.polar]; ring
  have h2 : Q (a - b) = Q a + Q b - QuadraticMap.polar Q a b := by
    have heq : a - b = a + -b := by abel
    have h3 : Q (a + -b) = Q a + Q (-b) + QuadraticMap.polar Q a (-b) := by
      rw [QuadraticMap.polar]; ring
    rw [heq, h3, hQa_neg, hpolar_ab_neg]; ring
  have hpolar_sum : QuadraticMap.polar Q (a + b) (a - b)
      = Q ((a + b) + (a - b)) - Q (a + b) - Q (a - b) := by rw [QuadraticMap.polar]
  have hsum2a : (a + b) + (a - b) = (2 : ℝ) • a := by rw [two_smul]; abel
  have hQ2a : Q ((2 : ℝ) • a) = 4 * Q a := by rw [QuadraticMap.map_smul]; ring
  have hpolar_eq : QuadraticMap.polar Q (a + b) (a - b) = 2 * (Q a - Q b) := by
    rw [hpolar_sum, hsum2a, hQ2a, h1, h2]; ring
  have hbound := quadratic_polar_bound hQ_nonneg hQ_le (a + b) (a - b)
  rw [hpolar_eq, abs_mul] at hbound
  norm_num at hbound
  have hnormab : ‖a + b‖ ≤ 2 := by
    calc ‖a + b‖ ≤ ‖a‖ + ‖b‖ := norm_add_le a b
    _ = 2 := by rw [ha, hb]; norm_num
  nlinarith [hbound, hnormab, norm_nonneg (a - b), abs_nonneg (Q a - Q b),
    mul_le_mul_of_nonneg_right hnormab (mul_nonneg hWnonneg (norm_nonneg (a - b)))]

include hg hnn in
/--
**FR.** Le poids d'une frame function complexe positive est positif (somme de valeurs `≥ 0`
sur n'importe quelle base).

**EN.** The weight of a positive complex frame function is positive (sum of values
`≥ 0` over any basis).
-/
theorem cframe_weight_nonneg : 0 ≤ W := by
  have hsum := hg (EuclideanSpace.basisFun (Fin n) ℂ)
  rw [← hsum]
  exact Finset.sum_nonneg (fun i _ => hnn _ ((EuclideanSpace.basisFun (Fin n) ℂ).norm_eq_one i))

set_option maxHeartbeats 1000000 in
include hg hnn hphase hn in
/--
**FR.** **M3-5(d).** `g` est `2W`-lipschitzienne sur la sphère unité. Ajustement de phase
(`exists_phase_adjust`) pour se ramener à `⟪u,w'⟫` réel `≥ 0` ; cas d'égalité de
Cauchy-Schwarz si `‖⟪u,w'⟫‖ = 1` (alors `w' = u`) ; sinon Gram-Schmidt (`v`, unitaire,
`⟪u,v⟫ = 0`), complété par `z` (`exists_unit_orthogonal_to_pair_complex`, LE point d'entrée
de `n ≥ 3`) en triplet orthonormé `(u,v,z)` ; la section réelle associée envoie
`p := (1,0,0)` sur `u` et `q := (C,s,0)` sur `w'`, et `quadratic_lipschitz` conclut.

**EN.** **M3-5(d).** `g` is `2W`-Lipschitz on the unit sphere. Phase adjustment
(`exists_phase_adjust`) reduces to `⟪u,w'⟫` real `≥ 0`; equality case of
Cauchy-Schwarz if `‖⟪u,w'⟫‖ = 1` (then `w' = u`); otherwise Gram-Schmidt (`v`, unit
vector, `⟪u,v⟫ = 0`), completed by `z` (`exists_unit_orthogonal_to_pair_complex`,
THE entry point of `n ≥ 3`) into an orthonormal triple `(u,v,z)`; the associated real
section sends `p := (1,0,0)` to `u` and `q := (C,s,0)` to `w'`, and
`quadratic_lipschitz` concludes.
-/
theorem g_lipschitz (u w : H n) (hu : ‖u‖ = 1) (hw : ‖w‖ = 1) :
    |g u - g w| ≤ 2 * W * ‖u - w‖ := by
  obtain ⟨c₀, hc₀norm, hc₀inner, hc₀close⟩ := exists_phase_adjust u w hu hw
  set w' : H n := c₀ • w with hw'_def
  have hw'norm : ‖w'‖ = 1 := by rw [hw'_def, norm_smul, hc₀norm, hw, one_mul]
  have hgw' : g w' = g w := hphase c₀ w hc₀norm
  set C : ℝ := ‖⟪u, w⟫_ℂ‖ with hC_def
  have hCnonneg : 0 ≤ C := norm_nonneg _
  have hCle1 : C ≤ 1 := by
    calc C ≤ ‖u‖ * ‖w‖ := norm_inner_le_norm u w
    _ = 1 := by rw [hu, hw]; ring
  have hWnonneg : 0 ≤ W := cframe_weight_nonneg hg hnn
  suffices hsuff : |g u - g w'| ≤ 2 * W * ‖u - w'‖ by
    calc |g u - g w| = |g u - g w'| := by rw [hgw']
    _ ≤ 2 * W * ‖u - w'‖ := hsuff
    _ ≤ 2 * W * ‖u - w‖ := mul_le_mul_of_nonneg_left hc₀close (by positivity)
  by_cases hC1 : C = 1
  · have heq_inner : ⟪u, w'⟫_ℂ = (‖u‖ : ℂ) * (‖w'‖ : ℂ) := by
      rw [hc₀inner, hu, hw'norm, hC1]; norm_num
    have heq : (‖w'‖ : ℂ) • u = (‖u‖ : ℂ) • w' := inner_eq_norm_mul_iff.mp heq_inner
    rw [hu, hw'norm] at heq
    simp only [Complex.ofReal_one, one_smul] at heq
    rw [heq]; simp
  · have hCsq_lt : C ^ 2 < 1 := by nlinarith [lt_of_le_of_ne hCle1 hC1, hCnonneg]
    set s : ℝ := Real.sqrt (1 - C ^ 2) with hs_def
    have hs_pos : 0 < s := Real.sqrt_pos.mpr (by linarith [hCsq_lt])
    have hssq : s ^ 2 = 1 - C ^ 2 := Real.sq_sqrt (by linarith [hCsq_lt])
    have hCssq : C ^ 2 + s ^ 2 = 1 := by rw [hssq]; ring
    have hwu_inner : ⟪w', u⟫_ℂ = (C : ℂ) := by
      rw [(inner_conj_symm w' u).symm, hc₀inner, Complex.conj_ofReal]
    set d : H n := w' - (C : ℂ) • u with hd_def
    have huu : ⟪u, u⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hu]; norm_num
    have hud : ⟪u, d⟫_ℂ = 0 := by
      have hstep : ⟪u, d⟫_ℂ = ⟪u, w'⟫_ℂ - (C : ℂ) * ⟪u, u⟫_ℂ := by
        rw [hd_def, inner_sub_right]
        congr 1
        exact inner_smul_right u u (C : ℂ)
      rw [hstep, huu, mul_one, hc₀inner, sub_self]
    have hCu_inner : ⟪w', (C : ℂ) • u⟫_ℂ = ((C ^ 2 : ℝ) : ℂ) := by
      rw [inner_smul_right, hwu_inner]; push_cast; ring
    have hCu_norm : ‖(C : ℂ) • u‖ = C := by
      rw [norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg hCnonneg, hu, mul_one]
    have hre_Csq : RCLike.re (((C ^ 2 : ℝ)) : ℂ) = C ^ 2 := RCLike.ofReal_re _
    have hd2 : ‖d‖ ^ 2 = s ^ 2 := by
      rw [hd_def, norm_sub_sq (𝕜 := ℂ), hw'norm, hCu_inner, hre_Csq, hCu_norm, hssq]; ring
    have hdnorm : ‖d‖ = s := by
      have hh := Real.sqrt_sq (norm_nonneg d)
      rw [hd2, Real.sqrt_sq hs_pos.le] at hh
      exact hh.symm
    set v : H n := (s⁻¹ : ℂ) • d with hv_def
    have hvnorm : ‖v‖ = 1 := by
      rw [hv_def, norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hs_pos,
        hdnorm, inv_mul_cancel₀ hs_pos.ne']
    have huv : ⟪u, v⟫_ℂ = 0 := by rw [hv_def, inner_smul_right, hud, mul_zero]
    have hvu : ⟪v, u⟫_ℂ = 0 := by
      rw [(inner_conj_symm v u).symm, huv, map_zero]
    obtain ⟨z, hznorm, hzu, hzv⟩ := exists_unit_orthogonal_to_pair_complex hn u v
    have huz : ⟪u, z⟫_ℂ = 0 := by
      rw [(inner_conj_symm u z).symm, hzu, map_zero]
    have hvz : ⟪v, z⟫_ℂ = 0 := by
      rw [(inner_conj_symm v z).symm, hzv, map_zero]
    have hvv : ⟪v, v⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hvnorm]; norm_num
    have hzz : ⟪z, z⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hznorm]; norm_num
    set triple : Fin 3 → H n := ![u, v, z] with htriple_def
    have htriple_orth : Orthonormal ℂ triple := by
      rw [orthonormal_iff_ite]
      intro i j
      fin_cases i <;> fin_cases j <;>
        simp [htriple_def, hu, hvnorm, hznorm, huv, hvu, huz, hzu, hvz, hzv]
    obtain ⟨Q, hQ⟩ := homogExt_realSection hg hnn hphase hn triple htriple_orth
    set p : E3 := (!₂[1, 0, 0] : E3) with hp_def
    set q : E3 := (!₂[C, s, 0] : E3) with hq_def
    have hrsp : realSection triple p = u := by
      unfold realSection
      rw [Fin.sum_univ_three]
      simp [hp_def, htriple_def]
    have hrsq : realSection triple q = w' := by
      have hcomp : realSection triple q = (C : ℂ) • u + (s : ℂ) • v + (0 : ℂ) • z := by
        unfold realSection
        rw [Fin.sum_univ_three]
        simp [hq_def, htriple_def]
      rw [hcomp, zero_smul, add_zero, hv_def, hd_def, smul_smul,
        show (s : ℂ) * (s⁻¹ : ℂ) = 1 from by
          rw [← Complex.ofReal_inv, ← Complex.ofReal_mul, mul_inv_cancel₀ hs_pos.ne',
            Complex.ofReal_one],
        one_smul]
      abel
    have hgu_eq : g u = Q p := by
      have h1 : ‖realSection triple p‖ = 1 := by rw [hrsp]; exact hu
      rw [← hrsp, ← homogExt_of_unit (g := g) h1]
      exact hQ p
    have hgw'_eq : g w' = Q q := by
      have h1 : ‖realSection triple q‖ = 1 := by rw [hrsq]; exact hw'norm
      rw [← hrsq, ← homogExt_of_unit (g := g) h1]
      exact hQ q
    have hQ_nonneg : ∀ x : E3, 0 ≤ Q x := fun x => by rw [← hQ x]; exact homogExt_nonneg hnn _
    have hQ_le : ∀ x : E3, Q x ≤ W * ‖x‖ ^ 2 := fun x => by
      rw [← hQ x, ← realSection_norm triple htriple_orth x]
      exact homogExt_le hg hnn hn _
    have hpnorm : ‖p‖ = 1 := by
      rw [hp_def, EuclideanSpace.norm_eq]
      simp [Fin.sum_univ_three]
    have hqnorm : ‖q‖ = 1 := by
      have hqsq : ‖q‖ ^ 2 = C ^ 2 + s ^ 2 := by
        rw [hq_def, EuclideanSpace.norm_eq, Real.sq_sqrt (by positivity)]
        simp [Fin.sum_univ_three, sq_abs]
      rw [hCssq] at hqsq
      have hh := Real.sqrt_sq (norm_nonneg q)
      rw [hqsq] at hh
      rw [← hh]; norm_num
    have hlip := quadratic_lipschitz hQ_nonneg hQ_le hpnorm hqnorm
    rw [← hgu_eq, ← hgw'_eq] at hlip
    have hpq_eq : realSection triple (p - q) = u - w' := by
      have hlinear : realSection triple (p - q)
          = realSection triple p - realSection triple q := by
        unfold realSection
        rw [← Finset.sum_sub_distrib]
        refine Finset.sum_congr rfl (fun i _ => ?_)
        rw [← sub_smul]
        congr 1
        simp [PiLp.sub_apply]
      rw [hlinear, hrsp, hrsq]
    have hpq_norm : ‖p - q‖ = ‖u - w'‖ := by
      rw [← realSection_norm triple htriple_orth (p - q), hpq_eq]
    rwa [hpq_norm] at hlip

set_option maxHeartbeats 800000 in
include hg hnn hphase hn in
/--
**FR.** **M3-5(e).** `g` atteint son maximum sur la sphère unité de tout sous-espace `U ≠ ⊥`,
par compacité (sphère de `H n` compacte, `U` fermé car de dimension finie, donc `S := U ∩ sphère`
compact) et continuité (`g_lipschitz` donne la lipschitzianité de `g` sur `S`).

**EN.** **M3-5(e).** `g` attains its maximum on the unit sphere of any subspace
`U ≠ ⊥`, by compactness (the sphere of `H n` is compact, `U` is closed since
finite-dimensional, so `S := U ∩ sphere` is compact) and continuity (`g_lipschitz`
gives the Lipschitz property of `g` on `S`).
-/
theorem attains_max_on (U : Submodule ℂ (H n)) (hU : U ≠ ⊥) :
    ∃ x ∈ U, ‖x‖ = 1 ∧ ∀ w ∈ U, ‖w‖ = 1 → g w ≤ g x := by
  set S : Set (H n) := (U : Set (H n)) ∩ Metric.sphere (0 : H n) 1 with hS_def
  have hUclosed : IsClosed (U : Set (H n)) := Submodule.closed_of_finiteDimensional _
  have hScompact : IsCompact S := (isCompact_sphere (0 : H n) 1).inter_left hUclosed
  obtain ⟨x0, hx0U, hx0ne⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hU
  have hx0norm : ‖x0‖ ≠ 0 := norm_ne_zero_iff.mpr hx0ne
  set x1 : H n := ((‖x0‖ : ℝ)⁻¹ : ℂ) • x0 with hx1_def
  have hx1U : x1 ∈ U := U.smul_mem _ hx0U
  have hx1norm : ‖x1‖ = 1 := by
    rw [hx1_def, norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs,
      abs_of_nonneg (norm_nonneg x0), inv_mul_cancel₀ hx0norm]
  have hSne : S.Nonempty :=
    ⟨x1, hx1U, by rw [Metric.mem_sphere, dist_eq_norm, sub_zero, hx1norm]⟩
  have hLip : LipschitzOnWith (Real.toNNReal (2 * W)) g S :=
    LipschitzOnWith.of_dist_le' (fun a ha b hb => by
      have haS : ‖a‖ = 1 := by
        have h := ha.2; rwa [Metric.mem_sphere, dist_eq_norm, sub_zero] at h
      have hbS : ‖b‖ = 1 := by
        have h := hb.2; rwa [Metric.mem_sphere, dist_eq_norm, sub_zero] at h
      rw [Real.dist_eq, dist_eq_norm]
      exact g_lipschitz hg hnn hphase hn a b haS hbS)
  obtain ⟨x, hxS, hxmax⟩ := hScompact.exists_isMaxOn hSne hLip.continuousOn
  refine ⟨x, hxS.1, ?_, fun w hwU hwnorm => isMaxOn_iff.mp hxmax w ⟨hwU, ?_⟩⟩
  · have h := hxS.2; rwa [Metric.mem_sphere, dist_eq_norm, sub_zero] at h
  · rw [Metric.mem_sphere, dist_eq_norm, sub_zero, hwnorm]

/- ═══════════════════════════════════════════════════════════════════
   M3-6. Identité d'épluchage (CKM / Dvurečenskij, cœur de la récurrence
   d'assemblage). Si `x` maximise `g` sur la sphère unité du plan complexe
   engendré par `x` et `y`, la valeur de l'extension homogène `q := homogExt g`
   en `y` se décompose selon la projection orthogonale sur `x`.
   ═══════════════════════════════════════════════════════════════════ -/

set_option maxHeartbeats 1600000 in
include hg hnn hphase hn in
theorem peel (x y : H n) (hx : ‖x‖ = 1) (hy : ‖y‖ = 1)
    (hmax : ∀ w ∈ Submodule.span ℂ ({x, y} : Set (H n)), ‖w‖ = 1 → g w ≤ g x) :
    homogExt g y = g x * ‖⟪x, y⟫_ℂ‖ ^ 2 + homogExt g (y - ⟪x, y⟫_ℂ • x) := by
  have hxx : ⟪x, x⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hx]; norm_num
  by_cases hcol : ‖⟪x, y⟫_ℂ‖ = 1
  · -- Cas colinéaire : égalité de Cauchy-Schwarz, y = r • x pour un r unitaire.
    have hx0 : x ≠ 0 := by intro h; rw [h, norm_zero] at hx; norm_num at hx
    have hy0 : y ≠ 0 := by intro h; rw [h, norm_zero] at hy; norm_num at hy
    obtain ⟨r, -, hyr⟩ := (norm_inner_eq_norm_iff hx0 hy0).mp (by rw [hcol, hx, hy]; ring)
    have hrnorm : ‖r‖ = 1 := by
      have h := hy; rw [hyr, norm_smul, hx, mul_one] at h; exact h
    have hzero : y - ⟪x, y⟫_ℂ • x = 0 := by
      rw [hyr, inner_smul_right, hxx, mul_one, sub_self]
    rw [hzero, hcol, homogExt_of_unit hy, hyr, hphase r x hrnorm]
    simp [homogExt]
  · -- Cas général : Gram-Schmidt (x, v, z), tueur de terme croisé, décomposition quadratique.
    set α : ℝ := ‖⟪x, y⟫_ℂ‖ with hα_def
    have hα_nonneg : 0 ≤ α := norm_nonneg _
    have hα_le1 : α ≤ 1 := by
      calc α ≤ ‖x‖ * ‖y‖ := norm_inner_le_norm x y
      _ = 1 := by rw [hx, hy]; ring
    have hα_lt1 : α < 1 := lt_of_le_of_ne hα_le1 hcol
    obtain ⟨c', hc'norm, hc'inner, -⟩ := exists_phase_adjust x y hx hy
    set w : H n := c' • y with hw_def
    have hwnorm : ‖w‖ = 1 := by rw [hw_def, norm_smul, hc'norm, hy, one_mul]
    have hxw_inner : ⟪x, w⟫_ℂ = (α : ℂ) := hc'inner
    have hy_eq : (starRingEnd ℂ c') • w = y := by
      rw [hw_def, smul_smul, RCLike.conj_mul, hc'norm]; simp
    have hxy_val : ⟪x, y⟫_ℂ = starRingEnd ℂ c' * (α : ℂ) := by
      rw [← hy_eq, inner_smul_right, hxw_inner]
    have hg_wy : g w = g y := by rw [hw_def]; exact hphase c' y hc'norm
    have hden1 : (0 : ℝ) < 1 - α := by linarith
    have hden2 : (0 : ℝ) < 1 + α := by linarith
    have hsq_pos : 0 < 1 - α ^ 2 := by nlinarith [mul_pos hden1 hden2]
    set s : ℝ := Real.sqrt (1 - α ^ 2) with hs_def
    have hs_pos : 0 < s := Real.sqrt_pos.mpr hsq_pos
    have hssq : s ^ 2 = 1 - α ^ 2 := Real.sq_sqrt hsq_pos.le
    set d : H n := w - (α : ℂ) • x with hd_def
    have hxd_inner : ⟪x, d⟫_ℂ = 0 := by
      have hstep : ⟪x, d⟫_ℂ = ⟪x, w⟫_ℂ - (α : ℂ) * ⟪x, x⟫_ℂ := by
        rw [hd_def, inner_sub_right]; congr 1; exact inner_smul_right x x (α : ℂ)
      rw [hstep, hxx, mul_one, hxw_inner, sub_self]
    have hwx_inner : ⟪w, x⟫_ℂ = (α : ℂ) := by
      rw [(inner_conj_symm w x).symm, hxw_inner, Complex.conj_ofReal]
    have hαx_inner : ⟪w, (α : ℂ) • x⟫_ℂ = ((α ^ 2 : ℝ) : ℂ) := by
      rw [inner_smul_right, hwx_inner]; push_cast; ring
    have hαx_norm : ‖(α : ℂ) • x‖ = α := by
      rw [norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg hα_nonneg, hx, mul_one]
    have hre_ααsq : RCLike.re (((α ^ 2 : ℝ)) : ℂ) = α ^ 2 := RCLike.ofReal_re _
    have hd2 : ‖d‖ ^ 2 = s ^ 2 := by
      rw [hd_def, norm_sub_sq (𝕜 := ℂ), hwnorm, hαx_inner, hre_ααsq, hαx_norm, hssq]; ring
    have hdnorm : ‖d‖ = s := by
      have hh := Real.sqrt_sq (norm_nonneg d)
      rw [hd2, Real.sqrt_sq hs_pos.le] at hh
      exact hh.symm
    set v : H n := (s⁻¹ : ℂ) • d with hv_def
    have hvnorm : ‖v‖ = 1 := by
      rw [hv_def, norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hs_pos,
        hdnorm, inv_mul_cancel₀ hs_pos.ne']
    have hxv_inner : ⟪x, v⟫_ℂ = 0 := by rw [hv_def, inner_smul_right, hxd_inner, mul_zero]
    have hvx_inner : ⟪v, x⟫_ℂ = 0 := by
      rw [(inner_conj_symm v x).symm, hxv_inner, map_zero]
    have hd_eq_v : d = (s : ℂ) • v := by
      rw [hv_def, smul_smul, ← Complex.ofReal_inv, ← Complex.ofReal_mul, mul_inv_cancel₀ hs_pos.ne',
        Complex.ofReal_one, one_smul]
    obtain ⟨z, hznorm, hzx, hzv⟩ := exists_unit_orthogonal_to_pair_complex hn x v
    have hxz_inner : ⟪x, z⟫_ℂ = 0 := by
      rw [(inner_conj_symm x z).symm, hzx, map_zero]
    have hvz_inner : ⟪v, z⟫_ℂ = 0 := by
      rw [(inner_conj_symm v z).symm, hzv, map_zero]
    have hvv1 : ⟪v, v⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hvnorm]; norm_num
    have hzz1 : ⟪z, z⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hznorm]; norm_num
    set triple : Fin 3 → H n := ![x, v, z] with htriple_def
    have htriple_orth : Orthonormal ℂ triple := by
      rw [orthonormal_iff_ite]
      intro i j
      fin_cases i <;> fin_cases j <;>
        simp [htriple_def, hx, hvnorm, hznorm, hxv_inner, hvx_inner, hxz_inner, hzx, hvz_inner,
          hzv]
    obtain ⟨Q, hQ⟩ := homogExt_realSection hg hnn hphase hn triple htriple_orth
    set e1 : E3 := (!₂[1, 0, 0] : E3) with he1_def
    set e2 : E3 := (!₂[0, 1, 0] : E3) with he2_def
    have he1x : realSection triple e1 = x := by
      unfold realSection; rw [Fin.sum_univ_three]; simp [he1_def, htriple_def]
    have he2v : realSection triple e2 = v := by
      unfold realSection; rw [Fin.sum_univ_three]; simp [he2_def, htriple_def]
    have hQe1 : Q e1 = g x := by rw [← hQ e1, he1x, homogExt_of_unit hx]
    have hQe2 : Q e2 = g v := by rw [← hQ e2, he2v, homogExt_of_unit hvnorm]
    have hv_mem : v ∈ Submodule.span ℂ ({x, y} : Set (H n)) := by
      have hw_mem : w ∈ Submodule.span ℂ ({x, y} : Set (H n)) :=
        hw_def ▸ Submodule.smul_mem _ _ (Submodule.subset_span (by simp))
      have hd_mem : d ∈ Submodule.span ℂ ({x, y} : Set (H n)) :=
        hd_def ▸ Submodule.sub_mem _ hw_mem
          (Submodule.smul_mem _ _ (Submodule.subset_span (by simp)))
      exact hv_def ▸ Submodule.smul_mem _ _ hd_mem
    have hgv_le : g v ≤ g x := hmax v hv_mem hvnorm
    have hK_nonneg : 0 ≤ g x - g v := by linarith
    have hcomb_norm : ∀ ε : ℝ, ‖e1 + ε • e2‖ ^ 2 = 1 + ε ^ 2 := by
      intro ε
      rw [EuclideanSpace.norm_eq, Real.sq_sqrt (by positivity)]
      simp [he1_def, he2_def, Fin.sum_univ_three, sq_abs]
    have hQexpand : ∀ ε : ℝ,
        Q (e1 + ε • e2) = Q e1 + ε ^ 2 * Q e2 + ε * QuadraticMap.polar Q e1 e2 := by
      intro ε
      have h1 := QuadraticMap.map_add Q e1 (ε • e2)
      simp only [QuadraticMap.map_smul, QuadraticMap.polar_smul_right, smul_eq_mul] at h1
      nlinarith [h1]
    have hQ_bound : ∀ ε : ℝ, Q (e1 + ε • e2) ≤ g x * (1 + ε ^ 2) := by
      intro ε
      set nrm : ℝ := ‖e1 + ε • e2‖ with hnrm_def
      have hnrm_sq : nrm ^ 2 = 1 + ε ^ 2 := hcomb_norm ε
      have hnrm_pos : 0 < nrm := by
        have hpos : (0 : ℝ) < 1 + ε ^ 2 := by positivity
        nlinarith [sq_nonneg (nrm - 1), norm_nonneg (e1 + ε • e2), hnrm_sq]
      set nε : E3 := (nrm⁻¹ : ℝ) • (e1 + ε • e2) with hnε_def
      have hnε_norm : ‖nε‖ = 1 := by
        rw [hnε_def, norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos hnrm_pos,
          inv_mul_cancel₀ hnrm_pos.ne']
      have hQnε : Q nε = (nrm ^ 2)⁻¹ * Q (e1 + ε • e2) := by
        rw [hnε_def, QuadraticMap.map_smul, smul_eq_mul]; ring
      have hrsnε_norm : ‖realSection triple nε‖ = 1 := by
        rw [realSection_norm triple htriple_orth]; exact hnε_norm
      have hcomp : realSection triple (e1 + ε • e2) = (1 : ℂ) • x + (ε : ℂ) • v + (0 : ℂ) • z := by
        unfold realSection
        rw [Fin.sum_univ_three]
        simp [he1_def, he2_def, htriple_def]
      have hsmul_comp : realSection triple nε = (nrm⁻¹ : ℂ) • realSection triple (e1 + ε • e2) := by
        rw [hnε_def]
        unfold realSection
        rw [Finset.smul_sum]
        refine Finset.sum_congr rfl (fun i _ => ?_)
        rw [smul_smul]; congr 1
        simp only [PiLp.smul_apply, smul_eq_mul]
        push_cast; ring
      have hrsnε_mem : realSection triple nε ∈ Submodule.span ℂ ({x, y} : Set (H n)) := by
        rw [hsmul_comp, hcomp, one_smul, zero_smul, add_zero]
        exact Submodule.smul_mem _ _ (Submodule.add_mem _ (Submodule.subset_span (by simp))
          (Submodule.smul_mem _ _ hv_mem))
      have hglenε : g (realSection triple nε) ≤ g x := hmax _ hrsnε_mem hrsnε_norm
      have hQeq : Q nε = g (realSection triple nε) := by
        rw [← hQ nε, homogExt_of_unit hrsnε_norm]
      rw [hQeq] at hQnε
      have hle : (nrm ^ 2)⁻¹ * Q (e1 + ε • e2) ≤ g x := by rw [← hQnε]; exact hglenε
      rw [hnrm_sq] at hle
      have hpos : (0 : ℝ) < 1 + ε ^ 2 := by positivity
      have := mul_le_mul_of_nonneg_left hle hpos.le
      rwa [← mul_assoc, mul_inv_cancel₀ hpos.ne', one_mul, mul_comm (1 + ε ^ 2) (g x)] at this
    have hbound : ∀ ε : ℝ, ε * QuadraticMap.polar Q e1 e2 ≤ ε ^ 2 * (g x - g v) := by
      intro ε
      have h1 := hQ_bound ε
      rw [hQexpand ε, hQe1, hQe2] at h1
      nlinarith [h1]
    have hB_zero : QuadraticMap.polar Q e1 e2 = 0 := by
      by_contra hBne
      set K : ℝ := g x - g v with hK_def2
      set ε0 : ℝ := QuadraticMap.polar Q e1 e2 / (K + 1) with hε0_def
      have hden_pos : 0 < K + 1 := by linarith
      have hidentity : ε0 * QuadraticMap.polar Q e1 e2 - ε0 ^ 2 * K
          = (QuadraticMap.polar Q e1 e2) ^ 2 / (K + 1) ^ 2 := by
        rw [hε0_def]; field_simp; ring
      have hpos : 0 < (QuadraticMap.polar Q e1 e2) ^ 2 / (K + 1) ^ 2 := by positivity
      have h := hbound ε0
      linarith [hidentity, hpos, h]
    have hQ_ab : ∀ a b : ℝ, Q (a • e1 + b • e2) = a ^ 2 * g x + b ^ 2 * g v := by
      intro a b
      have h1 := QuadraticMap.map_add Q (a • e1) (b • e2)
      simp only [QuadraticMap.map_smul, QuadraticMap.polar_smul_left,
        QuadraticMap.polar_smul_right, hB_zero, smul_eq_mul, hQe1, hQe2] at h1
      nlinarith [h1]
    have hy_sub : y - ⟪x, y⟫_ℂ • x = (starRingEnd ℂ c' * (s : ℂ)) • v := by
      rw [hxy_val, ← hy_eq, mul_smul, ← smul_sub, ← hd_def, hd_eq_v, ← smul_smul]
    have hscalar_norm : ‖starRingEnd ℂ c' * (s : ℂ)‖ = s := by
      rw [norm_mul, RCLike.norm_conj, hc'norm, one_mul, Complex.norm_real, Real.norm_eq_abs,
        abs_of_pos hs_pos]
    have hq_sub : homogExt g (y - ⟪x, y⟫_ℂ • x) = s ^ 2 * g v := by
      rw [hy_sub, homogExt_smul hphase, hscalar_norm, homogExt_of_unit hvnorm]
    have hgy_eq : g y = α ^ 2 * g x + s ^ 2 * g v := by
      have hcombQ := hQ_ab α s
      have hrs_eq : realSection triple (α • e1 + s • e2) = w := by
        have hcomp2 : realSection triple (α • e1 + s • e2)
            = (α : ℂ) • x + (s : ℂ) • v + (0 : ℂ) • z := by
          unfold realSection
          rw [Fin.sum_univ_three]
          simp [he1_def, he2_def, htriple_def]
        rw [hcomp2, zero_smul, add_zero, ← hd_eq_v, hd_def]
        abel
      have hQw : Q (α • e1 + s • e2) = g w := by
        rw [← hQ (α • e1 + s • e2), hrs_eq, homogExt_of_unit hwnorm]
      rw [hQw, hg_wy] at hcombQ
      exact hcombQ
    rw [homogExt_of_unit hy, hq_sub, hgy_eq]
    ring

include hg hnn hphase hn in
/--
**FR.** **M3-6 (forme homogène).** Version de `peel` sans hypothèse de norme unité sur `w`,
obtenue par transport d'homogénéité (`homogExt_smul`) : c'est cette forme qui sera utilisée
dans l'induction M3-8.

**EN.** **M3-6 (homogeneous form).** Version of `peel` without the unit-norm
hypothesis on `w`, obtained by transport of homogeneity (`homogExt_smul`): this is
the form that will be used in the M3-8 induction.
-/
theorem homogExt_peel (x w : H n) (hx : ‖x‖ = 1)
    (hmax : ∀ v ∈ Submodule.span ℂ ({x, w} : Set (H n)), ‖v‖ = 1 → g v ≤ g x) :
    homogExt g w = g x * ‖⟪x, w⟫_ℂ‖ ^ 2 + homogExt g (w - ⟪x, w⟫_ℂ • x) := by
  by_cases hw0 : w = 0
  · subst hw0; simp [homogExt]
  have hwnorm0 : ‖w‖ ≠ 0 := norm_ne_zero_iff.mpr hw0
  have hwnorm_pos : (0 : ℝ) < ‖w‖ := norm_pos_iff.mpr hw0
  set w1 : H n := (‖w‖⁻¹ : ℂ) • w with hw1_def
  have hw1norm : ‖w1‖ = 1 := by
    rw [hw1_def, norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_norm,
      inv_mul_cancel₀ hwnorm0]
  have hw_eq : w = (‖w‖ : ℂ) • w1 := by
    rw [hw1_def, smul_smul, ← Complex.ofReal_inv, ← Complex.ofReal_mul,
      mul_inv_cancel₀ hwnorm0, Complex.ofReal_one, one_smul]
  have hmax' : ∀ v ∈ Submodule.span ℂ ({x, w1} : Set (H n)), ‖v‖ = 1 → g v ≤ g x := by
    have hspan_eq :
        Submodule.span ℂ ({x, w1} : Set (H n)) = Submodule.span ℂ ({x, w} : Set (H n)) := by
      apply le_antisymm
      · rw [Submodule.span_le, Set.insert_subset_iff, Set.singleton_subset_iff]
        exact ⟨Submodule.subset_span (by simp),
          hw1_def ▸ Submodule.smul_mem _ _ (Submodule.subset_span (by simp))⟩
      · rw [Submodule.span_le, Set.insert_subset_iff, Set.singleton_subset_iff]
        exact ⟨Submodule.subset_span (by simp),
          hw_eq ▸ Submodule.smul_mem _ _ (Submodule.subset_span (by simp))⟩
    rw [hspan_eq]; exact hmax
  have hpeel := peel hg hnn hphase hn x w1 hx hw1norm hmax'
  have hxw1 : ⟪x, w1⟫_ℂ = (‖w‖⁻¹ : ℂ) * ⟪x, w⟫_ℂ := by rw [hw1_def, inner_smul_right]
  have hnorm_xw1 : ‖⟪x, w1⟫_ℂ‖ = ‖w‖⁻¹ * ‖⟪x, w⟫_ℂ‖ := by
    rw [hxw1, norm_mul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hwnorm_pos]
  have hsub_eq : w1 - ⟪x, w1⟫_ℂ • x = (‖w‖⁻¹ : ℂ) • (w - ⟪x, w⟫_ℂ • x) := by
    rw [hxw1, hw1_def, smul_sub, smul_smul, mul_comm]
  have hA : homogExt g w = ‖w‖ ^ 2 * homogExt g w1 := by
    conv_lhs => rw [hw_eq]
    rw [homogExt_smul hphase, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hwnorm_pos]
  have hB : homogExt g (w1 - ⟪x, w1⟫_ℂ • x)
      = ‖w‖⁻¹ ^ 2 * homogExt g (w - ⟪x, w⟫_ℂ • x) := by
    conv_lhs => rw [hsub_eq]
    rw [homogExt_smul hphase, norm_inv, Complex.norm_real, Real.norm_eq_abs,
      abs_of_pos hwnorm_pos]
  rw [hB, hnorm_xw1] at hpeel
  rw [hA, hpeel]
  field_simp

/- ═══════════════════════════════════════════════════════════════════
   M3-8. Induction d'épluchage : construction de ρ, symétrique, nul hors
   de `U`, représentant `q := homogExt g` sur `U`, par récurrence sur
   `finrank ℂ U`. Réutilise la construction rang-un de Busch (M-B, B8) :
   `InnerProductSpace.rankOne`.
   ═══════════════════════════════════════════════════════════════════ -/

include hg hnn hphase hn in
theorem exists_symmetric_rep_of_finrank :
    ∀ k : ℕ, ∀ U : Submodule ℂ (H n), Module.finrank ℂ U = k →
    ∃ ρ : H n →ₗ[ℂ] H n, LinearMap.IsSymmetric ρ ∧
      (∀ z : H n, (∀ u ∈ U, ⟪u, z⟫_ℂ = 0) → ρ z = 0) ∧
      (∀ w ∈ U, ⟪w, ρ w⟫_ℂ = (homogExt g w : ℂ)) := by
  intro k
  induction k with
  | zero =>
    intro U hU
    refine ⟨0, fun _ _ => by simp, fun z _ => by simp, fun w hw => ?_⟩
    have hUbot : U = ⊥ := Submodule.finrank_eq_zero.mp hU
    rw [hUbot, Submodule.mem_bot] at hw
    subst hw
    simp [homogExt]
  | succ k ih =>
    intro U hU
    have hUne : U ≠ ⊥ := by intro h; rw [h, finrank_bot] at hU; omega
    obtain ⟨x, hxU, hxnorm, hxmax⟩ := attains_max_on hg hnn hphase hn U hUne
    set U' : Submodule ℂ (H n) := U ⊓ (Submodule.span ℂ ({x} : Set (H n)))ᗮ with hU'_def
    have hU'fin : Module.finrank ℂ U' = k := by
      have h := finrank_inf_orthogonal_add_one hxU hxnorm
      rw [← hU'_def] at h
      omega
    obtain ⟨ρ', hρ'_sym, hρ'_zero, hρ'_val⟩ := ih U' hU'fin
    have hro_sym : (InnerProductSpace.rankOne ℂ x x : H n →L[ℂ] H n).toLinearMap.IsSymmetric := by
      intro a b
      simp only [ContinuousLinearMap.coe_coe, InnerProductSpace.rankOne_apply, inner_smul_left,
        inner_smul_right, inner_conj_symm]
      ring
    set ρ : H n →ₗ[ℂ] H n :=
      (g x : ℂ) • (InnerProductSpace.rankOne ℂ x x : H n →L[ℂ] H n).toLinearMap + ρ'
      with hρ_def
    have hρ_sym : ρ.IsSymmetric := by
      rw [hρ_def]; exact (hro_sym.smul (Complex.conj_ofReal (g x))).add hρ'_sym
    refine ⟨ρ, hρ_sym, ?_, ?_⟩
    · intro z hz
      have hxz : ⟪x, z⟫_ℂ = 0 := hz x hxU
      have hrx : (InnerProductSpace.rankOne ℂ x x : H n →L[ℂ] H n).toLinearMap z = 0 := by
        simp [InnerProductSpace.rankOne_apply, hxz]
      have hρ'z : ρ' z = 0 := hρ'_zero z (fun u hu => hz u (Submodule.mem_inf.mp hu).1)
      rw [hρ_def]
      simp [hrx, hρ'z]
    · intro w hwU
      have hspan_le : Submodule.span ℂ ({x, w} : Set (H n)) ≤ U := span_pair_le_of_mem hxU hwU
      have hmaxw : ∀ v ∈ Submodule.span ℂ ({x, w} : Set (H n)), ‖v‖ = 1 → g v ≤ g x :=
        fun v hv hvnorm => hxmax v (hspan_le hv) hvnorm
      have hpeel := homogExt_peel hg hnn hphase hn x w hxnorm hmaxw
      set Pw : H n := w - ⟪x, w⟫_ℂ • x with hPw_def
      have hPwU' : Pw ∈ U' := sub_proj_mem_inf_orthogonal hxU hxnorm hwU
      have hPw_val : ⟪Pw, ρ' Pw⟫_ℂ = (homogExt g Pw : ℂ) := hρ'_val Pw hPwU'
      have hw_decomp : w = ⟪x, w⟫_ℂ • x + Pw := by rw [hPw_def]; abel
      have hρx0 : ρ' x = 0 := hρ'_zero x (fun u hu =>
        Submodule.mem_orthogonal_singleton_iff_inner_left.mp (Submodule.mem_inf.mp hu).2)
      have hρ'w_eq : ρ' w = ρ' Pw := by
        conv_lhs => rw [hw_decomp]
        rw [map_add, map_smul, hρx0, smul_zero, zero_add]
      have hρw_apply : ρ w = (g x : ℂ) • (⟪x, w⟫_ℂ • x) + ρ' Pw := by
        rw [hρ_def]
        simp only [LinearMap.add_apply, LinearMap.smul_apply, ContinuousLinearMap.coe_coe,
          InnerProductSpace.rankOne_apply]
        rw [hρ'w_eq]
      have hxw_mul_conj : ⟪x, w⟫_ℂ * starRingEnd ℂ ⟪x, w⟫_ℂ = ((‖⟪x, w⟫_ℂ‖ ^ 2 : ℝ) : ℂ) := by
        rw [mul_comm, RCLike.conj_mul]; norm_cast
      have hterm1 : ⟪w, (g x : ℂ) • (⟪x, w⟫_ℂ • x)⟫_ℂ
          = ((‖⟪x, w⟫_ℂ‖ ^ 2 : ℝ) : ℂ) * (g x : ℂ) := by
        rw [inner_smul_right, inner_smul_right, (inner_conj_symm w x).symm, hxw_mul_conj]
        ring
      have hinner_final : ⟪w, ρ w⟫_ℂ
          = ((‖⟪x, w⟫_ℂ‖ ^ 2 : ℝ) : ℂ) * (g x : ℂ) + ⟪w, ρ' Pw⟫_ℂ := by
        rw [hρw_apply, inner_add_right, hterm1]
      have hcross : ⟪x, ρ' Pw⟫_ℂ = 0 := by
        rw [← hρ'_sym x Pw, hρx0, inner_zero_left]
      have hinner2 : ⟪w, ρ' Pw⟫_ℂ = (homogExt g Pw : ℂ) := by
        rw [hw_decomp, inner_add_left, inner_smul_left, hcross, mul_zero, zero_add]
        exact hPw_val
      have hpeelC : (homogExt g w : ℂ)
          = (g x : ℂ) * ((‖⟪x, w⟫_ℂ‖ ^ 2 : ℝ) : ℂ) + (homogExt g Pw : ℂ) := by
        exact_mod_cast hpeel
      rw [hinner_final, hinner2, hpeelC]
      ring

end CFrameSections

end
end Gleason
