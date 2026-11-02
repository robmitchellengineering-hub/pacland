"""Put measured rooms somewhere, so the coverage map can exist before a floor plan does.

`apply_measurements.py` fills a room's `w` and `h` from ARCore. That is a SIZE, not a POSITION: the coverage map needs
x and y as well, and a room with no position cannot be drawn.

This places the rooms that have measurements in a **provisional** layout - a simple shelf pack, widest first, north to
south - and marks every room it touches with `placement: "provisional"`. The map drawn from it is therefore a real
statement about sizes and levels and a guess about where things are, and it says so on the figure.

    python3 scripts/place_rooms.py            # report only
    python3 scripts/place_rooms.py --write    # write x/y for measured rooms

FALSIFIER, stated before the run: if a provisional placement is ever presented as a floor plan, this script has done
harm. The check is that `coverage_map.py` refuses to hide the `provisional` flag - and it does, in its title.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "docs/data/layout-template.json"

SHELF_WIDTH = 12.0          # metres of shelf before wrapping to the next row
GAP = 0.0                   # rooms touch: walls are shared, and layout_check requires contact


def place(rooms: list[dict]) -> list[dict]:
    """Shelf-pack the rooms that have sizes, preserving the template's order."""
    sized = [r for r in rooms if r.get("w") and r.get("h")]
    x = y = 0.0
    shelf_h = 0.0
    for room in sized:
        if x + room["w"] > SHELF_WIDTH and x > 0:
            x = 0.0
            y += shelf_h
            shelf_h = 0.0
        room["x"] = round(x, 2)
        room["y"] = round(y, 2)
        room["placement"] = "provisional"
        x += room["w"] + GAP
        shelf_h = max(shelf_h, room["h"])
    return sized


def main(argv) -> int:
    layout_path = LAYOUT
    if "--layout" in argv:
        layout_path = pathlib.Path(argv[argv.index("--layout") + 1])
    layout = json.loads(layout_path.read_text())
    rooms = layout["rooms"]
    sized = [r for r in rooms if r.get("w") and r.get("h")]
    if not sized:
        print("no room has a measured size yet — run the room scan and apply_measurements first")
        return 0
    placed = place(rooms)
    print(f"{len(placed)} of {len(rooms)} rooms placed (PROVISIONAL - sizes measured, positions guessed)")
    for r in placed:
        print(f"  {r['name']:<34} {r['w']:.2f} x {r['h']:.2f} m at ({r['x']:.1f}, {r['y']:.1f})")
    print(f"\n{len(rooms) - len(placed)} room(s) still unmeasured and therefore unplaced")
    if "--write" in argv:
        layout["_note"] = ("x/y for measured rooms are PROVISIONAL (shelf-pack). Sizes are measured with ARCore; "
                           "positions are not.")
        layout_path.write_text(json.dumps(layout, indent=1) + "\n")
        print(f"wrote {layout_path}")
    else:
        print("(dry run - pass --write to record the provisional positions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
