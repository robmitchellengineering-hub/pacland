import Gleason.Real3.Attainment

/-!
**FR.** # Régularité des frame functions positives sur ℝ³ (CKM 1985 §7)

**Théorème central du cœur analytique réel** : toute frame function positive
sur S² est la restriction d'une forme quadratique. Chemin CKM : cadre extrémal
(p,q,r) via le bloc G (H1, lemme-pivot COMBLANT une lacune du papier), deux
rotations d'axe (p̂, r̂) et les identités qu'elles induisent (H3), un « Claim »
de coïncidence f=g sur six grands cercles (H4), puis un second passage du même
argument à h:=g−f (poids nul, H6-H8) conclu par un argument de dénombrement
(H9, six cercles / deux paires de zéros / pigeonhole) qui exclut h≠0.

`heven` (parité) n'est PAS une hypothèse de ce théorème : elle est dérivable de
`hf` seule via `frameFunction_even` (P2, bloc A) — retirée de l'énoncé
d'origine (acté dans SORRIES.md, cf. règle 3 de CLAUDE.md).

**EN.** # Regularity of positive frame functions on ℝ³ (CKM 1985 §7)

**Central theorem of the real analytic core**: every positive frame function on
S² is the restriction of a quadratic form. CKM route: extremal frame (p,q,r) via
block G (H1, pivot lemma FILLING a gap in the paper), two axis rotations
(p̂, r̂) and the identities they induce (H3), a coincidence "Claim" `f=g` on six
great circles (H4), then a second pass of the same argument on `h:=g−f`
(zero weight, H6-H8) concluded by a counting argument (H9, six circles / two
pairs of zeros / pigeonhole) that rules out `h≠0`.

`heven` (parity) is NOT a hypothesis of this theorem: it is derivable from `hf`
alone via `frameFunction_even` (P2, block A) — removed from the original
statement (recorded in SORRIES.md, cf. rule 3 of CLAUDE.md).
-/

namespace Gleason

open scoped RealInnerProductSpace Real

noncomputable section

/- ═══════════════════════════════════════════════════════════════════
   H1 (lemme-pivot, comble une lacune du papier CKM). Étant un pôle `P`
   réalisant le sup d'une frame function bornée `φ` et un point `R0`
   réalisant l'inf, construit un triple orthonormé `(P, S1, U)` avec
   `φ(S1) = Wφ - φ(P) - φ(R0)` et `φ(U) = φ(R0)`.
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **H1.** `S1` orthogonal à `P` et `R0` (existence garantie en dimension 3,
`exists_unit_orthogonal_to_pair`) ; deux frames `(P,S1,T1)` et `(R0,S1,T2)`
encadrent `φ(S1)` par les extrema globaux `φ(P)` (max) et `φ(R0)` (min) des
DEUX côtés à la fois, forçant l'égalité `φ(S1) = Wφ-φ(P)-φ(R0)` (double
encadrement). `U` complète `(P,S1)` en un troisième frame, donnant
`φ(U) = φ(R0)` par soustraction.

**EN.** **H1.** `S1` orthogonal to `P` and `R0` (existence guaranteed in
dimension 3, `exists_unit_orthogonal_to_pair`); two frames `(P,S1,T1)` and
`(R0,S1,T2)` sandwich `φ(S1)` between the global extrema `φ(P)` (max) and
`φ(R0)` (min) from BOTH sides at once, forcing the equality
`φ(S1) = Wφ-φ(P)-φ(R0)` (double sandwich). `U` completes `(P,S1)` into a third
frame, giving `φ(U) = φ(R0)` by subtraction.
-/
theorem exists_extremal_frame {φ : E3 → ℝ} {Wφ : ℝ} (hφ : IsFrameFunction φ Wφ)
    {P : E3} (hP : ‖P‖ = 1) (hPmax : ∀ t : E3, ‖t‖ = 1 → φ t ≤ φ P)
    {R0 : E3} (hR0 : ‖R0‖ = 1) (hR0lb : ∀ t : E3, ‖t‖ = 1 → φ R0 ≤ φ t)
    (_hne : φ P ≠ φ R0) :
    ∃ S1 U : E3, ‖S1‖ = 1 ∧ ‖U‖ = 1 ∧ ⟪P, S1⟫ = 0 ∧ ⟪P, U⟫ = 0 ∧ ⟪S1, U⟫ = 0 ∧
      φ S1 = Wφ - φ P - φ R0 ∧ φ U = φ R0 := by
  obtain ⟨S1, hS1, hS1P', hS1R0'⟩ := exists_unit_orthogonal_to_pair P R0
  have hPS1 : ⟪P, S1⟫ = 0 := by rw [real_inner_comm]; exact hS1P'
  have hR0S1 : ⟪R0, S1⟫ = 0 := by rw [real_inner_comm]; exact hS1R0'
  obtain ⟨T1, hT1, hPT1, hS1T1⟩ := exists_third_orthogonal P S1 hP hS1 hPS1
  obtain ⟨T2, hT2, hR0T2, hS1T2⟩ := exists_third_orthogonal R0 S1 hR0 hS1 hR0S1
  obtain ⟨b1, hb1_0, hb1_1, hb1_2⟩ :=
    exists_orthonormalBasis_of_triple' P S1 T1 hP hS1 hT1 hPS1 hPT1 hS1T1
  obtain ⟨b2, hb2_0, hb2_1, hb2_2⟩ :=
    exists_orthonormalBasis_of_triple' R0 S1 T2 hR0 hS1 hT2 hR0S1 hR0T2 hS1T2
  have hsum1 := hφ b1
  rw [Fin.sum_univ_three, hb1_0, hb1_1, hb1_2] at hsum1
  have hsum2 := hφ b2
  rw [Fin.sum_univ_three, hb2_0, hb2_1, hb2_2] at hsum2
  have hT1le : φ T1 ≤ φ P := hPmax T1 hT1
  have hT1ge : φ R0 ≤ φ T1 := hR0lb T1 hT1
  have hT2le : φ T2 ≤ φ P := hPmax T2 hT2
  have hT2ge : φ R0 ≤ φ T2 := hR0lb T2 hT2
  have hS1eq : φ S1 = Wφ - φ P - φ R0 := by linarith [hsum1, hsum2, hT1le, hT1ge, hT2le, hT2ge]
  obtain ⟨U, hU, hUP', hUS1'⟩ := exists_unit_orthogonal_to_pair P S1
  have hPU : ⟪P, U⟫ = 0 := by rw [real_inner_comm]; exact hUP'
  have hS1U : ⟪S1, U⟫ = 0 := by rw [real_inner_comm]; exact hUS1'
  obtain ⟨b3, hb3_0, hb3_1, hb3_2⟩ :=
    exists_orthonormalBasis_of_triple' P S1 U hP hS1 hU hPS1 hPU hS1U
  have hsum3 := hφ b3
  rw [Fin.sum_univ_three, hb3_0, hb3_1, hb3_2] at hsum3
  have hUeq : φ U = φ R0 := by linarith [hsum3, hS1eq]
  exact ⟨S1, U, hS1, hU, hPS1, hPU, hS1U, hS1eq, hUeq⟩

/- ═══════════════════════════════════════════════════════════════════
   H3 (préliminaire). Rotation de 90° autour d'un axe `A`, envoyant une
   paire équatoriale prescrite `(X,Y) ↦ (Y,-X)`. Généralise `exists_rotate90`
   (bloc G) qui construisait sa propre paire ; ici `(X,Y)` est DONNÉE (on a
   besoin de coordonnées liées à un triple extrémal spécifique). Réutilisé
   deux fois : `p̂` (axe P, paire (Q,R)) et `r̂` (axe R, paire (P,Q)), puis à
   nouveau en H8 pour `h`.
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **H3 (préliminaire).** Même preuve que `exists_rotate90`, avec `(X,Y)`
prescrits au lieu d'auto-générés.

**EN.** **H3 (preliminary).** Same proof as `exists_rotate90`, with `(X,Y)`
prescribed instead of auto-generated.
-/
private theorem exists_axis_rotate {A X Y : E3} (hA : ‖A‖ = 1) (hX : ‖X‖ = 1) (hY : ‖Y‖ = 1)
    (hAX : ⟪A, X⟫ = 0) (hAY : ⟪A, Y⟫ = 0) (hXY : ⟪X, Y⟫ = 0) :
    ∃ ρ : E3 ≃ₗᵢ[ℝ] E3, ρ A = A ∧ ρ X = Y ∧ ρ Y = -X ∧
      ∀ s ∈ equator A, ρ s ∈ equator A ∧ ⟪s, ρ s⟫ = 0 := by
  have hYX : ⟪Y, X⟫ = 0 := by rw [real_inner_comm]; exact hXY
  have hAnX : ⟪A, -X⟫ = 0 := by rw [inner_neg_right, hAX]; ring
  have hYnX : ⟪Y, -X⟫ = 0 := by rw [inner_neg_right, hYX]; ring
  have hnX : ‖(-X : E3)‖ = 1 := by rw [norm_neg]; exact hX
  obtain ⟨ρ, hρA, hρX, hρY⟩ :=
    isometry_of_orthonormal_triples hA hX hY hAX hAY hXY hA hY hnX hAY hAnX hYnX
  refine ⟨ρ, hρA, hρX, hρY, ?_⟩
  intro s hs
  have hsu : ‖s‖ = 1 := hs.1
  have hsA : ⟪A, s⟫ = 0 := hs.2
  have hρsA : ⟪A, ρ s⟫ = 0 := by rw [← hρA, ρ.inner_map_map]; exact hsA
  have hρsnorm : ‖ρ s‖ = 1 := by rw [ρ.norm_map]; exact hsu
  refine ⟨⟨hρsnorm, hρsA⟩, ?_⟩
  obtain ⟨b, hb0, hb1, hb2⟩ := exists_orthonormalBasis_of_triple' A X Y hA hX hY hAX hAY hXY
  have hdecomp : ⟪X, s⟫ • X + ⟪Y, s⟫ • Y = s := by
    have h := b.sum_repr' s
    rw [Fin.sum_univ_three, hb0, hsA, zero_smul, zero_add, hb1, hb2] at h
    exact h
  set a : ℝ := ⟪X, s⟫ with ha_def
  set c : ℝ := ⟪Y, s⟫ with hc_def
  have hρs_eq : ρ s = a • Y - c • X := by
    rw [← hdecomp, ρ.map_add, ρ.map_smul, ρ.map_smul, hρX, hρY, smul_neg]
    abel
  rw [hρs_eq, ← hdecomp]
  simp only [inner_add_left, inner_sub_right, real_inner_smul_left, real_inner_smul_right,
    real_inner_self_eq_norm_sq, hX, hY, hXY, hYX]
  ring

