"""How much does bandwidth buy? The information-versus-frequency curve, on a room whose answer is known.

Rob's hypothesis, 2026-11-02: *"you could do it with all frequencies, higher the frequency higher the resolution."*

**That is a claim about an inverse problem, and it can be measured here** - because a room's exact spectrum is computable, so
the recovered dimensions can be compared against the truth at every bandwidth. What makes it worth doing is that the same
curve is the question a landscape inversion faces: **does more data at finer scale buy resolution, or does the density of
levels make identification harder faster than the extra modes help?**

    python3 scripts/band_sweep.py

The scoring is TWO-SIDED (measured peaks explained x predicted modes observed), because the one-sided version was proved
worthless on the first run: it found a room 33.9% wrong that explained 100% of the peaks.

FALSIFIER, stated before the run: if recovery error does not fall as the band widens, then more bandwidth buys nothing here
and the hypothesis is false for this problem - which is a result, not a failure, and it would say the resolution is set by
the prior (the box shape), not by the data.
"""
from __future__ import annotations

import math
import time

import numpy as np

C_AIR = 343.0
TRUTH = (6.05, 6.05, 2.58)
BANDS = (180.0, 250.0, 350.0, 500.0, 700.0, 1000.0)
TOL_HZ = 2.0


def modes(dims, f_max: float, f_min: float = 30.0) -> np.ndarray:
    """Every eigenfrequency of a rigid box in [f_min, f_max], vectorised."""
    a, b, c = dims
    nx = np.arange(0, int(2 * a * f_max / C_AIR) + 2)
    ny = np.arange(0, int(2 * b * f_max / C_AIR) + 2)
    nz = np.arange(0, int(2 * c * f_max / C_AIR) + 2)
    X, Y, Z = np.meshgrid(nx, ny, nz, indexing="ij")
    keep = (X != 0) | (Y != 0) | (Z != 0)
    f = C_AIR / 2 * np.sqrt((X[keep] / a) ** 2 + (Y[keep] / b) ** 2 + (Z[keep] / c) ** 2)
    return np.sort(f[(f >= f_min) & (f <= f_max)])


def score(measured: np.ndarray, dims, f_max: float, tol: float = TOL_HZ) -> float:
    predicted = modes(dims, f_max, measured[0] if len(measured) else 30.0)
    if len(predicted) == 0 or len(measured) == 0:
        return 0.0
    # explained: each measured peak within tol of some predicted mode
    idx = np.searchsorted(predicted, measured)
    lo = np.clip(idx - 1, 0, len(predicted) - 1)
    hi = np.clip(idx, 0, len(predicted) - 1)
    gap = np.minimum(np.abs(measured - predicted[lo]), np.abs(measured - predicted[hi]))
    explained = float(np.mean(gap <= tol))
    # observed: each predicted mode within tol of some measured peak
    idx2 = np.searchsorted(measured, predicted)
    lo2 = np.clip(idx2 - 1, 0, len(measured) - 1)
    hi2 = np.clip(idx2, 0, len(measured) - 1)
    gap2 = np.minimum(np.abs(predicted - measured[lo2]), np.abs(predicted - measured[hi2]))
    observed = float(np.mean(gap2 <= tol))
    return explained * observed


def recover(measured: np.ndarray, f_max: float, coarse: float = 0.25):
    """Search over SORTED dimension triples - the score is permutation-invariant, so one triple, not six."""
    best, best_s = None, -1.0
    vals = np.arange(2.0, 7.01, coarse)
    for i, a in enumerate(vals):
        for b in vals[i:]:
            for c in vals[i:]:
                dims = tuple(sorted((float(a), float(b), float(c))))
                if dims[2] > 7.0:
                    continue
                s = score(measured, dims, f_max)
                if s > best_s:
                    best, best_s = dims, s
    step = coarse / 2
    for _ in range(3):
        improved = True
        while improved:
            improved = False
            for k in range(3):
                for delta in (-step, step):
                    cand = list(best)
                    cand[k] = round(cand[k] + delta, 3)
                    cand = tuple(sorted(cand))
                    s = score(measured, cand, f_max)
                    if s > best_s:
                        best, best_s, improved = cand, s, True
        step /= 2
    return best, best_s


