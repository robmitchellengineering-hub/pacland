# Drug-discovery verification deficit — discipline #2 (playbook item #2)

Status: **computed and guarded** — `src/pacland/drugs/` + `tests/test_drugs_{deficit,guards}.py`
(11 tests, green). The reusable pacland machinery (`certificate.py`, `deficit.py`) is
imported unchanged; this file records the drug result and its honest limits.

## The headline, in one sentence

> **A screening campaign's decision surface is validated over only ~4 retrospective assay
> endpoints (`m = 4`, ≈68% radius) — and the prospective hit, the novel molecule you would
> actually synthesize, is extrapolation, not verification (`m = 0`).**

## The two-tier structure (why the novel molecule is the weak spot)

Same honest rule as climate: a *validation point* needs the model output O(x) **and** an
independent measurement c*(x) on the **same** compound. On a benchmark that pairing
exists (retrospective); for a novel molecule there is no assay yet.

| tier | what it covers | `m` | certificate radius (δ = 0.025) |
|---|---|---|---|
| **retrospective benchmark** | assay endpoints the model reproduces against measured labels | **4 of 10** | **0.679 (~68%)** |
| **prospective novel molecule** | the hit you would synthesize | **0 of 5** | **∞ (vacuous)** |

`radius = sqrt(ln(1/δ) / (2m))`; at `m = 4` that is ≈ 0.679. A 1% certificate needs
`m ≈ 18,000` simultaneously-measured endpoints — three orders of magnitude beyond any
benchmark.

## The m-count

The four that count (measured + computable + validated on the benchmark):

| endpoint | measured by | status |
|---|---|---|
| binding affinity | PDBbind (refined set) | ✅ validated |
| aqueous solubility | TDC | ✅ validated |
| hERG liability | TDC | ✅ validated |
| hepatic clearance | TDC | ✅ validated |

The rest — plasma protein binding, BBB penetration, metabolic stability, toxicity/
mutagenicity, synthesizability, cytotoxicity — are measured + computable but not
benchmark-validated to the same confidence, so they contribute nothing today. Full set:
`src/pacland/drugs/observables.py`.

## The two anchors (from the gap analysis)

- **Zhu et al. 2013** ([doi:10.1021/jm301916b](https://doi.org/10.1021/jm301916b)) — the
  field's own census: of 398 reported virtual-screening hits, **52% fail REOS, 18% are
  PAINS, and only 17% got direct-binding validation**. The "validated" retrospective hits
  were, in large part, artifacts — so even `m = 4` is the *optimistic* read.
- **Vander Meersche et al. 2025** ([Structure](https://hal.science/hal-05474189v1)) —
  AlphaFold's pLDDT, the field's most-used confidence score, is **not calibrated**: it
  conflates flexibility with uncertainty. The "confidence" that stands in for a
  certificate is a heuristic.

## The constraint guard-suite (the falsification half)

The field already runs forbidden-state filters as boolean heuristics; the guard-suite
wraps them as pass/fail, mutation-tested checks (`src/pacland/drugs/guards.py`):

| guard | what it forbids |
|---|---|
| `guard_total_charge_neutral` | a non-neutral molecule |
| `guard_valence_bounds` | over-valent atoms (e.g. pentavalent carbon) |
| `guard_lipinski` | > 1 rule-of-five violation (MW/logP/HBD/HBA) |
| `guard_synthesizable` | a RAScore above the synthesizability floor |

Each has a seeded-fault mutation test proving it goes red on the fault it exists to catch.

## Honest limits

- **"validated" ≠ "validated for a novel scaffold."** It means "reproduces the measured
  benchmark endpoint within tolerance." A novel molecule is a different claim with no
  assay, and the deficit is the *statement of that gap*.
- **`m = 4` is optimistic.** The Zhu 2013 census (18% PAINS, 52% REOS) shows even the
  retrospective tier is softer than it looks; tightening `m` makes the number worse.
- **This is a characterisation, not a predictor.** It says "you are here," not "this
  molecule will work."

## Reproduce

```
cd pacland && PYTHONPATH=src python3 -m pacland.drugs.deficit
PYTHONPATH=src python3 -m unittest tests.test_drugs_deficit tests.test_drugs_guards -v
```
