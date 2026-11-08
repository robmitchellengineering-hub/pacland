import Gleason.Real3.SphereGeometry

/-!
**FR.** # Coordonnées sphériques et chaîne de descente de Piron (CKM 1985 §5)

Extrait de `SphereGeometry.lean` (seuil des ~900 lignes atteint). Stratégie :
paramétrisation explicite `spherePoint b θ ψ` (colatitude `θ` depuis le pôle
`b 0`, azimut `ψ` dans le plan `(b 1, b 2)`), puis construction FERMÉE (sans
limite ni IVT) d'une chaîne de descente en deux phases : ajustement d'azimut
(`n` pas égaux, amplification contrôlée par Bernoulli, cf `Descent.lean`) puis
gain de distance pur (2 pas d'azimut opposé).

**EN.** # Spherical coordinates and Piron's descent chain (CKM 1985 §5)

Split off from `SphereGeometry.lean` (the ~900-line threshold was reached).
Strategy: explicit parametrization `spherePoint b θ ψ` (colatitude `θ` from the
pole `b 0`, azimuth `ψ` in the plane `(b 1, b 2)`), then a CLOSED construction
(no limit, no IVT) of a two-phase descent chain: azimuth adjustment (`n` equal
steps, amplification controlled by Bernoulli, cf. `Descent.lean`) then pure
distance gain (2 steps of opposite azimuth).
-/

namespace Gleason

open scoped RealInnerProductSpace Real

noncomputable section

/--
**FR.** **E1a.** Point de colatitude `θ` et azimut `ψ` dans la base `b` (pôle `b 0`,
plan équatorial `(b 1, b 2)`).

**EN.** **E1a.** Point of colatitude `θ` and azimuth `ψ` in the basis `b` (pole
`b 0`, equatorial plane `(b 1, b 2)`).
-/
noncomputable def spherePoint (b : OrthonormalBasis (Fin 3) ℝ E3) (θ ψ : ℝ) : E3 :=
  Real.cos θ • b 0 + (Real.sin θ * Real.cos ψ) • b 1 + (Real.sin θ * Real.sin ψ) • b 2

theorem inner_pole_spherePoint (b : OrthonormalBasis (Fin 3) ℝ E3) (θ ψ : ℝ) :
    ⟪b 0, spherePoint b θ ψ⟫ = Real.cos θ := by
  unfold spherePoint
  rw [inner_add_right, inner_add_right, real_inner_smul_right, real_inner_smul_right,
      real_inner_smul_right, b.inner_eq_one 0, b.inner_eq_zero (i := 0) (j := 1) (by decide),
      b.inner_eq_zero (i := 0) (j := 2) (by decide)]
  ring

theorem inner_snd_spherePoint (b : OrthonormalBasis (Fin 3) ℝ E3) (θ ψ : ℝ) :
    ⟪b 1, spherePoint b θ ψ⟫ = Real.sin θ * Real.cos ψ := by
  unfold spherePoint
  rw [inner_add_right, inner_add_right, real_inner_smul_right, real_inner_smul_right,
      real_inner_smul_right, b.inner_eq_zero (i := 1) (j := 0) (by decide), b.inner_eq_one 1,
      b.inner_eq_zero (i := 1) (j := 2) (by decide)]
  ring

theorem inner_trd_spherePoint (b : OrthonormalBasis (Fin 3) ℝ E3) (θ ψ : ℝ) :
    ⟪b 2, spherePoint b θ ψ⟫ = Real.sin θ * Real.sin ψ := by
  unfold spherePoint
  rw [inner_add_right, inner_add_right, real_inner_smul_right, real_inner_smul_right,
      real_inner_smul_right, b.inner_eq_zero (i := 2) (j := 0) (by decide),
      b.inner_eq_zero (i := 2) (j := 1) (by decide), b.inner_eq_one 2]
  ring

theorem norm_spherePoint (b : OrthonormalBasis (Fin 3) ℝ E3) (θ ψ : ℝ) :
    ‖spherePoint b θ ψ‖ = 1 := by
  set v : E3 := spherePoint b θ ψ with hv_def
  have hv0 : ⟪b 0, v⟫ = Real.cos θ := inner_pole_spherePoint b θ ψ
  have hv1 : ⟪b 1, v⟫ = Real.sin θ * Real.cos ψ := inner_snd_spherePoint b θ ψ
  have hv2 : ⟪b 2, v⟫ = Real.sin θ * Real.sin ψ := inner_trd_spherePoint b θ ψ
  have hvv : ⟪v, v⟫ = 1 := by
    nth_rewrite 1 [hv_def]
    unfold spherePoint
    rw [inner_add_left, inner_add_left, real_inner_smul_left, real_inner_smul_left,
        real_inner_smul_left, hv0, hv1, hv2]
    nlinarith [Real.sin_sq_add_cos_sq θ, Real.sin_sq_add_cos_sq ψ]
  have hsq : ‖v‖ ^ 2 = 1 := by rw [← real_inner_self_eq_norm_sq]; exact hvv
  nlinarith [norm_nonneg v, hsq]

theorem lat_spherePoint (b : OrthonormalBasis (Fin 3) ℝ E3) (θ ψ : ℝ) :
    lat (b 0) (spherePoint b θ ψ) = Real.cos θ ^ 2 := by
  unfold lat
  rw [inner_pole_spherePoint]

theorem mem_northern_spherePoint (b : OrthonormalBasis (Fin 3) ℝ E3) {θ : ℝ}
    (hθ0 : 0 ≤ θ) (hθ1 : θ ≤ π / 2) (ψ : ℝ) : spherePoint b θ ψ ∈ northern (b 0) := by
  refine ⟨norm_spherePoint b θ ψ, ?_⟩
  rw [inner_pole_spherePoint]
  exact Real.cos_nonneg_of_mem_Icc ⟨by linarith [Real.pi_pos], hθ1⟩

theorem ne_pole_spherePoint (b : OrthonormalBasis (Fin 3) ℝ E3) {θ : ℝ}
    (hθ0 : 0 < θ) (hθ1 : θ ≤ π / 2) (ψ : ℝ) : spherePoint b θ ψ ≠ b 0 := by
  intro heq
  have hsinpos : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθ0 (by linarith [Real.pi_pos])
  have h1 : ⟪b 1, spherePoint b θ ψ⟫ = 0 := by rw [heq]; exact b.inner_eq_zero (by decide)
  have h2 : ⟪b 2, spherePoint b θ ψ⟫ = 0 := by rw [heq]; exact b.inner_eq_zero (by decide)
  rw [inner_snd_spherePoint] at h1
  rw [inner_trd_spherePoint] at h2
  have hcosψ : Real.cos ψ = 0 := (mul_eq_zero.mp h1).resolve_left hsinpos.ne'
  have hsinψ : Real.sin ψ = 0 := (mul_eq_zero.mp h2).resolve_left hsinpos.ne'
  have hpyth := Real.sin_sq_add_cos_sq ψ
  rw [hcosψ, hsinψ] at hpyth
  norm_num at hpyth

/--
**FR.** **E1d (préliminaire).** Norme d'un point purement équatorial (colatitude
`π/2`) exprimé dans le plan `(b 1, b 2)`.

