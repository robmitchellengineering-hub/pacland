# Constraint-first economics — the plan

Use the proven hard-science unifications as **constraints** to do economic analysis better and find
solutions — the SEXTANT constraint-first methodology applied to the soft field.

## The principle

Each verified unification is a **proven law** (a hard-science theorem applied to economics). A valid
economic model must satisfy **every** law that applies to it; a model that violates any one is refuted.
This is "constraint-first": decompose a question into **FORCED** (the laws) + **OPEN** (the rest), and the
solution is the model that survives **all** the forced constraints.

## The constraint library (built — `econ_constraints.py`)

| constraint | law |
|---|---|
| wealth-boltzmann-bulk | the wealth bulk is exponential `P(w) ∝ e^{−w/T}` |
| wealth-pareto-tail | the wealth tail is a power law `P(w) ∝ w^{−(α+1)}` |
| wealth-conserved | total wealth is conserved |
| business-cycle-limit-cycle | the cycle is sustained (a limit cycle) |
| goodwin-conserved | the wage-employment cycle has a conserved first integral |
| tatonnement-converges | the price converges (a gradient flow) |
| quantity-theory | `MV = PY` |
| capm-linear | expected return is linear in beta |

Extensible to all 22 verified economics unifications.

## The method (demonstrated)

**Wealth distribution** — three candidates, three constraints:
```
pure lognormal          → REFUTED (violates Boltzmann bulk + Pareto tail)
pure Pareto             → REFUTED (violates Boltzmann bulk)
thermal + super-rich    → VALID (exponential bulk + power-law tail + conserved)
```

**Business cycle** — three candidates, two constraints:
```
damped harmonic oscillator → REFUTED (decays; not a limit cycle, not conserved)
pure Lotka-Volterra        → REFUTED (conservative but structurally unstable — not a limit cycle)
van der Pol limit cycle    → VALID
```

The intersection of constraints **narrows the space**: each proven law eliminates a whole class of wrong
models, and only the model satisfying *all* of them survives. This is the "multiple real constraints" power.

## The build order

1. **Extend the constraint library** — add a checker for every one of the 22 verified economics
   unifications (each is a checkable predicate: "does this model have an exponential bulk? a limit cycle? a
   conserved quantity?").
2. **Encode the real questions** — for each open economics question, write the applicable constraints + the
   candidate models.
3. **Run the elimination** — the constraint-first checker refutes the wrong models and returns the survivors.
4. **Solve the survivors** — the hard-science SOLVERS (closed-form period, threshold, convergence rate) give
   the answers for the surviving class.
5. **Lean-prove the constraints we actually use** — promote them from tier-4 (numerical) to tier-1
   (kernel-checked) as needed, using the churn loop (V1.5 local + V2 frontier).

## The honest boundary

The constraints are **proven hard-science laws**, but the *application* to economics ("a wealth model must
be exponential in the bulk") is a modeling claim that must be stated as an assumption, not a fact. The
constraint-first method eliminates *internally inconsistent* models; it does not by itself prove the
surviving model is *empirically* right — that is the empirical tier (the data), still to come.

## The first real targets

1. Wealth distribution — **solved**: thermal + super-rich (exponential bulk + Pareto tail).
2. Business cycle — **solved**: van der Pol limit cycle.
3. Next: the inflation-unemployment trade-off (Phillips + isotherm + gradient constraints), the market
   equilibrium (tâtonnement + gradient + fixed-point constraints), the epidemic threshold (SIR + percolation).
