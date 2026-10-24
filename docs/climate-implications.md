# Climate discipline — implications and where the work goes next

Status: **the synthesis, written down.** This is the "so what" of the climate
discipline's verified findings, plus the next-work roadmap with an explicit
compute-feasibility split. Numbers here are pulled from the guarded modules
(`deficit`, `cmip6_drift`, `ace_fidelity`, `ecs_model`, `trust_board`,
`reference_model`), never from memory.

## The bottom line

Running every model through the strictest checks we can build **does not change
the answer — it confirms the mainstream one, and shows why it is right.** The
models that actually conserve physics land at ~3 °C sensitivity and ~5 °C of
2100 warming on the current path — the IPCC consensus — reached by trust-gating
rather than averaging. That is an independent confirmation. The path there
exposed that most of the field cannot even conserve energy, and that is the
quantified defect nobody else has.

## The implications (five, in order of consequence)

### 1. Climate "verification" is mostly a category error
"Skillful" (ACE's 93%, every model's skill score) means **agrees with another
model**, not **right about the Earth**. 12 of 19 CMIP6 models **leak energy** —
broken physics, not a tunable bias — yet they are averaged into the projections
policy runs on. Oreskes' 30-year-old "you cannot verify a climate model" is now
a **number**: a 1% certificate needs ~18,000 validated observables; we have 4.
So "verified climate prediction" is, today, a misnomer — with a number saying
exactly how much.

### 2. Policy: sobering, and it cuts both ways
- **It lets nobody off the hook.** The one model that passes all three gates
  still projects **4.6–5.2 °C on SSP5-8.5**. Verification does not soften the
  warning; it sharpens it by deleting the untrustworthy models and confirming
  the trustworthy one.
- **It kills the "hot model" tail honestly.** The scary 5–6 °C ECS models are
  disproportionately the ones that leak energy. Dropping them on a physics basis
  (not a convenience basis) lands the ensemble at 2.7–3.1 °C.
- **It hands a decision-maker one sentence:** "The models that conserve physics
  say ~3 °C sensitivity and ~5 °C on this path; here is exactly why the other 38
  are excluded."

### 3. Spend on measurement, not simulation
The deficit says the bottleneck to a better prediction is **measured data, not
compute**. 68% → 1% certificate needs ~18,000 validated observables — that is
observational systems (ocean, ice, atmosphere), not a faster supercomputer or
another emulator. Money into "better models" is spending on the wrong wall.

### 4. AI climate models: a real, urgent caution
ACE's "100× faster" is real, but its "verification" is against a **reference GCM**
— itself a leaky model — never the Earth. The AI-emulator revolution is being
graded on the wrong target. Before these replace physics models in policy, they
need **reality-fidelity** checks, not reference-fidelity. The sector is not
hearing this yet.

### 5. The method is the asset, not the numbers
The same spine that found "the future cannot be verified" in string theory found
it in climate, and will find it in drugs, economics, AI. The reusable asset is
the **trust board** — per-model trust scores you can point at *any* quantity.
The numbers will move; the way we get the trustworthy number is what transfers.

### 6. The fix: we repair the model, not replace it
The conservation leak is a **fixable defect**, localized to the atmosphere-ocean
coupling, and the field's own repair — drift-correction — removes it. The
product is not "a rival climate model"; it is *"your model, analyzed, verified,
and fixed"*. See `docs/climate-repair.md` and
`src/pacland/climate/drift_correction.py`:

- **14 of 19 models leak** (energy/mass at the air-sea boundary), all correctable.
- **Correcting the leak changes the answer**: the strict three-axis gate collapses
  from 2 models (2.71 K) to the repaired 15-model, 13-family gate (**3.08 K**).
- **Honest boundary**: this corrects the global-mean drift; the spatial leak (the
  coupling) is the builders' deeper patch, and `leak_map()` hands them the spec.

## Where the work goes next — with the compute split

Rob's rule: **if we can do the compute, we do it and figure it out; if we
cannot, we name the wall and the way around it.** Every next step is tagged
with its compute requirement and its verdict.

