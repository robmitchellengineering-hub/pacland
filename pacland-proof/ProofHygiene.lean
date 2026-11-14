import Mathlib
import PaclandProof.QM.OSAxioms
import PaclandProof.QM.Su2Curvature

/-!
# Proof hygiene — the D47 gate (the title must match the content)

A `scaffold:` theorem is one whose proof uses NO named theorem or axiom — it only applies its own
hypotheses (modus ponens, conjunction intro) and definitional scaffolding (constructors, type-class
instances). A `proof:`/`claim:` theorem uses at least one named theorem.

The classifier collects the proof term's constants, drops type-class instances (elaboration
scaffolding, `*inst*`) and everything that is not a `thmInfo`/`axiomInfo`, and reports whether any
named theorem is left. This sidesteps the type-argument leak without `inferType`.

Run: `lake env lean ProofHygiene.lean` (from `pacland-proof/`).
Self-test: `clay_assembly` must classify SCAFFOLD (its "mass gap" is `0 < (1 : ℝ)` handed back as
`exact ⟨hgap_strong, hOS3⟩`); `clay_assembly_final` and `su2_curvature_pos_strong` must classify
SUBSTANTIVE.
-/
open Lean Meta Elab

def constsOf (e : Expr) : Array Name :=
  e.foldConsts #[] (fun n acc => acc.push n)

def theoremValue (ci : ConstantInfo) : Expr :=
  match ci with
  | .thmInfo t => t.value
  | _ => default

def isInstanceName (n : Name) : Bool := (n.toString).contains "inst"

def isNamedTheorem (n : Name) : MetaM Bool := do
  if isInstanceName n then return false
  let ci ← getConstInfo n
  match ci with
  | .thmInfo _ => return true
  | .axiomInfo _ => return true
  | _ => return false

def isScaffold (n : Name) : MetaM Bool := do
  let ci ← getConstInfo n
  let cs := constsOf (theoremValue ci)
  for c in cs do
    if (← isNamedTheorem c) then return false
  return true

#eval! do
  let clay ← isScaffold ``QM.clay_assembly
  let clayFinal ← isScaffold ``QM.clay_assembly_final
  let su2 ← isScaffold ``QM.su2_curvature_pos_strong
  if clay && !clayFinal && !su2 then
    return "SELF-TEST PASS: clay_assembly=SCAFFOLD, clay_assembly_final=SUBSTANTIVE, su2_curvature_pos_strong=SUBSTANTIVE"
  else
    return s!"SELF-TEST FAIL: clay={clay}, clayFinal={clayFinal}, su2={su2}"
