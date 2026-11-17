import Mathlib

/-!
# Perfect tensors and the HaPPY building block — the stabilizer characterization

A **perfect tensor** (Pastawski–Yoshida–Harlow–Preskill 2015) is a tensor with `2n` legs whose
every balanced `n | n` bipartition is, up to normalization, an isometry. For a **stabilizer state**
this is exactly the condition that its stabilizer group contains no non-identity element of weight
`≤ n`: no `n`-leg subsystem carries a stabilizer, so every `n`-party reduced density matrix is the
maximally mixed state — the **absolutely maximally entangled** (AME) property. (The density-matrix
equivalence is the standard stabilizer fact, `ρ_A = 2^{-|A|} Σ_{g ∈ S, supp g ⊆ A} g|_A`; this
file kernel-checks the concrete group-theoretic content, matching the algebraic style of `QM.MERA`.)

A Pauli string on `n` qubits is an `(X, Z)` mask: bit `i` is set iff qubit `i` carries `X` (resp.
`Z`); a qubit carrying both is `Y`, and the overall phase is irrelevant to the weight. The product
is bitwise `xor` on each mask.

Here we kernel-check the smallest perfect tensor — the **5-qubit `[[5,1,3]]` code coupled to a
reference qubit** through its logical operators, the HaPPY "hexagon" (6 legs, `n = 3`):

* the 4 code stabilizers have minimum weight 4 (the code is a distance-3 quantum code);
* adding the logical `Z` fixes a single state and gives minimum weight 3 (the `AME(5,2)` state);
* adding `Z_L ⊗ Z` and `X_L ⊗ X` on the reference qubit gives minimum weight 4 — the `AME(6,3)`
  state, i.e. the perfect tensor: every 3-qubit subsystem is maximally mixed.

Everything is kernel-checked by finite case analysis (`decide`); no `sorry`/`axiom`/`admit`.
-/

namespace QM

/-- A Pauli string on 6 qubits as an `(X-mask, Z-mask)`. -/
abbrev Pauli6 := Nat × Nat

/-- The weight of a 6-qubit Pauli: the number of qubits where `X` or `Z` (or both, `Y`) acts. -/
def pWeight (p : Pauli6) : ℕ :=
  (Nat.digits 2 (Nat.lor p.1 p.2)).sum

/-- The product of two Pauli strings (up to the ignored overall phase): bitwise `xor` per mask. -/
def pMul (p q : Pauli6) : Pauli6 :=
  (Nat.xor p.1 q.1, Nat.xor p.2 q.2)

/-- The product of the generators selected by the binary digits of `k` (bit `i` = include the
`i`-th generator in `gens`). -/
def prodOf (gens : List Pauli6) (k : Nat) : Pauli6 :=
  (gens.zip (List.range gens.length)).foldl
    (fun acc p => if Nat.testBit k p.2 then pMul acc p.1 else acc) (0, 0)

/-- The 4 stabilizer generators of the 5-qubit `[[5,1,3]]` code (qubits 0–4, qubit 5 unused):
`X Z Z X I`, `I X Z Z X`, `X I X Z Z`, `Z X I X Z`. -/
def codeGens : List Pauli6 := [(9, 6), (18, 12), (5, 24), (10, 17)]

/-- **The `[[5,1,3]]` code has distance ≥ 3.** Every non-identity element of its stabilizer group
has weight at least 4 (in fact exactly 4), so no single- or two-qubit subsystem carries a
stabilizer — the algebraic core of the code's 2-erasure-correcting property. -/
theorem code_min_weight :
    (List.range 16).all (fun k => decide (k = 0 ∨ 4 ≤ pWeight (prodOf codeGens k))) = true := by
  decide

/-- The 5 generators of the *fixed logical state* (one state in the code space): the 4 code
stabilizers plus the logical operator `Z_L = Z Z Z Z Z` (qubit 5 unused). -/
def fixedGens : List Pauli6 := [(9, 6), (18, 12), (5, 24), (10, 17), (0, 31)]

/-- **The `[[5,1,3]]` code state is `AME(5,2)`.** Every non-identity element of the fixed state's
stabilizer group has weight at least 3, so every two-qubit reduced density matrix is maximally
mixed — the 5 code qubits are absolutely maximally entangled across any 2 | 3 split. -/
theorem code_state_ame52 :
    (List.range 32).all (fun k => decide (k = 0 ∨ 3 ≤ pWeight (prodOf fixedGens k))) = true := by
  decide

/-- The 6 stabilizer generators of the HaPPY perfect tensor: the 4 code stabilizers (qubits 0–4)
plus the logical-operator couplings to the reference qubit (qubit 5), `Z_L ⊗ Z` and `X_L ⊗ X`. -/
def happyGens : List Pauli6 := [(9, 6), (18, 12), (5, 24), (10, 17), (0, 63), (63, 0)]

/-- **The HaPPY hexagon is a perfect tensor.** Every non-identity element of its stabilizer group
has weight at least 4, so no 3-qubit subsystem carries a stabilizer and every 3-party reduced
density matrix is maximally mixed: the `AME(6,3)` state — the smallest perfect tensor, the building
block of the HaPPY holographic code. -/
theorem happy_is_perfect_tensor :
    (List.range 64).all (fun k => decide (k = 0 ∨ 4 ≤ pWeight (prodOf happyGens k))) = true := by
  decide

end QM
