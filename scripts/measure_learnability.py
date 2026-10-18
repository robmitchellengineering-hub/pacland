"""Measure learnability + selection statistics on the real flux-vacua sample.

Loads data/vacua_sample.json and runs (a) the VC lower-bound estimator with a
threshold concept class — a sanity check that returns 1 for thresholds — and
(b) the selection / measure-verifier tests (KS uniformity and typicality).

This demonstrates both builds on real data; it is not yet the full
compactification->observables VC measurement, which needs the flux genotype and a
richer sample (see docs/selection.md and docs/evolvability.md).
"""
import json
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from pacland.learnability import vc_lower_bound  # noqa: E402
from pacland.selection import ks_uniformity, typicality_test  # noqa: E402

DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "vacua_sample.json",
)


def threshold_hypotheses(points):
    ts = sorted(points) + [min(points) - 1.0, max(points) + 1.0]
    return [lambda x, t=t: 1 if x >= t else 0 for t in ts]


def main() -> None:
    with open(DATA) as f:
        data = json.load(f)

    for key, d in data.items():
        logW, loggs, n = d["log_W0"], d["log_gs"], d["n"]
        s = sorted(logW)
        print(f"== {key} (n={n}) ==")
        print(f"  log|W0|: min={s[0]:.3f} median={s[n // 2]:.3f} max={s[-1]:.3f}")
        vc = vc_lower_bound(threshold_hypotheses(logW), logW[:6])
        print(f"  VC lower bound (threshold on log|W0|): {vc}  [sanity: expect 1]")
        lo, hi = min(loggs), max(loggs)
        dks = ks_uniformity(loggs, lo, hi)
        print(f"  KS( log gs vs uniform ) = {dks:.3f}")
        v = typicality_test(logW, s[n // 2])
        print(f"  typicality(median log|W0|) -> {v.note} (quantile {v.quantile:.2f})")
        print()


if __name__ == "__main__":
    main()
