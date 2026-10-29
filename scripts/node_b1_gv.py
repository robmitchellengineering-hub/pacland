"""B1 — GV integrality, extracted from the computed prepotential at several points.

Gopakumar-Vafa invariants n_d are integers by definition (BPS counts). Extracting them from the
*computed* prepotential and finding non-integers means the period pipeline is wrong at those points,
with no oracle needed.

FALSIFIER (stated before the run, plan §4 B1): a non-integer n_d, or n_d that move with the point when
they must not.

Method: `F_inst(moduli)` is the worldsheet-instanton part of the prepotential. At imaginary moduli
`t = i y` the instanton expansion is real and dominated by low degree:

    F_inst(i y) = sum_{d > 0} n_d * Li_3(e^{-2 pi d.y}) / (2 pi i)^3      (times the model's convention)

so with several y-vectors and a basis of Li_3 terms the n_d are a linear least-squares problem. Two
checks follow, and they are the two halves of the falsifier:

  1 INTEGRALITY — every fitted n_d must sit on an integer.
  2 STABILITY — the fit on one set of points must agree with the fit on a disjoint set.

Run on pacland-rog:
    /home/rob/cytools-venv/bin/python scripts/node_b1_gv.py [h12] [model_ID]
"""
import itertools
import json
import sys

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np  # noqa: E402
import jaxvacua as jvc  # noqa: E402


def li3(z: complex, terms: int = 60) -> complex:
    s = 0.0 + 0.0j
    for k in range(1, terms + 1):
        s += z ** k / k ** 3
    return s


def degrees(h12: int, max_component: int):
    out = []
    for combo in itertools.product(range(max_component + 1), repeat=h12):
        if sum(combo) == 0 or sum(combo) > max_component:
            continue
        out.append(tuple(combo))
    return out


def fit(model, ys, degs):
    """Least squares for n_d over the given moduli points."""
    A, b = [], []
    for y in ys:
        t = 1j * np.asarray(y)
        f = complex(model.F_inst(t, False))
        row = [li3(np.exp(-2 * np.pi * (np.dot(d, y)))) / (2 * np.pi * 1j) ** 3 for d in degs]
        A.append(row)
        b.append(f)
    A = np.asarray(A, dtype=complex)
    b = np.asarray(b, dtype=complex)
    coef, *_ = np.linalg.lstsq(A, b, rcond=None)
    resid = float(np.linalg.norm(A @ coef - b) / max(np.linalg.norm(b), 1e-300))
    return coef, resid


def main(argv):
    h12 = int(argv[1]) if len(argv) > 1 else 2
    model_id = int(argv[2]) if len(argv) > 2 else 1
    max_comp = 3
    degs = degrees(h12, max_comp)
    report = {"h12": h12, "model_id": model_id, "n_degrees": len(degs),
              "max_component": max_comp,
              "falsifier": "a non-integer n_d, or n_d that move with the point"}
    print("=" * 92)
    print(f"B1 · GV integrality from the computed prepotential — h12={h12} model_ID={model_id}")
    print("falsifier, stated before the run: a non-integer n_d, or n_d that move with the point")
    print("=" * 92)

    results = {}
    for degree in (1, 2, 3):
        model = jvc.FluxVacuaFinder(h12=h12, model_ID=model_id, model_type="KS",
                                    maximum_degree=degree, mirror_instanton=True)
        rng = np.random.default_rng(7)
        all_ys = [rng.uniform(0.8, 2.6, h12) for _ in range(2 * len(degs) + 6)]
        ys_a, ys_b = all_ys[0::2], all_ys[1::2]
        coef_a, res_a = fit(model, ys_a, degs)
        coef_b, res_b = fit(model, ys_b, degs)
        real_a = np.real(coef_a)
        dev = np.abs(real_a - np.round(real_a))
        drift = np.abs(real_a - np.real(coef_b))
        results[degree] = {
            "fit_residual_a": res_a, "fit_residual_b": res_b,
            "max_dev_from_integer": float(dev.max()), "median_dev": float(np.median(dev)),
            "max_drift_between_point_sets": float(drift.max()),
            "n_d": {str(d): float(v) for d, v in zip(degs, real_a)},
            "integral": bool(dev.max() < 1e-3), "stable": bool(drift.max() < 1e-3),
        }
        print(f"\nmaximum_degree={degree}: fit residual {res_a:.2e} / {res_b:.2e}")
        for d, v in list(zip(degs, real_a))[:8]:
            print(f"   n_{d} = {v:+.6f}   (dev {abs(v - round(v)):.1e})")
        print(f"   max deviation from integer: {dev.max():.3e} | max drift between point sets: "
              f"{drift.max():.3e}")
    report["results"] = {str(k): v for k, v in results.items()}

    # convergence across degrees, as a bonus check on the series
    if "1" in report["results"] and "3" in report["results"]:
        a = np.array(list(results[1]["n_d"].values()))
        c = np.array(list(results[3]["n_d"].values()))
        report["degree1_vs_degree3_max_rel"] = float(np.max(np.abs(a - c) / np.maximum(np.abs(c), 1e-12)))
        print(f"\ndegree 1 vs degree 3, max relative change: {report['degree1_vs_degree3_max_rel']:.3e}")

    print("\n" + json.dumps({"falsifier": report["falsifier"],
                             "integral_deg2": results[2]["integral"],
                             "stable_deg2": results[2]["stable"],
                             "max_dev_deg2": results[2]["max_dev_from_integer"]}, indent=2))
    with open("b1_gv.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nwrote b1_gv.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
