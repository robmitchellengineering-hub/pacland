import Mathlib

/-!
# The elementary counting lemma behind the Goldston–Suriajaya reduction.

The whole "remove RH from Montgomery's argument" question reduces to ONE horizontal-count estimate.
This file holds the ELEMENTARY counting part — a pure combinatorial statement that needs no analytic
number theory — and PROVES it. It is the correct, provable target.

Setup (from the note, arXiv:2511.20059 §5). A zero configuration is a finite set of DISTINCT
heights `γ`, each carrying a total multiplicity `m_γ ≥ 1` (the order of the zero). We represent it as a
finset of pairs `(γ, m)` with pairwise-distinct heights, so:

  * `N   = Z.card`                                   (number of distinct zeros)
  * `Σ m = ∑ x in Z, x.2`                            (total multiplicity)
  * `Σ_{γ=γ'} 1 = ∑_γ H(γ)² = ∑ x in Z, x.2^2`       (horizontal count: ordered pairs of zero-COPIES
                                                       on the same height; H(γ) = m_γ here because the
                                                       heights are already grouped)
  * `#simple = # {γ : m_γ = 1}`

The two counting facts are
  (1) `Σ m ≤ Σ_{γ=γ'} 1`   (diagonal pairs are a subset of the horizontal pairs), and
  (2) `#simple ≥ 2N − Σ m` (each non-simple zero has multiplicity ≥ 2),
and together with the assumption `Σ_{γ=γ'} 1 ≤ C·N` (C < 2) they give `#simple ≥ (2 − C)·N`.

The OPEN frontier — the analytic estimate `horizontalCount ≤ C·N` for some `C < 2` — is stated last and
left as `sorry`; it is the hard 50-year-open part, not a counting statement.
-/

open scoped BigOperators

/-- Total multiplicity `Σ m_ρ`. -/
def totalMultiplicity (Z : Finset (ℝ × ℕ)) : ℕ :=
  ∑ x in Z, x.2

/-- The horizontal count `Σ_{γ=γ'} 1` (ordered pairs of zero-copies on the same height).
Because `Z` stores distinct heights with their grouped multiplicity, this is `∑ x in Z, x.2^2`. -/
def horizontalCount (Z : Finset (ℝ × ℕ)) : ℕ :=
  ∑ x in Z, x.2 ^ 2

/-- The number of simple zeros (multiplicity exactly 1). -/
def simpleCount (Z : Finset (ℝ × ℕ)) : ℕ :=
  (Z.filter (fun x => x.2 = 1)).card

-- `m ≤ m²` for every natural `m` (used for fact (1)).
private lemma nat_le_self_mul (n : ℕ) : n ≤ n * n := by
  by_cases hn : n = 0
  · simp [hn]
  · have h1 : 1 ≤ n := Nat.succ_le_of_lt (Nat.pos_of_ne_zero hn)
    have : n * 1 ≤ n * n := Nat.mul_le_mul_left n h1
    simpa using this

/-- Fact (1): the total multiplicity is at most the horizontal count (`Σ m ≤ Σ m²`). -/
theorem totalMultiplicity_le_horizontalCount (Z : Finset (ℝ × ℕ)) :
    totalMultiplicity Z ≤ horizontalCount Z := by
  unfold totalMultiplicity horizontalCount
  apply Finset.sum_le_sum
  intro x _
  simpa [sq] using nat_le_self_mul x.2

/-- Fact (2): `2N ≤ #simple + Σ m`, i.e. `#simple ≥ 2N − Σ m`. Requires each multiplicity ≥ 1. -/
theorem simpleCount_lower_bound (Z : Finset (ℝ × ℕ)) (hpos : ∀ x ∈ Z, 1 ≤ x.2) :
    2 * Z.card ≤ simpleCount Z + totalMultiplicity Z := by
  classical
  -- Split into simple (m = 1) and non-simple (m ≠ 1) parts.
  let simple : Finset (ℝ × ℕ) := Z.filter (fun x => x.2 = 1)
  let nonsimple : Finset (ℝ × ℕ) := Z.filter (fun x => x.2 ≠ 1)
  -- Every element contributes 2 to the RHS: simple contributes 1 (to simpleCount) + 1 (m=1), and
  -- non-simple contributes 0 (to simpleCount) + m ≥ 2.
  have hpointwise : ∀ x ∈ Z, 2 ≤ (if x.2 = 1 then 1 else 0) + x.2 := by
    intro x hx
    have hx1 : 1 ≤ x.2 := hpos x hx
    by_cases hs : x.2 = 1
    · simp [hs]
    · have hx2 : 2 ≤ x.2 := by
        omega
      simp [hs, hx2]
  have hsum := Finset.sum_le_sum (s := Z) (f := fun _ : ℝ × ℕ => (2 : ℕ)) (g := fun x => (if x.2 = 1 then 1 else 0) + x.2) hpointwise
  -- LHS of the summed inequality is 2·N.
  have hlhs : (∑ _x in Z, (2 : ℕ)) = 2 * Z.card := by
    simp
  -- RHS splits into simpleCount + totalMultiplicity.
  have hrhs : (∑ x in Z, ((if x.2 = 1 then 1 else 0) + x.2)) = simpleCount Z + totalMultiplicity Z := by
    simp [simpleCount, totalMultiplicity, simple, nonsimple, Finset.sum_add_distrib]
  rw [hlhs, hrhs] at hsum
  exact hsum

/-- THE ELEMENTARY REDUCTION. If the horizontal count is at most `C·N` for `C < 2`, then at least a
proportion `2 − C` of the distinct zeros are simple. This is Goldston–Suriajaya's counting step. -/
theorem reduction_simple_zeros (Z : Finset (ℝ × ℕ)) (C : ℝ)
    (hpos : ∀ x ∈ Z, 1 ≤ x.2)
    (hC : 1 ≤ C) (hC2 : C < 2)
    (hcount : (horizontalCount Z : ℝ) ≤ C * (Z.card : ℝ)) :
    (simpleCount Z : ℝ) ≥ (2 - C) * (Z.card : ℝ) := by
  -- Fact (2) cast to ℝ: simple ≥ 2N − Σm.
  have h_simple : 2 * (Z.card : ℝ) ≤ (simpleCount Z : ℝ) + (totalMultiplicity Z : ℝ) := by
    exact_mod_cast simpleCount_lower_bound Z hpos
  -- Fact (1) cast to ℝ: Σm ≤ horizontalCount.
  have h_tot : (totalMultiplicity Z : ℝ) ≤ (horizontalCount Z : ℝ) := by
    exact_mod_cast totalMultiplicity_le_horizontalCount Z
  nlinarith

/-- THE OPEN FRONTIER (not provable here — the analytic estimate). Prove unconditionally that the
horizontal count is bounded by a constant `C < 2` times the zero count. Under RH it holds with `C = 4/3`
(Montgomery). This `sorry` is the whole gap. -/
theorem horizontal_count_bound (Z : Finset (ℝ × ℕ)) (C : ℝ) (hC : C < 2) :
    (horizontalCount Z : ℝ) ≤ C * (Z.card : ℝ) := by
  sorry
