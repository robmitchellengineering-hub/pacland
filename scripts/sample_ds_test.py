"""De Sitter conjecture test — do any critical points have V>0 with a minimum?

The de Sitter conjecture (Obied-Ooguri-Spodyneiko-Vafa 2018) forbids stable dS
vacua (V>0, positive-definite Hessian). JAXVacua's critical points carry V,
is_minimum, and is_susy, so we can test this directly on a natural-measure sample.
Writes /home/rob/ds_test.json on the node. Long run (~10-20 min).
"""
import json

import jax

jax.config.update("jax_enable_x64", True)

import numpy as np  # noqa: E402

import jaxvacua as jvc  # noqa: E402


def main() -> None:
    m = jvc.FluxVacuaFinder(h12=2, model_ID=1, model_type="KS", maximum_degree=0)
    cps = m.sample_critical_points(
        n_target=2000, isd_mode="ISD-", flux_prior="gaussian",
        n_batch=5000, verbose=False,
    )
    rows = []
    for cp in cps:
        eigs = list(cp["eigenvalues"])
        rows.append({
            "V": float(cp["V"]),
            "is_minimum": bool(cp["is_minimum"]),
            "is_susy": bool(cp["is_susy"]),
            "min_eig": float(min(eigs)) if eigs else None,
        })
    with open("/home/rob/ds_test.json", "w") as f:
        json.dump({"n": len(rows), "points": rows}, f)
    print(f"DS_TEST_DONE n={len(rows)}", flush=True)


if __name__ == "__main__":
    main()
