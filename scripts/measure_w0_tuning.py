"""Turn the measured log-uniform |W0| prior into the KKLT tuning probability.

From data/isd_susy.json (380 SUSY vacua), the log|W0| CDF is linear (R2 ~ 0.92),
i.e. |W0| is log-uniform over the observed range. The KKLT scenario needs
|W0| ~ 1e-4; this script reports the implied tuning probability, and separates
what is *measured* (within the observed range) from what is *extrapolated*
(far below it, which the sample cannot reach).
"""
import json
import math
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "isd_susy.json",
)


def main() -> int:
    with open(DATA) as f:
        logW = json.load(f)["logW_susy"]

    lo, hi = min(logW), max(logW)

    def p_less_than(log_t):
        """P(log|W0| < log_t) under the measured log-uniform prior."""
        if log_t <= lo:
            return 0.0
        if log_t >= hi:
            return 1.0
        return (log_t - lo) / (hi - lo)

    print(f"log|W0| observed range: [{lo:.2f}, {hi:.2f}]  (span {hi - lo:.2f} nats)")
    print(f"KKLT target |W0|~1e-4 -> log = {math.log(1e-4):.2f}")
    gap = math.log(1e-4) - lo
    print(f"  ...that is {gap:.1f} nats BELOW the observed minimum -> extrapolation\n")

    print("Measured (within the observed range):")
    for t in [0.0, -0.5, -1.0, lo]:
        print(f"  P(|W0| < e^{t:+.1f}) = {p_less_than(t) * 100:6.2f}%")

    print("\nExtrapolated (log-uniform assumed to hold far below the range):")
    for e in [-3, -4, -6, -9.21]:
        print(f"  P(|W0| < 1e{e}) = {p_less_than(math.log(10 ** e)) * 100:.3e}%")

    return 0


if __name__ == "__main__":
    sys.exit(main())
