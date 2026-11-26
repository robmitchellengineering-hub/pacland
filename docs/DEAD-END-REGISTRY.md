# Dead-end registry — every failed approach, and the exact point it breaks

The purpose of this registry is that the system never wastes a cycle rediscovering a wall. Each
entry names the approach, the precise point of failure, and where (if anywhere) the failure is
recorded in the tower or the falsifier layer. This is the "negative knowledge" half of the reduction:
it is as much part of the locked-in state as the proved chain.

## The mass-gap programme

### 1. Naive weak-coupling cluster expansion

- **Approach**: expand the Wilson action `e^{−β(2−Re Tr U)}` around the identity and resum connected
  clusters at *fixed* coupling.
- **Breakpoint**: the gauge orbit is **non-compact in the axial/full gauge**, so the small-field
  activity `ρ = 1 − e^{−β(2−Re Tr U)}` does **not** stay `< 1` uniformly — the expansion radius
  collapses where `Re Tr U` is far from 2. Weak coupling is not a small parameter over the whole group.
- **Recorded**: `cluster_activity_abs_lt_one` proves the activity bound *only* on the small-field
  region; the non-compactness is the reason the full-orbit version is not a theorem.

### 2. Single-plaquette `1/β` (compactness is the wall)

- **Approach**: bound the plaquette trace by its `1/β` saddle, treating each plaquette independently.
- **Breakpoint**: the plaquette is **compact** (`Re Tr U ∈ [−2, 2]`), so the `1/β` expansion of an
  integral over a compact group does not converge uniformly in the number of plaquettes — the
  saddle-point series is asymptotic, not convergent, and the remainder grows with the lattice size.
- **Recorded**: the `e^{−(12π²/11)β}` exponent is the *one-loop* beta function; the single-plaquette
  `1/β` correction does not resum to it (the `12π²/11` is a running-coupling, not a saddle, effect).

### 3. The horizon zero mode as a massless excitation

- **Approach**: read the Gribov-horizon / constant-mode zero eigenvalue as a physical massless mode
  that kills the gap.
- **Breakpoint**: the zero mode is a **measure-zero gauge artifact** — a flat direction of the
  Faddeev–Popov determinant, not a state of the physical Hilbert space.
- **Recorded**: `faddeevPopovConstantMode` (the flat direction is explicit); the physical transfer
  matrix is projected onto the gauge-invariant sector.

### 4. Compactness death in the infinite-volume / continuum limit

- **Approach**: carry a compact transfer operator (finite matrix) into the `N → ∞`, `a → 0` limit.
- **Breakpoint**: the transfer operator is compact only at finite volume; **compactness dies in the
  infinite-volume limit**, so the spectral-gap ⟺ clustering bridge (`clustering_iff_gap`) holds
  *per volume* but does **not** by itself survive the limit.
- **Recorded**: `volume_uniform_covariance_bound` + `wightman_limit_stable` are stated as the
  transports that *would* carry it — their hypothesis is the volume-uniformity (H). This is the exact
  reason the reduction is to a **volume-uniform** statement, not a per-volume one.

### 5. The free-walk animals bound `Δ^(2(n−1))`

- **Approach**: bound the connected-cluster count by the free-walk count (an Euler/DFS tour of length
  `2(n−1)`, each step ≤ Δ choices).
- **Breakpoint**: the Euler tour is **not a free walk** — each edge is traversed exactly twice, so the
  walk overcounts the rooted-tree count by a full factor of `(Δ+1)^(n−1)`. The sharp exponent is
  `(n−1)`, not `2(n−1)`.
- **Recorded**: `rooted_animals_count_bound` (the sharp rooted-tree form) and
  `connected_clusters_count_bound` — the wall is *resolved*, not open.

### 6. The `λ = e^{−E}` tautology (the "reduce-to-one-step" trap)

- **Approach**: state the mass gap as `λ₁ = e^{−E}` and declare the gap proved.
- **Breakpoint**: `λ₁ = e^{−E}` *defines* E from λ₁ — it is a tautology that carries no analytic
  content; it does not bound the spectral gap below, it just renames it.
- **Recorded**: `fe215aa2` replaces the tautology with the **spectral identification**
  `λ₁ = I₁(2β)/I₀(2β)` (the Bessel ratio), which is the concrete, falsifiable open step.

### 7. The spectral identification `λ₁ = I₁(2β)/I₀(2β)` (the current open rung)

- **Approach**: identify the transfer matrix's top eigenvalue with the Bessel ratio; the exponential
  bound `poly_beats_exp` + the volume-uniformity are then **conditional on this identification**.
- **Status**: this is the **single open step** as of the "one step from done" state (`fe215aa2`). It
  is concrete and falsifiable (a single β where the Bessel ratio mis-predicts the eigenvalue refutes
  it), but not yet a theorem.

## Cross-field (the discovery layer)

### 8. Keyword-only cross-field matching

- **Approach**: match reusable mechanisms to open problems by text overlap.
- **Breakpoint**: the word "bound" made everything match everything — a type-less matcher re-finds
  what is already written, never a new mapping.
- **Recorded**: `pacland/cross_field/propose.py` matches by **type** (structured `provides`/`needs`).

### 9. "Discovery" = LLM re-combination

- **Approach**: treat the LLM's generate step as the discoverer.
- **Breakpoint**: the generate step does not beat a neutral baseline; the LLM re-combines known
  mechanisms (reduction, verification, refutation) and does not make the generative leap a new result
  needs.
- **Recorded**: SEXTANT's real capability is verification-driven search, not generative discovery;
  the falsifiers + Lean are the engine, the LLM is a cheap proposer.
