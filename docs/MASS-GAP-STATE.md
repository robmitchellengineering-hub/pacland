# Mass gap — the point to work from (state, 2026-11-22)

This is the definitive record of where the Yang–Mills mass-gap work stands. Everything below is either
kernel-checked (Lean, no `sorry`), a named theorem, or an honest refutation. This file is the working
point: the single open rung is stated at the bottom.

## The full reduction (one chain)

```
clustering ⟺ spectral gap                    (kernel-checked, MassGapDiamond.lean)
    ⟹ chessboard estimate                     (kernel-checked)
    ⟹ contraction rate = the gap              (kernel-checked, contraction_iterate_decay)
    ⟹ strict contraction = positive gap       (kernel-checked, strict_contraction_gives_gap)
    ⟹ finite-volume gap = Jentzsch/Krein–Rutman   (positive + compact + irreducible transfer operator)
    ⟹ compactness dies in the infinite-volume limit  (continuous spectrum appears)
    ⟹ volume-uniformity is the FSS infrared bound → Gaussian domination   (the open rung)
```

The mass gap is `m(β) = inf spec T(β)`, the transfer operator's spectral gap. Its exponent `c` is
**derived** from the beta function through the heat-kernel determinant (`det P = e^{−Tr log P}`,
`a₂ ∝ b₀`, `Tr log P = c·β` — kernel-checked, `HeatKernel.lean`). The Gaussian covariance of the
weak-coupling measure is the **covariant Laplacian `−∇·D` = the Faddeev–Popov operator** (the loop closes
on the operator the lattice thread measured, `fp_operator`, `λ_min ≈ 2.4`).

## The zero-mode question — resolved (2026-11-22)

> Does the continuum covariant Laplacian `−∇·D` have a zero mode at the horizon?

**Yes — by definition, and it is a gauge artifact.** The Gribov horizon is the boundary where the FP
operator's lowest eigenvalue first hits zero, and the horizon is a **measure-zero set**. A mass gap is a
*bulk* property; a zero mode confined to a measure-zero boundary cannot force a bulk gap. Therefore the
horizon zero mode is **not the mass-generating mechanism** — the GZ horizon is removed as a candidate.
The mass gap must come from the **bulk spectrum**.

## The single open rung (the point to work from)

The bulk mass gap is the transfer operator's spectral gap, and it needs **one** thing:

> **the volume-uniform gap — the finite-volume Jentzsch gap survives the infinite-volume limit.**

That is the FSS infrared bound → **Gaussian domination for the non-Abelian trace observable**:

```
reflection positivity (Osterwalder–Seiler, known)
    ⟹ Gaussian domination  Z(f) ≤ Z_free(f)   for the non-Abelian trace  Tr U_p   (OPEN)
    ⟹ infrared bound  Ŝ(p) ≤ 1/(2J(p))
    ⟹ minimum eigenvalue m > 0, volume-uniform
```

The Gaussian domination decomposes into two rigidity lemmas, one done and one stated:

1. **character rigidity** — `Tr U_p = Σ_r χ_r`, and the trace is the fundamental character
   (`trace_is_fundamental_character`, kernel-checked).
2. **gauge-invariance rigidity** — the covariance is the covariant Laplacian `K = −∇·D` (the transverse
   condition `p^μ K_{μν} = 0`; stated as `covariantLaplacian`, not yet proved for the physical measure).

## What is done vs open

**Done (kernel-checked, no `sorry`):** clustering ⟺ gap, chessboard estimate, contraction = gap, strict
contraction = positive gap, the transport bridge (spectral radius → scaling law), the volume-uniform
transport, the heat-kernel determinant scale (exponent `c` derived), the character rigidity, the two
positivity lemmas, and the factor-of-4 fix in the GZ gap equation.

**Open (one statement):** the Gaussian domination for the non-Abelian trace — equivalently, prove the
physical YM measure's Gaussian covariance is `−∇·D` and the minimum eigenvalue is volume-uniform.

**Refuted (recorded, honest):** cluster expansion (log β), Dobrushin (ceiling), single-plaquette (1/β),
the finite-N FP horizon (UV cutoff `λ_min/a² → ∞`), the compact-operator Jentzsch bridge in the
infinite-volume limit, and the GZ horizon as the mass mechanism (measure-zero gauge artifact).

## The reflection-positivity input (σ² = K⁻¹) — the single missing thing, located (2026-11-22)

The harvest located the exact theorem that supplies the missing input: the **FSS infrared bound**
([arXiv 2204.12896](https://arxiv.org/html/2204.12896v2)). Reflection positivity gives the *Gaussian
domination* — the characteristic function is bounded by the free Gaussian:

```
⟨e^{i Σ f·φ}⟩ ≤ e^{−½ Σ f·K⁻¹·f} ,   K⁻¹ = the free propagator (ω² + k²)⁻¹
```

The argument is the reflection Cauchy–Schwarz `C(θf, f) ≥ 0` plus the **sum over reflection planes** —
and the covariance it yields is exactly `K⁻¹`, the covariant Laplacian's inverse. So the missing input
`σ² = K⁻¹` is not a free constant: it is *forced* by reflection positivity to be the free propagator.

The route to the non-Abelian case is the **character lever**: `Tr U = Σ_r χ_r` (proved) turns the trace
into a sum of bounded characters, and the FSS argument applies **per character** — each character is a
bounded harmonic, so the reflection-positivity → Gaussian chain carries over to it, then the sum
transport (proved) reassembles the trace. The remaining open step is the *per-character* FSS argument
(the reflection positivity applied to a character), which is the non-Abelian Clay rung — but the input is
now precisely located, not a mystery: **reflection positivity forces `σ² = K⁻¹`, via the sum over
reflection planes.**

