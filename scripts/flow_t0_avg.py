"""Config-averaged Wilson-flow t0 across beta — the finite-lattice running-coupling check.

Averages the flow energy density E(t) over configs before finding t0 (where t^2 <E> = target), so the
single-config noise that plagued the earlier run is averaged out. This is the finite-lattice evidence
that the flow-time scale tracks the running coupling — a falsifier for the gradient-flow scheme, not
the continuum theorem.

Usage: python3 scripts/flow_t0_avg.py "2.2,2.5,2.8" 8 50
"""
import os
import sys
import time

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np  # noqa: E402

sys.path.insert(0, "src")
from pacland import lattice_ym_su2 as lm  # noqa: E402
from pacland.lattice_ym_su2_fast import (  # noqa: E402
    _energy_density_flat, _wilson_flow_step_flat, metropolis_fast)


def t0_at_beta(beta, N, n_configs, n_flow_steps, epsilon, target, n_sweeps):
    d = 4
    nsites = N ** d
    E_sum = np.zeros(n_flow_steps)
    eps_eff = epsilon * (4.0 / float(beta))  # g0^2 = 4/beta
    for c in range(n_configs):
        rng = np.random.default_rng(c)
        links = np.array([lm.random_su2(rng) for _ in range(d * nsites)])
        links = links.reshape((d,) + (N,) * d + (4,))
        flat = metropolis_fast(links, beta, n_sweeps, seed=c).reshape(d, nsites, 4)
        for s in range(n_flow_steps):
            flat = _wilson_flow_step_flat(flat, eps_eff)
            E_sum[s] += _energy_density_flat(flat)
    E_avg = E_sum / n_configs
    t = 0.0
    t2E_prev = 0.0
    for s in range(n_flow_steps):
        t += epsilon  # the flow TIME advances by epsilon (the g0^2 factor is in the step)
        t2E = t * t * E_avg[s]
        if t2E >= target:
            if t2E > t2E_prev:
                return t - epsilon + epsilon * (target - t2E_prev) / (t2E - t2E_prev)
            return t
        t2E_prev = t2E
    return None


def main():
    betas = [float(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else "2.2,2.5,2.8")]
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    n_configs = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    for b in betas:
        t0 = t0_at_beta(b, N, n_configs, 200, 0.05, 0.08, 10)
        print(f"beta={b} N={N} n_configs={n_configs} t0={None if t0 is None else round(t0, 4)}")
    print("FLOW-T0-DONE")


if __name__ == "__main__":
    main()
