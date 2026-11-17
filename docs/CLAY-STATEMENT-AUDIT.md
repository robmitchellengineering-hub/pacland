# Audit — the formal-conjectures Yang–Mills statement (PR #7636)

Fetched and read the diff of [`google-deepmind/formal-conjectures` #7636](https://github.com/google-deepmind/formal-conjectures/pull/7636)
("feat(millennium): formalise 4D Yang-Mills Existence and Mass Gap conjecture", by Cloudhabil).
1569 lines, `FormalConjectures/Millennium/YangMills.lean`.

## Verdict: a legitimate anchor, not a fake solution

The file correctly states the Clay problem as an **open conjecture** — the terminal theorems are
`sorry` and tagged `@[category research open, AMS 81]`:

- `yang_mills_existence_and_mass_gap` (the full statement) — `sorry`, tagged "open". ✓
- `yang_mills_sun_mass_gap` / `yang_mills_su2_mass_gap` / `yang_mills_su3_mass_gap` — `sorry`, "open". ✓

This is exactly how an open conjecture *should* be formalized. It is **not** one of the unrefereed
"solutions" the search surfaced. It captures all four Jaffe–Witten clauses, which our tower never did:
1. Wightman axioms (Hilbert space, Poincaré rep, energy-momentum, vacuum, microcausality).
2. Local gauge-invariant curvature fields + Wilson loops + short-distance asymptotic freedom (`b₀ > 0`).
3. Mass gap `Δ > 0` on `(ℂΩ)ᵀ` (as `HasMassGap`).
4. Osterwalder–Schrader Euclidean framework (E0'–E4 + reconstruction).

## The caveats (why "don't trust, verify" still applies)

1. **`sun_compactSimpleLieGroup` is `sorry`** — the textbook fact "SU(N) is a compact, connected,
   non-abelian simple Lie group" is *assumed*, not proven. It's provable, so a `sorry` here is a
   fidelity gap, not a statement of the open problem.
2. **`osterwalder_schrader_reconstruction` is `sorry`** — the OS reconstruction is a *known theorem*
   (Osterwalder–Schrader 1973/75), so it should be proven, not assumed. (Formalizing it is large, but it
   is not the open rung.)
3. **The fidelity-critical definitions** — `CompactSimpleLieGroup`, `CurvaturePolynomialAlgebra`,
   `WightmanQuantumYangMills`, `OsterwalderSchraderYangMills` — encode the axioms and need expert review
   against Jaffe–Witten's actual text. These are where a formalization silently goes wrong.

## What this means for pacland

This is the **anchor to measure against** (Claude's #1). It is more faithful and more complete than
anything in our tower. The right move is **not** to re-derive it from scratch, but to:

1. **Cross-check its definitions** (`CompactSimpleLieGroup`, the curvature-polynomial algebra, the mass-gap
   clause) against Jaffe–Witten §4 — the fidelity review.
2. **Adopt or mirror** the parts that are faithful, and note the parts that are `sorry` where they should
   be proven (the group fact, the OS reconstruction).
3. **Reuse it as the ruler** for the gate protocol: our `Su2Haar` / Doeblin / Dobrushin work is measured
   against `HasMassGap` as stated there, not against the fitted referee.

No conclusion is drawn about correctness of the `sorry` theorems — they are open by design.
