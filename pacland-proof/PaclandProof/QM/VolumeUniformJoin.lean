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

/-- **The volume-uniform continuum join** (the open Clay rung), with its exact hypotheses.
`G` is the compact gauge group (SU(2)); `S_Wilson` its Wilson action; `mDobrushin` the strong-coupling
Dobrushin lower bound; `mGap β V` the lattice spectral gap (lattice units) at coupling β on volume V;
`spacing β` the lattice spacing `a(β)`. The join asserts, all required:
0. the Dobrushin bound is a lower bound wherever it is positive (the strong-coupling input);
1. the gap is positive on every finite volume;
2. at each coupling there is a *volume-independent* lower bound `c(β) ≤ mGap β V`;
3. the physical gap `Δ = lim_{β→∞} mGap β V / spacing β` is positive, *uniformly in V*.
NOT proved. Stated with the exact hypotheses + a falsifier. -/
def volumeUniformJoin
    (G : Type*) [Group G]         -- the compact gauge group (SU(2))
    (S_Wilson : ℝ → ℝ)            -- the Wilson action (coupling ↦ action coefficient)
    (mDobrushin : ℝ → ℝ)          -- the Dobrushin strong-coupling lower bound
    (mGap : ℝ → ℝ → ℝ)            -- the spectral gap (β, V) ↦ m(β, V)
    (spacing : ℝ → ℝ) : Prop :=    -- the lattice spacing a(β)
  (∀ β V, 0 < mDobrushin β → mDobrushin β ≤ mGap β V) ∧
  (∀ β V, 0 < mGap β V) ∧
  (∃ c : ℝ → ℝ, (∀ β, 0 < c β) ∧ (∀ β V, c β ≤ mGap β V)) ∧
  (∃ Δ : ℝ, 0 < Δ ∧ ∀ V, Tendsto (fun β => mGap β V / spacing β) atTop (nhds Δ))

/-- **The falsifier** of the volume-uniform join: any of the four clauses fails — the Dobrushin bound
is violated where it is positive; a non-positive gap on some (β, V); no positive volume-uniform lower
bound; or no positive physical gap that is volume-independent. This is the check that turns the join
into a falsifiable claim. -/
def volumeUniformJoinFalsifier
    (G : Type*) [Group G] (S_Wilson mDobrushin : ℝ → ℝ)
    (mGap : ℝ → ℝ → ℝ) (spacing : ℝ → ℝ) : Prop :=
  (∃ β V, 0 < mDobrushin β ∧ mDobrushin β > mGap β V) ∨
  (∃ β V, mGap β V ≤ 0) ∨
  (∀ c : ℝ → ℝ, (∀ β, 0 < c β) → ∃ β V, c β > mGap β V) ∨
  (∀ Δ : ℝ, 0 < Δ → ∃ V, ¬ Tendsto (fun β => mGap β V / spacing β) atTop (nhds Δ))

/-- **The join is the exact negation of its falsifier**: `volumeUniformJoin` ⟺ `¬ falsifier`. This is
the definitional shape that makes the rung a real, checkable statement rather than a slogan. -/
theorem volumeUniformJoin_not_falsifier
    (G : Type*) [Group G] (S_Wilson mDobrushin : ℝ → ℝ)
    (mGap : ℝ → ℝ → ℝ) (spacing : ℝ → ℝ) :
    volumeUniformJoin G S_Wilson mDobrushin mGap spacing ↔ ¬ volumeUniformJoinFalsifier G S_Wilson mDobrushin mGap spacing := by
  unfold volumeUniformJoin volumeUniformJoinFalsifier
  constructor
  · intro h hf
    rcases h with ⟨hd, hpos, ⟨c, hc0, hcb⟩, ⟨Δ, hΔ0, hΔt⟩⟩
    rcases hf with hf0 | hf1 | hf2 | hf3
    · rcases hf0 with ⟨β, V, hβV⟩
      exact (not_lt_of_ge (hd β V hβV.1)) hβV.2
    · rcases hf1 with ⟨β, V, hβV⟩
      exact (not_lt_of_ge hβV) (hpos β V)
    · have hbad := hf2 c hc0
      rcases hbad with ⟨β, V, hβV⟩
      exact (not_lt_of_ge (hcb β V)) hβV
    · have hbad := hf3 Δ hΔ0
      rcases hbad with ⟨V, hV⟩
      exact hV (hΔt V)
  · intro hn
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

