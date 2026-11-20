"""unified_constraints.py — the full economics constraint set: accounting + hard-science, bridged.

The in-tree `economics/constraint_set.py` holds the ACCOUNTING identities (true by construction — no model
may violate them). `econ_constraints.py` holds the HARD-SCIENCE laws (the unifications — which model is
correct). This bridges them into ONE report: a candidate must satisfy BOTH layers.
"""
from __future__ import annotations

from pacland.economics import constraint_set as acct
from pacland import econ_constraints as laws


def combined_report(model: dict, law_names: list[str], state: dict | None = None) -> dict:
    """Run both layers: the accounting identities (in-tree) + the hard-science laws (mine)."""
    s = state or acct._default_state()
    acct_violated = acct.violated(s)
    law_result = laws.check_model(model, law_names)
    return {
        "accounting_identities": {
            "count": len(acct.CONSTRAINTS),
            "violated": acct_violated,
            "independent_rank": acct.independence(s).get("rank") if hasattr(acct, "independence") else None,
            "ok": not acct_violated,
        },
        "hard_science_laws": {
            "checked": law_names,
            "violated": law_result["violated"],
            "ok": law_result["valid"],
            "verdict": law_result["verdict"],
        },
        "combined": "VALID — satisfies the accounting identities AND the hard-science laws"
                    if (not acct_violated and law_result["valid"])
                    else "REFUTED — " + "; ".join(
                        [f"accounting: {acct_violated}" if acct_violated else "",
                         f"laws: {law_result['violated']}" if law_result["violated"] else ""]).strip("; "),
    }
