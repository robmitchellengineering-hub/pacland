# The exactness programme — what exact terms exist, and what each one can decide

Written 2026-10-29 in the planning room (`~/Documents/DeepSeek`), under D9 (the planning room owns
intent, the repo owns code), D10 (job → plan → decision), D14 (pacland is the method at maximum
difficulty) and D15 (physics is discipline-scale; its framing is the risk).

Rob's question: *"are there other exact geometric terms we can use that already exist, and what other
types of exactness are we able to use?"* This answers both, then says what to do with them, and — the
part that matters — what each one can **falsify**.

Read with `docs/is-the-landscape-chaotic.md` (the chaos question and its current build) and
`docs/unification-claim.md` (C1–C4). This plan does not re-ask those questions; it supplies the
instrument they are missing.

---

## 1. The eight kinds of exactness available to this programme

They are not interchangeable. Each is exact for a different reason, and each can therefore certify a
different thing.

| # | kind | what makes it exact | where we have it | what it can decide |
|---|---|---|---|---|
| **X1** | **topological / integer** | it counts something: indices, intersections, charges | `κ_ijk`, `c₂`, `χ`, the tadpole `N = FᵀΣH`, the GV invariants `n_d` | whether a computed continuous quantity is right — the integer must come out whole |
| **X2** | **closed form at a locus** | the analytic answer is known there | T⁶ (`oracle/exact_t6.py`); the LCS prepotential; orbifold/Gepner points; GLSM | an oracle with **zero systematic error**, so the verifier is provably exact |
| **X3** | **structural / recursive closure** | a finite generating datum determines everything else | N=2 special geometry (one prepotential ⇒ the whole metric); Picard–Fuchs (a finite ODE ⇒ every period); the holomorphic anomaly (a finite boundary datum ⇒ all genera) | whether a truncation is *convergent* rather than merely tolerable |
| **X4** | **invariance** | change the description, not the world; the claim must not move | `Sp(b₃,ℤ) × SL(2,ℤ)`; Law II; the monodromy representation | whether a claimed observable is physics or a coordinate artefact |
| **X5** | **definitional / identity** | true by construction | no-scale `g^{ij̄}K_iK_j̄ = 3` (measured **3.0000000000**); `V = 0` at a SUSY Minkowski point; anomaly cancellation | whether an implementation is wrong — an identity that fails is a bug, not a finding |
| **X6** | **arithmetic** | the object is defined arithmetically (Euler product, point counts, p-adic periods) | **not used yet** — the zeros arm's own kind, borrowed for the spectrum but never applied to the geometry | a check on periods that shares no code, no sampler and no series with the period computation |
| **X7** | **finite-window exhaustion** | below `N ≤ L` the flux lattice is finite, so enumeration is complete | implicit in the corpus (5,885 vacua); never stated as a theorem | an exact statement conditional only on a **declared** window — the honest form of every "fraction of vacua" claim |
| **X8** | **known-answer (null) control** | the reference's answer is exact by construction | GUE/Poisson controls; equally-spaced zeros; persistence in climate; the trend null in finance | whether a statistic means anything at the size it was computed at |

Two lessons the programme already paid for, both instances of X8: the zeros' 0.5307 scare (a reference
that was the wrong **ensemble**, not the wrong sample size) and the `|W|` lattice (a reference object
with no fluctuations to report). A statistic without an exact control at the same size is a measurement
of the estimator.

**The important distinction:** X4, X5 and X8 are available *everywhere*, including the interior of
moduli space, because they need no closed form. X1, X2, X3 and X6 are only available topologically, at
special loci, or as structure. **The 5,885 vacua live in the interior, so the interior's exactness has
to come from X4/X5/X8 or from X1's discrete data — never from a closed form we might one day find.**

---

## 2. What the toolchain already exposes (verified, not assumed)

