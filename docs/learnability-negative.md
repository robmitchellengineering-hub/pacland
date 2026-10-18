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

**Refinement (2026-10-18, prior-dependence caught).** The single-coordinate
correlation above is robust, but the *ridge-on-quadratic* CV r is **prior-dependent**:
on flux bounded to [−5, 5] (root-find sampling), `log|W0|` gives r = 0.10 (uniform);
on ISD Gaussian flux (range [−46, 52]), the same observable gives r = 0.62. The cause
is a *weak scale-dependence*: `log|W0|` correlates with the D3 tadpole at only
r = 0.35, which is invisible when the flux range is narrow and visible when it is
wide. This does **not** overturn the result — `log|W0|` is still log-uniform in
distribution (CDF R² = 0.87–0.92) and still has insignificant mutual information
(z ≈ 1.95) — but it fixes the wording: the robust claim is *zero mutual
information*, not *zero ridge r*. The ridge r is model- and prior-dependent; the
MI is the information-theoretic quantity that matters for Valiant's theorem.

## 3. Valiant's contrapositive (2009)

Valiant's evolvability theorem: **evolvable ⇒ learnable.** Contrapositive:
**not learnable ⇒ not evolvable.**

**CORRECTION (2026-10-19, found by the joint test).** The premise "flux → W0 has
zero mutual information" is FALSE as stated. The MI measured here is the max over
*single* flux coordinates (the naive binned estimator, z ≈ 1.95), which is blind to
multi-coordinate structure. The *joint* test (ridge on the full quadratic basis) is
not blind, and it shows W0 is **weakly-to-moderately learnable** — r ≈ 0.62 on the
natural ISD measure (flux range [−46, 52]), r ≈ 0.10 only when flux is artificially
bounded to [−5, 5]. So `flux → W0` is *not* zero-information; it carries a weak
quadratic structure. The contrapositive therefore does **not** apply as originally
claimed: the "not evolvable" conclusion is **not established by the learnability
route**.

## 4. Conclusion — corrected

The robust part and the flawed part must now be separated:

> **Robust:** W0 is log-uniform in distribution (CDF R² = 0.87–0.92), so small W0
> is exponentially *rare* — the KKLT tuning problem is a *rarity* problem, not a
> search-with-gradient problem.
>
> **Corrected (was wrong):** `flux → W0` is not zero-information; it is weakly
> learnable (r ≈ 0.6) through multi-coordinate quadratic structure. The Valiant
> contrapositive therefore does not prove "not evolvable." Any future statement of
> this result must drop the learnability argument and rest on rarity alone.

This does **not** rescue search: rarity is a measure fact and remains. It corrects
the *argument*, not the physics. The honest status of "W0 not evolvable" is now
**open** (needs a rarity-based or a proper joint-MI argument), and this doc should
be read as a measurement of log-uniformity plus an explicit retraction of the
zero-information premise.

## 5. What it means (the honest payoff)

- **The rarity result survives.** W0 is log-uniform, so small W0 is exponentially
  rare — the KKLT tuning problem is real, and it is a *measure* fact independent of
  any learnability claim.
- **The learnability argument is retracted.** "flux → W0 is zero-information" was a
  single-coordinate artifact; the joint test shows weak learnability (r ≈ 0.6). So
  "not evolvable" no longer follows from Valiant's theorem, and any claim to that
  effect must be dropped or re-derived from rarity alone.
- **The lesson is methodological.** A single-coordinate MI is blind to
  multi-coordinate structure; the joint (ridge-quadratic) test is the one that must
  gate any "random vs. structured" claim. The tadpole (r = 1.0) is the positive
  control that proves the joint test works, which is exactly what exposed this.

## Limits (named, not hidden)

- Linear correlation misses nonlinear structure; the independence claim rests on
  Denef–Douglas, with the correlation as *confirmation*, not proof.
- `g_s` is only weakly supported (1.6σ); `W0` is the robust case.
- Scoped to the IIB flux corner; the full landscape is out of reach of any single sample.

## Where this lives

- `scripts/measure_flux_learnability.py` — rank + correlation measurement.
- `src/pacland/selection.py` — the KS/typicality tools to certify uniformity next.
- `docs/evolvability.md` §5–6 — the theorem this result applies.
