# The `hΘ` FSS rung — exact state and the label-inflation trap (round 1)

File: `pacland-proof/PaclandProof/QM/FSSGaussianDomination.lean` (namespace `FSSGaussianDomination`).

## What the rung is

The mass gap's mechanism 3 (volume-uniform finite-size scaling) is closed in this file by
`su2_character_volume_uniform_fss` (line 977), which takes as its single open input the hypothesis

```
hΘ : ⟪χ, latticeReflection χ⟫_ℝ
       = ∑ i : Fin m, ∑ j : Fin m, (WithLp.ofLp χ) i * (WithLp.ofLp χ) j * wilsonKernel θ β i j
```

with

- `latticeReflection : PiLp 2 (Fin m → ℝ) →ₗᵢ ℝ …` — the **geometric site reflection** `i ↦ −i`
  (`latticeReflection_inner` proves `⟪f, Θf⟫ = Σᵢ fᵢ·f(−i)`),
- `wilsonKernel θ β i j = Real.exp (2 * β * Real.cos (θ i − θ j))` — the **gauge-angle** Wilson/heat kernel.

## `hΘ` is FALSE as literally stated

For `m = 1` (single site, `Fin 1`), `−0 = 0`, so `latticeReflection` is the **identity**:
`⟪χ, latticeReflection χ⟫ = χ₀²`. But `wilsonKernel θ β 0 0 = exp(2β·cos 0) = exp(2β)`, so
`Σᵢⱼ χᵢχⱼ wilsonKernel = χ₀²·exp(2β)`. The hypothesis then forces `χ₀² = χ₀²·exp(2β)` for every `χ₀`,
i.e. `exp(2β) = 1` — false for `β > 0`.

So the ℓ² site-reflection `i ↦ −i` is **not** the gauge-angle Wilson kernel. This is exactly the
"label-inflation trap" the file's own doc comments warn about (`wilson_reflection_connection`, line 513,
is *trivially* the kernel-reflection definition — it proves `⟪f, wilsonReflection f⟫ = Σ fᵢfⱼKᵢⱼ` because
`wilsonReflection` is *defined* by that kernel, and is NOT the geometric reflection).

## The honest open estimate

The real input is `transferFactorization` (line 993), a `def`/`Prop`, not a theorem:

```
def transferFactorization {ι} [MeasurableSpace ι] [Fintype ι] (μ) (Θ : ι → ι) (K : ι → ι → ℝ) : Prop :=
  ∀ f : ι → ℝ, (∫ x, f x * f (Θ x) ∂μ) = ∑ i, ∑ j, f i * f j * K i j
```

i.e. the **Gibbs/Weyl measure's reflected correlation equals the Wilson-kernel quadratic form**. For SU(2)
this is the statement that the single-plaquette Gibbs measure (Weyl density `sin²θ dθ` on the class angle
`θ`, with `Θ : θ ↦ π − θ`) has two-point function the heat kernel `exp(2β cos(θᵢ−θⱼ))`, via the character /
Peter–Weyl / Jacobi–Anger expansion. This is the genuine measure-theoretic estimate — NOT the algebraic
square `(∫f)²` that `reflection_factorization` (line 1084) and `os3_weyl_positivity` (line 1101) already
prove for the product measure.

## What is already proved (do not redo)

- `wilson_reflection_connection` (513), `wilson_reflection_positivity` (529), `wilson_reflection_self_adjoint` (537) — the *kernel-defined* reflection's OS axioms (the trap, but useful for the transfer-matrix route).
- `latticeReflection_inner` (663) — `⟪f, latticeReflection f⟫ = Σᵢ fᵢ·f(−i)`.
- `fss_hpos_one_sided` (672), `os3_reflection_positivity_half` (649) — OS3 positivity for one-side-supported ℓ² fields (the honest ℓ² content).
- `weyl_reflection_invariant` (1040) — `∫ f(π−θ)·sin²θ = ∫ f·sin²θ`.
- `reflection_factorization` (1084), `os3_weyl_positivity` (1101) — product-measure factorization `(∫f)²`.
- `su2_running_mass_fss_bound` / `su2_momentum_space_fss_bound` / `fss_ir_bound_geometric(_one_sided)` — the FSS join *given* `hpos`.
- `freePropagatorDecay_holds` (1001) — the explicit Green's function `e^(−γ|x|)/(2 sinh γ)` satisfies `freePropagatorDecay`.

## Open `def`/`Prop` statements (the target)

1. `fssGaussianDomination (σ2 K) : Prop := σ2 = 1/K` (line 58) — σ² = K⁻¹.
2. `massGapTwoMechanisms (m A c) : Prop := ∀ β, A·e^(−cβ) ≤ m β` (line 66).
3. `freePropagatorDecay (mβ G) : Prop := ∃ C > 0, ∀ x, |G x| ≤ C·e^(−mβ|x|)` (line 968) — the *general* propagator decay (contour integration), beyond the explicit `freePropagatorDecay_holds`.
4. `transferFactorization` (line 993) — the honest measure→kernel connection (the real `hΘ`).

## Concrete next steps

1. Restate `su2_character_volume_uniform_fss` with the measure input `transferFactorization` in place of the
   false ℓ² `hΘ` (or add a sibling theorem that does).
2. Prove `transferFactorization` for the SU(2) Weyl measure: `∫₀^π f(θ)·f(π−θ)·sin²θ dθ = Σᵢⱼ fᵢfⱼ·exp(2β cos(θᵢ−θⱼ))`
   after discretization, via the Jacobi–Anger character expansion (the `Bessel.lean` machinery).
3. Prove the general `freePropagatorDecay` (contour integration) if the explicit `freePropagatorDecay_holds`
   is insufficient for the final `massGapTwoMechanisms` threading.
