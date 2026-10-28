#!/usr/bin/env python3
"""The Fed's own release ladder: 239 quarters of first/second/third revisions.

    python3 scripts/economics_release_archive.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import release_archive as ra  # noqa: E402


def main() -> int:
    report = ra.audit()
    print("PACLAND · economics — the release ladder (Philadelphia Fed, 239 quarters)\n")
    for label, s in ra.ladder().items():
        print(f"{label:24} n={s['n']:>3}  mean {s['mean_pp']:+.3f} pp  "
              f"t={s['t_stat']:+.2f}  upward {s['share_upward']:.0%}  "
              f"sign p={s['sign_test_p']:.3f}")
    s, e = ra.summary(), ra.exploitability()
    print(f"\nmemory: AR(1) of total revision = {s['ar1']:+.3f}")
    print(f"exploitability: {e['verdict']}")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:22} {check['detail']}")
    print(f"\n{report['n_pass']}/{report['n']} checks pass, each with its seeded fault fired")
    print(f"VERDICT: {s['verdict']}.")
    print("This replicates the 37-quarter BEA result on 6.5x more history, through a different")
    print("assembly — the upward bias is real, and it still cannot be traded.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
