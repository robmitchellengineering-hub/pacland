# The running-coupling lemma per scheme — what the harvest pulls for each

Status: 2026-11-22, the second harvest. The specific mathematical statement each renormalisation
scheme must produce to carry `e^{−cβ}` — the running coupling — and what it shares across schemes.

## The common core (all four schemes carry the same structure)

The `e^{−cβ}` shape is **dimensional transmutation**: the running coupling `g²(μ)` obeys the beta
function `β(g) = −b₀ g³ − …` (`b₀ = 11N/48π²`), so the scale

```
Λ = μ · e^{-1/(2 b₀ g²(μ))}       (log m ~ -c·β,  c = 12π²/(11·N)-class)
```

is generated, not put in by hand. Every scheme below is a *different way to exhibit this same
exponential*; the specific lemma is the one place in that scheme where the beta function enters.

## The specific lemma per scheme

| scheme | the specific lemma that carries `e^{−cβ}` | falsifier (what kills it) |
|---|---|---|
| **Polchinski flow** | the exact flow's integrated coupling obeys `g²(t) = g²/(1 + 2b₀ g² t)`, so the scale `Λ = μ e^{−1/(2b₀g²)}` emerges from the flow | the flow's scale not uniform in volume / not reaching `e^{−cβ}` |
| **block-spin / decimation** | the blocked coupling runs `β' = β + b₀ log 2 + …` per step; iterating `log m ~ Σ b₀ log 2 = c·β` | the iterated coupling not running (fixed point at a finite β) |
| **gradient flow / trivialising map (Lüscher)** | the flow at time `t` maps the measure to a Gaussian; the trivialising flow time `t* ~ ξ ~ e^{cβ}` (the flow-time scale is the correlation length) | no flow-time `t*` for which the measure is close to Gaussian (the trivialisation fails) |
| **constructive RG (Balaban)** | the multi-scale cluster expansion's scale-by-scale bound sums to `log m ~ −c·β` (each scale contributes the beta-function step) | the scale sum stops at a finite scale (no weak-coupling control) |

## What this tells the engine

The running coupling is **not four different problems — it is one structure (the beta function)
exhibited four ways.** The harvest's job is therefore to pull the *one estimate in each scheme* where
the beta function enters, express it as a candidate bound `c(β)`, and run it through
`bound_search.check_bound`. The falsifier for all four is the same: **does the scheme's scale reach
`e^{−cβ}` uniformly in volume, or does it stop at a finite coupling?**

The most concrete and recent of the four is the gradient-flow/trivialising-map lemma — Lüscher's
flow-time scale is the one with the cleanest lattice formulation (it is exactly the `t₀` scale we
already built), which is why the gradient-flow route is the natural first target for a real
estimate.
