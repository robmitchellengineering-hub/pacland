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

## What was ruled out

- **Missing worldsheet-instanton corrections** (`maximum_degree=0` → the
  "mirror WSI disabled" warning): enabling them (`maximum_degree=1,2`) does **not**
  help — `\|dV\|` stays O(300), `scipy` still 0/8.
- **`scipy` vs the vmapped `newton`**: not the differentiator — `hybrid` fails too.

## The wall, classified

This is the **intractable** wall in `AGENTS.md`, located at the *proposal*, not the
solver and not the hardware. The suspect is `sampler.ISD_sampling` /
`_generate_flux_candidates` at `dim_H3=26`: the ISD-completed fluxes are not
satisfying F-flatness even approximately at h12=25 (hence `\|dV\|` O(100–1000)).

## Next directions (not yet tried)

1. Instrument `ISD_sampling` at h12=25: does the ISD matrix / linearised-shifts
   computation stay well-conditioned at 26 dims, or is the returned flux far off
   the F-flat slice?
2. Try `sample_SUSY_flux_vacua` with a small `vmap_dim` (2–8, to dodge the 143 GB
   OOM) and a larger resample budget, and compare its *cone* moduli sampling to the
   box sampling `sample_critical_points` uses.
3. Check whether `model_ID=1` is a valid h12=25 polytope (ancillary polytopes
   arXiv:2306.06160 cover h12_5..h12_25) — a wrong/absent polytope would degrade the
   periods and hence the ISD matrix.

Recorded so this is not re-derived: the sampler runs end-to-end and the mesh job
path is proven; the open question is purely the h12=25 proposal.
