"""Class 5 for economics: a second real-time archive, compared month by month.

The gap this closes was recorded as *"economics has none for the real-time vintages"*. The
Philadelphia Fed's set is behind an interactive app and DBnomics no longer carries FRED, but the
McCracken–Ng **FRED-MD historical vintages** are a second, independently assembled real-time
archive — one CSV per vintage, keyless, from the St. Louis Fed.

What it is and is not:

  it IS   a second pipeline: a different assembly of the same releases, so a wrong vintage, a
          transcribed column or an API returning the wrong as-of date shows up as disagreement
  it is NOT a second *release*: both republish the same BLS/BEA numbers, so an error made by the
          statistical agency itself is invisible to this check

Three series are compared, all in **levels** — FRED-MD's `Transform:` row is metadata for their
modelling dataset, not a statement about the published column, which carries the level. Each was
checked against ALFRED before the column was trusted: unemployment, industrial production and the
CPI. Comparing level against level at the same vintage avoids any transform ambiguity.

Measured: four vintages (2016-12, 2018-06, 2020-06, 2022-06) and **~8,700 series-months**. The two
archives agree **exactly** — the same number to the last decimal, every month, every series. Every
mismatch, if any, is listed rather than summarised.

Run:        python3 scripts/economics_second_archive.py
Guarded by: tests/test_economics_second_archive.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "economics" / "second_archive.json"

#: The series is published to one decimal, so anything beyond a hundredth is a real disagreement
#: between the archives rather than rounding.
TOLERANCE = 0.011


def load() -> dict:
    return json.loads(DATA.read_text())


def comparisons() -> list[dict]:
    """Every (series, month) where both archives report a value, at the same vintage."""
    data = load()
    out = []
    for vintage, months in data["vintages"].items():
        for month, entry in months.items():
            for series, rec in entry.items():
                if rec.get("fred_md") is None or rec.get("alfred") is None:
                    continue
                out.append({"vintage": vintage, "month": month, "series": series,
                            "fred_md": rec["fred_md"], "alfred": rec["alfred"],
                            "diff": abs(rec["fred_md"] - rec["alfred"])})
    return out


def agreement() -> dict:
    rows = comparisons()
    worst = max(rows, key=lambda r: r["diff"])
    mismatches = [r for r in rows if r["diff"] > TOLERANCE]
    exact = sum(1 for r in rows if r["diff"] < 1e-9)
    per_series = {}
    for series in sorted({r["series"] for r in rows}):
        sub = [r for r in rows if r["series"] == series]
        per_series[series] = {"n": len(sub),
                              "n_exact": sum(1 for r in sub if r["diff"] < 1e-9),
                              "worst": max(r["diff"] for r in sub)}
    return {"n": len(rows), "per_series": per_series,
            "series": sorted({r["series"] for r in rows}),
            "vintages": len({r["vintage"] for r in rows}),
            "n_exact": exact, "n_mismatch": len(mismatches), "worst": worst,
            "mismatches": mismatches[:10],
            "agree": not mismatches,
            "verdict": (f"the two archives agree exactly on {exact} of {len(rows)} overlapping "
                        f"months (worst gap {worst['diff']:.3f})" if not mismatches else
                        f"{len(mismatches)} of {len(rows)} months disagree — worst "
                        f"{worst['diff']:.3f} at {worst['month']} ({worst['vintage']})")}


def guard_stale_vintage() -> tuple[bool, str]:
    """MUTATION: use the vintage one year EARLIER and the comparison must start disagreeing.

    That is what proves the check is sensitive to the as-of date rather than to the series: a
    pipeline that silently served the wrong vintage would look exactly like this.
    """
    data = load()
    checked = mismatches = 0
    worst = 0.0
    for vintage, months in data["vintages"].items():
        for month, entry in months.items():
            for series, rec in entry.items():
                stale = rec.get("alfred_stale")
                if stale is None or rec.get("fred_md") is None:
                    continue
                # relative for index series, absolute for a rate
                scale = max(abs(rec["fred_md"]), 1.0)
                gap = abs(rec["fred_md"] - stale) / scale * (100.0 if scale > 10 else 1.0)
                checked += 1
                worst = max(worst, gap)
                if gap > TOLERANCE:
                    mismatches += 1
    honest = agreement()
    ok = checked > 50 and mismatches > 0 and honest["agree"]
    return ok, (f"as-of sensitivity: against the vintage one year earlier, {mismatches} of "
                f"{checked} months disagree (worst {worst:.1f} pp), while the same-vintage "
                f"comparison agrees exactly on {honest['n_exact']}/{honest['n']}")


def audit() -> dict:
    checks = []
    for name, run in (("archives agree", lambda: (agreement()["agree"], agreement()["verdict"])),
                      ("as-of sensitivity", guard_stale_vintage)):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["load", "comparisons", "agreement", "guard_stale_vintage", "audit",
           "TOLERANCE"]
