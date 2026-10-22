# The orbit-space path to unification

**Status:** framing document. It contains no new computation. Every "proven" line below names the
check that proves it and was reproduced on 2026-10-22 (`python3 scripts/validate_all_theorems.py`,
all 6 PASS). Every "conjectured" line is marked as such, because the difference between the two is
the only thing standing between this program and the overclaims the adversarial review already
caught once (`docs/adversarial-review.md`).

## The claim, in one paragraph

Unification, here, is not a formula that links the Standard Model's 19 parameters to a Calabi–Yau's
topology. It is the statement that the vacuum landscape is **one space, stratified by duality
invariants**: vacua modulo the duality group, where the exact content of each stratum is
*constraints + labels*, and everything else is a coordinate *on* the stratum. On this reading the
"connecting equation" is the **quotient map**, not a polynomial relation. That is a weaker-looking
claim than "find the equation" and a far stronger one to defend: it is falsifiable, it is already
proven in one sector, and it says exactly where it stops being proven.

## What is proven

| piece | statement | check |
|---|---|---|
| **the symmetry** | the duality group is the full `Sp(b₃) × SL(2,ℤ)`, not just the monodromy subgroup | `scripts/validate_full_duality.py` — 5/5 symbolic |
| **the invariant ring** | the ring of exact symplectic invariants of the flux pair is `ℂ[N]` — a **single** generator, the tadpole `N = FᵀJH` (Weyl's FFT specialised to k=2) | `scripts/validate_constraint_first.py` — 5/5 degrees |
| **the invariant** | `N` is the **unique** bilinear symplectic invariant, for any compactification | `scripts/validate_mitchell_uniqueness.py` — 6/6 symbolic, plus the Lean 4 arm (`pacland-proof/`, general *n*, no `sorry`) |
| **the orbits** | `N` is **complete**: over ℝ, `Sp(b₃)` is transitive on each tadpole level set; over ℤ there are **finitely many orbits per tadpole**, one per divisor `d | √N` of the content `d = gcd(F,H)` with `d² | N`, and `N = 0` is a union of several lower-dimensional orbits | `scripts/validate_mitchell_completeness.py` — 6 exact + 2 numeric |

Consequence, stated at the strength the proofs actually support: **no exact polynomial
duality-invariant function can single out a vacuum.** That is a no-go on *exact invariant selectors*.
It is **not** a no-go on moduli-dependent, non-polynomial, or statistical selection, and `N ≤ L`
*bounds* the search space rather than emptying it. The audit's correction is binding here.

## What is conjectured (do not let this drift into the table above)

1. **That the Standard Model sector has the same shape.** This is *not* a corollary. The flux theorem
   is provable because the flux sector has a clean duality group and FFT applies; the SM's 19
   couplings have no such group. The extension is the research bet.
2. **"A ToE predicts relations, never values."** Refined by two research fan-outs: GUT and string
   constructions *do* relate parameters (gauge unification collapses 3 couplings to 1; b–τ collapses
   2 to 1), so "no invariant relates them" is overclaimed. What survives is "no unique *value* is
   derived — only relations".
3. **That the orbit-space picture is truncation-independent.** Untested. See below.

## The dictionary — the piece that actually unifies

The program can currently state the **dimension** of the parameter space and not the **map**:
19 = the orbit-space dimension, established three independent ways with the SM's own flavour symmetry
(`docs/sm-rank-test.md`), and the only known UV symmetry (GUT) collapses exactly 3 of those 19. That
is a measurement of the map's *image size*, not of the map.

The next step is therefore not more vacua but the **dictionary**: write the low-energy data as
functions on a stratum, on one tractable slice, and ask whether the map is constrained.

- **If the parameters vary freely within a stratum** → a *negative* theorem at degree 0: the
  parameters are not functions of the invariants. Still a unification result, and a sharper one than
  another frontier table, because it says the missing content is not "an equation we haven't found"
  but "content that cannot be an invariant".
- **If they vary only within a constrained slice** → the dictionary exists; the 19 become coordinates,
  and the relations among them are the connecting structure.

## Why the h12 work is *on* this path, not beside it

If the orbit-space picture is the connecting structure, it must not be an artefact of the truncation.
`h12` is the number of complex-structure moduli **kept** (2 of 272 in the bundled KS model), so the
whole measured frontier — the structure map, the fingerprint result, the SUSY-fraction curve — lives
inside a 2-moduli slice at the bottom of the table and a 4-moduli slice at its top.

`docs/h12-25-sampling-wall.md` locates the obstruction at the ISD proposal: the Hodge-⋆ matrix `M`
has cond 1.8e2 at h12=2 and 4.8e6 at h12=25, up to 2.7e10 across polytopes. Two readings exist and
they have opposite consequences:

- **numerical** — the proposal inverts a nearly-flat direction, so the starting points are wrong and
  a proposal fix opens h12 ≥ 5; or
- **physical** — the near-null eigenvalue is a real hierarchy that appears as moduli are kept, in
  which case "projecting it out" changes the measure and the honest deliverable is a boundary.

The decisive diagnostic is cheap and precedes any of the three named fixes: **cond(M) across
h12 = 2, 5, 10, 15, 20, 25 from one code path, plus where the near-null eigenvector points** — inside
the kept moduli subspace, or along the truncation boundary. A boundary-aligned eigenvector means the
truncation is the wall; an interior one means a flattish physical direction and a legitimate fix.

If the truncation is the wall, the SUSY-fraction collapse (27.9% → 19.7% → 1.1% from h12=2 to 4) is
partly a proposal curve, and the honest statement is a **lower bound** on the SUSY-vacuum density, not
a landscape fact. That correction belongs to this document's claim, not to the sampling appendix.

## How this dies (the falsifiers)

1. **Breaks the proven segment:** a single moduli-independent, duality-invariant flux quantity that is
   not a function of `FᵀJH`.
2. **Breaks the conjectured SM segment:** an exact UV relation among the 19 parameters beyond the
   GUT-style collapses already known (3 gauge, 2 b–τ).
3. **Breaks the orbit picture at scale:** the invariant structure changing when more moduli are kept —
   i.e. the h12 diagnostic coming back boundary-aligned.

A document whose claim cannot name its own killers is advertising.

## Where the numbers stand (verified 2026-10-22, not quoted)

- theorem tower: all 6 PASS, zero tolerance (`scripts/validate_all_theorems.py`).
- deficit `m = 9`, recomputed from the flags in `src/pacland/observables.py`: topology 4 + flux 1
  (of 5 defined, only the tadpole validated) + SM 4.
- landscape measurement: 14 models, **5,885 critical points, 1,245 SUSY (21.2%)**, recomputed from
  `data/h12_*_stats.json`; SUSY fraction 27.9% / 19.7% / 1.1% at h12 = 2 / 3 / 4.

## Open, in order

1. The truncation diagnostic (above) — decides whether the frontier is a landscape curve or a
   proposal curve.
2. The constraint claim's recordability: `data/h12_*_stats.json` stores `Nflux` but **not** `L`, so
   "all 5,885 satisfy `N_flux ≤ L`" is currently asserted rather than checkable from the committed
   data. Record `L = Q()` per `(h12, model_ID)`, or stop claiming it as verified.
3. The dictionary, on one tractable stratum (the unification step proper).
