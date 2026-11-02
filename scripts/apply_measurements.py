"""Turn ARCore measurements into room dimensions in the layout template.

The phone posts capability 'measure' with a room label and a list of straight-line measurements, each with its two
endpoints in ARCore world coordinates and its length in metres. This reads them back and puts the numbers where the
coverage map needs them.

    python3 scripts/apply_measurements.py [--root DIR] [--layout FILE] [--write]

THE RULE THAT SHAPES EVERYTHING HERE: **ARCore's world coordinates are per session.** Two scans have unrelated origins
and axes, so lengths from different sessions are unrelated numbers - they might even be the same wall measured twice. Every
comparison below happens inside ONE session, and a room is only resolved when that session gave it two usable walls.

A room needs three numbers, and the phone gives whatever was tapped, so measurements are sorted by DIRECTION:

  a WALL   is mostly horizontal (a hand-height wobble between the two ends is fine)
  a HEIGHT is mostly vertical
  anything else - a diagonal, or two points that drifted - is reported and NOT used
  a horizontal length beyond 1.6x the session's median horizontal is flagged as longer than the room can be

FALSIFIER, stated before the run: if two lengths from one session are used as a room while being the same line, the
output is an invention. `same_line` checks that from the coordinates, with a 5 cm tolerance in either direction.
"""
from __future__ import annotations

import difflib
import glob
import json
import math
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "docs/data/layout-template.json"

WALL_RATIO = 0.35          # vertical/horizontal below this is a wall
HEIGHT_RATIO = 1.2         # above this is a height
OUTLIER_FACTOR = 1.6       # longer than this many medians is not a wall of this room
SAME_LINE_TOL = 0.05       # metres


def load_measurements(root: str) -> dict[str, list[dict]]:
    """Every measurement the phone has uploaded, grouped by room, each tagged with the scan session it came from."""
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


def parts(m: dict) -> tuple[float, float]:
    """(horizontal, vertical) lengths: ARCore's Y is up, so the floor plane is X-Z."""
    a, b = m.get("from") or [0, 0, 0], m.get("to") or [0, 0, 0]
    d = [float(b[i]) - float(a[i]) for i in range(3)]
    return math.hypot(d[0], d[2]), abs(d[1])


def same_line(first: dict, second: dict, tol: float = SAME_LINE_TOL) -> bool:
    """True when two measurements join the SAME two points in world space - one wall measured twice."""
    def near(p, q) -> bool:
        return p is not None and q is not None and all(abs(float(p[i]) - float(q[i])) <= tol for i in range(3))

    return (near(first.get("from"), second.get("from")) and near(first.get("to"), second.get("to"))) or \
           (near(first.get("from"), second.get("to")) and near(first.get("to"), second.get("from")))


def classify(items: list[dict]) -> dict:
    """Walls, heights and suspects from ONE session's measurements."""
    horizontal = []
    for m in items:
        h, v = parts(m)
        if h > 1e-6 and v / h <= WALL_RATIO:
            horizontal.append(h)
    median = sorted(horizontal)[len(horizontal) // 2] if horizontal else 0.0

    walls, heights, suspect = [], [], []
    for m in items:
        h, v = parts(m)
        if h <= 0.05 and v <= 0.05:
            continue
        ratio = v / h if h > 1e-6 else float("inf")
        if ratio > HEIGHT_RATIO:
            heights.append(m)
        elif ratio <= WALL_RATIO:
            if median and h > OUTLIER_FACTOR * median:
                suspect.append(m)
            else:
                walls.append(m)
        else:
            suspect.append(m)
    walls.sort(key=lambda m: -m["metres"])
    heights.sort(key=lambda m: -m["metres"])
    return {"walls": walls, "heights": heights, "suspect": suspect, "median_horizontal": median}


def room_from_walls(walls: list[dict]) -> tuple[float, float] | None:
    """The two longest DISTINCT walls, or None when the session cannot give two."""
    if len(walls) < 2:
        return None
    first = walls[0]
    second = next((w for w in walls[1:] if not same_line(first, w)), None)
    if second is None:
        return None
    a, b = first["metres"], second["metres"]
    lo, hi = min(a, b), max(a, b)
    if lo / hi < 0.25:
        return None                  # a corridor rather than a room
    return lo, hi


def resolve_room(label: str, rooms: list[dict]) -> str | None:
    """Match a free-text label to a template room, or return None rather than guess."""
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


def main(argv) -> int:
    root = os.path.expanduser("~/harness-mesh/runs/phone")
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]
    layout_path = LAYOUT
    if "--layout" in argv:
        layout_path = pathlib.Path(argv[argv.index("--layout") + 1])
    layout = json.loads(layout_path.read_text())

    by_room = load_measurements(root)
    if not by_room:
        print("no measurements on the hub yet — run ROOM SCAN on the phone and press UPLOAD")
        return 0

    problems: list[str] = []
    resolved: dict[str, tuple[float, float]] = {}

    for room, items in sorted(by_room.items()):
        sessions: dict[str, list[dict]] = {}
        for m in items:
            sessions.setdefault(m["source"], []).append(m)
        print(f"\n{room}: {len(items)} measurement(s) in {len(sessions)} scan session(s)")

        best: tuple[float, float] | None = None
        best_source = ""
        for source, group in sorted(sessions.items()):
            cls = classify(group)
            print(f"  {source}: walls {[round(w['metres'], 2) for w in cls['walls']]}, "
                  f"heights {[round(h['metres'], 2) for h in cls['heights']]}, "
                  f"suspect {[round(s['metres'], 2) for s in cls['suspect']]}")
            for m in cls["suspect"]:
                h, v = parts(m)
                print(f"    ! {m['metres']:.2f} m used no direction that fits a room - not used as a wall"
                      f" (horizontal {h:.2f} m, vertical {v:.2f} m)")
            if cls["heights"]:
                top = cls["heights"][0]
                print(f"    height candidate: {top['metres']:.2f} m measured, vertical span {parts(top)[1]:.2f} m")
            else:
                spans = [(parts(m)[1], m) for m in group]
                best_span, best_m = max(spans) if spans else (0.0, None)
                if best_span >= 1.5:
                    print(f"    possible height: a vertical span of {best_span:.2f} m in the "
                          f"{best_m['metres']:.2f} m measurement - if that was floor to ceiling, the ceiling is "
                          f"{best_span:.2f} m")
            pair = room_from_walls(cls["walls"])
            if pair and (best is None or len(cls["walls"]) > 0):
                if best is None or pair[0] * pair[1] > best[0] * best[1]:
                    best, best_source = pair, source
        if best:
            resolved[room] = best
            print(f"  -> usable as a room: {best[0]:.2f} x {best[1]:.2f} m (from {best_source})")
        elif len(sessions) > 1:
            problems.append(f"{room}: no single scan session has two usable walls - ARCore's coordinates are per "
                            f"session, so measure both walls in one scan")
        else:
            problems.append(f"{room}: {len(items)} measurement(s) and not two walls among them - "
                            f"measure both walls in one scan")

    mapped: dict[str, tuple[float, float]] = {}
    if "--write" in argv and resolved and not problems:
        for label, dims in resolved.items():
            target = resolve_room(label, layout["rooms"])
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
        print(f"\nwrote {layout_path} for {len(mapped)} room(s)")
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
