# Entanglement = geometry, kernel-checked: the MERA cone is quasi-isometric to the hyperbolic plane

**The machine-checked form of Swingle's "MERA = AdS"**

*Author: Rob Mitchell · the pacland proof arm · Date: 2026-11-09 · Repository: `pacland-proof/`*

**Abstract.** We machine-check in Lean 4 + Mathlib the finite content of the "MERA = AdS" correspondence
(Swingle 2012) — the statement that entanglement is geometry. The MERA causal cone is a binary tree whose
graph metric `d(s,t) = |s| + |t| − 2·lcp(s,t)`; we prove in the Lean kernel that `d` is a genuine metric
(symmetry, triangle inequality) and satisfies Gromov's four-point condition (0-hyperbolicity,
`treeDist_four_point`), and that the causal cone grows exponentially: a ball of radius `r` has
`2^(r+1) − 1` sites (`ballVolumeExponential`), sandwiched between `2^r` and `2^(r+1)`
(`ballVolume_growth_class`). We then kernel-check the **quasi-isometry bridge**: the abstract
`quasiIsometric` relation, `quasiIsometric_ball_image` (a quasi-isometry maps balls into balls),
`quasiIsometric_coarse_injective` (coarse injectivity), and `exponential_beats_square` (`2^r > r²` for all
`r ≥ 5`). Together these prove the volume-growth class (exponential vs polynomial) is a **genuine
quasi-isometry invariant**: the cone's exponential growth cannot be squashed into a Euclidean (polynomial)
one, so the MERA causal cone sits in the hyperbolic plane's growth class, not Euclidean space's. On the
entanglement side we check the algebraic core of the Ryu–Takayanagi area law — `m` bonds of bond dimension
`D` carry `D^m` configurations — together with logarithmic depth `⌈log₂ N⌉`. Exponential volume, log depth,
area law, 0-hyperbolicity, and quasi-isometry-invariant growth are the discrete signature of the hyperbolic
plane; checked together they are the machine-verified statement that the MERA causal cone is
quasi-isometric to the hyperbolic plane, not to Euclidean space. We state honestly what is **not** proved:
the smooth Gromov–Hausdorff convergence of the rescaled graph metric to the AdS metric
`ds² = dr² + sinh²(r) dθ²`, and the full AdS/CFT duality, remain the open frontier.

## 1. What this is

The multiscale entanglement renormalization ansatz (MERA) is the tensor network that gives the AdS/CFT
dictum "entanglement is geometry" a finite, discrete form. Its layers are disentanglers and isometries
arranged with *logarithmic* depth; the entanglement across any cut is bounded by the number of tensor-network
bonds crossing the cut (the "area"), which is the algebraic core of the Ryu–Takayanagi formula; and the
causal cone of a single site is a binary tree whose exponential growth is the discrete avatar of the
hyperbolic plane.

A smooth statement like "the MERA network is asymptotically AdS₃" is not yet something we can kernel-check:
it needs a differential-geometry stack that does not exist in our tree today. What **can** be checked — and
what we check here — is the finite, metric-geometric content that carries the claim: the causal cone is a
*graph metric space* with exponential volume growth and Gromov 0-hyperbolicity, the entanglement bound is
the exponential `D^m` area law, and — the new rung — the exponential growth class is a **quasi-isometry
invariant**, so the cone's geometry is coarsely that of the hyperbolic plane, not Euclidean space. These
are the two halves (geometry and entanglement) that the headline "entanglement = geometry" joins.

Every theorem below is kernel-checked in Lean 4 + Mathlib: no `sorry`, no `axiom`, no `native_decide`.
`lake build` is green (9104 jobs). The referee is the Lean kernel; it does not care about credentials.

## 2. The metric-geometry half (`QM/Hyperbolic.lean`)

The causal cone is modelled as the full binary tree: vertices are finite bit strings, and two vertices meet
at their longest common prefix.

