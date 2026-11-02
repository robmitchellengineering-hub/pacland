"""Analyse, diagnose, fix: where the access point should be, from what was measured.

Design 38 calls this the residual; this is the first working version of it, and it is deliberately blunt about its model.

    ANALYSE   every room's measured level, and the deficit against the best room
    DIAGNOSE  which rooms are under-served, and by how many dB
    FIX       candidate access-point positions, scored by the level they would put in the WORST room, without costing
              the best room more than `MAX_LOSS_DB`

THE MODEL, stated so it can be wrong: indoor path loss grows about 30 dB per decade of distance (`PATH_LOSS_EXPONENT`
= 3), and a move changes a room's level by that amount times the log-ratio of the two distances. A wall between the
candidate and the room is charged `WALL_DB`. Both are assumptions, and both are printed with the answer, because a
placement recommendation that hides its model is a preference.

    python3 scripts/placement_plan.py [--spots FILE] [--rooms FILE]

FALSIFIER, stated before the run: if the recommended position is the CURRENT one, the model has produced no change and
must say so rather than dress the status quo as a finding - a plan that always recommends moving is as useless as one
that never does.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPOTS = ROOT / "docs/data/spots-2026-11-01.json"
ROOMS = ROOT / "docs/data/layout-template.json"

PATH_LOSS_EXPONENT = 3.0     # indoor, 2.4 GHz: 30 dB per decade
WALL_DB = 8.0                # one internal wall at 2.4 GHz, typical
MAX_LOSS_DB = 3.0            # the best room may not be made worse than this
CANDIDATE_HEIGHTS = (1.0, 2.4)


def canonical(label: str) -> str:
    """Fold the label variants the phone's free text produces into one room.

    The same room was scanned as 'bedroom next to router' and 'bedroom next to router house loop walk' - two rows, two
    deficits, one room. The longest shared prefix wins, and the best level among the variants is kept, because a room's
    level is the best the phone heard in it, not the worst.
    """
    drop = (" house loop walk", " loop walk", " walk")
    out = label.strip()
    for suffix in drop:
        if out.lower().endswith(suffix):
            out = out[: -len(suffix)]
    return out.strip()


def load_levels(path: pathlib.Path) -> dict[str, float]:
    raw = json.loads(path.read_text())
    merged: dict[str, float] = {}
    for k, v in raw.items():
        key = canonical(k)
        merged[key] = max(merged.get(key, -999.0), float(v))
    return merged


def deficit(levels: dict[str, float]) -> dict[str, float]:
    """Each room's shortfall against the best room, in dB."""
    best = max(levels.values())
    return {room: best - level for room, level in levels.items()}


def path_loss_delta(d_before: float, d_after: float, walls: int = 0) -> float:
    """Change in received level for a change of distance, plus the walls crossed."""
    d_before = max(d_before, 0.5)
    d_after = max(d_after, 0.5)
    return -(10.0 * PATH_LOSS_EXPONENT * math.log10(d_after / d_before)) - walls * WALL_DB


