import Mathlib.Data.Multiset.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# The elementary counting lemma behind the Goldston–Suriajaya reduction.

The whole "remove RH from Montgomery's argument" question reduces to ONE horizontal-count estimate.
This file holds the ELEMENTARY counting part — the reduction that is a pure multiset argument and needs
no analytic number theory. It is the correct, provable target for the churn loop.

From the note (arXiv:2511.20059, §5):
  * `N` = the number of DISTINCT zeros (support of the multiset).
  * `Σ m_ρ` = the total multiplicity (multiset cardinality) = `Z.card`.
  * the horizontal count `Σ_{γ=γ'} 1` counts ordered pairs of zero-copies on the same line `t=γ`.
  * key fact: `Σ m_ρ ≤ Σ_{γ=γ'} 1` (the diagonal pairs are a subset of the horizontal pairs).
  * key fact: `#simple ≥ 2N − Σ m_ρ`  (each non-simple zero has multiplicity ≥ 2).

Consequence (the reduction):  if `Σ_{γ=γ'} 1 ≤ C·N` for `C<2`, then `#simple ≥ (2−C)·N`.
-/

open scoped BigOperators

/-- A zero, recorded with its height γ and its multiplicity m. (The analytic content — that these are
the zeros of ζ — is external; the counting lemma only needs the multiset structure.) -/
structure Zero where
  gamma : ℝ
  multiplicity : ℕ

/-- The horizontal count Σ_{γ=γ'} 1 = Σ_ρ H(γ_ρ): the number of ordered pairs of zero-copies with the
same height. This is the quantity the OPEN estimate must bound. -/
noncomputable def horizontalCount (Z : Multiset Zero) : ℕ :=
  ∑ ρ in Z, Z.countP (fun ρ' => ρ'.gamma = ρ.gamma)

/-- THE ELEMENTARY REDUCTION. If the horizontal count is at most `C` times the number of distinct zeros,
then at least a proportion `2 − C` of the (distinct) zeros are simple. This is Goldston–Suriajaya's
counting step, stated purely in multisets. -/
theorem reduction_simple_zeros
    (Z : Multiset Zero) (C : ℝ)
    (hC : 1 ≤ C) (hC2 : C < 2)
    (hcount : (horizontalCount Z : ℝ) ≤ C * (Z.toFinset.card : ℝ)) :
    (Z.toFinset.filter (fun ρ => ρ.multiplicity = 1) |>.card : ℝ) ≥ (2 - C) * (Z.toFinset.card : ℝ) := by
  sorry

/-- The supporting fact: the total multiplicity (multiset card) is at most the horizontal count. -/
theorem total_multiplicity_le_horizontalCount (Z : Multiset Zero) :
    (Z.card : ℝ) ≤ (horizontalCount Z : ℝ) := by
  sorry

/-- The supporting fact: `#simple ≥ 2N − Σ m_ρ`. -/
theorem simple_count_lower_bound (Z : Multiset Zero) :
    (Z.toFinset.filter (fun ρ => ρ.multiplicity = 1) |>.card : ℝ)
      ≥ 2 * (Z.toFinset.card : ℝ) - (Z.card : ℝ) := by
  sorry

/-- THE OPEN FRONTIER (not provable here — it is the analytic estimate). Prove unconditionally that the
horizontal count is bounded by a constant `C < 2` times the zero count. Under RH it holds with `C = 4/3`
(Montgomery). This `sorry` is the whole gap. -/
theorem horizontal_count_bound
    (Z : Multiset Zero) (C : ℝ) (hC : C < 2) :
    (horizontalCount Z : ℝ) ≤ C * (Z.toFinset.card : ℝ) := by
  sorry
