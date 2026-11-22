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

## The honest boundary

Steps 1–2 and 3a are done and kernel-checked. Step 3b (the weak-coupling running-coupling scale) is the
unproven constructive-QFT rung — it is the Clay mass gap restated, and no lemma-assembly or search
manufactures it. This plan locates it precisely and names the three structures a proof must engage.
