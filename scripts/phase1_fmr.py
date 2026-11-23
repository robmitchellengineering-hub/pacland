"""Phase 1 — FMR (Gribov-copy) horizon probe: unfixed vs Landau vs FMR lambda_min.

Phase 0 showed Landau fixing leaves lambda_min ~2.4 (first Gribov region, expected). The horizon is
at the FMR boundary, so this compares unfixed, single-copy Landau, and the FMR (Gribov-copy search)
to see whether the copy search moves lambda_min toward zero.
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
    beta, N, n_sweeps, mode, n_copies, n_gf, seed = args
    rng = np.random.default_rng(seed)
    links = np.array([su2.random_su2(rng) for _ in range(4 * N ** 4)])
    links = links.reshape((4,) + (N,) * 4 + (4,))
    links = su2.metropolis(links, beta, rng, n_sweeps)
    if mode == "landau":
        links = lg.landau_gauge_fix(links, n_gf)
    elif mode == "fmr":
        links = lg.fmr_gauge_fix(links, n_copies=n_copies, n_gf=n_gf, seed=seed)
    return lg.lowest_fp_eigenvalue(links)


def main():
    beta = float(sys.argv[1]) if len(sys.argv) > 1 else 2.5
    Ns = [int(x) for x in (sys.argv[2].split(",") if len(sys.argv) > 2 else "8,12")]
    n_configs = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    workers = min(6, os.cpu_count() or 1)

    for N in Ns:
        for mode in ("unfixed", "landau", "fmr"):
            t0 = time.time()
            n_copies = 5 if mode == "fmr" else 1
            args = [(beta, N, 10, mode, n_copies, 20, i) for i in range(n_configs)]
            with ProcessPoolExecutor(max_workers=workers) as ex:
                lams = np.array(list(ex.map(one_config, args)))
            print(f"N={N} {mode}: mean={lams.mean():.4f} min={lams.min():.4f} "
                  f"P(lam<0.1)={np.mean(lams < 0.1):.3f} ({time.time()-t0:.0f}s)")
    print("PHASE1-DONE")


if __name__ == "__main__":
    main()
