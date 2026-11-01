"""Design the step detector from a real waveform instead of from a threshold picked out of the air.

The one thing that has never reached the hub is an accelerometer trace from a walk. Until it does, every threshold in
StepDetector is a guess, and three guesses in a row were each wrong in a different direction. This script takes a walk
payload and answers the questions that actually decide the design:

  - how far apart are the peaks that a footfall produces?
  - does one footfall produce ONE peak or TWO?
  - which peaks did the app's detector call, and which did it miss?
  - what enter/exit/refractory values would count footfalls, not halves of them?

    python3 scripts/step_trace_analysis.py docs/data/walk-YYYY-MM-DD.json

FALSIFIER, stated before the run: if the peak spacing within a footfall is not clearly separated from the spacing
between footfalls, no threshold can separate them and the detector needs a different signal (or a different sensor),
not a different number.
"""
from __future__ import annotations

import json
import statistics
import sys


def load(path):
    w = json.load(open(path))
    trace = w.get("accel_trace") or []
    if not trace:
        raise SystemExit("this walk has no accel_trace - it predates v0.5.2")
    t = [p[0] for p in trace]          # ms
    a = [p[1] for p in trace]          # |a| m/s^2
    fired = [i for i, p in enumerate(trace) if len(p) > 2 and p[2] == 1]
    return w, t, a, fired


def peaks(a, threshold):
    """Local maxima above the threshold, with their indices."""
    out = []
    for i in range(1, len(a) - 1):
        if a[i] >= threshold and a[i] >= a[i - 1] and a[i] > a[i + 1]:
            out.append(i)
    return out


def main(argv) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    w, t, a, fired = load(argv[1])
    print(f"walk {w.get('steps')} counts, {w.get('samples_count')} samples, {len(t)} trace points, "
          f"{t[-1]/1000:.0f} s")
    print(f"|a| range {min(a):.2f} .. {max(a):.2f} m/s^2, mean {statistics.mean(a):.2f}")

    for thr in (10.0, 10.2, 10.5, 11.0, 11.5):
        p = peaks(a, thr)
        if len(p) > 2:
            iv = [t[p[i]] - t[p[i-1]] for i in range(1, len(p))]
            print(f"  peaks above {thr:4.1f}: {len(p):3d}  median gap {statistics.median(iv):4.0f} ms  "
                  f"gaps<300ms {sum(1 for v in iv if v < 300):3d}")

    if len(fired) > 1:
        iv = [t[fired[i]] - t[fired[i-1]] for i in range(1, len(fired))]
        print(f"\nthe APP fired {len(fired)} times: median gap {statistics.median(iv):.0f} ms")
        print(f"  gaps <300 ms: {sum(1 for v in iv if v < 300)}  300-600: {sum(1 for v in iv if 300 <= v < 600)}"
              f"  >600: {sum(1 for v in iv if v >= 600)}")
        print("  -> a large 'under 300 ms' count means one footfall is being counted twice")

    # the decisive comparison: peak spacing inside a footfall vs between footfalls
    p = peaks(a, 10.2)
    if len(p) > 4:
        iv = [t[p[i]] - t[p[i-1]] for i in range(1, len(p))]
        short = [v for v in iv if v < 300]
        long_ = [v for v in iv if v >= 300]
        print(f"\npeak gaps: {len(short)} short (<300 ms) and {len(long_)} long")
        if short:
            print(f"  short gaps median {statistics.median(short):.0f} ms -> likely the second half of a footfall")
            print(f"  long  gaps median {statistics.median(long_):.0f} ms -> likely the real step interval")
            print("\nDESIGN: a refractory in the short-gap range, or a requirement to fall below the exit threshold "
                  "for 200 ms, would count one step per footfall.")
        else:
            print("  no short gaps: each footfall produces one peak at this threshold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
