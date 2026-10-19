# Darboux's theorem and the constraint-first result — two foundations, one conclusion

Two *different* theorems force the same sentence. This is a strengthening, not a
duplication.

## The two theorems

| theorem | what it says | what it kills | domain |
|---|---|---|---|
| **Darboux** | a symplectic form has **no local invariants** — every symplectic manifold is locally standard (`ω = Σ dpᵢ ∧ dqᵢ`) | the *local geometric* fingerprint (a symplectic analog of curvature) | differential geometry |
| **Weyl's FFT** (our backbone) | the symplectic group Sp(2n), acting on the flux pair, has exactly **one** invariant — the tadpole `Fᵀ J H` | the *duality-invariant algebraic* fingerprint | algebraic invariant theory |

We did **not** rediscover Darboux. The flux-sector proof (Mitchell's Uniqueness,
Constraint-First, Mitchell's Completeness) rests on **Weyl's First Fundamental Theorem
(1939)** — a result about the invariant ring of a group action, not about local
diffeomorphisms of a manifold.

## The bridge: two steps in one logical chain

Darboux's theorem says the local geometry of a symplectic manifold reduces entirely to
the **linear** symplectic group Sp(2n) acting on the tangent space — locally you are in
`ℝ²ⁿ` with structure group `Sp`. The FFT then classifies `Sp`'s invariants.

```
Darboux:   local symplectic geometry  ──▶  Sp(2n)  (no local invariant beyond linear)
FFT:       Sp(2n)-invariants on the flux pair  ──▶  the tadpole FᵀJH  (only invariant)
```

Together they are the full argument:

> **Darboux says "there is no local fingerprint"; the FFT says "there is no
> duality-invariant fingerprint either — only the pairing." What survives is global
> topology (symplectic capacities, Gromov–Witten, Floer homology, the Hodge numbers)
> plus the constraint (the tadpole).**

That surviving structure is exactly the **Complete Exact Structure theorem**: the ToE's
exact content is **constraints + labels (global topology)**, nothing else.

## Why this matters

The constraint-first result now has **two independent foundations**:

1. **Differential** — Darboux (no *local* fingerprint).
2. **Algebraic** — Weyl's FFT (no *duality-invariant* fingerprint, only the tadpole).

Two proofs from two branches of mathematics, landing on the same sentence. This is the
Rule of Three applied to the *foundations* of the result rather than to a measurement: a
claim is stronger when independent theorems force it. Darboux is the local half; the FFT
is the algebraic half; together they pinpoint the surviving exact structure as **global
topology + the constraint**.
