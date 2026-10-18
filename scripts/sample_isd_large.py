"""Large ISD (natural-measure) SUSY sampling to test Denef-Douglas uniformity.

Samples n_target=2000 critical points with ISD, keeps the SUSY subset, computes
W0, and writes log|W0| to /home/rob/isd_susy.json on the node. Prints a done line.
Run on studio-linux (long: ~10-20 min).
"""
import json

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import jaxvacua as jvc  # noqa: E402


def main() -> None:
    m = jvc.FluxVacuaFinder(h12=2, model_ID=1, model_type="KS", maximum_degree=0)
    cps = m.sample_critical_points(
        n_target=2000, isd_mode="ISD-", flux_prior="gaussian",
        n_batch=5000, verbose=False,
    )
    logW_susy = []
    for cp in cps:
        if cp["is_susy"] and float(np.imag(cp["tau"])) > 0:
            W0 = abs(complex(m.superpotential_gauge_invariant(
                jnp.array(cp["moduli"]), complex(cp["tau"]), jnp.array(cp["flux"])
            )))
            logW_susy.append(float(np.log(W0)))
    with open("/home/rob/isd_susy.json", "w") as f:
        json.dump({"n_susy": len(logW_susy), "logW_susy": logW_susy}, f)
    print(f"ISD_SUSY_DONE n_susy={len(logW_susy)}", flush=True)


if __name__ == "__main__":
    main()
