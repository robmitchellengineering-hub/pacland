"""What ten walks actually establish — and the one number that survives.

Ten PDR walks, 1069 samples. Eight were loops (they returned near their start) and two were one-way, which is not a
failure: a walk that goes somewhere and stops cannot close.

The honest findings, in the order they matter:

  1. LOOP CLOSURE is 9.3% to 25.1% of path, median 17.6%. That is the drift of this phone's dead reckoning.
  2. A CONSTANT-DRIFT MODEL DOES NOT FIX IT. Fitting a yaw bias and a scale to close each loop drives the parameters
     to the edges of the search range and still leaves 5-70% - i.e. there is no interior solution. The drift is not a
     constant, so it cannot be calibrated away.
  3. WHAT DOES SURVIVE IS THE SIGNAL PROFILE: RSSI against distance travelled, consistent across all ten walks.

So the deliverable is the profile, with the geometry marked as what it is.

    python3 scripts/house_from_walks.py

FALSIFIER, stated before the run: if the ten RSSI-versus-distance curves do not agree with each other, the profile is
not a property of the house either, and this dataset supports only the per-spot levels - nothing about distance.
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
DATA = ROOT / "docs" / "data" / "walks-2026-11-01.json"
OUT = ROOT / "docs" / "img" / "house-from-walks.png"


def classify(walk):
    s = walk["samples"]
    path = sum(math.hypot(s[i]["x"] - s[i - 1]["x"], s[i]["y"] - s[i - 1]["y"]) for i in range(1, len(s)))
    net = math.hypot(s[-1]["x"], s[-1]["y"])
    return path, net, (net / path if path else 1.0)


def cumulative(s):
    d = [0.0]
    for i in range(1, len(s)):
        d.append(d[-1] + math.hypot(s[i]["x"] - s[i - 1]["x"], s[i]["y"] - s[i - 1]["y"]))
    return d


def main() -> int:
    walks = json.loads(DATA.read_text())
    fig, ax = plt.subplots(1, 2, figsize=(16, 7), dpi=150)
    fig.patch.set_facecolor("#0d1117")
    for a in ax:
        a.set_facecolor("#0d1117")
        a.tick_params(colors="#8b949e")
        for sp in a.spines.values():
            sp.set_color("#30363d")

    print(f"{'walk':<40}{'path':>7}{'net':>7}{'type':>9}{'closure':>9}")
    loops = []
    for w in walks:
        path, net, ratio = classify(w)
        kind = "loop" if ratio < 0.5 else "one-way"
        if kind == "loop":
            loops.append(ratio)
        print(f"{w['name'][:40]:<40}{path:7.1f}{net:7.1f}{kind:>9}{ratio:9.1%}")

        s = w["samples"]
        d = cumulative(s)
        r = [p["rssi"] for p in s]
        ax[0].plot(d, r, linewidth=1.0, alpha=0.75, label=w["name"][5:26])
        ax[1].scatter([p["x"] for p in s], [p["y"] for p in s], c=r, cmap="plasma",
                      s=7, vmin=-80, vmax=-20)

    print()
    print(f"loops: {len(loops)}  closure min {min(loops):.1%}  median {statistics.median(loops):.1%}  "
          f"max {max(loops):.1%}")

    # bin the signal against distance to see whether the ten walks agree
    xs, ys = [], []
    for w in walks:
        s = w["samples"]
        d = cumulative(s)
        xs.extend(d)
        ys.extend([p["rssi"] for p in s])
    xs, ys = np.array(xs), np.array(ys)
    edges = np.arange(0, 220, 10)
    centres, med, lo, hi = [], [], [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (xs >= a) & (xs < b)
        if m.sum() >= 5:
            centres.append((a + b) / 2)
            med.append(np.median(ys[m]))
            lo.append(np.percentile(ys[m], 25))
            hi.append(np.percentile(ys[m], 75))
    ax[0].fill_between(centres, lo, hi, color="#38bdf8", alpha=0.18, label="25-75% band")
    ax[0].plot(centres, med, color="#38bdf8", linewidth=2.2, label="median")
    ax[0].set_xlabel("distance travelled (m)", color="#8b949e")
    ax[0].set_ylabel("RSSI (dBm)", color="#8b949e")
    ax[0].set_title("signal against distance — the part that reproduces", color="#e6edf3", fontsize=11)
    ax[0].legend(facecolor="#161b22", labelcolor="#e6edf3", edgecolor="#30363d", fontsize=7)

    ax[1].set_title("the shapes, with their drift left in\n(the geometry is a sketch, not a plan)", color="#e6edf3", fontsize=11)
    ax[1].set_xlabel("x (m)", color="#8b949e")
    ax[1].set_aspect("equal", adjustable="datalim")
    plt.colorbar(ax[1].collections[0], ax=ax[1], label="dBm")
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor=fig.get_facecolor())
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
