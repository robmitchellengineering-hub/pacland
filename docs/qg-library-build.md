# The QG library build — crossing the last gate

The constraint-first QG theory is complete at the algebraic level (Born rule, Einstein form,
constraint `∇·T = 0`, WdW `Ĥ|ψ⟩ = 0` as `ker Ĥ`, quantum/free coupling, time emergent). The one
remaining step — the **concrete `Ĥ` operator on quantum geometry** — is a *library build*, not a
physics gap. This is its precise scope, in dependency order.

## The wall, classified

Mathlib v4.35 has the metric (`RiemannianMetric`) but **no** Levi-Civita connection, Riemann tensor,
or covariant-derivative stack. So the ADM constraint cannot even be *stated* as a manifold theorem.
This is not intractable / unmeasurable / underdetermined / undecidable — it is a **tool gap**, and
per the standing rule ("a missing thing is a build task, not a wall") the move is to build it.

## The build, in order

1. **Levi-Civita connection** — the unique metric-compatible, torsion-free connection. Algebraic
   core (already done in `Gravity/Bianchi.lean`): the abstract `CovDerivCurvature` with the metric
   compatibility `∇g = 0` (used implicitly via the inverse-metric identity) and the curvature
   symmetries (`h_asym12`, `h_asym34`).
2. **Riemann tensor + Ricci + scalar** — the contractions. Algebraic core done (`ricci`,
   `scalarCurvature`); the manifold version needs the Levi-Civita stack.
3. **The 3+1 (ADM) split** — the 3-metric `q_ab`, lapse `N`, shift `N^a`, and the extrinsic
   curvature `K_ab` (the "momentum" `π_ab = √q (K_ab − K q_ab)`).
4. **The constraint operators** — the Hamiltonian constraint
   `Ĥ = G^abcd π_ab π_cd − √q R(³)` and the momentum constraints `Ĥ_a = −2 ∇_b π^b_a`, where
   `G^abcd = (1/2)(q^ac q^bd + q^ad q^bc) − q^ab q^cd` is the **DeWitt supermetric**.
5. **The Dirac (hypersurface-deformation) algebra** — the commutators `[Ĥ, Ĥ]`, `[Ĥ, Ĥ_a]`,
   `[Ĥ_a, Ĥ_b]` that close, encoding diffeomorphism invariance. This is the "unification"
   structure: the constraint algebra IS the diffeomorphism group.
6. **Physical states** — `ker Ĥ` (algebraic core done in `Gravity/WheelerDeWitt.lean`).

## The smallest buildable seed

Step 4's kinetic term — the **DeWitt supermetric** `G^abcd` — is pure finite-index linear algebra
over the abstract 3-metric, with no manifold machinery. It is the next kernel-checkable rung:

- `G^abcd` is symmetric in `(ab) ↔ (cd)` and in `a ↔ b`, `c ↔ d`.
- the Hamiltonian constraint is `G^abcd π_ab π_cd − √q R(³) = 0` (the two terms: kinetic + potential).
- the supermetric is the *unique* ultrahyperbolic metric on superspace (the space of 3-geometries).

Kernel-checking the supermetric's symmetry + its role in `Ĥ` is the concrete first step of the
build, and it can be done now (finite-index tensors only).

## What this delivers when done

The full constraint-first QG is then stated as an actual theorem: the physical states are `ker Ĥ`
with the *explicit* `Ĥ` above, the constraint algebra closes (diffeomorphism invariance), and time
is emergent. That is the honest end of the unification — and it is a **finite, well-scoped build**,
not an open physics problem.