| capability | where | evidence |
|---|---|---|
| Hodge numbers, triple intersections, `c₂`, Kähler/Mori cones, **GV invariants** | CYTools 1.4.12 | `docs/tooling.md`, verified live on `studio-linux` 2026-10-18 |
| LCS tree, prepotential, instanton sums, F-terms, Hessian | JAXVacua | `oracle/adapters.py:85` — `jvc.lcs_tree.from_cytools(cy, maximum_degree=1)` |
| **the truncation knob is a named parameter** | `maximum_degree` | same call — this is what "truncation" actually means in our stack |
| instanton sum is tiny in our models | 2 GV charges, correction ~0.004 | `src/pacland/limits.py:82` |
| explicit symbolic arithmetic | sympy 1.14.0 in `/home/rob/cytools-venv` | 2026-10-22 mesh job |
| `V`, the `DW=0` solver, Hessian | `oracle/potential_t6.py` | #198–#200, validated 4/4 |

**Routing, read live (not remembered):** `dispatch.py --list` on 2026-10-29 shows `mac`, `pacland-rog`,
`studio-linux2`, `win`, `win-2`. **`studio-linux` — the only node verified to have cytools + jaxvacua —
is not registered.** `studio-linux2` advertises `node:js` only. The VMs on `win-2` do not auto-start.

---

## 3. What the work is, ordered by (cost × what it can falsify)

### E1 — The truncation ladder: is `cond(M)` geometry or series truncation?

**Exact term used:** X3 (the instanton series is closed-form with integer coefficients, so its
truncation error is *bounded*, not estimated).

With `Im T ≥ 2` from the sampler bounds, the neglected degree-`d` instanton is suppressed by
`e^{−2π d·Im T}`: degree 1 ≤ **3.5×10⁻⁶**, degree 2 ≤ **1.2×10⁻¹¹**. The observed h12=25 failure is
`|dV|` of order **10²–10³** against 0.3–4.1 at h12=2 — eight orders above the largest neglected term.

**Hypothesis:** the near-null direction of `Im N` is **real geometry**, not truncation.
**Falsifier:** run `maximum_degree = 1, 2, 3` and see whether `cond(M)` moves. If it moves by more than
10%, the conditioning is a series artefact and the wall *is* a truncation wall.
**Can this fail?** Yes — that is the point. This is the first version of the wall question that has an
answer that is not "more sampling needed".
**Where:** any node with cytools + jaxvacua (see routing note).
**If it holds:** the h12 ≥ 5 wall is the integer-lattice problem (`docs/is-the-landscape-chaotic.md`
found the same thing from the other end this week: a generic integer flux is F-flat **nowhere**),
1/`λ_min` being the magnification. Then no solver, degree or ensemble size fixes it, and effort goes to
non-SUSY `DV = 0` vacua — which is where the chaos arm is already heading.

### E2 — GV integrality: an independent check on the period pipeline

**Exact term used:** X1. Extract `n_d` from the computed prepotential at several points. GV invariants
are integers by definition (BPS counts). Non-integral output means the periods are wrong *at that
point* — a detector that needs no oracle.
**Falsifier:** a non-integer `n_d`, or values that change with the point when they must not.
**Cost:** shares E1's runs.

### E3 — Monodromy: the covariance table as computation, not measurement

**Exact term used:** X4 + X3. The Picard–Fuchs/GKZ system gives integer monodromy matrices
`M ∈ Sp(2h+2,ℤ)` with the machine-checkable identity `MᵀΣM = Σ`. Every observable's transformation law
follows by differentiating the period action — so **G1** (`docs/SOLVING-STRING-THEORY.md` §4) becomes a
closed-form derivation instead of a fit with a log residual, and the open half of Law II (the phase) is
exactly what the monodromy fixes.
**Falsifier:** `MᵀΣM ≠ Σ` (implementation error), or a law that does not close under a full monodromy
generator when it closed under S and T.
**First step is a capability probe** — does `cytools` 1.4.12 expose periods/PF operators? If not, this
is a build (Frobenius on the GKZ system), and the build is the deliverable.

### E4 — Finite-window exhaustion: the first *exact* measure statement

**Exact term used:** X7. Below a declared tadpole bound `N ≤ L` the landscape is finite, so
"fraction of vacua with property P" is exact and reproducible — and the fraction's sensitivity to the
window is itself measurable.
**Why now:** `docs/quantum-arm-agenda.md` Q3 and the chaos doc both end at "this may be a measure
question". X7 is the only kind of exactness that lets us *state* a measure claim without an oracle.
**Falsifier:** the fraction must move with `L`; if it is flat in `L` for two different measures, the
"10⁵⁰⁰ argument is about measures" claim loses its demonstration.
**Where:** Mac, on the corpus already on disk — no node needed.