**EN.** **E1d (preliminary).** Norm of a purely equatorial point (colatitude
`π/2`) expressed in the plane `(b 1, b 2)`.
-/
theorem norm_equatorial_combo (b : OrthonormalBasis (Fin 3) ℝ E3) (ψ : ℝ) :
    ‖Real.cos ψ • b 1 + Real.sin ψ • b 2‖ = 1 := by
  have hb11 : (⟪b 1, b 1⟫ : ℝ) = 1 := b.inner_eq_one 1
  have hb22 : (⟪b 2, b 2⟫ : ℝ) = 1 := b.inner_eq_one 2
  have hb12 : (⟪b 1, b 2⟫ : ℝ) = 0 := b.inner_eq_zero (by decide)
  have hb21 : (⟪b 2, b 1⟫ : ℝ) = 0 := b.inner_eq_zero (by decide)
  set w : E3 := Real.cos ψ • b 1 + Real.sin ψ • b 2 with hw_def
  have hw1 : ⟪b 1, w⟫ = Real.cos ψ := by
    rw [hw_def, inner_add_right, real_inner_smul_right, real_inner_smul_right, hb11, hb12]
    ring
  have hw2 : ⟪b 2, w⟫ = Real.sin ψ := by
    rw [hw_def, inner_add_right, real_inner_smul_right, real_inner_smul_right, hb21, hb22]
    ring
  have hww : ⟪w, w⟫ = 1 := by
    nth_rewrite 1 [hw_def]
    rw [inner_add_left, real_inner_smul_left, real_inner_smul_left, hw1, hw2]
    nlinarith [Real.sin_sq_add_cos_sq ψ]
  have hsq : ‖w‖ ^ 2 = 1 := by rw [← real_inner_self_eq_norm_sq]; exact hww
  nlinarith [norm_nonneg w, hsq]

