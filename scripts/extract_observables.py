"""Extract a richer per-vacuum observable vector (L2 stage 5, partial).

Per SUSY flux vacuum, emit: log|W0|, log(gs), the D3 tadpole, and the log of the
positive eigenvalues of the SUSY mass matrix (moduli masses). This expands the
observable domain from 2 to ~3 + (mass-matrix dimension), which is what a
non-trivial learnability measurement needs.

Run on a node with jaxvacua (e.g. studio-linux):

    python scripts/extract_observables.py
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
            if not np.any(np.isnan(np.append(m, t))) and float(np.imag(t)) > 0:
                W0 = abs(complex(model.superpotential_gauge_invariant(
                    jnp.array(m), complex(t), jnp.array(fluxes0[i])
                )))
                row = {
                    "log_W0": float(np.log(W0)),
                    "log_gs": float(np.log(1.0 / np.imag(t))),
                    "tadpole": float(model.tadpole(jnp.array(fluxes0[i]))),
                }
                try:
                    gk = model.gauge_kinetic_matrix(
                        jnp.array(m), jnp.conj(jnp.array(m))
                    )
                    gk_np = np.asarray(gk)
                    if gk_np.ndim == 0:
                        diag = [float(np.real(gk_np))]
                    else:
                        diag = [float(np.real(gk_np[i, i]))
                                for i in range(min(gk_np.shape))]
                    # Re(f) ~ 1/g^2 ; log is a physical gauge-coupling observable
                    row["log_g2_inv"] = [float(np.log(x)) for x in diag if x > 0]
                except Exception:
                    row["log_g2_inv"] = []
                try:
                    mm = model.mass_matrix(
                        jnp.array(m), jnp.conj(jnp.array(m)),
                        complex(t), complex(t).conjugate(),
                        jnp.array(fluxes0[i]),
                    )
                    mm_np = np.asarray(mm)
                    eigs = np.sort(np.real(np.linalg.eigvalsh(mm_np)))
                    row["log_mass2"] = [float(np.log(e)) for e in eigs if e > 1e-12]
                except Exception:
                    row["log_mass2"] = []
                rows.append(row)
    return rows


def main() -> None:
    data = {}
    for mid in (1, 2):
        data[f"h12_2_model{mid}"] = run(
            {"h12": 2, "model_ID": mid, "model_type": "KS", "maximum_degree": 0},
            N=200, seed=42 + mid,
        )
    print(json.dumps(data))


if __name__ == "__main__":
    main()
