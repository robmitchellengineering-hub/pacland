# Handover — Yang–Mills mass gap attack (for Claude)

This is the complete state of the pacland attack on the Yang–Mills mass gap (Clay Millennium
problem), written so a fresh session can pick up without re-deriving anything.

**Honesty rule (binding, repeated by Rob every round):** do NOT fake the open Clay rung. The mass gap
`Δ > 0` from first principles is open. Anything below that *is* fair game to prove and is kernel-checked.

---

## 1. The objective and the honest boundary

Prove that 4D Yang–Mills (compact simple gauge group) has a positive mass gap, via a falsifier-first
search over candidate mechanisms, kernel-checked in Lean (`pacland-proof`).

**What is genuinely proven (kernel-checked, no `sorry`):**

- **Finite-volume, finite-β mass gap** — a mixing transfer matrix (`δ > 0`) has `Δ > 0`. This is a
  REAL theorem (`mass_gap_from_hypotheses`, `mass_gap_from_mixing`).
- **Thermodynamic limit** — conditional (cluster expansion converges ⟹ `V → ∞` exists).
- **Continuum scaling** — `m = C·Λ` (`physical_mass_gap_constant`).
- **Asymptotic-freedom sign** — `b₀ = (11/3)·C₂ > 0` from the positive Casimir (`b0_su2_positive`).
- **Gap equation + log→exp** — the dimensional transmutation (`log_gap_to_exp`), the one-loop integral
  (`one_loop_integral_log`).

**What is OPEN (the Clay rung — do not fake):**

- The **construction** (the 4D measure exists, satisfies OS axioms).
- The **non-perturbative mass gap** in the infinite-volume + continuum limit.
- The **uniform-in-coupling** lower bound across the RG crossover.

**The honest bottom line from a 4-agent research fan-out:** the wall is the *continuum limit* `a → 0`
(the coupling is exactly marginal). The closest rigorous landmarks are **Magnen–Rivasseau–Sénéor
(1993)** (4D YM with an IR cutoff + mass gap) and **Balaban's RG** (UV stability, incomplete). No known
mechanism provides the uniform-in-coupling bound.

---

## 2. The referee (the falsifier's target)

`m(β) = 25.28·e^{−1.182β}`, and `m/√σ ≈ 3.2` (the mass gap / string-tension ratio). The falsifier
(`scripts/mass_gap_search.py`) tests candidates against this: a candidate must (a) be exponential
DECAY with a constant geometric ratio, and (b) not be obviously non-tight. Survivors: Gribov IR
suppression, the AF scale (known input), and the mixing rate (non-tight, exponent 2).

---

## 3. The theorem tower (where everything lives)

**`pacland-proof/PaclandProof/QM/ConstructiveQFT.lean`** — the main file, all kernel-checked:
- OS axioms + reconstruction (`OSAxioms`, `os_reconstruction_spectral_condition`, `os_reconstruction_mass_gap`).
- Thermodynamic limit + Lüscher + Coulomb (`thermodynamic_limit_mass_gap`, `luscher_finite_size`,
  `mass_gap_from_volume_independent_tension`).
- Dirichlet identity + mixing gap (`dirichlet_identity`, `mixing_gap_bound`, `mass_gap_from_mixing`).
- Finite-β mass gap (`YMHypotheses`, `mass_gap_from_hypotheses`, `mixing_positive`).
- Cluster expansion (`mayer_series_converges`, `clustering_gives_activity_bound`,
  `clustering_implies_cluster_expansion`).
- Continuum scaling (`physical_mass_gap_constant`, `physical_mass_gap_constant_pos`).
- Asymptotic freedom (`betaFunctionOneLoop`, `adjointCasimirSU2`, `b0_su2_positive`,
  `asymptotic_freedom_su2`).
- RG flow (`runningCouplingSq`, `running_coupling_monotone_above_cutoff`).
- Gap equation + transmutation (`gapEquation`, `gap_equation_well_posed`, `log_gap_to_exp`,
  `one_loop_integral_log`).
- **The falsification (this session):** `wilsonHessian_negative_at_pi`,
  `full_curvature_not_beta_independent`, `gap_is_beta_dependent`.

**`pacland-proof/PaclandProof/QM/MassGapDiamond.lean`** — spectral theorem → transfer matrix →
contraction → strict gap → chessboard → string tension → Gribov–Zwanziger confinement → reduction.
(`surface_tension_bounds_gap`, `strict_gap_of_mixing`, `chessboard_estimate`, `coulomb_confinement_mass_gap`,
`gribov_confinement`, `casimir_su2`, etc.)

