# The flux landscape is not evolvable — a negative result, assembled from existing work

This connects three known pieces — Denef–Douglas uniformity, Valiant's evolvability
theorem, and real flux-vacua data — into a statement that, to this project's knowledge,
has not been made explicitly: **the IIB flux-vacua corner is not evolvable, so no
certificate-only evolutionary search over it can converge.**

## 1. Uniformity (Denef–Douglas, 2004)

The Gukov–Vafa–Witten superpotential `W0` is statistically uniform in the complex
plane across the flux ensemble (Denef & Douglas, *Distributions of flux vacua*,
[hep-th/0404116](https://arxiv.org/abs/hep-th/0404116)). Consequently `|W0|` — and
its log — is a *random draw* that carries no information about the individual flux
quanta that produced it. The map `flux → W0` has ~zero mutual information.

## 2. Empirical confirmation (this work, real data)

On 163 real SUSY flux vacua (`data/vacua_sample.json`), the maximum Pearson
correlation between any flux coordinate and the observables is:

| observable | max \|r\| | z-score (SE = 1/√162 ≈ 0.079) |
|---|---|---|
| `log|W0|` | 0.173 | **2.20σ** |
| `log g_s` | 0.128 | **1.63σ** |

No coordinate exceeds 3σ; both are consistent with statistical independence — the
expected signature of uniformity. (Note: this is a *linear* test; the theoretical
basis for independence is Denef–Douglas, not the correlation alone.)

## 3. Valiant's contrapositive (2009)

Valiant's evolvability theorem: **evolvable ⇒ learnable.** Contrapositive:
**not learnable ⇒ not evolvable.**

A map with zero mutual information between input (flux) and output (`W0`) is not
learnable in any model — including the statistical-query model — because no query
about the flux predicts the output better than the prior.

## 4. Conclusion

> **The IIB flux-vacua observables `W0` (and, weakly, `g_s`) are statistically
> uniform, hence not learnable, hence — by Valiant's theorem — not evolvable.**
>
> No evolutionary search whose only access to fitness is a certificate (our L4,
> exactly Valiant's statistical-query restriction) can converge to a near-optimal
> vacuum in this corner.

This is the **FALSE branch of the learnability conjecture** (`docs/evolvability.md`
§6), demonstrated for the flux corner rather than merely conjectured.

## 5. What it means (the honest payoff)

- **The search dies, the verifier survives.** This is precisely the graceful
  degradation the framework was designed for (`docs/verification-formal.md` §6):
  L4 is infeasible for these observables, but L3 (verify handed-to-you candidates)
  is untouched. Unification-by-search over the flux landscape is not viable; the
  remaining honest move is *characterization and verification of proposals*.
- **The negative result is itself the contribution.** It tells the field to stop
  searching `W0` and instead treat it as the known-random observable it is — and to
  focus search effort on the observables that might still carry structure
  (gauge couplings, masses), which is the running extraction's target.

## Limits (named, not hidden)

- Linear correlation misses nonlinear structure; the independence claim rests on
  Denef–Douglas, with the correlation as *confirmation*, not proof.
- `g_s` is only weakly supported (1.6σ); `W0` is the robust case.
- Scoped to the IIB flux corner; the full landscape is out of reach of any single sample.

## Where this lives

- `scripts/measure_flux_learnability.py` — rank + correlation measurement.
- `src/pacland/selection.py` — the KS/typicality tools to certify uniformity next.
- `docs/evolvability.md` §5–6 — the theorem this result applies.