/--
**FR.** **E1d.** `sperp` d'un point de colatitude `θ ∈ (0, π/2]` : le point de
l'équateur diamétralement opposé dans le plan `(pôle, point)`, exprimé dans
la base `(b 0, b 1, b 2)`.

**EN.** **E1d.** `sperp` of a point of colatitude `θ ∈ (0, π/2]`: the
diametrically opposite equatorial point in the plane `(pole, point)`, expressed
in the basis `(b 0, b 1, b 2)`.
-/
theorem sperp_spherePoint (b : OrthonormalBasis (Fin 3) ℝ E3) {θ : ℝ}
    (hθ0 : 0 < θ) (hθ1 : θ ≤ π / 2) (ψ : ℝ) :
    sperp (b 0) (spherePoint b θ ψ) =
      Real.sin θ • b 0 - Real.cos θ • (Real.cos ψ • b 1 + Real.sin ψ • b 2) := by
  have hsinpos : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθ0 (by linarith [Real.pi_pos])
  have hcs : ⟪b 0, spherePoint b θ ψ⟫ = Real.cos θ := inner_pole_spherePoint b θ ψ
  have hdecomp : spherePoint b θ ψ - Real.cos θ • b 0 =
      Real.sin θ • (Real.cos ψ • b 1 + Real.sin ψ • b 2) := by
    unfold spherePoint
    module
  have hnormw : ‖spherePoint b θ ψ - Real.cos θ • b 0‖ = Real.sin θ := by
    rw [hdecomp, norm_smul, norm_equatorial_combo, mul_one, Real.norm_eq_abs,
        abs_of_pos hsinpos]
  have hsqrt : Real.sqrt (1 - Real.cos θ ^ 2) = Real.sin θ := by
    rw [show (1 : ℝ) - Real.cos θ ^ 2 = Real.sin θ ^ 2 by nlinarith [Real.sin_sq_add_cos_sq θ]]
    exact Real.sqrt_sq hsinpos.le
  unfold sperp
  rw [hcs, hnormw, hsqrt, hdecomp, smul_smul, smul_smul]
  have hscalar : Real.cos θ * (Real.sin θ)⁻¹ * Real.sin θ = Real.cos θ := by
    field_simp
  rw [hscalar]

/--
**FR.** **E1d (critère de pas).** `spherePoint b θ' ψ'` est dans le cercle de
descente de `spherePoint b θ ψ` (autour du pôle `b 0`) ssi l'identité
trigonométrique suivante est vérifiée. Calcul direct de
`⟪sperp (b0) (spherePoint b θ ψ), spherePoint b θ' ψ'⟫` via `sperp_spherePoint`
et les formules `inner_*_spherePoint`.

