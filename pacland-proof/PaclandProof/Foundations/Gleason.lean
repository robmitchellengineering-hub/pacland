import Mathlib
import PaclandProof.Foundations.Cauchy
import PaclandProof.Foundations.SelfDual

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Gleason's theorem — step 1: the quadratic-form reconstruction

Gleason's theorem (finite-dimensional) says a frame function on dimension ≥ 3
is the Born rule. Its proof has a hard analytic step (continuity) and an
algebraic step: once the frame function is extended to a homogeneous degree-2
function `F` satisfying the parallelogram law, `F` **is** a quadratic form.

This file kernel-checks the algebraic core, rung by rung. Rung 1 (here): the
polarization `B(v,w) = (F(v+w) − F(v−w))/4` recovers `F` on the diagonal —
`B(v,v) = F(v)` — under homogeneity alone. Rung 2 (next) shows `B` is bilinear
from the parallelogram law, so `F(v) = vᵀ M v` for a symmetric `M`.
-/

noncomputable section

open BigOperators

namespace Gleason

/-- The polarization of `F`: `B(v,w) = (F(v+w) − F(v−w))/4`. -/
def polarization (F : (Fin 2 → ℝ) → ℝ) (v w : Fin 2 → ℝ) : ℝ :=
  (F (v + w) - F (v - w)) / 4

/-- Homogeneity degree 2 forces `F 0 = 0` (take `c = 0`). -/
theorem F_zero (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v) :
    F 0 = 0 := by
  have h := hhom 0 0
  norm_num at h
  exact h

