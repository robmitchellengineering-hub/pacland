"""Sample log|W0| at multiple flux-bound widths to test Denef-Douglas uniformity.

The narrow bounds ([-5,5]) gave a non-uniform |W0|^2 (R2 ~ 0.19). If that is
sampling bias, widening the flux box should push the empirical CDF toward linear
(uniform). Outputs {bounds_string: [log_W0, ...]}.
"""
import json

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import root  # noqa: E402

import jaxvacua as jvc  # noqa: E402


def run(model_args, N, flux_bounds, seed):
    model = jvc.FluxVacuaFinder(**model_args)
    sampler = jvc.data_sampler(
        model,
        moduli_bounds=(2.0, 5.0),
        dilaton_bounds=(2.0, 10.0),
        axion_bounds=(-0.5, 0.5),
        flux_bounds=flux_bounds,
        seed=seed,
    )
    z0, tau0, fluxes0 = sampler.initial_guesses(
        N=N, filter_moduli=True, include_fluxes=True
    )
    logW = []
    for i in range(len(z0)):
        x0 = model._convert_complex_to_real(
            z0[i], jnp.conj(z0[i]), tau0[i], jnp.conj(tau0[i])
        )
        r = root(model.DW_x, x0, args=(fluxes0[i],), jac=model.dDW_x,
                 method="hybr", tol=1e-10)
        if float(np.max(np.abs(r.fun))) < 1e-6:
            m, _, t, _ = model._convert_real_to_complex(r.x)
            if not np.any(np.isnan(np.append(m, t))) and float(np.imag(t)) > 0:
                W0 = abs(complex(model.superpotential_gauge_invariant(
                    jnp.array(m), complex(t), jnp.array(fluxes0[i])
                )))
                logW.append(float(np.log(W0)))
    return logW


def main() -> None:
    out = {}
    for fb in [(-5, 5), (-20, 20)]:
        logW = []
        for mid in (1, 2):
            logW += run(
                {"h12": 2, "model_ID": mid, "model_type": "KS", "maximum_degree": 0},
                N=200, flux_bounds=fb, seed=42 + mid,
            )
        out[str(fb)] = logW
    print(json.dumps(out))


if __name__ == "__main__":
    main()
