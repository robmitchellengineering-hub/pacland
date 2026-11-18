# Fidelity review — the Gross committee's existence-proof repo (`yang-mills-group/OpenAI-YM-20261028`)

Fetched and read the 5 public statement files (787 lines): `Challenge.lean`, `ChallengeSpec.lean`,
`PublicWilson.lean`, `PublicTheory.lean`, `PublicView.lean`. This is Claude's plan-A "crux": does the
statement actually match the Clay description?

## Verdict: serious and largely faithful, with two genuine fidelity gaps

The formalization is real and detailed — not vacuous, not scaffolded. But two clauses are **weaker than
Clay**, exactly the two Claude flagged.

## Findings, against Claude's five questions

**Q1 — the running coupling is NOT pinned to Yang–Mills. CONFIRMED (the biggest gap).**
`WilsonRegularity.running` (ChallengeSpec.lean:13) only asks `β/log(1/mesh) → slope` for **some positive
slope**. The slope is a free parameter — it is NOT the YM beta-function value `11C₂/(48π²)`. The README
confirms "MS-bar matching out of scope". So the short-distance asymptotic-freedom clause (Clay's clause 2)
is reduced to "the coupling runs with *some* log, not *the* YM log." This alone means the existence proof
does not tie the limit to 4D Yang–Mills as Clay states it.

**Q2 — the Wilson family is the plain Wilson action + product Haar. FIDEL.**
`wilsonLaw` (PublicWilson.lean:29) = `Measure.pi (fun _ => haar)`.withDensity `e^{−β·wilsonEnergy}`, and
`wilsonEnergy` (line 25) is the standard plaquette action `Σ(1 − Re tr U_p/(n+1))`. `haar` is constrained
by `probability` + `invariantHaar`. No hidden free parameters in the family itself.

**Q3 — subsequence-only limit, no uniqueness. CONFIRMED (a real gap).**
`JointExistence` (ChallengeSpec.lean:186) is `∀ g IsSimple, ∃ C, WilsonRegularity C ∧ ∀ p StrictMono,
∃ q StrictMono, ∃ T : Hierarchy C, T.Properties (p ∘ q)`. The `∃ q` (further subsequence) and the
existential `T` mean the theory is constructed along a subsequence with **no uniqueness of the
infinite-volume limit**. Clay asks for the theory to *exist*; this proves existence up to a subsequence.

**Q4 — non-freeness. Present, genuine.** `TraceTest.excludes` (line 175) asserts the grade-4 trace
two-point `traceTwo` is **not** a finite sum of free Wick profiles (`r⁸·log²(1/r)` short-distance
behavior, amplitude `3·dim 𝔤/π⁴`). This is a real non-triviality clause.

**Q5 — Wightman clauses are non-trivial.** `Reconstructed` (lines 117–143) carries `normalized`
(probability measure), `fullSupport`, `acts` (∃ a non-zero field), `injective`/`covers`/`represents`
(the field↔label correspondence is surjective/injective), and `mixture` (character-mixture consistency).
These force a non-trivial structure.

## The two gaps, precisely

1. **The running slope is free** — the statement does not tie the continuum limit to YM's actual
   beta function (only "some positive slope"). This is the single most important fidelity gap.
2. **Subsequence-only + non-unique infinite-volume limit** — weaker than "the theory exists".

Both match Claude's prior flags and the committee's own caveat ("doesn't fully understand the proof …
mass gap untouched"). The existence claim, even if the kernel proof is accepted, establishes a
**YM-flavored relativistic QFT along a subsequence**, not the full Clay existence clause.

## Not yet checked (next steps in Claude's plan A)

- `PublicTheory.lean` + `PublicView.lean` Wightman-axiom instance audit (Q5 details, `Classical` open,
  local notation/macros).
- Negative controls (zero action, degenerate measure, abelian group).
- The mass-gap interface: does `Reconstructed` expose a Hamiltonian to state `Δ > 0` against?
- Reproduce the build + standalone Comparator + `#print axioms`.
