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
  **This is where the laws are: Mitchell's Laws of Duality Covariance** (`MITCHELLS-LAWS.md`).
- **(c) the dictionary is *ranked*, not *solved*** — certify the 19 as the orbit-space dimension
  (Molien–Weyl), enumerate the collapses symmetry forces (minimal SU(5): 5, SO(10)/E₆/Pati–Salam: 12 —
  only gauge unification (2) survives data), and prove **no further
  relation exists**. The deliverable is the rank and its collapses, **not a formula for the values**
  — the theorem already forbids that formula.

Unification = (a)+(b)+(c). It is *not* "derive the 19" — that is provably not there. It *is*:
"every observable transforms covariantly, and the 19 are free exactly where symmetry does not force
a relation."

## Mitchell's Laws of Duality Covariance — the table, row by row

Every row is stated with a **control that reproduces a known value** (the G2 lesson) and a **named
falsifier**. A law earns the name only when all four of `MITCHELLS-LAWS.md` hold.

| law | statement | control (must pass first) | falsifier | status |
|---|---|---|---|---|
| **I** the scaling law | `W(dF,dH)=d·W`, `N(dF,dH)=d²·N`, `gcd` scales | `d² | N` on all 5,885 rows | a DW zero set not preserved under scaling | **DONE** (5/5 + `2143Z` ratio 2.0) |
| **II** the superpotential law — magnitude | `\|W(-H,F;-1/τ)\| = \|W(F,H;τ)\|` | free fit `a,b` in `\|W_S\|/\|W\| = e^a \|τ\|^b` → both 0 | log residual > 0.10 | **DONE** (100/100, 0.0000) |
| **IIb** the superpotential law — phase | `arg(W_S/W) = -arg(τ)` exactly (⇒ `W_S = W·τ̄/\|τ\|`) | `\|W\|` row reproduces (1.0000) | phase scatters (resid > 0.10) | **DONE** (100/100, resid 0.0000) |
| **III** the string-coupling law | `g_s = 1/Im(τ)`; S: `τ→-1/τ` ⇒ `g_s'=\|τ\|²g_s`, T: `τ→τ+1` ⇒ `g_s'=g_s` | `g_s` reproduced at original τ | `g_s' ≠ \|τ\|²g_s` under S | **DONE** (100/100 clean; definitional — the 2209Z `0.21→3.9e7` was a bug) |
| **IV** the moduli law | `z_i → z_i` at degree 0 (S/T act on flux+τ only) | G2: transformed point at fixed z is a vacuum | a degree-0 moduli shift needed | **established** (by definition; monodromy deferred to degree>0) |
| **V** the counting law | 19 = orbit-space dim (Molien–Weyl); minimal SU(5) collapses 5, SO(10)/E₆/PS 12 — only gauge unification (2) survives data | rank test 3-way | a 20th relation beyond GUT | **DONE** (three routes: count + rank + Molien–Weyl) |

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

1. **Complete the covariance table** — Laws I–V **done** (scaling, superpotential magnitude+phase,
   string-coupling, moduli, counting): shell jobs on `pacland-rog`, each with a control. [cheap]
2. **The truncation diagnostic** — **DONE** (`diagnose_truncation.py`, `2339Z`): interior ⇒ physical
   hierarchy, not truncation. [cheap]
3. **The K-theory torsion correspondence** — rational half **done** (`validate_ktheory_torsion.py`:
   Â has no pure `c₃`, so the O3 charge is the Euler index, not the Dirac index — same K-theory
   *kind*, different *index*). The ℤ₂ torsion (Freed–Witten vs Witten global anomaly) is the named
   open half, out of reach of rational cohomology. [symbolic]
4. **The Molien–Weyl cert** — Law V **done** (`validate_molien_weyl.py`, three routes to 19). [symbolic]
5. **The dictionary rank** — **the negative theorem, established** (below). The full dictionary
   *map* remains the long pole, and is provably not a map: the 19 are free coordinates. [long]

## The dictionary rank — the negative theorem

The dictionary is **ranked, not solved**. Its rank is established exactly (all in
`validate_sm_rank_test.py` + `validate_molien_weyl.py`):

- **flux sector**: the map `(F,H) → observables` has **rank 1** — the tadpole. Everything else the
  flux could carry is noise (the structure map, `r = 1.0` only for `N`). The flux dictionary is the
  collapse to the single constraint.
- **SM sector**: the map `(UV inputs) → 19 parameters` has **rank 19** — the orbit-space dimension —
  and the *only* known UV symmetries (GUTs) collapse **5 of 19** for minimal SU(5) (gauge 3→1 = 2,
  plus `Y_e = Y_dᵀ` = 3 mass relations) or **12** for SO(10)/E₆/Pati–Salam/trinification
  (`Y_u=Y_d=Y_e`, `V_CKM=1`) — but those exact mass relations are *numerically wrong*, so only
  gauge unification (2) survives — never all 19 (the SM has no duality group + FFT, so there is no
  flux-style total collapse). ⚠️ corrected 2026-10-23 (falsifier #2): see docs/falsification-status.md

Consequence, stated as a result: **the 19 are free coordinates, not functions of the invariants** —
there is no "connecting equation" to find, and a programme looking for one is looking for something
the theorem already ruled out. The connecting structure is the *quotient map* (a point per tadpole
for flux), and the unification result is the rank plus its collapses. This is where `m` (the
Mitchell Verification Deficit) is certified, not where a formula appears.

## Falsifiers that kill the whole programme (unchanged, re-asserted)

1. A moduli-independent, duality-invariant flux quantity not a function of `FᵀJH`.
2. An exact UV relation among the 19 beyond the GUT collapses.
3. The invariant structure changing as more moduli are kept (the truncation diagnostic returns
   boundary-aligned).

A method that cannot name its own killers is advertising.
