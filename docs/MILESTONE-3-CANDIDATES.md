# Milestone 3 — the three candidate inequalities and their falsifiers

Status: the reduction, 2026-11-21. This is the step between "SEXTANT located the missing bound"
and "the bound is proven": each cross-field candidate is written as a **precise inequality**, with
its **falsifier** and the **evidence we already have**. None of these is claimed to hold — that is
the open question, and the falsifiers are the judge.

Notation. `μ(A) ∝ e^{-S(A)}` is the Yang–Mills measure; `M = -∇·D` is the Faddeev–Popov operator in
the adjoint rep (Landau gauge); `λ_min(M)` is its lowest eigenvalue; `Γ(f) = |∇f|²` is the carré du
champ; `Ent_μ(f²) = ∫ f² log f² dμ - (∫ f²) log(∫ f²)` is the entropy.

## Candidate 1 — orbifold Bakry–Émery curvature (differential geometry)

**The inequality.** On the gauge-orbit quotient (where the FP operator `M` is the metric), the
Bakry–Émery condition

```
Γ₂(f) ≥ K · Γ(f)        for all f,        K = λ_min(M) > 0
```

would give a spectral gap `λ₁ ≥ K` and the log-Sobolev bound. The transfer claim is: *the YM measure
on the orbit space satisfies CD(λ_min(M), ∞)*.

**Falsifier.** `λ_min(M) → 0` — the Gribov horizon — which sends `K → 0` and kills the gap. This is
exactly the mechanism the horizon plan probes.

**Evidence.** `λ_min(M) ≈ 2.4` flat in `N` (6→12) and in β (2.2→2.6), gauge-invariant under Landau
and FMR fixing. So `K` is positive at finite N. **Open:** does `λ_min(M)/a²` stay positive in the
continuum — i.e. is `λ_min ≈ 2.4` really the UV cutoff and not a continuum-gap shadow?

## Candidate 2 — log-Sobolev on the gauge-fixed slice (functional inequalities)

**The inequality.** For the FMR-gauge-fixed measure (FP determinant included),

```
Ent_μ(f²) ≤ (2/ρ) ∫ Γ(f) dμ,        ρ ~ λ_min(M)
```

which gives `λ₁ ≥ ρ`. The transfer claim: *the gauge-fixed YM measure has a log-Sobolev constant
controlled by the FP gap.*

**Falsifier.** `ρ → 0` as `λ_min(M) → 0` — the log-Sobolev constant blowing up at the horizon.

**Evidence.** Same as Candidate 1: `λ_min(M)` positive at finite N ⇒ `ρ` bounded at finite N.
**Open:** the continuum limit of `ρ`, which is the same `λ_min(M)/a²` question.

## Candidate 3 — block-spin RG contraction (renormalisation)

**The inequality.** One block-spin step `T: μ_N → μ_{N/2}` is a contraction in some metric `d`,

```
d(Tμ, Tν) ≤ e^{-Δ} · d(μ, ν),        Δ > 0
```

and the mass gap **is** the contraction rate `Δ`. The transfer claim: *the RG flow of YM contracts
with a rate bounded away from 0, and that rate is the mass gap.*

**Falsifier.** `e^{-Δ} → 1` (no contraction) — the correlation length not shrinking under blocking,
or the flow landing on the trivial Gaussian fixed point.

**Evidence.** None yet — this is the one falsifier not built. Its spec is
`docs/BLOCK-SPIN-RG-FALSIFIER.md`; the acceptance test is a mutation of the block projection to the
identity returning `ρ ≈ 1` while the real projection returns `ρ > 1`.

## What this reduction shows

Candidates 1 and 2 are **the same test**: `λ_min(M)` staying positive in the continuum. Candidate 3
is the genuinely independent one — the RG contraction rate, not the FP gap. So the open work is two
measurements, not three:

1. the **continuum FP gap** `λ_min(M)/a²` (needs the Wilson-flow scale, since the Polyakov string
   tension came back noise-dominated);
2. the **block-spin contraction rate** (needs the block-spin falsifier built).

If (1) stays positive and (2) is bounded away from 1, then Milestone 3 has its bound and the proof is
"only" the transfer theorem for whichever candidate survives. If either fails, that candidate is
refuted and the cross-field search moves to the next structure — which is the engine doing its job.
