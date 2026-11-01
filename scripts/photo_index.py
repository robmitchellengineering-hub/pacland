"""What photos exist, for which spot, and what a room needs.

The phone uploads photos to the hub as runs/phone/photo-*/photo.jpg with the spot label in stdout. This lists them per
spot, checks each is a real JPEG, and reports what is still missing for a room atlas: a photo per room, ideally showing
two corners so the wall lines can be found.

    python3 scripts/photo_index.py [path-to-harness-mesh-runs]

FALSIFIER, stated before the run: if a 'photo' has no JPEG magic bytes, or is smaller than 20 KB, it is not a usable
room image and is counted as missing rather than present.
"""
from __future__ import annotations

import glob
import json
import os
import pathlib
import struct
import sys


def jpeg_size(path: str):
    try:
        with open(path, "rb") as fh:
            data = fh.read()
        if data[:2] != b"\xff\xd8":
            return None
        i = 2
        while i < len(data) - 9:
            if data[i] == 0xFF and data[i + 1] in (0xC0, 0xC1, 0xC2):
                h = struct.unpack(">H", data[i + 5:i + 7])[0]
                w = struct.unpack(">H", data[i + 7:i + 9])[0]
                return w, h, len(data)
            i += 1
        return None
    except Exception:
        return None


def main(argv) -> int:
    root = argv[1] if len(argv) > 1 else os.path.expanduser("~/harness-mesh/runs/phone")
    by_spot: dict[str, list] = {}
    for d in sorted(glob.glob(os.path.join(root, "photo-*"))):
        photo = os.path.join(d, "photo.jpg")
        try:
            meta = json.load(open(os.path.join(d, "stdout.txt")))
        except Exception:
            meta = {}
        spot = meta.get("spot") or os.path.basename(d)
        size = jpeg_size(photo) if os.path.exists(photo) else None
        usable = bool(size) and size[2] > 20_000
        by_spot.setdefault(spot, []).append({"dir": os.path.basename(d), "size": size, "usable": usable})

    print(f"{'spot':<26}{'photos':>7}{'usable':>8}   largest")
    for spot in sorted(by_spot):
        items = by_spot[spot]
        usable = [x for x in items if x["usable"]]
        biggest = max((x["size"][2] for x in items if x["size"]), default=0)
        mark = "" if usable else "   <- not usable for a plan"
        print(f"{spot[:26]:<26}{len(items):>7}{len(usable):>8}   {biggest/1024:.0f} KB{mark}")

    total = sum(len(v) for v in by_spot.values())
    usable_n = sum(1 for v in by_spot.values() for x in v if x["usable"])
    print(f"\n{total} photos over {len(by_spot)} spots, {usable_n} usable")
    print("for a room atlas: 2-4 photos per room, landscape, two corners visible, phone level")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
