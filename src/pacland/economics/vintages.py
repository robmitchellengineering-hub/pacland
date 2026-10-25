"""Real-time vintages — the data *as it was known*, and the guards that keep it honest.

A forecast evaluated on today's revised data is not an out-of-sample test: the revision
itself contains information the forecaster did not have (Meese–Rogoff 1983; Croushore–
Stark's real-time literature). So every forecast here may consume only observations that
had been *published* when the forecast was made.

The fixture (``data/economics/vintages.json``) is fetched from ALFRED's keyless graph
endpoint with an explicit ``vintage_date`` and committed, so the suite runs offline and
the numbers cannot drift without the fixture changing.

Pure stdlib.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[3] / "data" / "economics" / "vintages.json"


def parse_csv(text: str) -> dict[str, float]:
    """Parse an ALFRED graph CSV (``observation_date,<SERIES>_<vintage>``)."""
    lines = text.strip().splitlines()
    out: dict[str, float] = {}
    for row in lines[1:]:
        parts = row.split(",")
        if len(parts) != 2 or parts[1] in (".", "", "NA"):
            continue
        try:
            out[parts[0]] = float(parts[1])
        except ValueError:
            continue
    return out


@dataclass(frozen=True)
class Vintage:
    """One vintage: a date, and every series as published on that date."""

    as_of: str
    series: dict[str, dict[str, float]]

    def observations(self, series: str) -> list[tuple[str, float]]:
        return sorted(self.series.get(series, {}).items())

    def values(self, series: str) -> list[float]:
        return [v for _, v in self.observations(series)]

    def last(self, series: str) -> tuple[str, float] | None:
        obs = self.observations(series)
        return obs[-1] if obs else None


def load(path: Path | None = None) -> dict:
    return json.loads(Path(path or FIXTURE).read_text())


def vintages(data: dict) -> list[Vintage]:
    return [Vintage(as_of=a, series=s) for a, s in sorted(data["vintages"].items())]


def current(data: dict) -> dict[str, dict[str, float]]:
    """The *revised* (today's) values — the truth a real-time forecast is scored against."""
    return data["current"]


# --- guards ------------------------------------------------------------------


def guard_no_lookahead(vintage: Vintage) -> tuple[bool, str]:
    """Every observation in a vintage must predate the vintage date itself — the
    forecast was made on that date, so a later observation is an impossibility."""
    bad = []
    for series, obs in vintage.series.items():
        for date in obs:
            if date >= vintage.as_of:
                bad.append(f"{series}@{date}")
    ok = not bad
    return ok, (
        f"vintage {vintage.as_of}: {sum(len(o) for o in vintage.series.values())} observations, "
        f"{'no look-ahead' if ok else 'LOOK-AHEAD: ' + ', '.join(bad[:3])}"
    )


def guard_truth_is_not_input(history: list[tuple[str, float]], target: str) -> tuple[bool, str]:
    """A forecast may not be handed the realised target. Fails when the input series
    already contains the date being forecast — the seeded fault this guard exists to
    catch (evaluating a 'forecast' against data it was fitted on)."""
    ok = all(d != target for d, _ in history)
    return ok, (
        f"input ends {history[-1][0] if history else '—'}, target {target}: "
        f"{'clean' if ok else 'TARGET LEAKED INTO THE INPUT'}"
    )


def guard_benchmark_present(results: dict) -> tuple[bool, str]:
    """A skill claim without the no-change null in the same table is refused: the null
    is the unit the model is measured in, not an optional extra."""
    ok = "no-change" in results
    return ok, f"benchmark present: {'no-change' in results} (results: {sorted(results)})"
