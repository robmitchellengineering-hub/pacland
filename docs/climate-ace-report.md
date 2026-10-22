# The ACE worked example — reference-fidelity is not reality-fidelity

Status: **computed and guarded** — `src/pacland/climate/ace_fidelity.py` +
`tests/test_climate_ace_fidelity.py` (7 tests, green). This is the citable
report the gap analysis flagged as the sharpest single finding
(`docs/climate-gap-analysis.md` §6, target 2).

## The finding, in one sentence

> **ACE's "skillful" is a claim about a model's agreement with *another model*,
> not with the Earth — and its reality-fidelity term is, at best, a ~78%
> tolerance over 3 observables (or ~96% over the 2 headline observables an
> atmosphere-only emulator can even reach), not the ">90% skillful" it reports.**

## The two-level certificate (what "verification" must mean)

A climate projection is verified only if the bound holds:

```
p_*  ≤  p̂_g  +  p̂_e  +  radius_s  +  radius_e
```

| term | meaning | ACE's paper computes it? |
|---|---|---|
| `p̂_g` | candidate-vs-oracle — **ACE vs its reference GCM (FV3GFS)** | computed — this is the ">90% of tracked variables" |
| `p̂_e` | oracle-vs-truth — **the reference GCM vs the Earth** | not computed (and for a 100-year run, cannot be) |
| `radius_s` | finite-sample term over the scored channels | small (n = 44 channels) |
| `radius_e` | `sqrt(ln(1/δ_e)/(2m))` over the m reality-validated observables | not computed |

ACE's published "verification" is `p̂_g` **alone** — a model against a model. The
`p̂_e` term (is the reference GCM itself right against the Earth?) is the whole
question for a climate model, and it is absent, exactly as it is for every
climate projection.

## The ">90%" claim, counted

ACE (arXiv:2310.02074) reports "outperforming a challenging baseline on over
90% of tracked variables." Its Table 1 and Appendix E give the exact numbers:

| fact | value | check |
|---|---|---|
| output channels | **44** = 34 prognostic + 10 diagnostic | `channel_summary()` |
| ">90% of tracked" | **41/44 = 93.2%** beat a *2×-coarser FV3GFS* baseline | Appendix E: "41 out of 44 output variables" |

Every one of the 44 channels is scored against a **model** — the FV3GFS reference
or the coarser FV3GFS baseline. "Reference" and "baseline" are both models, so
"skillful" here means *closer to the reference GCM than the coarser GCM is* —
reference-fidelity, never reality-fidelity. That is the sentence the two-level
certificate makes rigorous.

## The reality-fidelity count (the missing `m`)

Map ACE's 44 channels onto physical observables and ask the pacland deficit's
question against the **Earth** (not the reference model): measured (an
independent observation `c*` exists) + computable (ACE outputs `O(x)`) +
validated (reproduces the historical record within tolerance). The standard is
`docs/climate-observables.md`; the table is `ACE_REALITY_OBSERVABLES`.

Three honest tiers:

| tier | `m` | `radius_e` (δ_e = 0.025) | meaning |
|---|---|---|---|
| **strict** | 0 | ∞ (vacuous) | ACE's own paper validates it against FV3GFS, never against any Earth observation |
| **anchor** | 2 | **0.960** | GMST (T7) + EEI (TOA fluxes) — the two of the four headline climate observables an atmosphere-only model can reach |
| **generous** | 3 | **0.784** | GMST + EEI + surface pressure (the best-observed atmospheric field) |

ACE is **atmosphere-only**, so it structurally cannot output the other two of the
climate discipline's four anchors — ocean heat content (OHC) and global-mean sea
level (GMSL) — they are "measured but not computable by ACE." Even granting ACE
full credit for its reference GCM's Earth-validation (the generous tier), the
reality certificate radius is **~78%**, a tolerance on 3 observables — not the
">90% skillful" headline, which was model-vs-model all along.

## Why this is the citable point

- **A "skillful" AI climate model is not a "true" one.** Skill is measured
  against a reference; truth against the Earth; the AI-emulator frontier
  currently checks only the first. The two-level certificate is the thing that
  makes that distinction explicit.
- **It applies one level up from the CMIP6 drift finding.** The conservation
  guard (`docs/climate-cmip6-drift.md`) shows the *reference models themselves*
  leak energy (12 of 19). ACE's verification is fidelity to one of those models.
  Reference-fidelity to a leaky reference is fidelity to a defect.
- **It names the gap the whole sector inherits.** Oreskes et al. 1994 ("earth
  models can never be verified, only falsified") stood for 30 years without a
  number. The deficit `m` — here 2–3 for the sharpest current emulator — is that
  number, and it says the field's "verification" certifies a model against
  another model, not against the Earth.

## Honest limits

- **Not a new measurement.** This re-expresses ACE's own published claim (44
  channels, 41/44 vs baseline) through the two-level certificate; it does not
  re-run ACE or FV3GFS. The contribution is the classification and the deficit
  number, not new model output.
- **`m` is a classification, not a re-analysis.** Each "validated" flag follows
  `docs/climate-observables.md` (the four headline observables are validated on
  the record; the rest are measured-but-not-validated or not measured). A
  different discipline would re-derive `m` from its own observable set; the
  three-tier structure is the durable part.
- **The strict tier is the truth, the generous tier is the concession.** ACE is
  an *emulator* — "of course it is validated against its reference, not the
  Earth" is the obvious reply. The generous tier (`m = 3`, ~78%) is what survives
  *even after* that objection, so it is the headline, not the strict tier.

## Reproduce

```sh
cd pacland
PYTHONPATH=src python3 -m pacland.climate.ace_fidelity       # the summary block
PYTHONPATH=src python3 -m unittest tests.test_climate_ace_fidelity -v   # 7 tests
```

References: ACE, arXiv:2310.02074 ([abstract](https://arxiv.org/abs/2310.02074),
[HTML](https://arxiv.org/html/2310.02074v2)); the two-level certificate is
`docs/verification-formal.md` §1–§5.
