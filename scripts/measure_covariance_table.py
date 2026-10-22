"""The covariance table, rows 2 and 3 — |W| and g_s under S and T (Law III + the T-row).

**Why this is the unification step.** "One theory described twice" is operational only when every
observable has a closed-form law under the duality group. Law II (validate_s_duality_vacua.py)
filled the S-row of |W|: |W_S|/|W| = 1, 25/25. This script fills two more rows of the covariance
table, each measured with a control that could have failed:

  * **g_s under S and T.** g_s = 1/Im(tau) is the definition; under S (tau -> -1/tau) it must give
    g_s' = |tau|^2 * g_s  (which is 1/g_s only when C0 = 0), and under T (tau -> tau+1) it must
    give g_s' = g_s. These are *theorems* of the S/T action, so a deviation is a bug in the
    measurement, not a physics finding — exactly what the 2209Z "g_s -> 3.9e7" result was.
  * **|W| under T.** The S-row (Law II) is the CONTROL: if this script reproduces |W_S|/|W| = 1 on
    the same sample, the code path is validated, and the T-row measured on the same path is a real
    measurement, not an artefact. The T-row is the new covariance-table entry.

**Transforms.** S: (F,H) -> (-H,F), tau -> -1/tau.  T: (F,H) -> (F, F+H), tau -> tau+1. Moduli held
fixed (degree-0 slice). W is `superpotential_gauge_invariant` (the Law II convention, normalise=True).

**Honest reporting.** Any row that fails (non-finite W, zero W) is printed as a failure, never
skipped. Fewer than half evaluated => INSUFFICIENT, exit non-zero.

Run on a node with jaxvacua:
    /home/rob/cytools-venv/bin/python scripts/measure_covariance_table.py [max_rows]
"""
import glob
import json
import sys
from functools import reduce
from math import gcd

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
import jaxvacua as jvc  # noqa: E402


def content(flux):
    return reduce(gcd, [int(round(abs(x))) for x in flux], 0)


def load_susy_primitive(limit):
    rows = []
    for fn in sorted(glob.glob("data/h12_*_stats.json")):
        doc = json.load(open(fn))
        for r in doc.get("vacua", []):
            if not r.get("is_susy") or not r.get("flux"):
                continue
            if content(r["flux"]) != 1 or abs(r["tau"][1]) == 0:
                continue
            rows.append((fn, doc.get("h12"), doc.get("model_ID"), r))
            if len(rows) >= limit:
                return rows
    return rows


def W_of(model, moduli, tau, flux):
    return complex(model.superpotential_gauge_invariant(
        moduli, tau, jnp.array(flux, dtype=float)))


def main(argv):
    limit = int(argv[1]) if len(argv) > 1 else 60
    rows = load_susy_primitive(limit)
    print("=" * 84)
    print("covariance table — |W| and g_s under S and T, at fixed moduli")
    print("=" * 84)
    if not rows:
        print("CANNOT-CHECK no primitive SUSY vacuum in data/")
        return 2

    pts = []       # (|tau|, gs_ratio_S, gs_ratio_T, w_ratio_S, w_ratio_T, source, h12)
    failures = 0
    for fn, h12, model_id, r in rows:
        try:
            model = jvc.FluxVacuaFinder(h12=h12, model_ID=model_id, model_type="KS",
                                        maximum_degree=0)
            moduli = jnp.array([complex(a, b) for a, b in r["moduli"]])
            tau = complex(r["tau"][0], r["tau"][1])
            f = [int(round(x)) for x in r["flux"]]
            half = len(f) // 2
            F, H = f[:half], f[half:]

            gs = 1.0 / tau.imag

            # S: (F,H)->(-H,F), tau -> -1/tau
            f_s = [-x for x in H] + [x for x in F]
            tau_s = -1.0 / tau
            gs_s = 1.0 / tau_s.imag
            # T: (F,H)->(F,F+H), tau -> tau+1
            f_t = [x for x in F] + [x + y for x, y in zip(F, H)]
            tau_t = tau + 1.0
            gs_t = 1.0 / tau_t.imag

            W = W_of(model, moduli, tau, f)
            W_s = W_of(model, moduli, tau_s, f_s)
            W_t = W_of(model, moduli, tau_t, f_t)

            if not (np.isfinite(abs(W)) and np.isfinite(abs(W_s)) and np.isfinite(abs(W_t))) \
                    or abs(W) == 0:
                failures += 1
                print(f"  FAIL {fn.split('/')[-1]} h12={h12}: non-finite or zero W")
                continue

            gs_ratio_S = gs_s / (abs(tau) ** 2 * gs)   # law: g_s' = |tau|^2 g_s  => 1
            gs_ratio_T = gs_t / gs                     # law: g_s' = g_s          => 1
            w_ratio_S = abs(W_s) / abs(W)              # Law II control            => 1
            w_ratio_T = abs(W_t) / abs(W)              # new row
            pts.append((abs(tau), gs_ratio_S, gs_ratio_T, w_ratio_S, w_ratio_T,
                        fn.split("/")[-1], h12))
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"  FAIL {fn.split('/')[-1]} h12={h12}: {type(e).__name__}: {e}")

    print(f"\nevaluated {len(pts)}   failed {failures}")
    if len(pts) < max(1, len(rows) // 2):
        print("INSUFFICIENT: fewer than half the rows evaluated — do not interpret")
        return 1

    gsr_s = np.array([p[1] for p in pts])
    gsr_t = np.array([p[2] for p in pts])
    wsr_s = np.array([p[3] for p in pts])
    wsr_t = np.array([p[4] for p in pts])

    def row(name, vals, target, tol):
        mean, std = float(vals.mean()), float(vals.std())
        ok = abs(mean - target) < tol and std < tol
        print(f"  {name:22s} mean {mean:12.6e}  std {std:12.6e}  "
              f"target {target:g}  -> {'LAW' if ok else 'DEVIATION'}")
        return ok

    print("\n--- g_s rows (definitional; a DEVIATION here is a measurement bug) ---")
    row("g_s_S / (|tau|^2 g_s)", gsr_s, 1.0, 1e-6)
    row("g_s_T / g_s", gsr_t, 1.0, 1e-6)

    print("\n--- |W| rows (library measurements) ---")
    row("|W_S| / |W|  (Law II)", wsr_s, 1.0, 1e-6)
    # the T-row is measured, not assumed: fit log|W_T|/|W| = a log|tau| + b
    x = np.log(np.array([p[0] for p in pts]))
    y = np.log(wsr_t)
    print(f"  |W_T| / |W|              mean {float(wsr_t.mean()):12.6e}  std {float(wsr_t.std()):12.6e}")
    if len(x) >= 3 and np.ptp(x) > 0:
        a, b = np.polyfit(x, y, 1)
        resid = y - (a * x + b)
        print(f"  T-law fit: |W_T|/|W| = exp({b:.4f}) * |tau|^{a:.4f}")
        print(f"  residual rms in log: {resid.std():.4f}  "
              f"({'LAW' if resid.std() < 0.10 else 'SCATTER'})")

    print("\n--- per-row (first 20) ---")
    print(f"{'|tau|':>10} {'gsS/|t|^2gs':>12} {'gsT/gs':>10} {'|W_S|/|W|':>10} {'|W_T|/|W|':>10}  src")
    for at, a1, a2, a3, a4, src, h12 in pts[:20]:
        print(f"{at:>10.3e} {a1:>12.4e} {a2:>10.4e} {a3:>10.4e} {a4:>10.4e}  {src} h12={h12}")

    print("\nNOTE: g_s rows are definitional; |W| rows are measured. The S-row is the control.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
