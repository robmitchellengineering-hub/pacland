"""Check a room layout before a coverage map is drawn on it.

An invented or half-filled layout produces a confident-looking picture with nothing behind it, which is the easiest
kind of wrong to publish. This refuses to be quiet about it:

  * every room needs four numbers, or it is not placed
  * rooms must not overlap (a wall in two places is two rooms drawn over each other)
  * rooms must not float apart (a house whose rooms do not touch is a diagram, not a plan)
  * areas must be plausible for the room's name

    python3 scripts/layout_check.py docs/data/layout-template.json

FALSIFIER, stated before the run: a layout that passes every check here can still be the WRONG house. These are
consistency checks, not measurements - they catch an invented or half-filled plan, and they say nothing about whether
the dimensions match the building.
"""
from __future__ import annotations

import json
import pathlib
import sys

PLAUSIBLE = {
    "bathroom": (2.0, 12.0),
    "kitchen": (4.0, 30.0),
    "hallway": (2.0, 30.0),
    "bedroom": (7.0, 40.0),
    "lounge": (8.0, 60.0),
    "loungeroom": (8.0, 60.0),
    "tv": (6.0, 40.0),
    "office": (5.0, 30.0),
}


def overlaps(a, b) -> bool:
    return not (a["x"] + a["w"] <= b["x"] or b["x"] + b["w"] <= a["x"]
                or a["y"] + a["h"] <= b["y"] or b["y"] + b["h"] <= a["y"])


def touches(a, b, tol=0.01) -> bool:
    """True when the two rooms share a boundary (they are side by side or end to end)."""
    x_gap = max(a["x"], b["x"]) - min(a["x"] + a["w"], b["x"] + b["w"])
    y_gap = max(a["y"], b["y"]) - min(a["y"] + a["h"], b["y"] + b["h"])
    return (abs(x_gap) <= tol and y_gap < -tol) or (abs(y_gap) <= tol and x_gap < -tol)


def main(argv) -> int:
    path = pathlib.Path(argv[1] if len(argv) > 1 else "docs/data/layout-template.json")
    layout = json.loads(path.read_text())
    rooms = layout["rooms"]
    problems = []

    placed, unplaced = [], []
    for r in rooms:
        if all(r.get(k) is not None for k in ("x", "y", "w", "h")):
            placed.append(r)
        else:
            unplaced.append(r["name"])

    print(f"{len(rooms)} rooms: {len(placed)} placed, {len(unplaced)} unplaced")
    if unplaced:
        problems.append(f"{len(unplaced)} rooms have no position: {', '.join(unplaced[:6])}"
                        + (" ..." if len(unplaced) > 6 else ""))

    for i, a in enumerate(placed):
        for b in placed[i + 1:]:
            if overlaps(a, b):
                problems.append(f"{a['name']} overlaps {b['name']}")
            elif not any(touches(a, c) for c in placed if c is not a):
                pass  # checked below, once

    for a in placed:
        if not any(touches(a, b) for b in placed if b is not a):
            problems.append(f"{a['name']} touches no other room (it floats)")

    for r in placed:
        area = r["w"] * r["h"]
        for key, (lo, hi) in PLAUSIBLE.items():
            if key in r["name"].lower():
                if not lo <= area <= hi:
                    problems.append(f"{r['name']}: {area:.1f} m^2 is outside the plausible {lo}-{hi} m^2 for that room")
                break
        if r["w"] <= 0 or r["h"] <= 0:
            problems.append(f"{r['name']} has a non-positive dimension")

    if problems:
        print("\nNOT READY:")
        for p in problems:
            print("  -", p)
        return 1

    total = sum(r["w"] * r["h"] for r in placed)
    print(f"\nREADY: {len(placed)} rooms, {total:.1f} m^2 total, no overlaps, everything touching")
    print("Note: consistency only. Whether these ARE the house's dimensions is not checkable from here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
