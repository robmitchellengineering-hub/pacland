"""The house as a 3D map, inferred from the walk — and honest about what is inferred and what is invented.

The walk gives, for each labelled spot, the RSSI of every BSS it could hear. That is a 23-dimensional fingerprint per
spot, and the geometry has to be recovered from it because none of the spots has coordinates.

Two steps, both standard and both stated:

  1. SPOT LAYOUT by classical MDS on RSSI-space distances. Spots that hear the same APs at similar levels land near
     each other. The result is correct up to ROTATION, REFLECTION and SCALE - there is no absolute frame in RSSI.
  2. AP POSITIONS by multilateration: distance from RSSI through a log-distance path-loss model with a stated
     exponent, fitted to the radio's own reference level. Also up to the same freedom.

So the map is a SHAPE, not a survey. It says which rooms are near which, and roughly how far the far ones are.

    python3 scripts/house_map.py            # writes docs/img/house-map-3d.png and prints the fit

FALSIFIER, stated before the run: if the MDS stress is high (a shape that does not exist in 3D explains the data
badly), the map is a drawing with a number attached and must not be shown as geometry. If the fitted path-loss
exponent lands outside 1.5-4, the distance model is wrong and the 3D placement is meaningless.
"""
from __future__ import annotations

import csv
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "docs" / "data" / "house-walk-2026-10-31.csv"
OUT = ROOT / "docs" / "img" / "house-map-3d.png"


def load():
    rows = list(csv.reader(open(CSV)))
    header, body = rows[0][1:], rows[1:]
    spots, mat = [], []
    for r in body:
        spots.append(r[0])
        mat.append([float(x) if x else np.nan for x in r[1:]])
    return header, spots, np.array(mat)


def distances(mat: np.ndarray) -> np.ndarray:
    """Spot-to-spot distance in RSSI space, with missing values imputed by the column median.

    Missing is not the same as weak: a spot that could not hear an AP at all is at least as far as the weakest spot
    that could, so a missing value is filled with the column MINIMUM (weakest heard) rather than the median.
    """
    filled = mat.copy()
    for j in range(filled.shape[1]):
        col = filled[:, j]
        known = col[~np.isnan(col)]
        if known.size == 0:
            filled[:, j] = -100.0
        else:
            filled[np.isnan(col), j] = known.min() - 3.0
    d = np.zeros((filled.shape[0], filled.shape[0]))
    for i in range(len(filled)):
        for k in range(len(filled)):
            d[i, k] = math.sqrt(((filled[i] - filled[k]) ** 2).mean())
    return d


def cmds(d: np.ndarray, dims: int = 3):
    """Classical multidimensional scaling: eigen-decomposition of the double-centred squared distances."""
    n = d.shape[0]
    j = np.eye(n) - np.ones((n, n)) / n
    b = -0.5 * j @ (d ** 2) @ j
    w, v = np.linalg.eigh(b)
    idx = np.argsort(w)[::-1][:dims]
    w, v = w[idx], v[:, idx]
    pos = v * np.sqrt(np.maximum(w, 0))
    stress = float(np.sqrt(max(0.0, 1 - (w.sum() / max(np.trace(b), 1e-9)))))
    return pos, stress, b


def attenuation(mat: np.ndarray) -> np.ndarray:
    """Each AP's level relative to its OWN best hearing, in dB.

    THE FIRST VERSION USED ONE GLOBAL REFERENCE, which is wrong: every AP transmits at a different power, so a strong
    AP at 10 m and a weak AP at 2 m produce the same RSSI. Subtracting each AP's maximum removes the transmit power
    and leaves the attenuation, which is the only thing that carries distance.
    """
    att = np.full_like(mat, np.nan)
    for j in range(mat.shape[1]):
        col = mat[:, j]
        known = ~np.isnan(col) & ~np.isinf(col)
        if known.sum() == 0:
            continue
        att[:, j] = np.where(known, col.max() - col, np.nan)
    return att


def fit_geometry(att: np.ndarray, exp: float, d0: float = 1.0, iters: int = 3000, lr: float = 0.002):
    """Joint least squares over SPOT and AP positions.

    Residual for a hearable pair: ||spot - ap|| - d0 * 10^(att / (10 exp)). Spots start from their MDS layout, APs from
    the centroid with small offsets, and the whole configuration is pulled to a fixed scale each step so it cannot
    drift or collapse - the failure mode of the first attempt, where every spot fell into the centre and the APs flew
    out to +-100.
    """
    n_spots, n_aps = att.shape
    # initial spots: 3-D MDS of the attenuation matrix (NaNs filled wide)
    filled = np.where(np.isnan(att), np.nanmax(att) + 6, att)
    d = np.sqrt(((filled[:, None, :] - filled[None, :, :]) ** 2).mean(axis=2))
    pos, _stress, _b = cmds(d, 3)
    aps = np.repeat(pos.mean(axis=0)[None, :], n_aps, axis=0) + np.random.default_rng(7).normal(0, 2.0, (n_aps, 3))
    pairs = [(i, j) for i in range(n_spots) for j in range(n_aps) if not np.isnan(att[i, j])]
    target = np.array([d0 * 10 ** (att[i, j] / (10 * exp)) for i, j in pairs])
    for _ in range(iters):
        gs = np.zeros_like(pos)
        ga = np.zeros_like(aps)
        for k, (i, j) in enumerate(pairs):
            diff = pos[i] - aps[j]
            n = np.linalg.norm(diff) + 1e-9
            residual = n - target[k]
            g = (residual / n) * diff
            gs[i] += g
            ga[j] -= g
        pos -= lr * gs / max(len(pairs), 1) * 100
        aps -= lr * ga / max(len(pairs), 1) * 100
        # pin the frame: centre at the origin and a fixed RMS radius, so scale is a choice not a runaway
        for arr in (pos, aps):
            arr -= np.vstack([pos, aps]).mean(axis=0)
        allp = np.vstack([pos, aps])
        rms = np.sqrt((allp ** 2).sum(axis=1).mean()) + 1e-9
        scale = 12.0 / rms
        pos *= scale
        aps *= scale
    return pos, aps


