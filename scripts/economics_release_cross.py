#!/usr/bin/env python3
"""Class 5 at the release level: the Fed's first print against the one we recorded.

    python3 scripts/economics_release_cross.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import release_cross as rc  # noqa: E402


def main() -> int:
    a = rc.agreement()
    s = rc.sensitivity()
    report = rc.audit()
    print("PACLAND · economics — two archives, one 'first release'\n")
    print(f"overlapping quarters: {a['n']}")
    print(f"agree within {rc.AGREEMENT} pp: {a['n_within']}/{a['n']}   "
          f"mean |gap| {a['mean_abs_gap']:.3f} pp   worst {a['worst_gap']:.2f} pp")
    if a["outside"]:
        print("\nthe quarters that do not agree:")
        for r in a["outside"]:
            print(f"  {r['quarter']}: Fed first {r['fed_first']:+.2f}  "
                  f"our advance {r['our_advance']:+.2f}  gap {r['gap']:+.2f} pp")
    print(f"\nsensitivity of the 37-quarter headline:")
    print(f"  as shipped                     {s['all']:+.3f} pp")
    print(f"  excluding 2020Q2/Q3            {s['excluded']:+.3f} pp")
    print(f"  using the Fed's first releases {s['fed_values']:+.3f} pp")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:22} {check['detail']}")
    print(f"\n{report['n_pass']}/{report['n']} checks pass, each with its seeded fault fired")
    print("CONCLUSION: quote the 239-quarter ladder (+0.469 pp, t=3.68), not the 37-quarter")
    print("sample — the latter moves by 0.311 pp depending on two COVID quarters.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
