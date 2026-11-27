# Methodology discoveries — the explainer and tracker

**Why this file exists.** A proof search produces two things: the *result* (if it lands) and the
*journey* — the methodologies that worked, the mechanisms that recurred, and the walls that taught
us something. The journey is usually the richer science. A final theorem is one sentence; the
techniques that produced it transfer to the next fifty problems. If the machine only records "the
answer", every intermediate discovery is thrown away with the dead ends — and a tool whose reasoning
we cannot read is a tool whose reasoning we cannot trust, reuse, or audit.

SEXTANT's answer to the mathematician's concern — *"I don't want to spend my career reconstructing
what the AI actually did"* — is exactly this file: **every reusable discovery along the way is
explained, tracked, and given named places it could go next.**

## The schema (how each entry is recorded)

Each discovery is one entry with six fields, all honest:

| field | meaning |
|---|---|
| **kind** | `methodology` (a transferable technique) · `mechanism` (a reusable structure) · `wall` (a refutation that became a lesson) |
| **what it is** | one plain-English line |
| **why it works** | the mechanism, for a mathematician who did not watch it happen |
| **where it came from** | the proof / commit / Lean theorem it emerged in |
| **potential uses** | named fields and problems where it transfers (cross-field) |
| **novel** | `known` (standard) · `new-formulation` (known idea, new shape) · `candidate-novel` (worth checking against the literature) |

---

## The catalog

### 1. The transfer-matrix spectral bridge — `methodology` · `known` (kernel-checked form is new)

**What it is.** "Clustering ⟺ spectral gap" — the mass gap `m` is the *second eigenvalue* of the
transfer operator, exactly, not an analogy.

**Why it works.** Reflection positivity makes the transfer operator self-adjoint and positive, so its
spectrum is real and its top eigenvalue is simple; exponential decay of the two-point function is
literally `λ₁ < λ₀`, i.e. `m = −log(λ₁/λ₀) > 0`. It turns "is there a gap" into "where is this
eigenvalue".

**Where it came from.** `MassGapDiamond.lean` — kernel-checked, no `sorry`.

**Potential uses.** Any lattice statistical-mechanics or Euclidean-QFT system where a mass / correlation
length must be *located in a spectrum*: spin systems, lattice gauge theory, the Anderson model, and any
discretised Euclidean field theory. It is the universal *container* for a spectral gap.

### 2. The block-spin contraction metric — `methodology` · `known`

**What it is.** The Kadanoff–Wilson decimation made quantitative: the block-spin map contracts a
suitable metric, and the contraction rate *is* the mass gap.

**Why it works.** Coarse-graining averages out short-distance modes; if the map contracts a distance
between measures by `e^{−m}`, the iteration converges and the fixed point has gap `m`. The contraction
rate and the gap are the same number, so one computation gives both.

**Where it came from.** `BlockSpin.lean`, `contraction_iterate_decay`, `strict_contraction_gives_gap`.

**Potential uses.** Any renormalisation-group argument that must show *convergence*, not just a fixed
point: dynamical systems, generative-model training (the "denoising" chain), and any multi-scale
coarse-graining where the contraction rate is a physically meaningful scale.

### 3. The animal→uniform-cluster bridge — `methodology` · `candidate-novel`

**What it is.** The number of connected clusters ("lattice animals") of size `n` is bounded by
`|V| · (2n) · (Δ+1)^(2(n−1))`, and — the bridge — this size-class summability is what makes the
single-cluster expansion close into a *uniform* cluster bound.

**Why it works.** A connected subset is counted by a rooted spanning tree (a tree has an Euler tour of
length `2(n−1)`, and each step has at most `Δ` choices), so the count is a *walks* count; summing the
size classes then gives the cluster-expansion convergence radius.

**Where it came from.** `AnimalsBound.lean` — `rooted_animals_count_bound_gen`, and the in-flight
`connected_clusters_count_bound` (Arrow A of the bridge).

**Potential uses.** Any combinatorial enumeration of connected subgraphs: percolation theory, the
random-cluster model, polymer expansion, and network/graph counting where connected-subgraph
summability is the hard step. The "rooted-tree tour" technique transfers verbatim.

### 4. The heat-kernel determinant scale — `methodology` · `candidate-novel` (derived, not fitted)

**What it is.** The weak-coupling exponent `c` in `m ≥ A·e^{−cβ}` is *derived* from the beta function
through the heat-kernel determinant `det P = e^{−Tr log P}`, with `a₂ ∝ b₀` and `Tr log P = c·β`.

