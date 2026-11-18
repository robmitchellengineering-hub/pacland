# Strip-mine synthesis — what the committee's construction changes in our picture

Five agents mined `/tmp/OpenAI-YM` (9,477 files). The three findings that genuinely change things:

## 1. Gap 1 is refined — the proof already pins the slope (the public statement just hides it)

The construction has `Gauge.slopeConstant := 11·casimir/(24π²)` (`YM/Gauge/Colors.lean:184`),
`casimir_pos` (`casimir_pos : 0 < G.casimir`, proved from `G.Simple` alone, `Casimir.lean:160`), and
`slopeConstant_pos`. The running coupling machinery (`RG/History.lean`) has `Transfer` (the one-loop
recurrence `|Δβ − slopeConstant·log(block)| ≤ drift`) and `Running` (the actual β tracks it). And
`Running.slope : slopeConstant = 2·b₀` with `b₀ = 11·C_A/(48π²)`.

**So the committee's proof uses the correct, Casimir-pinned slope `11·C_A/(24π²)`; only the PUBLIC
`WilsonRegularity.running` weakens it to "some positive slope".** Our `WilsonRegularityPinned` draft
(slope = c·C₂) is therefore not a new strengthening — it is *what the proof already establishes*, with
`c = 11/(24π²)`. The fix is to surface `slopeConstant` in the public statement, not to add new content.

## 2. The crossover is precisely located — the RG map is proven, the estimates are not

- **Proven exact:** `RG/StepData` (one coarse-graining step, fine → coarse) with `push`/`push_integral`
  (`RG/Block.lean`, `RG/Push.lean`) — but it is a pushforward on **observables** only.
- **Asserted, not proven:** the action-level flow `History.Selected`/`Transfer`/`Running`
  (`RG/History.lean`), and the finite-scale estimates — `Station.Admissible`, `Cells.CellHyp`,
  `Grill.Coarse`/`Credit`/`Furnace`, `Annulus.NodeBound`, `HorizCalc`. Each is documented "NO existence
  proof" / "physical hypothesis" / "outstanding RG question".

This is the exact crossover rung: prove the finite-scale estimates + the action-level RG trajectory from
the lattice Wilson measure. The machinery (`Grill.lean` explicitly withholds a positivity + mass-gap/cluster
input) is where the mass gap would enter.

## 3. The mass gap is untouched, but the right setting exists

`YM/Next/ROTATIONS/` (Mass/Mode/Tunnel/Cross) are all **upper bounds** on test-function profiles — a
`Budget a` means `‖u n‖ ≤ C·exp(a·n)` eventually, "never a lower gap bound". There is no spectral-gap
statement; the README's "mass gap out of scope" is accurate. However, `YM.Boundary.Fields` owns the
common-domain Poincaré + the projection-valued measure, and `Semigroup.descent` is present — exactly the
infrastructure `HasEnergyGap`/`HasMassGap` (from `MassGapSpec.lean`) needs. The missing rung is proving
the spectral measure has no support below `Δ > 0` on the vacuum complement.

## What this means for us

1. **Gap 1**: close it by surfacing `slopeConstant` in the public `WilsonRegularity` — the content already
   exists in the proof. Our draft's review question is answered: `IsSimple` ⟹ positive Casimir, proven.
2. **Crossover**: the target is now nameable — prove `Station.Admissible` + `CellHyp` + `Grill.Coarse` +
   `NodeBound` + `HorizCalc` and the `History.Selected` trajectory. These are the committee's declared
   hypotheses, and they are the genuine open rung.
3. **Mass gap**: state `HasEnergyGap` against `YM.Boundary.Fields`'s PVM and prove the spectral support is
   away from 0 — the untouched half, with the infrastructure now identified.
