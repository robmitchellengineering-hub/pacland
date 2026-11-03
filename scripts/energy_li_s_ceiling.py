#!/usr/bin/env python3
"""The Li–S ceiling: specific energy is set by the electrolyte/sulfur ratio.

    python3 scripts/energy_li_s_ceiling.py

Claim (docs/energy-conjectures.md): a Li–S cell's specific energy is set by the electrolyte/sulfur ratio,
not by cathode chemistry. At r = 3 uL/mg the cell caps at ~680 Wh/kg, so a "1600 Wh/kg" claim is
arithmetic-impossible at that electrolyte loading, however good the cathode is.

Everything here is published constants and arithmetic — no fitting, no simulation:

    Li2S: 2.15 V, 1672 mAh/g          (Materials Project / the Li–S literature)
    m_S      = q / 1.672              mg/cm2 for q mAh/cm2
    m_Li     = 0.433 m_S              mg/cm2 (2 Li per S: 2*6.94/32.06)
    m_elyte  = 1.2 r m_S              mg/cm2 (r in uL/mg, electrolyte density ~1.2 mg/uL)
    m_CB     = 0.25 m_S               mg/cm2 carbon black
    separator 1.1 mg, Cu 6 um + Al 12 um = 8.6 mg/cm2

    E(q, r) = 2.15 q / [q (1.007 + 0.718 r) + 9.7]   Wh/kg

Falsifier, registered before this ran: any full cell (>= 1 Ah, >= 50 cycles, total mass) measured above
680 Wh/kg at r >= 3 uL/mg.
"""
import sys

#: Li2S discharge voltage, V.
VOLTAGE = 2.15
#: Li2S theoretical capacity, mAh/g.
CAPACITY = 1672.0
#: mg per cm2 of sulfur per mAh/cm2 of areal capacity.
SULFUR_PER_Q = 1.0 / 1.672
#: lithium to sulfur mass ratio (2 Li : 1 S).
LI_TO_S = 2 * 6.94 / 32.06
#: electrolyte mass per unit r per unit sulfur mass (density 1.2 mg/uL).
ELYTE_PER_R = 1.2
#: carbon-black mass as a fraction of sulfur mass.
CARBON_FRACTION = 0.25
#: separator + current collectors, mg/cm2.
INACTIVE_MG = 1.1 + (6e-4 * 8.96 * 1000) + (12e-4 * 2.7 * 1000)


def specific_energy(q_mah_cm2: float, r_ul_mg: float) -> float:
    """Wh/kg for an areal capacity ``q`` (mAh/cm2) and electrolyte ratio ``r`` (uL/mg)."""
    if q_mah_cm2 <= 0:
        raise ValueError("q must be positive")
    if r_ul_mg < 0:
        raise ValueError("r cannot be negative")
    sulfur = q_mah_cm2 * SULFUR_PER_Q                      # mg/cm2
    mass = (sulfur * (1 + LI_TO_S + ELYTE_PER_R * r_ul_mg + CARBON_FRACTION)
            + INACTIVE_MG)                                  # mg/cm2
    return VOLTAGE * q_mah_cm2 / mass * 1000.0               # Wh/kg


def asymptote(r_ul_mg: float) -> float:
    """The q -> infinity limit — the absolute cap no areal capacity can beat."""
    per_q = SULFUR_PER_Q * (1 + LI_TO_S + ELYTE_PER_R * r_ul_mg + CARBON_FRACTION)
    return VOLTAGE * 1000.0 / per_q


def ceiling(r_ul_mg: float, q_max: float = 12.0) -> float:
    """Best specific energy reachable at this electrolyte ratio, over q up to ``q_max``."""
    return max(specific_energy(q, r_ul_mg) for q in
               [q_max * i / 200.0 for i in range(1, 201)])


def main() -> int:
    print("Li–S specific energy vs electrolyte/sulfur ratio (published constants, no fitting)\n")
    print(f"  {'r (uL/mg)':>10} {'ceiling Wh/kg':>14} {'E at q=4':>10} {'E at q=8':>10}")
    rows = []
    for r in (2.0, 3.0, 4.0, 6.0, 8.0):
        c = ceiling(r)
        rows.append((r, c))
        print(f"  {r:>10.1f} {c:>14.0f} {specific_energy(4.0, r):>10.0f} {specific_energy(8.0, r):>10.0f}")
    print()
    a3 = asymptote(3.0)
    print("Two different numbers, and the difference is the finding:")
    print(f"  asymptote at r = 3 (q -> infinity): {a3:.0f} Wh/kg   <- the absolute cap")
    print(f"  reachable at r = 3, q <= 12:        {ceiling(3.0):.0f} Wh/kg")
    print(f"  reachable at r = 3, q = 6:          {specific_energy(6.0, 3.0):.0f} Wh/kg")
    print()
    print(f"Claim under test: no cell at r >= 3 can exceed 680 Wh/kg.")
    print(f"Computed:         {a3:.0f} Wh/kg is the cap  ->  "
          f"{'CONSISTENT' if 640 <= a3 <= 720 else 'CONTRADICTED'} with the claim.")
    print()
    print("The correction this run produced: 680 Wh/kg is an ASYMPTOTE, not a target. At the")
    print("areal capacities Li-S cells actually reach (q ~ 6 mAh/cm2) the same arithmetic caps")
    print("them at ~450 Wh/kg, so '1600 Wh/kg' is impossible by a factor of 3.5, not 2.4.")
    print()
    print("Falsifier (registered before this ran): a full cell (>= 1 Ah, >= 50 cycles, total mass)")
    print("measured above 680 Wh/kg at r >= 3 uL/mg kills the claim.")
    print()
    print("Scope: constants are a materials budget (foil, separator, 6% packaging excluded),")
    print("not a measured bill of materials. A 10% budget error moves the cap by ~7%.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
