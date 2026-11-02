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
# A ROOM'S LONG WALL IS NOT AN OUTLIER. The first version rejected any wall longer than 1.6x the session's median, which is
# exactly what a rectangular room looks like when two of its three measured lines are the short ones: a 3.85 x 2.24 m room
# measured as 2.14, 2.24, 3.85 had its LONGEST wall thrown out as a suspect, and the room came back as 2.14 x 2.24.
# The bound is now absolute (no room in this programme is longer than this) plus a ratio that only applies when there are
# enough walls for a median to mean anything.
MAX_WALL_M = 15.0
#: A line shorter than this is a door, a window or a partial drag - not a wall. The 1.14 m line in a 5 x 5 m room was
#: being treated as one of the room's dimensions.
MIN_WALL_M = 1.5
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
            if h > MAX_WALL_M or (walls and h > 3.0 * min(w["metres"] for w in walls)):
                suspect.append(m)
            else:
                walls.append(m)
        else:
            suspect.append(m)
    walls.sort(key=lambda m: -m["metres"])
    heights.sort(key=lambda m: -m["metres"])
    # THE DIAGONAL BOUND WAS TRIED AND REMOVED. It rejected the bedroom's impossible 5.98 m line (diagonal 3.74 m) and also
    # rejected the spare room's 3.85 m wall (diagonal of its two short walls 3.10 m), turning one correct room into a
    # 2.14 x 2.24 m one. A rule that fixes one session by breaking another is not a rule; both sessions are ambiguous
    # about which line is a wall, and the answer is more measurements, not a tighter bound.
    walls = [w for w in walls if w["metres"] >= MIN_WALL_M]
    return {"walls": walls, "heights": heights, "suspect": suspect, "median_horizontal": median}


def drop_impossible_walls(walls: list[dict]) -> tuple[list[dict], list[dict]]:
    """A WALL CANNOT BE LONGER THAN THE ROOM'S DIAGONAL.

    A session in the 2.62 x 2.67 m bedroom carried a 5.98 m line classified as a wall: the room's own diagonal is 3.74 m, so
    no wall of that room can be 5.98 m. The line is a mis-tap or a walk across two walls; either way it is not a wall, and
    admitting it turned the bedroom into a 2.67 x 5.98 m room that does not exist.

    The bound is the diagonal of the two SHORTEST distinct walls - the smallest room those walls could enclose - and it is
    generous by 5% so a real long wall is not lost to rounding.
    """
    if len(walls) < 3:
        return walls, []
    ordered = sorted(walls, key=lambda w: w["metres"])
    a, b = ordered[0]["metres"], ordered[1]["metres"]
    diag = (a * a + b * b) ** 0.5
    keep = [w for w in walls if w["metres"] <= diag * 1.05]
    dropped = [w for w in walls if w["metres"] > diag * 1.05]
    if len(keep) < 2:
        return walls, []
    return keep, dropped


def room_from_walls(walls: list[dict]) -> tuple[float, float] | None:
    """The two longest DISTINCT walls, or None when the session cannot give two.

    THE DOCSTRING WAS RIGHT AND THE CODE WAS NOT. It said "the two longest", and it took `walls[0]` - the first one measured -
    and the first line that was not the same line. Sessions are uploaded in measurement order, so "first" is whatever the
    phone happened to record first, not the longest.
    """
    if len(walls) < 2:
        return None
    ordered = sorted(walls, key=lambda w: -w["metres"])
    first = ordered[0]
    second = next((w for w in ordered[1:] if not same_line(first, w)), None)
    if second is None:
        return None
    a, b = first["metres"], second["metres"]
    lo, hi = min(a, b), max(a, b)
    if lo / hi < 0.25:
        return None                  # a corridor rather than a room
    return lo, hi


def pairing_alternatives(walls: list[dict]) -> list[tuple[float, float]]:
    """The room candidates a session supports, when more than one is defensible.

    Two sessions with three walls each are the reason this exists:

        bedroom   2.62, 2.67, 5.98 (+ 2.74)   - a 2.62 x 2.67 room whose diagonal is 3.74, plus a 5.98 m line
        spare     2.14, 2.24, 3.85 (+ 2.70)   - a 2.14 x 2.24 room, or a 2.24 x 3.85 one

    **No geometric rule separates them.** A diagonal bound rejects the bedroom's 5.98 and also the spare room's genuine
    3.85; a ceiling multiple can be tuned to two sessions and is then fitted, not derived. So the honest output is BOTH
    candidates, and the decision goes where the evidence is: the operator knows which room it is, and a fourth wall settles
    it without asking anybody.
    """
    if len(walls) < 3:
        return []
    ordered = sorted(walls, key=lambda w: -w["metres"])
    out = []
    seen = set()
    for i, first in enumerate(ordered):
        for second in ordered[i + 1:]:
            if same_line(first, second):
                continue
            key = (round(min(first["metres"], second["metres"]), 2), round(max(first["metres"], second["metres"]), 2))
            if key in seen:
                continue
            seen.add(key)
            out.append(key)
    return out


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
