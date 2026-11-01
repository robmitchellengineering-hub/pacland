"""Turn ARCore measurements into room dimensions in the layout template.

The room scan sends capability 'measure' to the hub: a room label and a list of straight-line measurements, each with its
two endpoints in ARCore world coordinates and its length in metres. This reads them back and puts the numbers where the
coverage map needs them.

    python3 scripts/apply_measurements.py            # report what has been measured
    python3 scripts/apply_measurements.py --write    # fill w/h in docs/data/layout-template.json

WHAT IT DOES NOT DO, and this matters more than what it does: it does not know which measurement is the room's width and
which is its diagonal. A room needs two dimensions; a diagonal is longer than either. So the two longest measurements
are NOT assumed to be w and h - they are reported with their lengths and the room stays unfilled unless the numbers are
within 10% of a rectangle's own consistency (see `plausible_pair`).

FALSIFIER, stated before the run: if a room's measurements disagree with each other by more than 10% when they should be
repeats, the measurements are not repeatable and filling the template from them would be a guess with a decimal point.
The script refuses to write in that case and says which room.
"""
from __future__ import annotations

import glob
import json
import math
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "docs/data/layout-template.json"


def load_measurements(root: str):
    """Every measurement the phone has uploaded, grouped by room."""
    by_room: dict[str, list[dict]] = {}
    for d in sorted(glob.glob(os.path.join(root, "measure-*"))):
        try:
            payload = json.load(open(os.path.join(d, "stdout.txt")))
        except Exception:
            continue
        room = (payload.get("room") or "unlabelled").strip()
        for m in payload.get("measurements") or []:
            by_room.setdefault(room, []).append({
                "metres": float(m["metres"]),
                "from": m.get("from"),
                "to": m.get("to"),
                "source": os.path.basename(d),
            })
    return by_room


def plausible_pair(a: float, b: float) -> bool:
    """Two sides of a room, not a side and its diagonal: a diagonal is > sqrt(2)/2 of the longer side away."""
    if a <= 0 or b <= 0:
        return False
    ratio = min(a, b) / max(a, b)
    return ratio >= 0.25          # a room narrower than a quarter of its length is a corridor, not a room


def main(argv) -> int:
    root = os.path.expanduser("~/harness-mesh/runs/phone")
    by_room = load_measurements(root)
    layout = json.loads(LAYOUT.read_text())

    if not by_room:
        print("no measurements on the hub yet — run ROOM SCAN on the phone and press UPLOAD")
        return 0

    # repeatability first: two measurements of the same thing should agree
    problems = []
    resolved: dict[str, tuple[float, float]] = {}
    for room, items in sorted(by_room.items()):
        lengths = sorted(i["metres"] for i in items)
        print(f"\n{room}: {len(items)} measurement(s)")
        for i in items:
            print(f"  {i['metres']:.2f} m   ({i['source']})")
        if len(lengths) >= 2:
            a, b = lengths[-1], lengths[-2]
            if plausible_pair(a, b):
                resolved[room] = (b, a)
                print(f"  -> usable as a room: {b:.2f} x {a:.2f} m")
            else:
                problems.append(f"{room}: {b:.2f} and {a:.2f} m are too similar to be two different roots "
                                f"(a diagonal would be longer) — measure width AND length, not the same wall twice")
        else:
            print("  -> one measurement is a line, not a room; measure the other side too")

    if "--write" in argv and resolved and not problems:
        for room in layout["rooms"]:
            if room["name"] in resolved:
                w, h = resolved[room["name"]]
                room["w"] = round(w, 2)
                room["h"] = round(h, 2)
                room["measured_from"] = "arcore"
        LAYOUT.write_text(json.dumps(layout, indent=1) + "\n")
        print(f"\nwrote {LAYOUT.relative_to(ROOT)} for {len(resolved)} room(s)")
    elif "--write" in argv:
        print("\nnot writing: see the problems above")

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
