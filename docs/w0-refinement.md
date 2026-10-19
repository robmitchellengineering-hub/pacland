# W₀'s weak structure is its own flux dependence — not the tadpole's scale

A correction to the structure map, measured with the Rule of Three on the 174-SUSY
wide-flux sample (`data/rich_sample.json`).

## The claim being tested

The structure map recorded W₀ as "weakly learnable (r ≈ 0.62), scale via the
tadpole". That last clause was a hypothesis, not a measurement. It says W₀'s weak
learnability is *carried by* the D3 tadpole — i.e. W₀'s magnitude tracks N_flux =
FᵀJH, and once you remove the tadpole the rest is uniform.

## The test (condition on the tadpole)

1. Compute the exact tadpole FᵀJH from the flux (verified: Pearson 1.0 against the
   stored tadpole on the 107-vacua sample).
2. Fit log|W₀| on the tadpole (linear + quadratic).
3. Take the residual, and ask: is the residual still learnable from the flux?

## The result

| quantity | ridge-CV r | permutation z |
|---|---|---|
| W₀ ← full flux | 0.62 | — |
| W₀ ← tadpole alone | 0.31 | — |
| W₀ residual (tadpole removed) ← flux | **0.57** | **6.95** |

The residual's single-coordinate MI is also significant (z = 10.07). So the
tadpole explains only *part* of W₀'s learnability, and a large, significant piece
remains after it is removed.

## What this means

W₀ is *itself* a flux functional — at a fixed vacuum, W₀ = flux · Π(z_vac) is
linear in the flux — so its weak learnability is its **own direct flux dependence**,
not the tadpole's scale leaking through. The tadpole (FᵀJH) and W₀ (flux · Π) are
two *different* flux functionals, correlated (Pearson 0.35) but not the same.

**Refinement of the structure map — three tiers:**

1. **Exact (r = 1.0):** the D3 tadpole — the topological charge, the constraint.
2. **Weak (r ≈ 0.6):** W₀ — directly flux-determined (it is the superpotential),
   *not* via the tadpole.
3. **Uniform (r < 0.25):** g_s, gauge couplings, mass-spectrum shape, axions,
   dilaton, AdS V — genuinely stabilization-dependent and uniform.

The headline conclusion is unchanged: **no observable carries the strong (r > 0.9)
fingerprint** (W₀'s r = 0.62 is weak). But the *reason* W₀ is weakly learnable is
now correct: it is a flux functional, not a slave of the tadpole. This is the
honest correction the Rule of Three exists to force.
