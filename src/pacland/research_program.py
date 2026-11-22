"""research_program.py — the four competing mass-gap tracks + the ONE metric.

This is the "competing programmes" structure the master document calls for. The four tracks (Gribov,
Coulomb, RG, Curvature) each bet on a different heavy-lifting assumption; the ONE metric is how many of
the assumptions A1–A5 each track's best candidate bound currently satisfies. SEXTANT's job is to run all
four and report which one is closest to 5/5.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

# The five heavy-lifting assumptions. The missing uniformity is A1 + A3.
ASSUMPTIONS = {
    "A1": "volume-uniformity: the bound holds uniformly as V → ∞",
    "A2": "β-uniformity: the bound holds at every coupling, not just strong or weak",
    "A3": "continuum survival: the lattice bound transfers as a → 0",
    "A4": "spectral positivity: m > 0, not merely 'bounded'",
    "A5": "non-perturbativity: not a truncated expansion",
}


@dataclass
class Track:
    id: str
    name: str
    heavy_lifting: tuple[str, ...]   # the assumptions THIS track must prove
    objective: str
    falsification: str
    repo_assets: tuple[str, ...]


TRACKS: list[Track] = [
    Track(
        id="gribov", name="Gribov (gauge-orbit geometry)",
        heavy_lifting=("A4", "A5"),
        objective="a volume-uniform, non-perturbative lower bound from the Gribov–Zwanziger horizon",
        falsification="a residual Gribov copy / a horizon that does not yield m > 0",
        repo_assets=("GaugeOrbit.lean", "sextant.py gauge-orbit falsifier"),
    ),
    Track(
        id="coulomb", name="Coulomb (string tension)",
        heavy_lifting=("A1", "A3", "A4"),
        objective="a proved uniform lower bound on σ(β), so m = 3.2·√σ gives the gap",
        falsification="a Wilson loop violating the area law / σ(β) → 0 (the U(1) Coulomb phase)",
        repo_assets=("lattice_ym_su2.py", "lattice_ym_su3.py", "mass_gap_falsifiers.py"),
    ),
    Track(
        id="rg", name="RG (multiscale Polchinski flow)",
        heavy_lifting=("A1", "A3", "A5"),
        objective="a uniform bound on the flow's curvature → a scale-uniform mass-gap bound",
        falsification="a flow/truncation where the curvature diverges (couplings run away)",
        repo_assets=("energy/frg.py", "energy/frg_poly.py", "energy/referee.py"),
    ),
    Track(
        id="curvature", name="Curvature / functional inequalities",
        heavy_lifting=("A2", "A4", "A5"),
        objective="Wang's criterion / a weighted spectral inequality that is β-uniform",
        falsification="negative curvature on a measure-non-negligible set",
        repo_assets=("Su2Curvature.lean", "hypotheses.py"),
    ),
]


def track_by_id(track_id: str) -> Track:
    for t in TRACKS:
        if t.id == track_id:
            return t
    raise KeyError(f"unknown track {track_id!r}; known: {[t.id for t in TRACKS]}")


def track_score(track_id: str, satisfied: set[str]) -> int:
    """How many of the track's heavy-lifting assumptions its best candidate bound satisfies."""
    t = track_by_id(track_id)
    return len(set(t.heavy_lifting) & set(satisfied))


def track_max(track_id: str) -> int:
    """The number of heavy-lifting assumptions the track must prove (its 'full' score)."""
    return len(track_by_id(track_id).heavy_lifting)


def leaderboard(satisfied_by_track: dict[str, set[str]]) -> list[dict]:
    """Rank the tracks by fraction of their heavy-lifting assumptions cleared (closest to 1.0 first)."""
    rows = []
    for t in TRACKS:
        cleared = track_score(t.id, satisfied_by_track.get(t.id, set()))
        mx = track_max(t.id)
        rows.append({
            "track": t.id, "name": t.name,
            "cleared": cleared, "of": mx,
            "fraction": cleared / mx if mx else 0.0,
            "missing": sorted(set(t.heavy_lifting) - set(satisfied_by_track.get(t.id, set()))),
        })
    rows.sort(key=lambda r: -r["fraction"])
    return rows


def report(satisfied_by_track: dict[str, set[str]]) -> dict:
    """The race report: the leaderboard + who is closest to the result."""
    lb = leaderboard(satisfied_by_track)
    return {
        "metric": "closeness to a volume-uniform lower bound for the YM spectral gap",
        "leaderboard": lb,
        "leader": lb[0]["track"] if lb else None,
        "any_full": any(r["cleared"] == r["of"] for r in lb),
    }
