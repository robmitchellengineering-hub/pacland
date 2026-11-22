"""Phase 3 — continuum: the full horizon chain across beta (FMR + FP lambda_min + string tension).

For each beta: measure the string tension sigma(beta) -> the spacing a(beta) via scale_a, run the
FMR (Gribov-copy) gauge fix, then the FP lowest eigenvalue. Reports lambda_min in lattice units and
lambda_phys = lambda_min / a^2. This is the continuum-limit driver of docs/MASS-GAP-HORIZON-PLAN.md.

First pass — the physics (fit ranges, FMR depth, config count) will be tuned from the Phase 0/1
results.
"""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np  # noqa: E402

sys.path.insert(0, "src")
from pacland import lattice_ghost as lg  # noqa: E402
from pacland import lattice_ym_su2 as su2  # noqa: E402


def one_fmr_config(args):
    beta, N, n_sweeps, n_copies, n_gf, seed = args
    rng = np.random.default_rng(seed)
    links = np.array([su2.random_su2(rng) for _ in range(4 * N ** 4)])
    links = links.reshape((4,) + (N,) * 4 + (4,))
    try:
        from pacland.lattice_ym_su2_fast import metropolis_fast
        links = metropolis_fast(links, beta, n_sweeps, seed)
    except ImportError:
        links = su2.metropolis(links, beta, rng, n_sweeps)
    links = lg.fmr_gauge_fix(links, n_copies=n_copies, n_gf=n_gf, seed=seed)
    return lg.lowest_fp_eigenvalue(links)


def main():
    betas = [float(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else "2.2,2.4,2.6")]
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    n_configs = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    workers = min(6, os.cpu_count() or 1)

    sigma_ref = None
    for beta in betas:
        t0 = time.time()
        st = su2.string_tension_from_polyakov(beta, N=N, n_configs=40, n_sweeps=12, R_max=3, seed=1)
        sigma = st["sigma"]
        if sigma_ref is None:
            sigma_ref = sigma
        a = su2.scale_a(sigma, sigma_ref)
        with ProcessPoolExecutor(max_workers=workers) as ex:
            args = [(beta, N, 10, 5, 20, i) for i in range(n_configs)]
            lams = np.array(list(ex.map(one_fmr_config, args)))
        lam_phys = lams / (a * a)
        print(f"beta={beta} N={N} sigma={sigma:.4f} a={a:.4f} "
              f"lambda_min_FMR={lams.mean():.4f} (min {lams.min():.4f}) "
              f"lambda_phys={lam_phys.mean():.4f} ({time.time()-t0:.0f}s)")
    print("PHASE3-DONE")


if __name__ == "__main__":
    main()
