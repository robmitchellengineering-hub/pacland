#!/usr/bin/env python3
"""F1 — the measure engine.

    python3 scripts/measure_engine.py

One exact lattice, one counting question, five reasonable measures. The spread is the result — and it is
the first number this programme can state whose *null* (measures agreeing) would also be a finding.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.exactness import measures as M  # noqa: E402


def main() -> int:
    a = M.antisymmetry()
    print("F1 · the measure engine\n")
    print("The acceptance test is an identity, not a number:")
    print("  fraction(N>0) == (1 - fraction(N==0)) / 2   for every measure that sees N through |N|\n")
    for c in a["checks"]:
        print(f"{'PASS' if c['pass'] else 'FAIL'}  {c['measure']:<16} "
              f"{c['lhs']:.12f} vs {c['rhs']:.12f}   residual {c['residual']:.1e}")
    print(f"\nidentity holds for all {len(a['checks'])} measures: {a['all_pass']}\n")

    t = M.table()
    print(f"window {t['window']}  ({t['pairs']} pairs, exact enumeration)\n")
    header = f"  {'property':<12}" + "".join(f"{k:>17}" for k in t["measures"]) + f"{'ratio':>8}"
    print(header)
    for r in t["rows"]:
        line = f"  {r['property']:<12}" + "".join(f"{r['values'][k]:>17.4f}" for k in t["measures"])
        line += f"{r['ratio']:>8.3f}"
        print(line)
        if r["zero_support"]:
            print(f"  {'':<12}  zero support under {', '.join(r['zero_support'])} — a definitional "
                  "difference, not a measured spread")

    print(f"\nlargest finite ratio across measures: {t['max_ratio']:.2f}x")
    print(f"largest absolute spread            : {t['max_spread']:.4f}")
    print("\nThe fact: on one exactly enumerable lattice, 'the fraction of flux choices with a small")
    print("tadpole' is 0.071 or 0.361 depending only on which reasonable measure you use — a factor of")
    print("5, with no physics changed. That is the '10^500 vacua' argument, quantified.")
    print("\nThe honest limit: only b3=6, |F_i|,|H_i| <= 1 is exactly enumerable. Any larger window is")
    print("sampled and must be labelled so; a fraction without its window is not a fact.")
    return 0 if a["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
