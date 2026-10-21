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

- **⚠️ ADVERSARIAL REVIEW FOUND FLAWS — fix before publishing** (`docs/adversarial-review.md`,
  6 agents attacked the result). **FATAL:** (1) "search is provably dead" is overclaimed —
  the theorem only rules out *exact polynomial duality-invariant* selectors, NOT
  moduli-dependent / non-polynomial / statistical ones (and N ≤ L *bounds* the search space,
  supporting selection); downgrade to "no exact polynomial invariant selector". (2) The
  tadpole is NOT a complete invariant over ℤ — the content `d = gcd(F,H)` with `d² | N` is an
  extra invariant, so non-squarefree N splits into multiple orbits; restate Completeness as
  "finitely many orbits per tadpole (one per divisor d | √N)" and handle N=0. **SERIOUS:**
  (3) hypercharge uniqueness needs the extra assumption `Y_Q ≠ 0` (a third unphysical branch
  `(0,t,−t,0,0)`); (4) Chevalley–Shephard–Todd is misapplied (it is for FINITE reflection
  groups, Sp is infinite) — drop/replace the "free ring" claim; (5) name the FFT group as the
  FULL duality group Sp×SL(2,ℤ), not just "duality" (SL(2) alone gives the Plücker ring).
  **HELD:** Mitchell's Uniqueness, the constraint-first framework, the 19 count, Darboux,
  Atiyah–Singer, K-theory, Gromov. The core survives; the headlines need scoping.
- The **Mitchell Verification Deficit** is the count `m` of observables that are
  simultaneously measured + computable + validated. Today **m = 9**: topology
  (CYTools: h11, h21, c2, κ) = 4, flux (JAXVacua: tadpole = exact symplectic
  pairing FᵀJH) = 1, Standard Model (sympy, exact) = 4 (anomaly cancellation 5/5,
  hypercharge uniqueness 4/4, N_gen=3, 19 = orbit-space dim). The SM's 19 free
  parameters remain unvalidated as *predictions* — only their exact structure is climbed.
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
  **UPDATE 2026-10-21 — it is not only a speed problem.** The first real h12=25 run
  (pacland-rog, overnight) found **0 critical points in 13,311 candidates**: the ISD
  proposal itself degrades ~40x at h12=25 (starting `|dV|` median 173 vs 4 at h12=2),
  so `scipy`/`hybrid`/`sample_SUSY_flux_vacua` all fail, and enabling instanton
  corrections (`maximum_degree>0`) does not help. See `docs/h12-25-sampling-wall.md`
  for the measured numbers and next directions.
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
- **Darboux connection** (`docs/darboux-connection.md`): Darboux's theorem (a symplectic
  form has NO local invariants) is the DIFFERENTIAL half of the constraint-first result;
  Weyl's FFT (Sp's only invariant = the tadpole) is the ALGEBRAIC half. They are two
  different theorems, two steps in one chain (Darboux: local geometry → Sp(2n); FFT:
  Sp(2n)-invariants → tadpole), landing on the same sentence: the surviving exact
  structure is global topology (labels) + the constraint. NOT a duplication — a second
  independent foundation. (Rob found Darboux 2026-10-19.)
- **The Five Pillars** (`docs/five-pillars.md`): a 6-way fan-out found the COMPLETE
  scaffolding of constraint-first, in five slots each with named theorems — local (Darboux),
  algebraic (Weyl FFT: the invariant ring is C[tadpole], a single generator), global (Gromov
  non-squeezing / capacities, Eliashberg–Gromov C⁰-rigidity, Arnold conjecture, Marsden–Weinstein
  reduction, Delzant, Duistermaat–Heckman), topological (Atiyah–Singer: N_gen=|χ|/2 = index;
  K-theory: D-brane charges = K(X) classes, tadpole = "total charge = 0 in K(X)"; Bott
  periodicity), counting (Molien–Weyl + Hilbert–Serre: 19 = orbit-space dim; Morse m_k≥b_k;
  Ashok–Denef–Douglas: signed vacuum count = topological index, unsigned only bounded). Three
  sharper statements: (1) vacuum count is bounded-not-fixed by topology; (2) the constraint is
  a K-theory vanishing, not just an algebraic pairing; (3) the vacuum space is a symplectic
  quotient (Marsden–Weinstein). Mirrors the "four walls" (obstacles) with "five pillars"
  (foundations). Fan-out script: `research/theorem-hunt-fanout.js`.
