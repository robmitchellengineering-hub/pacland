#!/usr/bin/env python3
"""The ingest gate: how much of the corpus is outside the sampler's own declared domain?

    python3 scripts/ingest_gate.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import counterexample as C   # noqa: E402
from pacland.exactness import ingest_gate as G      # noqa: E402


def main() -> int:
    rows = [c["row"] for c in C.load_corpus()]
    per = G.report(rows)
    v = G.verdict(per)
    print("The ingest gate — how much of the corpus is outside the sampler's declared domain?\n")
    print(f"  bounds: in_domain {G.MODULI_BOUNDS}, loose {G.LOOSE_BAND}\n")
    print(f"  {'b3':>3} {'rows':>6} {'in-domain':>10} {'runaway':>8} {'runaway share':>14} "
          f"{'SUSY all':>9} {'SUSY in-domain':>15}")
    for b3, d in sorted(per.items()):
        print(f"  {b3:>3} {d['rows']:>6} {d['in_domain']:>10} {d['runaway']:>8} "
              f"{d['runaway_share']:>13.1%} {d['susy_rate_all']:>8.1%} {d['susy_rate_in_domain']:>14.1%}")
    print(f"\n  total: {v['rows']} rows, {v['runaway']} runaway ({v['runaway_share']:.1%})")
    print(f"\n  {v['statement']}")
    print(f"  {v['rule']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
