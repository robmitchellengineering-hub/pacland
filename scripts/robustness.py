#!/usr/bin/env python3
"""The robustness engine — the menu behind a quoted number.

    python3 scripts/robustness.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import robustness as R  # noqa: E402


def main() -> int:
    r = R.corpus_susy_fraction()
    print(f"ROBUSTNESS — {r.statistic}\n")
    for k, v in r.values.items():
        print(f"  {k:<40} {v:.4f}  ({v:.1%})")
    print(f"\n  spread {r.spread:.4f}   verdict: {r.verdict.upper()}")
    print(f"  dominant: {r.dominant}")
    print(f"  {r.note}")
    print("\nThe pooled 21.2% is not the spectrum's number — it is the campaign's. Stratified, the rate")
    print("runs from 27.9% (h12=2) to 1.2% (h12=4), so any pooled figure is partly a statement about how")
    print("many runs each h12 received. That is the kind of sentence a bare '21.17% +/- 1.2%' hides.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
