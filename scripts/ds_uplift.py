#!/usr/bin/env python3
"""B3 — de Sitter requires a positive term beyond the F-term potential.

    python3 scripts/ds_uplift.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402

from pacland.oracle import ds_needs_uplift as D  # noqa: E402


def main() -> int:
    mp.mp.dps = 30
    s = D.statement()
    print("B3, retried — de Sitter needs a lift, not just a modulus\n")
    print(f"  proved    : {s['proved']}")
    print(f"  exhibited : {s['exhibited']}")
    print(f"  survives  : {s['surviving_statement']}")
    print(f"\n  SUSY point: T = {s['susy_point']['T']:.4f}  V = {s['susy_point']['V']:.3e}  "
          f"identity residual {s['susy_point']['identity_residual']:.1e}")
    print(f"  {'uplift':>8} {'V':>14} {'verdict':>10}")
    for r in s["scan"]:
        verdict = "dS" if r["dS"] else ("Minkowski" if abs(r["V"]) < 1e-25 else "AdS")
        print(f"  {r['D_factor']:>8} {r['V']:>14.3e} {verdict:>10}")
    print(f"\n  excludes  : {s['excludes']}")
    print(f"  scope     : {s['scope']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
