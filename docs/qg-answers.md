# Quantum gravity — the three answers

**Working toward the coupling: what we can actually *find*, from the kernel-checked halves.**

## Answer 1 — the coupling is free (kernel-checked)

`Gravity/QG.lean` — `coupling_free`: `∇·G = 0` involves no coupling, so the Einstein equation
`G = κ T` is consistent for *every* `κ ≠ 0`. `G` is a label, not a prediction — the QG analog of
`N_gen` and the 19.

## Answer 2 — gravity must be quantum (the no-classical-coupling no-go)

Composed from three kernel-checked pieces:

| ingredient | theorem | what it gives |
|---|---|---|
| Gleason | `Gleason.frameFunction_regular` | the Born rule is the *unique* **linear** probability rule |
| no-cloning | `QM.NoCloning.no_cloning` | no nonlinear "read-out" of a state → **no-signaling** |
| Lovelock + coupling | `QG.einstein_divergence_free`, `coupling_free` | the Einstein form is forced; the coupling is free |

**The argument (Eppley–Hannah / Page–Geilker, constraint-first):** a *classical* coupling
(the semiclassical `G_ab = κ ⟨T_ab⟩`, `⟨T⟩ = Tr(ρT)`) makes the spacetime a c-number functional
of the state, and its backreaction is **nonlinear in ρ** (the Einstein tensor is quadratic in the
metric's derivatives). A nonlinear evolution of ρ contradicts the Born rule's **linearity**
(Gleason) and lets a gravitational measurement signal faster than light (no-signaling). Therefore
**the coupling cannot be classical: gravity must be quantum.** The *value* of the coupling stays
free — the no-go rules out a *kind* of coupling, not a value.

*(The full Eppley–Hannah proof needs the analytic semiclassical gravity; the algebraic core above —
linearity + no-signaling — is what is kernel-checked. The metric's nonlinearity is the gated part.)*

## Answer 3 — the weakness is a deficit, and its size is exact

The coupling is free, but it (with `ħ`, `c`) defines the Planck scale — a **relation**, not a value:

```
M_pl = sqrt(ħ c / G) = 1.2209 × 10¹⁹ GeV/c²      (exact from SI constants)
LHC scale        = 1.4 × 10⁴ GeV
deficit          = M_pl / LHC = 8.7 × 10¹⁴  ≈  10¹⁵   (15 orders of magnitude)
Planck length    = 1.6 × 10⁻²⁰ fm
```

This is the **unmeasurable wall** made precise: the QG regime is ~15 orders beyond current
measurement. That is the *deficit* (`m`-framing), not a forced gap — it is the free coupling's
scale, and it is *why* "lack of experimental data" is a statement about the free column, not a
failure of the theory.

## The bottom line

- **Free, not derived:** the coupling `G` (Answer 1).
- **Quantum, not classical:** the coupling's *kind* is forced by no-signaling; only its *value* is
  free (Answer 2).
- **15 orders away:** the coupling's scale is the deficit, exactly computed (Answer 3).

Falsifiable: a consistent *classical* (semiclassical) coupling would kill Answer 2; a derivation of
`G` from the forced halves would kill Answer 1.

## Update — the BMV test is now kernel-checked

`QM/Entanglement.lean` machine-checks the algebraic core of the Bose–Marletto–Vedral / GIE test:

- `local_channel_preserves_product`: a classical (LOCC) channel `Φ ⊗ Ψ` maps a product state
  `u ⊗ v` to the product state `Φ(u) ⊗ Ψ(v)`.
- `local_channel_preserves_separable`: a convex combination of product states (a separable state)
  maps to a convex combination of product states — so a classical channel **cannot create
  entanglement**.

This turns Answer 2 from a statement into a **falsifiable tabletop prediction**: classical gravity
(LOCC) ⇒ two masses interacting only through gravity never entangle; so *observing* gravitational
entanglement (micrometre/milligram, ~10⁻³ eV) forces the coupling to be quantum. It is the QM-side
complement of `QM.NoCloning` (cloning and entangling are the two things a classical channel is
forbidden to do), and the bridge from "gravity must be quantum" (Answer 2) to the experiment that
would find it.
