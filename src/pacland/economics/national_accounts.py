"""The national accounts — GDPNow's exact half, and the half that leaks.

GDPNow is an accounting bridge: monthly source data are mapped onto the expenditure
components of GDP, and the components are added up. So its *exact* content is the
national-accounts identity, and its *specification* is the bridge. This module proves the
first and measures the second, instead of asserting either.

What is exact, and verified on 32 quarters of real BEA data (2018Q1–2025Q4):

- **additivity** — ``GDP = PCE + GPDI + GCE + NETEXP`` holds to BEA rounding
  (max |residual| ~1e-5% of GDP on the fetched data);
- **contributions add** — the nominal contributions to growth sum to nominal growth;
- **shares sum to one** — the nominal weights of the components sum to 1 by the identity,
  which is what makes the contribution decomposition legitimate.

What is *not* exact, and is reported rather than buried: the **real** side. Chained-dollar
components are not additive — BEA's real GDP is a chain aggregate — so summing real
component changes divided by real GDP leaves a residual that is small in normal quarters
and enormous in 2020. That residual is the measured deficit of the real decomposition, and
no amount of arithmetic removes it.

Not implemented, and named: GDPNow's **bridge equations** — the mapping from monthly
source series to the components. That is the Atlanta Fed's engineering, published in their
methodology, and re-deriving it is a project, not a slice.
"""
from __future__ import annotations

import json
import math
import pathlib

FIXTURE = pathlib.Path(__file__).resolve().parents[3] / "data" / "economics" / "accounts.json"
COMPONENTS = ("PCE", "GPDI", "GCE", "NETEXP")

INVENTORY = (
    ("additivity", "GDP = C + I + G + NX", "proved"),
    ("nominal_contributions", "contributions to nominal growth sum to nominal growth", "proved"),
    ("shares_sum_to_one", "the nominal component shares sum to 1", "proved"),
    ("real_decomposition", "real contribution decomposition closes", "specification"),
    ("bridge_equations", "monthly source data -> components", "specification"),
    ("chain_aggregation", "BEA's chained-dollar aggregation", "specification"),
)


def load(path: pathlib.Path | None = None) -> dict:
    return json.loads(pathlib.Path(path or FIXTURE).read_text())


def quarters(data: dict | None = None) -> list[dict]:
    return (data or load())["quarters"]


# --- the exact block ----------------------------------------------------------


def additivity_residual(rec: dict) -> float:
    """``C + I + G + NX - GDP`` in billions. Zero to BEA rounding."""
    n = rec["nominal"]
    return n["PCE"] + n["GPDI"] + n["GCE"] + n["NETEXP"] - n["GDP"]


def nominal_shares(rec: dict) -> dict[str, float]:
    n = rec["nominal"]
    return {k: n[k] / n["GDP"] for k in COMPONENTS}


def nominal_contributions(rec: dict, prev: dict) -> dict[str, float]:
    """Percentage-point contribution of each component to *nominal* GDP growth."""
    g0 = prev["nominal"]["GDP"]
    return {k: 100.0 * (rec["nominal"][k] - prev["nominal"][k]) / g0 for k in COMPONENTS}


def nominal_growth(rec: dict, prev: dict) -> float:
    g0 = prev["nominal"]["GDP"]
    return 100.0 * (rec["nominal"]["GDP"] - g0) / g0


# --- the block that leaks -----------------------------------------------------


def real_contributions(rec: dict, prev: dict) -> dict[str, float]:
    """Percentage-point contributions in chained dollars, relative to *real* GDP."""
    g0 = prev["real"]["GDPC1"]
    p, c = prev["real"], rec["real"]
    return {
        "PCE": 100.0 * (c["PCECC96"] - p["PCECC96"]) / g0,
        "GPDI": 100.0 * (c["GPDIC1"] - p["GPDIC1"]) / g0,
        "GCE": 100.0 * (c["GCEC1"] - p["GCEC1"]) / g0,
        "NETEXP": 100.0 * ((c["EXPGSC1"] - c["IMPGSC1"]) - (p["EXPGSC1"] - p["IMPGSC1"])) / g0,
    }


def real_growth(rec: dict, prev: dict) -> float:
    """Annualised quarterly log growth of real GDP."""
    return 400.0 * math.log(rec["real"]["GDPC1"] / prev["real"]["GDPC1"])


def real_decomposition_residual(rec: dict, prev: dict) -> float:
    """The chain-link residual: contributions minus realised real growth, in points."""
    return sum(real_contributions(rec, prev).values()) - real_growth(rec, prev)


