# Falsification status — what is checked, and the two honest gaps

Status: **verification record** (2026-10-23). This documents, per falsifier of Mitchell's
Principle, what has been actively checked versus what remains open.

## The verification arms

| arm | what it checks | state |
|---|---|---|
| sympy tower (`validate_all_theorems.py`) | the six theorems, symbolically at zero tolerance | **6/6 PASS** |
| sympy FFT (`validate_constraint_first.py`) | the invariant ring is `ℂ[N]`, degree-by-degree | **5/5 degrees** |
| Lean (`pacland-proof/`, `lake build`) | Mitchell's Uniqueness at n=1 and general-n; transitivity at n=1 | **build green (9051 jobs)** |
| node measurements | the laws (h12=2,5), the SUSY collapse, no statistical selection, the flat CC | **measured, control-gated** |

## The four falsifiers, one by one

| # | falsifier | status |
|---|---|---|
| 1 | a moduli-independent, duality-invariant flux quantity **not** a function of `FᵀJH` | **proven absent** — the invariant ring is `ℂ[N]` (sympy 5/5 degrees); the degree-2 slice is machine-checked in Lean (Uniqueness) |
| 2 | a **20th** exact relation among the 19 (a completion collapsing more than GUT's 3) | **partially checked** — the 19 = orbit-space dimension is proven *within* the SM (rank test, three-way); the UV extension ("no completion collapses more than 3") is **conjectured**, adversarial pass in flight |
| 3 | a covariance law that **scatters** at higher h12 | **measured** — the laws hold exactly at h12=2 and h12=5; h12=10 has no in-cone vacua to test (the SUSY collapse) |
| 4 | a measured **non-uniform** `dN/d\|W₀\|²` near zero, or a proven dS no-go | **measured** — `dN/d\|W₀\|²` is locally flat near zero; the dS no-go is the community's open question (trending-forbidden, no theorem) |

## The two honest gaps

1. **Lean does not yet formalize the full Weyl FFT.** The Lean arm machine-checks the *degree-2*
   slice (Uniqueness — the only invariant *bilinear* form is the tadpole). The full
   Constraint-First statement (the invariant ring is `ℂ[N]` at *every* degree) is proven in sympy
   degree-by-degree (5 degrees) and is the First Fundamental Theorem of invariant theory
   (Weyl 1939, cited), but is **not** machine-checked at general degree. A full Lean formalization
   of the FFT is a research-grade task (Schur–Weyl duality / the double-commutant theorem), not a
   session task.
2. **Falsifier 2's ultraviolet extension is conjectured, not proven.** The nineteen are proven
   free *within* the Standard Model; that *no* ultraviolet completion collapses more than GUT's
   three is the open conjecture. The adversarial pass (searching every known completion — SO(10),
   E₆, Pati–Salam, string constructions, compositeness — for a 4th exact relation) is the check.

## What this means for the paper

The flagship paper's central equation `ℂ[F,H]^G = ℂ[N]` is:
- **proven** symbolically (sympy, 5/5 degrees);
- **machine-checked** at the bilinear (degree-2) level (Lean);
- **cited** at general degree (Weyl 1939) — the FFT is a known theorem, not our invention.

The falsifiers are named and three of four are actively checked; the fourth (a 20th relation in a
UV completion) is the one genuinely open test.