**EN.** **E1d (step criterion).** `spherePoint b θ' ψ'` lies in the descent
circle of `spherePoint b θ ψ` (around pole `b 0`) iff the following
trigonometric identity holds. Direct computation of
`⟪sperp (b0) (spherePoint b θ ψ), spherePoint b θ' ψ'⟫` via `sperp_spherePoint`
and the `inner_*_spherePoint` formulas.
-/
theorem spherePoint_mem_descent_iff (b : OrthonormalBasis (Fin 3) ℝ E3) {θ θ' : ℝ}
    (hθ0 : 0 < θ) (hθ1 : θ ≤ π / 2) (hθ'0 : 0 ≤ θ') (hθ'1 : θ' ≤ π / 2) (ψ ψ' : ℝ) :
    spherePoint b θ' ψ' ∈ descent (b 0) (spherePoint b θ ψ) ↔
      Real.sin θ * Real.cos θ' = Real.cos θ * Real.sin θ' * Real.cos (ψ' - ψ) := by
  have hmemN : spherePoint b θ' ψ' ∈ northern (b 0) := mem_northern_spherePoint b hθ'0 hθ'1 ψ'
  have hexpand : ⟪sperp (b 0) (spherePoint b θ ψ), spherePoint b θ' ψ'⟫ =
      Real.sin θ * Real.cos θ' - Real.cos θ * Real.sin θ' * Real.cos (ψ' - ψ) := by
    rw [sperp_spherePoint b hθ0 hθ1 ψ, Real.cos_sub]
    rw [inner_sub_left, real_inner_smul_left, real_inner_smul_left, inner_add_left,
        real_inner_smul_left, real_inner_smul_left, inner_pole_spherePoint,
        inner_snd_spherePoint, inner_trd_spherePoint]
    ring
  rw [mem_descent_iff]
  constructor
  · rintro ⟨_, h⟩
    rw [hexpand] at h
    linarith
  · intro h
    refine ⟨hmemN, ?_⟩
    rw [hexpand]
    linarith

/--
**FR.** **E1c.** Tout vecteur unitaire de `northern (b 0) \ {b 0}` s'exprime en
coordonnées sphériques dans la base `b`. Décomposition polaire de la
projection sur `(b 1, b 2)` via `Complex.arg` (aucun lemme Mathlib direct
« a²+b²=1 → ∃ψ, cosψ=a∧sinψ=b » : détour par `Complex.mk`/`normSq`).

**EN.** **E1c.** Every unit vector of `northern (b 0) \ {b 0}` can be expressed
in spherical coordinates in the basis `b`. Polar decomposition of the projection
onto `(b 1, b 2)` via `Complex.arg` (no direct Mathlib lemma
"a²+b²=1 → ∃ψ, cosψ=a∧sinψ=b": detour via `Complex.mk`/`normSq`).
-/
theorem exists_sphereCoords (b : OrthonormalBasis (Fin 3) ℝ E3) {t : E3}
    (ht : ‖t‖ = 1) (htN : t ∈ northern (b 0)) (htp : t ≠ b 0) :
    ∃ θ ψ : ℝ, 0 < θ ∧ θ ≤ π / 2 ∧ t = spherePoint b θ ψ := by
  set c : ℝ := ⟪b 0, t⟫ with hc_def
  have hc0 : 0 ≤ c := htN.2
  have hc1 : c ≤ 1 := by
    have h := abs_real_inner_le_norm (b 0) t
    rw [b.norm_eq_one 0, ht, mul_one] at h
    exact (abs_le.mp h).2
  have hcne1 : c ≠ 1 := by
    intro heq
    apply htp
    have hns : ‖t - c • b 0‖ ^ 2 = 1 - c ^ 2 := norm_sq_sub_inner_smul (b.norm_eq_one 0) ht
    rw [heq, one_smul] at hns
    norm_num at hns
    exact sub_eq_zero.mp hns
  set θ : ℝ := Real.arccos c with hθ_def
  have hθ0 : 0 < θ := by rw [hθ_def]; exact Real.arccos_pos.mpr (lt_of_le_of_ne hc1 hcne1)
  have hθ1 : θ ≤ π / 2 := by rw [hθ_def]; exact Real.arccos_le_pi_div_two.mpr hc0
  have hcosθ : Real.cos θ = c := Real.cos_arccos (by linarith) hc1
  have hsinθnn : Real.sin θ = Real.sqrt (1 - c ^ 2) := by rw [hθ_def]; exact Real.sin_arccos c
  have hsinθpos : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθ0 (by linarith [Real.pi_pos])
  set w : E3 := t - c • b 0 with hw_def
  have hw0 : ⟪b 0, w⟫ = 0 := by
    rw [hw_def, inner_sub_right, real_inner_smul_right, b.inner_eq_one 0, ← hc_def]
    ring
  have hwsq : ‖w‖ ^ 2 = Real.sin θ ^ 2 := by
    rw [hw_def, hc_def, norm_sq_sub_inner_smul (b.norm_eq_one 0) ht, ← hc_def, hsinθnn,
        Real.sq_sqrt (by nlinarith : (0 : ℝ) ≤ 1 - c ^ 2)]
  have hwnorm : ‖w‖ = Real.sin θ := by
    have heq0 : (‖w‖ - Real.sin θ) * (‖w‖ + Real.sin θ) = 0 := by linear_combination hwsq
    rcases mul_eq_zero.mp heq0 with h | h
    · linarith
    · linarith [norm_nonneg w]
  have hwne : w ≠ 0 := by
    intro h
    rw [h, norm_zero] at hwnorm
    linarith
  have hdecomp_w : ⟪b 1, w⟫ • b 1 + ⟪b 2, w⟫ • b 2 = w := by
    have h := b.sum_repr' w
    rw [Fin.sum_univ_three, hw0, zero_smul, zero_add] at h
    exact h
  have hw_sq_decomp : ‖w‖ ^ 2 = ⟪b 1, w⟫ ^ 2 + ⟪b 2, w⟫ ^ 2 := by
    rw [← real_inner_self_eq_norm_sq]
    nth_rewrite 1 [← hdecomp_w]
    rw [inner_add_left, real_inner_smul_left, real_inner_smul_left]
    ring
  have hwnn : ‖w‖ ≠ 0 := norm_ne_zero_iff.mpr hwne
  set a : ℝ := ⟪b 1, w⟫ / ‖w‖ with ha_def
  set d : ℝ := ⟪b 2, w⟫ / ‖w‖ with hd_def
  have had : a ^ 2 + d ^ 2 = 1 := by
    have hstep : a ^ 2 + d ^ 2 = (⟪b 1, w⟫ ^ 2 + ⟪b 2, w⟫ ^ 2) / ‖w‖ ^ 2 := by
      rw [ha_def, hd_def, div_pow, div_pow]; ring
    rw [hstep, ← hw_sq_decomp, div_self (pow_ne_zero 2 hwnn)]
  set z : ℂ := ⟨a, d⟩ with hz_def
  have hnormSqz : Complex.normSq z = 1 := by
    rw [hz_def, Complex.normSq_mk]
    nlinarith [had]
  have hzne : z ≠ 0 := by
    intro h
    rw [h, map_zero] at hnormSqz
    norm_num at hnormSqz
  have hzabs : ‖z‖ = 1 := by
    have hsq : ‖z‖ ^ 2 = 1 := by rw [← Complex.normSq_eq_norm_sq]; exact hnormSqz
    have heq0 : (‖z‖ - 1) * (‖z‖ + 1) = 0 := by linear_combination hsq
    rcases mul_eq_zero.mp heq0 with h | h
    · linarith
    · linarith [norm_nonneg z]
  set ψ : ℝ := Complex.arg z with hψ_def
  have hcosψ : Real.cos ψ = a := by
    rw [hψ_def, Complex.cos_arg hzne, hzabs, div_one]
  have hsinψ : Real.sin ψ = d := by
    rw [hψ_def, Complex.sin_arg, hzabs, div_one]
  refine ⟨θ, ψ, hθ0, hθ1, ?_⟩
  unfold spherePoint
  rw [hcosθ, hsinθnn, hcosψ, hsinψ, ha_def, hd_def]
  have h1 : Real.sqrt (1 - c ^ 2) * (⟪b 1, w⟫ / ‖w‖) = ⟪b 1, w⟫ := by
    rw [← hsinθnn, hwnorm]; field_simp
  have h2 : Real.sqrt (1 - c ^ 2) * (⟪b 2, w⟫ / ‖w‖) = ⟪b 2, w⟫ := by
    rw [← hsinθnn, hwnorm]; field_simp
  rw [h1, h2, add_assoc, hdecomp_w, hw_def]
  abel

/--
**FR.** **E3 (lemme de pas générique).** Formulation en `tan` du critère de
descente : pour `θ, θ' ∈ (0, π/2)`, si `tan θ' · cos(ψ'-ψ) = tan θ`, alors
`spherePoint b θ' ψ'` est dans le cercle de descente de `spherePoint b θ ψ`.
Se réduit à une tautologie pour les pas de la phase A de E4 (ajustement
d'azimut à rapport de distance constant).

**EN.** **E3 (generic step lemma).** `tan`-based formulation of the descent
criterion: for `θ, θ' ∈ (0, π/2)`, if `tan θ' · cos(ψ'-ψ) = tan θ`, then
`spherePoint b θ' ψ'` lies in the descent circle of `spherePoint b θ ψ`. Reduces
to a tautology for the phase-A steps of E4 (azimuth adjustment at constant
distance ratio).
-/
theorem spherePoint_mem_descent_of_tan (b : OrthonormalBasis (Fin 3) ℝ E3) {θ θ' : ℝ}
    (hθ0 : 0 < θ) (hθ1 : θ < π / 2) (hθ'0 : 0 < θ') (hθ'1 : θ' < π / 2) (ψ ψ' : ℝ)
    (htan : Real.tan θ' * Real.cos (ψ' - ψ) = Real.tan θ) :
    spherePoint b θ' ψ' ∈ descent (b 0) (spherePoint b θ ψ) := by
  have hcosθpos : 0 < Real.cos θ := Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], hθ1⟩
  have hcosθ'pos : 0 < Real.cos θ' := Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], hθ'1⟩
  rw [spherePoint_mem_descent_iff b hθ0 hθ1.le hθ'0.le hθ'1.le]
  rw [Real.tan_eq_sin_div_cos, Real.tan_eq_sin_div_cos] at htan
  field_simp at htan
  linarith [htan]

/--
**FR.** **E4 équatorial (pas terminal).** `spherePoint b (π/2) (ψ+π/2)` (un point de
l'équateur) est dans le cercle de descente de `spherePoint b θ ψ`, pour tout
`θ ∈ (0, π/2)`. Le critère se réduit à `0 = 0` (`cos(π/2) = 0` des deux côtés).

**EN.** **E4 equatorial (terminal step).** `spherePoint b (π/2) (ψ+π/2)` (a point
of the equator) lies in the descent circle of `spherePoint b θ ψ`, for every
`θ ∈ (0, π/2)`. The criterion reduces to `0 = 0` (`cos(π/2) = 0` on both
sides).
-/
theorem spherePoint_mem_descent_equatorial (b : OrthonormalBasis (Fin 3) ℝ E3) {θ : ℝ}
    (hθ0 : 0 < θ) (hθ1 : θ < π / 2) (ψ : ℝ) :
    spherePoint b (π / 2) (ψ + π / 2) ∈ descent (b 0) (spherePoint b θ ψ) := by
  rw [spherePoint_mem_descent_iff b hθ0 hθ1.le (by linarith [Real.pi_pos]) le_rfl]
  simp

/--
**FR.** **E4 (lemme-outil, réutilisé pour les phases A et B).** Une suite de rayons
`radius i > 0` et d'azimuts `azimuth i` satisfaisant la relation de pas
(`radius (i+1) · cos(Δazimut) = radius i`, i.e. `tan θᵢ₊₁ · cos(Δψ) = tan θᵢ`
une fois passée par `arctan`) produit, point par point, une chaîne de
descente valide via `spherePoint_mem_descent_of_tan`.

**EN.** **E4 (tool lemma, reused for phases A and B).** A sequence of radii
`radius i > 0` and azimuths `azimuth i` satisfying the step relation
(`radius (i+1) · cos(Δazimuth) = radius i`, i.e.
`tan θᵢ₊₁ · cos(Δψ) = tan θᵢ` once passed through `arctan`) produces, point by
point, a valid descent chain via `spherePoint_mem_descent_of_tan`.
-/
theorem tan_chain_step (b : OrthonormalBasis (Fin 3) ℝ E3) (radius azimuth : ℕ → ℝ)
    (hradius_pos : ∀ i, 0 < radius i) {N : ℕ}
    (hstep : ∀ i < N, radius (i + 1) * Real.cos (azimuth (i + 1) - azimuth i) = radius i) :
    ∀ i < N, spherePoint b (Real.arctan (radius i)) (azimuth i) ≠ b 0 ∧
      spherePoint b (Real.arctan (radius (i + 1))) (azimuth (i + 1)) ∈
        descent (b 0) (spherePoint b (Real.arctan (radius i)) (azimuth i)) := by
  intro i hi
  have hθi0 : 0 < Real.arctan (radius i) := Real.arctan_pos.mpr (hradius_pos i)
  have hθi1 : Real.arctan (radius i) < π / 2 := Real.arctan_lt_pi_div_two _
  have hθi1'0 : 0 < Real.arctan (radius (i + 1)) := Real.arctan_pos.mpr (hradius_pos (i + 1))
  have hθi1'1 : Real.arctan (radius (i + 1)) < π / 2 := Real.arctan_lt_pi_div_two _
  refine ⟨ne_pole_spherePoint b hθi0 hθi1.le _, ?_⟩
  apply spherePoint_mem_descent_of_tan b hθi0 hθi1 hθi1'0 hθi1'1
  rw [Real.tan_arctan, Real.tan_arctan]
  exact hstep i hi

/--
**FR.** **E4 (point de départ).** Toute paire `(p, s)` avec `s ∈ northern p \ {p}`
admet une base `b` avec `b 0 = p` et `s` d'azimut nul (`s = spherePoint b θ 0`).
Même construction que `sperp_core`/`exists_sphereCoords` (projection
équatoriale normalisée de `s`), mais construisant `b` plutôt que décomposant
dans un `b` donné.

**EN.** **E4 (starting point).** Every pair `(p, s)` with `s ∈ northern p \ {p}`
admits a basis `b` with `b 0 = p` and `s` at zero azimuth
(`s = spherePoint b θ 0`). Same construction as `sperp_core`/
`exists_sphereCoords` (normalized equatorial projection of `s`), but building
`b` rather than decomposing within a given `b`.
-/
theorem exists_basis_aligned {p s : E3} (hp : ‖p‖ = 1) (hs : ‖s‖ = 1)
    (hsN : s ∈ northern p) (hsp : s ≠ p) :
    ∃ (b : OrthonormalBasis (Fin 3) ℝ E3) (θ : ℝ), b 0 = p ∧ 0 < θ ∧ θ ≤ π / 2 ∧
      s = spherePoint b θ 0 := by
  set c : ℝ := ⟪p, s⟫ with hc_def
  have hc0 : 0 ≤ c := hsN.2
  have hc1 : c ≤ 1 := by
    have h := abs_real_inner_le_norm p s
    rw [hp, hs, mul_one] at h
    exact (abs_le.mp h).2
  have hnormsq : ‖s - c • p‖ ^ 2 = 1 - c ^ 2 := norm_sq_sub_inner_smul hp hs
  have hcne1 : c ≠ 1 := by
    intro heq
    apply hsp
    have hns := hnormsq
    rw [heq, one_smul] at hns
    norm_num at hns
    exact sub_eq_zero.mp hns
  set θ : ℝ := Real.arccos c with hθ_def
  have hθ0 : 0 < θ := by rw [hθ_def]; exact Real.arccos_pos.mpr (lt_of_le_of_ne hc1 hcne1)
  have hθ1 : θ ≤ π / 2 := by rw [hθ_def]; exact Real.arccos_le_pi_div_two.mpr hc0
  have hcosθ : Real.cos θ = c := Real.cos_arccos (by linarith) hc1
  have hsinθnn : Real.sin θ = Real.sqrt (1 - c ^ 2) := by rw [hθ_def]; exact Real.sin_arccos c
  have hvne : s - c • p ≠ 0 := by
    intro h
    apply hcne1
    rw [h, norm_zero] at hnormsq
    have heq0 : (c - 1) * (c + 1) = 0 := by linear_combination hnormsq
    rcases mul_eq_zero.mp heq0 with h1 | h1
    · linarith
    · linarith [hc0]
  have hvnormpos : 0 < ‖s - c • p‖ := norm_pos_iff.mpr hvne
  set e : E3 := ‖s - c • p‖⁻¹ • (s - c • p) with he_def
  have he_norm : ‖e‖ = 1 := by
    rw [he_def, norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hvnormpos)]
    field_simp
  have hpe : ⟪p, e⟫ = 0 := by
    have hstep : ⟪p, s - c • p⟫ = 0 := by
      rw [inner_sub_right, real_inner_smul_right, real_inner_self_eq_norm_sq, hp, ← hc_def]
      ring
    rw [he_def, real_inner_smul_right, hstep, mul_zero]
  obtain ⟨b, hb0, hb1⟩ := exists_orthonormalBasis_pair p e hp he_norm hpe
  refine ⟨b, θ, hb0, hθ0, hθ1, ?_⟩
  unfold spherePoint
  simp only [Real.cos_zero, Real.sin_zero, mul_one, mul_zero, zero_smul, add_zero]
  rw [hcosθ, hb0, hsinθnn, ← hnormsq, Real.sqrt_sq (norm_nonneg _), hb1, he_def, smul_smul,
      mul_inv_cancel₀ hvnormpos.ne', one_smul]
  abel

end
end Gleason
