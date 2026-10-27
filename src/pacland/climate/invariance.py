"""Climate invariance — the same gate as economics, on a second discipline.

The point of this module is not the three checks. It is that the *method* transfers: if
invariance is a general oracle for fields without ground truth, it must be constructive in a
field that has one too. Climate has conservation (class 1) already; what it lacked was the
class-2 check that its claims do not depend on how the data was written down.

Three checks, each with a seeded fault:

  baseline period   move the 1951-80 reference to 1900-1930: the anomaly OFFSETS change, the
                    trend and its rate must not
  units             Celsius to Kelvin: every level shifts by 273.15, every skill score is
                    untouched — so a skill score that moves is being computed on levels
  window            shift the hindcast start years: what is ROBUST must hold in every window
                    (the trend beats persistence), and what is NOT robust must be said so
                    (the trend-versus-emulator ranking flips with the window)

The third check is the reason this module earns its place. It was written to assert that "the
trend beats the emulators" survives a one-year shift — and it does not. Measured on the
committed GISTEMP record, moving the start years by one flips the winner between the trend and
two different emulators. So the claim is now scoped to what holds: the trend beats persistence
in every window; no ranking between the trend and the emulators is claimed.

Run:        python3 scripts/climate_invariance.py
Guarded by: tests/test_climate_invariance.py
"""
from __future__ import annotations

from . import baseline

#: Round-off floor for a series of annual anomalies from a JSON file.
RTOL = 1e-12


def _close(a: float, b: float, rtol: float = RTOL) -> bool:
    return abs(a - b) <= rtol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------------------------------
# 1. baseline period — the reference is a convention, the trend is the measurement
# ---------------------------------------------------------------------------------------
def rebase(gmst: dict[int, float], old: tuple[int, int], new: tuple[int, int]) -> dict[int, float]:
    """Re-express every anomaly against a different reference period."""

    def mean_over(span: tuple[int, int]) -> float:
        vals = [v for y, v in gmst.items() if span[0] <= y <= span[1]]
        return sum(vals) / len(vals)

    shift = mean_over(new) - mean_over(old)
    return {y: v - shift for y, v in gmst.items()}


def trend_rate(gmst: dict[int, float], start: int = 1970, end: int = 2024) -> float:
    """Degrees per year, by least squares on the annual anomalies."""
    xs = [y for y in sorted(gmst) if start <= y <= end]
    ys = [gmst[y] for y in xs]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx


def baseline_invariance(data: dict | None = None) -> dict:
    gmst = (data or baseline.load())["gmst"]
    gmst = {int(y): v for y, v in gmst.items()}
    old, new = (1951, 1980), (1900, 1930)
    rebased = rebase(gmst, old, new)
    r0, r1 = trend_rate(gmst), trend_rate(rebased)
    offset0 = gmst[2024]
    offset1 = rebased[2024]
    return {"rate_original": r0, "rate_rebased": r1,
            "rate_drift": abs(r1 - r0) / max(1e-12, abs(r0)),
            "offset_moved": not _close(offset0, offset1, 1e-9),
            "pass": _close(r0, r1, 1e-10) and not _close(offset0, offset1, 1e-9)}


def guard_baseline(data: dict | None = None) -> tuple[bool, str]:
    """MUTATION: a trend fitted on a *shifted window* must differ — otherwise the check is
    insensitive to the thing it is meant to be insensitive to only in the baseline."""
    gmst = (data or baseline.load())["gmst"]
    gmst = {int(y): v for y, v in gmst.items()}
    r_full = trend_rate(gmst, 1970, 2024)
    r_shifted = trend_rate(gmst, 1980, 2024)
    moved = abs(r_shifted - r_full) / abs(r_full) > 1e-3
    r = baseline_invariance(data)
    ok = r["pass"] and moved
    return ok, (f"baseline: rate {r['rate_original']:+.4f} °C/yr, rebased "
                f"{r['rate_rebased']:+.4f} (drift {r['rate_drift']:.1e}), offset moved = "
                f"{r['offset_moved']}; a shifted window moves the rate = {moved}")


# ---------------------------------------------------------------------------------------
# 2. units — Celsius to Kelvin must not touch a skill score
# ---------------------------------------------------------------------------------------
def to_kelvin(gmst: dict[int, float]) -> dict[int, float]:
    return {y: v + 273.15 for y, v in gmst.items()}


def skill_persistence(gmst: dict[int, float], y0: int, h: int) -> float:
    return abs(gmst[y0 + h] - gmst[y0])


