import Gleason.Operator
import Gleason.Nonvacuity
import Gleason.Busch.Main

/-!
**FR.** # Théorème de Gleason — assemblage final

`gleason` assemble : mesure → frame function complexe (`RealSections`) → régularité
complexe (`Patching`, qui repose sur `Real3/Regular`) → opérateur densité et formule
de Born (`Operator`). L'unicité vient de `symmetric_ext_of_quadratic`.

Garde de qualité : à la fin du projet, `#print axioms Gleason.gleason` ne doit
afficher QUE `propext`, `Classical.choice`, `Quot.sound` (et rien d'autre —
en particulier pas `sorryAx`).

**EN.** # Gleason's theorem — final assembly

`gleason` assembles: measure → complex frame function (`RealSections`) → complex
regularity (`Patching`, which rests on `Real3/Regular`) → density operator and the
Born formula (`Operator`). Uniqueness comes from `symmetric_ext_of_quadratic`.

Quality guard: at the end of the project, `#print axioms Gleason.gleason` must show
ONLY `propext`, `Classical.choice`, `Quot.sound` (and nothing else — in particular
no `sorryAx`).
-/

namespace Gleason

open scoped InnerProductSpace

noncomputable section

/--
**FR.** **Théorème de Gleason (projections, dimension finie ≥ 3).**
Toute mesure de probabilité finiment additive sur les sous-espaces de ℂⁿ, `n ≥ 3`,
est représentée par un unique opérateur densité via la règle de Born.

**EN.** **Gleason's theorem (projections, finite dimension ≥ 3).**
Every finitely additive probability measure on the subspaces of ℂⁿ, `n ≥ 3`, is
represented by a unique density operator via the Born rule.
-/
theorem gleason {n : ℕ} (hn : 3 ≤ n) (m : ProjMeasure n) :
    ∃! ρ : H n →ₗ[ℂ] H n, IsDensityOperator ρ ∧
      ∀ A : Submodule ℂ (H n), m.μ A = bornValue ρ A := by
  have hg_frame : IsCFrameFunction m.frameFunction 1 := m.isCFrameFunction
  have hg_nn : ∀ x : H n, ‖x‖ = 1 → 0 ≤ m.frameFunction x := fun x _ => m.nonneg _
  have hg_phase : ∀ (c : ℂ) (x : H n), ‖c‖ = 1 → m.frameFunction (c • x) = m.frameFunction x :=
    m.frameFunction_phase
  obtain ⟨ρ, hρ_sym, hρ_rep⟩ := cFrameFunction_regular hn m.frameFunction 1 hg_frame hg_nn hg_phase
  have hρ_density : IsDensityOperator ρ := isDensityOperator_of_represents m ρ hρ_sym hρ_rep
  have hρ_born : ∀ A : Submodule ℂ (H n), m.μ A = bornValue ρ A :=
    born_of_quadratic m ρ hρ_sym hρ_rep
  refine ⟨ρ, ⟨hρ_density, hρ_born⟩, ?_⟩
  rintro ρ' ⟨hρ'_density, hρ'_born⟩
  apply symmetric_ext_of_quadratic hρ'_density.symmetric hρ_sym
  intro x hx
  rw [← bornValue_span_singleton ρ' x hx, ← hρ'_born (ℂ ∙ x), hρ_born (ℂ ∙ x),
    bornValue_span_singleton ρ x hx]

/--
**FR.** **Test d'intégration** (corollaire classique) : pas de mesure dispersion-free
(à valeurs dans {0,1}) en dimension ≥ 3. Si `gleason` était vacuement vrai ou mal
énoncé, ce corollaire ne sortirait pas — c'est le détecteur anti-vacuité final.

