# The Standard-Model frontier — constraint-first, one sector up

The Complete Exact Structure Theorem proved that the **flux sector's** only exact
structure is its constraint (the D3 tadpole) plus its label (CY topology). This doc
extends the same classification to the **Standard Model**, which is the `m = 0`
frontier the theorem named as the open question: *are ALL exact structures
constraint structures?*

## The SM's exact structure decomposes exactly like the flux sector's

| type | flux sector (proven) | Standard Model |
|---|---|---|
| **constraint** — "what the theory forbids" | D3 tadpole `N ≤ L` (the *unique* invariant) | anomaly cancellation, charge quantization (Dirac) |
| **label** — "which geometry you picked" | `h¹¹, h²¹, c₂, κ` | gauge group SU(3)×SU(2)×U(1); **N_gen = 3** = a topological index (`|χ|/2` in the heterotic class) |
| **parameter** — unpredicable | `W₀, g_s`, couplings, masses, Λ | the **~19 free numbers** (masses, couplings, mixing angles, θ_QCD) |

The point is structural, not aesthetic: in both sectors the *exact* content is
**constraint + label**, and the *non-exact* content is the free parameters. A theory
of everything, under this reading, predicts nothing exactly except what it forbids
(constraints) and what it is handed (labels) — in *every* sector.

## The checkable piece: anomaly cancellation is a constraint, not a prediction

`scripts/validate_sm_anomaly.py` verifies, exactly (rational arithmetic, zero
floating point), that the SM fermion content cancels **all five** gauge/gravitational
anomalies per generation:

```
[SU(3)]^3       = 0      [SU(3)]^2 U(1)  = 0
[SU(2)]^2 U(1)  = 0      [U(1)]^3        = 0      [grav]^2 U(1) = 0
```

The hypercharges `(1/6, 2/3, −1/3, −1/2, −1)` are **forced** by these vanishing
conditions (up to overall normalization). They are not predicted; they are *required
for consistency*. This is the gauge-sector exact statement that parallels the flux
sector's "the tadpole is the unique exact invariant": the SM's first exact structure
is **what the theory forbids**, not what it selects.

## The gauge-sector uniqueness theorem (Mitchell's Uniqueness, one sector up)

`scripts/validate_sm_hypercharge_uniqueness.py` proves it symbolically (4/4, exact):

> **Given the SM matter content (gauge reps + chirality), the anomaly-cancellation
> conditions determine the hypercharge assignment uniquely, up to overall
> normalization and the u↔d flavor swap.**

The three *linear* conditions (`[grav]²U(1)`, `[SU(2)]²U(1)`, `[SU(3)]²U(1)`) leave a
2-dimensional family (`Y_L = −3Y_Q`, `Y_e = −6Y_Q`, `Y_d = 2Y_Q − Y_u`); the cubic
`[U(1)]³` then collapses it:

```
[U(1)]³ reduced  =  18·Y_Q·(2Y_Q + Y_u)(4Y_Q − Y_u)  =  0
⟹  Y_u = 4Y_Q   (the SM)    or    Y_u = −2Y_Q   (the u↔d swap)
```

So the hypercharges are **the unique solution** — the gauge-sector constraint is
unique, exactly as the flux constraint (the tadpole) is unique. This is the same
theorem shape: *the only exact structure is the constraint*.

## The parameters — "unpredicable" means two different things, and only one is proven

`scripts/validate_sm_parameter_count.py` counts the minimal SM's free couplings
exactly: **19** = 3 gauge + 9 masses + 4 CKM + 2 Higgs + 1 θ_QCD. These are the
independent gauge-invariant, renormalizable couplings — the free *inputs*.

There is a crucial, honest distinction here that the flux sector did **not** have to
draw:

1. **"Unpredicable within the SM" — trivially true.** The 19 parameters are free
   inputs *by definition*; the SM has no gauge or global symmetry that fixes any of
   them (its only continuous global symmetries, baryon and lepton number, are
   accidental and constrain nothing). This is a counting fact, not a theorem.
