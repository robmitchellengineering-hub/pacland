import Mathlib
import PaclandProof.QM.PerfectTensor

/-!
# The bulk→boundary isometry — the algebraic core (logical-operator validity)

A stabilizer code on `n` qubits encodes one logical qubit exactly when its **logical operators**
`X_L`, `Z_L` form a Pauli algebra on the code space: they square to the identity, **anticommute**,
and each **commutes with every code stabilizer**. That is the stabilizer form of "the encoding
`E : ℂ² → (ℂ²)^⊗n` is an isometry" — the map that takes the bulk qubit to the boundary is well
defined and preserves the algebra, so it is the HaPPY **bulk→boundary isometry** (for the single
tile / the 5-qubit `[[5,1,3]]` code).

This file kernel-checks exactly those facts. The full matrix statement (`E†E = I`) and the
entanglement-wedge / complementary-recovery direction build on this; they live one layer up (the
n-qubit matrix / density-matrix layer), and this is the algebraic floor they stand on.
-/

namespace QM

/-- Popcount of a bitmask (reuses the `Nat.digits` base-2 expansion). -/
def popcount (n : Nat) : Nat :=
  (Nat.digits 2 n).sum

/-- Two Pauli strings **commute** iff the symplectic overlap `|X_p ∩ Z_q| + |Z_p ∩ X_q|` is even
(up to the ignored phase). -/
def commutes (p q : Pauli6) : Bool :=
  ((popcount (Nat.land p.1 q.2)) + (popcount (Nat.land q.1 p.2))) % 2 == 0

/-- Two Pauli strings **anticommute** iff they do not commute. -/
def anticommutes (p q : Pauli6) : Bool :=
  ! commutes p q

/-- The logical `X` operator `X_L = X X X X X` (qubit 5 — the reference — untouched). -/
def logicalX : Pauli6 := (31, 0)

/-- The logical `Z` operator `Z_L = Z Z Z Z Z`. -/
def logicalZ : Pauli6 := (0, 31)

/-- `X_L` squares to the identity. -/
theorem logicalX_sq : pMul logicalX logicalX = (0, 0) := by
  decide

/-- `Z_L` squares to the identity. -/
theorem logicalZ_sq : pMul logicalZ logicalZ = (0, 0) := by
  decide

/-- **The code encodes one qubit.** `X_L` and `Z_L` anticommute — the single logical qubit's Pauli
algebra. -/
theorem logicalXZ_anticommute : anticommutes logicalX logicalZ = true := by
  decide

/-- **The logical operators live in the normalizer.** Each of `X_L`, `Z_L` commutes with every one
of the four code stabilizers, so the code space is preserved by the encoded Pauli algebra — the
stabilizer form of "the encoding isometry is well defined on the code space". -/
theorem logical_commute_with_stabilizers :
    codeGens.all (fun g => commutes logicalX g && commutes logicalZ g) = true := by
  decide

end QM
