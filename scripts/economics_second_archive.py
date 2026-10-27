#!/usr/bin/env python3
"""Class 5 for economics: a second real-time vintage archive, compared month by month.

    python3 scripts/economics_second_archive.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import second_archive as sa  # noqa: E402


def main() -> int:
    report = sa.audit()
    a = sa.agreement()
    print("PACLAND · economics — a second vintage archive (class 5)\n")
    print("archives compared: ALFRED vintages  vs  FRED-MD historical vintages")
    print(f"series-months:      {a['n']} across {a['vintages']} vintages, "
          f"{len(a['series'])} series ({', '.join(a['series'])})")
    print(f"exact agreement:    {a['n_exact']}/{a['n']}   worst gap {a['worst']['diff']:.3f}")
    for series, st in a["per_series"].items():
        print(f"  {series:10} {st['n_exact']:>5}/{st['n']:<5} exact   worst {st['worst']:.3f}")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:20} {check['detail']}")
    print(f"\nVERDICT: {a['verdict']}.")
    print("This is a second PIPELINE, not a second release: it catches a wrong vintage or a")
    print("transcribed column, not an error by the statistical agency itself.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
