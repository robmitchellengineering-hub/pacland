# The exactness programme — every kind of exactness we can use, and what each one decides

Planning room (`~/Documents/DeepSeek`), 2026-10-29, **v2**. Decisions: D9 (this folder owns intent, the
repo owns code), D10 (job → plan → decision), D14 (pacland is the method at maximum difficulty), D15
(physics is discipline-scale; its framing is the risk).

**v1 → v2.** v1 named eight kinds of exactness but built its six items almost entirely out of three of
them (X1/X2/X3), which are the kinds that exist **only** topologically, at special loci, or as
structure. The kinds that work **everywhere** — invariance, identity, exhaustion, known-answer controls
— had two uses between them. Rob: *"make a plan to use the other forms of exactness that work for us,
add the other types that work to the plan."* v2 turns each of those into work that runs on the data we
already hold, and adds the structural and closed-form rungs that are worth having.

Read with `docs/is-the-landscape-chaotic.md` (the chaos question and its build) and
`docs/unification-claim.md` (C1–C4). This plan does not re-ask those questions; it supplies instruments.

---

## 1. The eight kinds

| # | kind | exact because | where it exists | used by |
|---|---|---|---|---|
| **X1** | topological / integer | it counts something | everywhere (discrete) | A2, B1, R1 |
| **X2** | closed form at a locus | the analytic answer is known there | T⁶, LCS, orbifolds/Gepner, quintic special points | R1, R2 |
| **X3** | structural / recursive closure | a finite datum determines the rest | special geometry, Picard–Fuchs, holomorphic anomaly | B2, B3 |
| **X4** | invariance | change the description, not the world | **everywhere** | A1, A3, B3, B4 |
| **X5** | definitional identity | true by construction | **everywhere** | A1, A2, B4 |
| **X6** | arithmetic | Euler product / point counts / p-adic periods | not used yet | R3 (deferred) |
| **X7** | finite-window exhaustion | below `N ≤ L` the lattice is finite, so enumeration is complete | **everywhere**, conditional on a declared window | A4, D1 |
| **X8** | known-answer control | the reference answer is exact by construction | **everywhere** | A3, B4 |

The partition is the point: **X1/X2/X3/X6 are missing in the interior of moduli space and no search will
produce them.** X4/X5/X7/X8 need no closed form, so they are the only exactness available where all
5,885 vacua actually live. That is why seven of the twelve items below are built on them.

---

## 2. What the toolchain already exposes (verified, not remembered)

| capability | where | evidence |
|---|---|---|
| Hodge numbers, triple intersections, `c₂`, Kähler/Mori cones, GV invariants | CYTools 1.4.12 | `docs/tooling.md`, verified live on `studio-linux` 2026-10-18; the **quintic** returns `h11=1, h21=101, c₂=[-250,50,50,50,50,50]` |
| LCS tree, prepotential, instanton sums, F-terms, Hessian | JAXVacua | `oracle/adapters.py:85` — `jvc.lcs_tree.from_cytools(cy, maximum_degree=1)` |
| **the truncation knob is a named parameter** | `maximum_degree` | same call — this is what "truncation" means in our stack |
| instanton sum is tiny in our models | 2 GV charges, correction ~0.004 | `src/pacland/limits.py:82` |
| `V`, the `DW=0` solver, Hessian | `oracle/potential_t6.py` | #198–#200; no-scale `3.0000000000`, `V=0` at a SUSY Minkowski point, 4/4 |
| explicit symbolic arithmetic | sympy 1.14.0 in `/home/rob/cytools-venv` | 2026-10-22 mesh job |

**Routing, read live (not remembered):** `dispatch.py --list` on 2026-10-29 lists `mac`,
`pacland-rog`, `studio-linux2`, `win`, `win-2`. **`studio-linux` — the only node verified with cytools
+ jaxvacua — is not registered**, and the VMs on `win-2` do not auto-start. Group A, D1 and R1's analytic
target run on the Mac; B1/B2/B3 and R1's numeric periods need that node.

---

## 3. Group A — the interior's exactness (works on data already on disk)

### A1 · Kähler-gauge invariance, as a bug detector (X4 + X5)

`K → K + f + f̄` is a field redefinition: `V`, the masses and every physical quantity must be
**unchanged to machine precision**, because `D_iW` transforms covariantly. An implementation that uses
`K` without the covariant structure moves — and the move is invisible in any single run.

- **Test:** shift `K` by `c·z` (and by a constant), recompute `V`, the gradient and the Hessian
  eigenvalues; all must agree within 1e-12 relative.
