# The transfer-matrix / correlation-length route to the Milestone-3 bound

Status: the analytic formulation, 2026-11-22. This is the route the bound must come from, written
precisely so the open step is a single statement.

## The object

Discretise time: the lattice theory in the temporal direction is a **transfer matrix**
`T = e^{-aH}` on the spatial Hilbert space, with `H` the lattice Hamiltonian. Its spectrum is
`{e^{-aE_n}}`, ordered `E_0 < E_1 ≤ …`. The **mass gap** is

```
m = E_1 - E_0 = -(1/a) log(ρ_1/ρ_0) ,      ρ_n = e^{-aE_n}
```

and the correlation length is `ξ = 1/m`. Exponential clustering of the plaquette correlator is
equivalent (kernel-checked, the MassGapDiamond) to `m > 0` — i.e. to a **spectral gap** of `T`.

So the transfer-matrix route is the same object as the Hamiltonian route: a lower bound on the
transfer-matrix spectral gap **is** a mass-gap bound.

## The target (the referee)

`m(β) = 25.28 · e^{-1.182 β}`, `m/√σ ≈ 3.2`. In the language of the running coupling `g² = 2N/β`,
asymptotic freedom means the physical scale `m` is exponentially small in `β` — the `e^{-1.182 β}`
shape is the beta-function structure, not a fitted convenience. A bound that reaches it must
therefore carry the **running-coupling exponential** itself.

## Where the generic bounds fail (the recorded negative result)

- **Cluster expansion / polymer expansion**: gives `m ≥ c·log β` — a *polynomial* in β, which grows
  the wrong way and exceeds the referee at β = 3. It recombines existing inequalities and never
  sees the exponential.
- **Dobrushin single-site coupling**: `m ≥ (-log α)/2` with `α(β*) = 1` — dies at a finite ceiling
  and is negative past it. It is a *constant*, not an exponential.
- **Generic combinations**: any bound built from these primitives inherits their scale. The referee
  `check_bound` now rejects them mechanically — the negative result is that **recombination is
  provably insufficient**.

## The candidate structure (what the exponential must come from)

The mass gap is the energy of the lightest gauge-invariant excitation above the vacuum. Asymptotic
freedom says that excitation's mass is set by the running coupling `g²(μ)` at `μ ≈ m`:

```
m ~ μ e^{-1/(2 b_0 g²(μ))}        (b_0 = 11N / 48π²)
```

so `log m ~ -c·β` with `c = 12π²/(11N)`-class exponent — the `e^{-1.182 β}` shape. A bound that
reaches it must therefore be a **spectral estimate of the transfer matrix that sees the running
coupling**, not a rearrangement of known inequalities. The concrete carriers are:

1. **The correlation-length / transfer-matrix spectral estimate** — bound `ρ_1/ρ_0` (or equivalently
   the first excited energy) directly on the spatial lattice, using the gauge-invariant structure.
2. **The chessboard (reflection-positivity) estimate** — Fröhlich–Lieb–Loss: reflection positivity
   bounds the correlation function by a power of the partition-function ratio, and the ratio carries
   the `e^{-cβ}` coupling dependence.
3. **The gradient-flow / trivialising-map route** — Lüscher's Wilson flow as a change of measure; a
   flow-time lower bound that reaches `e^{-cβ}`.

## The open step, as one statement

Produce a **volume-uniform** lower bound `c(β) = A·e^{-c'β}` on the transfer-matrix spectral gap
`m = E_1 - E_0` with `c' ≥ 1.182`, derived from the running-coupling structure — and pass it through
`bound_search.check_bound`. The finite-lattice measurements (`λ_min`, string tension, screening mass)
remain the falsifiers that would kill a wrong candidate; they are not the candidate itself.
