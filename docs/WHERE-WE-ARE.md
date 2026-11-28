# Where we are — the Yang–Mills mass gap (honest state)

Last updated 2026-11-28. This is the anti-drift record: the one place to read before doing more
work, so we do not re-derive or over-claim.

## The one-liner

> The **lattice mass gap is proved** (sharp `A = 1/2`), the **gap survives** the continuum limit
> (`Δ_phys > 0`), and the **sharp value `β·gap → 1/4` is reduced to one verified-true irreducible
> inequality** — but the **continuum existence on ℝ⁴ is open**, and that sharp cubic is a standalone
> hard result, not yet kernel-checked.

## The Clay problem is NOT solved

Two halves: (1) continuum **existence** of 4D Yang–Mills (Wightman axioms on ℝ⁴), (2) the **mass
gap** `Δ > 0`. We proved the mass gap only at the **lattice** level. The continuum ℝ⁴ existence is
the open half. Do not claim otherwise.

## What is proved (kernel-checked, no `sorry`, in `feat/massgap-clean`)

1. **Lattice mass gap, sharp `A = 1/2`** — the heat-kernel gap `1 − I₁(2β)/I₀(2β)` with the sharp
   Amos bound, the block-spin/hΘ reflection-positivity machinery, the connected-correlation limit,
   and the cluster/polymer expansion (rungs 11–15). Published to Zenodo (DOI 10.5281/zenodo.24585251),
   honestly scoped.
2. **Gap-survival `Δ_phys > 0`** — the physical mass `β·(1 − I₁/I₀)` is bounded `1/5 ≤ · ≤ 1/2`, so
   it does not close in the `a → 0` limit. Scale analysis complete: bare gap `→ 0`, naive ratio
   `→∞`, physical mass on the `1/β` scale.
3. **The sharp-bound wiring (11 rungs)** — Riccati, Chu–Vandermonde ×4, reduction identity, product
   formulas `I₁²`/`I₀I₂`, Turán series + inequality, `I₂′` derivative, and the double-ratio
   cubic-nullcline ODE `W′ = 2x·C(Φ)/(Φ²(Φx−2)²)`.

## What is reduced but NOT proved

The sharp `β·gap → 1/4` (full 't Hooft cutoff-independence) reduces to the single irreducible
inequality

> `C(Φ) = xΦ³ − 2Φ² − xΦ + 1 < 0`  ⟺  `2I₀²I₂ < I₁²(I₀+I₂)`  ⟺  `I₀(I₁²−I₀I₂) > I₁³/x`

This is the second-order **Simpson–Spector / Segura** Bessel bound. It is **verified true**
(coefficients nonnegative through order 22) but resists ~18 routes (no-crossing, `x·s` monotonicity,
coefficient closed-form, monotonicity-in-`r`, factorization, rational relaxation, continued fraction,
leading-term, two termwise-matchings, pointwise recurrence, double-ratio ODE, Bakry–Émery curvature —
the last restates the Riccati rather than discharging it).

## What is genuinely open (not attempted)

- The **`a → 0` correlation-function continuum limit** — the actual construction of the ℝ⁴
  Wightman/Schwinger functions via region decomposition + RG + OS→Wightman reconstruction.
- The **sharp cubic** above (a standalone hard result; needs the published Simpson–Spector
  double-ratio *monotonicity* lemma, or total-positivity/Pólya-frequency, or the `K`-Bessel
  Wronskian route).

## The next real step (if resuming)

Transcribe the Simpson–Spector double-ratio **monotonicity** proof (we already have the ODE
`bessel_double_ratio_deriv`; the missing piece is the monotonicity argument that discharges
`C(Φ) < 0`), or move to the `a → 0` correlation-function limit.
