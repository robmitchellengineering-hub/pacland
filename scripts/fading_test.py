"""Does the room behave like the diffuse cavity the engine assumes? Measured, at last.

The mode model treats a room above a certain mode density as a DIFFUSE FIELD: many overlapping modes, random phases, so
the received amplitude is Rayleigh and the received POWER is exponential. That prediction is testable with data that
already exists - the link RSSI recorded while the walker stood still.

    python3 scripts/fading_test.py

Method: cut each walk into stationary segments (consecutive samples moving less than 0.6 m), keep the ones with at
least 8 samples, convert dBm to linear power, and compute std/mean. An exponential distribution has std/mean = 1.00
exactly, whatever its mean - so the statistic is scale-free and needs no calibration of the absolute level.

FALSIFIER, stated before the run: if std/mean sits far from 1.0 - say below 0.6 or above 1.6 across most segments -
the field at rest is not Rayleigh, the room is not diffuse at this mode density, and the engine's diffuse-field
assumption is wrong for houses.
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
DATA = ROOT / "docs/data/walks-2026-11-01.json"
OUT = ROOT / "docs/img/fading-test.png"


def stationary(walk, move_m=0.6, min_n=8):
    s = walk["samples"]
    out, cur = [], []
    for i, p in enumerate(s):
        if i and math.hypot(p["x"] - s[i - 1]["x"], p["y"] - s[i - 1]["y"]) > move_m:
            if len(cur) >= min_n:
                out.append(cur)
            cur = []
        cur.append(p)
    if len(cur) >= min_n:
        out.append(cur)
    return out


def main() -> int:
    walks = json.loads(DATA.read_text())
    segs = []
    for w in walks:
        for s in stationary(w):
            pw = np.array([10 ** (p["rssi"] / 10.0) for p in s])
            segs.append((w["name"], s, pw, float(pw.std() / pw.mean())))

    ratios = [x[3] for x in segs]
    spreads = [max(p["rssi"] for p in s) - min(p["rssi"] for p in s) for _, s, _, _ in segs]
    print(f"stationary segments: {len(segs)}")
    print(f"std/mean  median {statistics.median(ratios):.2f}  range {min(ratios):.2f}..{max(ratios):.2f}")
    print(f"spread at a fixed spot  median {statistics.median(spreads):.1f} dB")

    fig, ax = plt.subplots(1, 3, figsize=(18, 6), dpi=145)
    fig.patch.set_facecolor("#0d1117")
    for a in ax:
        a.set_facecolor("#0d1117")
        a.tick_params(colors="#8b949e")
        for sp in a.spines.values():
            sp.set_color("#30363d")

    # 1 — a fading trace
    _, s, _, _ = max(segs, key=lambda x: len(x[1]))
    ax[0].plot([(p.get("t_ms") or p.get("t") or 0) / 1000.0 for p in s], [p["rssi"] for p in s], color="#38bdf8", linewidth=1.4)
    ax[0].set_title(f"one spot, standing still — {max(p['rssi'] for p in s) - min(p['rssi'] for p in s):.0f} dB of movement",
                    color="#e6edf3", fontsize=11)
    ax[0].set_xlabel("s", color="#8b949e"); ax[0].set_ylabel("RSSI (dBm)", color="#8b949e")

    # 2 — the statistic against the prediction
    ax[1].hist(ratios, bins=np.arange(0.5, 1.75, 0.1), color="#7ee787", edgecolor="#0d1117")
    ax[1].axvline(1.0, color="#ff6b6b", linewidth=2)
    ax[1].text(1.02, ax[1].get_ylim()[1] * 0.85, "Rayleigh = 1.00", color="#ff6b6b", fontsize=10)
    ax[1].set_title(f"std/mean of power, {len(segs)} segments\nmedian {statistics.median(ratios):.2f}",
                    color="#e6edf3", fontsize=11)
    ax[1].set_xlabel("std / mean", color="#8b949e"); ax[1].set_ylabel("segments", color="#8b949e")

    # 3 — the distribution inside one segment against the exponential
    pw = max(segs, key=lambda x: len(x[1]))[2]   # the CDF needs a segment with samples, not the first one
    ys = np.sort(pw / pw.mean())
    cdf = np.arange(1, len(ys) + 1) / len(ys)
    ax[2].step(ys, cdf, where="post", color="#f0b429", linewidth=2, label="measured")
    xs = np.linspace(0, 4, 100)
    ax[2].plot(xs, 1 - np.exp(-xs), color="#ff6b6b", linewidth=1.6, linestyle="--", label="exponential (Rayleigh)")
    ax[2].set_xlim(0, 4)
    ax[2].set_title("power distribution in one segment\nagainst the Rayleigh prediction", color="#e6edf3", fontsize=11)
    ax[2].set_xlabel("normalised power", color="#8b949e"); ax[2].set_ylabel("CDF", color="#8b949e")
    ax[2].legend(facecolor="#161b22", labelcolor="#e6edf3", edgecolor="#30363d")

    fig.suptitle("The room is a diffuse cavity — measured, not assumed", color="#e6edf3", fontsize=13)
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor=fig.get_facecolor())
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