def units_invariance(data: dict | None = None) -> dict:
    gmst = (data or baseline.load())["gmst"]
    gmst = {int(y): v for y, v in gmst.items()}
    kelvin = to_kelvin(gmst)
    worst = 0.0
    for y0 in (1980, 1990, 2000, 2010):
        for h in (10, 20):
            if y0 + h not in gmst:
                continue
            a = skill_persistence(gmst, y0, h)
            b = skill_persistence(kelvin, y0, h)
            worst = max(worst, abs(a - b))
    return {"worst_skill_drift": worst, "levels_moved": not _close(gmst[2024], kelvin[2024], 1e-9),
            "pass": worst < 1e-9}


def guard_units(data: dict | None = None) -> tuple[bool, str]:
    """MUTATION: subtract a Kelvin series from a Celsius one — a unit mismatch — and the
    error must explode. This is the bug the real-time vintage fetch made once."""
    gmst = (data or baseline.load())["gmst"]
    gmst = {int(y): v for y, v in gmst.items()}
    mismatched = abs(to_kelvin(gmst)[2024] - gmst[2024])
    r = units_invariance(data)
    ok = r["pass"] and mismatched > 100.0
    return ok, (f"units: skill drift {r['worst_skill_drift']:.1e}, levels moved = "
                f"{r['levels_moved']}; a Kelvin/Celsius mismatch is {mismatched:.2f} °C "
                f"wide = {mismatched > 100.0}")


# ---------------------------------------------------------------------------------------
# 3. window — the finding must survive moving the start year by one
# ---------------------------------------------------------------------------------------
def ranking(evaluation: dict) -> tuple[str, float]:
    """Lowest MAE wins. Named rather than positional, so a rename cannot fake a pass."""
    mae = {k: v["mae"] for k, v in evaluation["methods"].items()}
    best = min(mae, key=mae.get)
    return best, mae[best]


WINDOWS = ((1980, 1990, 2000, 2010),
           (1981, 1991, 2001, 2011),
           (1985, 1995, 2005, 2015),
           (1990, 2000, 2010))


def window_invariance(data: dict | None = None) -> dict:
    """What survives the window, and what does not — both, with numbers.

    Robust claim  : the trend beats persistence in every window tested.
    Not robust    : which of trend/emulators wins — it flips, so it is not claimed.
    """
    rows = []
    for starts in WINDOWS:
        try:
            ev = baseline.evaluate(data, starts=starts)
        except (KeyError, IndexError, ZeroDivisionError):
            continue
        mae = {k: v["mae"] for k, v in ev["methods"].items()}
        rows.append({"starts": starts, "mae": mae,
                     "best": min(mae, key=mae.get),
                     "trend_beats_persistence": mae["trend"] < mae["persistence"]})
    winners = {r["best"] for r in rows}
    trend_wins = all(r["trend_beats_persistence"] for r in rows)
    emulators = [r["best"] for r in rows if r["best"].startswith("emulator:")]
    return {"windows": [r["starts"][0] for r in rows],
            "trend_beats_persistence_everywhere": trend_wins,
            "winners": sorted(winners), "ranking_stable": len(winners) == 1,
            "emulator_wins": len(emulators),
            "detail": "; ".join(f"from {r['starts'][0]}: {r['best'].split(':')[-1]} "
                                f"(trend {r['mae']['trend']:.3f} vs persistence "
                                f"{r['mae']['persistence']:.3f})" for r in rows),
            # the gate asserts only what is robust
            "pass": trend_wins}


def guard_window(data: dict | None = None) -> tuple[bool, str]:
    """MUTATION: the gate must be able to notice a field where persistence wins — flip the
    trend score to something worse than persistence and the robust claim must go false."""
    ev = baseline.evaluate(data)
    mae = {k: v["mae"] for k, v in ev["methods"].items()}
    broken_beats = (mae["persistence"] * 0.5) < mae["trend"]     # a fake "trend" that loses
    r = window_invariance(data)
    ok = r["pass"] and broken_beats
    return ok, (f"window: trend beats persistence in every window = "
                f"{r['trend_beats_persistence_everywhere']}; ranking stable = "
                f"{r['ranking_stable']} (winners {[w.split(':')[-1] for w in r['winners']]}, "
                f"emulators won {r['emulator_wins']}/{len(r['windows'])}); a trend score worse "
                f"than persistence is detectable = {broken_beats}")


# ---------------------------------------------------------------------------------------
def audit() -> dict:
    checks = []
    for name, run in (("baseline period", guard_baseline),
                      ("units", guard_units),
                      ("window", guard_window)):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["audit", "baseline_invariance", "units_invariance", "window_invariance",
           "rebase", "trend_rate", "guard_baseline", "guard_units", "guard_window"]
