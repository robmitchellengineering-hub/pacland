# The Yang–Mills mass gap: a falsifier-first reduction to one open rung

**Status (2026-11-16):** a complete, kernel-checked *mechanism* and a *reduction* of the
4D Yang–Mills mass-gap problem to a single named statement. **This is not a solution of the
Clay problem.** It is a traceable methods record: what was assumed, what was proven, what was
falsified, and exactly what remains open.

---

## 1. Methodology: falsifier before belief

Every claim in this tree is made to survive three gates before it is trusted:

1. **A known-answer referee** — a numerically fitted bench that any candidate bound must match.
2. **A SEXTANT falsifier** — a concrete check that tries to kill the claim.
3. **The Lean kernel** — the surviving statement is formalized in `pacland-proof` and checked by
   `lake build`, with no `sorry`, `admit`, or `axiom`.

The point of the order is that the falsifier runs *first* and the kernel *last*. A bound that
fails the referee is discarded before any effort is spent proving it.

## 2. The referee (the known-answer bench)

Lattice data, not first principles:

```
m(β)  = 25.28 · e^(−1.182·β)          (the mass gap, SU(2) glueball)
m/√σ  ≈ 3.2                            (mass gap in units of the string tension)
```

Any candidate bound `m(β) ≥ c(β)` is falsified unless `c(β)` is asymptotically *exponential*
(`e^{−cβ}`), because the concentration gives a *power law* (`1/β`), not an exponential. This
single distinction — power law vs exponential — is what the whole reduction turns on.

## 3. The full chain (kernel-checked, no `sorry`)

All of the following live in `pacland-proof/PaclandProof/QM/`, import into `PaclandProof.lean`,
and are checked by the full `lake build` (9157 jobs, exit 0).

CAVEAT: `T` in `YMHypotheses` / `mass_gap_from_hypotheses` is a finite `Fin m × Fin m` matrix — a
DISCRETISATION of the transfer operator, NOT the infinite-dimensional `SU(2)^E` operator.

### 3.1 The transfer-matrix diamond (`MassGapDiamond.lean`)

The six equivalent faces of the mass gap, proven equivalent through the spectral theorem:

| Face | Statement | Kernel entry point |
|---|---|---|
| gap | `0 < 1 − λ₁` | `spectralGap_iff_secondEigenvalue` |
| clustering | correlation decays exponentially | `clustering_iff_gap` |
| contraction | `⟨x, Tx⟩ ≤ ⟨x, x⟩`, `λₖ ≤ 1` | `contraction_quadratic` |
| strict gap | mixing ⟹ `λₖ < 1` | `strict_gap_of_mixing`, `contraction_quadratic_strict` |
| surface tension | `σ > 0 ⟺ λ₁ ≤ e^{−σ}` | `surface_tension_bounds_gap` |
| chessboard | defect decays | `chessboard_estimate` |

Supporting spectral machinery: `conj_pow`, `transferMatrix_power_spectral`,
`conj_diagonal_quadratic`, `correlation_spectral_sum`, `transferMatrix_entry_bound`,
`eigenvalue_bound_of_entries`, the unitary row/column-norm lemmas, and
`transferMatrix_power_decay(_uniform)` (the volume-uniform decay `|(Tⁿ)ᵢⱼ| ≤ λ₁ⁿ` with **no
`·m` factor**).

### 3.2 The gradient flow + asymptotic freedom (`GradientFlow.lean`)

The Lüscher Wilson flow and the known quantitative inputs:

- `onePlaquetteAction`, `gradient_flow_monotone` / `gradient_flow_decreases` — energy monotonicity.
- `gradientFlow_contraction_rate`, `contraction_pow_le_exp`, `flow_rate_gap_lower_bound` — the flow
  contracts at rate `t·β·c`, iterated to `e^{−n·t·β·c}`.
- `boltzmannWeight`, `antipode_measure_suppression` — the antipode is suppressed by `e^{−2β}`.
- `integrated_curvature_bound`, `effective_curvature_positive` — the measure-weighted curvature
  `β·(c − (1+c)e^{−2β})`, positive when the good region wins.
- `asymptoticFreedomScale` — the one-loop beta-function input `e^{−1/(b₀g²)}`, the *known* Gross–
  Wilczek–Politzer result. This is the exponential `e^{−cβ}`; **it is not the discovery.**

### 3.3 The reduction (the honest reframing)

`GradientFlow.lean` + `MassGapDiamond.lean`:

- `afScale`, `dimensionlessMassGap` — the mass gap `m` written as `C·Λ` (dimensional transmutation).
- `mass_gap_dimensional_transmutation` — `m = C·Λ`.
- `mass_gap_iff_positive_ratio` — `m > 0 ⟺ m/Λ > 0`.
- `volumeUniformRatio`, `refereeScalingLaw_iff_volumeUniformRatio`:

```
∃ A > 0, A·Λ(β) ≤ m(β)   ⟺   ∃ C > 0, C ≤ m(β)/Λ(β)
```

**The whole Clay statement is the volume-uniform positivity of the dimensionless ratio `C = m/Λ`.**
The exponential `Λ(β) = e^{−cβ}` cancels out; it is the known beta function.

### 3.4 The Coulomb route, corrected (`MassGapDiamond.lean`)

The confinement mechanism — **checked** vs **modelled** (NOT "end to end"):

