"""A truth bench: how far can a spectrum statistic move before the answer is lost?

The landscape work asks "is this structure real, or is it sampling or truncation?" and cannot answer it, because **there
is no landscape whose answer is known**. A room is the opposite: its spectrum is computable exactly from its dimensions, so
any statistic can be run on a system where the truth is arithmetic.

This takes the box that was measured with ARCore (6.05 x 6.05 x 2.58 m) and degrades its exact spectrum the way real
pipelines degrade a spectrum - truncating the band, dropping modes, jittering frequencies - then measures what the spacing
statistic and the mode count do. The output is a calibration: **how much degradation a statistic tolerates before its
verdict is noise**.

    python3 scripts/truth_bench.py

WHAT THIS IS NOT: it is not a claim about any landscape. It is the control that says how much a statistic can be trusted,
computed on a system whose modes are known exactly.

FALSIFIER, stated before the run: if the spacing statistic does not move as degradation increases, the bench is not
measuring what it claims and the whole idea is dead - a statistic insensitive to missing data would be useless as a
diagnostic and suspicious as a result.
"""
from __future__ import annotations

import math
import random
import statistics
import sys

C_AIR = 343.0                 # m/s at 20 C
ROOM = (6.05, 6.05, 2.58)     # the measured office, metres
F_MAX = 2000.0                # Hz: high enough for thousands of modes, low enough to enumerate


def box_modes(dims: tuple[float, float, float], f_max: float) -> list[float]:
    """Every eigenfrequency of a rigid-walled rectangular box below f_max, exactly."""
    a, b, c = dims
    f = []
    for nx in range(1, int(2 * a * f_max / C_AIR) + 2):
        for ny in range(1, int(2 * b * f_max / C_AIR) + 2):
            for nz in range(0, int(2 * c * f_max / C_AIR) + 2):
                if nx == ny == nz == 0:
                    continue
                v = C_AIR / 2 * math.sqrt((nx / a) ** 2 + (ny / b) ** 2 + (nz / c) ** 2)
                if v <= f_max:
                    f.append(v)
    return sorted(f)


def ratio_statistic(levels: list[float]) -> float:
    """<r>: the mean of min(s_i, s_{i+1}) / max(...) over consecutive gaps. 0.386 Poisson, 0.531 GOE."""
    v = sorted(float(x) for x in levels)
    if len(v) < 3:
        return float("nan")
    gaps = [b - a for a, b in zip(v, v[1:]) if b > a]
    if len(gaps) < 2:
        return float("nan")
    rs = [min(a, b) / max(a, b) for a, b in zip(gaps, gaps[1:]) if max(a, b) > 0]
    return statistics.mean(rs) if rs else float("nan")


def degrade(levels: list[float], drop: float, jitter_hz: float, seed: int = 7) -> list[float]:
    rng = random.Random(seed)
    out = [f for f in levels if rng.random() >= drop]
    if jitter_hz > 0:
        out = [f + rng.gauss(0, jitter_hz) for f in out]
    return sorted(out)


def main(argv) -> int:
    exact = box_modes(ROOM, F_MAX)
    print(f"room {ROOM[0]} x {ROOM[1]} x {ROOM[2]} m, below {F_MAX:.0f} Hz: {len(exact)} modes")
    print(f"spacing statistic of the EXACT spectrum: {ratio_statistic(exact):.3f}  "
          f"(Poisson 0.386, GOE 0.531)")
    print("\nthe bench: how the statistic and the mode count move as data is lost\n")
    print(f"{'dropped':>8}{'jitter':>8}{'modes':>8}{'<r>':>8}{'count err':>11}")
    base = ratio_statistic(exact)
    rows = []
    for drop in (0.0, 0.05, 0.20, 0.50, 0.80):
        for jitter in (0.0, 0.5, 2.0):
            d = degrade(exact, drop, jitter)
            r = ratio_statistic(d)
            err = 0.0 if not exact else (len(d) - len(exact)) / len(exact)
            rows.append((drop, jitter, len(d), r, err))
            print(f"{drop:>8.0%}{jitter:>7.1f}Hz{len(d):>8}{r:>8.3f}{err:>10.1%}")
    moved = max(abs(r - base) for _, _, _, r, _ in rows if r == r)
    print(f"\nthe statistic moves {moved:.3f} across the whole bench")
    if moved < 0.05:
        print("VERDICT: the statistic is insensitive to missing data - either it is a robust diagnostic, or this bench is "
              "not touching it. That ambiguity is the reason X8 asks for a control at the same N.")
        return 1
    print("VERDICT: the statistic is sensitive to lost data, so a landscape verdict computed on a truncated or subsampled "
          "spectrum inherits that sensitivity - and this bench is where the size of it can be read.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
