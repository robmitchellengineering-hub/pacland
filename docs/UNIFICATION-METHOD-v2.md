# UNIFICATION METHOD v2 — the method that works

**Status:** redefinition (2026-10-23), after the G2 false-pass fix and the point-orbit-space
correction. This **supersedes the G1–G5 gap list** in `SOLVING-STRING-THEORY.md`; the three-object
table and the standards there still bind. `unification-claim.md` (C1–C4) and
`orbit-space-unification.md` (the path) remain the claim and the framing.

## Why the method had to change

Three findings, each proven, break the old ladder:

1. **The orbit space is a point per tadpole.** Completeness: over ℝ, `Sp(b₃)` is transitive on each
   tadpole level set. There are no coordinates on a point, so "write the 19 as functions on orbit
   data" (old G5) is a category error. The connecting structure is the **quotient map**, not a
   polynomial relation — and a map that has nothing to quotient by gives a *negative* theorem.
2. **Exact content is three types, not two.** `unification-synthesis.md`: **constraint + label +
   counting**. The 19 is a counting invariant — exact as a count, free as values. The old
   two-type decomposition hid this and caused an internal contradiction.
3. **The covariance table is the theory.** "One theory described twice" is operational only when
   every observable has a closed-form law under `Sp(b₃,ℤ) × SL(2,ℤ)`. Law I, Law II, and G2 are
   the first rows; G2 was a false pass until 2026-10-23.

## The redefined target

String theory is **solved** for a sector when all three hold (same (a)+(b)+(c), but (c) re-ranked):

- **(a) the invariant ring is enumerated** — the exact invariants generate the ring.
  **Done for flux**: `ℂ[N]`, the tadpole (Weyl FFT + Uniqueness + Lean).
- **(b) the covariance table is complete** — every observable's law under `S` and `T`, closed form.
  **This is where the laws are.**
- **(c) the dictionary is *ranked*, not *solved*** — certify the 19 as the orbit-space dimension
  (Molien–Weyl), enumerate the collapses symmetry forces (GUT: 3 of 19), and prove **no further
  relation exists**. The deliverable is the rank and its collapses, **not a formula for the values**
  — the theorem already forbids that formula.

Unification = (a)+(b)+(c). It is *not* "derive the 19" — that is provably not there. It *is*:
"every observable transforms covariantly, and the 19 are free exactly where symmetry does not force
a relation."

## The laws — the covariance table, row by row

Every row is stated with a **control that reproduces a known value** (the G2 lesson) and a **named
falsifier**. A law earns the name only when all four of `MITCHELLS-LAWS.md` hold.

| law | statement | control (must pass first) | falsifier | status |
|---|---|---|---|---|
| **I** scaling | `W(dF,dH)=d·W`, `N(dF,dH)=d²·N`, `gcd` scales | `d² | N` on all 5,885 rows | a DW zero set not preserved under scaling | **DONE** (5/5 + `2143Z` ratio 2.0) |
| **II** `\|W\|` S-invariance | `\|W(-H,F;-1/τ)\| = \|W(F,H;τ)\|` | free fit `a,b` in `\|W_S\|/\|W\| = e^a \|τ\|^b` → both 0 | log residual > 0.10 | **DONE** (100/100, 0.0000) |
| **IIb** phase of `W` under S | `arg W` has a fixed law `f(τ)` | `\|W\|` row reproduces | phase not a function of τ | open |
| **III** `g_s` under S,T | `g_s = 1/Im(τ)`; S: `τ→-1/τ` ⇒ `g_s'=\|τ\|²g_s`, T: `τ→τ+1` ⇒ `g_s'=g_s` | `g_s` reproduced at original τ | `g_s' ≠ \|τ\|²g_s` under S | **DONE** (100/100 clean; definitional — the 2209Z `0.21→3.9e7` was a bug) |
| **IV** moduli covariance | `z_i` transforms by the moduli-sector law | reproduce the stored moduli row | moduli law scatters | open |
| **V** counting | 19 = orbit-space dim (Molien–Weyl); GUT collapses exactly 3 | rank test 3-way | a 20th relation beyond GUT | **next** (rank 3-way done; Molien cert owed) |

**The T-row of `|W|` is a finding, not a law.** `|W_T|/|W|` (T: `(F,H)→(F,H+F)`, `τ→τ+1`) does **not**
close to a clean law across the 100-row sample (mean 4.9e6, std 4.9e7, fit residual 0.22 — the
mean is carried by rows where `|W|≈0`, the no-scale locus, where the ratio is ill-defined). The
generic rows show a rough `|W_T|/|W| ≈ 0.6·|τ|`. Follow-up: re-fit on `|W|` away from zero.

## The walls, used (prime directive — walls are information)

- **Truncation (old G3) — RESOLVED: it is a physical hierarchy, not a truncation artefact.**
  The decisive diagnostic is *where the near-null eigenvector of the ISD matrix `M` points*.
  Measured at generic (proposal-stage) moduli via `model.ISD_matrix(moduli, moduli_c)` — note
  `data_sampler.initial_guesses_ISD` is NOT used (it JIT-compiles for minutes at h12≥5, and the
  proposal-stage moduli are just generic moduli before any solve). Result across h12=2..25
  (`scripts/diagnose_truncation.py`, job `2339Z`): the near-null eigenvector is **interior**
  (weight 0.969 → 1.000 → 0.572) at every h12, boundary-aligned weight ≈ 0 (≤ 0.028) throughout,
  and the dilaton direction only mixes in at h12=25 (0.426). So the ISD ill-conditioning
  (cond 4.2e3 → 1.2e7) is a **flattish physical direction in the CS-moduli metric**, and the
  SUSY-fraction collapse is a physical effect, not a proposal curve. The projection/regularisation
  fix is legitimate. (The earlier `1e135` was a stage error: at a converged vacuum `⋆G=iG` makes
  `M` singular by construction.)
- **Orbit-space-is-a-point.** Redefines the target (covariance table + rank), does not block it.
- **API mis-addresses** (`tau_c`, `initial_guesses_ISD`). Standing rule: **pin the signature with
  `inspect.signature` before writing any call.** Bought twice.

## Sequence (cheap → long)

1. **Complete the covariance table** — Law III (g_s) **done**, IIb (phase) **dispatched**, IV
   (moduli): shell jobs on `pacland-rog`, each with a control. [cheap]
2. **The truncation diagnostic** — **DONE** (`diagnose_truncation.py`, `2339Z`): interior ⇒ physical
   hierarchy, not truncation. [cheap]
3. **The K-theory torsion correspondence** — tadpole (Euler index, Freed–Witten ℤ₂) ≡ anomaly
   (Dirac index, Witten global ℤ₂) as the same K-theory kind. The flux↔SM bridge. [symbolic]
4. **The Molien–Weyl cert** — Law V, certify the 19 and the GUT 3-collapse. [symbolic]
5. **The dictionary rank on one stratum** — the long pole, and where `m` grows.

## Falsifiers that kill the whole programme (unchanged, re-asserted)

1. A moduli-independent, duality-invariant flux quantity not a function of `FᵀJH`.
2. An exact UV relation among the 19 beyond the GUT collapses.
3. The invariant structure changing as more moduli are kept (the truncation diagnostic returns
   boundary-aligned).

A method that cannot name its own killers is advertising.