/--
**FR.** **H3 (préliminaire).** Action de `ρ` (issue de `exists_axis_rotate`) sur
les coordonnées `⟪A,·⟫, ⟪X,·⟫, ⟪Y,·⟫` : `⟪a,ρs⟫ = ⟪ρ⁻¹a,s⟫` (isométrie),
puis `ρ⁻¹A=A, ρ⁻¹Y=X, ρ⁻¹X=-Y` (inverse de `ρA=A,ρX=Y,ρY=-X`).

**EN.** **H3 (preliminary).** Action of `ρ` (from `exists_axis_rotate`) on the
coordinates `⟪A,·⟫, ⟪X,·⟫, ⟪Y,·⟫`: `⟪a,ρs⟫ = ⟪ρ⁻¹a,s⟫` (isometry), then
`ρ⁻¹A=A, ρ⁻¹Y=X, ρ⁻¹X=-Y` (inverse of `ρA=A,ρX=Y,ρY=-X`).
-/
private theorem axis_rotate_coords {A X Y : E3} {ρ : E3 ≃ₗᵢ[ℝ] E3}
    (hρA : ρ A = A) (hρX : ρ X = Y) (hρY : ρ Y = -X) (s : E3) :
    ⟪A, ρ s⟫ = ⟪A, s⟫ ∧ ⟪X, ρ s⟫ = -⟪Y, s⟫ ∧ ⟪Y, ρ s⟫ = ⟪X, s⟫ := by
  have hsymm : ∀ a : E3, ⟪a, ρ s⟫ = ⟪ρ.symm a, s⟫ := by
    intro a
    rw [← ρ.inner_map_map (ρ.symm a) s, ρ.apply_symm_apply]
  have hsymmA : ρ.symm A = A := by
    have h := congrArg ρ.symm hρA
    rw [ρ.symm_apply_apply] at h
    exact h.symm
  have hsymmY : ρ.symm Y = X := by
    have h := congrArg ρ.symm hρX
    rw [ρ.symm_apply_apply] at h
    exact h.symm
  have hsymmX : ρ.symm X = -Y := by
    have h := congrArg ρ.symm hρY
    rw [ρ.symm_apply_apply, map_neg] at h
    have h2 := congrArg Neg.neg h
    rw [neg_neg] at h2
    exact h2.symm
  refine ⟨?_, ?_, ?_⟩
  · rw [hsymm A, hsymmA]
  · rw [hsymm X, hsymmX, inner_neg_left]
  · rw [hsymm Y, hsymmY]

/- ═══════════════════════════════════════════════════════════════════
   H3-H4 (Claim, lemme générique réutilisable en H8 pour h).
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **H3-H4 (Claim).** Étant `φ` frame function de poids `Wφ`, un triple
orthonormé `(P,Q,R)` avec `P` réalisant le sup, `R` l'inf, et
`φ(Q) = Wφ-φ(P)-φ(R)` (H1), la forme `g(s) := φ(P)⟪P,s⟫²+φ(Q)⟪Q,s⟫²+φ(R)⟪R,s⟫²`
coïncide avec `φ` sur les six grands cercles `⟪P,·⟫=±⟪Q,·⟫`, `⟪P,·⟫=±⟪R,·⟫`,
`⟪Q,·⟫=±⟪R,·⟫`. Deux rotations d'axe `P`/`R` (`p̂`,`r̂`) donnent deux identités
(I) `φ+φ∘p̂ = g+g∘p̂` et (II) `φ+φ∘r̂ = g+g∘r̂` (F appliqué à `φ+φ∘p̂` au pôle `P`,
à `-(φ+φ∘r̂)` au pôle `R`) ; les cas `x=y`/`y=z` sont primaires
(`p̂(p̂(r̂s))=-s` / `p̂(r̂(r̂s))=-s` sous ces conditions précises, + parité), les
quatre autres s'y ramènent via l'action de `p̂`/`r̂` sur les coordonnées.

