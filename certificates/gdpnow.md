# Model risk certificate — Atlanta Fed GDPNow (GDP nowcast, US)

**Issued:** 2026-10-28  
**Issuer:** Pacland / Valiant Verification  
**Grade:** **QUALIFIED**

Beats the no-change null by a wide margin (75% lower MAE) on 37 quarters of real-time vintages — qualified because that skill is measured against the advance estimate, not the settled number.

| clause | question | what the evidence says | status |
|---|---|---|---|
| Conceptual soundness | Is the forecast a model at all, or an accounting identity? | Bridge-equation nowcast; beats the no-change null on MAE by 75% (1.26 vs 5.05 pp) | **satisfied** |
| Outcomes analysis | Does it beat the null out of sample? | 28 of 37 quarters, MAE ratio 0.25 (<1 = beats the null) | **satisfied** |
| Outcomes analysis | Is that skill against the FIRST publication or the settled number? | Target matters: skill against the advance estimate is not skill against the number that survives revision. Both are reported. | **partial** |
| Data quality | Are the inputs real-time vintages, or revised history? | Real-time vintages (ALFRED) throughout; a vintage that post-dates the forecast is refused by guard_nowcast_predates_release | **satisfied** |
| Implementation | Can the evaluation go red? | Four guards, each mutation-proved: vintage ordering, shared benchmark vintage, first-publication target, units | **satisfied** |

## Evidence

- Data: data/economics/gdpnow_vintages.json (ALFRED vintages)
- Script: python3 scripts/economics_gdpnow.py
- Module: src/pacland/economics/gdpnow.py

## Limitations

- Skill is measured against the first publication; against the final number the nowcast's advantage narrows and is not established here.
- The evaluation uses one public dataset and one target definition; neither has been independently replicated outside this repository.

_5 findings: 1 partial, 4 satisfied._
