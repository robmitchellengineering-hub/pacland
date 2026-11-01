"""Attach the photos that have arrived to the rooms in the layout, and say what is still missing.

Tomorrow's photos should land in the template without anyone copying file names by hand: the phone already tags each
photo with the spot label, so the match is that label.

    python3 scripts/photo_glue.py [--write]

Without `--write` it only reports. With it, each matched room's `photos` list is filled with the hub directory names and
the file is rewritten. Rooms with no photo are listed, because those are the ones that cannot be measured yet.
"""
from __future__ import annotations

import glob
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "docs/data/layout-template.json"


def hub_photos(root: str):
    out = []
    for d in sorted(glob.glob(os.path.join(root, "photo-*"))):
        try:
            meta = json.load(open(os.path.join(d, "stdout.txt")))
        except Exception:
            continue
        photo = os.path.join(d, "photo.jpg")
        size = os.path.getsize(photo) if os.path.exists(photo) else 0
        out.append({"id": os.path.basename(d), "spot": (meta.get("spot") or "").strip(), "bytes": size})
    return out


def main(argv) -> int:
    root = os.path.expanduser("~/harness-mesh/runs/phone")
    photos = [p for p in hub_photos(root) if p["bytes"] > 20_000]
    layout = json.loads(LAYOUT.read_text())

    by_spot: dict[str, list[str]] = {}
    for p in photos:
        by_spot.setdefault(p["spot"].lower(), []).append(p["id"])

    matched, missing = 0, []
    for room in layout["rooms"]:
        key = room["name"].lower()
        found = []
        for spot, ids in by_spot.items():
            if spot and (spot in key or key in spot):
                found += ids
        if found:
            room["photos"] = sorted(set(found))
            matched += 1
        else:
            missing.append(room["name"])

    print(f"{len(photos)} usable photos on the hub, {matched} rooms matched, {len(missing)} rooms with none")
    for name in missing:
        print("  no photo:", name)

    if "--write" in argv:
        LAYOUT.write_text(json.dumps(layout, indent=1) + "\n")
        print(f"wrote {LAYOUT.relative_to(ROOT)}")
    else:
        print("(dry run - pass --write to record the matches)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
