"""Sample SUSY flux vacua across bundled KS models and emit trimmed observables.

Outputs one JSON object keyed by model, each with log|W0| and log(gs) lists.
Run on a node with jaxvacua (e.g. studio-linux):

    python scripts/sample_vacua.py
"""
import json

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import root  # noqa: E402

import jaxvacua as jvc  # noqa: E402


def run(model_args: dict, N: int, seed: int):
    model = jvc.FluxVacuaFinder(**model_args)
    sampler = jvc.data_sampler(
        model,
        moduli_bounds=(2.0, 5.0),
        dilaton_bounds=(2.0, 10.0),
        axion_bounds=(-0.5, 0.5),
        flux_bounds=(-5, 5),
        seed=seed,
    )
    z0, tau0, fluxes0 = sampler.initial_guesses(
        N=N, filter_moduli=True, include_fluxes=True
    )
    log_W0, log_gs = [], []
    for i in range(len(z0)):
        x0 = model._convert_complex_to_real(
            z0[i], jnp.conj(z0[i]), tau0[i], jnp.conj(tau0[i])
        )
        r = root(model.DW_x, x0, args=(fluxes0[i],), jac=model.dDW_x,
                 method="hybr", tol=1e-10)
        residual = float(np.max(np.abs(r.fun)))
        if residual < 1e-6:
            m, _, t, _ = model._convert_real_to_complex(r.x)
            # keep only physical solutions (Im(tau) > 0 => gs > 0)
            if not np.any(np.isnan(np.append(m, t))) and float(np.imag(t)) > 0:
                W0 = abs(complex(model.superpotential_gauge_invariant(
                    jnp.array(m), complex(t), jnp.array(fluxes0[i])
                )))
                log_W0.append(float(np.log(W0)))
                log_gs.append(float(np.log(1.0 / np.imag(t))))
    return {"n": len(log_W0), "log_W0": log_W0, "log_gs": log_gs}


def main() -> None:
    data = {}
    for mid in (1, 2):
        key = f"h12_2_model{mid}"
        data[key] = run(
            {"h12": 2, "model_ID": mid, "model_type": "KS", "maximum_degree": 0},
            N=250, seed=42 + mid,
        )
    print(json.dumps(data))


if __name__ == "__main__":
    main()