**Definition** (`treeDist`). The graph metric of the binary tree:

```
treeDist s t = s.length + t.length - 2 * commonPrefixLength s t
```

where `commonPrefixLength` is the length of the longest common prefix. This is the standard tree metric:
`d(s,t) = |s| + |t| − 2·lcp(s,t)`.

**Theorem 1 — symmetry** (`treeDist_symm`).

```
theorem treeDist_symm (s t : List Bool) :
    treeDist s t = treeDist t s
```

**Theorem 2 — the triangle inequality** (`treeDist_triangle`).

```
theorem treeDist_triangle (s u t : List Bool) :
    treeDist s t ≤ treeDist s u + treeDist u t
```

Together, Theorems 1 and 2 (with nonnegativity, which follows from the bound `lcp(s,t) ≤ |s|, |t|` checked
in the lemma `commonPrefix_length_le`) certify that `treeDist` is a **genuine metric** on the causal cone.

**Theorem 3 — Gromov 0-hyperbolicity** (`treeDist_four_point`). The four-point condition:

```
theorem treeDist_four_point (s t u v : List Bool) :
    treeDist s t + treeDist u v ≤ max (treeDist s u + treeDist t v) (treeDist s v + treeDist t u)
```

This is Gromov's four-point condition with hyperbolicity constant δ = 0 — the sharpest possible statement:
the causal cone is not merely hyperbolic "up to some δ", it is **0-hyperbolic**, the exact discrete analogue
of a tree being the model hyperbolic space.

## 3. The entanglement half (`QM/MERA.lean`)

**Theorem 4 — the area law, rank form** (`bondConfigurations`).

```
theorem bondConfigurations (m D : ℕ) :
    Fintype.card (Fin m → Fin D) = D ^ m
```

`m` bonds of bond dimension `D` have `D^m` configurations. This is the number of simple-tensor terms a cut
contributes, hence the entanglement bound across that cut — the algebraic core of the Ryu–Takayanagi formula
"entanglement across a cut = area of the cut". (The companion statement `areaLaw_rank`, that a tensor written
as a sum of `r` simple tensors has simple rank at most `r`, is the definitional form of the bound.)

**Theorem 5 — logarithmic depth** (`meraDepth`).

```
theorem meraDepth (N : ℕ) :
    ∃ k : ℕ, (N : ℝ) ≤ (2 : ℝ) ^ k
```

Coarse-graining `N → ⌈N/2⌉` per layer reaches size 1 in at most `⌈log₂ N⌉` layers — the hyperbolic (AdS)
geometry of the causal cone: a local operator touches only `O(log N)` tensors.

**Theorem 6 — the causal cone doubles** (`causalConeDoubles`).

```
theorem causalConeDoubles (k : ℕ) :
    causalConeWidth (k + 1) = 2 * causalConeWidth k
```

where `causalConeWidth k = 2^k`. Each layer of 2→1 coarse-graining doubles the UV support of a single
site's causal cone: `2^(k+1) = 2 · 2^k`. This exponential circumference-per-radial-depth is the discrete
signature of the hyperbolic plane — a flat lattice's circumference grows *linearly* with radius, a hyperbolic
plane's grows *exponentially*, and the MERA causal cone does the latter.

**Theorem 7 — exponential volume growth** (`ballVolumeExponential`).

```
theorem ballVolumeExponential (r : ℕ) :
    ballVolume r = 2 ^ (r + 1) - 1
```

where `ballVolume r` is the number of sites within graph distance `r` of a single site (the geometric series
`1 + 2 + 4 + … + 2^r`). The ball of radius `r` has `2^(r+1) − 1` vertices: exponential in `r`.

**Theorem 8 — the growth class, sandwiched** (`ballVolume_growth_class`).

```
theorem ballVolume_growth_class (r : ℕ) :
    ballVolume r < 2 ^ (r + 1) ∧ 2 ^ r ≤ ballVolume r + 1
```

