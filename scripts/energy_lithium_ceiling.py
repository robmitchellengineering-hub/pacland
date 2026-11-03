#!/usr/bin/env python3
"""Lithium mass balance, not cost, caps Li-ion deployment near 3.2 TWh/yr.

    python3 scripts/energy_lithium_ceiling.py

Claim (docs/energy-conjectures.md): an LFP cell carries ~0.41 kg LCE per kWh, so the 2024 world supply of
1.3 Mt LCE caps deployment at ~3.2 TWh/yr. Arithmetic on published constants — no fitting:

    LFP: 1.75 kg/kWh;  Li fraction = 6.94 / 157.76 = 0.044  ->  0.077 kg Li/kWh
    LCE factor: 5.32 kg lithium carbonate equivalent per kg Li -> 0.41 kg LCE/kWh
    world supply 2024: 1.3 Mt LCE (USGS Mineral Commodity Summaries 2025)

Falsifier, registered before this ran: more than 5 TWh/yr of Li-ion produced from less than 1.5 Mt LCE
primary supply, with no more than a 2x lithium price rise.
"""
import sys

#: kg of LFP cell per kWh (pack-level, published cell/pack data).
LFP_KG_PER_KWH = 1.75
#: lithium mass fraction of LiFePO4.
LI_FRACTION = 6.94 / 157.76
#: kg of lithium carbonate equivalent per kg of lithium.
LCE_PER_KG_LI = 5.32
#: 2024 world lithium supply, tonnes LCE (USGS MCS 2025).
WORLD_LCE_TONNES = 1.3e6
#: NMC811 intensity, for the comparison line.
NMC811_KG_PER_KWH = 1.9


def lce_per_kwh(kg_per_kwh: float) -> float:
    """kg LCE required per kWh of cells, from the cell's mass per kWh."""
    return kg_per_kwh * LI_FRACTION * LCE_PER_KG_LI


def deployment_ceiling_twh(lce_tonnes: float, kg_lce_per_kwh: float) -> float:
    """TWh/yr reachable from `lce_tonnes` tonnes at `kg_lce_per_kwh`.

    tonnes x 1000 = kg; kg / (kg/kWh) = kWh; kWh / 1e9 = TWh.  Together: tonnes / intensity / 1e6.
    """
    if kg_lce_per_kwh <= 0:
        raise ValueError("intensity must be positive")
    return lce_tonnes / kg_lce_per_kwh / 1e6


def main() -> int:
    lfp = lce_per_kwh(LFP_KG_PER_KWH)
    nmc = lce_per_kwh(NMC811_KG_PER_KWH)
    print("Lithium mass balance — how many TWh/yr the world's lithium allows\n")
    print(f"  LFP     : {LFP_KG_PER_KWH:.2f} kg/kWh -> {lfp:.3f} kg LCE/kWh")
    print(f"  NMC811  : {NMC811_KG_PER_KWH:.2f} kg/kWh -> {nmc:.3f} kg LCE/kWh")
    print(f"  supply  : {WORLD_LCE_TONNES/1e6:.1f} Mt LCE/yr (2024, USGS)")
    print()
    print(f"  ceiling : {deployment_ceiling_twh(WORLD_LCE_TONNES, lfp):.2f} TWh/yr of LFP")
    need_mt = 6e9 * lfp / 1e9
    supply_mt = WORLD_LCE_TONNES / 1e6
    print(f"  6 TWh/yr needs {need_mt:.1f} Mt LCE — {need_mt / supply_mt:.1f}x the 2024 supply")
    print()
    print("Claim under test: deployment is capped near 3.2 TWh/yr.")
    cap = deployment_ceiling_twh(WORLD_LCE_TONNES, lfp)
    print(f"Computed:        {cap:.2f} TWh/yr -> "
          f"{'CONSISTENT' if 3.0 <= cap <= 3.4 else 'CONTRADICTED'} with the claim.")
    print()
    print("Falsifier (registered before this ran): > 5 TWh/yr from < 1.5 Mt LCE primary supply,")
    print("with no more than a 2x lithium price rise.")
    print()
    print("Scope: ignores recycling (<5% in 2024) and cathode mix; intensity is a published")
    print("pack-level figure, not a measured bill of materials for every cell.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
