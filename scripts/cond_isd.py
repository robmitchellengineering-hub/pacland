#!/usr/bin/env python3
"""cond(M) at the corrected SUSY vacua — re-measures the ISD ill-conditioning claim.

The estate recorded "cond(M) rises 1.8e2 (h12=2) -> 4.8e6 (h12=25)" from a single ISD initial
guess. Re-measured over the data_sampler SUSY-vacuum population (0 runaway, in-domain), the
ill-conditioning is real but not that clean curve:

    h12=2 -> median 1.55e3   h12=3 -> 3.62e4   h12=4 -> 3.66e5
    h12=5 -> 3.85e6          h12=6 -> 1.46e4   (spread: p10-p90 spans 4-5 orders)

Run (JAXVacua host, cytools-venv):  python cond_isd.py <h12> <N> <model_ID>
"""
import sys
import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import root  # noqa: E402
import jaxvacua as jvc  # noqa: E402


def main():
    h12 = int(sys.argv[1])
    N = int(sys.argv[2])
    mid = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    model = jvc.FluxVacuaFinder(h12=h12, model_ID=mid, model_type="KS", maximum_degree=0)
    sampler = jvc.data_sampler(model, moduli_bounds=(2.0, 5.0), dilaton_bounds=(2.0, 10.0),
                               axion_bounds=(-0.5, 0.5), flux_bounds=(-5, 5), seed=7)
    z0, tau0, fluxes0 = sampler.initial_guesses(N=N, filter_moduli=True, include_fluxes=True)

    conds = []
    for i in range(len(z0)):
        x0 = model._convert_complex_to_real(z0[i], jnp.conj(z0[i]), tau0[i], jnp.conj(tau0[i]))
        r = root(model.DW_x, x0, args=(fluxes0[i],), jac=model.dDW_x, method="hybr", tol=1e-10)
        if float(np.max(np.abs(r.fun))) < 1e-6:
            m, mc, t, tc = model._convert_real_to_complex(r.x)
            if np.imag(t) > 0:
                M = np.asarray(model.ISD_matrix(np.asarray(m), np.asarray(mc)))  # (b3, b3)
                ev = np.linalg.eigvalsh((M + M.conj().T) / 2)
                idx = np.argsort(np.abs(ev))
                conds.append(float(abs(ev[idx[-1]]) / max(abs(ev[idx[0]]), 1e-300)))
    if conds:
        a = np.array(conds)
        print(f"h12={h12} mid={mid}: {len(a)} vacua, cond(M) median={np.median(a):.2e} "
              f"p10={np.percentile(a, 10):.2e} p90={np.percentile(a, 90):.2e}", flush=True)
    else:
        print(f"h12={h12} mid={mid}: no cond values", flush=True)


if __name__ == "__main__":
    main()