/-- The polarization recovers `F` on the diagonal: `B(v,v) = F(v)`. -/
theorem polarization_recovers (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (v : Fin 2 → ℝ) :
    polarization F v v = F v := by
  unfold polarization
  have hsum : v + v = (2 : ℝ) • v := by
    ext i
    simp
    ring
  have hdiff : v - v = 0 := by
    ext i
    simp
  rw [hsum, hdiff]
  have h2 : F ((2 : ℝ) • v) = 4 * F v := by
    have h := hhom 2 v
    norm_num at h
    exact h
  have h0 : F 0 = 0 := F_zero F hhom
  rw [h2, h0]
  ring

/-- Homogeneity degree 2 forces evenness: `F(-v) = F(v)` (take `c = -1`). -/
theorem F_even (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (v : Fin 2 → ℝ) : F (-v) = F v := by
  have h := hhom (-1) v
  have hsmul : (-1 : ℝ) • v = -v := by
    ext i
    simp
  rw [hsmul] at h
  norm_num at h
  exact h

/-- The polarization is symmetric: `B(v,w) = B(w,v)`. -/
theorem polarization_symm (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (v w : Fin 2 → ℝ) : polarization F v w = polarization F w v := by
  unfold polarization
  have h1 : F (v + w) = F (w + v) := by rw [add_comm]
  have h2 : F (v - w) = F (w - v) := by
    have hnegg : v - w = -(w - v) := by
      ext i
      simp
    rw [hnegg]
    exact F_even F hhom (w - v)
  rw [h1, h2]

/-- The polarization vanishes on the zero vector: `B(0,w) = 0`. -/
theorem polarization_zero (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (w : Fin 2 → ℝ) : polarization F 0 w = 0 := by
  unfold polarization
  have h1 : F (0 + w) = F w := by rw [zero_add]
  have h2 : F (0 - w) = F w := by
    rw [zero_sub]
    exact F_even F hhom w
  rw [h1, h2]
  ring

/-- The parallelogram law descends to the polarization:
`B(x+y, z) + B(x−y, z) = 2·B(x, z)`. Proved by applying the parallelogram law
twice (with `x+z` and `x−z`) and telescoping. -/
theorem polarization_parallelogram (F : (Fin 2 → ℝ) → ℝ)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (x y z : Fin 2 → ℝ) :
    polarization F (x + y) z + polarization F (x - y) z = 2 * polarization F x z := by
  unfold polarization
  have h1 : F (x + y + z) + F (x - y + z) = 2 * F (x + z) + 2 * F y := by
    have h := hpar (x + z) y
    have hA : x + z + y = x + y + z := by abel
    have hB : x + z - y = x - y + z := by abel
    rwa [hA, hB] at h
  have h2 : F (x + y - z) + F (x - y - z) = 2 * F (x - z) + 2 * F y := by
    have h := hpar (x - z) y
    have hA : x - z + y = x + y - z := by abel
    have hB : x - z - y = x - y - z := by abel
    rwa [hA, hB] at h
  nlinarith [h1, h2]

/-- The polarization doubles: `B(2x, z) = 2·B(x, z)`. -/
theorem polarization_double (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (x z : Fin 2 → ℝ) :
    polarization F ((2 : ℝ) • x) z = 2 * polarization F x z := by
  have h := polarization_parallelogram F hpar x x z
  have hsum : x + x = (2 : ℝ) • x := by
    ext i
    simp
    ring
  have hdiff : x - x = 0 := by
    ext i
    simp
  have hz : polarization F 0 z = 0 := polarization_zero F hhom z
  rw [hsum, hdiff, hz] at h
  simpa using h

/-- The polarization is additive in its first argument:
`B(x+y, z) = B(x, z) + B(y, z)`. -/
theorem polarization_add (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (x y z : Fin 2 → ℝ) :
    polarization F (x + y) z = polarization F x z + polarization F y z := by
  have h := polarization_parallelogram F hpar (x + y) (x - y) z
  have hA : (x + y) + (x - y) = (2 : ℝ) • x := by
    ext i
    simp
    ring
  have hB : (x + y) - (x - y) = (2 : ℝ) • y := by
    ext i
    simp
    ring
  rw [hA, hB] at h
  have hdx : polarization F ((2 : ℝ) • x) z = 2 * polarization F x z :=
    polarization_double F hhom hpar x z
  have hdy : polarization F ((2 : ℝ) • y) z = 2 * polarization F y z :=
    polarization_double F hhom hpar y z
  rw [hdx, hdy] at h
  nlinarith

/-- The diagonal is ℝ-homogeneous: `B(c·v, v) = c·B(v, v)`. This is the clean half
of the Jordan–von Neumann ℝ-linearity step, and follows from `F`'s homogeneity
alone (via `F((c±1)·v) = (c±1)² F v`). -/
theorem polarization_diag_hom (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (c : ℝ) (v : Fin 2 → ℝ) :
    polarization F (c • v) v = c * polarization F v v := by
  have hp : polarization F v v = F v := polarization_recovers F hhom v
  rw [hp]
  unfold polarization
  have hplus : c • v + v = (c + 1) • v := by
    ext i
    simp
    ring
  have hminus : c • v - v = (c - 1) • v := by
    ext i
    simp
    ring
  rw [hplus, hminus]
  have h1 : F ((c + 1) • v) = (c + 1) ^ 2 * F v := hhom (c + 1) v
  have h2 : F ((c - 1) • v) = (c - 1) ^ 2 * F v := hhom (c - 1) v
  rw [h1, h2]
  ring

/-- The polarization is `ℕ`-homogeneous in its first argument:
`B(n·v, w) = n·B(v, w)`. This is the seed of `ℚ`-linearity (then `ℝ`-linearity by
a regularity bound — the Jordan–von Neumann step). -/
theorem polarization_nsmul (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (n : ℕ) (v w : Fin 2 → ℝ) :
    polarization F (n • v) w = (n : ℝ) * polarization F v w := by
  induction n with
  | zero =>
      have hz : (0 : ℕ) • v = 0 := by rfl
      rw [hz]
      have h0 : polarization F 0 w = 0 := polarization_zero F hhom w
      rw [h0]
      norm_num
  | succ n ih =>
      have hsucc : (n + 1) • v = n • v + v := rfl
      rw [hsucc]
      rw [polarization_add F hhom hpar (n • v) v w]
      rw [ih]
      norm_num [Nat.cast_add, Nat.cast_one]
      ring

/-- The standard basis vectors. -/
def e0 : Fin 2 → ℝ := ![1, 0]
def e1 : Fin 2 → ℝ := ![0, 1]

/-- Any vector is its coordinate expansion: `v = v₀·e₀ + v₁·e₁`. -/
theorem basis_expand (v : Fin 2 → ℝ) : v = v 0 • e0 + v 1 • e1 := by
  ext i
  fin_cases i <;> simp [e0, e1]

/-- The polarization is homogeneous in its second argument (from `hlin` + symmetry). -/
theorem polarization_smul_right (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hlin : ∀ (c : ℝ) (v w : Fin 2 → ℝ), polarization F (c • v) w = c * polarization F v w)
    (c : ℝ) (v w : Fin 2 → ℝ) :
    polarization F v (c • w) = c * polarization F v w := by
  rw [polarization_symm F hhom v (c • w)]
  rw [hlin c w v]
  rw [polarization_symm F hhom w v]

/-- The bilinear expansion of the diagonal: `B(x+y, x+y) = B(x,x) + 2·B(x,y) + B(y,y)`. -/
theorem polarization_expand_diag (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (x y : Fin 2 → ℝ) :
    polarization F (x + y) (x + y) = polarization F x x + 2 * polarization F x y + polarization F y y := by
  rw [polarization_add F hhom hpar x y (x + y)]
  have hx : polarization F x (x + y) = polarization F x x + polarization F x y := by
    rw [polarization_symm F hhom x (x + y)]
    rw [polarization_add F hhom hpar x y x]
    rw [polarization_symm F hhom y x]
  have hy : polarization F y (x + y) = polarization F x y + polarization F y y := by
    rw [polarization_symm F hhom y (x + y)]
    rw [polarization_add F hhom hpar x y y]
  rw [hx, hy]
  ring

/-- **Step 1, conditionally complete.** Given the ℝ-linearity of `B` (the one
remaining Jordan–von Neumann assumption, named here as `hlin`), `F` is the
quadratic form `v ↦ v₀²F(e₀) + 2v₀v₁·B(e₀,e₁) + v₁²F(e₁)`. -/
theorem quadratic_form (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hlin : ∀ (c : ℝ) (v w : Fin 2 → ℝ), polarization F (c • v) w = c * polarization F v w)
    (v : Fin 2 → ℝ) :
    F v = (v 0) ^ 2 * F e0 + 2 * v 0 * v 1 * polarization F e0 e1 + (v 1) ^ 2 * F e1 := by
  rw [← polarization_recovers F hhom v]
  conv_lhs => rw [basis_expand v]
  rw [polarization_expand_diag F hhom hpar (v 0 • e0) (v 1 • e1)]
  rw [hlin (v 0) e0 (v 0 • e0), hlin (v 0) e0 (v 1 • e1), hlin (v 1) e1 (v 1 • e1)]
  rw [polarization_smul_right F hhom hlin (v 0) e0 e0, polarization_smul_right F hhom hlin (v 1) e0 e1, polarization_smul_right F hhom hlin (v 1) e1 e1]
  rw [polarization_recovers F hhom e0, polarization_recovers F hhom e1]
  simp [pow_two]
  ring

/-- The weak bound (a step toward ℝ-linearity): for `F ≥ 0`, `|B(v,w)| ≤ (F v + F w)/2`.
It is the local-boundedness that, with additivity, forces `B` ℝ-linear. -/
theorem polarization_bound (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hnonneg : ∀ v, 0 ≤ F v)
    (v w : Fin 2 → ℝ) :
    |polarization F v w| ≤ (F v + F w) / 2 := by
  unfold polarization
  rw [abs_div, abs_of_pos (by norm_num : 0 < (4 : ℝ))]
  have habs : |F (v + w) - F (v - w)| ≤ F (v + w) + F (v - w) := by
    rw [abs_sub_le_iff]
    constructor
    · linarith [hnonneg (v - w)]
    · linarith [hnonneg (v + w)]
  have htotal : F (v + w) + F (v - w) = 2 * F v + 2 * F w := hpar v w
  calc
    |F (v + w) - F (v - w)| / 4 ≤ (F (v + w) + F (v - w)) / 4 :=
      div_le_div_of_nonneg_right habs (by norm_num)
    _ = (F v + F w) / 2 := by rw [htotal]; ring

/-- **The ℝ-linearity of `B`** (the Jordan–von Neumann step, closed). `F ≥ 0`
gives the weak bound, so `c ↦ B(c·v, w)` is additive and bounded on `[-1,1]`,
hence ℝ-linear by Cauchy's equation. -/
theorem polarization_linear (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hnonneg : ∀ v, 0 ≤ F v)
    (c : ℝ) (v w : Fin 2 → ℝ) :
    polarization F (c • v) w = c * polarization F v w := by
  have hadd_map : ∀ (x y : ℝ), polarization F ((x + y) • v) w =
      polarization F (x • v) w + polarization F (y • v) w := by
    intro x y
    rw [add_smul x y v]
    exact polarization_add F hhom hpar (x • v) (y • v) w
  have hbounded : ∃ M : ℝ, ∀ (x : ℝ), |x| ≤ 1 → |polarization F (x • v) w| ≤ M := by
    refine ⟨(F v + F w) / 2, ?_⟩
    intro x hx
    have hb := polarization_bound F hhom hpar hnonneg (x • v) w
    rw [hhom x v] at hb
    have hxabs : -1 ≤ x ∧ x ≤ 1 := abs_le.mp hx
    have hx2 : x ^ 2 ≤ 1 := by nlinarith [hxabs.1, hxabs.2]
    have hxf : x ^ 2 * F v ≤ F v := by
      have := mul_le_mul_of_nonneg_right hx2 (hnonneg v)
      simpa using this
    linarith
  have hlin := Cauchy.additive_linear_of_bounded (fun c => polarization F (c • v) w) hadd_map hbounded
  have hc := hlin c
  simpa [one_smul] using hc

/-- **Step 1, unconditionally closed.** From `H` (homogeneity) + `P` (parallelogram)
+ `F ≥ 0`, `F` is the quadratic form `v ↦ v₀²F(e₀) + 2v₀v₁·B(e₀,e₁) + v₁²F(e₁)` —
the `ℝ`-linearity is no longer an assumption. -/
theorem quadratic_form_of_nonneg (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hnonneg : ∀ v, 0 ≤ F v)
    (v : Fin 2 → ℝ) :
    F v = (v 0) ^ 2 * F e0 + 2 * v 0 * v 1 * polarization F e0 e1 + (v 1) ^ 2 * F e1 := by
  exact quadratic_form F hhom hpar (polarization_linear F hhom hpar hnonneg) v

/-- The density matrix determined by `F` on the standard basis. -/
def densityMatrix (F : (Fin 2 → ℝ) → ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![F e0, polarization F e0 e1; polarization F e0 e1, F e1]

/-- **Step 3 (assembly), the Born-rule identity.** `F(v) = Tr(ρ · vvᵀ)` where `ρ`
is the density matrix above. -/
theorem born_rule (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hnonneg : ∀ v, 0 ≤ F v)
    (v : Fin 2 → ℝ) :
    F v = SelfDual.trProd (densityMatrix F) (SelfDual.outer v) := by
  rw [SelfDual.trProd_outer]
  rw [quadratic_form_of_nonneg F hhom hpar hnonneg v]
  simp [densityMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_two, sq]
  ring

/-- The trace of the density matrix is `F e₀ + F e₁` (so a *frame* function — one
that sums to `1` over the frame `{e₀, e₁}` — gives `Tr ρ = 1`). -/
theorem densityMatrix_trace (F : (Fin 2 → ℝ) → ℝ) :
    (densityMatrix F).trace = F e0 + F e1 := by
  simp [densityMatrix, Matrix.trace, Fin.sum_univ_two]

/-- The quadratic expansion along a line: `F(v + t·w) = F v + 2t·B(v,w) + t²·F w`
(the bilinear form is ℝ-linear now, so the discriminant argument opens). -/
theorem F_add_smul (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hnonneg : ∀ v, 0 ≤ F v)
    (v w : Fin 2 → ℝ) (t : ℝ) :
    F (v + t • w) = F v + 2 * t * polarization F v w + t ^ 2 * F w := by
  have hlin : ∀ (c : ℝ) (v w : Fin 2 → ℝ), polarization F (c • v) w = c * polarization F v w :=
    polarization_linear F hhom hpar hnonneg
  have htw : polarization F (t • w) (t • w) = t ^ 2 * F w := by
    rw [hlin t w (t • w)]
    rw [polarization_smul_right F hhom hlin t w w]
    rw [polarization_recovers F hhom w]
    ring
  calc
    F (v + t • w) = polarization F (v + t • w) (v + t • w) := by
      exact (polarization_recovers F hhom (v + t • w)).symm
    _ = polarization F v v + 2 * polarization F v (t • w) + polarization F (t • w) (t • w) := by
      exact polarization_expand_diag F hhom hpar v (t • w)
    _ = F v + 2 * t * polarization F v w + t ^ 2 * F w := by
      rw [polarization_recovers F hhom v, htw]
      rw [polarization_smul_right F hhom hlin t v w]
      ring

/-- **Cauchy–Schwarz for `B`.** `B(v,w)² ≤ F(v)·F(w)` from `F ≥ 0` and the
ℝ-bilinearity: `F(v + t·w) = F v + 2t·B + t²·F w ≥ 0` forces the discriminant
`B² − F(v)F(w) ≤ 0`. This is the self-duality core: `F ≥ 0` ⟹ the density matrix
is PSD. -/
theorem polarization_cauchy_schwarz (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hnonneg : ∀ v, 0 ≤ F v)
    (v w : Fin 2 → ℝ) :
    (polarization F v w) ^ 2 ≤ F v * F w := by
  by_cases hFw : F w = 0
  · have hBzero : polarization F v w = 0 := by
      by_contra hB
      let t : ℝ := -(F v + 1) / (2 * polarization F v w)
      have hnonneg_t : 0 ≤ F (v + t • w) := hnonneg (v + t • w)
      have hval : F (v + t • w) = -1 := by
        rw [F_add_smul F hhom hpar hnonneg v w t, hFw]
        simp only [mul_zero, add_zero]
        dsimp [t]
        field_simp [hB]
        ring
      linarith
    rw [hBzero, hFw]
    norm_num
  · have hFwpos : 0 < F w := lt_of_le_of_ne (hnonneg w) (Ne.symm hFw)
    let t : ℝ := - polarization F v w / F w
    have hnonneg_t : 0 ≤ F (v + t • w) := hnonneg (v + t • w)
    have hval : F (v + t • w) = F v - (polarization F v w) ^ 2 / F w := by
      rw [F_add_smul F hhom hpar hnonneg v w t]
      dsimp [t]
      field_simp [hFw]
      ring
    have hle : (polarization F v w) ^ 2 / F w ≤ F v := by
      nlinarith [hnonneg_t, hval]
    exact (div_le_iff₀ hFwpos).1 hle

/-- **The density matrix is PSD** (the self-duality close). `F ≥ 0` gives
`F e₀ ≥ 0`, `F e₁ ≥ 0`, and `det ρ = F(e₀)F(e₁) − B² ≥ 0` by Cauchy–Schwarz. -/
theorem densityMatrix_psd (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hnonneg : ∀ v, 0 ≤ F v) :
    Gleason2D.psd2 (densityMatrix F) := by
  constructor
  · simp [densityMatrix]
    exact hnonneg e0
  constructor
  · simp [densityMatrix]
    exact hnonneg e1
  · have hcs := polarization_cauchy_schwarz F hhom hpar hnonneg e0 e1
    simp [densityMatrix, Matrix.det_fin_two]
    nlinarith [hcs]

/-- **Step 3, the assembly, stated whole.** A positive homogeneous frame function
(`H` + `P` + `F ≥ 0`, plus the frame sum `F e₀ + F e₁ = 1`) is the Born rule with a
PSD trace-1 density matrix. -/
theorem gleason_assembly (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hnonneg : ∀ v, 0 ≤ F v)
    (hframe : F e0 + F e1 = 1) :
    (∀ v, F v = SelfDual.trProd (densityMatrix F) (SelfDual.outer v)) ∧
    Gleason2D.psd2 (densityMatrix F) ∧
    (densityMatrix F).trace = 1 := by
  constructor
  · exact born_rule F hhom hpar hnonneg
  constructor
  · exact densityMatrix_psd F hhom hpar hnonneg
  · rw [densityMatrix_trace F, hframe]

end Gleason

end