- **#1 · GISS-E2.1 sea-level by 2100** (finish the board) — compute: fetch the
  full Nazarenko paper body. Verdict: **doable now** (no compute, a text fetch).
- **#2 · 2100 warming for the full trusted set** (14 models, not just GISS) —
  compute: compile per-model SSP warming from CMIP6 archives. Verdict: **doable**
  (a fetch + small table, no heavy compute).
- **#3 · Widen conservation to all 53 models** (trust board 17→53 with drift
  data) — compute: recompute energy/mass/salt drift from raw CMIP6 piControl
  zarr. Verdict: **doable — mesh job** (studio-linux; xarray/zarr/dask).
- **#4 · Second-source the drift to all 19** (the documented "natural next
  step") — compute: raw CMIP6 zarr recompute. Verdict: **doable — mesh job**,
  same toolchain as #3.
- **#5 · The citable climate paper** (deficit + drift + ACE + ECS + predictions)
  — compute: writing + the existing PDF renderer. Verdict: **doable now**.
- **#6 · The string-landscape h12≥5 sampling** (the physics frontier) — compute:
  JAXVacua on the mesh (~96 GB / speed problem). Verdict: **other discipline**,
  owned by `main`, not this branch.

### The walls, and the way around each (so "cannot" is never a stop)

- **Sea-level (#1):** *wall = unmeasurable-in-hand* — the number is in the paper
  body, not the abstract. **Move:** fetch the full text (the Crossref record
  exposed a full-XML text-mining URL).
- **Conservation widening (#3, #4):** *wall = intractable-on-Mac* — xarray/zarr
  are not installed here and the data is a streaming fetch. **Move:** it is a
  mesh job, not a Mac job — install the toolchain on studio-linux (a build task,
  per "no limitations on the Rob Mesh") and dispatch.
- **Running GISS-E2.1 or the full CMIP6 ensemble ourselves:** *wall = intractable*
  — supercomputer-scale, and not our goal. **Move:** use the published projections
  (what we already do); the verification we add is the value, not the simulation.

## What changes the answer (honest caveats)

- The strict gate collapses to **one family** (GISS); 2.71 K is one family's view.
- GISS's own ECS (2.9–3.0 °C) differs from the cross-model 2.71 K — method-dependence is real.
- The drift data covers 19 of 53 models; the other 34 are scored on two axes, not three.

None of that reverses the headline: **trust the conserving models, and the
answer is ~3 °C / ~5 °C — alarming, defensible, and it says the fix is
measurement, not more models.**

## The findings, linked (so every claim traces to its evidence)

- The deficit `m = 4`, radius ~68% — [climate-verification-deficit.md](docs/climate-verification-deficit.md)
- The conservation drift, 12/19 energy · 6/19 mass · 2/19 salt — [climate-cmip6-drift.md](docs/climate-cmip6-drift.md)
- The independent second source of the drift — [climate-drift-second-source.md](docs/climate-drift-second-source.md)
- ACE's reference-fidelity ≠ reality-fidelity — [climate-ace-report.md](docs/climate-ace-report.md)
- The trust-gated ECS, bracket 2.71–3.08 K — [climate-ecs-model.md](docs/climate-ecs-model.md)
- The per-model trust board, 14 trusted of 53 — [climate-trust-board.md](docs/climate-trust-board.md)
- The verified reference model GISS-E2-1-G — [climate-reference-model.md](docs/climate-reference-model.md)
- The 5-angle gap analysis that opened the discipline — [climate-gap-analysis.md](docs/climate-gap-analysis.md)
- The plain-English brief for non-experts — [climate-verified.md](docs/climate-verified.md)

## Reproduce the numbers

```sh
PYTHONPATH=src python3 -m pacland.climate.deficit
PYTHONPATH=src python3 -m pacland.climate.trust_board
PYTHONPATH=src python3 -m pacland.climate.ecs_model
PYTHONPATH=src python3 -m pacland.climate.reference_model
```
