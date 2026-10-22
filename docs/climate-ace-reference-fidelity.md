# The ACE worked example — reference-fidelity is not reality-fidelity

ACE (AI2 Climate Emulator, [arXiv:2310.02074](https://arxiv.org/abs/2310.02074)) is a
200M-parameter, autoregressive ML emulator of a 100-km global atmospheric model
(FV3GFS). Its headline claims: *"stable for 100 years, nearly conserves column moisture,
and faithfully reproduces the reference model's climate, outperforming a challenging
baseline on over 90% of tracked variables."*

The two-level certificate shows what that "verification" actually is:

```
p_*  ≤  p̂_g  +  p̂_e  +  radius_s  +  radius_e
```

- **p̂_g (candidate-vs-oracle)** — ACE-vs-FV3GFS. This is what ">90% of tracked
  variables" measures. It is **model-vs-model**.
- **p̂_e (oracle-vs-truth)** — FV3GFS-vs-the-Earth. This term is **never computed**, and
  for a 100-year projection it *cannot* be: the future has no ground truth.

So ACE's "verification" certifies a model against another model, not against the Earth.
The ">90%" is **reference-fidelity, not reality-fidelity**.

## The honest verdict

- ACE is an excellent **emulator** — it reproduces its reference well, and it is
  explicitly built so "physical laws such as the conservation of mass and moisture" can
  be evaluated. None of that is being disputed.
- But its *verification* is the candidate-vs-oracle term alone. The oracle-vs-truth term
  — is the reference model itself right against the Earth? — is absent, exactly as it is
  for every climate projection. The deficit applies: ACE's future run is extrapolation,
  not verification, and its "skill" is measured against a model, not the Earth.

## Why this is the citable point

A "skillful" AI climate model is not a "true" one. Skill is measured against a reference;
truth against the Earth; and the AI-emulator frontier currently checks only the first. The
two-level certificate is the thing that makes that distinction explicit, and it is the same
object the CMIP6 drift finding uses — applied one level up, to the models that will
*replace* the CMIP6 ensemble.
