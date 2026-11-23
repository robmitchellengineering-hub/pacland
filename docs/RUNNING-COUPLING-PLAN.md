# Plan — the running-coupling step (deriving `c` from the beta function)

Status: 2026-11-22. The single open rung, made into a concrete plan. Goal: prove
`m(β) ≥ A·e^{−cβ}` with `c` **derived from the beta function** (not fitted), so the mass gap follows
with a genuine exponent.

## The chain (what the step must do)

```
beta function  b₀ = 11N/48π² > 0   ── (asymptotic freedom, the coupling runs)
        │
        ▼
dimensional transmutation  Λ = μ·e^{−1/(2b₀g²)}   ── (the scale is generated)
        │
        ▼
mass gap = the scale  m(β) ≥ A·e^{−cβ}   ── (the spectral gap carries the running scale)
```

## Step status

1. **The beta function is positive** — `b₀ > 0`, asymptotic freedom. **DONE** (`AsymptoticFreedomSign.lean`:
   `beta_function_positive`, `beta_positive_from_continuum_limit`).
2. **The dimensional transmutation** — the log-form `1 = b₀g²·log(μ/γ)` implies `γ = μ·e^{−1/(b₀g²)}`.
   **DONE** (`log_gap_to_exp` in `ConstructiveQFT.lean`, plus the factor-of-4 fix).
3. **The mass gap carries the scale** — `m(β) ≥ A·e^{−cβ}` with the derived `c`. **OPEN** — this is the
   constructive-QFT rung.

## Step 3, decomposed (the concrete work)

The transfer operator is `T(β) = e^{−aH(β)}` with the Kogut–Susskind Hamiltonian `H(β)`. The mass gap is
its spectral gap. The single bound `m(β) ≥ A·e^{−cβ}` needs the two mechanisms used together:

| sub-step | what it proves | status |
|---|---|---|
| 3a. **strong-coupling gap** | `m(β) > 0` at small β (the finite-volume Jentzsch gap) | DONE (kernel-checked: `strict_contraction_gives_gap`, `contraction_iterate_decay`) |
| 3b. **weak-coupling scale** | `m(β) ≥ A·e^{−cβ}` at large β — the running coupling sets the scale | **OPEN** |
| 3c. **crossover** | the strong- and weak-coupling bounds meet uniformly in β and volume | **OPEN** (follows 3b) |

3b is the whole rung. Its honest target: prove the Hamiltonian's spectral gap at weak coupling is set by
the running-coupling scale — i.e. the gap does **not** close faster than the beta function allows, and
carries the `e^{−cβ}` exponent derived from `b₀`.

## What 3b must engage (the three structures, from the earlier harvest)

1. **Heat-kernel / Gaussian approximation of SU(N)** — at weak coupling the measure becomes Gaussian on
   the Lie algebra, giving the `e^{−cβ}` from the Gaussian determinant.
2. **Character expansion (Peter–Weyl)** — `Tr U_p = Σ_r χ_r`, and the per-character spectral gap composes.
3. **Non-linear sigma-model analogy** — the weak-coupling YM as a sigma model on the group manifold.

Each is a `sorry`-target the churn loop (with me as the LLM) grinds; the kernel refuses anything but a
real proof.

## The jump at 3b (2026-11-22 harvest) — the heat-kernel determinant is the structure

The harvest located the specific transferable structure that derives `c` from the beta function: the
**heat-kernel determinant**. The chain is

```
det P = e^{−Tr log P}          (the weak-coupling partition function is a Gaussian determinant)
Tr log P ~ ∫ a₂(x,x) log(Λ²/μ²)   (the Seeley–DeWitt coefficient a₂ carries the beta function)
        ⟹  Z ~ e^{−cβ}          (the determinant's scale is the running coupling)
```

The `a₂` heat-kernel coefficient *is* the beta function (`a₂ ∝ b₀`), so the determinant
`e^{−Tr log P}` yields the exponent `c` **derived, not fitted**. The remaining move is to connect the
determinant's scale to the **spectral gap** — the smallest eigenvalue of the inverse propagator `P` is
the mass, so `m ≥ (the determinant's scale) = e^{−cβ}`. That is the single sub-lemma to formalise:

```
m(β) = inf spec P(β)   and   det P(β) ≥ e^{−2cβ}   ⟹   m(β) ≥ A·e^{−cβ}
```

So the jump at 3b is concrete: **formalise the heat-kernel determinant of the weak-coupling YM
propagator, show `a₂` gives `c`, and bound the spectral gap by the determinant's scale.** Each piece is
a `sorry`-target; the heat-kernel coefficient is the transferable structure (differential geometry →
running coupling → mass gap).

## The two halves of 3b — and where each stands (2026-11-22)

3b splits into the **scale** and the **gap**, and they are different mechanisms:

| half | mechanism | status |
|---|---|---|
| **scale** — the exponent `c` | heat-kernel determinant: `det P = e^{−Tr log P}`, `Tr log P ~ ∫ a₂ log(Λ²/μ²)`, `a₂ ∝ b₀` | **DONE** (`HeatKernel.lean`: `determinant_scale`, `determinant_gives_exponent`, kernel-checked) |
| **gap** — the minimum eigenvalue `m = inf spec P` | FSS/FILS infrared bound: reflection positivity → **Gaussian domination** → infrared bound `Ŝ(p) ≤ 1/(2J(p))` → spectral gap | **OPEN** — the Gaussian domination for the non-Abelian trace |

The scale half is now proven: the exponent `c` is derived from the beta function through the heat-kernel
determinant. The gap half is the FSS/FILS chain, and its only unproven link is the **Gaussian domination
for the non-Abelian trace observable** — the same single rung the whole reduction has been pointing at.
So the spectral-gap mechanism has been located precisely: reflection positivity (known) → Gaussian
domination (the rung) → infrared bound → minimum eigenvalue. The two halves of 3b meet at that one
estimate: it bounds the minimum eigenvalue (the gap) the same place the heat-kernel gave the scale.

## The Gaussian domination — the one estimate, and its specific structure (2026-11-22)

The harvest located the structure that could crack the Gaussian domination for the non-Abelian trace:
**the rigidity of the Gaussian under the non-Abelian symmetry.** In the presence of a non-linear symmetry
(non-Abelian gauge / BRST), Gaussianity is *forced* — the covariance is not free, it must be the
gauge-invariant kinetic operator, and the trace observable's Gaussian is determined by the group
structure. Concretely:

- the reflection-positivity → Gaussian chain (FSS/FILS) needs a *covariance*; for a non-Abelian theory
  the covariance is constrained by gauge invariance to the covariant Laplacian `K = −∇·D`;
- the observable `Tr U_p` is a character, and under the Peter–Weyl expansion `Tr U = Σ_r χ_r` the
  Gaussian domination reduces to the per-character case, where the group's rigidity fixes the covariance.

So the single estimate decomposes one final time into two rigidity lemmas:
1. **gauge-invariance rigidity** — the Gaussian covariance is the covariant Laplacian (forced by the
   non-Abelian symmetry), and
2. **character rigidity** — the trace's Gaussian is the per-character sum, each with the same covariance.

Each is a `sorry`-target; the transferable structure is the *rigidity* of Gaussianity under a non-linear
symmetry (the thing that turns "some Gaussian" into "the Gaussian", with the exponent carried by the
covariant Laplacian).




## The honest boundary

Steps 1–2 and 3a are done and kernel-checked. Step 3b (the weak-coupling running-coupling scale) is the
unproven constructive-QFT rung — it is the Clay mass gap restated, and no lemma-assembly or search
manufactures it. This plan locates it precisely and names the three structures a proof must engage.