- **Constraint-First Theorem** (`docs/constraint-first-theorem.md`,
  `scripts/validate_constraint_first.py`, 5/5 degrees, exact): the tadpole generates
  the **entire** ring of symplectic invariants of the flux pair — every
  duality-invariant exact polynomial in (F,H) is a power of FᵀJH. This is the First
  Fundamental Theorem of invariant theory (Weyl 1939) specialized to k=2; Mitchell's
  theorem is its degree-2 slice. So "the only exact structure is the constraint" is
  now a **theorem** (Weyl + measurement), not a conjecture.
- **Mitchell's Completeness Theorem** (`docs/mitchell-completeness-theorem.md`,
  `scripts/validate_mitchell_completeness.py`, 6 exact + 2 numeric): the tadpole FᵀJH is the
  **UNIQUE** duality-invariant of the flux. Lemma 1 = Constraint-First (FFT); Lemma 2 = over
  ℝ Sp(b₃) acts transitively on each tadpole level set (orbit tangent rank = 2b₃−1 = 11,
  exact), while over ℤ there are **finitely many orbits per tadpole** (content d=gcd(F,H),
  d²|N) and N=0 is several lower-dimensional orbits. Consequence: no *exact polynomial
  duality-invariant* function can single out a vacuum — a no-go on exact invariant selectors,
  NOT on statistical/moduli-dependent/non-polynomial selection (⚠️ corrected by the
  adversarial review; "complete invariant" and "search provably dead" were overclaims).
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
- **Standard-Model frontier (the next physics)** (`docs/sm-frontier.md`; scripts
  `validate_sm_anomaly.py` 5/5, `validate_sm_hypercharge_uniqueness.py` 4/4,
  `validate_sm_parameter_count.py`, all exact): extends constraint-first one sector up.
  The SM's exact structure decomposes exactly like the flux sector's — **constraints**
  (anomaly cancellation, charge quantization) + **labels** (gauge group SU(3)×SU(2)×U(1),
  N_gen=3 = topological index) + **parameters** (19 free couplings, counted). Proven:
  (1) anomaly cancellation 5/5; (2) **gauge-sector uniqueness** — anomaly conditions force
  the hypercharges uniquely up to normalization + u↔d swap (SM analog of Mitchell's
  Uniqueness). **Honest distinction (important):** "unpredicable within the SM" is a
  trivial counting fact (the 19 are free inputs); "unpredicable in any UV completion" is
  the CONJECTURED generalization, NOT proven — the flux theorem was provable only because
  flux has a clean duality group (Sp) + FFT, which the SM's couplings lack. Falsifiable:
  any UV relation among the 19 parameters (e.g. GUT unification) breaks the conjecture.
  **Refined by the 5-way fan-out** (`docs/sm-conjecture-notes.md`): GUT/string DO relate
  the parameters (gauge unification, geometric Yukawas) → "no invariant relates them" is
  overclaim; the surviving claim is "no unique *value* is derived — only relations"
  (a ToE predicts relations/invariants, never values). Fan-out tool + recipe:
  `research/sm-conjecture-fanout.js`, `docs/research-fanout.md`.
