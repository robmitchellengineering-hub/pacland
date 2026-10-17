# Architecture — six layers

Each layer is independently buildable; they are ordered so that the verification core
(L3) is pure and testable without the physics-heavy oracle being complete first.

```
L1 Encoding ──► L2 Physics oracle ──► L3 Valiant verifier ──► certificate
                    ▲                       │
                    │                       ▼
              L4 Evolvability ◄────────── fitness
                    │
                    ▼
              L5 Educability loop (accumulated verified knowledge)
                    │
                    ▼
              L6 Measure layer (selection — the physics hole)
```

---

## L1 — Encoding

Turn a vacuum into a **genotype** (searchable representation).

- Discrete/topological part: Calabi-Yau topology invariants (`h^{1,1}`, `h^{2,1}`,
  triple intersection numbers), sourced from a database (e.g. Kreuzer–Skarke).
- Discrete/quantized part: flux vectors `F₃, H₃ ∈ H³` (integers, tadpole-bounded),
  brane wrapping classes.
- Continuous part: complex-structure moduli `zᵃ`, Kähler moduli `tⁱ`.

The discrete and continuous parts are kept **separate** because mutation geometry
differs (Hamming-like vs Euclidean). See [`encoding.md`](encoding.md).

## L2 — Physics oracle (the labeler)

Compute the **phenotype** (observables) from a genotype: massless spectrum, gauge group,
charged matter, Yukawa couplings, and the cosmological constant after moduli
stabilization.

- Wraps existing tools: CY metric solvers (neural-metric / Donaldson approaches),
  cohomology and spectrum computation, flux-vacuum enumerators, Swampland constraint
  checkers, EFT extraction.
- **Load-bearing requirement:** every output is a vector of observables **plus a
  per-observable error model** (bias bound and noise). Without this, L3's bounds are
  fiction.

## L3 — Valiant verifier (the core)

Take a candidate vacuum and emit a **Valiant certificate**: a tuple

```
(ε, δ, n, agreement, oracle_bias)
```

meaning *with probability ≥ 1−δ, the true physics of this vacuum is within ε of
observation.*

- Sample `n` observables per a measure `D`, with `n` set by the PAC sample-complexity
  bound for the observable class's VC dimension.
- Compose a **two-level bound**: oracle bias (systematic) ⊗ sampling variance
  (statistical). See [`verification.md`](verification.md).

This is the whole point: replace "prove it's our universe" with "certify it's
observationally indistinguishable within stated tolerance."

## L4 — Evolvability engine (the search)

A population of vacua; fitness = verifier agreement; mutation operators = flux changes,
brane moves, and conifold transitions (topology change).

Run it **per Valiant's evolvability model**, not as a raw genetic algorithm. His theorem
— *any evolvable concept class is efficiently learnable* — then yields the complexity
ceiling: **selection can only find our vacuum if the `compactification → observables`
map is efficiently learnable in Valiant's sense.** That is the single governing question
for the whole system.

## L5 — Educability loop (knowledge transfer)

Persist verified partial results — vacuum classes ruled in or out, constraint regions,
structure in the map — and *educate* each new search generation with them instead of
blind mutation. This is Valiant's 2024 **educability** notion applied literally:
accumulation of verified knowledge across the search is what separates an ecorithm from
a search.

## L6 — Measure layer (selection — the physics hole)

Verification certifies *membership* in the "looks-like-our-universe" subset; it does not
say *why*. The **landscape measure** (cosmological dynamics, eternal inflation) is the
only thing that turns a verified vacuum class into unification.

- Treat the measure as a **hypothesis class in its own right**, PAC-verified against
  cosmological observables (CMB, large-scale structure).
- This layer is the honest boundary: **Valiant verification cannot supply it.** It
  constrains and is constrained by the measure, but does not derive it.

---

## Build order (recommended)

1. **L3 formalization** — pure math, no physics code. Highest-value first deliverable.
2. **L1 encoding** on a *tiny* flux-vacuum subclass — gets a real genotype in hand.
3. **L2** as a thin wrapper over one existing solver with an explicit error model.
4. **L4** once L2+L3 exist, on the tiny subclass.
5. **L5** as the search accumulates data.
6. **L6** only as a framing device — it is a research problem, not a build target.

## Deliberate exclusions

- No black-box learned surrogate that cannot emit a certificate.
- No claim that search alone selects; L6 exists to keep that honest.
- No early optimization toward the full 10⁵⁰⁰ landscape — the learnability question is
  answerable on small classes first.