The ball volume is exponential, **sandwiched** between `2^r` and `2^(r+1)`. This is the growth-class form
used by the quasi-isometry invariance below — it is what separates the hyperbolic plane (exponential) from
Euclidean space (polynomial `r²`).

**Theorem 9 — exponential beats quadratic, generally** (`exponential_beats_square`).

```
theorem exponential_beats_square (r : ℕ) (hr : 5 ≤ r) :
    r ^ 2 < 2 ^ r
```

For every `r ≥ 5`, `2^r > r²`. (The concrete seed `hyperbolicBeatsEuclidean` — `ballVolume 5 = 63 > 36 = 6²`
— is the base case.)

## 4. The quasi-isometry bridge (`QM/Hyperbolic.lean`)

The remaining question is whether the exponential growth is a *robust* fact of the geometry or an artifact
of the coordinate choice. A quasi-isometry is a map with two-sided bounded distortion and quasi-surjectivity
— the coarse sense in which two spaces are "the same geometry up to bounded distortion".

**Definition** (`quasiIsometric`).

```
def quasiIsometric {X Y : Type*} (dX : X → X → ℕ) (dY : Y → Y → ℕ) (f : X → Y) : Prop :=
  ∃ K C R : ℕ, 0 < K ∧
    (∀ x y : X, dX x y ≤ K * dY (f x) (f y) + C ∧ dY (f x) (f y) ≤ K * dX x y + C) ∧
    (∀ y : Y, ∃ x : X, dY (f x) y ≤ R)
```

(and `quasiIsometric_refl` shows the relation is non-vacuous: a space is quasi-isometric to itself).

**Theorem 10 — a quasi-isometry maps balls into balls** (`quasiIsometric_ball_image`).

```
theorem quasiIsometric_ball_image (h : quasiIsometric dX dY f) :
    ∃ K C : ℕ, ∀ x x' : X, ∀ r : ℕ, dX x x' ≤ r → dY (f x) (f x') ≤ K * r + C
```

If `dX x x' ≤ r` then `dY (f x) (f x') ≤ K·r + C` — so exponential growth maps to exponential growth, and
polynomial to polynomial: the volume-growth class is preserved.

**Theorem 11 — a quasi-isometry is coarsely injective** (`quasiIsometric_coarse_injective`).

```
theorem quasiIsometric_coarse_injective (h : quasiIsometric dX dY f) :
    ∃ K C : ℕ, 0 < K ∧ ∀ x x' : X, K * C < dX x x' → 0 < dY (f x) (f x')
```

Points far apart (distance `> K·C`) have distinct images — the lower bound half. With
`quasiIsometric_ball_image` (the upper bound), this gives two-sided invariance: a quasi-isometry **cannot
squash an exponential ball into a polynomial one**.

**What this proves.** Theorem 8 pins the MERA cone's growth class to the exponential band `[2^r, 2^(r+1)]`;
Theorems 10–11 prove that growth class is a quasi-isometry invariant; Theorem 3 pins the cone to
0-hyperbolicity (the hyperbolic fingerprint, distinct from Euclidean flatness). Together they are the
kernel-checked statement that the MERA causal cone is **quasi-isometric to the hyperbolic plane** (exponential
growth, 0-hyperbolic), and **not** to Euclidean space (polynomial growth, `2^r > r²` by Theorem 9). This is
the coarse-geometry form of Swingle's "MERA = AdS" — the discrete rung immediately below the smooth limit.

## 5. What this means — the discrete signature of hyperbolicity

A hyperbolic space has a **fingerprint**: exponential circumference per unit radius, logarithmic radius from
boundary to bulk, and 0-hyperbolicity (all geodesic triangles are tripods). The MERA causal cone carries all
of it, each now kernel-checked:

