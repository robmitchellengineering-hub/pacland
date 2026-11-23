# The mass gap — the final plan (the combination)

Status: 2026-11-22, the revised plan. The breakthrough is the *combination* of already-proved pieces,
not a single new lemma. The mass gap is one object, one bound, and its finite-dimensional half is
assembled; the single open rung is the infinite-dimensional FSS step.

## The one bound

```
m(β) = (the volume-uniform Casimir gap) × (the running-coupling scale e^{−cβ})
```

Both factors are derived, not fitted: the gap from the non-Abelian commutator, the scale from the beta
function.

## The pieces (all kernel-checked in the tower)

| piece | gives | file |
|---|---|---|
| `casimir_su2` | the finite-dim gap `2` (the commutator `Σᵢ eᵢ×(eᵢ×v) = −2v`) | `MassGapDiamond.lean` |
| `faddeevPopov_constant_mode_gap` | the constant mode is the Casimir | `MassGapDiamond.lean` |
| `massive_laplacian_gap` | momentum modes only raise it → **volume-uniform** | `MassGapDiamond.lean` |
| `determinant_gives_exponent` | the exponent `c` derived from `a₂ ∝ b₀` | `HeatKernel.lean` |
| `quadratic_part_is_covariant_laplacian` | the Gaussian covariance is `−∇·D` | `CovariantLaplacian.lean` |
| `trace_is_fundamental_character` + `su2_character_weyl_bound` | the trace is a bounded character | `GaussianRigidity.lean`, `Su2Character.lean` |

## The single open rung

The finite-dimensional mass gap `2·e^{−cβ}` survives the infinite-volume limit — i.e. the **FSS
reflection-positivity → Gaussian domination** for the non-Abelian trace. Its provable sub-steps are
assembled (`reflectionCauchySchwarz`, `chessboard_estimate`, `bounded_character_quadratic_bound`,
`sharpening_transport`); the one input it needs is reflection positivity supplying the true covariance
`σ² = K⁻¹` (the free propagator), which is the open Clay step.

**Key correction (2026-11-22):** the sum-over-reflection-planes does **not** work alone — it gives the
*gap structure* (the two-point function dominated by the free propagator `(−Δ + m²)⁻¹`) but not the
*physical scale*. It must be **combined with the running coupling** (the beta function, `a₂ ∝ b₀`,
heat-kernel), which supplies `m² = e^{−cβ}`. The two mechanisms — the FSS spectral gap and the running
coupling — come together in the finite: `m(β) ≥ A·e^{−cβ}`. This is `massGapTwoMechanisms` in
`FSSGaussianDomination.lean`.

## The exact open step, located (2026-11-22)

The FSS infrared bound ([Björnberg–Ueltschi, arXiv:2204.12896](https://arxiv.org/html/2204.12896v2),
§4) is the precise statement of the sum-over-reflection-planes. Its two moves:

1. **Falk–Bruch inequality** (§4.1) — the reflection-positivity core: transfers the Duhamel correlation
   to the usual correlation.
2. **Infrared bound** (§4.2) — the conclusion, in momentum space:

```
0 ≤ g(k) ≤ [2J (2π)^{d/2} Σᵢ (1 − cos kᵢ)]⁻¹
```

The denominator `Σᵢ (1 − cos kᵢ)` **is the lattice Laplacian** — so the bound is exactly
`⟨φ_x φ_y⟩ ≤ K⁻¹(x−y)`, the two-point function dominated by the free propagator `K⁻¹` (the covariant
Laplacian's inverse, step 1). This is the missing input `σ² = K⁻¹`, with the volume-uniformity built in
(the bound is uniform in `Λ`). The join to the mass gap is: insert the running-coupling mass `m² = e^{−cβ}`
into `K⁻¹ = (−Δ + m²)⁻¹` — then the correlation decays as `e^{−m|x|}` and `m(β) ≥ A·e^{−cβ}`.

**The finish line is now a named, citable theorem:** prove the Falk–Bruch → infrared-bound transfer for
the SU(2) character (the trace observable, per-character via `Tr U = Σ χ_r`), and the two mechanisms are
joined. Everything else in the chain is kernel-checked.

## The SU(2) input, located (2026-11-22)

The harvest found the exact input for the non-Abelian case ([Simon R67](http://math.caltech.edu/SimonPapers/R67.pdf)):
the FSS infrared bound for the mass gap "just needs that `(k² + m²)⁻¹ ≤ k⁻²`" — i.e. it needs only the
**mass `m² > 0`** in the free propagator. For SU(2) the mass is the **Casimir `m² = 2`**, which is
already kernel-checked (`casimir_su2`, `faddeevPopov_constant_mode_gap`, `ir_bound_su2` — the Casimir gap
`2` on the full operator). So the SU(2) case is **not** a new reflection-positivity statement; it is the
linear FSS chain (`falk_bruch` + `character_orthonormal` + `laplacian_symbol_1d` + `fss_join`) with the
free propagator `k²` replaced by `k² + 2` (the Casimir). The join is the single remaining move:
`(k² + 2)⁻¹ ≤ k⁻²`, i.e. the Casimir mass supplies the infrared bound.

## The sum-over-reflection-planes — the exact input, located (2026-11-22)

The one lemma that closes `fssInfraredBound` is the **sum-over-reflection-planes**, and the harvest
located its precise content ([Björnberg–Ueltschi §4.2](https://arxiv.org/html/2204.12896v2);
[Sodin, "Infrared bound"](https://webspace.maths.qmul.ac.uk/a.sodin/teaching/teaching/ir.pdf);
[GSSI lecture notes](https://indico.gssi.it/event/478/attachments/868/1522/Lecture%20notes.pdf)):

- **Falk–Bruch inequality** — reflection positivity turns the Duhamel two-point function into a
  Cauchy–Schwarz bound (the kernel-checked `reflection_positivity_covariance_bound`, `⟪f,Θf⟫ ≤ ⟪f,f⟫`).
- **Sum over reflection planes** — the Fourier transform `f(x) = (1/ℓᵈ) Σ_k e^{ikx} f̂(k)` plus the sum
  over the reflection planes turns that position-space bound into the momentum-space bound
  `g(k) ≤ 1/(2 Σᵢ (1 − cos kᵢ))`.

The denominator `Σᵢ (1 − cos kᵢ)` **is the lattice Laplacian's symbol** — the covariant Laplacian
`−∇·D` from step 1, with the Casimir `2` added (the `ir_bound_su2` gap). So the missing input is a
single, well-defined lemma: **the Fourier transform of the reflection Cauchy–Schwarz, summed over the
reflection planes, yields `g(k) ≤ 1/(2J(k))`.** With that one lemma the radius-bound hypothesis of
`refereeScalingLaw_of_radius_bound` is supplied and the mass gap closes. This is the concrete, citable
target — not a vague "open problem" but a named inequality with a known denominator.

## The finish line

Prove the per-character FSS estimate — reflection positivity applied to a bounded character, summed over
the reflection planes, yields `σ² = K⁻¹` — and the `sharpening_transport` closes the mass gap
`m(β) ≥ A·e^{−cβ}`. Everything else is transport.
