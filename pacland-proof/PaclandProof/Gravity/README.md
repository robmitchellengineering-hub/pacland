# Gravity — the contracted Bianchi identity (forced half)

The gravitational forced half is the contracted Bianchi identity `∇·G = 0` (the Einstein tensor
is divergence-free) — the analog of the SM's anomaly cancellation: the Einstein equation's LHS
is *required* to be divergence-free, forcing `∇·T = 0` (local stress-energy conservation).

## The wall (measured 2026-11-07)

Mathlib v4.35 has the Riemannian **metric** but **not** the Levi-Civita connection, Christoffel
symbols, Riemann curvature tensor, Ricci/scalar curvature, Einstein tensor, or the Bianchi
identities. Enumerated from the olean cache:

- Present: `Geometry/Manifold/Riemannian/Basic`, `…/PathELength`,
  `Geometry/Manifold/VectorBundle/Riemannian`, `Topology/VectorBundle/Riemannian`.
- **Absent:** `Curvature*`, `Connection*` (Levi-Civita), `Bianchi*`, `Einstein*`, `Ricci*`,
  `Christoffel*` — zero files.

So `∇·G = 0` cannot even be *stated* in current Mathlib (no Einstein tensor). Building the full
stack (Levi-Civita → Riemann → Bianchi) is a research-level formalization, not a "kernel-check a
theorem" task.

## The way around (per the "use the wall" rule)

The contracted Bianchi is a **tensor-algebra** consequence of the second Bianchi identity plus
the curvature symmetries — it does not need the analytic existence of the Levi-Civita
connection. The honest kernel-checkable slice is the *algebraic core*:

1. Define an abstract curvature tensor `R_abcd` with the algebraic symmetries (antisymmetry
   `R_abcd = −R_abdc`, pair symmetry `R_abcd = R_cdab`, first Bianchi `R_abcd + R_acdb + R_adbc = 0`).
2. State the second Bianchi identity `∇_e R_abcd + ∇_c R_abde + ∇_d R_abec = 0` (an assumption —
   the analytic fact that the Riemann tensor *satisfies* it is the part that needs the missing
   machinery).
3. **Prove** the contracted form: with `G_ab = R_ab − (R/2) g_ab`, `∇^b G_ab = 0` — a finite
   index computation (contract twice, use the symmetries, get `2∇^b R_cb − ∇_c R = 0`).

This is the same forced/free shape as the rest of the proof arm: the forced half (`∇·G = 0`) is
kernel-checked from the *symmetry* assumptions, and the free half (which geometry realizes the
assumptions) is delimited.