**EN.** **H3-H4 (Claim).** Given `φ` a frame function of weight `Wφ`, an
orthonormal triple `(P,Q,R)` with `P` realizing the sup, `R` the inf, and
`φ(Q) = Wφ-φ(P)-φ(R)` (H1), the form
`g(s) := φ(P)⟪P,s⟫²+φ(Q)⟪Q,s⟫²+φ(R)⟪R,s⟫²` coincides with `φ` on the six great
circles `⟪P,·⟫=±⟪Q,·⟫`, `⟪P,·⟫=±⟪R,·⟫`, `⟪Q,·⟫=±⟪R,·⟫`. Two axis rotations
`P`/`R` (`p̂`,`r̂`) give two identities: (I) `φ+φ∘p̂ = g+g∘p̂` and
(II) `φ+φ∘r̂ = g+g∘r̂` (F applied to `φ+φ∘p̂` at pole `P`, to `-(φ+φ∘r̂)` at
pole `R`); the cases `x=y`/`y=z` are primary
(`p̂(p̂(r̂s))=-s` / `p̂(r̂(r̂s))=-s` under these precise conditions, plus
parity), the other four reduce to them via the action of `p̂`/`r̂` on the
coordinates.
-/
theorem frame_eq_quadratic_of_extremal_triple {φ : E3 → ℝ} {Wφ : ℝ} (hφ : IsFrameFunction φ Wφ)
    {P Q R : E3} (hP : ‖P‖ = 1) (hQ : ‖Q‖ = 1) (hR : ‖R‖ = 1)
    (hPQ : ⟪P, Q⟫ = 0) (hPR : ⟪P, R⟫ = 0) (hQR : ⟪Q, R⟫ = 0)
    (hPmax : ∀ t : E3, ‖t‖ = 1 → φ t ≤ φ P) (hRmin : ∀ t : E3, ‖t‖ = 1 → φ R ≤ φ t)
    (hQeq : φ Q = Wφ - φ P - φ R) :
    ∀ s : E3, ‖s‖ = 1 →
      (⟪P, s⟫ = ⟪Q, s⟫ ∨ ⟪P, s⟫ = -⟪Q, s⟫ ∨ ⟪P, s⟫ = ⟪R, s⟫ ∨ ⟪P, s⟫ = -⟪R, s⟫ ∨
        ⟪Q, s⟫ = ⟪R, s⟫ ∨ ⟪Q, s⟫ = -⟪R, s⟫) →
      φ s = φ P * ⟪P, s⟫ ^ 2 + φ Q * ⟪Q, s⟫ ^ 2 + φ R * ⟪R, s⟫ ^ 2 := by
  set g : E3 → ℝ := fun s => φ P * ⟪P, s⟫ ^ 2 + φ Q * ⟪Q, s⟫ ^ 2 + φ R * ⟪R, s⟫ ^ 2 with hg_def
  have hRP : ⟪R, P⟫ = 0 := by rw [real_inner_comm]; exact hPR
  have hRQ : ⟪R, Q⟫ = 0 := by rw [real_inner_comm]; exact hQR
  obtain ⟨phat, hphatP, hphatQ, hphatR, hphat_equator⟩ := exists_axis_rotate hP hQ hR hPQ hPR hQR
  obtain ⟨rhat, hrhatR, hrhatP, hrhatQ, hrhat_equator⟩ := exists_axis_rotate hR hP hQ hRP hRQ hPQ
  have hp_coords : ∀ s : E3, ⟪P, phat s⟫ = ⟪P, s⟫ ∧ ⟪Q, phat s⟫ = -⟪R, s⟫ ∧
      ⟪R, phat s⟫ = ⟪Q, s⟫ := fun s => axis_rotate_coords hphatP hphatQ hphatR s
  have hr_coords : ∀ s : E3, ⟪R, rhat s⟫ = ⟪R, s⟫ ∧ ⟪P, rhat s⟫ = -⟪Q, s⟫ ∧
      ⟪Q, rhat s⟫ = ⟪P, s⟫ := fun s => axis_rotate_coords hrhatR hrhatP hrhatQ s
  have hParseval : ∀ s : E3, ⟪P, s⟫ ^ 2 + ⟪Q, s⟫ ^ 2 + ⟪R, s⟫ ^ 2 = ‖s‖ ^ 2 := by
    intro s
    obtain ⟨b, hb0, hb1, hb2⟩ := exists_orthonormalBasis_of_triple' P Q R hP hQ hR hPQ hPR hQR
    rw [real_inner_comm s P, real_inner_comm s Q, real_inner_comm s R]
    have h := b.sum_sq_inner_left s
    rw [Fin.sum_univ_three, hb0, hb1, hb2] at h
    exact h
  have hbasis_decomp : ∀ v : E3, ⟪P, v⟫ • P + ⟪Q, v⟫ • Q + ⟪R, v⟫ • R = v := by
    intro v
    obtain ⟨b, hb0, hb1, hb2⟩ := exists_orthonormalBasis_of_triple' P Q R hP hQ hR hPQ hPR hQR
    have h := b.sum_repr' v
    rw [Fin.sum_univ_three, hb0, hb1, hb2] at h
    exact h
  have hg_even : ∀ s : E3, g (-s) = g s := by
    intro s; simp only [hg_def, inner_neg_right]; ring
  -- **Identité (I)** : φ + φ∘p̂ = g + g∘p̂.
  have hI : ∀ s : E3, ‖s‖ = 1 → φ s + φ (phat s) = g s + g (phat s) := by
    intro s hs
    have hψframe : IsFrameFunction (fun x => φ x + φ (phat x)) (2 * Wφ) := by
      have h := hφ.add (hφ.comp_isometry phat)
      rwa [two_mul]
    have hψequator : ∀ e ∈ equator P, (fun x => φ x + φ (phat x)) e = Wφ - φ P := by
      intro e he
      obtain ⟨hpe_mem, hpe_orth⟩ := hphat_equator e he
      obtain ⟨b, hb0, hb1, hb2⟩ := exists_orthonormalBasis_of_triple' P e (phat e) hP he.1
        hpe_mem.1 he.2 hpe_mem.2 hpe_orth
      have hsum := hφ b
      rw [Fin.sum_univ_three, hb0, hb1, hb2] at hsum
      simp only
      linarith [hsum]
    have hψmax : ∀ t : E3, ‖t‖ = 1 →
        (fun x => φ x + φ (phat x)) t ≤ (fun x => φ x + φ (phat x)) P := by
      intro t ht
      have h2 : ‖phat t‖ = 1 := by rw [phat.norm_map]; exact ht
      simp only [hphatP]
      linarith [hPmax t ht, hPmax (phat t) h2]
    have hex := frameFunction_exact_pole hψframe hP hψmax hψequator s hs
    simp only [hphatP] at hex
    unfold lat at hex
    have hgcomp : g s + g (phat s) = (Wφ - φ P) + (φ P + φ P - (Wφ - φ P)) * ⟪P, s⟫ ^ 2 := by
      obtain ⟨e1, e2, e3⟩ := hp_coords s
      have hPar := hParseval s
      rw [hs] at hPar
      have hqr : φ Q + φ R = Wφ - φ P := by linarith [hQeq]
      simp only [hg_def, e1, e2, e3]
      linear_combination (Wφ - φ P) * hPar + (⟪Q, s⟫ ^ 2 + ⟪R, s⟫ ^ 2) * hqr
    linarith [hex, hgcomp]
  -- **Identité (II)** : φ + φ∘r̂ = g + g∘r̂.
  have hII : ∀ s : E3, ‖s‖ = 1 → φ s + φ (rhat s) = g s + g (rhat s) := by
    intro s hs
    have hψ'frame : IsFrameFunction (fun x => -(φ x + φ (rhat x))) (-(2 * Wφ)) := by
      have h := (hφ.add (hφ.comp_isometry rhat)).neg
      rwa [two_mul]
    have hψ'equator : ∀ e ∈ equator R, (fun x => -(φ x + φ (rhat x))) e = -(Wφ - φ R) := by
      intro e he
      obtain ⟨hre_mem, hre_orth⟩ := hrhat_equator e he
      obtain ⟨b, hb0, hb1, hb2⟩ := exists_orthonormalBasis_of_triple' R e (rhat e) hR he.1
        hre_mem.1 he.2 hre_mem.2 hre_orth
      have hsum := hφ b
      rw [Fin.sum_univ_three, hb0, hb1, hb2] at hsum
      simp only
      linarith [hsum]
    have hψ'max : ∀ t : E3, ‖t‖ = 1 →
        (fun x => -(φ x + φ (rhat x))) t ≤ (fun x => -(φ x + φ (rhat x))) R := by
      intro t ht
      have h2 : ‖rhat t‖ = 1 := by rw [rhat.norm_map]; exact ht
      simp only [hrhatR]
      linarith [hRmin t ht, hRmin (rhat t) h2]
    have hex := frameFunction_exact_pole hψ'frame hR hψ'max hψ'equator s hs
    simp only [hrhatR] at hex
    unfold lat at hex
    have hgcomp : g s + g (rhat s) = (Wφ - φ R) + (φ R + φ R - (Wφ - φ R)) * ⟪R, s⟫ ^ 2 := by
      obtain ⟨e1, e2, e3⟩ := hr_coords s
      have hPar := hParseval s
      rw [hs] at hPar
      have hpq : φ P + φ Q = Wφ - φ R := by linarith [hQeq]
      simp only [hg_def, e1, e2, e3]
      linear_combination (Wφ - φ R) * hPar + (⟪P, s⟫ ^ 2 + ⟪Q, s⟫ ^ 2) * hpq
    linarith [hex, hgcomp]
  -- Cas primaire [x=y].
  have hcase_xy : ∀ s : E3, ‖s‖ = 1 → ⟪P, s⟫ = ⟪Q, s⟫ → φ s = g s := by
    intro s hs hxy
    have hs1 : ‖rhat s‖ = 1 := by rw [rhat.norm_map]; exact hs
    have hs2 : ‖phat (rhat s)‖ = 1 := by rw [phat.norm_map]; exact hs1
    have heq3 : phat (phat (rhat s)) = -s := by
      have hP3 : ⟪P, phat (phat (rhat s))⟫ = -⟪Q, s⟫ := by
        rw [(hp_coords (phat (rhat s))).1, (hp_coords (rhat s)).1, (hr_coords s).2.1]
      have hQ3 : ⟪Q, phat (phat (rhat s))⟫ = -⟪P, s⟫ := by
        rw [(hp_coords (phat (rhat s))).2.1, (hp_coords (rhat s)).2.2, (hr_coords s).2.2]
      have hR3 : ⟪R, phat (phat (rhat s))⟫ = -⟪R, s⟫ := by
        rw [(hp_coords (phat (rhat s))).2.2, (hp_coords (rhat s)).2.1, (hr_coords s).1]
      have hLHS := (hbasis_decomp (phat (phat (rhat s)))).symm
      rw [hP3, hQ3, hR3] at hLHS
      have hRHS : (-s : E3) = -(⟪P, s⟫ • P + ⟪Q, s⟫ • Q + ⟪R, s⟫ • R) := by rw [hbasis_decomp]
      rw [hLHS, hRHS, hxy]
      module
    have hII1 := hII s hs
    have hI2 := hI (rhat s) hs1
    have hI3 := hI (phat (rhat s)) hs2
    have hchain : φ s + φ (phat (phat (rhat s))) = g s + g (phat (phat (rhat s))) := by
      linarith [hII1, hI2, hI3]
    rw [heq3, frameFunction_even hφ s hs, hg_even s] at hchain
    linarith [hchain]
  -- Cas primaire [y=z].
  have hcase_yz : ∀ s : E3, ‖s‖ = 1 → ⟪Q, s⟫ = ⟪R, s⟫ → φ s = g s := by
    intro s hs hyz
    have hs1 : ‖rhat s‖ = 1 := by rw [rhat.norm_map]; exact hs
    have hs2 : ‖rhat (rhat s)‖ = 1 := by rw [rhat.norm_map]; exact hs1
    have heq3 : phat (rhat (rhat s)) = -s := by
      have hP3 : ⟪P, phat (rhat (rhat s))⟫ = -⟪P, s⟫ := by
        rw [(hp_coords (rhat (rhat s))).1, (hr_coords (rhat s)).2.1, (hr_coords s).2.2]
      have hQ3 : ⟪Q, phat (rhat (rhat s))⟫ = -⟪R, s⟫ := by
        rw [(hp_coords (rhat (rhat s))).2.1, (hr_coords (rhat s)).1, (hr_coords s).1]
      have hR3 : ⟪R, phat (rhat (rhat s))⟫ = -⟪Q, s⟫ := by
        rw [(hp_coords (rhat (rhat s))).2.2, (hr_coords (rhat s)).2.2, (hr_coords s).2.1]
      have hLHS := (hbasis_decomp (phat (rhat (rhat s)))).symm
      rw [hP3, hQ3, hR3] at hLHS
      have hRHS : (-s : E3) = -(⟪P, s⟫ • P + ⟪Q, s⟫ • Q + ⟪R, s⟫ • R) := by rw [hbasis_decomp]
      rw [hLHS, hRHS, hyz]
      module
    have hII1 := hII s hs
    have hII2 := hII (rhat s) hs1
    have hI1 := hI (rhat (rhat s)) hs2
    have hchain : φ s + φ (phat (rhat (rhat s))) = g s + g (phat (rhat (rhat s))) := by
      linarith [hII1, hII2, hI1]
    rw [heq3, frameFunction_even hφ s hs, hg_even s] at hchain
    linarith [hchain]
  intro s hs hcond
  rcases hcond with hxy | hxny | hxz | hxnz | hyz | hynz
  · exact hcase_xy s hs hxy
  · -- x = -y : r̂s satisfait x'=y' (coords (-y,x,z), -y=x).
    have hrs : ‖rhat s‖ = 1 := by rw [rhat.norm_map]; exact hs
    have hcond' : ⟪P, rhat s⟫ = ⟪Q, rhat s⟫ := by
      rw [(hr_coords s).2.1, (hr_coords s).2.2, ← hxny]
    have hgr := hcase_xy (rhat s) hrs hcond'
    have hII1 := hII s hs
    linarith [hII1, hgr]
  · -- x = z : ramené à y = z sur r̂s.
    have hrs : ‖rhat s‖ = 1 := by rw [rhat.norm_map]; exact hs
    have hcond' : ⟪Q, rhat s⟫ = ⟪R, rhat s⟫ := by
      rw [(hr_coords s).2.2, (hr_coords s).1, ← hxz]
    have hgr := hcase_yz (rhat s) hrs hcond'
    have hII1 := hII s hs
    linarith [hII1, hgr]
  · -- x = -z : p̂s satisfait x'=y' (coords (x,-z,y), x=-z).
    have hps : ‖phat s‖ = 1 := by rw [phat.norm_map]; exact hs
    have hcond' : ⟪P, phat s⟫ = ⟪Q, phat s⟫ := by
      rw [(hp_coords s).1, (hp_coords s).2.1, ← hxnz]
    have hgp := hcase_xy (phat s) hps hcond'
    have hI1 := hI s hs
    linarith [hI1, hgp]
  · exact hcase_yz s hs hyz
  · -- y = -z : p̂s satisfait y'=z' (coords (x,-z,y), -z=y).
    have hps : ‖phat s‖ = 1 := by rw [phat.norm_map]; exact hs
    have hcond' : ⟪Q, phat s⟫ = ⟪R, phat s⟫ := by
      rw [(hp_coords s).2.1, (hp_coords s).2.2, ← hynz]
    have hgp := hcase_yz (phat s) hps hcond'
    have hI1 := hI s hs
    linarith [hI1, hgp]

