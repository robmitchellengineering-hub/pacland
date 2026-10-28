#!/usr/bin/env python3
"""Smets–Wouters, solved from the authors' own file — and checked four ways.

    python3 scripts/econ_sw_solve.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import sw_solve  # noqa: E402


def main() -> int:
    solved = sw_solve.solve_model()
    report = sw_solve.audit()
    print("PACLAND · economics — Smets–Wouters, solved\n")
    print(f"equations {solved['n_equations']}, endogenous {solved['n_endogenous']}, "
          f"innovations {len(solved['innovations'])}, square {solved['square']}")
    print(f"steady-state residual {solved['worst_steady_state_residual']:.1e}   "
          f"policy residuals {solved['residual_P']:.1e} / {solved['residual_Q']:.1e}")
    print(f"stability: peak ratio {solved['peak_ratio']:.2f} (decays = {solved['stable']})\n")
    print("impulse responses, one unit of each innovation (deviation units, not percent):")
    for shock, label in (("em", "monetary policy"), ("epinf", "cost-push"), ("ea", "TFP")):
        path = sw_solve.irf(solved, shock, horizon=16)
        trough_y = min(path["y"][:13])
        print(f"  {shock:6} {label:16} output impact {path['y'][0]:+.4f} "
              f"trough {trough_y:+.4f}   inflation impact {path['pinf'][0]:+.4f} "
              f"peak {max(abs(x) for x in path['pinf'][:13]):.4f}")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:24} {check['detail']}")
    print(f"\n{report['n_pass']}/{report['n']} checks pass")
    print("verdict:", "SW SOLVED" if report["all_pass"] else "NOT SOLVED")
    print("\nnext: map the six observables to the real-time vintages and project out of sample.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
