# The mass gap — the consolidated state (the hard think, 2026-11-22)

The mass gap `m(β) ≥ A·e^{−cβ}` is **three mechanisms multiplying**, not one thing in isolation.

| # | mechanism | what it is | status |
|---|---|---|---|
| 1 | **spectral gap** | the finite-volume gap `2` (the Casimir `Σᵢ eᵢ×(eᵢ×v) = −2v`) | PROVED (`casimir_su2`, `massive_laplacian_gap`) |
| 2 | **running coupling** | the exponent `c = 12π²/11` (heat-kernel `det P = e^{−Tr log P}`, `a₂ ∝ b₀`) | PROVED (`determinant_gives_exponent`) |
| 3 | **volume-uniformity** | the finite gap survives the thermodynamic + continuum limit (FSS infrared bound on the non-Abelian trace) | **OPEN** |

## The precise open rung

Mechanism 1 gives the gap at every finite volume (the momentum modes only *raise* `2`). Mechanism 2
gives the scale. The single open rung is mechanism 3: **the volume-uniform reflection-positivity estimate
for the SU(2) character** — the two-point function of the trace observable dominated by the free
propagator, uniformly in the volume — the step that lets the finite gap survive the thermodynamic limit.

Everything proved this session is the **linear/Abelian** version of mechanism 3:

- `falk_bruch` — reflection Cauchy–Schwarz (via `real_inner_mul_inner_self_le`).
- `character_orthonormal` — the Fourier isometry (via `AddChar.wInner_cWeight_eq_boole`).
- `laplacian_symbol_1d` — the `2(1−cos k)` symbol.
- `fss_join` — the covariance bound `⟪f,Θf⟫ ≤ ⟪f,Lf⟫/J`.
- `casimir_infrared_bound` — `(k²+2)⁻¹ ≤ k⁻²` (the SU(2) input, proved).

The **SU(2) character** version of mechanism 3 (the trace's reflection positivity, volume-uniform) is the
open Clay rung. Not "one more lemma" in the sense of a shuffleable detail — it is the heart of the Clay
problem.

## What is NOT a solution (the traps to stop repeating)

- `su2_mass_gap_join` (defining `m(β) = 2·e^{−cβ}` then proving the scaling law) is a **tautology**, not
  the mass gap. The actual mass gap is the spectral gap in the infinite-volume limit.
- Re-naming the abstract inner-product Cauchy–Schwarz as "the FSS bound" is not mechanism 3; mechanism 3
  is a statement about the reflection-positive **measure** of the SU(2) trace, uniform in volume.

## The two-system note (SEXTANT / discovery engine)

This work has been done **in chat** (manual Lean edits + kernel-check over SSH + `web_search`). It has
**not** been routed through SEXTANT / the discovery engine / the falsifier infrastructure / the mesh.
That is a gap to close: the volume-uniform SU(2) estimate is exactly the kind of thing the discovery
engine + falsifiers + mesh compute should be pointed at, not hand-rolled in a chat loop.
