"""Phase 0 — Landau-gauge-fixed FP near-zero density at beta=2.5, N=8..16.

Checkpoint: does lambda_min -> 0 under Landau gauge fixing (vs the unfixed covariant-Laplacian
gap ~2.4)? If it does not move, the whole renormalized-continuum route is falsified at step one.

Parallel across configs (ProcessPoolExecutor); reports mean/min lambda_min and P(lambda < 0.1)
for both the unfixed and Landau-fixed FP operator at each N.
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


def one_config(args):
    beta, N, n_sweeps, n_gf, landau, seed = args
    rng = np.random.default_rng(seed)
    links = np.array([su2.random_su2(rng) for _ in range(4 * N ** 4)])
    links = links.reshape((4,) + (N,) * 4 + (4,))
    links = su2.metropolis(links, beta, rng, n_sweeps)
    if landau:
        links = lg.landau_gauge_fix(links, n_gf)
    return lg.lowest_fp_eigenvalue(links)


def main():
    beta = float(sys.argv[1]) if len(sys.argv) > 1 else 2.5
    Ns = [int(x) for x in (sys.argv[2].split(",") if len(sys.argv) > 2 else "8,12")]
    n_configs = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    workers = min(6, os.cpu_count() or 1)

    for N in Ns:
        t0 = time.time()
        for landau in (False, True):
            args = [(beta, N, 10, 20, landau, i) for i in range(n_configs)]
            with ProcessPoolExecutor(max_workers=workers) as ex:
                lams = np.array(list(ex.map(one_config, args)))
            tag = "LANDAU " if landau else "unfixed"
            print(f"N={N} {tag}: mean={lams.mean():.4f} min={lams.min():.4f} "
                  f"P(lam<0.1)={np.mean(lams < 0.1):.3f} ({time.time()-t0:.0f}s)")
    print("PHASE0-DONE")


if __name__ == "__main__":
    main()
