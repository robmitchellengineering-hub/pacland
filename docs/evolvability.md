# L4 formalization — evolvability over the landscape

This formalizes the search layer. It maps Valiant's evolvability model onto the L1
genotype and the L3 certificate, and states the one theorem that governs whether L4 can
work at all.

Status: draft. Statements attributed to Valiant are marked; the mapping and the
two-level generalization are PACLAND's own.

---

## 1. Why Valiant's evolvability model, not a generic GA

A generic genetic algorithm is too weak a model to say anything rigorous, and too strong
in one respect — it assumes it can read each genotype's fitness exactly. PACLAND can do
neither of those things, and Valiant's model is the one that makes *exactly those
restrictions explicit*:

- **No exact fitness.** In Valiant's model, selection and mutation access the target
  only through *statistical queries* — aggregate statistics, never per-instance ground
  truth. That is literally how L4 works: L3 hands L4 a **certificate** (sampled rates
  `p̂_g`, `p̂_e` with confidence radii), never the true physics.
- **Provable limits.** The model comes with a theorem — *evolvable ⇒ learnable* — that
  turns "will search work?" into a checkable property of the hypothesis class.

So this is not an analogy bolted on for flavor; the model's constraints are the ones the
system already has.

## 2. Component mapping

| Valiant evolvability model | PACLAND |
|---|---|
| Instance space `X`, distribution `D` | Observable space, observable measure `D` |
| Representation class `R` (genotypes → functions) | Vacua `V` → hypotheses `h_v : X → Y` (L1 → L2) |
| Target concept / performance function | `c*` (our universe's physics); `Perf(v) = −p_*(v)` |
| Mutation neighborhood | L1 mutation operators: flux nudge, brane move, conifold transition |
| Population = distribution over genotypes | `P_t`, a distribution over vacua |
| Selection operator | Concentrate on higher `Perf`, read only via L3 certificates |
| Mutation operator | Sample a neighbor of `v` per the mutation graph |
| Statistical-query access | The L3 certificate (aggregate, sampled) |

## 3. The statistical-query restriction is real here, not imposed

This is the load-bearing observation. Valiant imposed the SQ restriction for biological
realism: an organism's fitness is not stamped on it, it is *estimated from experience*.
PACLAND inherits the same restriction by construction, because the performance of a
vacuum is the true error `p_*(v) = Pr[|h_v − c*| > ε]`, which:

1. cannot be computed (it depends on `c*`, see `verification-formal.md` §2), and
2. can only be *estimated* by sampling the oracle — which is precisely what the L3
   certificate is.

So L4 is not "a GA with a noisy fitness function"; it is an evolutionary process whose
only access to fitness is a statistical query. Valiant's theorem applies to it directly.

## 4. Formal setup

- **Genotype space** `V` — vacuum encodings (L1).
- **Representation** `h_v : X → Y` — the observables predicted by vacuum `v` (via L2).
- **Performance** `Perf(v) = −p_*(v) = −Pr[|h_v(x) − c*(x)| > ε]`. Higher is better;
  optimal is `Perf = 0` error.
- **Mutation neighborhood** `N(v)` — vacua reachable by one flux nudge, brane move, or
  conifold transition.
- **Population** `P_t` — a distribution over `V` at generation `t`.
- **Evolution step**:

```
P_{t+1}  =  Mut( Sel( P_t ) )
```

where `Sel` concentrates mass on higher-performing vacua and `Mut` re-spreads it over
their neighborhoods — both reading performance **only** through the L3 certificate.

### The two-level indirection (the PACLAND generalization)

Valiant's model assumes the performance function is *fixed* and that selection queries it
statistically. PACLAND has **two** layers of uncertainty stacked:

1. the oracle `Ô` differs from `c*` (systematic, `p_e`), and
2. the certificate estimates `p_g` from `n` samples (statistical).

This is *evolvability with an imperfect performance oracle* — a generalization of
Valiant's model, and the same imperfect-oracle theme that already appears in L3
(`verification-formal.md` §9.2). It is open question #3 of `open-questions.md`,
reappearing in the search layer. **The imperfect oracle is the through-line of the whole
system.**

## 5. The theorem that governs L4

**Theorem (Valiant, 2009, *Evolvability*).** If a concept class is evolvable in the
restricted model, then it is learnable in the corresponding statistical-query model.

**Contrapositive (what PACLAND actually uses).** If the class `C` of
vacuum-induced prediction functions is *not* SQ-learnable, then **no** evolutionary
search — with selection reading fitness only through certificates — can efficiently
converge to a near-optimal vacuum.

This is the gate. It is not a performance optimization; it is a *necessary-condition
test* on the whole search program, and it is checkable in principle on small classes.

## 6. The learnability conjecture, tightened

`verification-formal.md` §7 stated the conjecture in PAC/VC terms. The evolvability
theorem tightens it: the relevant model is **statistical-query learning**, which is
strictly weaker than general PAC learning (some PAC-learnable classes, e.g. parity, are
not SQ-learnable).

> **Conjecture (tightened).** The class `C = { h_v : v ∈ V }` has **polynomial SQ
> dimension** — i.e. it is SQ-learnable, hence evolvable.

- **True** ⇒ there exists an evolutionary procedure (with certificate-only access) that
  converges to near-optimal performance in polynomial generations.
- **False** ⇒ L4 is impossible as specified; the system degrades to L3-only
  (verify handed-to-you candidates), exactly as `verification-formal.md` §6 describes.

## 7. What L4 guarantees, and what it does not

| Guarantees | Does not guarantee |
|---|---|
| Convergence to a vacuum with near-optimal *performance* (close to `c*` under `D`) | Convergence to **the** vacuum (uniqueness is L6's problem, not L4's) |
| Polynomial resource bounds *if* the conjecture holds | Anything at all if the conjecture fails |
| A principled cost model (generations × certificate cost) | Selection of a *measure*; that is selection, not search |

The distinction matters: L4 can deliver a certified near-optimal vacuum *class* and still
have said nothing about *why* that class — that remains the L6 hole.

## 8. Landscape-specific obstacles (why this is hard even if learnable)

1. **Mutation-graph connectivity.** Is `V` connected under the three mutation
   operators? Conifold transitions may or may not connect the relevant nodes; if the
   graph is disconnected, evolvability is relative to each component, and the target
   vacuum must lie in the component reachable from the initial population.
2. **The discretuum / chaotic sensitivity.** Flux vacua are famously sensitive —
   small flux changes can move Λ discontinuously. `Perf` is a jagged function over `V`,
   so no smooth-gradient intuition survives. Valiant's model needs no gradient, which is
   precisely why it is the right one here.
3. **Neutrality and redundancy.** Un-quotiented SL(2,ℤ) duality (`encoding.md` §4)
   creates plateaus of identical fitness; unmodeled, these inflate effective class size
   and wreck the SQ-dimension estimate.
4. **Non-local jumps.** A conifold transition changes topology — it is a *jump* in the
   mutation graph, not a local step. Valiant's model admits arbitrary neighborhood
   structure, but the analysis must account for it; the transition operator is where the
   "landscape as graph" picture of `encoding.md` §3 becomes load-bearing.

## 9. Open items specific to L4

1. **Formalize "evolvability with an imperfect performance oracle."** Generalize
   Valiant's model so the performance function is itself only statistically estimable
   with systematic error (`p_e`), and re-derive the evolvable⇒learnable implication
   under that weakening. This is the most publishable item and the natural joint of L3
   and L4.
2. **Measure the SQ dimension** of `C` on the IIB flux corner — the empirical attack on
   the tightened conjecture.
3. **Characterize mutation-graph connectivity** on a small subclass: is the target
   vacuum in the same component as a "reasonable" initial population?
4. **Selection operator choice** under certificate uncertainty: how should `Sel` weigh
   a vacuum whose certificate has a wide confidence radius (few samples) versus a narrow
   one? This is a bandit problem, and it is the L4 analogue of L3's sample-cost tradeoff.

## 10. Relation to the other layers

- **L1** supplies `V` and `N(v)` (§4).
- **L3** supplies the certificate that *is* L4's statistical-query access (§3).
- **L5** (educability) is what L4 becomes when the population retains and reuses verified
  knowledge across generations rather than mutating blind — the ecorithm upgrade.
- **L6** is untouched by all of this: L4's optimum is "near `c*`", not "selected by a
  measure."
