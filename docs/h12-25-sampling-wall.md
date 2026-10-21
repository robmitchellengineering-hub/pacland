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

## What was ruled out

- **Missing worldsheet-instanton corrections** (`maximum_degree=0` → the
  "mirror WSI disabled" warning): enabling them (`maximum_degree=1,2`) does **not**
  help — `\|dV\|` stays O(300), `scipy` still 0/8.
- **`scipy` vs the vmapped `newton`**: not the differentiator — `hybrid` fails too.
- **`ISD+` vs `ISD-` and the flux-prior σ** (0.5 / 2.0 / 5.0): none recovers —
  best case `ISD+`, σ=0.5 gives `\|dV\|` min 13, still ~100× a critical point.
  The ill-conditioning is not a sampling-config problem.

## The wall, classified

This is the **intractable** wall in `AGENTS.md`, located at the *proposal*, not the
solver and not the hardware. The cause is measured: **the ISD matrix `M` is
ill-conditioned at h12=25 (cond 4.8e6 vs 183)**, so integer-rounding the
ISD-completed flux lands far off the F-flat slice.

## Next directions

1. **Re-condition the ISD step** — the near-null eigenvalue of `M` is a nearly-flat
   direction in the field-space metric. A different period basis / gauge choice, or
   a nearest-integer rounding that respects the ill-conditioned directions, may land
   back on the F-flat slice.
2. Check whether the near-null direction is real (a hierarchy in the h12=25
   geometry) or an artifact of `maximum_degree=0` / the polytope data — confirm
   `model_ID=1` is a valid h12=25 polytope (ancillary polytopes arXiv:2306.06160
   cover h12_5..h12_25), and re-measure cond(`M`) with instanton corrections on.
3. Try `sample_SUSY_flux_vacua` with a small `vmap_dim` (2–8) and its *cone* moduli
   sampling; the cone may stay inside the well-conditioned region that box sampling
   does not.

Recorded so this is not re-derived: the sampler runs end-to-end and the mesh job
path is proven; the open question is purely the h12=25 proposal.
