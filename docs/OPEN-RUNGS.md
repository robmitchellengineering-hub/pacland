# The two open rungs, stated precisely

Everything formalizable up to the Clay content is now kernel-checked. These two are the open content —
stated precisely here so the boundary is unambiguous. Both are research programs, not session-scale edits.

## Rung A — the Polchinski-equation multiscale Bakry–Émery criterion (for gauge theory)

**What we have:** the falsified single-scale route (`κ = Ric + β·cos θ`, negative at the antipode) and
its toy fix (`effectiveHessian_bounded_below`: the flow softens the Hessian to `β·cos θ + Λ`, bounded
below by `Λ − β`).

**What is open:** the *actual* Polchinski equation — the effective action's RG flow
`∂_Λ S_Λ = (1/2)(S_Λ'' − (S_Λ')²)` — and the proof that the effective Bakry–Émery curvature
`κ_Λ = Ric + Hess(S_Λ)` satisfies a differential inequality that keeps it **bounded below uniformly in
Λ**. This is the Bauerschmidt–Bodineau multiscale BE criterion. **Status in the literature: proven for
sine-Gordon (`β < 6π`); NOT for gauge theory.** The toy `Λ·θ²` is a stand-in for the flow's true convex
contribution.

This rung would discharge the committee's UV finite-scale hypotheses (`Station.Admissible`, `CellHyp`,
`Grill.Coarse`, `NodeBound`, `HorizCalc`) — i.e. it is the crossover.

## Rung B — the mass gap (spectral support away from 0)

**What we have:** the statement (`HasEnergyGap` / `HasMassGap` against the committee's
`WightmanTheory.energyMomentum`), the PVM monotonicity (`projection_subset_zero`), and the vacuousness
sanity control (`hasEnergyGap_of_spectrum_at_zero`).

**What is open:** proving the constructed theory's joint spectral measure has **no support in the forward
cone below `Δ > 0`, off the vacuum** — i.e. discharging the two measurability side goals and, crucially,
proving the actual spectral-support bound from the Wilson measure. That is the Clay mass gap itself.

## The honest bottom line

"Completing" either rung is solving the corresponding half of the Millennium problem. The value of this
arc is that both halves are now reduced to **precise, nameable theorems** — with their foundations (the
toy, the PVM facts, the sanity controls) kernel-checked — rather than vague "the renormalization is hard."

No claim of either is made. They remain open.
