# Model risk certificate — Atlanta Fed GDPNow (GDP nowcast, US)

**Issued:** 2026-10-28  
**Issuer:** Pacland / Valiant Verification  
**Grade:** **VERIFIED**

Beats the no-change null on 37 quarters of real-time vintages — 75% lower MAE against the advance estimate and 25% lower against the settled number, so the edge is not an artefact of targeting the first print.

| clause | question | what the evidence says | status |
|---|---|---|---|
| Conceptual soundness | Is the forecast a model at all, or an accounting identity? | Bridge-equation nowcast; beats the no-change null on MAE by 75% (1.26 vs 5.05 pp) | **satisfied** |
| Outcomes analysis | Does it beat the null out of sample? | 28 of 37 quarters, MAE ratio 0.25 (<1 = beats the null) | **satisfied** |
| Outcomes analysis | Is that skill against the FIRST publication or the settled number? | Against the settled number it still beats the null: MAE ratio 0.31 on all 37 quarters, 0.75 excluding 2020 — the edge narrows but survives | **satisfied** |
| Data quality | Are the inputs real-time vintages, or revised history? | Real-time vintages (ALFRED) throughout; a vintage that post-dates the forecast is refused by guard_nowcast_predates_release | **satisfied** |
| Implementation | Can the evaluation go red? | Four guards, each mutation-proved: vintage ordering, shared benchmark vintage, first-publication target, units | **satisfied** |

## Evidence

- Data: data/economics/gdpnow_vintages.json (ALFRED vintages)
- Script: python3 scripts/economics_gdpnow.py
- Module: src/pacland/economics/gdpnow.py

## Limitations

- The advantage survives the settled-number target but narrows sharply: 0.25 against the advance estimate, 0.75 against the settled number excluding 2020.
- The evaluation uses one public dataset and one target definition; neither has been independently replicated outside this repository.

_5 findings: 5 satisfied._
