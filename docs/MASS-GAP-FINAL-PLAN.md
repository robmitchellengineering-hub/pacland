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

## The finish line

Prove the per-character FSS estimate — reflection positivity applied to a bounded character, summed over
the reflection planes, yields `σ² = K⁻¹` — and the `sharpening_transport` closes the mass gap
`m(β) ≥ A·e^{−cβ}`. Everything else is transport.
