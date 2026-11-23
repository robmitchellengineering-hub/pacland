# The mass-gap proof — the full plan (not the rung in isolation)

Status: 2026-11-22. This is the big plan. The mistake so far was attacking the Gaussian domination in
isolation; the proof has to use the *proved* pieces as levers, in one connected argument. The lever is
the **character rigidity** (proved), and the plan is how it drives the whole final section.

## The one theorem, restated with the two mechanisms joined

```
m(β) = inf spec T(β)  ≥  A·e^{−cβ}          (volume-uniform)
    │                                        │
    ├─ mechanism 1: the gap  ────────────────┤ (the minimum eigenvalue, from the bulk spectrum)
    └─ mechanism 2: the scale ───────────────┘ (the exponent c, from the beta function)
```

The two mechanisms are **one bound on one object** — the transfer operator's spectral gap — and the
proof must carry them together, not conjoin them at the end.

## The lever: character rigidity (already proved)

The non-Abelian trace is a character, and the characters are a complete orthonormal system (Peter–Weyl):

```
Tr U_p = Σ_r χ_r(U_p)          (character rigidity — PROVED, trace_is_fundamental_character)
|χ_r| ≤ dim r                  (the Weyl bound — PROVED, su2_character_weyl_bound)
```

This is the lever because it **linearises the non-linearity**: the trace is not an arbitrary non-linear
function — it is a *sum of bounded characters*, and each character is a harmonic (smooth) function on the
group. The Gaussian domination, which FSS proved for linear observables, is attacked **per character**,
where the group's harmonic analysis gives the linear structure back.

## The connected proof (each step uses the previous, no step in isolation)

1. **Weak-coupling Gaussian** — the quadratic part of the plaquette action is the covariant Laplacian
   `−∇·D` (the FP operator). The Gaussian covariance is `−∇·D`; its determinant gives the scale
   `det = e^{−Tr log}` with `a₂ ∝ b₀` (the exponent `c`).
   *Done:* the determinant transport (`HeatKernel.lean`). *Open:* prove the physical measure's quadratic
   part *is* `−∇·D`.

2. **Reflection positivity** — the OS3 on the gauge-invariant Hilbert space. *Known* (Osterwalder–Seiler).

3. **Per-character Gaussian domination** — for each character `χ_r`, the partition function in an
   external field is dominated by the Gaussian: `Z_r(f) ≤ Z_free(f)`. This is the FSS chain
   (reflection positivity → chessboard → Gaussian), now applied **to one character at a time**, where
   the character's boundedness (Weyl) makes the FSS argument go through.
   *This is the core open step.* Its lever is: a character is not an arbitrary observable — it is a
   bounded harmonic, so the FSS reflection-positivity argument for linear observables extends to it.

4. **Sum over characters** — `Tr U = Σ_r χ_r`, and the per-character domination sums to the trace's
   domination, convergent by the Weyl bound (the heat-kernel character expansion converges).

5. **Minimum eigenvalue is volume-uniform** — the infrared bound `Ŝ(p) ≤ 1/(2J(p))` follows from the
   Gaussian domination, and its rate is uniform in volume, so `m = inf spec` is bounded below uniformly.
   This is `volumeUniformGap`, the survival of the finite-volume gap in the thermodynamic limit.

6. **Join with the scale** — the volume-uniform gap (step 5) and the derived exponent `c` (step 1) are
   the one bound `m(β) ≥ A·e^{−cβ}`.

## The honest core — step 3 is the whole problem, and here is how to attack it

The per-character Gaussian domination is the single step. It is attacked **not in isolation but with
steps 1–2 as hypotheses**:

- **Hypothesis A (gauge-invariance rigidity):** the Gaussian covariance is `−∇·D`. Once proved, the
  free propagator `Z_free` is `e^{½ ⟨f, (−∇·D)^{-1} f⟩}`, and the comparison is against the *correct*
  operator — not an arbitrary Gaussian.
- **Hypothesis B (character rigidity + Weyl):** the observable is a bounded character, so the external
  field's effect is controlled by `dim r`, and the FSS chessboard estimate (already kernel-checked in
  the transfer-matrix form) applies to it.

Step 3 = FSS chessboard (have it) + reflection positivity (known) + the covariance is `−∇·D` (step 1,
open) + the observable is a bounded character (proved). That is the *connected* target, not an isolated
one: three of its four ingredients exist, and the fourth (the covariance is `−∇·D`) is the gauge-invariance
rigidity.

## The work order

1. Prove **step 1** (the quadratic part of the plaquette action is `−∇·D`) — the weak-coupling expansion.
2. Prove **step 3** with steps 1–2 + the character lever — the per-character Gaussian domination.
3. Steps 4–6 are then transport and sum lemmas, each provable from the previous.

The honest boundary stays: step 3 is the Clay rung, and this plan is how the proved pieces (character
rigidity, Weyl bound, chessboard estimate, reflection positivity, determinant scale) *combine* to attack
it — the thing that has been missing is exactly this connected use of them.
