"""SU(2) 0++ glueball mass — thin CLI over pacland.glueball.

Usage:
    python3 scripts/glueball_mass.py N beta n_sweeps n_meas [seed]
"""
from __future__ import annotations

import sys

sys.path.insert(0, "src")
from pacland.glueball import glueball_correlation  # noqa: E402


def main(argv: list[str]) -> int:
    N = int(argv[0]) if len(argv) > 0 else 6
    beta = float(argv[1]) if len(argv) > 1 else 2.4
    n_sweeps = int(argv[2]) if len(argv) > 2 else 30
    n_meas = int(argv[3]) if len(argv) > 3 else 200
    seed = int(argv[4]) if len(argv) > 4 else 0
    c, m_eff, gbar = glueball_correlation(N=N, beta=beta, n_sweeps=n_sweeps, n_meas=n_meas, seed=seed)
    print(f"SU(2) glueball mass  N={N} beta={beta} sweeps={n_sweeps} meas={n_meas} seed={seed}")
    print(f"  <G> = {gbar:.4f}")
    print("  dt  C(dt)         m_eff(dt)")
    for dt in range(len(m_eff)):
        print(f"  {dt:<3} {c[dt]:.4e}   {m_eff[dt]:.4f}")
    print(f"  glueball mass m (lattice units) ~ {m_eff[-2]:.4f}  (effective-mass plateau, last two bins)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
