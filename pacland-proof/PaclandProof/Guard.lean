import Mathlib

/-!
# VVS guard contract — the kernel-checked half of a guard's proof

The black-box guard `{ file, find, replace, check }` cannot have its *runtime* behaviour proved
(the `check` is an opaque command). What CAN be kernel-checked is the layer around it:

1. **`find_once`** — the sabotage site is unambiguous (`find` occurs exactly once), so the mutation
   protocol cannot sabotage "the wrong copy". FORMALISABLE, proved by reflection against the subject.
2. **`rejects_sabotage`** — the black-box conformance, an `opaque` (observed by mutation, not proved).
3. **`catches`** — the CONDITIONAL GUARANTEE: an unambiguous site + a conforming check means the
   guard catches its declared fault. The assume–guarantee theorem.

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

/-- The number of non-overlapping occurrences of `find` in `s`. -/
def count (s find : String) : Nat := (s.splitOn find).length - 1

/-- FORMALISABLE FACT: the sabotage site is unambiguous — `find` occurs exactly once in the subject. -/
def find_once (g : Guard) (subject : String) : Prop := count subject g.find = 1

/-- BLACK-BOX CONFORMANCE: the check rejects the sabotaged subject. OBSERVED by mutation, not provable. -/
opaque rejects_sabotage (g : Guard) : Prop

/-- THE CONDITIONAL GUARANTEE: unambiguous site + conforming check ⇒ the guard catches its fault. -/
def catches (g : Guard) (subject : String) : Prop := find_once g subject ∧ rejects_sabotage g

/-- The assume–guarantee in one step: given the site is unambiguous and the box conforms, the guard
    catches its declared fault. This is the whole value of the layer — safety is conditional on a
    named, checkable assumption, not on trust. -/
theorem catches_intro (g : Guard) (subject : String)
    (h_site : find_once g subject) (h_box : rejects_sabotage g) :
    catches g subject :=
  ⟨h_site, h_box⟩

/-- SOUNDNESS of the sabotage: an unambiguous site means there is exactly one occurrence to replace,
    so the mutation is deterministic. -/
theorem sound_site (g : Guard) (subject : String) (h : find_once g subject) :
    count subject g.find = 1 := h

end Guard
