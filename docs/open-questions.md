# Open questions and honest limits

Ranked roughly by "what must be true for the program to have legs."

## 1. The measure problem (L6) — verification ≠ selection

The deepest, and the one PACLAND does **not** solve. Even a fully verified vacuum class
certifies *membership* in "looks-like-our-universe"; it does not explain *why* this
vacuum. A landscape measure (cosmological dynamics, eternal inflation, or a
first-principles selection) is a separate physics problem.

- Open: can the measure itself be cast as a hypothesis class and PAC-verified against
  CMB / large-scale-structure data? If yes, PACLAND gains a real selection layer; if no,
  the project is honest only as a *characterization* tool, not a *unification* tool.

## 2. The learnability conjecture — VCdim of `compactification → observables`

This is the single governing question (see `verification.md` §5). It is worth stating as
a conjecture:

> **Conjecture.** The concept class `C` of observable-prediction functions induced by
> flux vacua has *finite, modest* VC dimension — i.e. the compactification→observables
> map is efficiently learnable, hence evolvable.

- If **true**: L4's evolutionary search has provable guarantees; the landscape is
  *navigable*.
- If **false**: no search can find our vacuum, a negative result about the whole
  landscape program.

Either way, it is testable on small subclasses (the IIB flux corner in `encoding.md`)
without touching 10⁵⁰⁰.

## 3. Imperfect-oracle formalism

`verification.md` §3 treats the oracle bias `β` as a pointwise bound. Reality: `β` is a
random variable (the solver's error varies across observables and is correlated with
them), and the oracle's own systematic error is *not* independent of `D`.

- Open: rigorous composition of the sampling bound with a *distributional* oracle-error
  model — i.e. the two-level bound with `β` as a random variable carrying its own
  confidence, not a constant. This is a concrete, publishable piece of work and the most
  likely first paper out of the project.

## 4. The choice of `D` is a scientific commitment, not a technical detail

`D` (the measure over observables) defines what "close to our universe" *means*. It is
not given by the physics. Choosing it is choosing which observables are load-bearing
(Λ? gauge group? a specific mass ratio?) and with what weight.

- Open: an explicit, default `D`, with the sensitivity of every certificate to `D` made
  visible — a certificate should say "this vacuum is (ε,δ)-close *under this observable
  measure*," and the measure must be a named, critiquable object.

## 5. What "unified" means as a falsifiable claim

Under the PAC framing, "unified string theory" decomposes into two claims, only one of
which is PACLAND's:

1. **Existence**: there is a vacuum class observationally indistinguishable from ours
   (PAC-verifiable — PACLAND's job).
2. **Selection**: a measure assigns that class weight ~1 (the physics job, L6).

- Open: phrase claim (2) as a falsifiable prediction. If no measure can be PAC-verified,
  the honest conclusion is that string theory is *unable* to select — which is itself a
  significant statement about the theory's scientific status.

## 6. Known traps (self-imposed honesty rules)

- **Never call a surrogate "verified."** A learned fast-evaluator that cannot emit a
  certificate is a speedup, not a verification result.
- **Never inflate the class with redundancy.** Un-quotiented SL(2,ℤ) duality makes the
  same vacuum count many times and corrupts the VC-dimension estimate.
- **Never report oracle output without its error model.** A number without a bias bound
  is a fiction in this framework.
- **Never let "green search" read as "found it."** L4 returning a high-fitness vacuum is
  a candidate for L3, not a result; L3 is the only thing that emits a certificate.

## 7. Hardest-to-defend assumption

The framework assumes the `compactification → observables` map is a well-defined
*function* one can sample. It is not, in two ways:

- The oracle is stochastic and biased (addressed in §3).
- The "true" target `c*` is known only through *one* realization — our universe — so
  `D` cannot be estimated from a distribution of universes; it is stipulated (§4).

Both are survivable as long as they stay *named* as assumptions rather than hidden in
the machinery.
