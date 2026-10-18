"""Test the central structural claim: is |W0|^2 uniformly distributed?

Denef-Douglas says flux vacua have W0 uniform in the complex plane, which implies
|W0|^2 is uniform — so its empirical CDF should be *linear*. This script measures
that linearity on the real sample, and contrasts with log(gs), for which no
uniformity is claimed.
"""
import json
import math
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from pacland.constraints import elimination_curve, linearity_r2  # noqa: E402

DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "vacua_sample.json",
)


def main() -> int:
    with open(DATA) as f:
        data = json.load(f)

    logW, loggs = [], []
    for d in data.values():
        logW.extend(d["log_W0"])
        loggs.extend(d["log_gs"])

    # |W0|^2 = exp(2 * log|W0|)
    w0sq = [math.exp(2.0 * w) for w in logW]
    gs = [math.exp(g) for g in loggs]

    for name, vals in [("|W0|^2", w0sq), ("gs", gs)]:
        lo, hi = min(vals), max(vals)
        ts = [lo + (hi - lo) * i / 20 for i in range(21)]
        cdf = elimination_curve(vals, ts)
        r2 = linearity_r2(ts, cdf)
        print(f"{name:8s}  CDF linearity R^2 = {r2:.3f}   (1.0 = perfectly uniform)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
