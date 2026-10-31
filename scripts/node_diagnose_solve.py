"""Diagnose the h12>=5 solve: is the returned "critical point" a root nearby, or nowhere near one?

FALSIFIER, before the run: if the F-term residual |DW| at the returned critical point is small (< 1e-4) and the
SUSY test still says false, then the CLASSIFIER is wrong and the solve is fine. If |DW| is large, the solve is
the failure — and the Jacobian's condition number then says whether a root is reachable from there.

Run on pacland-rog:
    /home/rob/cytools-venv/bin/python scripts/node_diagnose_solve.py [h12] [n_target] [max_batches]
"""
import json
import sys
import time

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np  # noqa: E402
import jaxvacua as jvc  # noqa: E402


def main(argv):
    h12 = int(argv[1]) if len(argv) > 1 else 5
    n_target = int(argv[2]) if len(argv) > 2 else 2
    max_batches = int(argv[3]) if len(argv) > 3 else 120
    out = {"h12": h12, "falsifier": "small |DW| with is_susy=False means the classifier is wrong, not the solve",
           "points": []}
    print(f"building h12={h12} degree=2 (corrections ON)", flush=True)
    model = jvc.FluxVacuaFinder(h12=h12, model_ID=1, model_type="KS", maximum_degree=2,
                                mirror_instanton=True)
    print("sampling", flush=True)
    t0 = time.time()
    vacua = list(model.sample_critical_points(Q=None, n_target=n_target, n_batch=25,
                                              max_batches=max_batches, isd_mode="ISD-",
                                              solver="scipy", verbose=False))
    print(f"got {len(vacua)} critical points in {round(time.time()-t0,1)}s", flush=True)
    for i, v in enumerate(vacua):
        keys = sorted(v.keys()) if hasattr(v, "keys") else []
        row = {"index": i, "keys": keys, "is_susy": bool(v.get("is_susy")) if hasattr(v, "get") else None}
        z = v.get("moduli") if hasattr(v, "get") else None
        if z is None:
            out["points"].append(row)
            print(f"  point {i}: no moduli key (keys={keys})", flush=True)
            continue
        z = np.asarray(z, dtype=complex)
        try:
            dw = np.asarray(model.DW(z), dtype=complex).ravel()
            res = float(np.linalg.norm(dw))
            row["dw_norm"] = res
            # the local Jacobian of the F-terms, by finite difference in the moduli directions
            n = z.size
            J = np.zeros((2 * n, 2 * n))
            step = 1e-6
            base = np.concatenate([dw.real, dw.imag])
            for k in range(n):
                zp = z.copy(); zp[k] += step
                d1 = np.asarray(model.DW(zp), dtype=complex).ravel()
                J[:, k] = (np.concatenate([d1.real, d1.imag]) - base) / step
                zp = z.copy(); zp[k] += 1j * step
                d2 = np.asarray(model.DW(zp), dtype=complex).ravel()
                J[:, n + k] = (np.concatenate([d2.real, d2.imag]) - base) / step
            sv = np.linalg.svd(J, compute_uv=False)
            row["jacobian_cond"] = float(sv[0] / max(sv[-1], 1e-300))
            row["jacobian_sv_min"] = float(sv[-1])
            row["jacobian_sv_max"] = float(sv[0])
        except Exception as e:  # noqa: BLE001
            row["error"] = f"{type(e).__name__}: {e}"
        out["points"].append(row)
        print(f"  point {i}: susy={row.get('is_susy')} |DW|={row.get('dw_norm')} "
              f"cond(J)={row.get('jacobian_cond')}", flush=True)
        with open("diagnose_solve.json", "w") as f:
            json.dump(out, f, indent=2)
    print("\nwrote diagnose_solve.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
