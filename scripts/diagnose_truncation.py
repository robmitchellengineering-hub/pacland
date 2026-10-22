"""G3 — truncation vs hierarchy, measured FAST at generic (proposal-stage) moduli.

**Root cause of the earlier slowness.** `data_sampler.initial_guesses_ISD` JIT-compiles for
minutes at h12 >= 5. It is not needed: the "proposal stage" moduli are just *generic* moduli
before any solve. The ISD matrix `M = model.ISD_matrix(moduli, moduli_c)` is cheap (0.9s at
h12=2). So this script samples generic cone-like moduli directly and evaluates M there — no
`initial_guesses_ISD`, no solver, no stage error.

**What it measures.** At a fixed generic moduli point, for each h12, the condition number of the
Hodge-star / ISD matrix M (dim 2h12+2) and where its near-null eigenvector points:
  * dilaton band  = components {0, 2h12+1}  (the h3,0 / h0,3 endpoints — always near-flat, no-scale)
  * interior band = the low-index CS moduli   (a physical hierarchy if the flat direction is here)
  * boundary band = the highest-index CS modulus {h12, 2h12} (a truncation artefact if here)

A near-null eigenvector weighted on the *boundary* band that grows with h12 is the truncation
wall; one on the dilaton/interior band is a physical flat direction.

Run on a node with jaxvacua:
    /home/rob/cytools-venv/bin/python scripts/diagnose_truncation.py [h12_csv] [N_points]
"""
import sys

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np  # noqa: E402
import jaxvacua as jvc  # noqa: E402


def main(argv):
    h12s = [2, 5, 10, 15, 20, 25]
    if len(argv) > 1:
        h12s = [int(x) for x in argv[1].split(",")]
    npts = int(argv[2]) if len(argv) > 2 else 1

    rng = np.random.default_rng(42)
    print("=" * 88)
    print(f"truncation diagnostic — cond(M) + near-null eigenvector, GENERIC moduli, h12 in {h12s}")
    print("=" * 88)
    print(f"{'h12':>4} {'dim':>4} {'cond(M)':>11} {'eig_min':>10} {'eig_max':>10} "
          f"{'dilaton':>9} {'interior':>9} {'boundary':>9}  top components")
    for h12 in h12s:
        try:
            model = jvc.FluxVacuaFinder(h12=h12, model_ID=1, model_type="KS",
                                        maximum_degree=0)
            # generic cone-like moduli: Re z in [-1,1], Im z in [0.5, 3]
            z = (rng.uniform(-1.0, 1.0, (npts, h12))
                 + 1j * rng.uniform(0.5, 3.0, (npts, h12)))
            M = np.asarray(model.ISD_matrix(z, np.conjugate(z)))     # (npts, d, d)
            Mk = M[0]
            d = Mk.shape[0]
            evals, evecs = np.linalg.eigh(Mk)                        # M is Hermitian
            idx = np.argsort(np.abs(evals))
            e_min, e_max = evals[idx[0]], evals[idx[-1]]
            cond = float(abs(e_max) / max(abs(e_min), 1e-300))
            v = evecs[:, idx[0]]
            w = np.abs(v) ** 2
            w = w / w.sum()
            h = h12  # CS moduli count; basis order [Omega, chi_1..chi_h, chi_c_1..chi_c_h, Omega_c]
            dilaton = float(w[0] + w[2 * h + 1])
            interior = float(w[1:h].sum() + w[h + 1:2 * h].sum())
            boundary = float(w[h] + w[2 * h])
            top = np.argsort(w)[::-1][:4].tolist()
            print(f"{h12:>4} {d:>4} {cond:>11.3e} {float(e_min):>10.3e} {float(e_max):>10.3e} "
                  f"{dilaton:>9.3f} {interior:>9.3f} {boundary:>9.3f}  {top}")
        except Exception as e:  # noqa: BLE001
            print(f"{h12:>4}  FAIL: {type(e).__name__}: {e}")

    print("\nboundary -> 1.0 = truncation artefact; dilaton/interior = physical flat direction.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
