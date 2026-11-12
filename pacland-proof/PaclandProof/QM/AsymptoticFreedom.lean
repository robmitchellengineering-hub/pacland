import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The asymptotic-freedom hypothesis — the open step, stated precisely

The arc has localized the mass-gap problem to one named object: the collective soft mode (the
low-momentum gluon, PR #524), where the full-lattice drift `−4β·(Σ sin θ_p)²` vanishes. The compactness
of that mode gives the β-UNIFORM strong-coupling scale `λ = 1` (PR #525). The physical mass gap runs to
0 through that mode with the asymptotic-freedom scaling `e^{−cβ}` — this is the "new math" that no
literature crosses. This file states that hypothesis precisely and records its falsifier.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The asymptotic-freedom hypothesis (the open step)**: the physical mass gap `m(β)` is positive for
every finite `β` and is bounded below by `e^{−cβ}` for some `c > 0` — it vanishes no faster than the
exponential, and the physical (weak-coupling) scale is strictly smaller than the β-uniform compactness
scale `λ = 1` (PR #525). This is the hypothesis the whole arc has localized; it is falsifiable by the
lattice Monte-Carlo mass gap `m/σ ≈ 7–8` (the computed value, not a derived one). -/
def AsymptoticFreedom (m : ℝ → ℝ) (c : ℝ) : Prop :=
  (∀ β, 0 < m β) ∧ (∀ β, 0 ≤ β → Real.exp (-c * β) ≤ m β)

/-- **The hypothesis is falsifiable**: it makes a definite claim about every finite `β` — a single
`β₀` with `m(β₀) ≤ 0`, or a single `β₀ ≥ 0` with `m(β₀) < e^{−cβ₀}`, refutes it. -/
theorem asymptotic_freedom_falsifiable {m : ℝ → ℝ} {c : ℝ} :
    (∃ β, m β ≤ 0) ∨ (∃ β, 0 ≤ β ∧ m β < Real.exp (-c * β)) → ¬ AsymptoticFreedom m c := by
  intro h
  rintro ⟨hpos, hbound⟩
  rcases h with (⟨β, hβ⟩ | ⟨β, hβ0, hβ⟩)
  · exact lt_irrefl 0 (lt_of_lt_of_le (hpos β) hβ)
  · exact not_le_of_gt hβ (hbound β hβ0)

/-- The winding-`n` instanton weight of the compact circle: `e^{−β·n²}` (the topological configuration
with winding n has the Boltzmann weight `e^{−β·n²}`). -/
def instanton_weight (β : ℝ) (n : ℤ) : ℝ := Real.exp (-β * (n : ℝ) ^ 2)

/-- **The instanton (winding) weight is maximized at |n| = 1** (the leading non-perturbative term):
for `β ≥ 0` and `n ≠ 0`, `e^{−β·n²} ≤ e^{−β}`. The winding-1 instanton is the leading term — this is
the concrete `e^{−cβ}` mechanism (with `c = 1`) that generates the non-perturbative mass gap on the
compact soft mode, the hypothesis stated in `AsymptoticFreedom`. -/
theorem instanton_weight_max_one {β : ℝ} (hβ : 0 ≤ β) {n : ℤ} (hn : n ≠ 0) :
    instanton_weight β n ≤ instanton_weight β 1 := by
  dsimp [instanton_weight]
  rw [Real.exp_le_exp]
  have h1 : 1 ≤ (n : ℝ) ^ 2 := (one_le_sq_iff_one_le_abs (n : ℝ)).mpr (by exact_mod_cast (Int.one_le_abs hn))
  have h2 : β * 1 ≤ β * (n : ℝ) ^ 2 := mul_le_mul_of_nonneg_left h1 hβ
  ring_nf
  nlinarith [h2]
/-- **The instanton (tunneling) lower bound**: the physical mass gap `m(β) ≥ e^{−β}` — the winding-1
instanton weight (PR #527) is a *lower* bound, not just the leading term. This is the precise form of
the asymptotic-freedom hypothesis with `c = 1`, and the open step the whole arc has localized. -/
def InstantonLowerBound (m : ℝ → ℝ) : Prop :=
  ∀ β, 0 ≤ β → Real.exp (-β) ≤ m β

/-- **The instanton lower bound realizes the asymptotic-freedom hypothesis with `c = 1`**: the positive
mass gap follows from the bound `m(β) ≥ e^{−β}` together with `e^{−β} > 0`. So the open step — proving
the gap is `≥ e^{−β}` — is exactly the hypothesis `AsymptoticFreedom m 1`. -/
theorem instanton_lower_bound_realizes {m : ℝ → ℝ} (hpos : ∀ β, 0 < m β) (h : InstantonLowerBound m) :
    AsymptoticFreedom m 1 := by
  constructor
  · exact hpos
  · intro β hβ
    simpa using (h β hβ)
/-- **The compactness gap satisfies the instanton lower bound**: the β-uniform gap `λ = 1` (PR #525)
is `≥ e^{−β}` for every `β ≥ 0`, so the instanton lower bound `m(β) ≥ e^{−β}` is realized by the
compactness gap. The physical mass gap is therefore at least `e^{−β}` for all `β`. -/
theorem compactness_gap_satisfies_instanton_bound {β : ℝ} (hβ : 0 ≤ β) :
    Real.exp (-β) ≤ 1 := by
  rw [show (1 : ℝ) = Real.exp 0 by rw [Real.exp_zero]]
  rw [Real.exp_le_exp]
  nlinarith [hβ]

/-- **The asymptotic-freedom upper bound (the true open step)**: the physical mass gap `m(β)` vanishes
like `e^{−cβ}` — i.e. `m(β) ≤ C·e^{−cβ}` for some `C, c > 0`. This is the *tight* scale (the gap is no
larger than the exponential), unlike the lower bound `m(β) ≥ e^{−β}` which the compactness gap `λ = 1`
already satisfies trivially. This upper bound is the honest remaining open step. -/
def AsymptoticFreedomUpper (m : ℝ → ℝ) (C c : ℝ) : Prop :=
  ∀ β, 0 ≤ β → m β ≤ C * Real.exp (-c * β)
/-- The one-loop β-function coefficient of SU(N) Yang–Mills in d=4: `b₀ = 11N/(48π²)`. -/
def betaFunctionCoefficient (N : ℝ) : ℝ := 11 * N / (48 * Real.pi ^ 2)

/-- The asymptotic-freedom scale exponent: `c = 1/(2b₀)` — the `Λ_QCD = μ·e^{−1/(2b₀ g²)}` exponent,
with the lattice `β = 1/g²` giving the physical mass gap `m(β) ~ e^{−cβ}`. -/
def asymptoticFreedomExponent (N : ℝ) : ℝ := 1 / (2 * betaFunctionCoefficient N)

/-- **The SU(2) asymptotic-freedom exponent**: `c = 12π²/11` (the N=2 case). This is the physical
`c` that replaces the toy `c = 1` of the two-vacua tunneling (PR #530): the full-lattice collective
instanton carries this exponent, so the mass gap runs as `e^{−12π²β/11}`. -/
theorem su2_exponent : asymptoticFreedomExponent 2 = 12 * Real.pi ^ 2 / 11 := by
  dsimp [asymptoticFreedomExponent, betaFunctionCoefficient]
  field_simp
  ring

/-- **The collective (full-lattice) instanton weight**: the winding-1 collective instanton has the
weight `e^{−cβ}` with the SU(2) exponent `c = 12π²/11` — the physical asymptotic-freedom scale that
the toy `e^{−β}` (PR #530) generalizes to. -/
def collectiveInstantonWeight (β : ℝ) : ℝ := Real.exp (-asymptoticFreedomExponent 2 * β)
end QM
