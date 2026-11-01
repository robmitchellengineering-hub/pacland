"""One board: what has actually been measured.

Three panels, because three different questions have three different answers:

  1. THE SHAPE — ten PDR walks, drift left in. It is a sketch and the closure figures say how much of a sketch.
  2. THE LEVELS — the strongest signal heard at each labelled spot. Direct measurements, no geometry.
  3. THE TEST THAT FAILED — signal against distance travelled, R^2 = 0.03: a walk that loops does not decay with
     distance, so a coverage map cannot be made from path length.

    python3 scripts/state_of_rf.py
"""
from __future__ import annotations

import json
import math
import pathlib
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "img" / "state-of-rf.png"


def main() -> int:
    walks = json.loads((ROOT / "docs/data/walks-2026-11-01.json").read_text())
    spots = json.loads((ROOT / "docs/data/spots-2026-11-01.json").read_text())

    fig = plt.figure(figsize=(19, 7), dpi=145)
    fig.patch.set_facecolor("#0d1117")
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)
    for a in (ax1, ax2, ax3):
        a.set_facecolor("#0d1117")
        a.tick_params(colors="#8b949e")
        for sp in a.spines.values():
            sp.set_color("#30363d")

    # 1 — the shapes
    closures = []
    for w in walks:
        s = w["samples"]
        x = np.array([p["x"] for p in s]); y = np.array([p["y"] for p in s])
        path = float(np.sum(np.hypot(np.diff(x), np.diff(y))))
        net = float(math.hypot(x[-1], y[-1]))
        ratio = net / path if path else 1.0
        if ratio < 0.5:
            closures.append(ratio)
        ax1.plot(x, y, linewidth=0.9, alpha=0.8)
    ax1.set_title(f"1. the shape — {len(closures)} loops, closure "
                  f"{min(closures):.0%}–{max(closures):.0%} (median {statistics.median(closures):.0%})",
                  color="#e6edf3", fontsize=11)
    ax1.set_xlabel("x (m)", color="#8b949e"); ax1.set_ylabel("y (m)", color="#8b949e")
    ax1.set_aspect("equal", adjustable="datalim")

    # 2 — the levels
    names = sorted(spots, key=lambda k: -spots[k])
    vals = [spots[n] for n in names]
    ax2.barh(range(len(names)), vals, color="#38bdf8")
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels([n[:22] for n in names], color="#e6edf3", fontsize=8)
    ax2.invert_yaxis()
    ax2.set_xlabel("strongest level at that spot (dBm)", color="#8b949e")
    ax2.set_title("2. the levels — measured, no geometry claimed", color="#e6edf3", fontsize=11)

    # 3 — the test that failed
    xs, ys = [], []
    for w in walks:
        s = w["samples"]
        d = [0.0]
        for i in range(1, len(s)):
            d.append(d[-1] + math.hypot(s[i]["x"] - s[i - 1]["x"], s[i]["y"] - s[i - 1]["y"]))
        xs.extend(d); ys.extend([p["rssi"] for p in s])
    xs, ys = np.array(xs), np.array(ys)
    r = float(np.corrcoef(xs, ys)[0, 1])
    ax3.scatter(xs, ys, s=4, c="#f0b429", alpha=0.35)
    ax3.set_xlabel("distance travelled along the walk (m)", color="#8b949e")
    ax3.set_ylabel("RSSI (dBm)", color="#8b949e")
    ax3.set_title(f"3. the test that failed — R² = {r*r:.2f}\nwalks loop, so distance travelled is not distance from the AP",
                  color="#e6edf3", fontsize=11)

    fig.suptitle(f"State of the RF work — 10 walks, {sum(len(w['samples']) for w in walks)} samples, "
                 f"{len(spots)} labelled spots", color="#e6edf3", fontsize=13)
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor=fig.get_facecolor())
    print("wrote", OUT.relative_to(ROOT), "| R2 =", round(r * r, 3))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
