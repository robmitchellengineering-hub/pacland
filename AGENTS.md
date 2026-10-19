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
- **Exact T⁶ toroidal orbifold oracle (build #2 done properly):**
  `src/pacland/oracle/exact_t6.py` — closed-form periods, Kähler potential/metric,
  tadpole FᵀΣH (the *unique* moduli-independent observable), W, g_s, KK/winding
  tower, geodesic distance. The full swampland package (distance, WGC, no global
  symmetries) is *proven exactly*. Two verification grades: numerical 21/21
  (`scripts/validate_t6.py`) + **exact symbolic 8/8** (`scripts/validate_t6_sympy.py`,
  sympy, zero tolerance).
- **Mitchell's Uniqueness Theorem** (`docs/mitchell-uniqueness-theorem.md`,
  `scripts/validate_mitchell_uniqueness.py`, 6/6 symbolic): the D3 tadpole FᵀJH is
  the **unique** bilinear symplectic invariant of the flux, for *any* compactification.
  This is the rigorous backbone of the constraint-first conjecture — "the only exact
  structure is the constraint" is forced by symplectic geometry, not just measured.
- **Constraint-First Theorem** (`docs/constraint-first-theorem.md`,
  `scripts/validate_constraint_first.py`, 5/5 degrees, exact): the tadpole generates
  the **entire** ring of symplectic invariants of the flux pair — every
  duality-invariant exact polynomial in (F,H) is a power of FᵀJH. This is the First
  Fundamental Theorem of invariant theory (Weyl 1939) specialized to k=2; Mitchell's
  theorem is its degree-2 slice. So "the only exact structure is the constraint" is
  now a **theorem** (Weyl + measurement), not a conjecture.
- **Mitchell's Completeness Theorem** (`docs/mitchell-completeness-theorem.md`,
  `scripts/validate_mitchell_completeness.py`, 6 exact + 2 numeric): the tadpole FᵀJH is a
  **COMPLETE** invariant of the flux under duality — two pairs with N≠0 are
  dual-equivalent iff they have the same tadpole. Lemma 1 = Constraint-First (FFT);
  Lemma 2 = Sp(b₃) acts transitively on each tadpole level set (orbit tangent rank
  = 2b₃−1 = 11, exact, at generic points AND at the canonical pair). Consequence:
  no exact frame-independent quantity can distinguish vacua sharing a tadpole, and
  since N ≤ L is bounded, **search can only eliminate, never select** — the 20-year
  "search for a special vacuum" program is provably dead. Open question this names
  for the ToE: are ALL exact structures constraint structures (topology, charges,
  anomalies), with flux now proven to be a single constraint?
- **Full-duality completion** (`scripts/validate_full_duality.py`, 5/5 symbolic): the
  no-go holds for the FULL duality group Sp(b₃) × SL(2,Z), not just the monodromy
  subgroup. S-duality S:(F,H)→(−H,F) and T:(F,H)→(F,H+F) preserve the tadpole, and
  since Sp-invariants = C[N] (FFT) with N SL(2,Z)-invariant, the full invariant ring
  is exactly C[N].
- **Complete Exact Structure Theorem** (`docs/complete-exact-structure.md`): the ToE's
  exact content is exhausted by two types — **constraints** (tadpole N ≤ L, flux
  quantization, RR tadpoles, anomaly cancellation) and **labels** (topology h¹¹,h²¹,
  c₂,κ). Nothing else is exact; W₀, g_s, masses, couplings, Λ are provably NOT exact
  observables. Key consequence: the flux sector's contribution to the deficit m is
  **saturated at 1** (the tadpole) — m can never grow from flux again; future growth
  is only from branes/SM (the m=0 frontier). Falsifiable: a single moduli-independent
  duality-invariant flux quantity not a function of FᵀJH breaks the tower.
  `scripts/validate_all_theorems.py` runs the whole tower (6 proofs) in one command.
- **The Lean "proof arm" is STARTED, not deferred** (`pacland-proof/`, Lean 4.35 +
  Mathlib): `PaclandProof/Mitchell.lean` machine-checks **Mitchell's Uniqueness
  Theorem** for n=1 — the only `2×2` matrix with `SᵀMS=M` for all symplectic `S` is a
  scalar multiple of `J` (plus `J` antisymmetric ⇒ `FᵀJF=HᵀJH=0`). **The "bigger
  machine" was a false wall:** the 16 GB Mac runs `lake build` fine via the mathlib
  cache (only your own file compiles; mathlib's olean cache is downloaded, 7.2 GB in
  `.lake`, git-ignored). Reproduce: `cd pacland-proof && lake build`. Next targets:
  general-n uniqueness (block matrices over `Fin (2n)`), then transitivity
  (Mitchell's Completeness). PhysLib is public (leanprover-community/physlib).
- `pacland climb` runs the deficit climber on the mesh (studio-linux via
  `mac → win-2 → studio-linux`); `data/cy_corpus.json` is the answer key.
- **Swampland connection (2026-10-19):** `src/pacland/swampland.py` +
  `scripts/test_swampland.py` turn the constraint-first conjecture into per-conjecture
  tests. WGC scale g·M_pl is uniform in flux (r < 0.25, confirmed); charge gcd = 1
  (no forced discrete global symmetry); distance proxy real signal (CS-sector; clean DC test needs the bigger
  machine). Extends the *prediction* surface, NOT the deficit (m stays 5).
- Live site: https://pacland.netlify.app (Netlify) + GitHub Pages mirror.
- The four-wall map is `src/pacland/limits.py` and `docs/boundary-map.md`.
