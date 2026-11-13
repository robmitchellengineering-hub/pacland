# The CS-vs-Kähler (mirror) moduli convention — read from arXiv:2306.06160

The blocker named in `src/pacland/limits.py` for the instanton-corrected spectrum:
"the CS-vs-Kähler (mirror) moduli convention." This file records what that convention is,
so the hand-written finite-difference Kähler metric can be built without re-deriving it.

## The identification (the convention)

At a Large Complex Structure (LCS) limit, the complex-structure moduli `Z^i` of `X_3` are
**identified with the Type IIA Kähler moduli of the mirror** `X̃_3` (paper, §2.2, eq. 13):

> the coordinates `Z^i` of `M_cs(X_3)` are identified with the Type IIA Kähler moduli in the
> large-volume limit … on the mirror dual CY `X̃_3`.

So "Kähler modulus" in the jaxvacua code is **the same variable as a CS modulus**, read on the
mirror side. The CS moduli take values in the mirror's Kähler cone `K = {J : Vol_J(U) > 0}`.

## The Kähler potential (eq. 1) and the prepotential (eq. 14)

```
K = -log(-i Π† · Σ · Π) - log(-i(τ - τ̄))          Σ = [[0, 1], [-1, 0]]
Π = (2F - Z^i F_i,  F_i,  1,  Z^i)                F_i = ∂F/∂Z^i

F = -1/6 κ_ijk Z^i Z^j Z^k + 1/2 a_ij Z^i Z^j + b_i Z^i + i/2 ξ̃ + F_inst(Z)
```

- `κ_ijk` = triple intersection numbers of `X̃_3`; `a_ij`, `b_i`, `ξ̃` from eq. (15).
- `F_inst(Z)` = the worldsheet-instanton sum (the term whose second derivative hangs under autodiff).
- `W = (f - τ h)^T · Σ · Π(Z)` (eq. 4) — the GVW superpotential.

## The Kähler metric — the piece autodiff hangs on

The moduli-space metric is the Hessian of `K`:

```
g_iȷ̄ = ∂²K / ∂Z^i ∂Z̄^ȷ̄
```

Since `K = -log(-i Π† Σ Π) - …`, the metric is built from `Π` and its first derivatives — all of
which are **callable** (the periods `period_vector` / `period_derivatives` in `exact_t6.py`). The
finite-difference shortcut is therefore:

```
g_iȷ̄ ≈ [K(Z⁺ᵢ, Z̄⁺ⱼ) - K(Z⁺ᵢ, Z̄⁻ⱼ) - K(Z⁻ᵢ, Z̄⁺ⱼ) + K(Z⁻ᵢ, Z̄⁻ⱼ)] / (4 h²)
```

a pure-function four-point stencil on `K`, **no JAX autodiff** — which is what `limits.py` already
specified and what unblocks the instanton-corrected Hessian.

## Scope of the T⁶ oracle vs the full convention

- `potential_t6.py` carries the **CS side** (axio-dilaton `τ0` + 3 CS moduli `τ1,τ2,τ3`), with the
  STU Kähler potential `K = -ln(2 Im τ0) - ln(8 Im τ1 Im τ2 Im τ3)` and the **diagonal** metric
  `g_ii = 1/(4 Im τ_i²)`.
- The **Kähler side** (the mirror `T_i`, and the `F_inst` instanton term) is what jaxvacua adds and
  what the full EFT mass matrix needs. The T⁶ is self-mirror, so `T_i ↔ τ_i` up to the cone
  identification — the mirror map is the identity for the torus.

## Source

Dubey, Krippendorf, Schachner, "JAXVacua — A Framework for Sampling String Vacua",
[arXiv:2306.06160](https://arxiv.org/abs/2306.06160), §2.1–2.2 (eqs. 1, 2, 4, 13, 14).
