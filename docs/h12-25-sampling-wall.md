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

Each is a small, testable change against the real sampler entry points. An earlier
version of this section pointed at `sampler.ISD_sampling` / `linearised_shifts_ISD` —
those pointers were wrong: there is no `sampler.py` in the installed package. A later
version still pointed at `bounded_fluxes.py`, which **does not exist** either: the
module is `flux_bounding.py`. Both wrong pointers cost a working session more than an
hour of read-only probes hunting a file that was never installed, so the table below
is re-verified against the installed package, with line numbers, by a job that prints
them (`jaxvacua 0.1.2`, `/home/rob/cytools-venv`, `pacland-rog`, 2026-10-22T21:39Z):

| what | real symbol | file:line |
|---|---|---|
| ISD proposal (sampler method) | `sampling.data_sampler.ISD_sampling` | `sampling.py:1897` |
| variant | `data_sampler._ISD_sampling_FH` / `_ISD_sampling_PM` | `sampling.py:1645` / `:1767` |
| initial guesses | `data_sampler.initial_guesses_ISD` | `sampling.py:2029` |
| `class data_sampler` | — | `sampling.py:250` |
| one-step linearised shifts | `flux_vacua_finder.FluxVacuaFinder.linearised_shifts_ISD` | `flux_vacua_finder.py:666` |
| shared shift entry point | `FluxVacuaFinder.linearised_shifts` | `flux_vacua_finder.py:1019` |
| ISD matrix `M` + spectrum | `flux_bounding._compute_evs_and_M_raw` | `flux_bounding.py:782` |
| ISD integer rounding | `flux_bounding._build_isd_apply_init` | `flux_bounding.py:951` |
| `M` on the model | `ISD_matrix` | `css.py:514`, `periods.py:1516` |

Installed modules (`ls $P/*.py`): `css, cytools_interface, flux_bounding, flux_eft,
flux_utils, flux_vacua_finder, freezer, hypergeometric_models, lcs, periods, sampling,
util, vacuum`. **There is no `bounded_fluxes.py` and no `sampler.py`** — a `grep` of a
path that does not exist exits 2 and reads like "the symbol is gone"; it is not.

**Interpreter trap — the one that bit the session.** `sympy` *is* installed
(1.14.0 in `/home/rob/cytools-venv`, verified 2026-10-22T21:42Z), but a job that runs
bare `python3` gets the system interpreter, and there
`import sympy` raises `ModuleNotFoundError`. So `validate_flux_scaling_lemma.py` died
at import and its arm reported nothing, which reads as "the exact algebra is
unavailable" when the module was there all along. **Every job on `pacland-rog` must
call `/home/rob/cytools-venv/bin/python`** — the system `python3` has neither sympy
nor the pinned jax/numpy the numbers were measured with.

Two details from the table matter when writing the experiment. `ISD_matrix` is a
method **on the model** (`periods.py` / `css.py`), not on the finder — call it as
`model.ISD_matrix(XPer, cXPer)`. And `_compute_evs_and_M_raw(moduli)` already returns
both the eigenvalues and `M` itself, so the conditioning probe should call it rather
than rebuild `M`; rebuilding is how the earlier "2200x amplification" story drifted
away from the library's own construction. The batched ISD kernels
(`precompute_isd_data`, `_build_isd_kernels`, `isd_refine_batch`, `_prepare_isd_pipeline`)
are all in `flux_bounding.py`.

The diagnostic is the same cond(`M`) + `|dV|`-after-round table in this file.

Recorded so this is not re-derived: the sampler runs end-to-end and the mesh job
path is proven; the open question is purely the h12=25 proposal.

## 2026-10-23 — the failure is localised to the rounding, and rounding tweaks cannot fix it

Measured directly on `pacland-rog` (jaxvacua 0.1.2), generic proposal moduli + a random
integer magnetic flux `h`:

| h12 | `\|DW\|` continuous ISD flux | `\|DW\|` after `round()` | cond(`M`) |
|---|---|---|---|
| 2 | **8.3e-14** (F-flat) | 1.8e1 | 4.2e3 |
| 5 | **1.4e-8** (F-flat) | 8.7e3 | 9.9e9 |

So the ISD **completion is correct** — `f_cont = (s·M·Σ + c₀)·h` is F-flat to ~1e-8 even at
h12=5. The whole failure is the **integer rounding**, amplified ~500× by cond(`M`).

Three rounding fixes were tried, and all fail at h12=5 for the same reason:

1. **Truncate `M`'s near-null eigenvalues** (raise to a floor) — makes `\|DW\|` *worse*
   (it breaks the F-flat `f_cont`). Setting them to zero changes `f_cont` off the F-flat slice.
2. **Coordinate-descent rounding** (flip flux components to minimise `\|DW\|`) — helps h12=2
   (18→4.5) but not h12=5 (8.7e3→8.73e3): the flat direction is a *combination* of flux
   components, so single-component flips cannot cancel it.
3. **Nearest-plane rounding** (one integer adjustment along `round(v_min)`) — no effect: the
   near-null eigenvector is *spread* across ~12 components with small coefficients, so there is
   no short integer vector parallel to it, and `round(v_min) ≈ 0`.

**Conclusion.** The h12=5 wall is *not* a rounding bug and *not* a completion bug — it is the
spread of the flat direction across the integer lattice, which no local integer adjustment can
cancel.

**CORRECTION (same day, follow-up) — the fix is simpler than option 3.** The one thing the
rounding analysis missed is that the *moduli* can absorb the rounding error, not just the flux.
The library's linearised shift (`A @ shift = b`, with `b = f − f_cont`) is a **Newton step** for
finding the moduli where the *rounded* flux is F-flat — and **iterating it converges**:

| h12 | `\|DW\|` after round | after 1 shift | after 2 shifts | after 3–6 shifts |
|---|---|---|---|---|
| 2 | 1.8e1 | 7.9 | 2.4e-1 | **1e-8 … 1e-13** |
| 5 | 8.7e3 | 4.0e1 | 2.2e-2 | **~1e-8** |
| 10 | — | — | — | ~1e-11 (converges) |

So the wall-doc's "one shift + stuck scipy solver" is the failure — **a single shift is not
enough, and iterating it reaches F-flat at h12=5 and 10.** On 15 cone-sampled candidates at
h12=5, the damped Newton finds **8/15 F-flat points, 3 in-cone SUSY vacua** (vs the wall-doc's
0/13,311), while h12=2 gives 12/15 in-cone. The in-cone fraction falls 80% → ~20–30% with h12 —
so the SUSY collapse is *both* a sampler bug (iterating the shift finds the points) *and* a
physical effect (fewer land in the cone). The fix is a **Newton iteration, not a proposal
redesign**; the `initial_guesses_ISD` proposal is still impractically slow (vmapped JIT, 20+ min
CPU at h12=5), so a fast cone sampler + iterated shift is the working path.

