# Yang-Mills mass gap — the plan v2 (solve existence + compute the value)

Supersedes the M1/M2/M3 order in `ym-mass-gap-plan.md`. Built on the 3-way research fan-out
(`ym-mass-gap-shorter-path.md`).

## The two targets, kept separate (this is the key correction)

1. **The Clay problem = EXISTENCE.** Prove the spectral gap > 0 for non-Abelian YM in d=4 (no mass term).
   This is a proof.
2. **The mass gap VALUE = a free parameter.** `m = c · Λ_QCD`, `c ≈ 7–8` (glueball mass in units of the
   string tension). `MassGap.lean` already proved the value is NOT derivable from the constraints — it is
   measured/computed, never predicted. So "find the value" is a NUMERICAL (lattice) job, not a derivation.

## Phase 1 — formalize the proven mechanism (achievable)

Replace "M3 = reconstruct Balaban's multiscale RG" with the **Bakry–Émery spectral-gap route**:

- **SZZ 2023** (arXiv:2204.12737): the lattice YM mass gap = the spectral gap of the Langevin generator,
  proven at strong coupling for SU(N)/SO(N) in any d>1. Finite-dimensional; the gap is a Poincaré/
  log-Sobolev inequality via the Bakry–Émery Γ₂-calculus + the Lie-group Ricci lower bound.
- **Bridges:** Durhuus–Fröhlich 1980 (mass gap ⇒ area law) + Chatterjee 2021 (confinement ⇔ center).
- Keep M1 (2D exact) + M2 (clustering ⇔ gap bridge) as the scaffolding.

Deliverable: the first machine-checked mass-gap theorem (strong-coupling lattice) + the two bridges.

## Phase 2 — attack the open step (the Clay problem itself)

The precise open statement:

> **Prove a β-dependent spectral-gap bound with the correct `e^{−cβ}` (asymptotic-freedom) scaling that
> survives past the curvature ceiling where `Ric − β·Hess(action)` turns negative.**

Attack: characterize exactly why the Bakry–Émery curvature fails at large β (the non-compact gauge-orbit
flat directions — Gribov–Singer), then find the bound that gets past it (the analogue of Polyakov's d=3
monopole mechanism, which does NOT exist yet in d=4). This is new mathematics; no literature crosses it.

## Phase 3 — compute the value (the "find the number")

Lattice Monte-Carlo for the glueball mass ratio `m/σ` (and `m/Λ`), targeting `c ≈ 7–8`. This is the honest
"mass gap value" — a number, not a theorem — and it is separate from the Clay existence proof.

## Honest boundary

- Phase 1 + Phase 3 are doable now.
- Phase 2 is the Millennium problem. No promise of a solution; the commitment is to attack the exact
  point (the curvature ceiling) with the hypothesis engine, landing every step kernel-checked, so that a
  path past the ceiling — if one exists — is found and machine-verified.

## Five sharper insights for Phase 2 (2026-11, added after the fan-out)

1. **The curvature ceiling is the GAUGE ORBIT, and it is unphysical.** `Ric − β·Hess(action)` turns negative
   along the flat gauge directions (the orbit G^{|V|−1}). The mass gap lives on the gauge-invariant sector —
   the orbit space — where Singer's observation is that the curvature is positive. So run Bakry–Émery on the
   ORBIT SPACE (or quotient the flat directions with a gauge-fixing — the axial gauge, #489, already does
   this). The ceiling is the coordinates, not the physics.
2. **The Tomboulis–Yaffe vortex criterion is a different route past the ceiling.** Prove the box is
   insensitive to a center vortex (`1 − Z^(−)/Z` decays exponentially in cross-section) ⇒ positive string
   tension. It is a boundary-condition argument, so it does not hit the curvature ceiling at all — the most
   concrete formalizable alternative (Tomboulis–Yaffe 1985; Kanazawa arXiv:0808.3442).
3. **The d=3 monopole mechanism is the template; d=4's analogue is instantons/vortices.** Polyakov's monopole
   condensation gives the gap at all couplings in d=3. The d=4 picture (center vortices, instantons) says the
   non-perturbative bound past the ceiling is a vortex/instanton expansion, not a perturbative one. That is
   the SHAPE the missing bound will take.
4. **The `e^{−cβ}` scaling is the falsifier.** `m ~ Λ_QCD = μ e^{−1/(2b₀g²)}` is non-perturbative. Any candidate
   bound that does NOT produce `e^{−cβ}` is provably wrong — requiring that scaling is a sharp hunt falsifier.
5. **Nissim's U(1)×SU(N) split.** Split the flat U(1) direction off and treat it as a random environment —
   a concrete technique for handling the one flat direction instead of the whole orbit (arXiv:2510.22788).