2. **"Unpredicable in any UV completion" — the non-trivial claim, and *unproven*.** The
   flux theorem said "no invariant exists *in principle*" — and that was provable only
   because the flux has a clean duality group (Sp) with a known invariant theory (the
   FFT). The SM has **no such clean group action** on its couplings, so the analogous
   claim ("no ToE can predict the masses and couplings either") is a *conjecture* — and
   it may well be **false**: a GUT or string construction that relates the couplings
   (e.g. gauge-coupling unification, a Yukawa relation) would be exactly such a
   prediction.

So the honest status: the SM frontier has *proven* that its **constraint** (anomaly
cancellation → unique hypercharge) is unique, and *classified* that its **parameters**
are the free inputs. The headline generalization — "the ToE predicts nothing exactly
except constraints and labels, in *every* sector" — is **proven for flux, conjectured
for the SM**, and the conjecture is falsifiable in the clearest possible way: any UV
relation among the 19 parameters breaks it.

## The generalization (the ToE's shape)

> **In every sector, the exact structure is constraint + label; everything else is a
> free, unpredicable parameter.**

- Flux sector: *proven* (Mitchell's Completeness + Complete Exact Structure).
- Gauge/SM sector: *constraint proven unique (hypercharge), parameters classified as
  free inputs; the "unpredicable in any UV completion" half is conjectured, not proven.*

## The falsifiable test

This is what makes it science, not slogan:

> **Derive any one of the SM's ~19 free parameters from first principles** (rather
> than measuring it), and the constraint-first generalization is falsified.

Conversely, every new "exact" structure that turns out to be a constraint or a
topological label is evidence *for* it. The SM's celebrated fine-tuning problems
(hierarchy, strong CP, the mass ratios) are, under this reading, exactly what the
theorem predicts: they are *not* derivable, because there is no invariant for them to
be a function of.

## Honest boundaries (named, not hidden)

- **Anomaly cancellation fixes the hypercharges up to overall normalization** — the
  actual value of the U(1) coupling is a free parameter, not fixed. "Constraint"
  means "the *pattern* is forced", not "every number is determined".
- **N_gen = 3 as a topological label** is exactly true in the heterotic class
  (`|χ|/2`); in the broader landscape, generation number is geometric/bundle-topological
  data — still a *label*, but the precise invariant varies by construction.
- **No theorem yet** (fully): unlike the flux sector (where symplectic invariant theory
  gives a *complete* proof), the SM classification here is a *verified observation* plus
  the **hypercharge-uniqueness theorem** (the gauge constraint is unique). The remaining
  open target is the *full* gauge-sector analog: is there an invariant-theory proof that
  the SM's exact structure is *only* constraint + label — i.e. that the 19 parameters
  have no invariant to be a function of, the way the flux couplings provably don't?

## Reproduce

```
python3 scripts/validate_sm_anomaly.py                    # 5/5 SM anomaly coefficients vanish
python3 scripts/validate_sm_hypercharge_uniqueness.py     # 4/4 hypercharge is forced (unique)
python3 scripts/validate_sm_parameter_count.py            # 19 free couplings, counted exactly
python3 scripts/validate_sm_invariant_ring.py             # 19 = orbit-space dim (the FFT analog) + GUT reduction
```

## The sharpened open question: the "floor"

`validate_sm_invariant_ring.py` makes the FFT analog exact: the 19 parameters are the
orbit-space dimension of the flavor/reparametrization group (Bento–Silva–Trautner,
JHEP 2024), i.e. they are the *independent flavor invariants* — nothing relates them
within the SM, by a theorem. A UV completion with a larger group shrinks the ring
(minimal SU(5): 19 → 16). The refined conjecture ("a ToE predicts relations, never
values") now has a precise target:

> **What is the minimum orbit-space dimension any consistent UV completion can reach —
> a lower bound on free parameters below which no ToE can go?**

The flux sector's floor is 1 (the tadpole). The SM sector's floor is unknown, and
finding it is the concrete next theorem.
