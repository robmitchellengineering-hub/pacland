"""Class 5 at the release level: the Fed's first print against the one we recorded.

Two archives now hold a "first release" of quarterly real GDP growth for 2016–2025:

  ours     `gdpnow.json`'s `advance` column — the advance estimate read from ALFRED at the time
  the Fed  `release_archive.json`'s `first` column — the Real-Time Data Set's First Release

They should be the same number. Mostly they are: **34 of 36 overlapping quarters agree within
0.5 pp, 29 within 0.1 pp**. Two do not, and they are the two COVID quarters:

| quarter | Fed first release | our advance | gap |
|---|---|---|---|
| 2020Q2 | **−32.90%** | −39.91% | **−7.00 pp** |
| 2020Q3 | **+33.08%** | +28.58% | **−4.50 pp** |

That is the class-5 check doing its job: a disagreement this large is not noise, it is a statement
that one of the two numbers is not what it claims to be. The Fed's ladder is the more authoritative
record of what the Bureau *first published*, so the working conclusion is that our `advance` column
is not the first print for those two quarters.

**Why this matters to our own headline.** The 37-quarter revision result is sensitive to how those
quarters are treated:

    as shipped                     +0.565 pp  (t = 2.39)
    excluding 2020Q2/Q3            +0.357 pp  (t = 2.26)
    using the Fed's first releases  +0.254 pp  (t = 1.43)

So the 37-quarter figure should not be quoted as though it were stable. The **239-quarter ladder
result** (`release_archive.py`: +0.469 pp, t = 3.68) never depended on our advance column and is
unaffected — that is the number to quote.

Run:        python3 scripts/economics_release_cross.py
Guarded by: tests/test_economics_release_cross.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
RELEASES = ROOT / "data" / "economics" / "release_archive.json"
GDPNOW = ROOT / "data" / "economics" / "gdpnow.json"

#: Beyond this the two records are not the same quantity. Set well above the 0.04 pp typical gap
#: and well below the 4.5 pp COVID disagreement, so it separates them cleanly.
AGREEMENT = 0.5

#: The quarters the cross-check found disagreeing by more than a point.
OUTLIERS = ("2020Q2", "2020Q3")


def _norm(quarter: str) -> str:
    return quarter.replace(":", "")


def load_pairs() -> list[dict]:
    fed = {_norm(x["quarter"]): x["first"]
           for x in json.loads(RELEASES.read_text())["quarters"]}
    ours = {_norm(x["quarter"]): x["advance"]
            for x in json.loads(GDPNOW.read_text())["quarters"]}
    common = sorted(set(fed) & set(ours))
    return [{"quarter": q, "fed_first": fed[q], "our_advance": ours[q],
             "gap": ours[q] - fed[q]} for q in common]


def agreement() -> dict:
    rows = load_pairs()
    gaps = [abs(r["gap"]) for r in rows]
    within = [r for r in rows if abs(r["gap"]) <= AGREEMENT]
    outside = sorted([r for r in rows if abs(r["gap"]) > AGREEMENT],
                     key=lambda r: -abs(r["gap"]))
    return {"n": len(rows), "n_within": len(within), "n_outside": len(outside),
            "worst_gap": max(gaps), "mean_abs_gap": sum(gaps) / len(gaps),
            "outside": outside,
            "agrees": not outside,
            "verdict": (f"{len(within)} of {len(rows)} quarters agree within {AGREEMENT} pp "
                        f"(mean |gap| {sum(gaps) / len(gaps):.3f} pp)"
                        + ("" if not outside else
                           f"; {len(outside)} do not, led by "
                           f"{outside[0]['quarter']} at {outside[0]['gap']:+.2f} pp"))}


def sensitivity() -> dict:
    """How much does our 37-quarter revision headline depend on those quarters?"""
    rows = json.loads(GDPNOW.read_text())["quarters"]

    def mean_rev(rs: list[dict]) -> float:
        revs = [r["final"] - r["advance"] for r in rs]
        return sum(revs) / len(revs)

    fed = {_norm(x["quarter"]): x["first"]
           for x in json.loads(RELEASES.read_text())["quarters"]}
    substituted = []
    for r in rows:
        q = dict(r)
        key = _norm(r["quarter"])
        if key in fed and key in {_norm(o) for o in OUTLIERS}:
            q["advance"] = fed[key]
        substituted.append(q)
    everything = mean_rev(rows)
    excluded = mean_rev([r for r in rows if _norm(r["quarter"]) not in
                         {_norm(o) for o in OUTLIERS}])
    with_fed = mean_rev(substituted)
    return {"all": everything, "excluded": excluded, "fed_values": with_fed,
            "swing": max(everything, excluded, with_fed) - min(everything, excluded, with_fed),
            "stable": abs(everything - with_fed) < 0.1,
            "verdict": (f"the 37-quarter mean revision moves from {everything:+.3f} to "
                        f"{excluded:+.3f} (excluding the two quarters) and {with_fed:+.3f} "
                        f"(using the Fed's first releases) — a swing of "
                        f"{max(everything, excluded, with_fed) - min(everything, excluded, with_fed):.3f} pp")}


def guard_misalignment() -> tuple[bool, str]:
    """MUTATION: shift one series by a quarter and the agreement must collapse. If it did not, the
    comparison would be measuring levels rather than quarter-by-quarter releases."""
    rows = load_pairs()
    aligned = sum(1 for r in rows if abs(r["gap"]) <= AGREEMENT)
    shifted = [{"gap": rows[i]["our_advance"] - rows[i - 1]["fed_first"]}
               for i in range(1, len(rows))]
    shifted_within = sum(1 for r in shifted if abs(r["gap"]) <= AGREEMENT)
    ok = shifted_within < aligned and aligned > len(rows) * 0.8
    return ok, (f"alignment: {aligned}/{len(rows)} agree when quarters line up, only "
                f"{shifted_within}/{len(shifted)} when shifted by one — pairing matters = {ok}")


def guard_outliers_are_named() -> tuple[bool, str]:
    """MUTATION: the two COVID disagreements must be REPORTED, not averaged away. The mean |gap|
    is 0.4 pp; the worst is 7 pp, and a summary that hides the second number is misleading."""
    a = agreement()
    named = [r["quarter"] for r in a["outside"]]
    ok = all(_norm(o) in named for o in OUTLIERS) and a["worst_gap"] > 3.0
    return ok, (f"outliers: {named} are reported individually; worst {a['worst_gap']:.2f} pp "
                f"against a mean |gap| of {a['mean_abs_gap']:.3f} pp — both numbers appear")


def audit() -> dict:
    checks = []
    for name, run in (("agreement quantified", lambda: (True, agreement()["verdict"])),
                      ("outliers named", guard_outliers_are_named),
                      ("alignment matters", guard_misalignment),
                      ("sensitivity disclosed", lambda: (True, sensitivity()["verdict"]))):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["load_pairs", "agreement", "sensitivity", "guard_misalignment",
           "guard_outliers_are_named", "audit", "AGREEMENT", "OUTLIERS"]
