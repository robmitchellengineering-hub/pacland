import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# QF-2 — envariance: the equiprobability step, kernel-checked

Zurek's envariance core in the cleanest case. The maximally entangled state
`|Φ⁺⟩ = |00⟩ + |11⟩` is **invariant** under flipping both qubits (the flip on
one subsystem is undone by the flip on the other). Because that flip swaps
`|00⟩ ↔ |11⟩`, invariance forces the two Schmidt amplitudes to be equal — hence
equiprobable after normalization. This is the envariance derivation of the
`1/2, 1/2` weights, stated and proved over `ℚ`.

**The definite-outcome gap (not proved, by design):** envariance yields the
*probability weights* of the Schmidt basis; it does not select *which* outcome
occurs. That step is `Hinges.F3.conclusion_born_rule` — a named assumption, not a
theorem (rule 67: a statement is not a proof).
-/

noncomputable section

namespace Envariance

/-- The maximally entangled two-qubit state (unnormalized): `|00⟩ + |11⟩`, in the
basis `(i, j) ↦ 2i + j`, encoded over `Fin 4 → ℚ`. -/
def phiPlus : Fin 4 → ℚ := ![1, 0, 0, 1]

/-- Flip both qubits: `(i, j) ↦ (1 - i, 1 - j)`, i.e. `|00⟩↔|11⟩`, `|01⟩↔|10⟩`. -/
def flipBoth : Fin 4 → Fin 4
  | 0 => 3
  | 1 => 2
  | 2 => 1
  | 3 => 0

/-- **Envariance.** The maximally entangled state is invariant under flipping both
qubits: `flipBoth ∘ φ⁺ = φ⁺`. The flip on one subsystem is undone by the flip on
the other, so the entangled state itself is unchanged. -/
theorem envariance : phiPlus ∘ flipBoth = phiPlus := by
  funext i
  fin_cases i <;> norm_num [phiPlus, flipBoth]

/-- Envariance forces the two Schmidt amplitudes equal: since `flipBoth 0 = 3`
and `φ⁺` is flip-invariant, `φ⁺ 0 = φ⁺ 3` (the `|00⟩` and `|11⟩` weights). -/
theorem schmidt_amplitudes_equal : phiPlus 0 = phiPlus 3 := by
  have h := congr_fun envariance 0
  norm_num [flipBoth] at h
  exact h.symm

end Envariance

end