**Why it works.** The running coupling's first coefficient `b₀` is fixed by the one-loop determinant of
the fluctuation operator; the exponent `c` is then a *consequence* of `b₀`, not a free parameter. A
fitted `c` is a free lunch; a derived `c` is a theorem.

**Where it came from.** `HeatKernel.lean` — kernel-checked.

**Potential uses.** Any place a critical exponent or a running-coupling scale must be *derived from the
symmetries* rather than measured: conformal field theory (operator scaling dimensions), statistical
mechanics (critical exponents), and lattice-QCD determinations of the QCD scale `Λ`.

### 5. Trace is the fundamental character — `mechanism` · `known`

**What it is.** On the diagonal torus `g = diag(e^{iθ}, e^{−iθ})`, `Tr g = 2 cos θ = sin(2θ)/sin θ` —
the SU(2) trace *is* the spin-1/2 character, not a coincidental equality.

**Why it works.** `Tr U = Σ_r χ_r` (Peter–Weyl); for SU(2) the trace observable lands on the
fundamental character, so any bound on the trace reduces to the per-character case.

**Where it came from.** `GaussianRigidity.lean` — `trace_is_fundamental_character`, kernel-checked.

**Potential uses.** Any non-Abelian observable decomposition: lattice gauge theory, random-matrix
theory, and representation-theoretic reductions where a group-average observable must be expressed
per-irrep.

### 6. Gauge-invariance rigidity → the covariant Laplacian — `mechanism` · `known` (the open rung)

**What it is.** The Gaussian covariance of a gauge theory is *forced* by gauge invariance to be the
covariant kinetic operator `K = −∇·D` (the transverse condition `p^μ K_{μν} = 0`).

**Why it works.** Gauge invariance is a *rigidity*: there is essentially one quadratic form compatible
with it, the covariant Laplacian. So "the covariance is Gaussian" collapses to "the covariance is
`−∇·D`", and the Gaussian domination of the trace becomes a statement about the Faddeev–Popov operator.

**Where it came from.** `GaussianRigidity.lean` — `covariantLaplacian` (stated, not yet proved for the
physical measure). This is the *single open rung* of the current reduction.

**Potential uses.** Any gauge theory where a fluctuation covariance must be identified from symmetry
alone: Yang–Mills, gravity (the DeWitt metric plays the same rigidity role), and any constrained
system where the symmetry fixes the quadratic form.

---

## The walls (rejections that became lessons — `kind: wall`)

A wall is not a mistake; it is a *measured* boundary. Each is recorded so it is not hit twice.

| wall | what it taught |
|---|---|
| **Compactness dies in the infinite-volume limit** | the transfer operator is positive + irreducible, but its spectrum gains a continuous part as `V → ∞`; the Jentzsch/Krein–Rutman bridge needs *compactness*, so the finite-volume gap does not transfer by that route. Use: know when a Perron–Frobenius-style argument *cannot* cross a limit. |
| **The horizon zero mode is a measure-zero gauge artifact** | the Gribov horizon's zero mode lives on a measure-zero set, and a mass gap is a *bulk* property; a boundary zero mode cannot force a bulk gap. Use: distinguish bulk vs boundary spectral obstructions in any constrained theory. |
| **Cluster expansion stops at log β** | the strong-coupling cluster expansion gives `m ≥ −log u(β)`, which dies at weak coupling — it is a strong-coupling tool only. Use: know the *ceiling* of the cluster expansion before trusting it in a regime. |
| **Single-plaquette stops at 1/β** | the one-plaquette Gaussian comparison gives `1/β`, not the exponential — the non-linearity of the trace defeats the naive comparison. Use: the Gaussian comparison must survive the *trace*, not the plaquette. |

---

## The two-step rule (so this file stays alive)

1. **A discovery is not a discovery until it has an entry here.** When the engine lands a lemma, it
   records *both* the theorem and the reusable technique it used — otherwise the technique dies with
   the proof.
2. **The uses are hypotheses, not claims.** "Could transfer to X" is a *proposal* until X's verifier
   fires; list it, but do not assert it as done.

The companion to this file is `docs/expansion-map.md` (the ranked *where-next* analysis) and
`docs/SEXTANT-KNOWLEDGE-ARCHITECTURE.md` (the node-schema these entries should eventually migrate
into as `kind: methodology-discovery` nodes).
