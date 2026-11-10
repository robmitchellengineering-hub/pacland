import Mathlib

/-!
# Mechanical completion

A single `complete` tactic that runs the cheap, deterministic tactic battery until one closes the
goal. This is the "completion layer" of `docs/mechanical-completion.md`: the AI emits the decision
(the lemma sequence), and `complete` fills the glue, with the kernel as the only acceptance test.

Usage: `by complete` at the end of a goal. If it closes the goal, the glue was mechanical; if it
does not, the remaining goal is the *decision* (which invariant / lemma / route) — the AI's job.
-/

/-- Runs the mechanical battery: `aesop`, `simp_all`, `ring_nf`, `linarith`, `nlinarith`, `omega`,
`norm_num`, `group`, `abel`, `positivity`, `tauto`. Succeeds iff any of them closes the goal. -/
macro "complete" : tactic =>
  `(tactic| (first
    | aesop
    | simp_all
    | ring_nf
    | linarith
    | nlinarith
    | omega
    | norm_num
    | group
    | abel
    | positivity
    | tauto))
