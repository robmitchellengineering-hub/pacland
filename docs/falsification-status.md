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
| 2 | a **20th** exact relation among the 19 (a completion collapsing more than GUT's 3) | **REFUTED as stated** — see the correction below: "no collapse > 3" is false, and the "3" was itself miscounted |
| 3 | a covariance law that **scatters** at higher h12 | **measured** — the laws hold exactly at h12=2 and h12=5; h12=10 has no in-cone vacua to test (the SUSY collapse) |
| 4 | a measured **non-uniform** `dN/d\|W₀\|²` near zero, or a proven dS no-go | **measured** — `dN/d\|W₀\|²` is locally flat near zero; the dS no-go is the community's open question (trending-forbidden, no theorem) |

## Correction — the "GUT collapses 3" claim was wrong (falsifier #2 verdict)

The adversarial pass refuted the conjecture "no completion collapses more than 3 of the 19",
and caught a counting error in our own claim:

- **The "3" was miscounted.** `Y_e = Y_dᵀ` is a 3×3 *matrix* identity — three eigenvalue
  relations (`m_e=m_d, m_μ=m_s, m_τ=m_b` at `M_GUT`), collapsing 3, not 1. So minimal SU(5)
  collapses **2 (gauge) + 3 = 5**, not 3.
- **"SU(5) is the maximum" is backwards.** Minimal single-Higgs SO(10), E₆, Pati–Salam and
  trinification unify the up sector too (`Y_u=Y_d=Y_e`, `V_CKM=1`), collapsing **12** of the 19 —
  exact, derivable relations that are *numerically wrong* and hence excluded by data.
- **SUSY adds a missed relation.** In the MSSM the Higgs quartic is not free
  (`λ = (g²+g′²)/8` from D-terms), collapsing one Higgs parameter and stacking with unification.

**The salvageable, true statement (much weaker):** no known completion gives an *exact, derivable,
and numerically-correct* relation among the 19 beyond gauge-coupling unification (2 collapse).
The exact relations that do exist (up to 12 in SO(10)) are wrong against data; only 2 survive.
The strongest near-miss for a genuine 20th relation is the **Koide formula** (correct to 10⁻⁵ but
underived). "GUT collapses exactly 3" must be dropped from the program's copy.

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
