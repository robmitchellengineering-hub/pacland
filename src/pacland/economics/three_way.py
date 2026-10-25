"""The three-way, at the level this repository can actually support.

The objective asked for **SW vs BVAR vs the no-change null**. SW's full model is a
20-condition, ~40-parameter system; estimating it is a project, not a slice, and this
module does not pretend to have done it. What it *does* is run the comparison at the
level the published record supports:

- the **SW-calibrated subsystem**: the three-equation reduction of SW's mechanism, at
  SW's *published* parameters — κ from their Calvo estimate (ξ_p = 0.66), the discount
  factor from their Euler equation, and their estimated policy rule (φπ = 2.04,
  φy = 0.08). It is **not** SW: no capital, no Calvo wages, no partial indexation, no
  seven shocks. The name says so, and the doc says so twice.
- the **textbook NK3** (κ = 0.1, φπ = 1.5, φy = 0.5), for contrast;
- the **VAR(1)** and the **no-change null**, on the same real-time vintage fixture.

So the answer to "does structure beat the null?" is given for *two* structural
calibrations rather than one, and the gap to SW's own model is stated as a gap.

Pure stdlib.
"""
from __future__ import annotations

from . import meese_rogoff, nk3, nk3_oos, sw2007, sw_structure

#: SW's published parameters, mapped onto the three-equation reduction. ``rho_r`` and
#: ``rho_u`` have no SW counterpart at this level (SW has seven shocks), so the same
#: typical persistences as the textbook run are used and labelled as borrowed.
BORROWED_PERSISTENCE = {"rho_r": 0.9, "rho_u": 0.8}


def sw_calibration() -> dict[str, float]:
    return {
        "beta": sw2007.beta_tilde(),          # detrended, from the published tau
        "kappa": sw2007.calvo_kappa(),        # from the published Calvo stickiness
        "sigma": 1.0,                         # not identified in this reduction
        "phi_pi": sw2007.PUBLISHED_STRUCTURAL["r_pi"],
        "phi_y": sw2007.PUBLISHED_STRUCTURAL["r_y"],
        **BORROWED_PERSISTENCE,
    }


def run() -> dict:
    """The four-way table: null, VAR(1), textbook NK3, SW-calibrated subsystem."""
    sw = nk3_oos.evaluate(cal=sw_calibration())
    nk = nk3_oos.evaluate()
    var = meese_rogoff.evaluate()
    return {"sw_subsystem": sw, "nk3": nk, "var1": var,
            "params": {"sw_subsystem": sw_calibration(), "nk3": dict(nk3.CALIBRATION)}}


def summary() -> str:
    r = run()
    lines = [
        "THE THREE-WAY, at the level this repository supports",
        "=" * 62,
        "SW SUBSYSTEM = SW's published parameters in a 3-equation reduction.",
        "It is NOT the 20-condition SW model: no capital, no Calvo wages, no",
        "indexation, no seven shocks. SW itself still owes its out-of-sample run.",
        "",
        "INFLATION (annualised pp), real-time vintages, vs today's revised values",
    ]
    sw, nk = r["sw_subsystem"], r["nk3"]
    base_pi = nk["no-change"]["pi"]
    for label, m in (("no-change", "no-change"), ("AR(1)", "AR(1)"),
                     ("textbook NK3", "NK3"), ("SW subsystem", "NK3")):
        src = sw if label == "SW subsystem" else nk
        vals = " ".join(f"h={h}: {src[m]['pi'][h]:.3f}" for h in (1, 2, 4))
        ratio = " ".join(f"{src[m]['pi'][h]/base_pi[h]:.2f}x" for h in (1, 2, 4))
        lines.append(f"  {label:<14} {vals}   {ratio}")
    lines.append("")
    lines.append("OUTPUT GAP (pp)")
    base_gap = nk["no-change"]["gap"]
    for label, m in (("no-change", "no-change"), ("textbook NK3", "NK3"),
                     ("SW subsystem", "NK3")):
        src = sw if label == "SW subsystem" else nk
        vals = " ".join(f"h={h}: {src[m]['gap'][h]:.3f}" for h in (1, 2, 4))
        ratio = " ".join(f"{src[m]['gap'][h]/base_gap[h]:.2f}x" for h in (1, 2, 4))
        lines.append(f"  {label:<14} {vals}   {ratio}")
    lines.append("")
    lines.append(f"VAR(1) on the same fixture: "
                 + " ".join(f"h={h}: {r['var1']['VAR(1)'][h]/r['var1']['no-change'][h]:.2f}x"
                            for h in (1, 2, 4))
                 + "  (a three-series growth run, not a like-for-like target)")
    return "\n".join(lines)


def finding() -> dict:
    """The answer, as data — so the doc and the tests cannot drift apart."""
    r = run()
    sw, nk = r["sw_subsystem"], r["nk3"]
    return {
        "sw_loses_pi": all(sw["NK3"]["pi"][h] > nk["no-change"]["pi"][h] for h in (1, 2, 4)),
        "sw_beats_pi_h4": sw["NK3"]["pi"][4] < nk["no-change"]["pi"][4],
        "sw_beats_gap_h4": sw["NK3"]["gap"][4] < nk["no-change"]["gap"][4],
        "ratios_pi": {h: sw["NK3"]["pi"][h] / nk["no-change"]["pi"][h] for h in (1, 2, 4)},
        "ratios_gap": {h: sw["NK3"]["gap"][h] / nk["no-change"]["gap"][h] for h in (1, 2, 4)},
    }


if __name__ == "__main__":
    print(summary())
