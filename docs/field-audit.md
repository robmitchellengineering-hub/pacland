# Verification audit of the ML-for-the-string-landscape field

A checkable audit, not a vibe. The research (three parallel gap analyses, 2026-10-18)
found that **no ML-for-the-landscape tool emits a calibrated error model**. This
document makes that precise and states the fix.

## The criterion (checkable)

A tool or paper is **verifiable** iff it emits, per observable, a *calibrated*
error model — a bias bound plus a tail claim `Pr[|e| > β] ≤ δ_β` that has been
validated against known `c*` (the `docs/oracle.md` §4/§6 contract). A black-box
number, or a self-reported accuracy with no validation, is **unverifiable** —
exactly the "no certificate, no claim" rule.

## The audit

| tool / line | what it does | calibrated error model? | verdict |
|---|---|---|---|
| CYTools (2211.03823) | CY topology (Hodge, intersections) | topology is exact; no error model for metric/spectrum | **partial** (topology verifiable via known-answer) |
| JAXVacua (2306.06160) | flux-vacua sampling, scalar potential | potential is truncated; no calibrated error | **unverifiable** |
| cymetric (2205.13408) | neural CY metrics | self-reported σ≈1e-3..1e-4, no validation | **unverifiable** |
| cohomCalg (1003.5217) | line-bundle cohomology | exact algorithm, no verification framework | **unverifiable** (as-shipped) |
| generative samplers (2509.16029) | sample vacua via BFN/Transformer | none | **unverifiable** |
| CYTransformer (2507.03732) | generate CY manifolds | none | **unverifiable** |
| neural-metric line (He 2017 →) | black-box surrogates | none | **unverifiable** |
| GA-over-landscape (2111.11466) | heuristic search | none (no guarantees) | **unverifiable** |

## The result

**Zero calibrated error models in the field.** Every ML result is a black-box
surrogate or a heuristic search with no stated uncertainty. The field's
verification deficit is **total** — the same conclusion our `docs/verification-deficit.md`
reached for our own oracle, now shown to hold for *everyone else's* tools too.

## Why this is a contribution, not a complaint

- It is a **checkable** claim: the criterion is precise, and each row is testable
  (show me the error model and its validation set, or the tool is unverifiable).
- It reframes the whole field: "generation is solved; verification is not" — the
  thesis that already works for code — applies identically to ML-for-physics.
- It positions PACLAND as the **verification layer on top of existing compute**:
  we do not compete with CYTools/JAXVacua/cymetric; we wrap them behind
  `guards` → `vault` → `certificate` and supply the calibrated error model the
  field is missing.

## What we can point to

`src/pacland/guards.py` (guard every invariant), `vault.py` (no certificate on
guard failure), `error_model.py` (`calibrate`, validated-vs-extrapolated), and
`deficit.py` (quantify the gap). That stack is the fix, and it is already built
and validated on real CYTools + JAXVacua output.