### E5 — Two exact controls for the mass spectrum (plugs into the chaos arm now)

**Exact terms used:** X4 and X5, and both are provable today:

1. **`d`-scaling cannot contaminate the level statistics.** The flux-scaling lemma (`W → dW`,
   `DW → d·DW`) makes `V → d²V` and therefore `M² → d²M²` at a shared critical point. The *unfolded*
   spacing statistic is invariant under an overall scale, so ensembles mixing different `d` are
   provably clean. Without this, every chaos number would carry an "is it just the lattice label?"
   asterisk; with it, that question is closed before the run.
2. **No-scale is an exact zero-mode detector.** At a SUSY Minkowski point `V = 0` exactly and the
   Kähler sector is flat, so the Hessian must show exact zeros. The chaos doc names zero-modes as the
   trap that would make the spacing statistic a statement about degeneracies — this turns the trap into
   a pass/fail check rather than a judgement call.

**Falsifier:** a spectrum whose unfolded statistic moves under `d → 2d`, or a claimed SUSY point whose
Hessian has no exact zero mode. Either is a bug in the spectrum, not a finding.

### E6 — A second exact rung, and the one item that can falsify rather than certify

**Exact term used:** X2. Two candidates, pick by cost:

- **K3 × T²** — complex-structure moduli space is the symmetric space `O(2,19)/(O(2)×O(19))`, so the
  period domain and the special-Kähler metric are closed form. Gives a second exact oracle with
  `h¹¹ = 20`: real gauge structure, unlike T⁶.
- **toroidal orbifolds / Gepner points** — the *worldsheet CFT* is exactly solvable, so **every `α′`
  correction is exact**, not just the leading term. And they carry **discrete torsion**, which is:

> the sharpest test on the board. Discrete torsion is exact, discrete, topologically classified, cheap
> to enumerate — and it **changes the spectrum**. C3 says distinct orbits ⇒ distinct physics; discrete
> torsion is a label the orbit data does not contain, so two configurations with the same `(N, d)` and
> the same moduli can differ physically. That is C3's **injectivity** failing from a direction the
> corpus cannot even represent (it samples smooth CYs and records no torsion). It is the same *class*
> of object as `d`, except `d` is provably empty and discrete torsion is provably not.

**Falsifier:** a pair of orbifold configurations, identical orbit data, different spectra. If that
exists, "the exact content is constraints + labels + orbit coordinates" needs a fourth bucket, or
"label" needs splitting into *observable* and *redundant*.

### Deferred (named, not planned)

- **X6 arithmetic** — the L-function of the family / p-adic periods: the only exactness that shares
  nothing with the period computation, so the only true cross-source check on it. Expensive; revisit
  when E1's answer is known.
- **GLSM exact Kähler potential** — exact on the Kähler side only, where the flux vacua are not.

---

## 4. Order, and why

```
E1  truncation ladder      decides the wall; cheapest decisive test; needs the node
E2  GV integrality         rides on E1's runs
E5  the two exact controls unblocks the chaos arm immediately, provable on the Mac
E4  finite-window measure  first exact measure statement, no new machinery
E3  monodromy table        closes G1; starts with a capability probe
E6  second rung            the only scope test of C1/C3 — and the only falsifier here
```

**Gates:** E1's verdict decides whether E4/E6 are aimed at "a landscape" or at "a truncation". Nothing
downstream should be read as a landscape statement until E1 reports.

## 5. What none of this does

- It does not raise `m` (still **9**: topology 4 + flux 1 + SM 4). Exactness changes the *oracle class*
  of what is already claimed; it does not add a certified parameter.
- It does not produce a closed form for the interior of moduli space, because none is known and
  searching for one is not a plan.
- It does not touch the 19 Standard-Model parameters. C4 remains a conjectured bet.
- It does not rescue C1 or C3. E6 is here partly to see whether they survive.

## 6. The rule this plan works under

Every item names the exact term it uses, the falsifier, and — before it runs — *how the falsifier could
come out*. An item whose falsifier cannot fail is a demonstration, not a test, and belongs in the docs
rather than in this plan.
