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
2. **No-scale is an exact zero-mode detector.** At a SUSY Minkowski point `V = 0` exactly and the
   Kähler sector is flat, so the Hessian must show exact zeros. The chaos doc names zero-modes as the
   trap that would turn the spacing statistic into a statement about degeneracies; this makes the trap
   a pass/fail check.

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
A1  gauge invariance      an hour, and it may already be a bug in V
A3  the control gate      stops the fourth repeat; needed before any chaos number counts
A2  the identity battery  first check of the corpus against its own geometry
B4  the two controls      unblocks the chaos arm; provable, no build
B2  truncation ladder     decides the wall; needs studio-linux up
B1  GV integrality        rides on B2's runs
A4  coverage / recall     converts every "fraction" into a checked claim
D1  finite-window measure first exact measure statement
B3  monodromy table       closes G1; starts with a capability probe
R1  quintic rung          the only real-CY known-answer we can reach cheaply
R2  second rung           the only scope test of the claim's C1/C3 — and the only falsifier here
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