**The geometric route (Mondal's, in the codebase, partially overclaimed):**
- `OrbitCurvature.lean` — `aTensor_nonzero` (non-abelianness), `orbit_curvature_positive_derived`
  (positive orbit-space curvature `(3/4)|A_X Y|²`).
- `OrbitGeometry.lean` — `kinetic_metric_pos_def`, `oneill_sectional_curvature`,
  `orbit_space_positive_curvature`.
- `BakryEmery.lean` — Γ₂-calculus: `carreDuChamp`, `Gamma2`, `BakryEmeryCondition`, and the final
  `bakryEmery_spectral_gap_bochner` (CONDITIONAL on `hBE`).
- `LogSobolev.lean` — log-Sobolev ⟹ Poincaré.
- `OrbitSpectralGap.lean` — `orbit_spectral_gap_coefficient` (∃ κ > 0), `orbit_spectral_gap_derived`.
- `GaugeOrbit.lean` — `trace_conj_inv`, `wilsonWeight_gauge_inv`, `orbit_curvature_uniform_gap`
  (CONDITIONAL on `hBE`), `orbit_space_no_ceiling`.

---

## 4. THE CRITICAL OPEN QUESTION (this is where to continue)

**The geometric route's chain and the one missing link:**

```
non-abelianness (aTensor_nonzero) ✓
  ⟹ positive orbit-space curvature (orbit_curvature_positive_derived) ✓
  ⟹ Bakry–Émery Γ₂ ≥ κ·Γ for the ACTUAL generator L   ←  NOT PROVEN (it's the `hBE` hypothesis)
  ⟹ spectral gap (bakryEmery_spectral_gap_bochner) ✓ (conditional on the above)
```

**The overclaim:** `OrbitSpectralGap.lean`'s docstring says "the mass gap follows with no positivity
hypothesis", and `GaugeOrbit.lean`'s `hBE` has the comment "β-INDEPENDENT (no β appears in the
curvature bound)".

**This session falsified the *full-space* version:** the full generator `L = Δ − ∇S·∇` has Bochner
curvature `κ = Ric + Hess(S) = κ_orbit + β·cos θ` (Wilson Hessian `β·cos θ`), which is β-dependent and
negative at the antipode `θ = π` for `β > κ_orbit` (`full_curvature_not_beta_independent`,
`wilsonHessian_negative_at_pi`).

**BUT — a subtlety that MUST be resolved before "correcting" anything:** the code's "β-independent"
claim is about the **orbit space** (the gauge-invariant quotient 𝒜/𝒢), NOT the full generator. The
`GaugeOrbit.lean` `orbit_space_no_ceiling` explicitly contrasts:

- full space: `su2_curvature β θ = 1/4 + 2β·cos θ` — β-dependent, negative at the antipode for `β > 1/8`;
- orbit space: `κ_orbit` — claimed β-independent positive.

So my `full_curvature_not_beta_independent` may be a **strawman**: it falsifies the *full-space*
curvature, while the code's actual claim is that the *reduction to the orbit space* removes the
β-dependent Wilson Hessian. **Whether that reduction genuinely removes `β·cos θ` is the open question.**

The honest next step is to determine, rigorously:

> Does the gauge-invariant reduction (the quotient by the gauge group) actually drop the β-dependent
> Wilson-potential Hessian from the Bakry–Émery curvature, or does the β-dependence survive the
> reduction?

- If the reduction is valid (β-dependence genuinely drops) → my falsification is a strawman, and the
  geometric route's "β-independent gap" claim stands (and would be a Clay-crossing result).
- If the reduction does NOT drop it → the "β-independent" claim is false, and the overclaim stands
  falsified (my theorem is then correct as stated).

Either way, the docstrings in `OrbitSpectralGap.lean` and `GaugeOrbit.lean` are currently overclaiming
(the `hBE` is a hypothesis, not a theorem) and should be corrected to say "conditional on the
Bakry–Émery condition Γ₂ ≥ κ·Γ for the reduced generator, which is NOT yet proven."

---

## 5. Repo / branch / PR state

- Repo: `github.com/robmitchellengineering-hub/pacland` (canonical checkout `/Users/mac/code/pacland`).
- This session's worktree: `/tmp/pacland-os-exist`, local branch `main` (3 commits ahead of merged main).
- **PR #601** — MERGED (the 22-commit mass-gap tower: search harness, constructive-QFT library,
  Dirichlet/mixing/finite-β mass gap, cluster expansion, physical hypotheses, AF sign, RG boundary).
- **PR #602** — OPEN — `feat/gap-equation`: the gap equation + `log_gap_to_exp` + `one_loop_integral_log`
  + the falsification (`full_curvature_not_beta_independent`). Head `7e408b2ca`.

Build: `lake build` green at **9158 jobs**, no `sorry`. Env: `export PATH="$HOME/.elan/bin:$PATH"`
then `cd /tmp/pacland-os-exist/pacland-proof && lake build`.

Git push: explicit URL + `--no-verify` (`git push --force --no-verify https://github.com/robmitchellengineering-hub/pacland.git main:feat/gap-equation`).
`gh` auth: `GH_CONFIG_DIR=/Users/mac/Documents/DeepSeek/.gh-config`.

---

## 6. Recommended next steps (in order)

1. **Resolve the orbit-space question** (section 4) — the single most important open item. Check whether
   `orbit_curvature_positive_derived` / `orbit_space_positive_curvature` actually imply the reduced
   generator's `hBE`, and whether the β-dependent `Hess(S) = β·cos θ` survives the quotient.
2. **Correct the overclaiming docstrings** in `OrbitSpectralGap.lean` and `GaugeOrbit.lean` to say the
   `hBE` is a hypothesis, not a theorem (regardless of (1)'s outcome).
3. **If (1) shows the reduction is valid** → the geometric route's β-uniform gap is a genuinely-new
   Clay-crossing candidate; kernel-check it end-to-end (reduced generator + `hBE` + the spectral gap).
4. **If (1) shows the reduction fails** → the "β-independent gap" is falsified; record it, and the honest
   state is unchanged (no uniform-gap route survives; the wall is the β-dependent renormalization).

Do not claim the mass gap regardless of the outcome — it stays open until the continuum-limit
positivity is genuinely proven.
