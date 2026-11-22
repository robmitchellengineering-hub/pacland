# Proof-verification standard — the four criteria (adopted 2026-11-22)

Adopted from the Lean + Mathlib communities' certification of the Alpöge Riemann-Hypothesis proof
([Lean verification of the Riemann Hypothesis](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)).
The same four criteria are the standard every theorem in `pacland-proof` must meet before it is a
verified result — not just "compiles", but *is the right statement, provably checked*.

## The four criteria

1. **The statement is correct.** The theorem states the canonical, vetted `Prop` (e.g.
   `QM.refereeScalingLaw`, `QM.volumeUniformGap`, `FSSInfraredBound.gaussianDomination`) — the def is the
   statement, and the def is part of the tower, not an ad-hoc local restatement.
2. **The library compiles.** `lake build` is green with no errors and no `sorry`/`admit`/`axiom`
   (the kernel's "green" is not enough — a placeholder compiles; the tower refuses it).
3. **The code proves the correct statement.** The theorem's conclusion is *exactly* the canonical
   def — verified by isolating the statement (an import-only file that restates the def) and checking
   the theorem concludes that def, not a lookalike.
4. **The proof is valid, independently.** The proof is accepted by Lean's kernel (via `lake env lean`)
   and, for the highest bar, by an independent checker (`con-leche` / `con-ron`) that carries its own
   formal guarantee of soundness — a second opinion on the kernel.

## How the tower enforces each criterion today

| criterion | mechanism in `pacland-proof` |
|---|---|
| 1. statement correct | the target is a `def` in the tower (`refereeScalingLaw`, `volumeUniformGap`, `gaussianDomination`) |
| 2. compiles | `lake build` + the `_check_lean` refusal of `sorry`/`admit`/`axiom` |
| 3. proves the right statement | the theorem's type is the def itself (the kernel unifies it — no lookalike possible) |
| 4. independent validity | `lake env lean` (kernel) today; `con-leche`/`con-ron` as the independent layer to add |

`scripts/verify_theorem.sh <path.lean>` runs criteria 2–4 on a given theorem file (build, `lake env lean`,
and a note on the independent checker), so the standard is a runnable check, not a paragraph.
