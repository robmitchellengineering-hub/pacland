import Mathlib
import PaclandProof.QM.YMMassGap

/-!
# The volume-uniform continuum join — the open Clay rung (stated, not proved)

The honest reduction of the Yang–Mills mass gap:
    mass gap = OS3 (⟹ gap ≥ 0)  +  strong-coupling gap > 0 (Dobrushin)  +  THIS JOIN (open).

`OS3 ⟹ gap ≥ 0` (`CosPowers.heat_kernel_posdef`) gives a *non-negative* gap; the Dobrushin bound
(`YMMassGap.lean`) gives a *positive* gap on the finite lattice. The step nobody has proved is the
**join**: the strong-coupling positive gap must survive the continuum limit **uniformly in the
volume**. This file states that rung with its exact hypotheses and a falsifier — it does NOT prove it,
and it must not be read as progress. A candidate proof must, instantiated at the lattice numbers,
reproduce `m/√σ ≈ 3.2` and `m(β) = 25.28·e^(−1.182β)`.
-/

open Filter

noncomputable section

namespace QM

/-- **The volume-uniform continuum join** (the open Clay rung). `mGap β V` is the lattice spectral
gap (lattice units) at coupling β on volume V; `spacing β` is the lattice spacing `a(β)`. The join
asserts three things, all required:
1. the gap is positive on every finite volume (the Dobrushin/strong-coupling input);
2. at each coupling there is a *volume-independent* lower bound `c(β) ≤ mGap β V`;
3. the physical gap `Δ = lim_{β→∞} mGap β V / spacing β` is positive, *uniformly in V* (same Δ for
   every volume).
NOT proved. Stated with exact hypotheses + a falsifier. -/
def volumeUniformJoin (mGap : ℝ → ℝ → ℝ) (spacing : ℝ → ℝ) : Prop :=
  (∀ β V, 0 < mGap β V) ∧
  (∃ c : ℝ → ℝ, (∀ β, 0 < c β) ∧ (∀ β V, c β ≤ mGap β V)) ∧
  (∃ Δ : ℝ, 0 < Δ ∧ ∀ V, Tendsto (fun β => mGap β V / spacing β) atTop (nhds Δ))

/-- **The falsifier** of the volume-uniform join: any of the three clauses fails — a non-positive gap
on some (β, V); no positive volume-uniform lower bound; or no positive physical gap that is
volume-independent. This is the check that turns the join into a falsifiable claim. -/
def volumeUniformJoinFalsifier (mGap : ℝ → ℝ → ℝ) (spacing : ℝ → ℝ) : Prop :=
  (∃ β V, mGap β V ≤ 0) ∨
  (∀ c : ℝ → ℝ, (∀ β, 0 < c β) → ∃ β V, c β > mGap β V) ∨
  (∀ Δ : ℝ, 0 < Δ → ∃ V, ¬ Tendsto (fun β => mGap β V / spacing β) atTop (nhds Δ))

/-- **The join is the exact negation of its falsifier**: `volumeUniformJoin` ⟺ `¬ falsifier`. This is
the definitional shape that makes the rung a real, checkable statement rather than a slogan. -/
theorem volumeUniformJoin_not_falsifier (mGap : ℝ → ℝ → ℝ) (spacing : ℝ → ℝ) :
    volumeUniformJoin mGap spacing ↔ ¬ volumeUniformJoinFalsifier mGap spacing := by
  unfold volumeUniformJoin volumeUniformJoinFalsifier
  constructor
  · intro h hf
    rcases h with ⟨hpos, ⟨c, hc0, hcb⟩, ⟨Δ, hΔ0, hΔt⟩⟩
    rcases hf with hf1 | hf2 | hf3
    · rcases hf1 with ⟨β, V, hβV⟩
      exact (not_lt_of_ge hβV) (hpos β V)
    · have hbad := hf2 c hc0
      rcases hbad with ⟨β, V, hβV⟩
      exact (not_lt_of_ge (hcb β V)) hβV
    · have hbad := hf3 Δ hΔ0
      rcases hbad with ⟨V, hV⟩
      exact hV (hΔt V)
  · intro hn
    -- push the negation through the three disjuncts
    push_neg at hn
    exact hn

/-- `alphaAt` is strictly monotone increasing in β: the Dobrushin parameter grows toward 1 as the
coupling weakens. -/
lemma alphaAt_strictMono {c n β₁ β₂ : ℝ} (hc : 0 < c) (hn : 0 < n) (h : β₁ < β₂) :
    alphaAt c n β₁ < alphaAt c n β₂ := by
  dsimp [alphaAt]
  have hexp : Real.exp (-4 * n * β₂) < Real.exp (-4 * n * β₁) := by
    rw [Real.exp_lt_exp]
    have harg : -4 * n * β₂ < -4 * n * β₁ := by
      nlinarith [mul_lt_mul_of_pos_left h (by nlinarith : 0 < 4 * n)]
    exact harg
  nlinarith [mul_lt_mul_of_pos_left (sub_lt_sub_right hexp 1) hc]

/-- **The Dobrushin mass rate is NOT a volume-uniform positive lower bound** — the exact obstruction
that makes the volume-uniform join the open Clay rung. Past the ceiling `β > ceilingBeta`, the
Dobrushin parameter `α > 1`, so `massRate α = (−log α)/2 < 0`: the strong-coupling bound is vacuous
there and cannot be the `c(β) > 0` the join's clause (2) requires. This is what `mass_gap_join : Δ/a = 1`
hides: the strong-coupling gap does not survive to the continuum uniformly. -/
theorem dobrushin_not_volume_uniform {c n : ℝ} (hc : 1 < c) (hn : 0 < n) :
    ∃ β : ℝ, massRate (alphaAt c n β) ≤ 0 := by
  use ceilingBeta c n + 1
  have hceiling : alphaAt c n (ceilingBeta c n) = 1 := alphaAt_ceiling_eq_one hc (ne_of_gt hn)
  have hα : 1 < alphaAt c n (ceilingBeta c n + 1) := by
    rw [← hceiling]
    exact alphaAt_strictMono (lt_trans zero_lt_one hc) hn (by linarith)
  exact le_of_lt (massRate_neg_of_one_lt hα)

end QM
