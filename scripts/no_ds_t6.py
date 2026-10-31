#!/usr/bin/env python3
"""Route B — the T^6 oracle has no de Sitter vacuum, and it is proved rather than sampled.

    python3 scripts/no_ds_t6.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.oracle import no_ds_t6 as N  # noqa: E402


def main() -> int:
    s = N.statement()
    print("Route B — an impossibility about the spectrum\n")
    print(f"  CLAIM      : {s['claim']}")
    print(f"  BECAUSE    : {s['because']}")
    print(f"  PROVED     : not sampled — no budget, no window, no node\n")
    print("  cross-checks on the algebra:")
    for r in s["checks"]:
        print(f"    K = {r['K']:+.4f}  |W|^2 = {r['abs_W_sq']:.4f}  V = {r['V']:+.6f}  "
              f"identity {r['identity_residual']:.1e}")
    print(f"\n  worst identity residual: {s['worst_identity_residual']:.1e}")
    print(f"\n  SCOPE      : {s['scope']}")
    print("\nThis is the strongest kind of result the estate produces: an impossibility that no new data can")
    print("overturn WITHIN the model. It does not answer the KKLT question, and it says so.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
