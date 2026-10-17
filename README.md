# PACLAND

**Probably Approximately Correct Landscape** — a Valiant-verification system for the string landscape.

> **Start with [`ROADMAP.md`](ROADMAP.md)** — the whole argument in paper form: abstract,
> section-by-section, and a ledger of what's proven vs conjectured vs open.

## Thesis

Replace the impossible goal of string-theory unification — *prove that one vacuum is our
universe* — with the achievable goal: **characterize the learnability structure of the
`compactification → low-energy physics` map, and certify candidate vacua as
observationally indistinguishable within an explicit (ε, δ) tolerance.**

The system is built on three ideas from Leslie Valiant:

| Idea | Role here |
|---|---|
| **PAC learning** (1984) | The verification semantics — "with probability ≥ 1−δ, error ≤ ε" |
| **Evolvability** (2008, *Probably Approximately Correct*) | The search engine, bounded by the theorem that any evolvable class is efficiently learnable |
| **Ecorithm / educability** (2013, 2024) | The meta-loop — verified knowledge transfers across search generations |

## Status

**Spec phase.** No physics code yet. The documents under `docs/` are the authoritative
design; implementation is a later, separable phase.

## What this is NOT

- It does **not** find "the" vacuum — ~10⁵⁰⁰ defeats any search.
- It does **not** unify by itself: **verification ≠ selection**. The landscape *measure*
  (a dynamical/cosmological reason *this* vacuum, not *that* one) is a separate, open
  physics problem.
- The physics oracle is an **approximate simulator, not ground truth** — verification
  must bound oracle error, not assume it away.

## Repo map

- [`ROADMAP.md`](ROADMAP.md) — the linear argument as a paper outline (start here)
- [`docs/architecture.md`](docs/architecture.md) — the six layers (L1–L6)
- [`docs/verification.md`](docs/verification.md) — the Valiant certificate and the two-level error bound (conceptual)
- [`docs/verification-formal.md`](docs/verification-formal.md) — the rigorous bound, cost model, and formal learnability conjecture
- [`docs/evolvability.md`](docs/evolvability.md) — L4 formalization: Valiant's evolvability model over the landscape
- [`docs/educability.md`](docs/educability.md) — L5 formalization: verified knowledge transfer and revision
- [`docs/observable-measure.md`](docs/observable-measure.md) — the toy observable measure `D`, and what it reveals about the certificate
- [`docs/oracle.md`](docs/oracle.md) — L2 spec: the oracle interface, error model, and calibration protocol
- [`docs/encoding.md`](docs/encoding.md) — the genotype encoding and mutation operators
- [`docs/open-questions.md`](docs/open-questions.md) — limits, the measure problem, and the learnability conjecture

## Non-goals (so the project stays honest)

- No claim of a unique prediction. A verified vacuum class is a *necessary*, not
  *sufficient*, step toward unification.
- No black-box ML. The statistical guarantees are the product; a learned surrogate that
  cannot emit a certificate is out of scope.
