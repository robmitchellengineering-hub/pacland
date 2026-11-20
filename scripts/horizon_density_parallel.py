"""Parallel horizon-density measurement — run N configs across all cores, gather the FP spectrum
near zero. Standalone: imports lattice_ym_su2 + lattice_ghost from the same directory."""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

# single-thread the BLAS inside each worker so the eigsh does not oversubscribe/over-allocate
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice_ghost import lowest_fp_eigenvalue  # noqa: E402
from lattice_ym_su2 import metropolis, random_su2  # noqa: E402


def one_config(args):
    beta, N, n_sweeps, seed = args
    rng = np.random.default_rng(seed)
    links = np.array([random_su2(rng) for _ in range(4 * N ** 4)])
    links = links.reshape((4,) + (N,) * 4 + (4,))
    links = metropolis(links, beta, rng, n_sweeps)
    return lowest_fp_eigenvalue(links)


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    beta = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    n_configs = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    n_sweeps = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    workers = min(6, os.cpu_count() or 1)

    t0 = time.time()
    args = [(beta, N, n_sweeps, i) for i in range(n_configs)]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        lams = np.array(list(ex.map(one_config, args)))
    dt = time.time() - t0

    print(f"N={N} beta={beta} configs={n_configs} workers={workers} ({dt:.0f}s)")
    print(f"  lambda_min: mean={lams.mean():.4f} min={lams.min():.4f} max={lams.max():.4f}")
    for thresh in [0.05, 0.1, 0.5, 1.0, 2.0, 2.4]:
        n_below = int(np.sum(lams < thresh))
        print(f"  lambda < {thresh:5.2f}: {n_below:4d}/{len(lams)} = {n_below/len(lams):.4f}")


if __name__ == "__main__":
    main()
