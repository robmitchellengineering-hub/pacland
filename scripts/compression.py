#!/usr/bin/env python3
"""The compression engine — does the corpus predict, or is it a list?

    python3 scripts/compression.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import compression as X  # noqa: E402


def main() -> int:
    r = X.compression()
    print("COMPRESSION — does (log N, degree, h12) beat the marginal on unseen families?\n")
    print(f"  folds ................. {r['folds']}")
    print(f"  held-out rows ......... {r['rows']}")
    print(f"  log-loss  marginal .... {r['logloss_marginal']:.4f}")
    print(f"  log-loss  model ....... {r['logloss_model']:.4f}")
    print(f"  Brier     marginal .... {r['brier_marginal']:.4f}")
    print(f"  Brier     model ....... {r['brier_model']:.4f}")
    print(f"  improvement ........... {r['improvement']:+.2%}")
    print(f"\n  VERDICT: {r['verdict'].upper()}")
    print(f"  boundary: {r['boundary']}")
    print("\nA model that cannot beat a constant on unseen families is the finding: the corpus's SUSY rate")
    print("is a description of the sample, not a rule that generalises. That is a full result, and it is")
    print("reported as one rather than softened into 'more data needed'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
