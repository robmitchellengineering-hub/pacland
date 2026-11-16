#!/usr/bin/env python3
"""Stable SUSY minima vs saddles — the physically meaningful classification.

A SUSY vacuum (DW=0) is a *stable minimum* iff its scalar-potential Hessian is positive-definite
(all masses^2 > 0); otherwise it is a saddle with a tachyonic direction. The old "SUSY collapse"
was garbling this: the raw SUSY count is flat across h12, but the *stable* minima collapse.

Measured (pacland-rog, 2026-11-14, N=2000, data_sampler):
    h12=2 -> 57/634 stable (9.0%)   h12=3 -> 0/203   h12=4 -> 0/249
    h12=5 -> 0/160                  h12=6 -> 1/472 (0.2%)

Run (JAXVacua host, cytools-venv):  python susy_minima.py <h12> <N> <model_ID>
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

    n_susy = n_min = 0
    for i in range(len(z0)):
        x0 = model._convert_complex_to_real(z0[i], jnp.conj(z0[i]), tau0[i], jnp.conj(tau0[i]))
        r = root(model.DW_x, x0, args=(fluxes0[i],), jac=model.dDW_x, method="hybr", tol=1e-10)
        if float(np.max(np.abs(r.fun))) < 1e-6:
            m, mc, t, tc = model._convert_real_to_complex(r.x)
            if np.imag(t) > 0:
                n_susy += 1
                H = np.asarray(model.hessian(jnp.array(m), jnp.array(mc), t, tc,
                                             jnp.array(fluxes0[i]), noscale=True, mode="SUSY"))
                ev = np.linalg.eigvalsh((H + H.conj().T) / 2)
                if np.min(ev) > 1e-6:
                    n_min += 1
    print(f"h12={h12} mid={mid}: {n_susy} SUSY -> {n_min} stable minima "
          f"({n_min / max(1, n_susy):.1%}), {n_susy - n_min} saddles", flush=True)


if __name__ == "__main__":
    main()
