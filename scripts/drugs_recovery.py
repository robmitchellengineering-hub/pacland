#!/usr/bin/env python3
"""Drug discovery: can the assay fit recover a potency we invented, and does it survive a
change of units? (classes 4 and 2, third discipline)

    python3 scripts/drugs_recovery.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.drugs import recovery  # noqa: E402


def main() -> int:
    report = recovery.audit()
    print("PACLAND · drug discovery — synthetic recovery and invariance\n")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:22} {check['detail']}")
    r = recovery.recovery()
    print(f"\ninvented truth: IC50 {r['truth'].ic50:.1f}, Hill {r['truth'].hill:.2f}, "
          f"asymptotes {r['truth'].bottom:.0f}-{r['truth'].top:.0f}")
    print(f"recovered:      IC50 {r['estimate'].ic50:.4f}, Hill {r['estimate'].hill:.4f}")
    print("\nthe trap that bites in practice: pin the asymptotes at the textbook 0/100 and the")
    print("IC50 comes out 43.6% high — while looking perfectly precise.")
    print(f"\n{report['n_pass']}/{report['n']} checks pass, each with its seeded fault fired")
    print("verdict:", "RECOVERABLE (where claimed)" if report["all_pass"] else "NOT RECOVERABLE")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
