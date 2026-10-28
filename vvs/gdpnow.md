# Valiant Verification certificate — Atlanta Fed GDPNow (GDP nowcast, US)

**Format:** `valiant-verification/named-gate@1`  
**Issuer:** Pacland / Valiant Verification  
**Issued:** 2026-10-28  
**Grade:** **VERIFIED**  
**Gates:** 5 of 5 pass  
**Verified:** yes

| gate | result | evidence | falsifier |
|---|---|---|---|
| `conceptual_soundness_is_the_forecast_a_model_at_all_or_an_accoun` | **pass** | Bridge-equation nowcast; beats the no-change null on MAE by 75% (1.26 vs 5.05 pp) | the bridge equations would not aggregate to a GDP path at all, and the MAE ratio would sit at or above 1 |
| `outcomes_analysis_does_it_beat_the_null_out_of_sample` | **pass** | 28 of 37 quarters, MAE ratio 0.25 (<1 = beats the null) | ratio >= 1.0, i.e. no better than carrying the previous quarter forward |
| `outcomes_analysis_is_that_skill_against_the_first_publication_or` | **pass** | Against the settled number it still beats the null: MAE ratio 0.31 on all 37 quarters, 0.75 excluding 2020 — the edge narrows but survives | a settled-number ratio above 1.0, or one that flips when 2020 is dropped |
| `data_quality_are_the_inputs_real_time_vintages_or_revised_histor` | **pass** | Real-time vintages (ALFRED) throughout; a vintage that post-dates the forecast is refused by guard_nowcast_predates_release | a fixture where the nowcast vintage post-dates the release — the guard would go red and the evaluation would be refused |
| `implementation_can_the_evaluation_go_red` | **pass** | Four guards, each mutation-proved: vintage ordering, shared benchmark vintage, first-publication target, units | each guard is mutation-proved: the seeded fault makes it read red |

**Producer:** Data: data/economics/gdpnow_vintages.json (ALFRED vintages); Script: python3 scripts/economics_gdpnow.py; Module: src/pacland/economics/gdpnow.py

## Limitations

- The advantage survives the settled-number target but narrows sharply: 0.25 against the advance estimate, 0.75 against the settled number excluding 2020.
- The evaluation uses one public dataset and one target definition; neither has been independently replicated outside this repository.
