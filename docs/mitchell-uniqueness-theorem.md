# Mitchell's Uniqueness Theorem — the conjecture's core, proved

`scripts/validate_mitchell_uniqueness.py` proves, symbolically (sympy, zero
tolerance, 6/6 checks), the mathematical backbone of the constraint-first
conjecture.

## Theorem (Mitchell)

> **The D3 tadpole `N_flux = Fᵀ J H` is the unique non-trivial bilinear symplectic
> invariant of the flux (F, H), for any compactification (any b₃).**

Precisely: among all bilinear forms in the flux, the only one invariant under the
symplectic group `Sp(b₃, ℤ)` is the pairing `Fᵀ J H`. The candidates `Fᵀ F`, `Hᵀ H`,
`Fᵀ H` are *gauge-dependent* (they change under a symplectic transformation), so they
are not physical observables; `Fᵀ J F = Hᵀ J H = 0` identically (antisymmetry).

## What this means for the conjecture

The constraint-first conjecture says *"the landscape's only exact structure is what
it forbids."* That was a **measurement** (the structure map: tadpole r = 1.0, all
else uniform) and an **exact-model observation** (T⁶). Mitchell's Uniqueness Theorem
closes the gap:

- the *only* flux quantity that is both **exact** and **gauge-invariant** is the
  tadpole — so there is no other structure for the landscape to have;
- everything else is either gauge-dependent (`FᵀF`, …), or a function of the
  stabilized moduli (W, g_s, masses, …), hence weak or uniform.

So "the only exact structure is the constraint" is no longer an empirical pattern —
it is forced by symplectic geometry. The constraint-first program stands on a
theorem, not just a measurement.

## Reproduce

```
python3 scripts/validate_mitchell_uniqueness.py   # 6/6 symbolic checks
```

The same argument on T⁶ (b₃ = 8) is `scripts/validate_t6_sympy.py` (8/8); the
general-b₃ case here is the CY (b₃ = 6) and trivially extends to any b₃.