- **Why now:** the `limits.py` boundary for the instanton-corrected spectrum ends on *"the CS-vs-Kähler
  (mirror) moduli convention, to be read from arXiv:2306.06160"*. That convention bug is exactly what a
  gauge-invariance test catches, and it is cheaper than reading the paper.
- **Falsifier:** a shift that moves `V`. That is a bug in `potential_t6.py`, not a finding.
- **Where:** Mac. Cost: an hour.

### A2 · The identity battery over the whole corpus (X5 + X1)

One command over the 14 `data/h12_*_stats.json` files, printing per-row failures rather than a verdict:

| identity | why it must hold |
|---|---|
| `N = FᵀJH ∈ ℤ` | the flux pairing is integral; a non-integer means the basis or the flux record is wrong |
| `N = χ/24` per model | the flux charge is the topological charge — this ties the discrete flux data to the geometry, and nothing in the corpus currently checks it |
| `det Σ = ±1` | the intersection form is unimodular; a wrong basis breaks it |
| gauge-invariance residual (A1) per row | the recorded `V` and `eigenvalues` must be gauge-invariant |
| `d² | N` and `gcd(F,H) = d` | already known to hold on all 5,885 rows — keep it as a **regression**, not a discovery |

- **Can it fail?** Prove it before trusting it: seed a basis change into one model and the battery must
  go red. A battery that cannot go red is decoration.
- **What it buys:** the first time the corpus is checked against the geometry it claims to come from.
- **Where:** Mac, on disk. Cost: an afternoon.

### A3 · The same-size known-answer gate for every statistic (X8)

