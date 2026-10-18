"""ISD (natural-measure) sampling + W0 uniformity test.

Sample critical points with JAXVacua's ISD measure (flux_prior='gaussian',
isd_mode='ISD-'), compute W0 at each, and separate SUSY (DW=0) from non-SUSY.
Outputs log|W0| for both, so the uniformity of |W0|^2 can be tested against the
Denef-Douglas prediction.
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
        n_target=150, isd_mode="ISD-", flux_prior="gaussian",
        n_batch=2000, verbose=False,
    )
    logW_all, logW_susy = [], []
    for cp in cps:
        W0 = abs(complex(m.superpotential_gauge_invariant(
            jnp.array(cp["moduli"]), complex(cp["tau"]), jnp.array(cp["flux"])
        )))
        lw = float(np.log(W0))
        logW_all.append(lw)
        if cp["is_susy"] and float(np.imag(cp["tau"])) > 0:
            logW_susy.append(lw)
    print(json.dumps({
        "n_all": len(logW_all),
        "n_susy": len(logW_susy),
        "logW_all": logW_all,
        "logW_susy": logW_susy,
    }))


if __name__ == "__main__":
    main()
