# Mechanical completion — route the decision to the AI, the glue to the CPU

> The one-line idea: **a formalization (and every other operation) splits into a
> *decision layer* and a *completion layer*. The decision needs judgement; the
> completion is mechanical and should run on the CPU against the kernel, not on AI tokens.**

## The split

| layer | what it is | who does it |
|---|---|---|
| **decision** | which theorem, which invariant, which route, which bijection | the AI (judgement) |
| **completion** | `rw`/`simp`/`ring`/`by_cases` glue, typeclass chasing, trivial subgoals, "which lemma has this name", the kernel check | the CPU (deterministic) |

Measured on the Cayley identity work: the `reverseZeroCycle_cycleOf_zero` proof is ~40 lines and
~35 of them are glue. The insight — *use `cycleOf_mul_of_apply_right_eq_self` instead of `cycleOf_inv`
to dodge the `SameCycle` decidability* — was one line. The ratio is ~90% completion, ~10% decision.
The AI has been paying for the 90%.

## The principle that makes it safe to automate

**The kernel is the source of truth, so mechanical search is free.**

An LLM suggestion is a heuristic; a kernel check is *truth*. The completion layer can therefore be
**brute-force**: try hundreds of cheap tactics, and let the kernel filter the garbage. There is no
risk of "the machine believing itself" because nothing is accepted without the kernel (or the
falsifier, or the CI — the same pattern in every discipline).

This is not new machinery — Isabelle's `sledgehammer`, Coq's `hammer`, Lean's `aesop`/`grind` already
do it. What is new here is making it a **named, estate-wide methodology** and a **program**, instead of
an implicit habit.

## The routing rule

Before any next step, ask: **is this a decision or a completion?**

- *"Which bijection proves det = Pf²?"* → decision → the AI.
- *"Apply `cycleOf_mul_of_apply_right_eq_self`, discharge the disjointness subgoal"* → completion → the CPU.
- *"Which invariant survives the SM?"* → decision.
- *"Recompute the tadpole on this manifold"* → completion.
- *"What should the site say?"* → decision.
- *"Ship `web/` to gh-pages"* → completion.

## The tools (Stage 1)

1. **`complete` tactic** — `pacland-proof/PaclandProof/Tactic/Complete.lean`. A single `complete`
   tactic that runs the mechanical battery in order (`aesop` → `simp_all` → `ring_nf` → `linarith` →
   `nlinarith` → `omega` → `norm_num` → `group` → `abel` → `positivity` → `tauto` → `grind`) and
   succeeds if *any* of them closes the goal. The AI writes `by complete` instead of hand-writing the
   glue; the kernel verifies whatever `complete` produced.

2. **`complete.sh`** — `pacland-proof/scripts/complete.sh`. The audit half: `lake build` (kernel check)
   plus a `sorry`/`axiom`/`admit` count per file, so "mechanical status" is a number you can read.

3. **The suggest→verify loop** (the AI's new role). The AI emits only a *skeleton* — the sequence of
   `rw [lemmaA, lemmaB]` / `apply lemmaC` with the gaps left as `sorry`. `complete` fills the gaps and
   the kernel checks the whole. The AI is promoted from typist to architect: it picks the lemmas and
   the order; the CPU does the rest.

## The honest boundary (do not overclaim)

The even-cycle ↔ ordered-pair-of-matchings bijection is a **decision**. No `simp`/`aesop` battery finds
it. `complete` absorbs the ~90% glue + verification *around* the decision; it does not make the decision.
The win is real because the token spend is dominated by the glue, but "mechanical completion" is a
completion layer, not an insight engine.

## Extrapolation — the same classifier on every operation

The split is discipline-independent; only the *verifier* changes:

| operation | decision (AI) | completion (CPU) | verifier |
|---|---|---|---|
| Lean proof | theorem / invariant / bijection | `complete` tactic, glue | `lake build` (kernel) |
| physics claim | which invariant to test | `validate_*.py` recompute | sympy exact + Rule-of-Three |
| falsification | which claim to attack | `sextant_node` falsifier | the simulator's verdict |
| site | the copy | `deploy-pages.sh` | fetch the live bytes |
| mesh | which machine / what for | `shell` job | `pass` requires output |

The methodology doc is the estate's **theory of what's mechanical**: a classifier you run before any
task, so the scarce resource — AI judgement — is spent only where it is irreducibly needed.
