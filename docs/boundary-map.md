# Computing the uncomputable — a cartography of the boundary

The thing we actually want — *pin down the compactification* — is, in several
distinct senses, uncomputable. The mistake is to treat "uncomputable" as one wall.
It is **four different walls**, each with its own way around, and we have been
climbing them without naming them. This doc names them.

## The four senses of "uncomputable"

| sense | meaning | the move | our instance |
|---|---|---|---|
| **intractable** | answer exists, no feasible algorithm | prove intractability, or find structure that shortcuts it | search over W₀ (10⁵⁰⁰, not evolvable) |
| **unmeasurable** | answer exists, ground truth / data absent | compute the *deficit*, characterize what is measurable | m=0 verification; the KKLT tail |
| **underdetermined** | no unique answer exists | the answer is a *set*; compute its invariants and constraints | the measure / selection |
| **undecidable** | provably no algorithm | prove undecidability (Turing/Gödel) | not yet found in this project |

The key realization: **for each sense, "compute the uncomputable" has a different
meaning, and each is a positive act, not a surrender.**

- Intractable → *prove it's intractable* (a theorem), or find the hidden structure
  that makes it tractable (compressed sensing).
- Unmeasurable → *compute the deficit* (how far are we from measuring it), which is
  itself the answer.
- Underdetermined → *compute the set's invariants* (its uniformities, its
  constraints, its boundary), not the nonexistent point.
- Undecidable → *prove the undecidability* (a machine-checkable impossibility
  certificate).

## The boundary map (certified to date)

`src/pacland/limits.py` records the boundary as data, each entry with the question,
the sense of limit, the justification, and what *remains* computable:

1. **Search over W₀** — *intractable*. Justification: log-uniform W₀ (measured) →
   not learnable → not evolvable. Positive: the verifier survives.
2. **Verify a candidate today** — *unmeasurable*. Justification: m=0 → vacuous
   certificate. Positive: the deficit is computable and closes as oracles are built.
3. **KKLT tuning probability** — *unmeasurable*. Justification: target 7.6 nats
   below data. Positive: the prior is measured over 3.7 nats; extrapolation is
   flagged.
4. **The measure / selection** — *underdetermined*. Justification: verification ≠
   selection; the measure is a principle, not a computation. Positive: candidate
   measures are evaluable.
5. **The inverse problem (observables → compactification)** — *underdetermined*.
   Justification: no strong fingerprint in W₀, g_s, or the gauge couplings. Positive:
   constraints eliminate fast; answerable-by-elimination once richer observables exist.
6. **The full EFT spectrum** — *unmeasurable*. Justification: massless moduli at
   maximum_degree=0. Positive: a scoped build (instanton corrections), and the miner
   is calibrated to test it.
7. **Small-Λ typicality** — *unmeasurable*. Justification: SUSY V is AdS; Λ needs the
   de Sitter uplift, which is contentious. Positive: the log-uniform prior is measured;
   the Λ distribution follows once an uplift model exists.

## The reframe that makes this a program, not a resignation

We have been asking "how do we compute the uncomputable?" The answer is: **we don't —
we compute its boundary, and we certify each boundary point with the same rigor we
demanded of positive results.** Every negative result so far (search dead, deficit
total, KKLT tail, measure underdetermined) is not a failure; it is a *boundary point*,
and the accumulating set of boundary points **is** the theory of where computation
ends and physics begins.

This is the same move Valiant made: you cannot have exactness, so you have (ε, δ).
You cannot have the vacuum, so you have its boundary — and the boundary is
computable even when the vacuum is not.

## What to build next

The boundary map is a *map*, and a map is only as good as its completeness. The next
build is to fill it in: for each remaining question ("what is the compactification?",
"is the full EFT spectrum structured?"), certify its sense of uncomputability and its
positive content — until the map itself is the deliverable, independent of whether any
single question is ever answered.