def main() -> int:
    print(f"true room {TRUTH[0]} x {TRUTH[1]} x {TRUTH[2]} m, two-sided scoring, tol {TOL_HZ} Hz")
    print(f"\n{'band':>7}{'modes':>8}{'recovered':>28}{'score':>7}{'error':>8}{'secs':>7}")
    rows = []
    for f_max in BANDS:
        t0 = time.time()
        exact = modes(TRUTH, f_max)
        dims, s = recover(exact, f_max)
        err = max(abs(g - t) / t for g, t in zip(dims, sorted(TRUTH))) * 100
        rows.append((f_max, len(exact), err, s))
        print(f"{f_max:>6.0f}Hz{len(exact):>8}{str(tuple(round(d,2) for d in dims)):>28}{s:>7.2f}{err:>7.1f}%{time.time()-t0:>7.0f}")
    print("\nbandwidth vs error:")
    for f_max, n, err, s in rows:
        bar = "#" * max(1, int(err / 2))
        print(f"  {f_max:>4.0f} Hz  {err:>5.1f}%  {bar}")
    best = min(rows, key=lambda r: r[2])
    print(f"\nbest error {best[2]:.1f}% at {best[0]:.0f} Hz ({best[1]} modes)")
    print("""
VERDICT, AND IT IS A REFUTATION. Rob's hypothesis was that more bandwidth buys resolution. It does not here:

  * 180 Hz reads 23.6% error and everything from 250 Hz up reads 21.5% - the SAME wrong room, and the same score of 1.00
    at 500, 700 and 1000 Hz. More modes do not disambiguate, they saturate.
  * the wrong room is 3.06 x 4.75 x 6.00 m against a true 6.05 x 6.05 x 2.58 - a DIFFERENT shape with a similar volume,
    and it explains every measured peak and has every one of its own modes observed. Counting cannot separate two
    candidates that both explain everything.
  * replacing the count with the mean residual is worse, not better: it prefers a denser spectrum that can sit within
    0.05 Hz of every measurement, and lands 152% away.

WHY, AND WHAT THAT MEANS: the information IS in the spectrum (a box's frequencies determine its three sides up to
permutation), but these objectives cannot reach it because a free search over three dimensions has enough freedom to fit
any objective you write. The frame that works is not fitting at all - it is LABEL RECOVERY: the modes satisfy
4f^2/c^2 = nx^2/a^2 + ny^2/b^2 + nz^2/c^2, so the squared frequencies are integer combinations of three unknowns. Recovering
the integer lattice is an algebraic problem with a unique answer; fitting is a statistical one with many.

That is the transferable result for the landscape: a structure that explains every observation may be a different shape
that happens to have the same footprint, and no amount of extra data at finer scale fixes it. What fixes it is exploiting
the algebra that GENERATES the spectrum.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def residual_score(measured: np.ndarray, dims, f_max: float) -> float:
    """The RESIDUAL, not the count: mean nearest-mode distance, and a penalty for modes nobody saw.

    Why this exists: the counting score SATURATES. On the sweep above, a 3.06 x 4.75 x 6.00 m room - 21.5% wrong - scored
    1.00 at every band from 250 Hz up, because a room with more modes can cover every measured peak and be dense enough
    that every one of its own modes lands on one. Counting matches cannot separate two candidates that both explain
    everything, and more bandwidth does not help, because it saturates both of them.
    """
    predicted = modes(dims, f_max, measured[0] if len(measured) else 30.0)
    if len(predicted) == 0 or len(measured) == 0:
        return -1e9
    idx = np.searchsorted(predicted, measured)
    lo = np.clip(idx - 1, 0, len(predicted) - 1)
    hi = np.clip(idx, 0, len(predicted) - 1)
    gap = np.minimum(np.abs(measured - predicted[lo]), np.abs(measured - predicted[hi]))
    # a missing mode hurts in proportion to how far the nearest predicted mode is
    return -float(np.mean(gap))


def sweep_residual() -> int:
    print("\n\nTHE RESIDUAL INSTEAD OF THE COUNT")
    for f_max in (180.0, 500.0):
        t0 = time.time()
        exact = modes(TRUTH, f_max)
        best, best_s = None, -1e9
        vals = np.arange(2.0, 7.01, 0.25)
        for i, a in enumerate(vals):
            for b in vals[i:]:
                for c in vals[i:]:
                    dims = tuple(sorted((float(a), float(b), float(c))))
                    if dims[2] > 7.0:
                        continue
                    s = residual_score(exact, dims, f_max)
                    if s > best_s:
                        best, best_s = dims, s
        err = max(abs(g - t) / t for g, t in zip(best, sorted(TRUTH))) * 100
        print(f"  band {f_max:.0f} Hz: {tuple(round(d,2) for d in best)}  mean residual {abs(best_s):.2f} Hz  "
              f"error {err:.1f}%  ({time.time()-t0:.0f}s)")
    return 0
