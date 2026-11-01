"""The coverage map, ready for a frame — and run here on an ASSUMED layout to show what the frame buys.

Nothing in this script needs a floor plan to exist; it needs one to be TRUE. The layout below is invented, clearly
marked, and exists so that the moment a real sketch or photo-derived plan arrives, the map is a data file away rather
than a project away.

    python3 scripts/coverage_map.py

Input: a layout JSON (rooms as rectangles in metres), the labelled spot levels, and the walk samples.
Output: a 2D map with each room coloured by the measured level, plus the walk paths laid over it.

FALSIFIER, stated before the run: on an invented layout the room-level colours are a DEMONSTRATION of the pipeline and
carry no information about Rob's house. The script says so on the figure, because a picture that looks like a result
is the easiest thing in this project to mistake for one.
"""
from __future__ import annotations

import json
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "docs" / "data" / "layout-assumed.json"
SPOTS = ROOT / "docs" / "data" / "spots-2026-11-01.json"
WALKS = ROOT / "docs" / "data" / "walks-2026-11-01.json"
OUT = ROOT / "docs" / "img" / "coverage-map.png"


def main() -> int:
    layout = json.loads(LAYOUT.read_text())
    spots = json.loads(SPOTS.read_text())
    walks = json.loads(WALKS.read_text())

    fig, ax = plt.subplots(figsize=(13, 9), dpi=145)
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")
    ax.tick_params(colors="#8b949e")
    for sp in ax.spines.values():
        sp.set_color("#30363d")

    # MATCH LABELS TO ROOMS BY OVERLAP, not by first word. The first version matched 'bedroom' to whichever bedroom
    # came first in the dict, and missed 'lougeroom' entirely because the room is spelled 'loungeroom'. A prefix match
    # is not a matcher.
    import difflib
    def level_for(room):
        best, score = None, 0.0
        for label, v in spots.items():
            r = difflib.SequenceMatcher(None, room.lower(), label.lower()).ratio()
            if r > score:
                score, best = r, v
        return best if score > 0.45 else None

    cmap = plt.cm.plasma
    norm = plt.Normalize(-70, -25)
    for room in layout["rooms"]:
        v = level_for(room["name"])
        x, y, w, h = room["x"], room["y"], room["w"], room["h"]
        colour = cmap(norm(v)) if v is not None else "#1c2128"
        ax.add_patch(Rectangle((x, y), w, h, facecolor=colour, edgecolor="#30363d", linewidth=1.2, alpha=0.85))
        ax.text(x + w / 2, y + h / 2,
                f"{room['name']}\n{v:.0f} dBm" if v is not None else f"{room['name']}\nno spot measured",
                ha="center", va="center", color="#e6edf3", fontsize=9)

    # THE WALK PATHS ARE DELIBERATELY NOT DRAWN. They have shape but no position: they start at their own origin with
    # their own heading and ±18% drift, so putting them on a metric floor plan would be a lie with a legend. Drawing
    # nothing is the honest rendering of that fact.

    provisional = [r["name"] for r in layout["rooms"] if r.get("placement") == "provisional"]
    title_prefix = ("Coverage map — PROVISIONAL PLACEMENT\n"
                    "sizes measured with ARCore; room positions are a shelf-pack, not a floor plan\n"
                    if provisional else "")
    ax.set_title(
        title_prefix +
        "Coverage map — PIPELINE DEMONSTRATION ON AN INVENTED LAYOUT\n"
        "room positions here are made up; the dBm values are the real measurements from 12 spots",
        color="#e6edf3", fontsize=12)
    ax.set_xlabel("x (m)", color="#8b949e")
    ax.set_ylabel("y (m)", color="#8b949e")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.5, 12.5); ax.set_ylim(-0.5, 8)
    ax.text(0.01, -0.09, "the ten walk paths are not shown: they have shape but no position, so they cannot be "
            "placed on a metric plan", transform=ax.transAxes, color="#8b949e", fontsize=8)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    plt.colorbar(sm, ax=ax, label="strongest level measured (dBm)")
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor=fig.get_facecolor())
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