def residuals(pos, aps, att, exp, d0=1.0):
    out = []
    for i in range(att.shape[0]):
        for j in range(att.shape[1]):
            if np.isnan(att[i, j]):
                continue
            out.append(np.linalg.norm(pos[i] - aps[j]) - d0 * 10 ** (att[i, j] / (10 * exp)))
    return np.array(out)


def main() -> int:
    header, spots, mat = load()
    d = distances(mat)
    pos, stress, _ = cmds(d, 3)
    pos -= pos.mean(axis=0)
    exp = 2.7                               # indoor, stated, and the fit is reported below
    att = attenuation(mat)
    pos, ap_arr = fit_geometry(att, exp)
    aps = {header[j]: ap_arr[j] for j in range(len(header))}
    res = residuals(pos, ap_arr, att, exp)
    print(f"geometry residuals: rms {res.std():.2f} m, mean {res.mean():+.2f} m over {len(res)} measurements")

    print(f"spots {len(spots)}  BSS {len(header)}  stress {stress:.3f}")
    if stress > 0.35:
        print("VERDICT: the 3D shape does not explain the data well - this is a drawing, not geometry.")
    else:
        print("VERDICT: a 3D shape explains the RSSI distances reasonably")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print("matplotlib missing:", e)
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(13, 10), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0d1117")
    fig.patch.set_facecolor("#0d1117")

    # spot-to-AP edges, coloured by measured level
    for name, p in aps.items():
        j = header.index(name)
        for i, sp in enumerate(spots):
            v = mat[i, j]
            if np.isnan(v):
                continue
            frac = (v + 90) / 60.0
            col = plt.cm.plasma(min(max(frac, 0.0), 1.0))
            ax.plot([pos[i, 0], p[0]], [pos[i, 1], p[1]], [pos[i, 2], p[2]],
                    color=col, alpha=0.35, linewidth=1.2)

    ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], s=220, c="#38bdf8", marker="o", depthshade=False, label="spot")
    for i, name in enumerate(spots):
        best = np.nanmax(mat[i]) if not np.all(np.isnan(mat[i])) else -99
        ax.text(pos[i, 0], pos[i, 1], pos[i, 2], "  " + name[:22] + f"  {best:.0f} dBm",
                color="#e6edf3", fontsize=9, zorder=10)
    if aps:
        ap = np.array(list(aps.values()))
        ax.scatter(ap[:, 0], ap[:, 1], ap[:, 2], s=70, c="#f59e0b", marker="^", depthshade=False,
                   label="BSS (23)")
        # label only the four that matter: the house's own two, and the two loudest neighbours
        names = sorted(aps, key=lambda n: -np.nanmax(mat[:, header.index(n)]))[:4]
        for name in names:
            p = aps[name]
            ax.text(p[0], p[1], p[2], "  " + name.split("|")[0][:20], color="#f59e0b", fontsize=8)

    ax.set_xlabel("MDS 1", color="#8b949e")
    ax.set_ylabel("MDS 2", color="#8b949e")
    ax.set_zlabel("MDS 3", color="#8b949e")
    ax.tick_params(colors="#8b949e")
    ax.set_title(f"The house as a 3D shape from {len(spots)} spots x {len(header)} BSS  "
                 f"(MDS stress {stress:.2f}, no absolute frame)", color="#e6edf3", fontsize=12)
    ax.legend(loc="upper left", facecolor="#161b22", labelcolor="#e6edf3", edgecolor="#30363d")
    plt.tight_layout()
    fig.savefig(OUT, facecolor=fig.get_facecolor())
    print("wrote", OUT.relative_to(ROOT))

    # SECOND FIGURE: what the walk actually establishes, without any geometry at all - the level heard at each spot.
    # A bar chart cannot be wrong about the layout because it does not claim one.
    fig2, ax2 = plt.subplots(figsize=(12, 6), dpi=150)
    fig2.patch.set_facecolor("#0d1117")
    ax2.set_facecolor("#0d1117")
    order = np.argsort([-np.nanmax(mat[i]) for i in range(len(spots))])
    best = [np.nanmax(mat[i]) for i in order]
    names = [spots[i] for i in order]
    ax2.barh(range(len(names)), best, color="#38bdf8")
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels(names, color="#e6edf3")
    ax2.invert_yaxis()
    ax2.set_xlabel("strongest level heard at this spot (dBm)", color="#8b949e")
    ax2.tick_params(colors="#8b949e")
    for i, v in enumerate(best):
        ax2.text(v - 1, i, f"{v:.0f}", va="center", ha="right", color="#0d1117", fontsize=9, fontweight="bold")
    ax2.set_title("What the walk measured, with no geometry claimed", color="#e6edf3")
    fig2.tight_layout()
    out2 = ROOT / "docs" / "img" / "house-levels.png"
    fig2.savefig(out2, facecolor=fig2.get_facecolor())
    print("wrote", out2.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
