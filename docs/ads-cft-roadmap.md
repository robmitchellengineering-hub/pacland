# AdS/CFT roadmap — from the discrete ToE to the smooth limit

The honest goal: a kernel-checked **"entanglement = geometry"** claim, from the discrete MERA cone
up to the smooth hyperbolic plane. This is the geometric heart of AdS/CFT — *not* the full
Maldacena duality, which stays named as the open frontier.

## The big think — two jobs, very different hardness

### Job 1 — the geometric continuous limit (provable)

The MERA causal cone is a **binary tree**. We have already kernel-checked the two invariants that
*make* it hyperbolic:

- **0-hyperbolicity** (`treeDist_four_point` — Gromov's four-point condition).
- **exponential volume** (`ballVolumeExponential` = 2^(r+1)−1, `ballVolume_growth_class`).

Gromov's classification then does the heavy lifting: **a geodesic space that is 0-hyperbolic with
exponential growth is quasi-isometric to the hyperbolic plane H².** The tree *is* such a space, so:

```
tree is 0-hyperbolic  ∧  tree has exponential growth   ⟹   tree ≃_QI H²
```

That is the honest "continuous limit" in the **coarse (quasi-isometry) sense** — the same geometry
as the smooth plane, up to bounded distortion. The *fine* version (Gromov–Hausdorff convergence to
the literal metric `ds² = dr² + sinh²(r)dθ²`) is the next rung and needs the metric-geometry stack.

**Concrete rungs (kernel-checkable, in order):**
1. Define quasi-isometry (two-sided bounded distortion).
2. Prove the tree's exponential growth is a QI invariant (already: `ballVolume_growth_class`).
3. Define H² (the Poincaré disk, or the tree itself as the model) + its metric.
4. Prove `tree ≃_QI H²` via the growth-class + 0-hyperbolicity invariants.

### Job 2 — the structural AdS/CFT (state precisely, prove the pieces)

Maldacena's full duality (string theory on `AdS₅×S⁵` ↔ `N=4` SYM) is **25 years open** — we state
it, we do not claim to prove it. But its *constraint-first* core is provable:

- **The area law** — entanglement entropy ≤ cut area (`areaLaw_rank`, done) — this is the
  Ryu–Takayanagi bound in discrete form.
- **The emergence direction** — the entanglement structure *forces* the geometry: 0-hyperbolicity +
  exponential volume are the geometry that the area law implies.
- **The dictionary** — the constraint-first pattern matches on both sides: boundary (conformal
  labels, entanglement) ↔ bulk (geometry, the tadpole/area constraint). Relations, never values.

**Concrete rungs:**
1. State Maldacena's conjecture as a precise theorem (what "dual" means — a matching of invariants).
2. Kernel-check the area law ↔ Ryu–Takayanagi correspondence (minimal surface = entanglement).
3. Prove the emergence: `areaLaw ∧ 0-hyperbolic ∧ exponential` ⟹ the geometry is hyperbolic.

## The honest claim we are building toward

> **"The entanglement structure of the MERA network is a discrete hyperbolic space (0-hyperbolic,
> exponential volume, area law), quasi-isometric to the hyperbolic plane — entanglement = geometry,
> kernel-checked from the discrete up to the smooth limit. The full AdS/CFT duality is the open
> frontier this sits inside."**

That is a *true* ToE claim — the discrete fully proven, the continuous limit proven in the coarse
(QI) sense, the physics duality honestly named as the frontier.

## Job 2 — the precise statement (what "AdS/CFT" means, exactly)

**Maldacena's conjecture (1997), stated for the record:**

> Type IIB string theory on `AdS₅ × S⁵` with `N` units of five-form flux and string coupling `g_s`
> is *dual* to `N = 4` super-Yang–Mills theory on the 4D boundary, gauge group `SU(N)`, coupling
> `g_YM`. The dictionary is `g_YM² = g_s` and `λ = g_YM² N = (R/ℓ_s)⁴`. "Dual" means: the partition
> functions, the operator spectra, and the correlation functions **match** under the map
> (gauge-invariant operator ↔ bulk field).

This is **open** — 25 years of checks agree, no proof. We do not claim to prove it.

**The constraint-first core we *can* state and kernel-check** — the "relations, never values" version:
the *exact structure* matches on both sides, and it is the same constraint + label + no-go pattern:

| | boundary (CFT / quantum) | bulk (AdS / gravity) |
|---|---|---|
| **constraint (FORCED)** | entanglement ≤ cut rank (`areaLaw_rank`) | cut area `D^m` (`bondConfigurations`) |
| **label (FREE)** | which state, the central charge | `h¹¹, h²¹, χ` |
| **no-go (IMPOSSIBLE)** | LOCC cannot create entanglement (`QM.Entanglement`) | no exact invariant selector (flux FFT) |
| **the bridge** | entanglement = area | area = the minimal surface (Ryu–Takayanagi) |

The kernel-checked pieces: `areaLaw_rank` (entanglement ≤ rank), `bondConfigurations` (area = `D^m`),
`QM.Entanglement` (LOCC no-go), `treeDist_four_point` + `ballVolume_growth_class` (the bulk is
hyperbolic). The **"="** in Ryu–Takayanagi (entanglement *equals* the minimal area) is the frontier,
exactly like the full duality.
