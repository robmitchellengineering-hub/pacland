# The continuum 4D Yang–Mills mass gap — the precise missing lemma

Source: the `lgt` formalization (Douglas + Rajasekaran), `LGT/MassGap/StrongCoupling.lean`.
This records the *exact* boundary of what is proven and the *exact* statement that remains.

## What is proven (machine-checked, `lgt`)

For U(n) Wilson lattice YM on the periodic torus (ℤ/Nℤ)^d, d ≥ 2, the connected plaquette
2-point function decays exponentially:

```
|⟨Re Tr U_p · Re Tr U_q⟩_c| ≤ C · exp(−m · latticePlaquetteDist p q)
```

with the mass-gap rate, explicitly (from `DobrushinVerification.lean`):

```
influenceBound n β   = 1 − exp(−4nβ)
dobrushinAlpha n d β = maxNeighbors d · influenceBound n β
m                     = (−log(dobrushinAlpha n d β)) / 2
```

valid under the strong-coupling hypothesis

```
β < 1 / (4n · maxNeighbors d)          (the Dobrushin ceiling)
```

## The regime gap (the whole remaining problem, stated exactly)

The lattice spacing does **not** appear in `lgt` — distances are integer lattice units, so
`m` is a decay rate *per lattice step*. The physical mass is `m_phys = m / a` (a = lattice spacing).

The continuum limit `a → 0` at fixed physical coupling is **asymptotic freedom**: the lattice
inverse coupling `β = 2n / g(a)²` diverges, `β → ∞`, as `g(a) → 0`.

But the theorem's hypothesis is `β < 1/(4n·maxNeighbors d)` — **small β (strong coupling)**. At
the ceiling `β → β_c`, `α → 1` and `m = (−log α)/2 → 0`. Beyond the ceiling the bound is vacuous.

So the two regimes are **disjoint**:

```
proven:  β < β_c = 1/(4n·maxNeighbors d)   (strong coupling, m > 0)
needed:  β → ∞                             (weak coupling / asymptotic freedom)
```

The strong-coupling bound cannot be "extended" across the ceiling — the method itself (Dobrushin)
degenerates there. This is the gap, and it is the Clay problem (confinement).

## The target lemma (to state + attack in Lean)

> **Spacing-uniform mass gap.** For fixed physical coupling `g` (so `β(a) = 2n/g(a)²` with
> `g(a) → 0` as `a → 0` by asymptotic freedom), the physical mass gap is bounded below uniformly:
>
> ```
> ∃ m > 0, ∀ a > 0,   m_phys(a) := (−log α(β(a))) / (2a)  ≥  m
> ```
>
> i.e. the lattice mass `m(a) = (−log α(β(a)))/2` decays at most linearly in `a`, not faster.

Equivalently (the form a Lean statement would take): for the renormalized mass
`m_phys(a) = m(a)/a`, show `liminf_{a→0} m_phys(a) > 0`.

## The concrete next formalization targets (in increasing difficulty)

1. **State it.** Add a spacing parameter `a` and the physical coupling relation `β = 2n/g²` to the
   `lgt` lattice, define `m_phys(a) = (−log(dobrushinAlpha n d β(a)))/2 / a`, and state the lemma.
2. **The provable negative direction.** Kernel-check that `m(a) → 0` as `β → β_c` (the ceiling),
   i.e. the *strong-coupling* bound cannot be spacing-uniform — this makes the regime gap a theorem.
3. **The positive direction (open).** The mass gap at `β → ∞` — a genuinely new argument (the
   Dobrushin method fails there), equivalent to confinement. This is the Clay problem.
