# De Sitter conjecture test — first falsification benchmark

The de Sitter conjecture forbids stable de Sitter vacua (V > 0 with positive-definite
Hessian) in quantum gravity. Its refined form (Garg–Krishnan / Ooguri–Palti–Shiu–Vafa)
replaces "no dS" with a bound on the Hessian. Neither is expected to hold in *toy*
models — and that is exactly what makes a toy model the right first benchmark: any
guard claiming "no stable dS" that *passes* on this data is broken, because the data
contains stable dS by construction.

## Method

2683 critical points sampled by JAXVacua's natural (ISD) measure on the toy flux model
(`h12=2, model_ID=1, maximum_degree=0` — polynomial prepotential, no instantons). Each
point carries V, the Hessian eigenvalues, and `is_minimum`.

## Result

| category | count |
|---|---|
| critical points | 2683 |
| local minima | 585 |
| Minkowski minima (V ≈ 0, SUSY) | 354 |
| **stable de Sitter (V > 10⁻³, positive Hessian)** | **231** |
| of which, robust min-eigenvalue > 10⁻⁴ | 228 |

Examples: V = 23.26 (min eig 2×10⁻³), V = 8.16 (min eig 2×10⁻²), V = 4.65 (min eig
3.7×10⁻²) — all non-SUSY, clearly positive V, positive-definite Hessian.

## Honest interpretation

- **The toy model violates the (refined) de Sitter conjecture** — 231 stable dS vacua.
  This is *expected*: the conjecture constrains *realistic* quantum gravity /
  asymptotic constructions, not polynomial toy models, and "the naive dS conjecture is
  too strong" is a known refinement point.
- **This is not a refutation of the dS conjecture.** It is a **seeded counterexample**:
  a benchmark that any dS-conjecture *guard* must correctly classify as "toy, not a
  counterexample to the real conjecture." That is the mutation-testing discipline
  applied to the swampland — the first concrete artifact of the "falsify the swampland"
  approach (approach #3 in `PACLAND-V2-PLAN.md`).
- **What would actually falsify the conjecture** is a stable dS vacuum in a *realistic*
  compactification (full moduli stabilization, instantons, uplift). This benchmark is
  the calibration point for the guard that would detect that.

## Where this lives

- `scripts/sample_ds_test.py` — the sampler.
- `data/ds_test.json` — the 2683 critical points (V, is_minimum, is_susy, min_eig).