/-- **The asymptotic-freedom lower bound** — the join's clause (2) instantiated. The spectral gap
`mGap β` is bounded below by the confinement scale `A·e^(−c′β)` for every β. This is the
volume-uniform bound the join needs: the Dobrushin rate fails it (`dobrushin_not_volume_uniform`), but
the measured scaling law is the candidate. NOT proved — stated as the precise sub-rung, with the
referee numbers `A ≈ 25.28`, `c′ ≈ 1.182`. -/
def asymptoticFreedomLowerBound (mGap : ℝ → ℝ) (A c' : ℝ) : Prop :=
  ∀ β, A * Real.exp (-c' * β) ≤ mGap β

/-- **The falsifier** of the asymptotic-freedom lower bound: a coupling β where the gap dips below the
confinement scale `A·e^(−c′β)`. This is the check that turns the bound into a falsifiable claim — and
it is the check the measured scaling law `m(β) = 25.28·e^(−1.182β)` passed (it is the exact value, not
a mere lower bound). -/
def asymptoticFreedomLowerBoundFalsifier (mGap : ℝ → ℝ) (A c' : ℝ) : Prop :=
  ∃ β, mGap β < A * Real.exp (-c' * β)

/-- **The measured scaling law is referee-consistent with the asymptotic-freedom bound**: with the
measured `A = 25.28`, `c′ = 1.182`, the bound `25.28·e^(−1.182β) ≤ mGap β` holds at equality for the
measured `mGap`. This is the *numerical referee* the join must reproduce — stated as the exact
instantiation, not a proof of the join. -/
def refereeScalingLaw (mGap : ℝ → ℝ) : Prop :=
  asymptoticFreedomLowerBound mGap (25.28) (1.182)

/-- **The Dobrushin rate fails the asymptotic-freedom lower bound** — the precise statement that the
strong-coupling bound cannot be the join's clause (2). For any positive A, c′, the Dobrushin rate
`massRate (alphaAt c n β)` is negative past the ceiling while `A·e^(−c′β) > 0`, so no positive
asymptotic-freedom bound holds. This connects the obstruction (round 12) to the referee instantiation
(round 13): the join needs a bound *other* than Dobrushin. -/
theorem dobrushin_fails_asymptotic_freedom {c n : ℝ} (hc : 1 < c) (hn : 0 < n) :
    ∀ A c' : ℝ, 0 < A → ¬ asymptoticFreedomLowerBound (fun β => massRate (alphaAt c n β)) A c' := by
  intro A c' hA hb
  have hceiling : alphaAt c n (ceilingBeta c n) = 1 := alphaAt_ceiling_eq_one hc (ne_of_gt hn)
  have hα : 1 < alphaAt c n (ceilingBeta c n + 1) := by
    rw [← hceiling]
    exact alphaAt_strictMono (lt_trans zero_lt_one hc) hn (by linarith)
  have hneg : massRate (alphaAt c n (ceilingBeta c n + 1)) < 0 := massRate_neg_of_one_lt hα
  have hpos : 0 < A * Real.exp (-c' * (ceilingBeta c n + 1)) := mul_pos hA (Real.exp_pos _)
  have hb' : A * Real.exp (-c' * (ceilingBeta c n + 1)) ≤ massRate (alphaAt c n (ceilingBeta c n + 1)) :=
    hb (ceilingBeta c n + 1)
  exact not_lt_of_ge hb' (lt_trans hneg hpos)

/-- **The asymptotic-freedom bound + the matching spacing ⟹ a uniformly positive physical gap.**
If `m(β) ≥ A·e^(−cβ)` (clause (2), the asymptotic-freedom lower bound) and the spacing `a(β) = e^(−cβ)`
has the *same* exponent, then `m/a ≥ A > 0` for every β — the physical gap is uniformly bounded below
by the positive amplitude. This is the referee-consistent instantiation of the join's clause (3):
clause (3) follows from clause (2) precisely when the mass and the spacing share the RG exponent. The
matching-exponent condition is the open part (the Clay rung). -/
theorem asymptotic_freedom_physical_gap {A c : ℝ} (hA : 0 < A) (mGap spacing : ℝ → ℝ)
    (hm : ∀ β, A * Real.exp (-c * β) ≤ mGap β)
    (ha : ∀ β, spacing β = Real.exp (-c * β)) :
    ∀ β, A ≤ mGap β / spacing β := by
  intro β
  rw [ha β]
  have hpos : 0 < Real.exp (-c * β) := Real.exp_pos _
  rw [le_div_iff₀' hpos]
  simpa [mul_comm] using hm β

end QM
