# The economics constraint-first structure — the deep analog of the SM frontier

This is the economics twin of `docs/sm-frontier.md`. It applies the same three-way
classification — **constraint / label / parameter** — to an economy, and it follows the
expansion recipe's honesty rule (`docs/expansion-map.md` §5): fields without a clean
symmetry group get the *heuristic* version of constraint-first, and that is said out loud.

## The economy's exact structure decomposes the same three ways

| type | flux sector (proven) | Standard Model | economics |
|---|---|---|---|
| **constraint** — "what the system forbids" | D3 tadpole `N ≤ L` (the *unique* invariant) | anomaly cancellation, charge quantization | the accounting identities: double-entry conservation, Walras' law, sectoral balances, stock-flow |
| **label** — "which setup you picked" | `h¹¹, h²¹, c₂, κ` | gauge group; N_gen = 3 | the institutional structure: number of sectors, numéraire/currency, market structure |
| **parameter** — unpredicable | `W₀, g_s`, couplings, Λ | the ~19 free numbers | the deep parameters (β, σ, φ, θ, α, …) — free inputs |

The structural point is identical to physics: the *exact* content is **constraint +
label**, and the *non-exact* content is the free parameters. A model of the economy
predicts nothing exactly except what accounting forbids and what the institutions hand it.

## The checkable piece — and what is *provable* vs *heuristic*

The key honesty split, made precise. Unlike the flux sector (provable because Sp + the
First Fundamental Theorem existed), economics has **no clean symmetry group**. So:

**Provable — exact, by construction (no symmetry group needed).** The accounting
identities are not empirical laws; they are the *definition* of double-entry bookkeeping
and budget consistency, so they are exact regardless of any model:

```
E1   double-entry conservation   for ANY flow-of-funds matrix, Σᵢ bᵢ = 0
E1'  uniqueness                  the only value-free LINEAR conservation law is total conservation
E2   Walras' law → numéraire     p·z ≡ 0 forces N−1 independent conditions for N prices
                                 → only the RELATIVE price is fixed, the level is a free ray
```

`scripts/validate_economics_constraint_first.py` proves these exactly (Python `Fraction`,
zero floating point), the way `validate_sm_anomaly.py` proves anomaly cancellation.

**Cited — not proved here.** *Sonnenschein–Mantel–Debreu* (SMD): the *only* restrictions
on aggregate excess demand are Walras' law and degree-0 homogeneity, so *any* function
satisfying them is the aggregate demand of *some* economy. Consequence: aggregate data can
never *select* an equilibrium — the micro parameters are always needed. This is the
economics analog of Mitchell's Completeness ("no exact invariant selector").

**Heuristic — said so.** The generalization *"constraint + label exhausts the exact
structure"* is **not** a theorem for economics. It is the economics analog of the SM's
"unpredicable in any UV completion", which `sm-frontier.md` already flags as *conjectured,
not proven* — and economics is one step further out, because it lacks even the SM's
structure to anchor an invariant-theory argument.

## The deep parameters — the "19", and a stronger failure than the SM's

The SM's 19 parameters are free inputs *within* the SM, but a UV symmetry (GUT) could in
principle relate them (19 → 16). Economics is worse, and the reason is SMD: there is no
"economic GUT" that reduces the deep parameters, because **any** preference/technology
structure is consistent with **any** aggregate behavior. The deep parameters are not merely
unpredicable — they are **unidentifiable from aggregates**. That is the economics form of
the underdetermined wall (`docs/expansion-map.md` names causal identifiability as
economics' core wall).

## The falsifiable test

> **Derive any deep parameter of a canonical model from first principles** (rather than
> estimating it), or show that aggregate data alone identifies it — and the economics
> constraint-first generalization is falsified.

## Honest boundaries

- **"Constraint" means the pattern is forced, not that every number is determined** — the
  accounting identities fix the *relations* (sectoral balances sum to zero), never the
  *levels* (the price level, the size of any sector's surplus).
- **The identities are exact by definition, which is both a strength and a limit.** It is
  a strength (they are provable without a symmetry group); it is a limit (they carry no
  information about behavior — that is the whole point of SMD).
- **No theorem yet** for the heuristic half, exactly as the SM's full gauge-sector analog
  is still open. The honest claim is: the accounting identities are the *only exact linear
  structure*, and everything beyond that is free.

## Reproduce

```
python3 scripts/validate_economics_constraint_first.py    # 5/5 exact checks
PYTHONPATH=src python3 -m unittest tests.test_economics_constraint_first -v
```
