"""The walk, drawn — and the loop-closure error measured rather than hand-waved.

The walk is the first one that recorded: 162 samples at 1 Hz, RSSI from -22 to -73 dBm. It was supposed to be a loop
and ended 27 m from where it started, so this figure exists to show exactly where the dead reckoning went wrong.

    python3 scripts/walk_plot.py

FALSIFIER, stated before the run: the design note (docs/wifi-lidar.md) says a walk whose path length disagrees with
itself by more than 10% is not good enough to supply a frame. This prints that number for the real walk, and the
figure shows the heading that produced it.
"""
from __future__ import annotations

import json
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "docs" / "data" / "walk-2026-11-01.json"
OUT = ROOT / "docs" / "img" / "walk-2026-11-01.png"


def main() -> int:
    w = json.loads(DATA.read_text())
    s = w["samples"]
    x = np.array([p["x_m"] for p in s])
    y = np.array([p["y_m"] for p in s])
    r = np.array([p["rssi_dbm"] for p in s])
    h = np.array([p["heading_deg"] for p in s])
    t = np.array([p["t_ms"] for p in s]) / 1000.0

    path = float(np.sum(np.hypot(np.diff(x), np.diff(y))))
    net = float(math.hypot(x[-1], y[-1]))
    closure = net / path if path else float("nan")

    print(f"samples {len(s)}  duration {t[-1]:.0f} s")
    print(f"path length {path:.1f} m   net displacement {net:.1f} m   closure error {closure:.1%} of path")
    print(f"rssi {r.min()} to {r.max()} dBm   heading distinct {len(set(np.round(h)))}")
    verdict = "PASS" if closure < 0.10 else "FAIL"
    print(f"loop closure {verdict} (the design note allows 10%)")

    fig, ax = plt.subplots(1, 3, figsize=(17, 6), dpi=150)
    fig.patch.set_facecolor("#0d1117")
    for a in ax:
        a.set_facecolor("#0d1117")
        a.tick_params(colors="#8b949e")
        for side in a.spines.values():
            side.set_color("#30363d")

    sc = ax[0].scatter(x, y, c=r, cmap="plasma", s=18)
    ax[0].plot(x, y, color="#30363d", linewidth=0.6, zorder=0)
    ax[0].scatter([x[0]], [y[0]], marker="o", s=120, c="#38bdf8", label="start", zorder=5)
    ax[0].scatter([x[-1]], [y[-1]], marker="X", s=150, c="#ff6b6b", label="end", zorder=5)
    ax[0].annotate("", xy=(x[-1], y[-1]), xytext=(x[0], y[0]),
                   arrowprops=dict(arrowstyle="->", color="#ff6b6b", lw=1.4, ls="--"))
    ax[0].set_title(f"dead-reckoned path, coloured by RSSI\nloop closed to {closure:.0%} of path",
                    color="#e6edf3", fontsize=11)
    ax[0].set_xlabel("x (m)", color="#8b949e"); ax[0].set_ylabel("y (m)", color="#8b949e")
    ax[0].legend(facecolor="#161b22", labelcolor="#e6edf3", edgecolor="#30363d")
    ax[0].set_aspect("equal", adjustable="datalim")
    plt.colorbar(sc, ax=ax[0], label="dBm")

    ax[1].plot(t, r, color="#38bdf8", linewidth=1.2)
    ax[1].set_title("link RSSI along the walk", color="#e6edf3", fontsize=11)
    ax[1].set_xlabel("s", color="#8b949e"); ax[1].set_ylabel("dBm", color="#8b949e")

    ax[2].plot(t, h, color="#f0b429", linewidth=1.0)
    ax[2].set_title("heading — the number the path depends on", color="#e6edf3", fontsize=11)
    ax[2].set_xlabel("s", color="#8b949e"); ax[2].set_ylabel("degrees", color="#8b949e")
    ax[2].set_ylim(0, 360)

    fig.suptitle("Walk 2026-11-01 — first recording that worked: 162 samples, 133 m of path, 51 dB of signal",
                 color="#e6edf3", fontsize=12)
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor=fig.get_facecolor())
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
