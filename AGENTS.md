# PACLAND — operating rules (read before working in this repo)

## The Rule of Three — no result from one test (Rob: "we need at least 3")

Never claim "structured" or "random" from a single measurement. Every such claim
needs **at least three independent confirmations**, and they must *agree*:

1. **Single-coordinate MI** (information-theoretic — catches single-coordinate structure).
2. **Joint ridge-quadratic CV r** (catches multi-coordinate structure — the strong test).
3. **Permutation null z** (catches spurious correlation — separates signal from finite-sample bias).

The canonical failure: W0 was called "random" on test 1 alone (MI z≈1.95), but test
2 disagreed (ridge r≈0.62 on the natural measure), so the claim was **retracted**.
If all three had been required, the error would never have shipped. The tadpole
(r=1.0 on all three) is the positive control proving the tests work; a claim whose
three tests disagree is *unresolved*, never "one test says X so X."

## The one rule that matters: USE the wall, don't hit it

"Uncomputable" is **four different walls**, each with a *way around*. A wall is
not a place to stop — the way around IS the result.

| wall | meaning | the move (use this, don't just report the wall) |
|---|---|---|
| **intractable** | answer exists, no feasible algorithm | prove intractability (a theorem), or find structure that shortcuts it |
| **unmeasurable** | answer exists, ground truth / data absent | compute the **deficit** — how far we are from measuring it |
| **underdetermined** | no unique answer exists | compute the **set's invariants** (constraints, boundary), not the nonexistent point |
| **undecidable** | provably no algorithm | prove undecidability (an impossibility certificate) |

Rob's rule, verbatim: *"you hit a wall instead of using the wall."* When a
computation fails (OOM, too slow, no known value), classify which wall it is and
apply the move. Example that already happened: the mass spectrum is killed even at
n=10 → that is the **unmeasurable** wall → the deliverable is the *deficit* (m), not
the spectrum. Documenting the wall is not the result; using it is.

## Hard physics rule: mirror symmetry is a free validation target

For a Calabi-Yau threefold and its mirror (the polar dual polytope):

    h11_m = h21,   h21_m = h11,   chi_m = -chi    (chi = 2(h11 - h21))

This is an always-true theorem, so **any CY's mirror gives a known-exact answer to
validate the oracle against, for free** — no external database needed. Encoded as
`pacland.guards.guard_mirror_symmetry` (mutation-tested). Verified pair:
quintic (1,101,−200) ↔ mirror quintic (101,1,+200). Use it whenever the corpus needs
more known-answer manifolds.

## Gotchas that already cost retractions (check before claiming a wall)

Three "walls" turned out not to be walls, each caught by a source/control check.
**Before claiming any elimination, verify the number against the model's own
source, not a textbook formula:**

1. **Orientifold charge is `model.Q()`, not χ/24.** `FluxEFT(...).Q()` returns the
   D3 tadpole bound (276 for the h12=2 KS model). χ/24 ≈ 22 is the O3-only piece and
   is *wrong* for the full O3/O7 orientifold. With L=276 the tadpole bound is
   pre-satisfied (max N_flux ≈ 265), so it eliminates 0% — not 74%.
2. **Weak coupling is a sampler artifact.** The ISD sampler only produces g_s < 1, so
   "gs<1" eliminates 0% of both SUSY and non-SUSY points. Check the *distribution* of
   the pre-imposed condition before calling it a wall.
3. **The "Kähler cone" on the CS moduli is a mislabel.** The Kähler cone is a
   condition on the *Kähler* moduli (flat at degree-0), not the complex-structure
   moduli. A positivity cut on `moduli_re` is not the Kähler cone.
4. **`kahler_metric` is the CS+dilaton field-space metric, NOT the Kähler moduli.**
   JAXVacua's `FluxVacuaFinder.kahler_metric` / `christoffel_symbols` compute the
   Kähler metric g_{i j̄}=∂∂̄K on the *complex-structure moduli + axio-dilaton* field
   space (K = −log(i∫Ω∧Ω̄)) — the fields the degree-0 model actually stabilizes. The
   *Kähler moduli* (volume T_i) are FLAT at degree-0 and do not appear. A geodesic
   from `kahler_metric` therefore lives in the CS sector, where the distance
   conjecture does NOT run (its tower is in the Kähler-moduli direction). Do not
   present a CS-sector geodesic distance as a distance-conjecture test.

## State (durable facts)

- The **Mitchell Verification Deficit** is the count `m` of observables that are
  simultaneously measured + computable + validated. Today **m = 5**: topology
  (CYTools: h11, h21, c2, κ) = 4, flux (JAXVacua: tadpole = exact symplectic
  pairing FᵀJH) = 1. SM physics = 0 (the real frontier).
- **Every JAXVacua model is a truncation.** `h12` = number of CS moduli KEPT. The
  bundled `h12=2` keeps 2 of 272 (its polytope has h¹¹=2, h²¹=272). All measured
  results (structure map, fingerprint, no-scale) are inside this 2-moduli slice.
- **TO-DO (bigger systems): run the full model — memory is solved, speed is not.** Two
  JAXVacua bugs are FIXED (studio-linux venv, `.bak` backups): (1) `M_cap_generators`
  unbound in `cytools_interface.py` — fixed, so **h12=272 now BUILDS**; (2) `ddV_x`
  was `jax.jacrev(grad(V_x))` — fixed to `jax.hessian(V_x)`. The ~96 GB OOM is now
  PROVEN to be the **vmapped Newton solver's** JIT tracing (`jax.vmap` + `while_loop`
  + `jnp.linalg.solve` → `broadcast_in_dim`): `V_x`/`dV_x`/`ddV_x` each compile fine
  individually ((), (52,), (52,52), in seconds), but the batched Newton trace explodes.
  **`solver="scipy"` bypasses it** (sequential, no vmap) and runs h12=25 on 4 GB —
  memory-safe but slow (~43 s/candidate). So the chase is a SPEED problem, not a 96 GB
  problem: make `scipy` (or a chunked `newton`) fast enough to sample hundreds of
  vacua. Paper's ancillary polytopes: arXiv:2306.06160 (h12_5..h12_25).
- `pacland climb` runs the deficit climber on the mesh (studio-linux via
  `mac → win-2 → studio-linux`); `data/cy_corpus.json` is the answer key.
- **Swampland connection (2026-10-19):** `src/pacland/swampland.py` +
  `scripts/test_swampland.py` turn the constraint-first conjecture into per-conjecture
  tests. WGC scale g·M_pl is uniform in flux (r < 0.25, confirmed); charge gcd = 1
  (no forced discrete global symmetry); distance proxy real signal (CS-sector; clean DC test needs the bigger
  machine). Extends the *prediction* surface, NOT the deficit (m stays 5).
- Live site: https://pacland.netlify.app (Netlify) + GitHub Pages mirror.
- The four-wall map is `src/pacland/limits.py` and `docs/boundary-map.md`.
