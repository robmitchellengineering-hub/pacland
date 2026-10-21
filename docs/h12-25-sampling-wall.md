# h12=25 sampling wall — the ISD proposal degrades (measured 2026-10-21)

The overnight h12=25 run on `pacland-rog` (first-ever h12=25 sampling) found
**0 critical points in 13,311 valid candidates (16,000 tried, 8h42m)**. This is a
measured negative result, not a guess — and the root cause is now located.

## What was measured

| config | result |
|---|---|
| h12=2 + `scipy` + `ISD-` (control) | **11 critical pts / 74 valid in 31s**, residuals 1e-14..1e-43 |
| h12=25 + `scipy` + `ISD-` (overnight) | **0 / 13,311**, `scipy` returns "not making progress", `\|dV\|` stuck O(1)–O(1000) |
| h12=25 + `hybrid` (adam_v + Newton) | **0 / 84** |
| h12=25 + `sample_SUSY_flux_vacua` (proper SUSY method) | OOM 143 GB at `vmap_dim=100`; `vmap_dim=1` → 0/200 filter passes |

**The solver is not the problem.** `scipy`+`ISD-` works perfectly at h12=2. The
break is specific to h12=25.

## Root cause — the ISD starting points are ~40x too far out

Initial potential-gradient at the ISD- starting points:

| h12 | min `\|dV\|` | median `\|dV\|` | max |
|---|---|---|---|
| 2  | 0.30 | **4.14**  | 2.2e2 |
| 25 | 18   | **173**   | 6.5e4 |

At h12=25 **no** candidate starts anywhere near a critical point (min `\|dV\|`=18 vs
0.30 at h12=2), so no local method — first-order (`adam_v`) or second-order
(`scipy` Newton) — can converge. The ISD importance sampling, which at h12=2 lands
you *near* SUSY vacua, stops concentrating at 25 moduli.

## The smoking gun — the ISD matrix is pathologically ill-conditioned at h12=25

The ISD proposal works by computing a non-integer flux that satisfies the ISD
condition ⋆G₃ = iG₃ (⇔ F-flatness) exactly, then **rounding it to integers**. The
rounding error (~O(0.5) per component) is amplified by the conditioning of the
Hodge-⋆ matrix `M` (built from the gauge kinetic matrix `N = R + iI`):

| h12 | `M` eig min | `M` eig max | cond(`M`) | `\|dV\|` after ISD+round |
|---|---|---|---|---|
| 2  | 7.4e-2 | 1.35e1 | **1.8e2**   | **0.73** |
| 25 | 4.5e-4 | 2.20e3 | **4.8e6**   | **669**  |

The condition number blows up **~26,000×** (183 → 4.8 million). A near-null
eigenvalue (4.5e-4) means there is a nearly-flat direction in the field-space
metric `I = Im N` at h12=25, so rounding the ISD flux perturbs that direction by
~1/4.5e-4 ≈ 2200× and lands ~1000× further from the F-flat slice. That is why no
solver can recover — the starting points are not just "a bit off", they are in the
wrong region of field space.

**It is intrinsic, not a polytope bug.** cond(`M`) across h12 and across every
bundled h12=25 polytope:

| scope | cond(`M`) |
|---|---|
| h12 = 2 / 5 / 10 / 15 / 20 / 25 | 1.8e2 / 1.1e10 / 2.9e6 / 7.5e7 / 7.3e8 / 4.8e6 |
| h12=25, `model_ID` 1..9 | 4.8e6, 9.6e8, 2.3e9, 3.3e9, 3.7e8, 1.8e8, 1.1e8, 8.2e8, 2.7e10 |

Every h12 ≥ 5 is ill-conditioned (1e6–1e10), and `model_ID=1` is already the
*best* h12=25 polytope. The near-null eigenvalue is a real nearly-flat direction
in the moduli metric (a hierarchy), not bad data.

**It breaks the linearised shifts too, not only the rounding.** The SUSY method
(`sample_SUSY_flux_vacua` → `linearised_shifts`) leaves the Kähler cone on the very
first step (`hyperplanes @ Im(z) < 0`) with residual still O(100), so the one-step
filter rejects every candidate.

## What was ruled out

- **Missing worldsheet-instanton corrections** (`maximum_degree=0` → the
  "mirror WSI disabled" warning): enabling them (`maximum_degree=1,2`) does **not**
  help — `\|dV\|` stays O(300), `scipy` still 0/8.
- **`scipy` vs the vmapped `newton`**: not the differentiator — `hybrid` fails too.
- **`ISD+` vs `ISD-` and the flux-prior σ** (0.5 / 2.0 / 5.0): none recovers —
  best case `ISD+`, σ=0.5 gives `\|dV\|` min 13, still ~100× a critical point.
  The ill-conditioning is not a sampling-config problem.
- **A different polytope**: all 9 bundled h12=25 models are ill-conditioned.
- **Damped `step_size` / cone sampling**: the shift leaves the Kähler cone anyway.

## The wall, classified

This is the **intractable** wall in `AGENTS.md`, located at the *proposal*, not the
solver and not the hardware. The cause is measured and exhaustive: **the ISD matrix
`M` is ill-conditioned for every h12 ≥ 5 (cond 1e6–1e10, all polytopes)**, so both
the integer-rounding of the proposal and the linearised shifts are pushed off the
F-flat slice / out of the Kähler cone.

## The fix (the actual lever)

The near-null eigenvalue of `M` is a nearly-flat direction in the field-space
metric — a *hierarchy* that the h12 truncation must respect. The ISD proposal and
the linearised shifts both invert quantities in `M`, so both break. The fix is to
stop inverting the flat direction:

1. **Regularise / project out the flat direction** before the ISD completion and
   before each linearised shift (truncate `M`'s eigensystem above a condition
   threshold), or
2. **Nearest-integer rounding in the `M` metric** (lattice/coordinate-descent that
   minimises `Σ|D_A W|` instead of naive `round()`), or
3. **A different proposal** that never inverts the flat direction (e.g. sample in
   the well-conditioned subspace and lift).

Each is a small, testable change against `sampler.ISD_sampling` /
`linearised_shifts_ISD`; the diagnostic is the same cond(`M`) + `|dV|`-after-round
table in this file.

Recorded so this is not re-derived: the sampler runs end-to-end and the mesh job
path is proven; the open question is purely the h12=25 proposal.
