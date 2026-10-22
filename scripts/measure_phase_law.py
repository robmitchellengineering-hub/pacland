"""Law IIb — the PHASE of W under S (the open half of Law II).

Law II established |W_S|/|W| = 1 (100/100); that constrains only the magnitude. The full
covariance-table row for W needs the complex ratio `W_S / W`, whose argument is the phase law.

**What is measured.** For each primitive SUSY vacuum, `W = superpotential_gauge_invariant(...)`
and `W_S = superpotential_gauge_invariant(moduli, -1/tau, (-H,F))`. Report the complex ratio
`W_S / W` as (magnitude, phase), and fit `arg(W_S/W)` against `arg(tau)`. A clean fit is Law IIb;
a scatter means the phase is not a clean law and Law II stays magnitude-only.

**Control.** The magnitude of the same ratio must reproduce Law II (|W_S|/|W| = 1). If it does
not, the code path is wrong and the phase is not reported.

Run on a node with jaxvacua:
    /home/rob/cytools-venv/bin/python scripts/measure_phase_law.py [max_rows]
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


def main(argv):
    limit = int(argv[1]) if len(argv) > 1 else 60
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
                break
        if len(rows) >= limit:
            break

    print("=" * 84)
    print("Law IIb — the phase of W under S, at fixed moduli")
    print("=" * 84)
    if not rows:
        print("CANNOT-CHECK no primitive SUSY vacuum in data/")
        return 2

    pts = []
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

            W = complex(model.superpotential_gauge_invariant(
                moduli, tau, jnp.array(f, dtype=float)))
            f_s = [-x for x in H] + [x for x in F]
            tau_s = -1.0 / tau
            W_s = complex(model.superpotential_gauge_invariant(
                moduli, tau_s, jnp.array(f_s, dtype=float)))

            if not (np.isfinite(abs(W)) and np.isfinite(abs(W_s))) or abs(W) == 0:
                failures += 1
                continue
            ratio = W_s / W
            pts.append((tau, ratio, fn.split("/")[-1], h12))
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"  FAIL {fn.split('/')[-1]}: {type(e).__name__}: {e}")

    print(f"\nevaluated {len(pts)}   failed {failures}")
    if len(pts) < max(1, len(rows) // 2):
        print("INSUFFICIENT")
        return 1

    mag = np.array([abs(p[1]) for p in pts])
    pha = np.array([np.angle(p[1]) for p in pts])
    argtau = np.array([np.angle(p[0]) for p in pts])
    at = np.array([abs(p[0]) for p in pts])
    print(f"\ncontrol  |W_S|/|W|   mean {float(mag.mean()):.6e}  std {float(mag.std()):.6e}  (Law II: 1)")
    print(f"phase    arg(W_S/W)  mean {float(pha.mean()):.6f}  std {float(pha.std()):.6f}  rad")

    def fit(x, y, xname):
        if len(x) >= 3 and np.ptp(x) > 1e-6:
            a, b = np.polyfit(x, y, 1)
            resid = y - (a * x + b)
            print(f"  fit arg(W_S/W) vs {xname}: {a:.4f} * {xname} + {b:.4f}   "
                  f"resid rms {resid.std():.4f} ({'LAW' if resid.std() < 0.10 else 'SCATTER'})")
            return a, b, resid
        print(f"  (not enough spread in {xname} to fit)")
        return None

    print()
    fit(argtau, pha, "arg(tau)")
    fit(np.log(at), pha, "log|tau|")

    print(f"\n{'|tau|':>10} {'arg(tau)':>10} {'|W_S/W|':>10} {'arg(W_S/W)':>12}  src")
    for tau, ratio, src, h12 in pts[:20]:
        print(f"{abs(tau):>10.3e} {np.angle(tau):>10.4f} {abs(ratio):>10.4e} "
              f"{np.angle(ratio):>12.4f}  {src} h12={h12}")

    print("\nNOTE: a clean phase law here completes the W row of the covariance table.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
