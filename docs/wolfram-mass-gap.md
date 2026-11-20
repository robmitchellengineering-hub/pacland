# Wolfram methodology → the mass gap (what transfers)

**Status: research note, not a physics claim.** Stephen Wolfram's *Wolfram Physics Project* is a
speculative framework, not established physics — but one methodological point in it transfers to the
mass-gap work and changes how the machine should attack the problem. This is that point, stated once.

## The Wolfram methodology (physics from computation)

1. The universe is a **hypergraph** that evolves by simple rewriting rules.
2. **Causal invariance** (different rewrite orders give the same causal structure) → special/general
   relativity *emerge*, not assumed.
3. The **multiway system** (all possible histories) → the branchial space is momentum space → quantum
   mechanics *emerges*.
4. **Gauge invariance** emerges from the local freedom in the rewriting (Gorard/Wolfram) — Yang–Mills
   structure is *derived*, not postulated.
5. **Computational irreducibility** — many questions about the system have no closed-form answer; they
   can only be answered by running the computation.

## The point that transfers to the mass gap

**The mass gap may be computationally irreducible — and that is a *classification*, not a failure.**

SEXTANT already classifies every claim FORCED / FREE / IMPOSSIBLE (kernel-checked, no `sorry`). Wolfram
adds a fourth class the referee does not yet name: **IRREDUCIBLE** — a claim that is *computable*
(a lattice/falsifier can decide it at each finite lattice size) but has **no closed-form derivation**.
The Clay formulation asks for a *proof*; Wolfram's point is that the honest object may only be a
*computational demonstration*: the mass gap is FORCED only in the sense of "the lattice keeps forcing
`m/√σ → 3.2` as N → ∞", not "a finite chain of symbols derives it".

Concretely, this is what it means for the machine:

1. **Do not wait for a closed-form bound.** The right product is the *convergence record*: the
   falsifier-first lattice sequence (`mass_gap_falsifiers`) *is* the argument, not a fallback.
2. **Confinement = topological gauge defects.** Wolfram's picture identifies confinement/the gap with
   the topological structure of the discrete gauge field (vortex/monopole-like defects). That is
   exactly the mechanism space the machine already falsifies — center-vortex condensation, monopole
   condensation, bulk transition. The framework says those are *the right place to look*, not a dead end.
3. **SEXTANT should name IRREDUCIBLE.** A claim that survives every lattice falsifier at every N tested
   but has no `sorry`-free Lean proof is not "FREE" (it is not a free parameter) and not "FORCED" (it
   has no closed certificate) — it is **IRREDUCIBLE**, and the honest record is the convergence
   evidence, not a pretence of a theorem.

## The honest falsifier for this note

> If the mass gap turns out to have a short closed-form proof after all, then the "IRREDUCIBLE" class
> is empty for this problem and this note overstates Wolfram's transfer. The point stands regardless:
> the machine should **record convergence evidence**, and not discard a claim because a `sorry`-free
> Lean certificate is not yet in reach.
