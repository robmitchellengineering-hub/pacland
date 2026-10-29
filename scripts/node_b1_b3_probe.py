"""B1 + B3 capability probe — what the oracle stack actually exposes, and the first real check of each.

B1 (GV integrality): the Gopakumar-Vafa invariants n_d are integers by definition. If the period
pipeline is right at a point, n_d comes out integral; non-integral means the periods are wrong THERE,
with no oracle needed. FALSIFIER: a non-integer n_d, or n_d that move with the point when they must not.

B3 (monodromy): the PF/GKZ system gives integer monodromy M with M^T Sigma M = Sigma.
FALSIFIER: M^T Sigma M != Sigma (implementation error), or a law that fails to close under a generator.

The first step of B3 is a CAPABILITY PROBE (the plan says so explicitly): does CYTools expose the
Picard-Fuchs operator and its monodromy? If not, this is a build and the build is the deliverable.

Run on pacland-rog:
    /home/rob/cytools-venv/bin/python scripts/node_b1_b3_probe.py
"""
import json
import sys

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np  # noqa: E402


def describe(obj, interesting):
    out = {}
    for name in interesting:
        out[name] = hasattr(obj, name)
    return out


def main() -> int:
    report = {"b1": {}, "b3": {}, "api": {}}
    import jaxvacua as jvc
    import cytools
    report["api"]["cytools_version"] = getattr(cytools, "__version__", "unknown")
    report["api"]["jaxvacua_version"] = getattr(jvc, "__version__", "unknown")

    # ---- B1: GV invariants -------------------------------------------------------------
    try:
        model = jvc.FluxVacuaFinder(h12=2, model_ID=1, model_type="KS", maximum_degree=1)
        report["b1"]["model_built"] = True
        names = [n for n in dir(model) if "gv" in n.lower() or "invariant" in n.lower()
                 or "prepot" in n.lower() or "period" in n.lower()]
        report["b1"]["candidate_attributes"] = names
        gv = None
        for attr in ("gv_invariants", "gv", "gv_invariants_list"):
            if hasattr(model, attr):
                val = getattr(model, attr)
                gv = val() if callable(val) else val
                report["b1"]["attribute_used"] = attr
                break
        if gv is None:
            cy = getattr(model, "cy", None) or getattr(model, "cy_model", None)
            if cy is not None:
                cands = [n for n in dir(cy) if "gv" in n.lower()]
                report["b1"]["cy_candidates"] = cands
                for attr in cands:
                    try:
                        val = getattr(cy, attr)
                        gv = val() if callable(val) else val
                        report["b1"]["attribute_used"] = f"cy.{attr}"
                        break
                    except Exception as e:  # noqa: BLE001
                        report["b1"].setdefault("errors", []).append(f"cy.{attr}: {e}")
        if gv is not None:
            arr = np.asarray(gv, dtype=float).ravel()
            finite = arr[np.isfinite(arr)]
            report["b1"]["n_values"] = int(finite.size)
            if finite.size:
                worst = float(np.max(np.abs(finite - np.round(finite))))
                report["b1"]["max_deviation_from_integer"] = worst
                report["b1"]["sample"] = [float(x) for x in finite[:8]]
                report["b1"]["verdict"] = "integral" if worst < 1e-6 else "NOT integral"
        else:
            report["b1"]["verdict"] = "not exposed"
    except Exception as e:  # noqa: BLE001
        report["b1"]["error"] = f"{type(e).__name__}: {e}"

    # ---- B3: monodromy capability ------------------------------------------------------
    try:
        cy = cytools.CalabiYau(h11=1, h12=101, favorite_coordinate="x", backend="atlas")
        report["b3"]["quintic_built"] = True
        has = describe(cy, ["picard_fuchs_equation", "picard_fuchs_operator",
                            "monodromy_matrices", "periods", "intersection_matrix",
                            "gv_invariants", "prepotential"])
        report["b3"]["capabilities"] = has
        if has.get("picard_fuchs_equation"):
            pf = cy.picard_fuchs_equation()
            report["b3"]["pf_curve"] = str(pf)[:300]
        if has.get("monodromy_matrices"):
            M = cy.monodromy_matrices()
            report["b3"]["n_monodromy"] = len(M) if hasattr(M, "__len__") else 1
            Sigma = np.array(cy.intersection_matrix(), dtype=float)
            ok = []
            for Mk in (M if hasattr(M, "__len__") else [M]):
                Mk = np.asarray(Mk, dtype=float)
                ok.append({"shape": list(Mk.shape),
                           "sp_residual": float(np.max(np.abs(Mk.T @ Sigma @ Mk - Sigma)))})
            report["b3"]["monodromy_checks"] = ok
    except Exception as e:  # noqa: BLE001
        report["b3"]["error"] = f"{type(e).__name__}: {e}"

    print(json.dumps(report, indent=2))
    with open("b1_b3_result.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nwrote b1_b3_result.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
