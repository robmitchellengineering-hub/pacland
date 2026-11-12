import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# M2 — the clustering ⟺ transfer-operator gap bridge (algebraic heart)

The Eriksson "clustering ⟺ transfer-operator gap" bridge (machine-checked elsewhere) reduces the
mass gap to the exponential decay of the connected 2-point function. Its algebraic heart is that the
connected 2-point function of a transfer operator `T = S + P` (vacuum projection `P`, `S Ω = 0`,
`P S = 0`) equals the `S`-power matrix element:

```
G_v(k) = ⟪v, T^k v⟫ − |⟪Ω, v⟫|² = ⟪v, S^k v⟫   (k ≥ 1)
```

So "the mass gap (‖S‖ < 1)" is literally equivalent to "the connected 2-point function decays as
‖S‖^k". This file kernel-checks the identity; the operator-norm bound `|⟪v, S^k v⟫| ≤ ‖v‖² ‖S‖^k`
(Cauchy–Schwarz + submultiplicativity) is the next step.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The connected 2-point function of the transfer operator T with vacuum Ω:
`G_v(k) = ⟪v, T^k v⟫ − |⟪Ω, v⟫|²`. -/
def connected2pt {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (T : H →L[ℂ] H) (Ω v : H) (k : ℕ) : ℂ :=
  inner ℂ v ((T ^ k) v) - inner ℂ Ω v * inner ℂ v Ω

/-- **M2, the algebraic heart of the clustering ⟺ gap bridge.** If `T = S + P` with `P` the
rank-one projection onto the unit vacuum `Ω`, `S Ω = 0`, and `P S = 0` pointwise, then the connected
2-point function equals the `S`-power matrix element: `G_v(k) = ⟪v, S^k v⟫` for `k ≥ 1`. -/
theorem connected2pt_eq_spower {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (T S P : H →L[ℂ] H) (Ω : H) (hΩ : ‖Ω‖ = 1) (hT : T = S + P)
    (hP : ∀ w, P w = inner ℂ Ω w • Ω) (hSΩ : S Ω = 0)
    (hPS : ∀ w, P (S w) = 0)
    (v : H) (k : ℕ) (hk : 1 ≤ k) :
    connected2pt T Ω v k = inner ℂ v ((S ^ k) v) := by
  dsimp [connected2pt]
  have hpow : (T ^ k) v = (S ^ k) v + inner ℂ Ω v • Ω := by
    induction' k with k ih
    · omega
    · by_cases hk0 : k = 0
      · subst hk0
        rw [pow_one, pow_one, hT]
        simp [hP]
      · have hk1 : 1 ≤ k := by omega
        have ih' := ih hk1
        rw [pow_succ']
        change T ((T ^ k) v) = (S ^ (k + 1)) v + inner ℂ Ω v • Ω
        rw [ih', hT]
        simp only [add_apply, map_add]
        have hS1 : S (inner ℂ Ω v • Ω) = 0 := by rw [map_smul, hSΩ]; simp
        have hP1 : P ((S ^ k) v) = 0 := by
          rcases k with _ | m
          · omega
          · rw [pow_succ']
            change P (S ((S ^ m) v)) = 0
            exact hPS ((S ^ m) v)
        have hP2 : P (inner ℂ Ω v • Ω) = inner ℂ Ω v • Ω := by
          rw [hP, inner_smul_right]; simp [hΩ]
        rw [hS1, hP1, hP2]
        simp [pow_succ']
  rw [hpow]
  have hin : inner ℂ v (inner ℂ Ω v • Ω) = inner ℂ Ω v * inner ℂ v Ω := by
    rw [inner_smul_right]
  rw [inner_add_right, hin]
  ring

theorem spower_matrix_element_le {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (S : H →L[ℂ] H) (v : H) (k : ℕ) :
    ‖inner ℂ v ((S ^ k) v)‖ ≤ ‖v‖^2 * ‖S‖^k := by
  have hpow : ‖(S ^ k) v‖ ≤ ‖S‖^k * ‖v‖ := by
    induction' k with k ih
    · simp
    · rw [pow_succ']
      change ‖S ((S ^ k) v)‖ ≤ ‖S‖^(k+1) * ‖v‖
      calc
        ‖S ((S ^ k) v)‖ ≤ ‖S‖ * ‖(S ^ k) v‖ := ContinuousLinearMap.le_opNorm S ((S ^ k) v)
        _ ≤ ‖S‖ * (‖S‖^k * ‖v‖) := by
          exact mul_le_mul_of_nonneg_left ih (norm_nonneg _)
        _ = ‖S‖^(k+1) * ‖v‖ := by ring
  calc
    ‖inner ℂ v ((S ^ k) v)‖ ≤ ‖v‖ * ‖(S ^ k) v‖ := norm_inner_le_norm v ((S ^ k) v)
    _ ≤ ‖v‖ * (‖S‖^k * ‖v‖) := mul_le_mul_of_nonneg_left hpow (norm_nonneg _)
    _ = ‖v‖^2 * ‖S‖^k := by ring
theorem inner_sq_eq_norm_sq {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    [CompleteSpace H]
    (S : H →L[ℂ] H) (hS : IsSelfAdjoint S) (v : H) :
    RCLike.re (inner ℂ v ((S ^ 2) v)) = ‖S v‖ ^ 2 := by
  change RCLike.re (inner ℂ v (S (S v))) = ‖S v‖ ^ 2
  rw [← ContinuousLinearMap.adjoint_inner_left]
  have hS' : ContinuousLinearMap.adjoint S = S := (hS : star S = S)
  rw [hS']
  exact inner_self_eq_norm_sq (𝕜 := ℂ) (S v)
end QM