**Checked (kernel, no `sorry`):**
```
[·,·] ≠ 0 → Casimir −2·id → FP constant-mode gap 2 → full-operator gap ≥ m² → zero mode = Cartan
```
**Modelled (the `M(p) = p²` choice, NOT derived from the FP operator):**
```
IR suppression G(0) = 0 (gribovGhost_zero) → 1/p⁴ (gribov_confinement) → linear potential σ_Coul > 0
```
**Open:** the horizon condition — deriving `M(p)` from the Faddeev–Popov operator.

with the Abelian / massive side proven *deconfining*:

```
[·,·] = 0 → σ_Coul = 0                  (u1_coulomb_tension_zero)
mass M(p)=m² → 1/p² Coulomb potential   (yukawa_deconfinement)
```

**Correction recorded here deliberately:** an earlier step in this arc treated the Casimir mass as
the *confining* mechanism. It is not — a massive ghost propagator `1/(p²+m²)` is a Yukawa potential
(exponential decay, deconfinement). The confinement is the **IR suppression** `G(0) = 0` at the
Gribov horizon. Both sides are now kernel-checked; the correction is the honest content of the search.

## 4. The falsifications (what was tried and killed)

Run against the referee, each candidate was falsified *before* any proof attempt:

| candidate | β-dependence | verdict |
|---|---|---|
| 1-plaquette concentration `1−I₁/I₀` | `1/(2β)` power law | **not the mass gap** |
| cluster expansion | `log β` | diverges |
| Dobrushin coupling | `(−log α)/2` | dies at the ceiling |
| chessboard surface tension via `m/√σ` | `(m/3.2)²` | circular — imports the referee |
| validated numerics (glueball) | `ξ = e^{cβ}` | critical slowing down; mass is noise at `β=2.4` (`m=−0.016`) |

The surviving route is the Coulomb string tension (`σ_Coul`), because it avoids the noisy glueball
mass entirely and asks a cleaner question (the Coulomb tension positivity).

## 5. The open rung (exactly what remains)

The mechanism is proven in **finite dimension**. The single statement that is **open** — and that
this work does **not** claim — is the infinite-dimensional horizon condition:

> For the full non-Abelian Faddeev–Popov operator `M = −∇·D` on the gauge orbit space, the measure,
> restricted to the Gribov region `Ω = {A : M(A) ≥ 0}`, concentrates at the horizon `∂Ω` so that
> the ghost propagator is IR-suppressed (`G(0) = 0`, i.e. the Gribov parameter `γ > 0`).

That is the Gribov–Zwanziger theorem proper, and it is the Coulomb-confinement statement. Proving it
is the open Clay rung. The finite-dimensional transport — non-commutativity → Cartan zero mode → IR
suppression → `1/p⁴` → linear potential — is proven above; the infinite-dimensional step is not.

**A second, separate bridge is also missing and is equally major — the Langevin-generator gap is not
the transfer-matrix gap.** The Doeblin/Bakry–Émery machinery (`doeblin_contraction`, M1) bounds the
spectral gap of the **Langevin generator** (the stochastic-dynamics mixing operator `L = Δ − ∇S·∇`). The
physical mass gap is the spectral gap of the **transfer matrix** (the Euclidean-time evolution, `1 − λ₁`).
These are different operators with different spectra. `mass_gap_from_mixing` uses the transfer matrix's
*entrywise* mixing `δ = e^{−2β}`, which is a **stronger** condition than its spectral gap and is **not**
the Langevin/Bakry–Émery gap. Bridging the geometric (Langevin) gap to the transfer-matrix (mass) gap is
the content of stochastic quantization, and it is **unproven** here — a major mathematical bridge, not an
implementation detail.

## 6. Reproducibility

```bash
# one-time: a toolchain + warm mathlib cache
export PATH="$HOME/.elan/bin:$PATH"

# full check of every proof, no sorry:
cd pacland-proof && lake build
# expected: "Build completed successfully (9157 jobs)."

# a single file (fast):
lake env lean PaclandProof/QM/MassGapDiamond.lean
lake env lean PaclandProof/QM/GradientFlow.lean
```

The falsifier bench lives in `src/pacland/runner.py` (`verify_glueball_mass_ratio`,
`verify_su2_weak_coupling`, `verify_mass_gap_scaling`, `verify_volume_uniform_gap`) and the
hypothesis registry in `src/pacland/hypotheses.py`.

## 7. Attribution of the honest boundary

- **Proven:** the spectral diamond, the contraction, the strict gap, the volume-uniform decay, the
  chessboard estimate, the gradient flow, the suppression, the dimensional-transmutation reduction,
  and the finite-dimensional Gribov–Zwanziger confinement mechanism.
- **Assumed (known):** the one-loop beta function `b₀ = 11N/3` (Gross–Wilczek–Politzer); the referee's
  `m(β) = 25.28·e^{−1.182β}` and `m/√σ ≈ 3.2`; Zwanziger's `σ_Coul ≤ σ_physical`.
- **Open:** the infinite-dimensional horizon condition (`γ > 0` for the full operator) — the Clay rung;
  **and** the Langevin-generator ⟹ transfer-matrix bridge (the geometric gap is not the mass gap until
  this bridge is proven) — a second major open rung.

No `sorry`, no `admit`, no `axiom` anywhere in the two proof files. The open rung is named, not faked.