**EN.** **Integration test** (classical corollary): no dispersion-free measure
(valued in {0,1}) exists in dimension ≥ 3. If `gleason` were vacuously true or
misstated, this corollary would not follow — it is the final anti-vacuity
detector.
-/
theorem no_dispersion_free {n : ℕ} (hn : 3 ≤ n) (m : ProjMeasure n) :
    ¬ (∀ A : Submodule ℂ (H n), m.μ A = 0 ∨ m.μ A = 1) := by
  intro h
  obtain ⟨ρ, ⟨hρ_density, hρ_born⟩, -⟩ := gleason hn m
  -- (a) Il existe une droite de mesure 1 (sinon la somme sur une base orthonormée est 0).
  have hexists : ∃ x : H n, ‖x‖ = 1 ∧ m.μ (ℂ ∙ x) = 1 := by
    by_contra hcon
    push Not at hcon
    have hall_zero : ∀ x : H n, ‖x‖ = 1 → m.μ (ℂ ∙ x) = 0 := by
      intro x hx
      rcases h (ℂ ∙ x) with h0 | h1
      · exact h0
      · exact absurd h1 (hcon x hx)
    have hsum : ∑ i, m.frameFunction (EuclideanSpace.basisFun (Fin n) ℂ i) = 1 :=
      m.isCFrameFunction (EuclideanSpace.basisFun (Fin n) ℂ)
    have hzero : ∀ i, m.frameFunction (EuclideanSpace.basisFun (Fin n) ℂ i) = 0 := fun i =>
      hall_zero _ ((EuclideanSpace.basisFun (Fin n) ℂ).norm_eq_one i)
    rw [Finset.sum_congr rfl (fun i _ => hzero i), Finset.sum_const_zero] at hsum
    exact absurd hsum (by norm_num)
  obtain ⟨x, hx1, hxval⟩ := hexists
  -- (b) Toute droite unitaire orthogonale à x a mesure 0 (ne dépend pas de la dichotomie).
  have hyzero : ∀ y : H n, ‖y‖ = 1 → ⟪x, y⟫_ℂ = 0 → m.μ (ℂ ∙ y) = 0 := by
    intro y hy1 hxy
    have hyx : ⟪y, x⟫_ℂ = 0 := by rw [(inner_conj_symm y x).symm, hxy]; simp
    set v : Fin 2 → H n := ![x, y] with hv_def
    have hv_orth : Orthonormal ℂ v := by
      rw [orthonormal_iff_ite]
      intro i j
      fin_cases i <;> fin_cases j <;> simp [hv_def, hx1, hy1, hxy, hyx]
    have h2n : 2 ≤ n := by omega
    obtain ⟨b, hb⟩ := exists_orthonormalBasis_extension_complex h2n v hv_orth
    have hb0 : b (Fin.castLE h2n 0) = x := hb 0
    have hb1 : b (Fin.castLE h2n 1) = y := hb 1
    have hsum : ∑ i, m.frameFunction (b i) = 1 := m.isCFrameFunction b
    have hnn : ∀ i, 0 ≤ m.frameFunction (b i) := fun i => m.nonneg _
    have hi0_val : m.frameFunction (b (Fin.castLE h2n 0)) = 1 := by rw [hb0]; exact hxval
    have hne : Fin.castLE h2n (0 : Fin 2) ≠ Fin.castLE h2n 1 :=
      (Fin.castLE_injective h2n).ne (by decide)
    have hpair_le : m.frameFunction (b (Fin.castLE h2n 0))
        + m.frameFunction (b (Fin.castLE h2n 1)) ≤ ∑ i, m.frameFunction (b i) := by
      have hsub : ({Fin.castLE h2n 0, Fin.castLE h2n 1} : Finset (Fin n)) ⊆ Finset.univ :=
        Finset.subset_univ _
      have hle := Finset.sum_le_sum_of_subset_of_nonneg hsub (fun i _ _ => hnn i)
      rwa [Finset.sum_pair hne] at hle
    rw [hsum, hi0_val] at hpair_le
    have hnn1 := hnn (Fin.castLE h2n 1)
    have hzero1 : m.frameFunction (b (Fin.castLE h2n 1)) = 0 := by linarith
    rwa [hb1] at hzero1
  -- (d) ρ x = x.
  have h1n : 1 ≤ n := by omega
  set v0 : Fin 1 → H n := fun _ => x with hv0_def
  have hv0_orth : Orthonormal ℂ v0 := by
    rw [orthonormal_iff_ite]
    intro i j
    fin_cases i; fin_cases j
    simp [hv0_def, hx1]
  obtain ⟨b0, hb0⟩ := exists_orthonormalBasis_extension_complex h1n v0 hv0_orth
  set i0 : Fin n := Fin.castLE h1n (0 : Fin 1) with hi0_def
  have hb0x : b0 i0 = x := hb0 0
  have hρbi_zero : ∀ i : Fin n, i ≠ i0 → ρ (b0 i) = 0 := by
    intro i hi
    have hortho : ⟪b0 i0, b0 i⟫_ℂ = 0 := by rw [b0.inner_eq_ite]; simp [Ne.symm hi]
    have hxbi : ⟪x, b0 i⟫_ℂ = 0 := by rw [← hb0x]; exact hortho
    have hbinorm : ‖b0 i‖ = 1 := b0.norm_eq_one i
    have hμzero : m.μ (ℂ ∙ (b0 i)) = 0 := hyzero (b0 i) hbinorm hxbi
    have hre_zero : (⟪ρ (b0 i), b0 i⟫_ℂ).re = 0 := by
      rw [← bornValue_span_singleton ρ (b0 i) hbinorm, ← hρ_born (ℂ ∙ (b0 i))]; exact hμzero
    have him_zero : (⟪ρ (b0 i), b0 i⟫_ℂ).im = 0 := by
      apply Complex.conj_eq_iff_im.mp; exact hρ_density.symmetric.conj_inner_sym (b0 i) (b0 i)
    have hcplx_zero : ⟪ρ (b0 i), b0 i⟫_ℂ = 0 := Complex.ext hre_zero (by rw [him_zero]; simp)
    exact positive_inner_self_eq_zero hρ_density.symmetric hρ_density.nonneg hcplx_zero
  have hρxx_re : (⟪ρ x, x⟫_ℂ).re = 1 := by
    rw [← bornValue_span_singleton ρ x hx1, ← hρ_born (ℂ ∙ x)]; exact hxval
  have hρxx_im : (⟪ρ x, x⟫_ℂ).im = 0 := by
    apply Complex.conj_eq_iff_im.mp; exact hρ_density.symmetric.conj_inner_sym x x
  have hρxx : ⟪ρ x, x⟫_ℂ = 1 := Complex.ext hρxx_re (by rw [hρxx_im]; simp)
  have hcoeff0 : ⟪b0 i0, ρ x⟫_ℂ = 1 := by
    rw [hb0x, ← hρ_density.symmetric x x]; exact hρxx
  have hcoeff_i : ∀ i : Fin n, i ≠ i0 → ⟪b0 i, ρ x⟫_ℂ = 0 := by
    intro i hi
    rw [← hρ_density.symmetric (b0 i) x, hρbi_zero i hi, inner_zero_left]
  have hρx_eq : ρ x = x := by
    have hrepr : (∑ i, ⟪b0 i, ρ x⟫_ℂ • b0 i) = ρ x := b0.sum_repr' (ρ x)
    have hsingle : (∑ i, ⟪b0 i, ρ x⟫_ℂ • b0 i) = ⟪b0 i0, ρ x⟫_ℂ • b0 i0 :=
      Finset.sum_eq_single i0 (fun i _ hi => by rw [hcoeff_i i hi, zero_smul])
        (fun hi0mem => absurd (Finset.mem_univ i0) hi0mem)
    rw [hsingle, hcoeff0, hb0x, one_smul] at hrepr
    exact hrepr.symm
  -- (e) Contradiction : w := (√2)⁻¹•(x+y) pour y unitaire ⊥ x a mesure 1/2.
  obtain ⟨y, hynorm, hyx, -⟩ := exists_unit_orthogonal_to_pair_complex hn x x
  have hxy : ⟪x, y⟫_ℂ = 0 := by rw [(inner_conj_symm x y).symm, hyx]; simp
  have hμy_zero : m.μ (ℂ ∙ y) = 0 := hyzero y hynorm hxy
  have hρyy_re : (⟪ρ y, y⟫_ℂ).re = 0 := by
    rw [← bornValue_span_singleton ρ y hynorm, ← hρ_born (ℂ ∙ y)]; exact hμy_zero
  have hρyy_im : (⟪ρ y, y⟫_ℂ).im = 0 := by
    apply Complex.conj_eq_iff_im.mp; exact hρ_density.symmetric.conj_inner_sym y y
  have hρyy : ⟪ρ y, y⟫_ℂ = 0 := Complex.ext hρyy_re (by rw [hρyy_im]; simp)
  have hρy_eq : ρ y = 0 := positive_inner_self_eq_zero hρ_density.symmetric hρ_density.nonneg hρyy
  set s : ℝ := Real.sqrt 2 with hs_def
  have hs_pos : 0 < s := Real.sqrt_pos.mpr (by norm_num)
  have hs_sq : s ^ 2 = 2 := by rw [hs_def, Real.sq_sqrt]; norm_num
  set w : H n := (s⁻¹ : ℂ) • (x + y) with hw_def
  have hxysq : ‖x + y‖ * ‖x + y‖ = 2 := by
    rw [norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero x y hxy, hx1, hynorm]
    norm_num
  have hwnorm : ‖w‖ = 1 := by
    rw [hw_def, norm_smul, norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hs_pos]
    have hxy_norm : ‖x + y‖ = s := by
      rw [← Real.sqrt_sq (norm_nonneg (x + y)), sq, hxysq, hs_def]
    rw [hxy_norm, inv_mul_cancel₀ hs_pos.ne']
  have hρw_eq : ρ w = (s⁻¹ : ℂ) • x := by
    rw [hw_def, map_smul, map_add, hρx_eq, hρy_eq, add_zero]
  have hρw_inner : ⟪ρ w, w⟫_ℂ = (((s ^ 2)⁻¹ : ℝ) : ℂ) := by
    rw [hρw_eq, hw_def, inner_smul_left, inner_smul_right, map_inv₀, Complex.conj_ofReal,
      inner_add_right, inner_self_eq_norm_sq_to_K, hx1, hxy]
    push_cast
    ring
  have hμw : m.μ (ℂ ∙ w) = 1 / 2 := by
    rw [hρ_born (ℂ ∙ w), bornValue_span_singleton ρ w hwnorm, hρw_inner, hs_sq]
    norm_num
  rcases h (ℂ ∙ w) with h0 | h1
  · rw [hμw] at h0; norm_num at h0
  · rw [hμw] at h1; norm_num at h1

-- Audit d'axiomes (fin de projet) : dans les quatre cas, uniquement
-- `propext`, `Classical.choice`, `Quot.sound` — aucun `sorryAx`, aucun axiome ad hoc.
#print axioms gleason
#print axioms busch
#print axioms busch_born_rule
#print axioms no_dispersion_free

end
end Gleason
