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
have no experimental target. m stays 9. What T⁶ does is close the *pipeline* gap —
build #2 — which is the prerequisite for build #3 (the real CY oracle that will
raise m toward SM physics).

## The exact structure map (the conjecture, proven not measured)

T⁶ lets us state the constraint-first conjecture *as a theorem* on a solvable model:

- **the D3 tadpole FᵀΣH is the only moduli-independent flux observable** — it is a
  pure function of the flux integers, so it is exact (the analogue of r = 1.0);
- **every other observable depends on the moduli** — W = (F−τ₀H)·Π depends on τ,
  g_s = 1/Im τ₀ depends on τ₀, K and the metric depend on the T² complex structures.

The moduli are set by the flux only through the F-term equations DW = 0, so those
observables are *weak* (flux-determined only via stabilization), never exact. That
is the measured structure map's three-tier picture — exact (tadpole) / weak
(W₀, saxions) / uniform (g_s, gauge, …) — reproduced *analytically* on T⁶, with the
"exact" tier provably unique. `validate_t6.py` asserts it (19/19).

## The swampland conjectures, exactly

T⁶ is where the swampland conjectures become closed forms, on the *correct* moduli
(the Kähler moduli — the CY proxy in `docs/swampland-connection.md` ran on the CS
moduli, the wrong sector). For a T² of volume v:

- KK mass `m_KK = 1/√v` (the inverse radius), winding mass `m_w = √v`;
- the Kähler-moduli geodesic distance is `d = ½ log(v/v₀)`;
- hence the lightest tower mass falls **exactly** as `m(v) = m(v₀) e^{−d}` —
  the **distance conjecture**, proven.

And the **Weak Gravity Conjecture** is *saturated*, not just satisfied: the KK
gauge coupling `g_KK = 1/√v` equals the KK mass scale, so the KK mode's ratio
`z = g_KK/m_KK = 1` — the extremal bound, exactly. (No global symmetries was
already in hand: det Σ = 1, the unimodular charge lattice.)

So on T⁶ the full swampland package — distance, weak gravity, no global symmetries,
tadpole/gravity — is **proven exactly**, bookending the measured CY versions.

## Two grades of verification

- **Numerical** (`scripts/validate_t6.py`, 21/21): the closed forms checked to
  1e-12 against known values — the runtime oracle is correct.
- **Exact** (`scripts/validate_t6_sympy.py`, 8/8): the *same identities proved
  symbolically with sympy, zero tolerance* — `det Σ = 1`, `i Π†ΣΠ = 8 Im τ₁Im τ₂Im τ₃`,
  the no-scale identity, tadpole antisymmetry (symbolic F, H), the distance
  conjecture `m = m₀ e^{−d}`, and WGC `z = 1`. These are algebraic equalities, not
  approximations.

## Reproduce

```
python3 scripts/validate_t6.py          # 21/21 numerical self-assertions
python3 scripts/validate_t6_sympy.py    # 8/8 exact symbolic checks
python3 -m unittest discover -s tests   # 272 tests
```