/- ═══════════════════════════════════════════════════════════════════
   H2 (préliminaires). Forme quadratique de la norme au carré (outil
   partagé par les cas dégénérés et l'assemblage final).
   ═══════════════════════════════════════════════════════════════════ -/

/-- **H2 (outil).** `∑ᵢ ⟪bᵢ,s⟫²` comme forme quadratique, valant `‖s‖²`. -/
def normSqQF (b : OrthonormalBasis (Fin 3) ℝ E3) : QuadraticForm ℝ E3 :=
  QuadraticMap.linMulLin (innerₗ E3 (b 0)) (innerₗ E3 (b 0)) +
  QuadraticMap.linMulLin (innerₗ E3 (b 1)) (innerₗ E3 (b 1)) +
  QuadraticMap.linMulLin (innerₗ E3 (b 2)) (innerₗ E3 (b 2))

theorem normSqQF_apply (b : OrthonormalBasis (Fin 3) ℝ E3) (s : E3) :
    normSqQF b s = ‖s‖ ^ 2 := by
  simp only [normSqQF, QuadraticMap.add_apply, QuadraticMap.linMulLin_apply, innerₗ_apply_apply]
  rw [← b.sum_sq_inner_right s, Fin.sum_univ_three]
  ring

set_option maxHeartbeats 2000000 in
/--
**FR.** **Régularité (Gleason réel, dimension 3).** Toute frame function positive
est quadratique sur la sphère (`heven` retirée : dérivable via
`frameFunction_even`, cf. le commentaire d'en-tête).

**EN.** **Regularity (real Gleason, dimension 3).** Every positive frame function
is quadratic on the sphere (`heven` removed: derivable via
`frameFunction_even`, see the header comment).
-/
theorem frameFunction_regular (f : E3 → ℝ) (W : ℝ)
    (hf : IsFrameFunction f W) (hnn : ∀ x, ‖x‖ = 1 → 0 ≤ f x) :
    ∃ q : QuadraticForm ℝ E3, ∀ x, ‖x‖ = 1 → f x = q x := by
  have hle : ∀ x : E3, ‖x‖ = 1 → f x ≤ W := fun x hx => hf.le_of_nonneg hnn hx
  obtain ⟨p, hp, hpmax⟩ := frameFunction_attains_sup hf hle
  obtain ⟨r0, hr0, hr0lb⟩ := frameFunction_attains_inf hf hnn
  set b0 := EuclideanSpace.basisFun (Fin 3) ℝ with hb0_def
  by_cases hMm : f p = f r0
  · -- **H2a.** M = m : f est constante.
    refine ⟨f p • normSqQF b0, fun x hx => ?_⟩
    have hle1 : f x ≤ f p := hpmax x hx
    have hge1 : f r0 ≤ f x := hr0lb x hx
    have hfx : f x = f p := by linarith [hMm ▸ hge1]
    rw [QuadraticMap.smul_apply, normSqQF_apply, hx]
    norm_num [hfx]
  · -- H1 fournit le triple extrémal (p, q, r) avec f(q) = W - f(p) - f(r0).
    obtain ⟨q, r, hq, hr, hpq, hpr, hqr, hqeq, hreq⟩ :=
      exists_extremal_frame hf hp hpmax hr0 hr0lb hMm
    set M : ℝ := f p with hM_def
    set α : ℝ := f q with hα_def
    set m : ℝ := f r0 with hm_def
    by_cases hαm : α = m
    · -- **H2b.** α = m ⟺ W = M + 2m : f ≡ m sur l'équateur de p, F conclut.
      have hWeq : W = M + 2 * m := by linarith [hqeq, hαm]
      have hconst : ∀ e ∈ equator p, f e = m := by
        intro e he
        obtain ⟨e', he', hpe', hee'⟩ := exists_third_orthogonal p e hp he.1 he.2
        obtain ⟨b, hb0, hb1, hb2⟩ :=
          exists_orthonormalBasis_of_triple' p e e' hp he.1 he' he.2 hpe' hee'
        have hsum := hf b
        rw [Fin.sum_univ_three, hb0, hb1, hb2] at hsum
        have hem : m ≤ f e := hr0lb e he.1
        have he'm : m ≤ f e' := hr0lb e' he'
        linarith [hsum, hWeq, hem, he'm]
      have hexact := frameFunction_exact_pole hf hp hpmax hconst
      refine ⟨m • normSqQF b0 + (M - m) • QuadraticMap.linMulLin (innerₗ E3 p) (innerₗ E3 p),
        fun x hx => ?_⟩
      have hex := hexact x hx
      unfold lat at hex
      rw [hex, QuadraticMap.add_apply, QuadraticMap.smul_apply, QuadraticMap.smul_apply,
        normSqQF_apply, hx, QuadraticMap.linMulLin_apply, innerₗ_apply_apply]
      ring
    · by_cases hαM : α = M
      · -- **H2c.** α = M ⟺ W = 2M + m : f ≡ M sur l'équateur de r0, F sur −f.
        have hWeq : W = 2 * M + m := by linarith [hqeq, hαM]
        have hconst : ∀ e ∈ equator r0, f e = M := by
          intro e he
          obtain ⟨e', he', hr0e', hee'⟩ := exists_third_orthogonal r0 e hr0 he.1 he.2
          obtain ⟨b, hb0, hb1, hb2⟩ :=
            exists_orthonormalBasis_of_triple' r0 e e' hr0 he.1 he' he.2 hr0e' hee'
          have hsum := hf b
          rw [Fin.sum_univ_three, hb0, hb1, hb2] at hsum
          have hem : f e ≤ M := hpmax e he.1
          have he'm : f e' ≤ M := hpmax e' he'
          linarith [hsum, hWeq, hem, he'm]
        have hconst_neg : ∀ e ∈ equator r0, (fun x => -f x) e = -M := by
          intro e he; simp only; rw [hconst e he]
        have hmax_neg : ∀ t : E3, ‖t‖ = 1 → (fun x => -f x) t ≤ (fun x => -f x) r0 := by
          intro t ht; simp only; linarith [hr0lb t ht]
        have hexact := frameFunction_exact_pole hf.neg hr0 hmax_neg hconst_neg
        refine ⟨M • normSqQF b0 - (M - m) • QuadraticMap.linMulLin (innerₗ E3 r0) (innerₗ E3 r0),
          fun x hx => ?_⟩
        have hex := hexact x hx
        unfold lat at hex
        rw [QuadraticMap.sub_apply, QuadraticMap.smul_apply, QuadraticMap.smul_apply,
          normSqQF_apply, hx, QuadraticMap.linMulLin_apply, innerₗ_apply_apply, smul_eq_mul,
          smul_eq_mul]
        linarith [hex]
      · -- Cas principal : m < α < M strictement (H3-H9).
        have hRmin_r : ∀ t : E3, ‖t‖ = 1 → f r ≤ f t := by rw [hreq]; exact hr0lb
        have hqeq' : f q = W - f p - f r := by rw [hreq]; exact hqeq
        have hαM : α ≤ M := hpmax q hq
        have hmα : m ≤ α := hr0lb q hq
        set g : E3 → ℝ := fun s => M * ⟪p, s⟫ ^ 2 + α * ⟪q, s⟫ ^ 2 + m * ⟪r, s⟫ ^ 2 with hg_def
        have hParseval_pqr : ∀ s : E3, ⟪p, s⟫ ^ 2 + ⟪q, s⟫ ^ 2 + ⟪r, s⟫ ^ 2 = ‖s‖ ^ 2 := by
          intro s
          obtain ⟨b, hb0, hb1, hb2⟩ := exists_orthonormalBasis_of_triple' p q r hp hq hr hpq hpr hqr
          rw [real_inner_comm s p, real_inner_comm s q, real_inner_comm s r]
          have hh := b.sum_sq_inner_left s
          rw [Fin.sum_univ_three, hb0, hb1, hb2] at hh
          exact hh
        have hclaim : ∀ s : E3, ‖s‖ = 1 →
            (⟪p, s⟫ = ⟪q, s⟫ ∨ ⟪p, s⟫ = -⟪q, s⟫ ∨ ⟪p, s⟫ = ⟪r, s⟫ ∨ ⟪p, s⟫ = -⟪r, s⟫ ∨
              ⟪q, s⟫ = ⟪r, s⟫ ∨ ⟪q, s⟫ = -⟪r, s⟫) → f s = g s := by
          intro s hs hcond
          have hh := frame_eq_quadratic_of_extremal_triple hf hp hq hr hpq hpr hqr hpmax hRmin_r
            hqeq' s hs hcond
          rw [hreq] at hh
          exact hh
        have hgframe : IsFrameFunction g W := by
          intro b
          have e1 := b.sum_sq_inner_left p
          have e2 := b.sum_sq_inner_left q
          have e3 := b.sum_sq_inner_left r
          rw [hp] at e1
          rw [hq] at e2
          rw [hr] at e3
          norm_num at e1 e2 e3
          have hsum : ∑ i, g (b i) = M * ∑ i, ⟪p, b i⟫ ^ 2 + α * ∑ i, ⟪q, b i⟫ ^ 2 +
              m * ∑ i, ⟪r, b i⟫ ^ 2 := by
            simp only [hg_def, Finset.mul_sum]
            rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
          rw [hsum, e1, e2, e3]
          linarith [hqeq]
        have hg_bound_le : ∀ s : E3, ‖s‖ = 1 → g s ≤ M := by
          intro s hs
          have hPar := hParseval_pqr s
          rw [hs] at hPar
          norm_num at hPar
          have hMeq : M * ⟪p, s⟫ ^ 2 + M * ⟪q, s⟫ ^ 2 + M * ⟪r, s⟫ ^ 2 = M := by
            rw [← mul_add, ← mul_add, hPar, mul_one]
          have h1 : α * ⟪q, s⟫ ^ 2 ≤ M * ⟪q, s⟫ ^ 2 := mul_le_mul_of_nonneg_right hαM (sq_nonneg _)
          have h2 : m * ⟪r, s⟫ ^ 2 ≤ M * ⟪r, s⟫ ^ 2 :=
            mul_le_mul_of_nonneg_right (by linarith [hαM, hmα]) (sq_nonneg _)
          simp only [hg_def]
          linarith [hMeq, h1, h2]
        have hg_bound_ge : ∀ s : E3, ‖s‖ = 1 → m ≤ g s := by
          intro s hs
          have hPar := hParseval_pqr s
          rw [hs] at hPar
          norm_num at hPar
          have hmeq : m * ⟪p, s⟫ ^ 2 + m * ⟪q, s⟫ ^ 2 + m * ⟪r, s⟫ ^ 2 = m := by
            rw [← mul_add, ← mul_add, hPar, mul_one]
          have h1 : m * ⟪p, s⟫ ^ 2 ≤ M * ⟪p, s⟫ ^ 2 :=
            mul_le_mul_of_nonneg_right (by linarith [hαM, hmα]) (sq_nonneg _)
          have h2 : m * ⟪q, s⟫ ^ 2 ≤ α * ⟪q, s⟫ ^ 2 := mul_le_mul_of_nonneg_right hmα (sq_nonneg _)
          simp only [hg_def]
          linarith [hmeq, h1, h2]
        set h : E3 → ℝ := fun s => g s - f s with hh_def
        have hhframe : IsFrameFunction h 0 := by
          have hsub := hgframe.sub hf
          simpa [hh_def] using hsub
        have hh_even : ∀ s : E3, ‖s‖ = 1 → h (-s) = h s := by
          intro s hs
          simp only [hh_def, hg_def, inner_neg_right]
          rw [frameFunction_even hf s hs]
          ring
        have hh_le : ∀ s : E3, ‖s‖ = 1 → h s ≤ M - m := by
          intro s hs
          have h1 := hg_bound_le s hs
          have h2 : m ≤ f s := hr0lb s hs
          simp only [hh_def]; linarith
        have hh_ge : ∀ s : E3, ‖s‖ = 1 → -(M - m) ≤ h s := by
          intro s hs
          have h1 := hg_bound_ge s hs
          have h2 : f s ≤ M := hpmax s hs
          simp only [hh_def]; linarith
        have hh_zero : ∀ s : E3, ‖s‖ = 1 →
            (⟪p, s⟫ = ⟪q, s⟫ ∨ ⟪p, s⟫ = -⟪q, s⟫ ∨ ⟪p, s⟫ = ⟪r, s⟫ ∨ ⟪p, s⟫ = -⟪r, s⟫ ∨
              ⟪q, s⟫ = ⟪r, s⟫ ∨ ⟪q, s⟫ = -⟪r, s⟫) → h s = 0 := by
          intro s hs hcond
          simp only [hh_def]
          rw [hclaim s hs hcond]
          ring
        -- Forme quadratique cible (partagée par les deux branches de H6-H7).
        set Q0 : QuadraticForm ℝ E3 :=
          M • QuadraticMap.linMulLin (innerₗ E3 p) (innerₗ E3 p) +
          α • QuadraticMap.linMulLin (innerₗ E3 q) (innerₗ E3 q) +
          m • QuadraticMap.linMulLin (innerₗ E3 r) (innerₗ E3 r) with hQ0_def
        have hQ0_apply : ∀ s : E3, Q0 s = g s := by
          intro s
          simp only [hQ0_def, hg_def, QuadraticMap.add_apply, QuadraticMap.smul_apply,
            QuadraticMap.linMulLin_apply, innerₗ_apply_apply, smul_eq_mul]
          ring
        suffices hzero_final : ∀ s : E3, ‖s‖ = 1 → h s = 0 by
          refine ⟨Q0, fun x hx => ?_⟩
          have hhx := hzero_final x hx
          simp only [hh_def] at hhx
          rw [hQ0_apply x]
          linarith [hhx]
        -- **H6.** Extrema de `h` (via G).
        obtain ⟨p2, hp2_norm, hp2max⟩ := frameFunction_attains_sup hhframe hh_le
        obtain ⟨r2, hr2_norm, hr2min⟩ := frameFunction_attains_inf hhframe hh_ge
        by_cases hMm2 : h p2 = h r2
        · -- `h` constante ; poids nul ⟹ `h ≡ 0`.
          obtain ⟨b, hb0⟩ := exists_orthonormalBasis_fst p2 hp2_norm
          have hsum := hhframe b
          rw [Fin.sum_univ_three, hb0] at hsum
          have e1 : h (b 1) = h p2 := le_antisymm (hp2max (b 1) (b.norm_eq_one 1))
            (by rw [hMm2]; exact hr2min (b 1) (b.norm_eq_one 1))
          have e2 : h (b 2) = h p2 := le_antisymm (hp2max (b 2) (b.norm_eq_one 2))
            (by rw [hMm2]; exact hr2min (b 2) (b.norm_eq_one 2))
          rw [e1, e2] at hsum
          have hp2zero : h p2 = 0 := by linarith [hsum]
          intro s hs
          have h1 : h s ≤ h p2 := hp2max s hs
          have h2 : h r2 ≤ h s := hr2min s hs
          rw [hMm2] at h1
          linarith [h1, h2, hp2zero, hMm2]
        · -- **H7.** `h(p2) ≠ h(r2)` : H1 donne un triple extrémal `(p2,q2,r2)` pour `h`.
          obtain ⟨q2, r2', hq2_norm, hr2'_norm, hp2q2, hp2r2', hq2r2', hq2eq, hr2'eq⟩ :=
            exists_extremal_frame hhframe hp2_norm hp2max hr2_norm hr2min hMm2
          -- Zéro de `h` sur l'équateur de `p2`, via le cercle `⟪p-q,·⟫=0` (H4/H5).
          obtain ⟨s0, hs0_norm, hs0pq, hs0p2⟩ := exists_unit_orthogonal_to_pair (p - q) p2
          have hs0_cond : ⟪p, s0⟫ = ⟪q, s0⟫ := by
            have hz : ⟪p - q, s0⟫ = 0 := by rw [real_inner_comm]; exact hs0pq
            rw [inner_sub_left] at hz; linarith [hz]
          have hs0_zero : h s0 = 0 := hh_zero s0 hs0_norm (Or.inl hs0_cond)
          have hp2s0 : ⟪p2, s0⟫ = 0 := by rw [real_inner_comm]; exact hs0p2
          have hM2nonneg : 0 ≤ h p2 := by rw [← hs0_zero]; exact hp2max s0 hs0_norm
          obtain ⟨t0, ht0_norm, hp2t0, hs0t0⟩ :=
            exists_third_orthogonal p2 s0 hp2_norm hs0_norm hp2s0
          obtain ⟨bt, hbt0, hbt1, hbt2⟩ :=
            exists_orthonormalBasis_of_triple' p2 s0 t0 hp2_norm hs0_norm ht0_norm hp2s0 hp2t0 hs0t0
          have hsumt := hhframe bt
          rw [Fin.sum_univ_three, hbt0, hbt1, hbt2, hs0_zero] at hsumt
          have ht0eq : h t0 = -(h p2) := by linarith [hsumt]
          have hstep1 : h r2 ≤ -(h p2) := by rw [← ht0eq]; exact hr2min t0 ht0_norm
          -- Argument miroir sur l'équateur de `r2`.
          obtain ⟨s0', hs0'_norm, hs0'pq, hs0'r2⟩ := exists_unit_orthogonal_to_pair (p - q) r2
          have hs0'_cond : ⟪p, s0'⟫ = ⟪q, s0'⟫ := by
            have hz : ⟪p - q, s0'⟫ = 0 := by rw [real_inner_comm]; exact hs0'pq
            rw [inner_sub_left] at hz; linarith [hz]
          have hs0'_zero : h s0' = 0 := hh_zero s0' hs0'_norm (Or.inl hs0'_cond)
          have hr2s0' : ⟪r2, s0'⟫ = 0 := by rw [real_inner_comm]; exact hs0'r2
          obtain ⟨t0', ht0'_norm, hr2t0', hs0't0'⟩ :=
            exists_third_orthogonal r2 s0' hr2_norm hs0'_norm hr2s0'
          obtain ⟨bt', hbt0', hbt1', hbt2'⟩ := exists_orthonormalBasis_of_triple' r2 s0' t0'
            hr2_norm hs0'_norm ht0'_norm hr2s0' hr2t0' hs0't0'
          have hsumt' := hhframe bt'
          rw [Fin.sum_univ_three, hbt0', hbt1', hbt2', hs0'_zero] at hsumt'
          have ht0'eq : h t0' = -(h r2) := by linarith [hsumt']
          have hstep2 : h t0' ≤ h p2 := hp2max t0' ht0'_norm
          have hMm2eq : h p2 + h r2 = 0 := by
            rw [ht0'eq] at hstep2
            linarith [hstep1, hstep2]
          have hq2zero : h q2 = 0 := by linarith [hq2eq, hMm2eq]
          -- **H8.** Réapplique le Claim (H3-H4) à `h` sur le triple (p2,q2,r2').
          have hRmin_r2' : ∀ t : E3, ‖t‖ = 1 → h r2' ≤ h t := by rw [hr2'eq]; exact hr2min
          have hq2eq' : h q2 = 0 - h p2 - h r2' := by rw [hr2'eq]; exact hq2eq
          have hclaim_h := frame_eq_quadratic_of_extremal_triple hhframe hp2_norm hq2_norm
            hr2'_norm hp2q2 hp2r2' hq2r2' hp2max hRmin_r2' hq2eq'
          rw [hq2zero] at hclaim_h
          have hr2'M2 : h r2' = -(h p2) := by rw [hr2'eq]; linarith [hMm2eq]
          -- `hclaim_h : ∀ s, ‖s‖=1 → (6 cond en p2,q2,r2') → h s = h(p2)*⟪p2,s⟫² - h(p2)*⟪r2',s⟫²`
          -- **H9 (CKM §7, fin).** `M2 := h p2 > 0` (strict) et deux points diagonaux
          -- NON PRIMÉS `u,w` (combinaisons de p,q,r) forcés dans le cercle primé
          -- `Γ := {x2 = y2}` par un argument de tiroirs (2 issues possibles pour
          -- chaque zéro de `h` sur `Γ`, cf. `hclaim_h` + `hh_zero`), donnant
          -- `r2' ∈ span{u,w} ⊆ {y = z}` (non primé) donc `h r2' = 0`, contredisant
          -- `h r2' = -M2 ≠ 0`.
          set M2 : ℝ := h p2 with hM2_def
          have hM2pos : 0 < M2 := by
            rcases hM2nonneg.lt_or_eq with hM20 | hM20
            · exact hM20
            · exact absurd (by linarith [hMm2eq, hM20, hM2_def] : h p2 = h r2) hMm2
          -- Rend `g`, `h`, `Q0`, `M2` opaques : leur définition ne sert plus, seules
          -- les propriétés déjà établies (hhframe, hh_zero, hclaim_h, hQ0_apply...)
          -- sont utilisées à partir d'ici (cf. CLAUDE.md, pattern anti-lenteur).
          clear_value Q0 M2 h g
          have hqp : ⟪q, p⟫ = 0 := by rw [real_inner_comm]; exact hpq
          have hrp : ⟪r, p⟫ = 0 := by rw [real_inner_comm]; exact hpr
          have hrq : ⟪r, q⟫ = 0 := by rw [real_inner_comm]; exact hqr
          set u : E3 := (Real.sqrt 3)⁻¹ • (p + q + r) with hu_def
          set w : E3 := (Real.sqrt 3)⁻¹ • (p - q - r) with hw_def
          have h3sq : Real.sqrt 3 * Real.sqrt 3 = 3 := Real.mul_self_sqrt (by norm_num)
          have hinner_uu : ⟪p + q + r, p + q + r⟫ = 3 := by
            simp only [inner_add_left, inner_add_right, real_inner_self_eq_norm_sq, hp, hq, hr,
              hpq, hpr, hqr, hqp, hrp, hrq]
            norm_num
          have hinner_ww : ⟪p - q - r, p - q - r⟫ = 3 := by
            simp only [inner_sub_left, inner_sub_right, real_inner_self_eq_norm_sq, hp, hq, hr,
              hpq, hpr, hqr, hqp, hrp, hrq]
            norm_num
          have hsqrt3_eq : (Real.sqrt 3)⁻¹ * ((Real.sqrt 3)⁻¹ * 3) = 1 := by
            rw [← mul_assoc, ← mul_inv, h3sq]
            norm_num
          have hu_norm : ‖u‖ = 1 := by
            have h2 : ‖u‖ ^ 2 = 1 := by
              rw [← real_inner_self_eq_norm_sq, hu_def, real_inner_smul_left,
                real_inner_smul_right, hinner_uu]
              exact hsqrt3_eq
            have hh := Real.sqrt_sq (norm_nonneg u)
            rw [h2, Real.sqrt_one] at hh
            exact hh.symm
          have hw_norm : ‖w‖ = 1 := by
            have h2 : ‖w‖ ^ 2 = 1 := by
              rw [← real_inner_self_eq_norm_sq, hw_def, real_inner_smul_left,
                real_inner_smul_right, hinner_ww]
              exact hsqrt3_eq
            have hh := Real.sqrt_sq (norm_nonneg w)
            rw [h2, Real.sqrt_one] at hh
            exact hh.symm
          -- Boîte à outils : orthonormalité ⟹ distinction, non-colinéarité via un témoin.
          have hvne : ∀ A B : E3, ‖A‖ = 1 → ‖B‖ = 1 → ⟪A, B⟫ = 0 → A ≠ B := by
            intro A B hA hB hAB heq
            rw [heq, real_inner_self_eq_norm_sq, hB] at hAB
            norm_num at hAB
          have hpq_ne0 : (p - q : E3) ≠ 0 := sub_ne_zero.mpr (hvne p q hp hq hpq)
          have hpr_ne0 : (p - r : E3) ≠ 0 := sub_ne_zero.mpr (hvne p r hp hr hpr)
          have hp2q2_ne0 : (p2 - q2 : E3) ≠ 0 := sub_ne_zero.mpr (hvne p2 q2 hp2_norm hq2_norm hp2q2)
          have hnprop : ∀ A B C : E3, ⟪C, A⟫ = 0 → ⟪C, B⟫ ≠ 0 → ∀ c : ℝ, c • A ≠ B := by
            intro A B C hCA hCB c hc
            exact hCB (by rw [← hc, real_inner_smul_right, hCA, mul_zero])
          have hne_pq_pr : ∀ c : ℝ, c • (p - q) ≠ p - r := by
            apply hnprop (p - q) (p - r) r
            · rw [inner_sub_right, hrp, hrq]; ring
            · rw [inner_sub_right, hrp, real_inner_self_eq_norm_sq, hr]; norm_num
          have hne_pq_qr : ∀ c : ℝ, c • (p - q) ≠ q - r := by
            apply hnprop (p - q) (q - r) r
            · rw [inner_sub_right, hrp, hrq]; ring
            · rw [inner_sub_right, hrq, real_inner_self_eq_norm_sq, hr]; norm_num
          have hne_pr_qr : ∀ c : ℝ, c • (p - r) ≠ q - r := by
            apply hnprop (p - r) (q - r) q
            · rw [inner_sub_right, hqp, hqr]; ring
            · rw [inner_sub_right, real_inner_self_eq_norm_sq, hq, hqr]; norm_num
          have hne_p2r2' : ∀ c : ℝ, c • (p2 - q2) ≠ p2 - r2' := by
            have h1 : ⟪r2', p2⟫ = 0 := by rw [real_inner_comm]; exact hp2r2'
            have h2 : ⟪r2', q2⟫ = 0 := by rw [real_inner_comm]; exact hq2r2'
            apply hnprop (p2 - q2) (p2 - r2') r2'
            · rw [inner_sub_right, h1, h2]; ring
            · rw [inner_sub_right, h1, real_inner_self_eq_norm_sq, hr2'_norm]; norm_num
          have hne_p2plusr2' : ∀ c : ℝ, c • (p2 - q2) ≠ p2 + r2' := by
            have h1 : ⟪r2', p2⟫ = 0 := by rw [real_inner_comm]; exact hp2r2'
            have h2 : ⟪r2', q2⟫ = 0 := by rw [real_inner_comm]; exact hq2r2'
            apply hnprop (p2 - q2) (p2 + r2') r2'
            · rw [inner_sub_right, h1, h2]; ring
            · rw [inner_add_right, h1, real_inner_self_eq_norm_sq, hr2'_norm]; norm_num
          -- Coordonnées de `u` : `⟪p,u⟫ = ⟪q,u⟫ = ⟪r,u⟫`, donc `u` est sur les trois
          -- cercles non-primés `x = y`, `x = z`, `y = z`.
          have hu_p : ⟪p, u⟫ = (Real.sqrt 3)⁻¹ := by
            rw [hu_def, real_inner_smul_right]
            simp only [inner_add_right, real_inner_self_eq_norm_sq, hp, hpq, hpr]
            norm_num
          have hu_q : ⟪q, u⟫ = (Real.sqrt 3)⁻¹ := by
            rw [hu_def, real_inner_smul_right]
            simp only [inner_add_right, real_inner_self_eq_norm_sq, hq, hqp, hqr]
            norm_num
          have hu_r : ⟪r, u⟫ = (Real.sqrt 3)⁻¹ := by
            rw [hu_def, real_inner_smul_right]
            simp only [inner_add_right, real_inner_self_eq_norm_sq, hr, hrp, hrq]
            norm_num
          have hu_C1 : ⟪p, u⟫ = ⟪q, u⟫ := hu_p.trans hu_q.symm
          have hu_C2 : ⟪p, u⟫ = ⟪r, u⟫ := hu_p.trans hu_r.symm
          have hu_C3 : ⟪q, u⟫ = ⟪r, u⟫ := hu_q.trans hu_r.symm
          have hto_orth : ∀ X A B : E3, ⟪A, X⟫ = ⟪B, X⟫ → ⟪X, A - B⟫ = 0 := by
            intro X A B hAB
            rw [inner_sub_right, real_inner_comm A X, real_inner_comm B X, hAB]; ring
          have hto_orth' : ∀ X A B : E3, ⟪A, X⟫ = -⟪B, X⟫ → ⟪X, A + B⟫ = 0 := by
            intro X A B hAB
            rw [inner_add_right, real_inner_comm A X, real_inner_comm B X, hAB]; ring
          have hu_orth_pq : ⟪u, p - q⟫ = 0 := hto_orth u p q hu_C1
          have hu_orth_pr : ⟪u, p - r⟫ = 0 := hto_orth u p r hu_C2
          have hu_orth_qr : ⟪u, q - r⟫ = 0 := hto_orth u q r hu_C3
          -- Deux cercles non-primés distincts (parmi `x=y,x=z,y=z`) ne se coupent qu'en `±u`.
          have hCiCj_to_u : ∀ nA nB : E3, nA ≠ 0 → (∀ c : ℝ, c • nA ≠ nB) →
              ⟪u, nA⟫ = 0 → ⟪u, nB⟫ = 0 →
              ∀ X : E3, ‖X‖ = 1 → ⟪X, nA⟫ = 0 → ⟪X, nB⟫ = 0 → X = u ∨ X = -u :=
            fun nA nB hA0 hindep huA huB X hX hXA hXB =>
              unique_unit_orthogonal_to_pair hA0 hindep huA huB hu_norm hXA hXB hX
          -- Zéro de `h` sur `Γ ∩ Cᵢ` (i=1,2,3, non-primés) : via le Claim `hclaim_h`, ce zéro
          -- force la coordonnée `x2` à égaler `±z2` (les deux seules issues, car `M2 ≠ 0`).
          have hbin_of : ∀ X : E3, ‖X‖ = 1 → ⟪p2, X⟫ = ⟪q2, X⟫ → h X = 0 →
              ⟪p2, X⟫ = ⟪r2', X⟫ ∨ ⟪p2, X⟫ = -⟪r2', X⟫ := by
            intro X hX hXΓ hX0
            have hcl := hclaim_h X hX (Or.inl hXΓ)
            rw [hX0, hr2'M2] at hcl
            have hfact : M2 * (⟪p2, X⟫ - ⟪r2', X⟫) * (⟪p2, X⟫ + ⟪r2', X⟫) = 0 := by
              linear_combination -hcl
            rcases mul_eq_zero.mp hfact with h | h
            · rcases mul_eq_zero.mp h with h1 | h1
              · exact absurd h1 hM2pos.ne'
              · left; linarith [h1]
            · right; linarith [h]
          obtain ⟨A1, hA1_norm, hA1Γ0, hA1C10⟩ := exists_unit_orthogonal_to_pair (p2 - q2) (p - q)
          have hA1_Γ : ⟪p2, A1⟫ = ⟪q2, A1⟫ := by
            have hz : ⟪p2 - q2, A1⟫ = 0 := by rw [real_inner_comm]; exact hA1Γ0
            rw [inner_sub_left] at hz; linarith [hz]
          have hA1_cond : ⟪p, A1⟫ = ⟪q, A1⟫ := by
            have hz : ⟪p - q, A1⟫ = 0 := by rw [real_inner_comm]; exact hA1C10
            rw [inner_sub_left] at hz; linarith [hz]
          have hA1_zero : h A1 = 0 := hh_zero A1 hA1_norm (Or.inl hA1_cond)
          have hA1_bin := hbin_of A1 hA1_norm hA1_Γ hA1_zero
          obtain ⟨A2, hA2_norm, hA2Γ0, hA2C0⟩ := exists_unit_orthogonal_to_pair (p2 - q2) (p - r)
          have hA2_Γ : ⟪p2, A2⟫ = ⟪q2, A2⟫ := by
            have hz : ⟪p2 - q2, A2⟫ = 0 := by rw [real_inner_comm]; exact hA2Γ0
            rw [inner_sub_left] at hz; linarith [hz]
          have hA2_cond : ⟪p, A2⟫ = ⟪r, A2⟫ := by
            have hz : ⟪p - r, A2⟫ = 0 := by rw [real_inner_comm]; exact hA2C0
            rw [inner_sub_left] at hz; linarith [hz]
          have hA2_zero : h A2 = 0 := hh_zero A2 hA2_norm (Or.inr (Or.inr (Or.inl hA2_cond)))
          have hA2_bin := hbin_of A2 hA2_norm hA2_Γ hA2_zero
          obtain ⟨A3, hA3_norm, hA3Γ0, hA3C0⟩ := exists_unit_orthogonal_to_pair (p2 - q2) (q - r)
          have hA3_Γ : ⟪p2, A3⟫ = ⟪q2, A3⟫ := by
            have hz : ⟪p2 - q2, A3⟫ = 0 := by rw [real_inner_comm]; exact hA3Γ0
            rw [inner_sub_left] at hz; linarith [hz]
          have hA3_cond : ⟪q, A3⟫ = ⟪r, A3⟫ := by
            have hz : ⟪q - r, A3⟫ = 0 := by rw [real_inner_comm]; exact hA3C0
            rw [inner_sub_left] at hz; linarith [hz]
          have hA3_zero : h A3 = 0 :=
            hh_zero A3 hA3_norm (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl hA3_cond)))))
          have hA3_bin := hbin_of A3 hA3_norm hA3_Γ hA3_zero
          -- Si deux `Aᵢ` tombent dans la même "case" (`x2=z2` ou `x2=-z2`), l'unicité
          -- (`unique_unit_orthogonal_to_pair`, appliquée à `Γ` et au cercle-case primé)
          -- force `Aᵢ = ±Aⱼ`.
          have hmatchL : ∀ X Y : E3, ‖X‖ = 1 → ‖Y‖ = 1 → ⟪p2, X⟫ = ⟪q2, X⟫ → ⟪p2, Y⟫ = ⟪q2, Y⟫ →
              ⟪p2, X⟫ = ⟪r2', X⟫ → ⟪p2, Y⟫ = ⟪r2', Y⟫ → X = Y ∨ X = -Y := by
            intro X Y hX hY hXΓ hYΓ hXb hYb
            exact unique_unit_orthogonal_to_pair hp2q2_ne0 hne_p2r2'
              (hto_orth Y p2 q2 hYΓ) (hto_orth Y p2 r2' hYb) hY
              (hto_orth X p2 q2 hXΓ) (hto_orth X p2 r2' hXb) hX
          have hmatchR : ∀ X Y : E3, ‖X‖ = 1 → ‖Y‖ = 1 → ⟪p2, X⟫ = ⟪q2, X⟫ → ⟪p2, Y⟫ = ⟪q2, Y⟫ →
              ⟪p2, X⟫ = -⟪r2', X⟫ → ⟪p2, Y⟫ = -⟪r2', Y⟫ → X = Y ∨ X = -Y := by
            intro X Y hX hY hXΓ hYΓ hXb hYb
            exact unique_unit_orthogonal_to_pair hp2q2_ne0 hne_p2plusr2'
              (hto_orth Y p2 q2 hYΓ) (hto_orth' Y p2 r2' hYb) hY
              (hto_orth X p2 q2 hXΓ) (hto_orth' X p2 r2' hXb) hX
          have hmatch : (A1 = A2 ∨ A1 = -A2) ∨ (A1 = A3 ∨ A1 = -A3) ∨ (A2 = A3 ∨ A2 = -A3) := by
            rcases hA1_bin with hb1 | hb1 <;> rcases hA2_bin with hb2 | hb2 <;>
              rcases hA3_bin with hb3 | hb3
            · exact Or.inl (hmatchL A1 A2 hA1_norm hA2_norm hA1_Γ hA2_Γ hb1 hb2)
            · exact Or.inl (hmatchL A1 A2 hA1_norm hA2_norm hA1_Γ hA2_Γ hb1 hb2)
            · exact Or.inr (Or.inl (hmatchL A1 A3 hA1_norm hA3_norm hA1_Γ hA3_Γ hb1 hb3))
            · exact Or.inr (Or.inr (hmatchR A2 A3 hA2_norm hA3_norm hA2_Γ hA3_Γ hb2 hb3))
            · exact Or.inr (Or.inr (hmatchL A2 A3 hA2_norm hA3_norm hA2_Γ hA3_Γ hb2 hb3))
            · exact Or.inr (Or.inl (hmatchR A1 A3 hA1_norm hA3_norm hA1_Γ hA3_Γ hb1 hb3))
            · exact Or.inl (hmatchR A1 A2 hA1_norm hA2_norm hA1_Γ hA2_Γ hb1 hb2)
            · exact Or.inl (hmatchR A1 A2 hA1_norm hA2_norm hA1_Γ hA2_Γ hb1 hb2)
          have hA2_orth_pr : ⟪A2, p - r⟫ = 0 := hto_orth A2 p r hA2_cond
          have hA3_orth_qr : ⟪A3, q - r⟫ = 0 := hto_orth A3 q r hA3_cond
          have hu_in_Γ : ⟪p2, u⟫ = ⟪q2, u⟫ := by
            rcases hmatch with h12 | h13 | h23
            · have hA1u : A1 = u ∨ A1 = -u := by
                apply hCiCj_to_u (p - q) (p - r) hpq_ne0 hne_pq_pr hu_orth_pq hu_orth_pr A1 hA1_norm
                  (hto_orth A1 p q hA1_cond)
                rcases h12 with heq | heq
                · rw [heq]; exact hA2_orth_pr
                · rw [heq, inner_neg_left, hA2_orth_pr]; ring
              rcases hA1u with heq | heq
              · rw [← heq]; exact hA1_Γ
              · have : ⟪p2, -u⟫ = ⟪q2, -u⟫ := heq ▸ hA1_Γ
                rw [inner_neg_right, inner_neg_right] at this; linarith [this]
            · have hA1u : A1 = u ∨ A1 = -u := by
                apply hCiCj_to_u (p - q) (q - r) hpq_ne0 hne_pq_qr hu_orth_pq hu_orth_qr A1 hA1_norm
                  (hto_orth A1 p q hA1_cond)
                rcases h13 with heq | heq
                · rw [heq]; exact hA3_orth_qr
                · rw [heq, inner_neg_left, hA3_orth_qr]; ring
              rcases hA1u with heq | heq
              · rw [← heq]; exact hA1_Γ
              · have : ⟪p2, -u⟫ = ⟪q2, -u⟫ := heq ▸ hA1_Γ
                rw [inner_neg_right, inner_neg_right] at this; linarith [this]
            · have hA2u : A2 = u ∨ A2 = -u := by
                apply hCiCj_to_u (p - r) (q - r) hpr_ne0 hne_pr_qr hu_orth_pr hu_orth_qr A2 hA2_norm
                  hA2_orth_pr
                rcases h23 with heq | heq
                · rw [heq]; exact hA3_orth_qr
                · rw [heq, inner_neg_left, hA3_orth_qr]; ring
              rcases hA2u with heq | heq
              · rw [← heq]; exact hA2_Γ
              · have : ⟪p2, -u⟫ = ⟪q2, -u⟫ := heq ▸ hA2_Γ
                rw [inner_neg_right, inner_neg_right] at this; linarith [this]
          -- **H9d.** Même argument pour `w := (p-q-r)/√3`, sur les cercles non-primés
          -- `y=z` (réutilise `A3`), `x=-y`, `x=-z`.
          have hqr_ne0 : (q - r : E3) ≠ 0 := sub_ne_zero.mpr (hvne q r hq hr hqr)
          have hpq_plus_ne0 : (p + q : E3) ≠ 0 := by
            intro hcontra
            have h1 : ⟪p, p + q⟫ = 0 := by rw [hcontra, inner_zero_right]
            rw [inner_add_right, real_inner_self_eq_norm_sq, hp, hpq] at h1
            norm_num at h1
          have hne_qr_pq : ∀ c : ℝ, c • (q - r) ≠ p + q := by
            apply hnprop (q - r) (p + q) p
            · rw [inner_sub_right, hpq, hpr]; ring
            · rw [inner_add_right, real_inner_self_eq_norm_sq, hp, hpq]; norm_num
          have hne_qr_pr : ∀ c : ℝ, c • (q - r) ≠ p + r := by
            apply hnprop (q - r) (p + r) p
            · rw [inner_sub_right, hpq, hpr]; ring
            · rw [inner_add_right, real_inner_self_eq_norm_sq, hp, hpr]; norm_num
          have hne_pq_pr' : ∀ c : ℝ, c • (p + q) ≠ p + r := by
            apply hnprop (p + q) (p + r) r
            · rw [inner_add_right, hrp, hrq]; ring
            · rw [inner_add_right, hrp, real_inner_self_eq_norm_sq, hr]; norm_num
          have hw_p : ⟪p, w⟫ = (Real.sqrt 3)⁻¹ := by
            rw [hw_def, real_inner_smul_right]
            simp only [inner_sub_right, real_inner_self_eq_norm_sq, hp, hpq, hpr]
            ring
          have hw_q : ⟪q, w⟫ = -(Real.sqrt 3)⁻¹ := by
            rw [hw_def, real_inner_smul_right]
            simp only [inner_sub_right, real_inner_self_eq_norm_sq, hq, hqp, hqr]
            ring
          have hw_r : ⟪r, w⟫ = -(Real.sqrt 3)⁻¹ := by
            rw [hw_def, real_inner_smul_right]
            simp only [inner_sub_right, real_inner_self_eq_norm_sq, hr, hrp, hrq]
            ring
          have hw_C3 : ⟪q, w⟫ = ⟪r, w⟫ := hw_q.trans hw_r.symm
          have hw_C4 : ⟪p, w⟫ = -⟪q, w⟫ := by rw [hw_p, hw_q]; ring
          have hw_C5 : ⟪p, w⟫ = -⟪r, w⟫ := by rw [hw_p, hw_r]; ring
          have hw_orth_qr : ⟪w, q - r⟫ = 0 := hto_orth w q r hw_C3
          have hw_orth_pq : ⟪w, p + q⟫ = 0 := hto_orth' w p q hw_C4
          have hw_orth_pr : ⟪w, p + r⟫ = 0 := hto_orth' w p r hw_C5
          have hCiCj_to_w : ∀ nA nB : E3, nA ≠ 0 → (∀ c : ℝ, c • nA ≠ nB) →
              ⟪w, nA⟫ = 0 → ⟪w, nB⟫ = 0 →
              ∀ X : E3, ‖X‖ = 1 → ⟪X, nA⟫ = 0 → ⟪X, nB⟫ = 0 → X = w ∨ X = -w :=
            fun nA nB hA0 hindep hwA hwB X hX hXA hXB =>
              unique_unit_orthogonal_to_pair hA0 hindep hwA hwB hw_norm hXA hXB hX
          obtain ⟨B2, hB2_norm, hB2Γ0, hB2C0⟩ := exists_unit_orthogonal_to_pair (p2 - q2) (p + q)
          have hB2_Γ : ⟪p2, B2⟫ = ⟪q2, B2⟫ := by
            have hz : ⟪p2 - q2, B2⟫ = 0 := by rw [real_inner_comm]; exact hB2Γ0
            rw [inner_sub_left] at hz; linarith [hz]
          have hB2_cond : ⟪p, B2⟫ = -⟪q, B2⟫ := by
            have hz : ⟪p + q, B2⟫ = 0 := by rw [real_inner_comm]; exact hB2C0
            rw [inner_add_left] at hz; linarith [hz]
          have hB2_zero : h B2 = 0 := hh_zero B2 hB2_norm (Or.inr (Or.inl hB2_cond))
          have hB2_bin := hbin_of B2 hB2_norm hB2_Γ hB2_zero
          obtain ⟨B3, hB3_norm, hB3Γ0, hB3C0⟩ := exists_unit_orthogonal_to_pair (p2 - q2) (p + r)
          have hB3_Γ : ⟪p2, B3⟫ = ⟪q2, B3⟫ := by
            have hz : ⟪p2 - q2, B3⟫ = 0 := by rw [real_inner_comm]; exact hB3Γ0
            rw [inner_sub_left] at hz; linarith [hz]
          have hB3_cond : ⟪p, B3⟫ = -⟪r, B3⟫ := by
            have hz : ⟪p + r, B3⟫ = 0 := by rw [real_inner_comm]; exact hB3C0
            rw [inner_add_left] at hz; linarith [hz]
          have hB3_zero : h B3 = 0 :=
            hh_zero B3 hB3_norm (Or.inr (Or.inr (Or.inr (Or.inl hB3_cond))))
          have hB3_bin := hbin_of B3 hB3_norm hB3_Γ hB3_zero
          have hmatchw : (A3 = B2 ∨ A3 = -B2) ∨ (A3 = B3 ∨ A3 = -B3) ∨ (B2 = B3 ∨ B2 = -B3) := by
            rcases hA3_bin with hb3 | hb3 <;> rcases hB2_bin with hb2 | hb2 <;>
              rcases hB3_bin with hb3' | hb3'
            · exact Or.inl (hmatchL A3 B2 hA3_norm hB2_norm hA3_Γ hB2_Γ hb3 hb2)
            · exact Or.inl (hmatchL A3 B2 hA3_norm hB2_norm hA3_Γ hB2_Γ hb3 hb2)
            · exact Or.inr (Or.inl (hmatchL A3 B3 hA3_norm hB3_norm hA3_Γ hB3_Γ hb3 hb3'))
            · exact Or.inr (Or.inr (hmatchR B2 B3 hB2_norm hB3_norm hB2_Γ hB3_Γ hb2 hb3'))
            · exact Or.inr (Or.inr (hmatchL B2 B3 hB2_norm hB3_norm hB2_Γ hB3_Γ hb2 hb3'))
            · exact Or.inr (Or.inl (hmatchR A3 B3 hA3_norm hB3_norm hA3_Γ hB3_Γ hb3 hb3'))
            · exact Or.inl (hmatchR A3 B2 hA3_norm hB2_norm hA3_Γ hB2_Γ hb3 hb2)
            · exact Or.inl (hmatchR A3 B2 hA3_norm hB2_norm hA3_Γ hB2_Γ hb3 hb2)
          have hB2_orth_pq : ⟪B2, p + q⟫ = 0 := hto_orth' B2 p q hB2_cond
          have hB3_orth_pr : ⟪B3, p + r⟫ = 0 := hto_orth' B3 p r hB3_cond
          have hw_in_Γ : ⟪p2, w⟫ = ⟪q2, w⟫ := by
            rcases hmatchw with h12 | h13 | h23
            · have hA3w : A3 = w ∨ A3 = -w := by
                apply hCiCj_to_w (q - r) (p + q) hqr_ne0 hne_qr_pq hw_orth_qr hw_orth_pq A3
                  hA3_norm hA3_orth_qr
                rcases h12 with heq | heq
                · rw [heq]; exact hB2_orth_pq
                · rw [heq, inner_neg_left, hB2_orth_pq]; ring
              rcases hA3w with heq | heq
              · rw [← heq]; exact hA3_Γ
              · have : ⟪p2, -w⟫ = ⟪q2, -w⟫ := heq ▸ hA3_Γ
                rw [inner_neg_right, inner_neg_right] at this; linarith [this]
            · have hA3w : A3 = w ∨ A3 = -w := by
                apply hCiCj_to_w (q - r) (p + r) hqr_ne0 hne_qr_pr hw_orth_qr hw_orth_pr A3
                  hA3_norm hA3_orth_qr
                rcases h13 with heq | heq
                · rw [heq]; exact hB3_orth_pr
                · rw [heq, inner_neg_left, hB3_orth_pr]; ring
              rcases hA3w with heq | heq
              · rw [← heq]; exact hA3_Γ
              · have : ⟪p2, -w⟫ = ⟪q2, -w⟫ := heq ▸ hA3_Γ
                rw [inner_neg_right, inner_neg_right] at this; linarith [this]
            · have hB2w : B2 = w ∨ B2 = -w := by
                apply hCiCj_to_w (p + q) (p + r) hpq_plus_ne0 hne_pq_pr' hw_orth_pq hw_orth_pr B2
                  hB2_norm hB2_orth_pq
                rcases h23 with heq | heq
                · rw [heq]; exact hB3_orth_pr
                · rw [heq, inner_neg_left, hB3_orth_pr]; ring
              rcases hB2w with heq | heq
              · rw [← heq]; exact hB2_Γ
              · have : ⟪p2, -w⟫ = ⟪q2, -w⟫ := heq ▸ hB2_Γ
                rw [inner_neg_right, inner_neg_right] at this; linarith [this]
          -- **H9e.** `u ≠ ±w` (indépendants) ; `u,w ∈ span{u,w} = (span{p2-q2})ᗮ` (rangs 2 = 2)
          -- contient `r2'` (trivialement orthogonal à `p2-q2`), qui hérite donc de `y=z`
          -- (satisfaite par `u` et `w`) par linéarité — contredit `h r2' = -M2 ≠ 0`.
          have huw_inner : ⟪u, w⟫ = -(3 : ℝ)⁻¹ := by
            rw [hu_def, hw_def, real_inner_smul_left, real_inner_smul_right]
            have hinner : ⟪p + q + r, p - q - r⟫ = -1 := by
              simp only [inner_add_left, inner_sub_right, real_inner_self_eq_norm_sq, hp, hq, hr,
                hpq, hpr, hqr, hqp, hrp, hrq]
              ring
            have hinv_sq : (Real.sqrt 3)⁻¹ * (Real.sqrt 3)⁻¹ = (3 : ℝ)⁻¹ := by
              rw [← mul_inv, h3sq]
            rw [hinner, show (Real.sqrt 3)⁻¹ * ((Real.sqrt 3)⁻¹ * (-1))
              = (Real.sqrt 3)⁻¹ * (Real.sqrt 3)⁻¹ * (-1) from by ring, hinv_sq]
            ring
          -- `u`, `w` deviennent opaques : leur définition explicite (combinaison de
          -- p,q,r) ne sert plus, seules leurs propriétés déjà établies sont utilisées
          -- (évite un sur-filtrage de `rw` via le dépliage de `set`, CLAUDE.md).
          clear_value u w
          have hune_w : u ≠ w := by
            intro heq
            rw [← heq, real_inner_self_eq_norm_sq, hu_norm] at huw_inner
            norm_num at huw_inner
          have hune_negw : u ≠ -w := by
            intro heq
            rw [heq, inner_neg_left, real_inner_self_eq_norm_sq, hw_norm] at huw_inner
            norm_num at huw_inner
          have hu_ne0 : u ≠ 0 := by
            intro hh; rw [hh, norm_zero] at hu_norm; norm_num at hu_norm
          have huw_ne : ∀ c : ℝ, c • u ≠ w := by
            intro c hc
            have hcabs : |c| = 1 := by
              have hnorm : ‖c • u‖ = 1 := by rw [hc]; exact hw_norm
              rwa [norm_smul, Real.norm_eq_abs, hu_norm, mul_one] at hnorm
            rcases (abs_eq (by norm_num : (0:ℝ) ≤ 1)).mp hcabs with h1 | h1
            · rw [h1, one_smul] at hc; exact hune_w hc
            · rw [h1, neg_one_smul] at hc
              exact hune_negw (by rw [← hc, neg_neg])
          have huw_indep : LinearIndependent ℝ ![u, w] := (LinearIndependent.pair_iff' hu_ne0).mpr huw_ne
          set K : Submodule ℝ E3 := (Submodule.span ℝ ({p2 - q2} : Set E3))ᗮ with hK_def
          have hKfin : Module.finrank ℝ K = 2 := by
            have h1 : Module.finrank ℝ (Submodule.span ℝ ({p2 - q2} : Set E3)) = 1 :=
              finrank_span_singleton hp2q2_ne0
            have hE3 : Module.finrank ℝ E3 = 3 := by simp
            have hsum : Module.finrank ℝ (Submodule.span ℝ ({p2 - q2} : Set E3)) +
                Module.finrank ℝ K = Module.finrank ℝ E3 :=
              Submodule.finrank_add_finrank_orthogonal _
            omega
          have hu_mem_K : u ∈ K := by
            rw [hK_def, Submodule.mem_orthogonal]
            intro y hy
            rw [Submodule.mem_span_singleton] at hy
            obtain ⟨c, hc⟩ := hy
            have hz : ⟪p2 - q2, u⟫ = 0 := by rw [inner_sub_left, hu_in_Γ]; ring
            rw [← hc, real_inner_smul_left, hz, mul_zero]
          have hw_mem_K : w ∈ K := by
            rw [hK_def, Submodule.mem_orthogonal]
            intro y hy
            rw [Submodule.mem_span_singleton] at hy
            obtain ⟨c, hc⟩ := hy
            have hz : ⟪p2 - q2, w⟫ = 0 := by rw [inner_sub_left, hw_in_Γ]; ring
            rw [← hc, real_inner_smul_left, hz, mul_zero]
          have hr2'_mem_K : r2' ∈ K := by
            rw [hK_def, Submodule.mem_orthogonal]
            intro y hy
            rw [Submodule.mem_span_singleton] at hy
            obtain ⟨c, hc⟩ := hy
            have hz : ⟪p2 - q2, r2'⟫ = 0 := by rw [inner_sub_left, hp2r2', hq2r2']; ring
            rw [← hc, real_inner_smul_left, hz, mul_zero]
          have hL_range : ({u, w} : Set E3) = Set.range ![u, w] := by
            ext x; simp [eq_comm, or_comm]
          have hLfin : Module.finrank ℝ (Submodule.span ℝ ({u, w} : Set E3)) = 2 := by
            rw [hL_range]
            have h := finrank_span_eq_card huw_indep
            simpa using h
          have hL_le_K : Submodule.span ℝ ({u, w} : Set E3) ≤ K := by
            rw [Submodule.span_le]
            intro x hx
            simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
            rcases hx with hx | hx
            · rw [hx]; exact hu_mem_K
            · rw [hx]; exact hw_mem_K
          have hLK_eq : Submodule.span ℝ ({u, w} : Set E3) = K :=
            Submodule.eq_of_le_of_finrank_eq hL_le_K (by rw [hLfin, hKfin])
          have hr2'_mem_L : r2' ∈ Submodule.span ℝ ({u, w} : Set E3) := by
            rw [hLK_eq]; exact hr2'_mem_K
          obtain ⟨a, b, hab⟩ := Submodule.mem_span_pair.mp hr2'_mem_L
          have hr2'_C3 : ⟪q, r2'⟫ = ⟪r, r2'⟫ := by
            rw [← hab, inner_add_right, inner_add_right, real_inner_smul_right,
              real_inner_smul_right, real_inner_smul_right, real_inner_smul_right, hu_C3, hw_C3]
          have hr2'_zero : h r2' = 0 :=
            hh_zero r2' hr2'_norm (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl hr2'_C3)))))
          exfalso
          rw [hr2'M2] at hr2'_zero
          linarith [hr2'_zero, hM2pos]

end
end Gleason

-- Vérification (M2 complet) : `#print axioms Gleason.frameFunction_regular` donne
-- `propext, Classical.choice, Quot.sound` uniquement (aucun axiome ajouté).
