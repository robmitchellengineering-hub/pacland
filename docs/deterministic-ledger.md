# The deterministic ledger — every result that is exact in its use

**A result is *deterministic in use* when it ends in an exact answer — a count, a closed form, or a
machine-checked proof — with no sampler, no probability, no run-to-run variance.** This is the inventory
of those results, so "deterministic in use" is a category we can point at, not one figure on a page.

The scoped flagship is `docs/deterministic-in-use.md` (the flux-vacua count). The same standard, applied
elsewhere, already covers every row below. Each row names what is exact and how it was verified — a row
that needs a sampler to settle does not belong here by definition.

## Flux sector

| result | what is exact | verified by | doc |
|---|---|---|---|
| vacuum count | 43,046,720 primitive orbits at `b3 = 8`; `count(N) = [x^N] P(x)^(b3/2)` | full enumeration + a second implementation sharing no code | `deterministic-in-use.md` |
| invariant ring | the duality-invariant ring is `ℂ[N]` — one generator | Weyl FFT, machine-checked (Lean, degrees 1–4) | `constraint-first-theorem.md` |
| measure dimension | the measure space has dimension **exactly** `b3` | proved, not fitted | `deterministic-in-use.md` |

## The exact T⁶ oracle

| result | what is exact | verified by | doc |
|---|---|---|---|
| toroidal orbifold | periods, Kähler metric, tadpole `FᵀΣH`, `W`, `g_s`, KK/winding tower, geodesic distance — all closed form | 21/21 numerical + 8/8 symbolic (sympy, zero tolerance) | `t6-exact-oracle.md` |

## The theorem tower (machine-checked)

| result | what is exact | verified by | doc |
|---|---|---|---|
| Mitchell's Uniqueness | the D3 tadpole `FᵀJH` is the unique bilinear symplectic invariant | 6/6 symbolic + Lean (n=1 and general n) | `mitchell-uniqueness-theorem.md` |
| Constraint-First | the tadpole generates the entire invariant ring | 5/5 degrees exact | `constraint-first-theorem.md` |
| Mitchell's Completeness | finitely many orbits per tadpole; content `d = gcd(F,H)`, `d² | N` | 6 exact + 2 numeric | `mitchell-completeness-theorem.md` |
| Full-duality | the no-go holds for the full group `Sp × SL(2,ℤ)` | 5/5 symbolic | — |
| Complete Exact Structure | the exact content is constraints + labels, nothing else | assembly of the four above | `complete-exact-structure.md` |

## Standard Model

| result | what is exact | verified by | doc |
|---|---|---|---|
| anomaly cancellation | hypercharges satisfy all gauge-anomaly conditions | 5/5 exact (sympy) | `sm-frontier.md` |
| hypercharge uniqueness | anomaly conditions force the hypercharges up to normalisation + u↔d swap | 4/4 exact | `sm-frontier.md` |
| generation count | `N_gen = 3 = |χ|/2` (topological index) | exact | `sm-frontier.md` |
| parameter count | 19 free parameters = orbit-space dimension | rank test, exact | `sm-frontier.md` |

## Arithmetic

| result | what is exact | verified by | doc |
|---|---|---|---|
| conifold coefficients | exact rationals `37/30, 2309/1800, …` | exact arithmetic; PSLQ null above 10⁶ for the basis change | `plan-bold-claims.md` (B2) |
| `max|N| = b3` | the invariant content is bounded exactly in the enumerable window | exact ladder | `deterministic-in-use.md` |

## What this list is not

Not a claim about nature, and not "string theory is solved". Each row is exact *in its use* — within its
own stated scope. The honest split stays the same as everywhere in PACLAND: **what is exact here is
constraints, labels, counts and arithmetic; the values are not.**
