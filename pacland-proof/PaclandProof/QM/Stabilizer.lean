import Mathlib

/-!
# Gottesman–Knill (algebraic core) — the Clifford group normalizes the Pauli group

The boundary of what a classical computer can simulate. A **stabilizer state** on `n` qubits is the
unique `+1` eigenstate of `n` commuting Pauli operators; instead of `2ⁿ` amplitudes it is described
by `n` Pauli operators (a `2n`-bit tableau). The **Clifford gates** (Hadamard `H`, phase `S`, CNOT)
are exactly those that conjugate Pauli operators back into the Pauli group; therefore a stabilizer
state evolved by Clifford gates and measured in the Pauli basis stays a stabilizer state, and the
whole computation is classically simulable in polynomial time — this is the **Gottesman–Knill
theorem**. Here we kernel-check the algebraic core: the single-qubit Clifford relations (H and S
conjugate X, Y, Z back to ±X, ±Y, ±Z), which is the "normalizer" property.

Consequence for "a quantum computer on regular hardware": classical bits can run **exactly** the
Clifford/stabilizer class for free; anything beyond it (a non-Clifford gate like `T`, which creates
the entanglement outside the stabilizer class) costs `2ⁿ` to simulate — the free column (see
`QM.Entanglement`: LOCC cannot create entanglement).
-/

namespace QM

noncomputable section

/-- Pauli `X`. -/
def pauliX : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]

/-- Pauli `Y`. -/
def pauliY : Matrix (Fin 2) (Fin 2) ℂ := !![0, -Complex.I; Complex.I, 0]

/-- Pauli `Z`. -/
def pauliZ : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- `√2` times the Hadamard gate (unnormalized, to keep the algebra rational). -/
def had2 : Matrix (Fin 2) (Fin 2) ℂ := !![1, 1; 1, -1]

/-- The phase gate `S = diag(1, i)`. -/
def phaseS : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, Complex.I]

/-- The adjoint of the phase gate `S† = diag(1, -i)`. -/
def phaseSdag : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -Complex.I]

/-- `H X H = Z` (unnormalized: `(√2 H) X (√2 H) = 2 Z`). The Hadamard conjugates X to Z. -/
theorem hxh : had2 * pauliX * had2 = 2 • pauliZ := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [had2, pauliX, pauliZ]

/-- `H Z H = X`. The Hadamard conjugates Z to X. -/
theorem hzh : had2 * pauliZ * had2 = 2 • pauliX := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [had2, pauliZ, pauliX]

/-- `H Y H = -Y`. The Hadamard conjugates Y to −Y. -/
theorem hyh : had2 * pauliY * had2 = (-2) • pauliY := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [had2, pauliY] <;> ring

/-- `S X S† = Y`. The phase gate conjugates X to Y. -/
theorem sxs : phaseS * pauliX * phaseSdag = pauliY := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [phaseS, pauliX, phaseSdag, pauliY]

/-- `S Z S† = Z`. The phase gate fixes Z. -/
theorem szs : phaseS * pauliZ * phaseSdag = pauliZ := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [phaseS, pauliZ, phaseSdag]

/-- `S Y S† = -X`. The phase gate conjugates Y to −X. -/
theorem sys : phaseS * pauliY * phaseSdag = -pauliX := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [phaseS, pauliY, phaseSdag, pauliX]

/-- **The Clifford group normalizes the Pauli group** (single-qubit core). Each of H and S maps
every single-qubit Pauli `{X, Y, Z}` to `±X, ±Y, ±Z` — a Pauli up to sign/phase. This closure is
the algebraic fact behind Gottesman–Knill: stabilizer states (defined by Pauli stabilizers) stay
stabilizer states under Clifford evolution, so the class is classically simulable. -/
theorem clifford_normalizes_pauli :
    (had2 * pauliX * had2 = 2 • pauliZ) ∧ (had2 * pauliZ * had2 = 2 • pauliX) ∧
    (had2 * pauliY * had2 = (-2) • pauliY) ∧
    (phaseS * pauliX * phaseSdag = pauliY) ∧ (phaseS * pauliZ * phaseSdag = pauliZ) ∧
    (phaseS * pauliY * phaseSdag = -pauliX) := by
  constructor
  · exact hxh
  constructor
  · exact hzh
  constructor
  · exact hyh
  constructor
  · exact sxs
  constructor
  · exact szs
  · exact sys

end

end QM