Three times now a statistic has been read against the wrong reference: the `|W|` lattice (no
fluctuations to report), the 0.5307 zeros scare (the GOE value used as GUE's), and the chaos arm's
zero-mode trap. Make the control a **gate** rather than a habit:

- one function — `control(statistic, n, dim, pooling)` — that builds a **GOE** control, a **GUE**
  control, and a **Poisson** control matched on dimension, level density **and** pooling, and returns
  the measured value with its finite-size offset;
- an **authority test**: the pipeline is not allowed to report an unknown class until it recovers a
  *known* one — feed it a deliberately order-destroyed spectrum (shuffle the eigenvalues) and it must
  return Poisson; feed it GOE matrices and it must return GOE.
- **Falsifier:** a shuffled spectrum that still reads "repulsion". Then the estimator is broken and no
  chaos number from it counts.
- **Where:** Mac. Cost: small, and it is the item that stops the fourth repeat.

### A4 · The sampler's coverage — and its recall — in the smallest window (X7 + X8)

The corpus is a **heuristic** sample (the ISD proposal). Its recall is unknown, and every "fraction of
vacua" sentence silently assumes it is 100%.

- **Step 1 (exact, instant):** enumerate the smallest flux window exhaustively — `|F_i|, |H_i| ≤ 1` at
  h12=2 is `3¹² = 531,441` pairs, cut further by the flux-scaling lemma (primitive pairs only, since
  `(F,H)` and `d(F,H)` are the same vacuum). Match every corpus row's orbit against the enumerated set
  and report **coverage**: which small-flux orbits the sampler has never visited.
- **Step 2 (the cost decision):** for the uncovered orbits, run the `DW=0` solver to get the true count
  of SUSY-admitting pairs in the window, and divide.
- **Falsifier:** recall below 100% in a window where enumeration is complete. Then **every** fraction
  in this programme is a statement about the sampler and must be relabelled as such — which is a
  publishable finding, not a nuisance.
- **Where:** Mac for step 1; a node for step 2 if the solve count is large.

---

## 4. Group B — discrete and structural exactness (the wall, and gaps G1/G2)

### B1 · GV integrality — an independent check on the period pipeline (X1)

Extract `n_d` from the computed prepotential at several points. GV invariants are integers by
definition (BPS counts); non-integral output means the periods are wrong **at that point**, with no
oracle needed.
**Falsifier:** a non-integer `n_d`, or values that move with the point when they must not. Shares B2's runs.

### B2 · The truncation ladder — the item that can decide the wall (X3)

With `Im T ≥ 2` from the sampler bounds, the neglected degree-`d` instanton is suppressed by
`e^{−2π d·Im T}`: degree 1 ≤ **3.5×10⁻⁶**, degree 2 ≤ **1.2×10⁻¹¹**. The observed h12=25 failure is
`|dV|` of order **10²–10³** against 0.3–4.1 at h12=2 — eight orders above the largest neglected term.

- **Hypothesis:** the near-null direction of `Im N` is real geometry, not truncation.
- **Test:** `maximum_degree = 1, 2, 3`; does `cond(M)` move?
- **Falsifier:** `cond(M)` moving by more than 10% ⇒ it *is* truncation, and the degree is the fix.
- **If it holds:** the h12 ≥ 5 wall is the integer-lattice problem that
  `docs/is-the-landscape-chaotic.md` found from the other end this week (a generic integer flux is
  F-flat **nowhere**), with `1/λ_min` as the magnification. Then no solver, degree or ensemble size
  fixes it, and the effort belongs to non-SUSY `DV = 0` vacua.

### B3 · Monodromy — the covariance table as a derivation (X4 + X3)

The Picard–Fuchs/GKZ system gives integer monodromy matrices `M ∈ Sp(2h+2,ℤ)` with the
machine-checkable identity `MᵀΣM = Σ`. Every observable's transformation law follows by differentiating
the period action — so **G1** becomes a closed-form derivation instead of a fit with a log residual, and
the open phase half of Law II is exactly what the monodromy fixes.
**Falsifier:** `MᵀΣM ≠ Σ` (implementation error), or a law that fails to close under a full generator.
**First step is a capability probe** — does CYTools 1.4.12 expose periods/PF operators? If not, this is
a build (Frobenius on the GKZ system), and the build is the deliverable.

### B4 · Two provable controls for the mass spectrum (X4 + X5)

Both provable today, both for the chaos arm:

1. **`d`-scaling cannot contaminate the level statistics.** The flux-scaling lemma (`W → dW`,
   `DW → d·DW`) gives `V → d²V` and therefore `M² → d²M²` at a shared critical point; an overall scale
   drops out of *unfolded* spacings. Ensembles mixing `d` are provably clean — that asterisk is closed
   before the run, not carried.
2. **A supersymmetric point is AdS, and the value is fixed.** At `DW = 0` every term in
   `g^{i jbar} D_i W D_jbar Wbar` vanishes, so what is left is `V = -3 e^K |W|^2` — exactly, with no
   freedom. Measured on the recovered constructed vacuum: relative residual **1.9e-16**. So the exact
   control is this identity, not a zero mode: **v2 of this plan said "Minkowski", and that was wrong**
   for this model (`potential_t6.py` has no Kähler modulus, and `V = 0` at SUSY needs `W = 0`). The
   zero-mode trap the chaos doc warns about is real, but it lives at `W -> 0`, and the identity is what
   tells you which case you are in.

**Falsifier:** an unfolded statistic that moves under `d → 2d`, or a claimed SUSY point with no exact
zero mode. Either is a bug in the spectrum.

---

## 5. Group C — closed-form rungs (X2), and the one kind still unused (X6)

### R1 · A known-answer rung on a *real* Calabi–Yau: the quintic's special points (X2 + X8)

`docs/quantum-arm-agenda.md` names the gap to a real CY as the arm's largest missing machinery, and
`exact_t6.py` is the only exact oracle. But the quintic has **exact period values at special points of
its moduli space** (the conifold point, and the large-complex-structure limit) with a closed form built
from Γ-functions — literature to be pinned down and cited before use, not asserted here.

- **What it buys:** a real-CY (not torus) known-answer target for the period pipeline — a rung between
  T⁶ and a general CY oracle, on the model the CYTools adapter already handles.
- **Falsifier:** the pipeline's period at the special point misses the closed value by more than the
  series bound. Then the period pipeline is wrong on real CYs and every downstream number is suspect.
- **Where:** the Mac for the analytic target; the node for the numeric periods.

### R2 · A second exact rung — and the only item that can falsify the claim's C3 (X2)

- **K3 × T²**: complex-structure moduli space is the symmetric space `O(2,19)/(O(2)×O(19))`, so the
  period domain and special-Kähler metric are closed form. A second exact oracle with `h¹¹ = 20` — real
  gauge structure, unlike T⁶.
- **Toroidal orbifolds / Gepner points**: the worldsheet CFT is exactly solvable, so **every `α′`
  correction is exact**, not just the leading term. And they carry **discrete torsion**:

> the sharpest test on the board. Discrete torsion is exact, discrete, topologically classified, cheap
> to enumerate — and it **changes the spectrum**. C3 says distinct orbits ⇒ distinct physics; torsion is
> a label the orbit data does not contain, so two configurations with the same `(N, d)` and the same
> moduli can differ physically. That is C3's **injectivity** failing from a direction the corpus cannot
> represent (it samples smooth CYs and records no torsion). Same *class* of object as `d` — except `d`
> is provably empty and discrete torsion is provably not.

**Falsifier:** a pair of orbifold configurations with identical orbit data and different spectra. Then
the claim needs a fourth bucket, or "label" needs splitting into *observable* and *redundant*.

### R3 · Deferred — arithmetic exactness (X6)

The L-function of the family / p-adic periods: the only exactness that shares no code, no sampler and no
series with the period computation, so the only true cross-source check on it. Expensive; revisit once
B2 has answered the wall.

---

## 5a. First results — the interior instruments, run (2026-10-29)

`src/pacland/exactness/` · `python3 scripts/exactness.py` · 18 tests, every check mutation-tested.

| item | measured | reading |
|---|---|---|
| A1 + B4 | 5/5 invariance and identity checks pass; `D_i W` covariant to `1.9e-9`, `V` phase-invariant, `V(dF,dH) = d^2 V`, the unfolded spectrum and ratio statistic unchanged under `d = 2` | the potential's assembly is the documented one, and the `d`-content provably cannot contaminate a spacing statistic |
| A1 (correction) | at the recovered SUSY vacuum `V = -3 e^K \|W\|^2` to **1.9e-16**, `V = -1.847e-02 < 0` | a SUSY vacuum here is **AdS4**, not Minkowski. v2 of this plan had this wrong — see B4.2 |
| A2 | 5,885 rows: **5 failures, all one kind** — recorded `Nflux` is the negative of `F^T J H` for the stored ordering (either the pair is stored `H ++ F` or the tadpole was recorded as a magnitude) | pinned as `KNOWN_SIGN_FLIPS`, 0 unexplained. A new one goes red. `N <= chi/24` is **skipped** (no `h11` on disk) — unknown, not green |
| A3 | at 40 spectra of dim 6 the GOE and Poisson bands sit **2.4 combined sd** apart, so the gate returns `undecidable`; the required size is **202–273** spectra | **the chaos question is reachable**: the h12=2 corpus holds 3,424. And the gate states the budget instead of discovering it after the run |
| A4 | the corpus covers **13 of 531,440** primitive orbits in the smallest window (**0.0025%**); its largest flux component is **62** | the sampler never visits the small-flux region. Every "fraction of vacua" is a statement about its flux range until recall is measured inside a window |
| D1 | same window, two measures: at `L = 1` the fraction is **0.2015** flux-uniform vs **0.1667** label-uniform; at `L = 6`, **0.3797** vs **1.0000**. Largest shift **0.62** | the measure problem, demonstrated on a finite lattice rather than argued. (All-vs-primitive coincides here — every non-zero pair in this window is primitive — and the code says so instead of reporting a vacuous agreement) |

Three of these are findings, not checks, and they arrived by running rather than by plan: the AdS
identity, the 5 pinned corpus defects, and the fact that the chaos question needs ~200 spectra rather
than being out of reach.

## 6. D1 — the finite-window measure tool (X7)

`docs/quantum-arm-agenda.md` Q3 and the chaos doc both end at "this may be a measure question". X7 is
the only exactness that lets us *state* a measure claim without an oracle:

- **D1:** an exact enumerator over the bounded flux lattice with the **window printed in the output**, so
  "the fraction of vacua with property P below `N ≤ L`" is a reproducible artefact rather than a number
  from a run;
- plus the **convergence table in `L`** — the fraction at each window, which is what makes the "is it
  the measure?" claim demonstrable instead of rhetorical.
- **Falsifier:** the fraction must move with `L`; if it is flat in `L` for two different measures, the
  claim that the 10⁵⁰⁰ argument is about measures loses its demonstration.
- **Where:** Mac, corpus on disk.

---

## 7. Order, and why

```
A1  gauge invariance      DONE — 5 checks, mutation-tested; produced the AdS correction
A3  the control gate      DONE — and it says the chaos question needs ~200 spectra
A2  the identity battery  DONE — 5 pinned sign-flip rows, 0 unexplained, chi/24 skipped
B4  the two controls      DONE — d-scaling proven clean; the SUSY identity measured
A4  coverage / recall     step 1 DONE (0.0025% coverage); step 2 needs the solver on a node
D1  finite-window measure DONE — two measures, shift 0.62, demo in the report
B2  truncation ladder     NOT STARTED — decides the wall; needs studio-linux up
B1  GV integrality        NOT STARTED — rides on B2's runs
B3  monodromy table       NOT STARTED — closes G1; starts with a capability probe
R1  quintic rung          NOT STARTED — the only real-CY known-answer we can reach cheaply
R2  second rung           NOT STARTED — the only scope test of the claim's C1/C3
R3  arithmetic            deferred
```

**Gates:** A3 before any spacing statistic is published. B2 before any h12 ≥ 5 number is called a
landscape fact. A4 before any fraction is quoted. R2 is the only item that can overturn a claim rather
than certify one — it should not be starved.

## 8. What none of this does

- It does not raise `m` (still **9**: topology 4 + flux 1 + SM 4). Exactness changes the *oracle class*
  of what is already claimed; it does not certify a new parameter.
- It does not produce a closed form for the interior of moduli space, because none is known.
- It does not touch the 19 Standard-Model parameters. C4 remains a conjectured bet.
- It does not rescue the claim's C1 or C3. R2 is here partly to see whether they survive.

## 9. The rule this plan works under

Every item names its exact term, its falsifier, and — before it runs — **how the falsifier could come
out**. An item whose falsifier cannot fail is a demonstration, not a test, and belongs in the docs
rather than in this plan.

## 5b. B2 ANSWERED — the wall IS series truncation at degree 1, and degree 2 fixes it

Two runs on **pacland-rog** (the only node with the oracle stack: `jax 0.12.0` imported clean), by
`scripts/node_b2_truncation.py` and `scripts/node_b2_followup.py`. Both had the falsifier written into
the script and printed before the run: **a move >10% in `cond(M)` between degrees 1/2/3 means the wall
is series truncation, not geometry.**

### Run 1 — one generic point per h12, instanton corrections as the library left them

| h12 | cond @deg1 | cond @deg3 | move | verdict |
|---|---|---|---|---|
| 2 | 6.1347e3 | 6.1347e3 | 0.00% | geometry |
| 5 | 8.2173e9 | 8.2173e9 | 0.00% | geometry |
| 10 | 9.3210e5 | 1.1716e6 | 27.75% | truncation |
| 25 | 1.7287e6 | 1.7206e6 | **0.47%** | **geometry** |

Run 1 said h12 = 25 was geometry. **It was wrong**, and for exactly the reason the caveat written next
to it said: one point per h12 cannot separate a degree effect from where the point landed, and jaxvacua
had warned that mirror worldsheet instanton corrections were **disabled** while GV charges were provided.

### Run 2 — five points per h12, instanton corrections ON (`mirror_instanton=True`, accepted by the constructor)

The warning is gone from all four h12, so the ladder is now measuring the series it claims to.

| h12 | max move | median move | verdict |
|---|---|---|---|
| 2 | 0.00% | 0.00% | geometry |
| 5 | 0.00% | 0.00% | geometry |
| 10 | **33.41%** | 6.75% | **truncation** |
| 25 | **88.39%** | 6.38% | **truncation** |

And the shape of the failure is the finding. At h12 = 25, per point (degrees 1 / 2 / 3):

| point | deg 1 | deg 2 | deg 3 | deg2 vs deg3 |
|---|---|---|---|---|
| 0 | 1.9385e6 | 1.8223e6 | 1.8223e6 | **identical** |
| 1 | 1.2658e6 | 1.6326e6 | 1.6326e6 | **identical** |
| 2 | 2.6337e6 | 1.3980e6 | 1.3980e6 | **identical** |
| 3 | 1.3122e6 | 1.3156e6 | 1.3156e6 | **identical** |
| 4 | 5.8137e6 | 5.6015e6 | 5.6015e6 | **identical** |

**Degree 1 has not converged; degree 2 has.** `d2 = d3` at every one of the five points, while `d1`
differs from them by up to 88%. So the h12 ≥ 5 wall is **series truncation at degree 1** — which is what
the sampler uses (`maximum_degree = 0/1`) — and **the fix is `maximum_degree = 2`**, not a new solver,
not a new ensemble, and not "the wall is geometry".

That inverts the reading of the plan's own hypothesis (B2: *"If it holds: the h12 ≥ 5 wall is the integer
lattice problem"*). It does not hold: the truncation hypothesis is the one that survives, and the degree
is the fix.

### What run 1 taught, kept because it will happen again

The single-point answer was **plausible, wrong, and consistent with a caveat already written next to
it**. The correction cost one extra dispatch. The rule this repo already has — *a statistic needs a
same-size control and more than one sample, or it is a draw* — is the rule that caught it.

## 5c. B1 — GV integrality fires, and only on the NON-PRIMITIVE degrees (2026-10-29)

`scripts/node_b1_gv.py` on pacland-rog, h12 = 2, `maximum_degree = 2`, `mirror_instanton = True`.
`F_inst` is fitted against a basis of `Li_3` terms over 20 imaginary moduli points (y ∈ [0.30, 1.00]).
**Falsifier, stated before the run:** a non-integer `n_d`, or `n_d` that move with the point.

| degree d | fitted n_d | deviation from integer | verdict |
|---|---|---|---|
| (0,1) | **-3.0004** | 4e-04 | integer |
| (1,0) | **-540.0009** | 9e-04 | integer |
| (1,1) | **1080.009** | 9e-03 | integer |
| (0,2) | **+5.6265** | **3.7e-01** | **NOT integer** |
| (2,0) | **-607.48** | **4.8e-01** | **NOT integer** |

**Every primitive class comes out integral. The two non-primitive classes do not.** The values are not
noise: they recur between two disjoint point sets (drift 1.9e-02, against a fit residual of 2.5e-07), and
`n_(0,2)` and `n_(2,0)` reproduce across `maximum_degree` 2 and 3 even when the rest of the fit does not.

**So B1's falsifier fires, and it fires in a specific place.** That is the useful outcome: the period
pipeline is integral on primitive curve classes and not on non-primitive ones, which points at the
curve-class basis convention (a half-integral normalisation shows up exactly this way) rather than at the
periods themselves. Until that is settled, **primitive-class `n_d` are usable and non-primitive ones are
not**, and any GV table taken from this pipeline should say which classes it is quoting.

### The first run of B1 was wrong, and the reason matters more than the fix

It fitted degrees up to 3 over a window y ∈ [0.8, 2.6], where `e^{-2π d·y} ~ 1e-7`: the higher basis
columns were **noise**, least squares was free to put anything in them, and it duly reported "non-integer
n_d" — the falsifier firing on **my test**, not on the pipeline. The window is now chosen so the
instantons are *visible* (`q ~ 0.15`), the basis is restricted to what the window can resolve, and the fit
residual is checked first (2.5e-07 here) before any integer claim is made.

**A fit whose basis outruns its data will always produce a finding. It just won't be about the physics.**

## 5d. B3 — the capability probe says BUILD, and names what the build needs (2026-10-29)

The plan is explicit that B3's first step is a capability probe: *"does CYTools 1.4.12 expose
periods/PF operators? If not, this is a build (Frobenius on the GKZ system), and the build is the
deliverable."*

**It does not.** `cytools.calabiyau.CalabiYau` on pacland-rog exposes `compute_gv`, `compute_gvs`,
`compute_gw`, `intersection_numbers`, `compute_kappa_matrix`, `curve_basis`, `triangulation` and the
rest of the toric/intersection toolkit — and **no** `picard_fuchs_equation`, **no** `monodromy_matrices`,
**no** period solver. (The earlier probe's `AttributeError: module 'cytools' has no attribute
'CalabiYau'` was a wrong import path, not a missing feature: the class lives at
`cytools.calabiyau.CalabiYau`.)

So **B3 is a build**, and the build has a natural first target where the operator is already known in
closed form: the **quintic**, whose Picard–Fuchs operator is the hypergeometric

    L = θ⁴ − 5z (5θ+1)(5θ+2)(5θ+3)(5θ+4),    θ = z d/dz

with monodromy generated by the unipotent `z → 0` generator and the conifold generator at `z = 1/5⁵`.
That is also exactly where R1's target value lives, so **one build serves B3 and R1** — the Frobenius
solution at the conifold point and the monodromy around it are the same computation looked at twice.

**Not done here, and stated as not done:** neither the build nor R1's literature value has been
established in this session. R1's instruction is explicit — *pin the conifold Γ(1/5) value from the
literature before use* — and it has not been pinned from a citable source, so no R1 number is claimed.

### The node stopped polling, and why

The B2 run wrote a `result.json` with `"summary": ,` — an empty summary — which is invalid JSON. The node
recorded the job as **suspect** and has not polled since, so the B1/B3 probe and the B2 follow-up are
queued and unrun. That is a mesh bug worth its own note: **a job whose stdout cannot be summarised should
degrade to a plain "pass, no summary", not produce a result file that halts the loop.**
