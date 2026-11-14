# STRATA (NVIDIA) — the km-scale emulator, reference-fidelity is not reality-fidelity

Status: **computed and guarded** — `src/pacland/climate/strata_fidelity.py` +
`tests/test_climate_strata_fidelity.py` (13 tests, green). This is the ACE
worked example (`docs/climate-ace-report.md`) applied one resolution tier up: to
the first storm-resolving AI climate emulator.

## The finding, in one sentence

> **STRATA's "realistic km-scale dynamics" is a claim about a model's agreement
> with *another model* (SCREAM), not with the Earth — and its headline number is
> *throughput*, not fidelity: 48 sim-days/MWh measures how cheaply it reproduces
> SCREAM, not how close either is to the climate. Worse, the released checkpoint
> emits no top-of-atmosphere radiative flux, so the Earth energy imbalance (EEI)
> — the one diagnostic the CMIP6-drift finding turns on — cannot even be computed
> from it.**

## What STRATA is

STRATA (Storm-resolving Tile-based autoRegressive Atmosphere Transformer,
[arXiv:2606.31248](https://arxiv.org/abs/2606.31248), NeurIPS 2026) is NVIDIA's
first autoregressive AI emulator of global *storm-resolving* atmosphere. It was
trained on **17 days** of SCREAM physics-model output at **4.9 km** (~25M grid
cells, sampled every 10 minutes) and produces stable 24-hour global rollouts.
Code: [NVlabs/STRATA](https://github.com/NVlabs/STRATA); weights:
[huggingface.co/nvidia/strata](https://huggingface.co/nvidia/strata).

| fact | value | source |
|---|---|---|
| parameters | **331,664,906** (~332M) | `config.json` |
| grid | cubed-sphere ne1024pg2 (6 × 2048²) | `channels.json` |
| output variables | **7 prognostic + 3 diagnostic**, 4 forcing | `channels.json` |
| vertical levels | **24** (SCREAM model levels 8–31) | `train_config.json` (`level_start` 8, `level_end` 32) |
| training data | 17 days @ 4.9 km, 10-min sampling | abstract |
| energy | **48 sim-days/MWh (~50× SCREAM)**; 741 sim-days/day @ 512 H100 | abstract |

## The two-level certificate (what "verification" must mean)

A climate projection is verified only if the bound holds:

```
p_*  ≤  p̂_g  +  p̂_e  +  radius_s  +  radius_e
```

| term | meaning | STRATA's paper computes it? |
|---|---|---|
| `p̂_g` | candidate-vs-oracle — **STRATA vs SCREAM** | computed — this is the "realistic km-scale dynamics" |
| `p̂_e` | oracle-vs-truth — **SCREAM vs the Earth** | not computed |
| `radius_s` | finite-sample term over the scored channels | small (n = 148 scalar channels) |
| `radius_e` | `sqrt(ln(1/δ_e)/(2m))` over the m reality-validated observables | not computed |

STRATA's published "verification" is `p̂_g` **alone** — a model against a model.
And its own abstract concedes the limit: *"large-scale biases develop with lead
time."* Reference-fidelity, admitted at km scale.

## The two findings the ACE report did not have

**1. The headline is throughput, not fidelity.** ACE's headline was *skill*
(">90% of tracked variables"). STRATA's is *efficiency* (48 sim-days/MWh, 50×
SCREAM). Efficiency is orthogonal to truth: an emulator that cheaply reproduces a
leaky reference is cheaply wrong. This is a new axis the certificate exposes —
the sector is learning to advertise *how fast*, not *how close*.

**2. The EEI hook is missing.** STRATA's released checkpoint emits **no
top-of-atmosphere radiative flux** — its diagnostics are
`precip_ice_surf_mass_flux`, `precip_liq_surf_mass_flux` and `ps` only. ACE at
least emitted TOA fluxes, so EEI was computable for it. STRATA cannot be checked
against the energy imbalance at all.

This matters because EEI is precisely the quantity the conservation finding
(`docs/climate-cmip6-drift.md`) shows **12 of 19** reference models get wrong.
STRATA is an emulator of one of those reference models (SCREAM), and the one
output that would reveal whether its reference leaks is absent from the emulator.

## The reality-fidelity count (the missing `m`)

Map STRATA's output onto the climate discipline's four anchors (GMST, EEI, OHC,
GMSL) and ask the deficit's question against the **Earth**:

| tier | `m` | `radius_e` (δ_e = 0.025) | meaning |
|---|---|---|---|
| **strict** | 0 | ∞ (vacuous) | STRATA's paper validates it against SCREAM, never any Earth observation |
| **anchor** | **1** | **1.358** | GMST (T_2m) only — EEI/OGC/GMSL not computable |
| **generous** | **2** | **0.960** | GMST + surface pressure (`ps`) |

Compare ACE: anchor **m = 2**, generous **m = 3** (ACE emits TOA fluxes). The
km-scale emulator is 20× finer than ACE and *verifies worse on the reality axis*:
it traded the observability of the energy imbalance for resolution. Finer is not
truer.

## Honest limits

- **Not a new measurement.** This re-expresses STRATA's own published facts
  (abstract + released `config.json` / `channels.json`) through the two-level
  certificate; it does not re-run STRATA or SCREAM. The contribution is the
  classification and the deficit number, not new model output — exactly as the
  ACE report.
- **The EEI gap is about the *released checkpoint's output*, not the physics.**
  SCREAM computes radiation; STRATA's released channel set does not emit it. The
  claim is "not computable from this emulator's output," not "SCREAM has no
  radiation."
- **`m` is a classification, not a re-analysis.** Each "validated" flag follows
  `docs/climate-observables.md`; the three-tier structure is the durable part.

## Reproduce

```sh
cd pacland
PYTHONPATH=src python3 -m pacland.climate.strata_fidelity        # the summary block
PYTHONPATH=src python3 -m unittest tests.test_climate_strata_fidelity -v   # 13 tests
```

References: STRATA, arXiv:2606.31248
([abstract](https://arxiv.org/abs/2606.31248),
[HTML](https://arxiv.org/html/2606.31248v1));
[NVlabs/STRATA](https://github.com/NVlabs/STRATA);
[huggingface.co/nvidia/strata](https://huggingface.co/nvidia/strata).
The two-level certificate is `docs/verification-formal.md` §1–§5; the ACE
predecessor is `docs/climate-ace-report.md`.