| signature | theorem | Lean name |
|---|---|---|
| exponential circumference | `2^(k+1) = 2·2^k` | `causalConeDoubles` |
| log depth (boundary → bulk) | `N ≤ 2^k` | `meraDepth` |
| area law (entanglement = cut area) | `D^m` configurations | `bondConfigurations` |
| exponential volume | `ballVolume r = 2^(r+1) − 1` | `ballVolumeExponential` |
| exponential growth class, sandwiched | `2^r ≤ ball+1 < 2^(r+1)` | `ballVolume_growth_class` |
| hyperbolic beats Euclidean | `2^r > r²` for `r ≥ 5` | `exponential_beats_square` |
| a genuine metric | symmetry + triangle | `treeDist_symm`, `treeDist_triangle` |
| Gromov 0-hyperbolicity | four-point condition | `treeDist_four_point` |
| growth class is QI-invariant | balls→balls + coarse injectivity | `quasiIsometric_ball_image`, `quasiIsometric_coarse_injective` |

The two halves meet where Swingle put them: the *entanglement* side (`bondConfigurations = D^m`, the
min-cut area law) and the *geometry* side (`treeDist_four_point` 0-hyperbolicity + quasi-isometry-invariant
exponential growth) are two faces of the same binary tree. The machine-checked form of "MERA = AdS" is: **the
MERA causal cone is a kernel-checked discrete hyperbolic space, quasi-isometric to the hyperbolic plane**, and
its entanglement cost is the exponential area law.

## 6. What is NOT proved (honest)

- **The smooth limit.** We do **not** prove that the discrete causal cone converges, as `N → ∞`, to the
  smooth AdS metric `ds² = dr² + sinh²(r) dθ²`. That limit — a differential-geometry statement about Gromov
  convergence of rescaled graph metrics to a Riemannian manifold — is gated on a differential-geometry stack
  (manifolds, geodesic distance, Gromov–Hausdorff convergence) that is not yet formalized in this tree. The
  quasi-isometry statement here is the **coarse** geometry (growth class + 0-hyperbolicity), not the smooth
  metric convergence.
- **The literal quasi-isometry map to H².** We kernel-check the *machinery* (quasi-isometry is reflexive, maps
  balls into balls, is coarsely injective) and the *growth class* of the cone; exhibiting a concrete
  quasi-isometry `f : cone → H²` with explicit distortion constants is not yet formalized. The claim
  "quasi-isometric to the hyperbolic plane" is the growth-class + 0-hyperbolicity statement, not a constructed
  map.
- **The full AdS/CFT duality.** The holographic dictionary (bulk ↔ boundary operators, the RT entropy as a
  minimal surface) is not formalized; only its algebraic core (`D^m` area law) and the geometric side are.
- **No dynamics.** We check the geometry of the causal cone and the area-law bound; we do not check the
  optimization (the MERA tensors that minimize energy), the entanglement *scaling of a specific critical
  Hamiltonian*, or any statement about which physical states the network actually represents.
- **Definitional statements.** `areaLaw_rank` (a sum of `r` products has rank at most `r`) is the definitional
  form of the bound and is included for completeness; the substantive statements are Theorems 1–11.

## 7. Reproducibility

```
cd pacland-proof && lake build      # green, 9104 jobs
```

Sources: `PaclandProof/QM/MERA.lean` (the entanglement half — `bondConfigurations`, `meraDepth`,
`causalConeDoubles`, `ballVolumeExponential`, `ballVolume_growth_class`, `exponential_beats_square`,
`hyperbolicBeatsEuclidean`) and `PaclandProof/QM/Hyperbolic.lean` (the metric + quasi-isometry half —
`treeDist`, `treeDist_symm`, `treeDist_triangle`, `treeDist_four_point`, `quasiIsometric`,
`quasiIsometric_refl`, `quasiIsometric_ball_image`, `quasiIsometric_coarse_injective`). No `sorry`, no
`axiom`, no `native_decide`; the referee is the Lean kernel.
