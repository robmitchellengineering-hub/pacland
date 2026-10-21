# Climate observable measure — the candidate `D` for the deficit

The pacland deficit needs a **finite observable measure** `D`: the list of quantities
that define "close to reality." For string theory it was the Standard Model's ~19 free
parameters; for climate this is the candidate set below. **A quantity counts toward the
deficit `m` only if it is simultaneously measured + computable + validated**; everything
else is extrapolated and earns no certificate term.

Status tags are **proposals to verify, not assertions** (Rule of Three applies: each
"validated" claim needs evidence — model-vs-observation on the historical record — before
it counts). `TO-VERIFY` marks the ones I have not yet confirmed against a source.

---

## Global state (the strongest tier — measured, computed, and validated on the record)

| observable | measured | computable | validated | status |
|---|---|---|---|---|
| Global-mean surface temperature (GMST) | HadCRUT5 / GISTEMP / Berkeley Earth | all GCMs output `tas` | CMIP reproduces historical warming | ✅ counts |
| Top-of-atmosphere energy imbalance (EEI) | CERES + Argo | GCMs output net TOA flux | models vs CERES within published range | ✅ counts |
| Ocean heat content (0–2000 m) | Argo | GCMs output | reproduces the observed uptake | ✅ counts |
| Global-mean sea level (GMSL) | tide gauges + satellite altimetry | GCMs + ice-sheet modules | reproduces historical rise | ✅ counts (partial: ice-sheet term lags) |

## Large-scale patterns (measured + computable; validation is uneven)

| observable | measured | computable | validated | status |
|---|---|---|---|---|
| Arctic sea-ice extent | NSIDC satellite | all GCMs | models historically *underestimated* the decline | ⚠️ partial |
| AMOC strength | RAPID array (2004–) | GCMs | short record; models spread wide | ⚠️ partial (TO-VERIFY) |
| ENSO amplitude / indices | NINO3.4 etc. | GCMs | realism varies widely across models | ⚠️ partial |
| Global precipitation & pattern | GPCP / reanalysis | GCMs | known tropical/precip biases | ⚠️ partial |
| Ice-sheet mass balance (GrIS/AIS) | GRACE/-FO | ice-sheet modules | models lag observed acceleration | ⚠️ partial |

## Extremes (the least validated — largely extrapolated)

| observable | measured | computable | validated | status |
|---|---|---|---|---|
| Heat-wave frequency/intensity | station + reanalysis | GCMs (index-based) | weak; attribution, not projection | ❌ extrapolated |
| Extreme precipitation | gauge + reanalysis | GCMs (coarse) | convection-permitting only recently | ❌ extrapolated |
| Tropical-cyclone intensity | best-track archives | needs high-res | very weak | ❌ extrapolated |

---

## How this splits along the constraint-first line (the point of the exercise)

- **Constraints (the reliable content):** the energy budget (`EEI = net TOA flux`), the
  water budget, the carbon budget — conservation laws a model must satisfy; plus
  **emergent constraints** (observation-conditioned bounds). These are what a model
  *forbids*, and they are where the guard-suite will live.
- **Labels (handed, not predicted):** the forcing trajectory (CO₂/CH₄ concentration is a
  *scenario input*, not a model output), grid/resolution, the model family. Analogous to
  pacland's topological labels `h¹¹, h²¹`.
- **Parameters (the free values):** equilibrium climate sensitivity (ECS), cloud
  feedbacks, aerosol forcing. ECS is the canonical climate example of *"the theory does
  not predict the value"* — it is inferred, not directly measurable, and is the thing the
  40-year range (1.5–4.5 °C) is about.

## Next

- Verify each `⚠️`/`✅` tag against a source (the fan-out's angle-4 agent is closest;
  confirm independently before the deficit report counts anything).
- The deficit report will count `m` from this table and attach the `1/√m` radius to one
  concrete projection target (chosen from the gap analysis).
