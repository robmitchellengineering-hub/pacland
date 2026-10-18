"""Mass spectrum with instanton corrections (maximum_degree=1).

At maximum_degree=0 the moduli are massless (flat directions). Instanton
corrections (degree >= 1) stabilize them, giving a genuine mass spectrum — the one
observable the structure miner has not yet seen. Saves the full Hessian eigenvalue
spectrum (mass^2) per critical point. Writes /home/rob/mass_test.json. Long run.
"""
import json

import jax

jax.config.update("jax_enable_x64", True)

import jaxvacua as jvc  # noqa: E402


def main() -> None:
    m = jvc.FluxVacuaFinder(h12=2, model_ID=1, model_type="KS", maximum_degree=1)
    cps = m.sample_critical_points(
        n_target=600, isd_mode="ISD-", flux_prior="gaussian",
        n_batch=3000, verbose=False,
    )
    rows = []
    for cp in cps:
        rows.append({
            "eigs": [float(e) for e in cp["eigenvalues"]],
            "V": float(cp["V"]),
            "is_susy": bool(cp["is_susy"]),
            "is_minimum": bool(cp["is_minimum"]),
        })
    with open("/home/rob/mass_test.json", "w") as f:
        json.dump({"n": len(rows), "points": rows}, f)
    print(f"MASS_TEST_DONE n={len(rows)}", flush=True)


if __name__ == "__main__":
    main()
