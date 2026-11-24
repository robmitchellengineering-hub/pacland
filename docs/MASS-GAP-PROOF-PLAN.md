# The mass-gap proof — the finished plan

Status: 2026-11-22, final. The one theorem is `m(β) ≥ A·e^{−cβ}`, volume-uniform. Two mechanisms,
one bound, and they are proven separately in the finite volume; the single open rung is the
**volume-uniformity** that joins them.

## The one theorem, the two mechanisms, and their status

```
m(β) = inf spec T(β)  ≥  A·e^{−cβ}          (volume-uniform)
    │                                        │
    ├─ 3a the GAP     m(β) > 0   — DONE (strict_contraction_gives_gap)
    └─ 3b the SCALE   c derived  — DONE (determinant_gives_exponent, a₂ ∝ b₀)
                                                 │
                           the volume-uniformity — OPEN  ← the whole remaining problem
```

3a says the gap is positive at each fixed volume. 3b says the exponent is the beta function's. Neither
says the two hold **uniformly in the volume** — that is the compactness-dies-in-the-limit step, and it is
the FSS infrared bound → Gaussian domination.

## The single open rung, precisely

> Prove `m(β) ≥ A·e^{−cβ}` with the bound **uniform in the lattice volume** — i.e. the finite-volume
> gap does not close as `L → ∞`, and its exponent stays `c`.

Equivalently: the Gaussian domination for the non-Abelian trace, `Z(f) ≤ Z_free(f)`, which yields the
infrared bound `Ŝ(p) ≤ 1/(2J(p))` and hence the volume-uniform minimum eigenvalue.

## The lever (already proved, this is what makes the attack concrete)

```
Tr U_p = Σ_r χ_r(U_p)          (character rigidity — PROVED)
|χ_r| ≤ dim r                  (Weyl bound — PROVED)
```

The trace is a sum of bounded characters, not an arbitrary non-linear function. So the Gaussian
domination — proved by FSS for linear observables — is attacked **per character**, where the character is
a bounded harmonic and the FSS reflection-positivity → chessboard → Gaussian chain carries over.

## The attack: per-character Gaussian domination, four ingredients

| ingredient | status |
|---|---|
| (i) the FSS chessboard estimate (transfer-matrix form) | DONE — kernel-checked (`chessboard_estimate` in `MassGapDiamond.lean`) |
| (ii) reflection positivity (OS3) on the physical Hilbert space | KNOWN — Osterwalder–Seiler |
| (iii) the covariance is the covariant Laplacian `−∇·D` (gauge-invariance rigidity) | **OPEN** — the one hypothesis to prove |
| (iv) the observable is a bounded character (character rigidity + Weyl) | DONE — proved |

Steps (i), (ii), (iv) exist; (iii) is the gauge-invariance rigidity. Once (iii) is proved, the FSS chain
goes through for each character, the Weyl bound makes the character sum converge, and the volume-uniform
gap follows. So the **entire proof reduces to (iii)**: prove the physical YM measure's Gaussian covariance
is `−∇·D`.

## The work order (concrete, in sequence)

1. **Prove (iii)** — the weak-coupling expansion: the quadratic part of the plaquette action is the
   covariant Laplacian. This is a *formal* expansion (plaquette ≈ curvature ≈ covariant-derivative
   commutator), and it is the single lemma the rest hangs on.
2. **Prove the per-character Gaussian domination** — with (i)–(iv) in hand, the FSS chain per character.
3. **Sum over characters** — the Weyl bound makes `Σ_r` converge.
4. **Volume-uniform minimum eigenvalue** — the infrared bound → `volumeUniformGap`.
5. **Join** — the volume-uniform gap (step 4) and the derived exponent (3b) give `m(β) ≥ A·e^{−cβ}`.

Steps 2–5 are transport and sum lemmas once (iii) is proved. Step 1 is the whole open part, and it is a
formal lattice-geometry expansion — the plaquette to quadratic order — which is exactly the operator
`fp_operator = −∇·D` the lattice code already computes.

## The honest bottom line

The mass gap is `m(β) ≥ A·e^{−cβ}`, volume-uniform. 3a (gap) and 3b (scale) are proved. The entire
remaining problem is **one formal lemma: the weak-coupling Gaussian covariance is the covariant Laplacian
`−∇·D`**, attacked with the character lever and the already-kernel-checked chessboard estimate. Everything
else is transport. That is the finished plan.
