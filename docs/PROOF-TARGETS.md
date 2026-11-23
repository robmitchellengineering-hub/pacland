# Proof targets — the β-dependence rung (queued for the churn loop)

Status: formulated 2026-11-22. These are the precise Lean statements the prover grinds on once the
`lake build` lands. They are the *provable* sub-lemmas between the (kernel-checked) transport bridge
and the open running-coupling bound — each is an assembly of existing lemmas, which is exactly the
loop's Level-1 capability.

## The target chain

```
runningCouplingBound (λ₁)          — the OPEN rung:  ∃ A>0, ∀ β>0, λ₁(β) ≤ e^{-A·e^{-(12π²/11)β}}
        │  (the β-dependence of the transfer-matrix spectral gap — running coupling)
        ▼
RefereeScalingLaw.transport         — CLOSED:  radius bound → scaling law  (RefereeScalingLaw.lean)
        ▼
QM.refereeScalingLaw                — the Milestone-3 target
```

The transport is done. What remains is to carry the coupling β into the spectral gap `λ₁`.

## The precise target (the one statement to prove)

```lean
theorem scalingLaw_of_runningCoupling {λ₁ : ℝ → ℝ}
    (h : runningCouplingBound λ₁) (hpos : ∀ β, 0 < β → 0 < λ₁ β) :
    QM.refereeScalingLaw (fun β => -Real.log (λ₁ β)) := by
  rcases h with ⟨A, hA0, hλ⟩
  exact RefereeScalingLaw.refereeScalingLaw_of_radius_bound hA0 hλ hpos
```

This is a one-line assembly — it needs `runningCouplingBound` and the positivity of the spectral
radius, and the loop proves it mechanically.

## The provable sub-lemmas (the assembly steps to grind)

1. **Spectral-radius positivity** (Perron–Frobenius): a non-negative irreducible transfer matrix has
   a positive leading eigenvalue — `∀ β, 0 < λ₁ β`. This closes `hpos` above.
2. **Coupling monotonicity**: if the transfer-matrix entries have the Boltzmann structure
   `T(β)ᵢⱼ = e^{-β·ΔSᵢⱼ}` (`ΔSᵢⱼ ≥ 0`, off-diagonal), then `λ₁(β)` is non-increasing in β — the gap
   closes at weak coupling. This is the *direction* of asymptotic freedom, and it is a genuine
   spectral-theory + entry-monotonicity assembly.
3. **Chessboard coupling dependence**: bound the chessboard estimate's defect rate `λ₁(β)` by the
   partition-function ratio that carries `e^{-cβ}` — the step that turns "decreasing" into
   "exponentially decreasing at the running-coupling rate".

Each of 1–3 is a `sorry`-target in `.prove/` (never committed) that the loop fills and the kernel
refuses unless it is a real proof. 3 is where the honest frontier sits: it needs the running-coupling
exponential, which is the Clay step — 1 and 2 are its provable scaffolding.

## What the loop does NOT do (honest boundary)

The loop proves *assemblies of known lemmas*. It cannot manufacture the running-coupling exponential
in 3 — that is the open mathematics. Targets 1 and 2 are the mechanical scaffolding it *can* grind;
3 is the rung the scaffolding is being built to reach.
