#!/usr/bin/env python3
"""Sample SUSY flux vacua at any h12 with the **data_sampler** (the effective method).

`sample_h12.py` uses `sample_critical_points(isd_mode="ISD-")`, which finds **0 SUSY out of 400
candidates at h12=4**. The corpus's own vacua came from `data_sampler` + scipy `root` (hybr), which
finds them fast. This script is that method, parameterised by h12, N and model_ID.

Measured (pacland-rog, 2026-11-14, data_sampler, 0 runaway at every rung):
    b3=6  (h12=2, mid=1)  1513 SUSY, 1195 in-domain (79.0%)
    b3=8  (h12=3, mid=2)   474 SUSY,  282 in-domain (59.5%)   # mid=1 has no cone (H is None)
    b3=10 (h12=4, mid=1)   547 SUSY,  338 in-domain (61.8%)

The quoted "SUSY fraction falls to 1.1%" at b3=10 was measured over a corpus whose rows were mostly
out-of-domain sampler artefacts; the correct sampler finds abundant SUSY vacua, ~60-79% in-domain,
with no collapse.

Run (JAXVacua host, cytools-venv):
    /home/rob/cytools-venv/bin/python sample_h12_ds.py <h12> <N_guesses> <output.json> [model_ID]
"""
import json
import sys
import time

import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import root  # noqa: E402
import jaxvacua as jvc  # noqa: E402


def main():
    h12 = int(sys.argv[1])
    N = int(sys.argv[2])
    out = sys.argv[3]
    mid = int(sys.argv[4]) if len(sys.argv) > 4 else 1

    model = jvc.FluxVacuaFinder(h12=h12, model_ID=mid, model_type="KS", maximum_degree=0)
    sampler = jvc.data_sampler(model, moduli_bounds=(2.0, 5.0), dilaton_bounds=(2.0, 10.0),
                               axion_bounds=(-0.5, 0.5), flux_bounds=(-5, 5), seed=7)
    z0, tau0, fluxes0 = sampler.initial_guesses(N=N, filter_moduli=True, include_fluxes=True)

    t0 = time.time()
    rows = []
    for i in range(len(z0)):
        x0 = model._convert_complex_to_real(z0[i], jnp.conj(z0[i]), tau0[i], jnp.conj(tau0[i]))
        r = root(model.DW_x, x0, args=(fluxes0[i],), jac=model.dDW_x, method="hybr", tol=1e-10)
        residual = float(np.max(np.abs(r.fun)))
        if residual < 1e-6:
            m, _, t, _ = model._convert_real_to_complex(r.x)
            moduli = [[float(np.real(x)), float(np.imag(x))] for x in np.atleast_1d(np.asarray(m))]
            tau = [float(np.real(t)), float(np.imag(t))]
            if not np.any(np.isnan(np.asarray(moduli, dtype=float))) and not np.isnan(tau[0]) and tau[1] > 0:
                rows.append({"moduli": moduli, "tau": tau, "is_susy": True})
    dt = time.time() - t0
    json.dump({"h12": h12, "model_ID": mid, "n": len(rows), "elapsed_s": dt, "vacua": rows}, open(out, "w"))
    print(f"DONE h12={h12} mid={mid} {len(rows)} SUSY in {dt:.1f}s -> {out}", flush=True)


if __name__ == "__main__":
    main()
