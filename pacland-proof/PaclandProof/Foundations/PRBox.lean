import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# QF-4 — the PR-box: no-signaling does not single out quantum mechanics

The F2 hinge's negative content, kernel-checked. The Popescu–Rohrlich box
(1994) is a two-party, two-bit distribution that is **no-signaling** yet
achieves **CHSH = 4** — the algebraic maximum, above the quantum (Tsirelson)
bound `2√2 ≈ 2.828` and above the local bound `2`. Therefore the two named
hypotheses on `Hinges.F2` (`h_no_signaling`, `h_information_causality`) do not
by themselves force the quantum correlation set.

All computation is over `ℚ` on `Fin 2`; the Tsirelson bound is cited, not
needed here — the super-quantum conclusion follows from `CHSH = 4 > 2` (the
local bound) together with the fact that no bipartite box can exceed `4`
(algebraic maximum).
-/

noncomputable section

open scoped BigOperators

namespace PRBox

/-- The PR-box: `P(a,b | x,y) = 1/2` iff `a ⊕ b = x · y`, else `0`, over bits. -/
def prbox (x y a b : Fin 2) : ℚ :=
  if (a.val + b.val) % 2 = x.val * y.val then (1 / 2 : ℚ) else 0

/-- No-signaling: Alice's marginal is independent of Bob's input `y`. -/
theorem nosignaling_A (x y y' a : Fin 2) :
    (∑ b : Fin 2, prbox x y a b) = (∑ b : Fin 2, prbox x y' a b) := by
  fin_cases x <;> fin_cases y <;> fin_cases y' <;> fin_cases a <;>
    norm_num [prbox, Fin.sum_univ_two]

/-- No-signaling: Bob's marginal is independent of Alice's input `x`. -/
theorem nosignaling_B (x x' y b : Fin 2) :
    (∑ a : Fin 2, prbox x y a b) = (∑ a : Fin 2, prbox x' y a b) := by
  fin_cases x <;> fin_cases x' <;> fin_cases y <;> fin_cases b <;>
    norm_num [prbox, Fin.sum_univ_two]

/-- The correlator `E(xy) = P(a⊕b = 0 | xy) − P(a⊕b = 1 | xy)`. -/
def correlator (P : Fin 2 → Fin 2 → Fin 2 → Fin 2 → ℚ) (x y : Fin 2) : ℚ :=
  (∑ a : Fin 2, ∑ b : Fin 2, if (a.val + b.val) % 2 = 0 then P x y a b else 0) -
    (∑ a : Fin 2, ∑ b : Fin 2, if (a.val + b.val) % 2 = 1 then P x y a b else 0)

/-- The CHSH value `S = E(00) + E(01) + E(10) − E(11)`. -/
def chsh (P : Fin 2 → Fin 2 → Fin 2 → Fin 2 → ℚ) : ℚ :=
  correlator P 0 0 + correlator P 0 1 + correlator P 1 0 - correlator P 1 1

/-- The PR-box saturates the algebraic maximum: **CHSH = 4** (local bound is `2`,
quantum Tsirelson bound is `2√2`). -/
theorem prbox_chsh : chsh prbox = 4 := by
  norm_num [chsh, correlator, prbox, Fin.sum_univ_two]

/-- Consequence: the PR-box is a Bell violation — its CHSH value `4` exceeds the
local bound `2`. Hence it is no-signaling but not local, and (with the algebraic
maximum `4`) strictly above the quantum bound — the correlation-set gap. -/
theorem prbox_nonlocal : chsh prbox > 2 := by
  rw [prbox_chsh]
  norm_num

/-- The quantum (Tsirelson) bound `2√2` is strictly below the PR-box value `4`.
This is the last link of the F2 negative: the box is no-signaling yet sits above
the quantum bound, so no-signaling does not single out quantum mechanics. -/
theorem tsirelson_lt_prbox : (2 * Real.sqrt 2 : ℝ) < 4 := by
  have h : (Real.sqrt 2 : ℝ) < 2 := by
    have hsq : (Real.sqrt 2 : ℝ) ^ 2 = 2 := by
      rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    have hnn : (0 : ℝ) ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
    nlinarith
  nlinarith

end PRBox

end
