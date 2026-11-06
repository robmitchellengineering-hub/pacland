# The Standard Model flavor invariant ring

**An independent Molien–Weyl computation confirming Bento–Silva–Trautner, with the GUT dimension drop**

*Authors: the pacland proof arm · Date: 2026-11-07 · Repository: `scripts/`*

**Abstract.** We recompute the Hilbert series of the Standard Model quark-sector flavor
invariant ring by a method independent of the literature — the **Molien–Weyl formula** (torus
constant-term + Weyl averaging), validated against the classical single-matrix series — and
recover the exact closed form, including the Jarlskog syzygy. For two 3×3 matrices under U(3)
conjugation we find

```
H(t) = (1 − t¹²) / ((1−t)² (1−t²)³ (1−t³)⁴ (1−t⁴) (1−t⁶)),
```

i.e. **10 CP-even primary + 1 CP-odd secondary invariant**, the numerator `(1 − t¹²)` being the
Jarlskog identity `J² = (CP-even polynomial)`. For the SM Yukawa sector (H = YY†, so every degree
doubles) this is

```
H_Y(t) = (1 − t²⁴) / ((1−t²)³ (1−t⁴)⁴ (1−t⁶)⁵ (1−t⁸) (1−t¹²)),
```

of Krull dimension **13** (= 9 masses + 4 CKM), matching the Lie-algebra rank test. Our
independent method **agrees** with Bento–Silva–Trautner ("The basis invariant flavor puzzle",
arXiv:2308.00019), who derived the same 10+1 ring via the plethystic logarithm. We add the explicit
**GUT dimension drop**: the orbit space shrinks 19 → 14 (SU(5)) → 7 (SO(10)), and of those
relations only gauge unification survives data.

## 1. Setup

The SM quark Yukawa sector is two 3×3 matrices `H_u = Y_u Y_u†`, `H_d = Y_d Y_d†` (Hermitian)
under U(3) conjugation `H → U H U†`. The flavor invariants are the ring `C[H_u, H_d]^{U(3)}`. The
Molien–Weyl formula gives its Hilbert series as the constant term

```
H(t) = (1/6) · CT_z [ ∏_{i≠j}(1 − z_i/z_j) / ∏_{i,j}(1 − t z_i/z_j)² ],
```

where `z₁,z₂,z₃` are the torus coordinates and `CT_z` is the constant term (z⁰) of the Laurent
series. We compute it degree-by-degree in `t` (sympy, exact rational arithmetic), validated by
reproducing the classical single-matrix series `1/((1−t)(1−t²)(1−t³))`.

## 2. Result — the exact Hilbert series

The coefficients `c_d = dim(degree-d invariants)` are

```
1, 2, 6, 14, 29, 56, 107, 186, 320, 530, 851, 1332, 2051, …
```

which match the closed form

```
H(t) = (1 − t¹²) / ((1−t)² (1−t²)³ (1−t³)⁴ (1−t⁴) (1−t⁶)).
```

Reading off the structure:

- **11 generators**, degrees `{1,1,2,2,2,3,3,3,3,4,6}`: the six "mass" traces `tr(H_u^k)`,
  `tr(H_d^k)` (k=1,2,3) and the five mixed traces `tr(H_u H_d)`, `tr(H_u²H_d)`, `tr(H_u H_d²)`,
  `tr(H_u²H_d²)`, and the CP-odd Jarlskog `J`.
- **One syzygy** at degree 12: the numerator `(1 − t¹²)` is the Jarlskog identity `J² =
  polynomial in the CP-even invariants`, so `J` is a *secondary* invariant — algebraic of degree 2
  over the primary ring.
- **Krull dimension** 11 − 1 = **10** (6 masses + 3 CKM angles + 1 CP phase).

For the SM Yukawa matrices (degree 2 in Y), every degree doubles (`t → t²`) and the lepton sector
`1/((1−t²)(1−t⁴)(1−t⁶))` multiplies in:

```
H_Y(t) = (1 − t²⁴) / ((1−t²)³ (1−t⁴)⁴ (1−t⁶)⁵ (1−t⁸) (1−t¹²)),
```

Krull dimension 3 + 4 + 5 + 1 + 1 − 1 = **13** = 9 masses + 4 CKM, matching the Lie-algebra rank
test (`validate_sm_rank_test.py`: quark 36→10, lepton 18→3).

## 3. Agreement with Bento–Silva–Trautner

Bento, Silva, Trautner (arXiv:2308.00019, JHEP01(2024)024) derive "the algebraic ring of 10 CP
even (primary) and 1 CP odd (secondary) basis invariants, using the Hilbert series and plethystic
logarithm." Our 10 primary + 1 secondary (the Jarlskog `J`, secondary via `J² = CP-even`) is the
**same ring**, obtained here by the Molien–Weyl constant-term rather than the plethystic logarithm.
The two methods agree — an independent confirmation of the published result.

## 4. The GUT dimension drop (our addition)

The 19 SM parameters are the orbit-space dimension of the full coupling space (13 Yukawa + 3 gauge
+ 2 Higgs + 1 θ). The GUT embeddings act on the couplings and shrink the orbit space
(`validate_sm_invariant_dimension.py`, cross-section count):

| group | Yukawa invariants | total | drop |
|---|---|---|---|
| SM (flavor only) | 13 | **19** | — |
| SU(5) (`Y_d = Y_e`) | 10 | **14** | 5 (3 mass ties + 2 gauge) |
| SO(10) (`Y_u = Y_d = Y_e`) | 3 | **7** | 12 (6 mass unifications + 4 CKM + 2 gauge) |

So the claim "the SM has no clean duality group" is **false as stated**: the GUT groups *do* reduce
the 19. The precise truth is that only the SM's own flavor symmetry leaves 19; the known UV groups
reduce it, and only their **gauge unification (drop 2) survives data** — the Yukawa unifications are
numerically wrong. This refines "no UV completion predicts the 19" to: *no known* completion derives
more than 2 of the 19 correctly, and those 2 are relations, not values.

## 5. Reproducibility

```
python3 scripts/validate_sm_molien_weyl.py        # the exact Hilbert series (this paper)
python3 scripts/validate_sm_invariant_dimension.py # the GUT dimension drop
python3 scripts/validate_sm_rank_test.py           # the Lie-algebra rank cross-check
```

All scripts are exact (rational arithmetic, no floating point), and the numbers were independently
re-verified on a second machine (the harness mesh, `pacland-rog`).
