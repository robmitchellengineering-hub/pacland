# Constraint-First Unification, machine-checked

**The exact content of a theory of everything is constraints, labels, and parameters**

*Authors: the pacland proof arm · Date: 2026-11-07 · Repository: `pacland-proof/`*

**DOI:** https://doi.org/10.5281/zenodo.24030942

**Abstract.** We machine-check (Lean 4 / Mathlib) the forced/free split across all four sectors of
physics, and from it state the constraint-first unification principle as a *falsifiable theorem*:
a theory of everything's **exact** content is exhausted by three classes — **constraints** (what
it forbids), **labels** (which geometry/group is picked), and **parameters** (free inputs) — and
the notorious "issues" between quantum mechanics and particle physics (the measurement problem,
"why these 19") are *provably the free column*: not bugs, and not derivable from the forced
column. The four forced halves are each kernel-checked with zero `sorry`/`axiom`.

## The four sectors, certified

| sector | forced (kernel-checked) | free (delimited) | the "issue" |
|---|---|---|---|
| Quantum | the Born rule `Tr(ρP)` is the *unique* non-contextual probability rule (Gleason) | which outcome | the measurement problem |
| Standard Model | the hypercharges are *forced* by anomaly cancellation (and `N_gen` is free) | the 19 values | "why these 19" |
| Flux / string | the tadpole is the *unique* duality invariant (Mitchell/FFT) | `W₀, g_s`, masses, Λ | "which vacuum" |
| Gravity | the Einstein equation is the *unique* divergence-free theory (Lovelock) | `G`, Λ | "why G, Λ" |

## What "machine-checked" means here

- **Gleason** (the CKM descent-chain route, no continuity): `Gleason.frameFunction_regular`.
- **SM**: `SM.Hypercharge.hypercharge_uniqueness` (anomaly conditions force the hypercharges up to
  scale + u↔d swap), `SM.Anomaly.anomaly_cancellation` (5/5), `SM.Generation.anomaly_homogeneous`
  (`N_gen` is a free label).
- **Gravity**: `Gravity.Bianchi.contracted_bianchi` (`∇·G = 0`) and `Gravity.Lovelock.lovelock_divergence`
  (the Einstein tensor is the *unique* divergence-free 2-tensor).
- **Flux**: `PaclandProof/Mitchell.lean` + `Transitivity.lean` (the tadpole is the unique
  bilinear symplectic invariant; the general-n FFT is sympy-verified, Weyl 1939).

`#print axioms` reports only `propext, Classical.choice, Quot.sound` throughout; `lake build`
is green (9093 jobs).

## The falsification half (the "no" side, also certified)

The QM falsification suite closes the three doors people mean by "can we sort out the
non-determinism": **non-contextuality** (Gleason, Kochen–Specker, Mermin), **locality** (Bell/CHSH
both forms + Tsirelson `2√2`), **copying** (no-cloning, no-broadcasting), and **ψ-epistemic**
(PBR). Each is a theorem, not an assertion.

## The principle, stated precisely

> **Constraint-First Unification.** A theory of everything predicts **relations, never values**.
> Its exact content is `constraints + labels + parameters`; the free column (QM's outcome, the
> SM's 19, gravity's `G, Λ`) is delimited by the forced column but not derivable from it.

**Falsifier 1** — a single non-contextual deterministic completion of QM (would kill Gleason).
**Falsifier 2** — a hidden symmetry fixing any one of the 19 (would kill the SM uniqueness).
**Falsifier 3** — a second divergence-free gravity theory in 4D (would kill Lovelock).
**Falsifier 4** — a second duality-invariant flux quantity (would kill Mitchell).

The unification this paper *does not* claim: a formula for the 19, a collapse of the measurement
problem, or a prediction of `G, Λ`. The unification it *does* claim — and certifies — is that all
four sectors share the **same** forced/free architecture, so the "issues" are one phenomenon (the
free column), not four mysteries.

## Reproducibility

```
cd pacland-proof && lake build          # green, 9093 jobs
```

Sources: `PaclandProof/Foundations/GleasonBridge.lean`, `PaclandProof/SM/{Hypercharge,Anomaly,
Generation}.lean`, `PaclandProof/Gravity/{Bianchi,Lovelock}.lean`, `PaclandProof/QM/{CHSH,
Tsirelson,NoCloning,NoBroadcasting,PBR,Mermin}.lean`, `PaclandProof/Mitchell.lean`.