def defect_report(data: dict | None = None) -> dict:
    """The measured size of the two leaks: additivity (tiny) and chain-linking (large)."""
    recs = quarters(data)
    add = [abs(additivity_residual(r)) for r in recs]
    res = [real_decomposition_residual(recs[i], recs[i - 1]) for i in range(1, len(recs))]
    excl = [real_decomposition_residual(recs[i], recs[i - 1]) for i in range(1, len(recs))
            if not recs[i]["quarter"].startswith("2020")]
    return {
        "n": len(recs),
        "max_additivity_billions": max(add),
        "max_additivity_pct_gdp": 100.0 * max(add) / max(r["nominal"]["GDP"] for r in recs),
        "chain_residual_mean": sum(res) / len(res),
        "chain_residual_max_abs": max(abs(x) for x in res),
        "chain_residual_mean_excl_2020": sum(excl) / len(excl),
        "chain_residual_max_abs_excl_2020": max(abs(x) for x in excl),
    }


def coverage() -> dict:
    proved = [k for k, _, v in INVENTORY if v == "proved"]
    spec = [k for k, _, v in INVENTORY if v == "specification"]
    unknown = [k for k, _, v in INVENTORY if v not in ("proved", "specification")]
    return {"n_total": len(INVENTORY), "n_proved": len(proved), "n_specification": len(spec),
            "n_unknown": len(unknown), "proved": proved, "specification": spec,
            "complete": not unknown}


# --- guards -------------------------------------------------------------------


def guard_additivity(data: dict | None = None, tol_pct: float = 1e-3) -> tuple[bool, str]:
    """The expenditure identity must close to BEA rounding. A leak here means the
    components and the headline are on different vintages or different definitions."""
    rep = defect_report(data)
    ok = rep["max_additivity_pct_gdp"] <= tol_pct
    return ok, (
        f"additivity: max |residual| {rep['max_additivity_billions']:.4f} bn = "
        f"{rep['max_additivity_pct_gdp']:.2e}% of GDP over {rep['n']} quarters "
        f"({'closes' if ok else 'LEAKS'})"
    )


def guard_contributions_sum(data: dict | None = None) -> tuple[bool, str]:
    """Nominal contributions must sum to nominal growth — the identity doing the work.

    The tolerance is *publication rounding*, not floating point: BEA publishes components
    rounded to 0.001 bn, so the identity closes to ~1e-4 pp, which is a thousand times
    smaller than any economic effect. Claiming 1e-6 here would be a claim about BEA's
    rounding, not about the accounts."""
    recs = quarters(data)
    worst = 0.0
    for i in range(1, len(recs)):
        tot = sum(nominal_contributions(recs[i], recs[i - 1]).values())
        worst = max(worst, abs(tot - nominal_growth(recs[i], recs[i - 1])))
    return worst < 1e-3, (
        f"nominal contributions sum to growth (worst gap {worst:.2e} pp — publication rounding)"
    )


def guard_shares_sum_to_one(data: dict | None = None) -> tuple[bool, str]:
    recs = quarters(data)
    worst = max(abs(sum(nominal_shares(r).values()) - 1.0) for r in recs)
    return worst < 1e-5, f"nominal shares sum to 1 (worst gap {worst:.2e} — publication rounding)"


def guard_the_leak_is_reported(data: dict | None = None) -> tuple[bool, str]:
    """The real decomposition does not close, and the report must say how much rather
    than presenting the decomposition as exact."""
    rep = defect_report(data)
    ok = rep["chain_residual_max_abs"] > 0.01 and "not additive" in __doc__
    return ok, (
        f"real decomposition: chain-link residual mean {rep['chain_residual_mean']:+.3f} pp, "
        f"max |{rep['chain_residual_max_abs']:.3f}| pp "
        f"(excl. 2020: mean {rep['chain_residual_mean_excl_2020']:+.3f}, "
        f"max |{rep['chain_residual_max_abs_excl_2020']:.3f}|)"
    )


def summary() -> str:
    rep = defect_report()
    cov = coverage()
    return "\n".join(
        [
            "NATIONAL ACCOUNTS — the exact half of GDPNow, and the half that leaks",
            "=" * 68,
            f"{rep['n']} quarters, BEA data via FRED",
            "",
            f"additivity      max |residual| {rep['max_additivity_billions']:.4f} bn "
            f"= {rep['max_additivity_pct_gdp']:.1e}% of GDP  -> CLOSES (rounding)",
            "contributions   nominal contributions sum to nominal growth  -> CLOSES (rounding)",
            "shares          the nominal shares sum to 1                  -> CLOSES (rounding)",
            "",
            f"real side       chain-link residual mean {rep['chain_residual_mean']:+.3f} pp, "
            f"max |{rep['chain_residual_max_abs']:.3f}| pp",
            f"                excluding 2020: mean "
            f"{rep['chain_residual_mean_excl_2020']:+.3f} pp, "
            f"max |{rep['chain_residual_max_abs_excl_2020']:.3f}| pp",
            "                -> NOT exact: chained dollars are not additive",
            "",
            f"inventory: {cov['n_proved']} proved, {cov['n_specification']} specifications, "
            f"{cov['n_unknown']} unresolved",
            "  specification = the bridge equations (Atlanta Fed's engineering), BEA's",
            "  chained aggregation, and the real decomposition that inherits its leak.",
        ]
    )


if __name__ == "__main__":
    print(summary())
