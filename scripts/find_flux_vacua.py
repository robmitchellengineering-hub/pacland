"""Find SUSY flux vacua for a bundled KS model (JAXVacua quickstart workflow).

Runs the four-step loop — load model -> sample guesses -> Newton-refine DW=0 ->
inspect (|W0|, gs, residual) — and prints one JSON line: {"n_vacua": N, "vacua": [...]}.

Usage (on a node with jaxvacua installed, e.g. studio-linux):
    python scripts/find_flux_vacua.py
"""
import json

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import root  # noqa: E402

import jaxvacua as jvc  # noqa: E402


def main() -> None:
    model = jvc.FluxVacuaFinder(
        h12=2, model_ID=1, model_type="KS", maximum_degree=0
    )
    sampler = jvc.data_sampler(
        model,
        moduli_bounds=(2.0, 5.0),
        dilaton_bounds=(2.0, 10.0),
        axion_bounds=(-0.5, 0.5),
        flux_bounds=(-5, 5),
        seed=42,
    )
    z0, tau0, fluxes0 = sampler.initial_guesses(
        N=100, filter_moduli=True, include_fluxes=True
    )

    rows = []
    for i in range(len(z0)):
        x0 = model._convert_complex_to_real(
            z0[i], jnp.conj(z0[i]), tau0[i], jnp.conj(tau0[i])
        )
        r = root(model.DW_x, x0, args=(fluxes0[i],), jac=model.dDW_x,
                 method="hybr", tol=1e-10)
        residual = float(np.max(np.abs(r.fun)))
        if residual < 1e-6:
            m, _, t, _ = model._convert_real_to_complex(r.x)
            if not np.any(np.isnan(np.append(m, t))):
                W0 = abs(complex(model.superpotential_gauge_invariant(
                    jnp.array(m), complex(t), jnp.array(fluxes0[i])
                )))
                rows.append({
                    "W0": float(W0),
                    "gs": float(1.0 / np.imag(t)),
                    "residual": residual,
                    "Re_z1": float(np.real(m[0])),
                    "Im_z1": float(np.imag(m[0])),
                })

    print(json.dumps({"n_vacua": len(rows), "vacua": rows}))


if __name__ == "__main__":
    main()
