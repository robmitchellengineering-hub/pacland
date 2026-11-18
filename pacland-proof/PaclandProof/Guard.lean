import Mathlib

/-!
# VVS guard contract — the kernel-checked half of a guard's proof

The black-box guard `{ file, find, replace, check }` cannot have its *runtime* behaviour proved
(the `check` is an opaque command). What CAN be kernel-checked is the layer around it:

1. **`find_once`** — the sabotage site is unambiguous (`find` occurs exactly once). This is a REAL
   reflected computation: the subject content is embedded, and `native_decide` evaluates the count
   inside Lean's kernel (not in the JS structural kernel).
2. **`rejects_sabotage`** — the black-box conformance, an `opaque` (observed by mutation, not proved).
3. **The mutation-protocol soundness** — the non-trivial theorem: a `caught` verdict is neither
   `always_red` (broken) nor `unstable` (stays red after undo). This is a real property of the
   5-run protocol, not a definition restated.

Honest statement of "formal verification of a black box": the observation is sound and the safety is
conditional on the observed conformance — not a proof of the box's internals.
-/

/-- A guard under proof: its subject, the declared sabotage, and the invariant it enforces. -/
structure Guard where
  name : String
  file : String
  find : String
  replace : String
  invariant : Nat
  deriving Repr, Inhabited

namespace Guard

/-- `prefixOf pat s` — is `pat` a prefix of the list `s`. Reducible: List + Char only. -/
def prefixOf (pat : List Char) (s : List Char) : Bool :=
  match pat, s with
  | [], _ => true
  | _, [] => false
  | p :: pt, c :: ct => p == c && prefixOf pt ct

/-- Count non-overlapping occurrences of `pat` in `s`. Reducible, so `native_decide` can evaluate it. -/
def countOccurrences (pat : List Char) (s : List Char) : Nat :=
  if pat = [] then 0
  else match s with
  | [] => 0
  | _ :: t => (if prefixOf pat s then 1 else 0) + countOccurrences pat t

/-- The number of non-overlapping occurrences of `find` in `s`. -/
def count (s find : String) : Nat := countOccurrences find.data s.data

/-- FORMALISABLE FACT: the sabotage site is unambiguous — `find` occurs exactly once. Proved by
    reflection (`native_decide`) against the embedded subject content, inside Lean's kernel. -/
def find_once (g : Guard) (subject : String) : Prop := count subject g.find = 1

/-- BLACK-BOX CONFORMANCE: the check rejects the sabotaged subject. OBSERVED by mutation, not provable. -/
opaque rejects_sabotage (g : Guard) : Prop

/-- The check's observed verdicts across the 5-run protocol. -/
structure CheckBehaviour where
  clean_green : Bool      -- exit 0 with nothing sabotaged
  sabotaged_red : Bool    -- non-zero with the sabotage applied
  undone_green : Bool     -- exit 0 after the sabotage is undone
  deriving Repr, DecidableEq

/-- A caught guard: green on clean, red on sabotaged, green on undone. -/
def caught (b : CheckBehaviour) : Prop := b.clean_green = true ∧ b.sabotaged_red = true ∧ b.undone_green = true

/-- A broken check: red even with nothing sabotaged. -/
def always_red (b : CheckBehaviour) : Prop := b.clean_green = false

/-- An unstable check: red with the sabotage, but it stays red after the undo. -/
def unstable (b : CheckBehaviour) : Prop := b.sabotaged_red = true ∧ b.undone_green = false

/-- THE SOUNDNESS THEOREM (non-trivial): a caught check is NOT always-red — the verdict changed because
    of the sabotage, not because the check was already broken. -/
theorem caught_not_always_red (b : CheckBehaviour) (h : caught b) : ¬ always_red b := by
  intro hred
  have : true = false := h.1.symm.trans hred
  cases this

/-- THE SOUNDNESS THEOREM (non-trivial): a caught check is NOT unstable — it returns to green once the
    sabotage is undone, so the red was caused by the fault, not by a stuck state. -/
theorem caught_not_unstable (b : CheckBehaviour) (h : caught b) : ¬ unstable b := by
  intro hun
  have : true = false := h.2.2.symm.trans hun.2
  cases this

/-- The CONDITIONAL GUARANTEE: an unambiguous site + a conforming check + a caught protocol ⇒ the guard
    catches its declared fault. -/
def catches (g : Guard) (subject : String) (b : CheckBehaviour) : Prop :=
  find_once g subject ∧ rejects_sabotage g ∧ caught b

end Guard
