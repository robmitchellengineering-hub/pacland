# The exact T⁶ toroidal orbifold oracle — build #2 done properly

`src/pacland/oracle/exact_t6.py` is the **exactly-solvable IIB flux compactification**
on T⁶ = (T²)³, replacing the toy `exact_toric` (whose tadpole was a placeholder).
Every observable is a **closed form**, so the oracle's systematic error is
identically zero — the verifier is *provably* exact.

## The closed forms (all real physics, none illustrative)

| quantity | closed form |
|---|---|
| intersection form Σ | `σ ⊗ σ ⊗ σ`, `σ = [[0,1],[-1,0]]` (8×8, unimodular) |
| period vector Π | `(1,τ₁) ⊗ (1,τ₂) ⊗ (1,τ₃)` (8-dim) |
| Kähler potential K | `−log(8 Im τ₁ Im τ₂ Im τ₃)` = `−log(i Π† Σ Π)` |
| Kähler metric g | `δᵢⱼ / (4 Im τᵢ²)` (diagonal) |
| D3 tadpole N_flux | `Fᵀ Σ H` (the symplectic pairing, an integer) |
| superpotential W | `(F − τ₀ H) · Π` |
| string coupling g_s | `1 / Im τ₀` |

## Why it matters (the two things it proves)

1. **The verifier is validated, not just claimed.** `scripts/validate_t6.py`
   self-asserts 13 known-exact identities to machine precision (det Σ = 1, the
   Kähler-potential identity, the metric against numerical ∂∂̄K, tadpole
   antisymmetry, W = (F−τ₀H)·Π, g_s = 1/Im τ₀). This is the **us-verifying-the-
   verifier** step: the oracle's error model is `bias = scale = beta = 0`,
   i.e. `p̂_e = 0`, so the certificate's oracle term vanishes and the two-level
   bound collapses to the candidate term only. The pipeline handles the exact
   case correctly — which is exactly the positive control build #2 exists to give.

2. **A bank of free validated rungs.** Each closed form is a known-exact target
   (c*), so the T⁶ background calibrates the whole certificate loop without any
   numerical sampler.

## What it does *not* do (honest scope)

It does **not** raise the SM Mitchell Deficit m (which counts *measured* +
computable + validated SM observables): T⁶ is not our universe, so its observables
have no experimental target. m stays 5. What T⁶ does is close the *pipeline* gap —
build #2 — which is the prerequisite for build #3 (the real CY oracle that will
raise m toward SM physics).

## Reproduce

```
python3 scripts/validate_t6.py          # 13/13 self-assertions
python3 -m unittest discover -s tests   # 137 tests
```
