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

## The generalization (the ToE's shape)

> **In every sector, the exact structure is constraint + label; everything else is a
> free, unpredicable parameter.**

- Flux sector: *proven* (Mitchell's Completeness + Complete Exact Structure).
- Gauge/SM sector: *the anomaly cancellation is a constraint (verified); the gauge
  group and generations are labels; the 19 parameters are candidates for
  "unpredicable"* — the same claim, not yet a theorem.

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
- **No theorem yet**: unlike the flux sector (where symplectic invariant theory gives
  a *proof*), the SM classification here is a *verified observation* — the anomaly
  cancellation is checked, not derived from a uniqueness theorem. The gauge-sector
  analog of "the tadpole is the unique invariant" is the open target: is there a
  unique-invariant theorem for the SM's exact structure?

## Reproduce

```
python3 scripts/validate_sm_anomaly.py    # 5/5 SM anomaly coefficients vanish
```
