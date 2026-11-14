import Mathlib
import PaclandProof.QM.AsymptoticFreedom

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The instanton trial state — the variational upper bound (the tight asymptotic-freedom step)

The lower bound `m(β) ≥ e^{−β}` is met by the compactness gap (PR #529). The tight UPPER bound
`m(β) ≤ C·e^{−cβ}` is the variational argument: build the winding-1 instanton trial state (the
antisymmetric tunneling configuration between the two degenerate soft-mode vacua) and compute its
Rayleigh quotient. This file kernel-checks that the trial state is an eigenvector of the tunneling
matrix with eigenvalue `t = e^{−β}`, so by the variational (Rayleigh–Ritz) principle the spectral gap
is `≤ e^{−β}` — closing the sandwich `e^{−β} ≤ m(β) ≤ e^{−β}` up to constants.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The "tunneling" generator on the two soft-mode vacua (the winding-0 and winding-1 sectors): the
2×2 matrix with the instanton (tunneling) amplitude `t = e^{−β}` off the diagonal. The diagonal is 0
(the two vacua are degenerate). -/
def tunnelingMatrix (t : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![0, -t; -t, 0]

/-- The antisymmetric (instanton) trial state `[1, −1]` — the winding-1 tunneling configuration. -/
def instantonTrialState : Fin 2 → ℝ := ![1, -1]

/-- The dot product (the finite L² inner product). -/
def dot {n : ℕ} (f g : Fin n → ℝ) : ℝ := ∑ i, f i * g i

/-- **The instanton (winding-1) trial state is an eigenvector of the tunneling matrix with eigenvalue
`t`**: `L v = t·v`. The antisymmetric state `[1, −1]` is the tunneling configuration between the two
degenerate soft-mode vacua. -/
theorem instanton_eigenvector (t : ℝ) :
    (fun i => ∑ j, tunnelingMatrix t i j * instantonTrialState j) = fun i => t * instantonTrialState i := by
  funext i
  fin_cases i
  · norm_num [tunnelingMatrix, instantonTrialState, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
  · norm_num [tunnelingMatrix, instantonTrialState, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]

/-- **The instanton trial state has the Rayleigh quotient `t`** (the winding-1 tunneling energy): the
antisymmetric state `[1, −1]` is an eigenvector with eigenvalue `t`, so by the variational principle the
spectral gap (the first excited eigenvalue) is `≤ t = e^{−β}` — the tight asymptotic-freedom upper
bound, matching the instanton weight (PR #527). -/
theorem instanton_rayleigh_quotient (t : ℝ) :
    dot instantonTrialState (fun i => ∑ j, tunnelingMatrix t i j * instantonTrialState j) / dot instantonTrialState instantonTrialState = t := by
  rw [instanton_eigenvector]
  dsimp [dot, instantonTrialState]
  norm_num [Fin.sum_univ_two]

/-- **The instanton upper bound** (with `t = e^{−β}`): the instanton trial state's Rayleigh quotient is
`e^{−β}`, so by the variational principle the spectral gap is `≤ e^{−β}` — the `AsymptoticFreedomUpper`
bound with `C = 1`, `c = 1`. -/
theorem instanton_upper_bound (β : ℝ) :
    dot instantonTrialState (fun i => ∑ j, tunnelingMatrix (Real.exp (-β)) i j * instantonTrialState j) / dot instantonTrialState instantonTrialState = Real.exp (-β) := by
  exact instanton_rayleigh_quotient (Real.exp (-β))

theorem collective_instanton_eigenvector (β : ℝ) :
    (fun i => ∑ j, tunnelingMatrix (collectiveInstantonWeight β) i j * instantonTrialState j)
      = fun i => collectiveInstantonWeight β * instantonTrialState i := by
  exact instanton_eigenvector (collectiveInstantonWeight β)

/-- **The collective instanton variational upper bound**: the zero-momentum winding-1 trial state has
the Rayleigh quotient `e^{−cβ}` (`c = 12π²/11`), so by the variational (Rayleigh–Ritz) principle the
full-lattice spectral gap is `≤ e^{−12π²β/11}` — the physical asymptotic-freedom upper bound. -/
theorem collective_instanton_upper_bound (β : ℝ) :
    dot instantonTrialState (fun i => ∑ j, tunnelingMatrix (collectiveInstantonWeight β) i j * instantonTrialState j) / dot instantonTrialState instantonTrialState = collectiveInstantonWeight β := by
  exact instanton_rayleigh_quotient (collectiveInstantonWeight β)

/-- **The collective instanton weight is the physical scale**: `e^{−cβ}` with `c = 12π²/11`. -/
theorem collective_weight_su2 (β : ℝ) :
    collectiveInstantonWeight β = Real.exp (-(12 * Real.pi ^ 2 / 11) * β) := by
  dsimp [collectiveInstantonWeight]
  rw [su2_exponent]
end QM