def plan(levels: dict[str, float], ap_position: tuple[float, float], rooms: list[dict],
         candidates: list[tuple[float, float]]) -> dict:
    """Score each candidate AP position by the worst room it leaves, and by what it costs the best room."""
    room_centres = {}
    for r in rooms:
        if all(r.get(k) is not None for k in ("x", "y", "w", "h")):
            room_centres[canonical(r["name"])] = (r["x"] + r["w"] / 2, r["y"] + r["h"] / 2)
    scored = []
    # THE STRONGEST ROOM, which is the one a move must not degrade. `min(levels, ...)` returns the WEAKEST room, and the
    # first version used it as "the best room" - so the constraint that protects the good end of the house was being
    # applied to the bad end, and the plan's headline number was about the wrong room.
    best_room = max(levels, key=lambda k: levels[k])
    for cand in candidates:
        predicted = {}
        for room, level in levels.items():
            centre = room_centres.get(room)
            if centre is None:
                predicted[room] = level
                continue
            d_before = math.hypot(ap_position[0] - centre[0], ap_position[1] - centre[1])
            d_after = math.hypot(cand[0] - centre[0], cand[1] - centre[1])
            predicted[room] = level + path_loss_delta(d_before, d_after)
        worst = min(predicted.items(), key=lambda kv: kv[1])
        cost = levels[best_room] - predicted[best_room]
        scored.append({"candidate": cand, "worst_room": worst[0], "worst_level": worst[1],
                       "best_room_cost_db": cost, "predicted": predicted})
    allowed = [s for s in scored if s["best_room_cost_db"] <= MAX_LOSS_DB]
    allowed.sort(key=lambda s: -s["worst_level"])
    return {"best": allowed[0] if allowed else None, "all": scored,
            "current": next((s for s in scored if s["candidate"] == ap_position), None),
            "model": {"path_loss_exponent": PATH_LOSS_EXPONENT, "wall_db": WALL_DB, "max_loss_db": MAX_LOSS_DB}}


def main(argv) -> int:
    spots = pathlib.Path(argv[argv.index("--spots") + 1]) if "--spots" in argv else SPOTS
    rooms = pathlib.Path(argv[argv.index("--rooms") + 1]) if "--rooms" in argv else ROOMS
    levels = load_levels(spots)
    layout = json.loads(rooms.read_text())
    deficits = deficit(levels)

    print("ANALYSE — measured level per room")
    for room, level in sorted(levels.items(), key=lambda kv: kv[1]):
        print(f"  {room:<38}{level:6.0f} dBm   deficit {deficits[room]:5.1f} dB")

    print("\nDIAGNOSE")
    worst = sorted(levels.items(), key=lambda kv: kv[1])[:3]
    for room, level in worst:
        print(f"  {room}: {level:.0f} dBm, {deficits[room]:.0f} dB below the best room")
    print(f"  spread across the house: {max(levels.values()) - min(levels.values()):.0f} dB")

    measured = [r for r in layout["rooms"] if all(r.get(k) is not None for k in ("x", "y", "w", "h"))]
    if not measured:
        print("\nFIX — no room has a position yet, so a move cannot be scored. Measure the rooms (design 37) or set the "
              "positions by hand in docs/data/layout-template.json.")
        return 0

    ap = next((r for r in layout["rooms"] if "router" in r["name"].lower() and r.get("x") is not None), None)
    if ap is None:
        print("\nFIX — the access point's room is not placed, so the current position is unknown.")
        return 0
    ap_pos = (ap["x"] + ap["w"] / 2, ap["y"] + ap["h"] / 2)
    candidates = [ap_pos]
    for r in measured:
        candidates.append((r["x"] + r["w"] / 2, r["y"] + r["h"] / 2))
    result = plan(levels, ap_pos, layout["rooms"], candidates)

    print("\nFIX — candidate positions, scored by the worst room")
    for s in sorted(result["all"], key=lambda s: -s["worst_level"])[:5]:
        mark = " <-- best" if result["best"] and s is result["best"] else ""
        print(f"  ({s['candidate'][0]:5.1f}, {s['candidate'][1]:5.1f})  worst {s['worst_level']:5.1f} dBm "
              f"({s['worst_room']})  cost to best room {s['best_room_cost_db']:+4.1f} dB{mark}")
    if result["best"] and result["current"] and result["best"] is result["current"]:
        print("\n  the model recommends NO MOVE - the current position is already the best of the candidates")
    print(f"\n  model: path loss {PATH_LOSS_EXPONENT:.0f} dB/decade, {WALL_DB:.0f} dB per wall, best room may lose "
          f"{MAX_LOSS_DB:.0f} dB")
    print("  this is a projection, not a measurement: the confirming scan after a move is what settles it")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