- **The Lean "proof arm" is STARTED, not deferred** (`pacland-proof/`, Lean 4.35 +
  Mathlib): `PaclandProof/Mitchell.lean` machine-checks **Mitchell's Uniqueness
  Theorem** for n=1 — the only `2×2` matrix with `SᵀMS=M` for all symplectic `S` is a
  scalar multiple of `J` (plus `J` antisymmetric ⇒ `FᵀJF=HᵀJH=0`). `General.lean` now
  machine-checks the **general-n** theorem too: `scalar_of_commute_all_symm` +
  `mitchell_uniqueness` (for abstract `l`, any field `R`) — the only matrix with
  `SᵀMS=M` for every symplectic `S` is a scalar multiple of `J l R`, plus the shear /
  block-diagonal / swap generators and the pairing invariance. **The "bigger machine"
  was a false wall:** the 16 GB Mac runs `lake build` fine via the mathlib cache (7.2 GB
  in `.lake`, git-ignored). No `sorry`/`axiom`/`admit`/`native_decide` — all
  kernel-checked. Reproduce: `cd pacland-proof && lake build`.
  **Completeness (transitivity) is now machine-checked for n=1** (`PaclandProof/Transitivity.lean`:
  `Sᵀ J S = det S • J`, so symplectic ⟺ det = 1, and `{xᵀJy = 1}` is one SL(2) orbit).
  Remaining Lean target: transitivity for **general n** (the orbit-tangent rank argument).
  PhysLib is public (leanprover-community/physlib).
- `pacland climb` runs the deficit climber on the mesh (studio-linux via
  `mac → win-2 → studio-linux`); `data/cy_corpus.json` is the answer key.
- **Swampland connection (2026-10-19):** `src/pacland/swampland.py` +
  `scripts/test_swampland.py` turn the constraint-first conjecture into per-conjecture
  tests. WGC scale g·M_pl is uniform in flux (r < 0.25, confirmed); charge gcd = 1
  (no forced discrete global symmetry); distance proxy real signal (CS-sector; clean DC test needs the bigger
  machine). Extends the *prediction* surface, NOT the deficit (m stays 9).
- Live site: https://pacland.netlify.app (Netlify) + GitHub Pages mirror.
- The four-wall map is `src/pacland/limits.py` and `docs/boundary-map.md`.
- **TO-DO — the verification system's remaining uses (queued, not done):**
  1. Climb the SM deficit — **DONE** (`src/pacland/observables.py::SM_OBSERVABLES`): the
     SM's exact structure is now 4 validated rungs (anomaly 5/5, hypercharge 4/4, N_gen=3,
     19 = orbit-space dim), raising **m from 5 to 9** (topology 4 + flux 1 + SM 4).
  2. Rule of Three on the SM results — **DONE** (`scripts/crosscheck_sm_float.py` +
     `docs/sm-rule-of-three.md`): anomaly cancellation and hypercharge uniqueness now have
     three agreeing arms (sympy exact + independent float method + literature); the "19"
     was already three-way checked by the rank test.
  3. The rank test (the floor question) — **DONE** (`scripts/validate_sm_rank_test.py` +
     `docs/sm-rank-test.md`): the SM's *own* flavor symmetry leaves orbit-space rank **19**
     (quark 26→10, lepton 15→3, exact Jacobian rank; flux control collapses to rank 1),
     three-way checked; the *dynamical* rank bound is **rank ≤ 2·h¹¹ + 2·h²¹ + 2** → reducible
     for h¹¹+h²¹ ≤ 8, generically real only for h¹¹+h²¹ ≥ 9; the ONLY known UV symmetry (GUT)
     collapses exactly **3 of 19** (gauge 3→1, b–τ 2→1) — no total collapse (SM has no duality
     group + FFT). **Answer: the 19 floor is real.**
  4. Four-wall map for the SM — **DONE** (`src/pacland/limits.py::SM_BOUNDARIES` +
     `docs/sm-boundary-map.md`): the 19 values (underdetermined), the UV completion
     (underdetermined), UV verification (unmeasurable), non-perturbative QCD (intractable),
     strong CP (underdetermined). The SM's exact structure is computable — the values are not.
