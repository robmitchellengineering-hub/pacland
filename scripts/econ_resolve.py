#!/usr/bin/env python3
"""The linear RE solver Smets–Wouters needs — verified three ways before it touches SW.

    python3 scripts/econ_resolve.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import resolve as R  # noqa: E402


def main() -> int:
    print("PACLAND · economics — the linear rational-expectations solver\n")
    u = R.univariate_forward_check()
    print(f"1 · closed form        c = {u['c_computed']:.12f} (truth {u['c_truth']:.12f}), "
          f"residuals {u['residuals'][0]:.1e}/{u['residuals'][1]:.1e}")
    n = R.nk3_cross_check()
    print(f"2 · NK3 cross-check    solver ({n['solver']['a_u']:+.9f}, {n['solver']['b_u']:+.9f}) "
          f"vs closed form ({n['closed_form']['a_u']:+.9f}, {n['closed_form']['b_u']:+.9f})")
    print(f"                       max error {n['error']:.2e}")
    d = R.determinacy_refusal()
    print(f"3 · indeterminate      refused = {d['refused']} ({d['message'][:60]}...)")
    report = R.audit()
    print(f"\n{report['n_pass']}/{report['n']} verifications pass")
    print("verdict:", "SOLVER VERIFIED" if report["all_pass"] else "NOT VERIFIED")
    print("\nnext: feed sw_linear's 40 equations into this and project — the out-of-sample run.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
