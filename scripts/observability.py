#!/usr/bin/env python3
"""The observability engine — what the corpus can measure, and what it only appears to.

    python3 scripts/observability.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import observability as O  # noqa: E402


def main() -> int:
    print("Observability — a proportion is a claim with three parts\n")
    for r in O.corpus_readings():
        print(f"{r.quantity}")
        print(f"  estimate  {r.estimate:.3%}   [{r.ci_low:.3%}, {r.ci_high:.3%}]   rows used {r.n_used}")
        if r.parameter_spread is not None:
            print(f"  threshold moves it by {r.parameter_spread:.3%} of the rows")
        print(f"  VERDICT   {r.verdict.upper()}: {r.why}")
        print()
    print("The minima fraction is the worked case: 39.9% of primitive rows, ±1.2% statistically — and")
    print("the is_minimum threshold moves it by 35 points. The interval is honest; the estimate is not")
    print("a property of the landscape until the threshold is stated with it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
