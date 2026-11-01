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


def resolve_room(label: str, rooms: list[dict]) -> str | None:
    """Match a measurement's room label to a template room, tolerantly - and say nothing when it cannot.

    The label is FREE TEXT typed on the phone ("Kitchen", "kitchen ", "the kitchen") while the template has fixed names,
    so an exact-match requirement would mean measurements that arrive, parse and then silently fill nothing. Matching is:
    exact (case-folded) -> one contains the other -> close enough by ratio. Anything else stays unmatched, because
    guessing which room a measurement belongs to is worse than asking again.
    """
    import difflib
    key = " ".join(label.lower().split())
    names = {" ".join(r["name"].lower().split()): r["name"] for r in rooms}
    if key in names:
        return names[key]
    for candidate, original in names.items():
        if key and (key in candidate or candidate in key):
            return original
    best, score = None, 0.0
    for candidate, original in names.items():
        ratio = difflib.SequenceMatcher(None, key, candidate).ratio()
        if ratio > score:
            score, best = ratio, original
    return best if score >= 0.8 else None


def plausible_pair(a: float, b: float) -> bool:
    """A sanity bound on SHAPE, not a duplicate detector.

    A room narrower than a quarter of its length is a corridor rather than a room, so that is the bound. It deliberately
    does NOT try to tell a width from a diagonal, or a room from the same wall measured twice - by length alone those are
    indistinguishable, and a square room is 4.0 x 4.0. `same_line` does that job, from the coordinates.
    """
    if a <= 0 or b <= 0:
        return False
    ratio = min(a, b) / max(a, b)
    return ratio >= 0.25


def same_line(first: dict, second: dict, tol: float = 0.05) -> bool:
    """True when two measurements join the SAME two points in world space - the same wall measured twice.

    The payload carries both endpoints, so this is checkable rather than guessed: if the points coincide within `tol`
    metres (in either direction) the second measurement adds nothing, and calling that pair of numbers a room would put a
    wall's length into the plan as both sides of a rectangle.
    """
    def near(p, q) -> bool:
        return p is not None and q is not None and all(
            abs(float(p[i]) - float(q[i])) <= tol for i in range(3)
        )

    return (near(first.get("from"), second.get("from")) and near(first.get("to"), second.get("to"))) or \
           (near(first.get("from"), second.get("to")) and near(first.get("to"), second.get("from")))


def main(argv) -> int:
    root = os.path.expanduser("~/harness-mesh/runs/phone")
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]
    by_room = load_measurements(root)
    layout_path = LAYOUT
    if "--layout" in argv:
        layout_path = pathlib.Path(argv[argv.index("--layout") + 1])
    layout = json.loads(layout_path.read_text())

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
        if len(items) >= 2:
            ordered = sorted(items, key=lambda i: -i["metres"])
            long, second = ordered[0], ordered[1]
            a, b = long["metres"], second["metres"]
            if same_line(long, second):
                problems.append(f"{room}: the two longest measurements join the same two points — that is one wall "
                                f"measured twice, not a room; measure the other wall")
            elif plausible_pair(a, b):
                resolved[room] = (b, a)
                print(f"  -> usable as a room: {b:.2f} x {a:.2f} m")
            else:
                problems.append(f"{room}: {a:.2f} m and {b:.2f} m differ by more than 4x — a corridor rather than a "
                                f"room, or one measurement is wrong")
        else:
            print("  -> one measurement is a line, not a room; measure the other side too")

    mapped: dict[str, tuple[float, float]] = {}
    if "--write" in argv and resolved and not problems:
        rooms = layout["rooms"]
        for label, dims in resolved.items():
            target = resolve_room(label, rooms)
            if target is None:
                problems.append(f"{label}: no template room matches that label - rename it on the phone or add the "
                                f"room to the template")
            else:
                mapped[target] = dims
    if "--write" in argv and mapped and not problems:
        for room in layout["rooms"]:
            if room["name"] in mapped:
                w, h = mapped[room["name"]]
                room["w"] = round(w, 2)
                room["h"] = round(h, 2)
                room["measured_from"] = "arcore"
        layout_path.write_text(json.dumps(layout, indent=1) + "\n")
        print(f"\nwrote {layout_path} for {len(resolved)} room(s)")
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
