"""S-duality on real vacuua — the first direct test of the unification mechanism.

**Why this is the first unification step.** In this program unification is duality: the
claim is that vacua related by `Sp(b3, ℤ) × SL(2,ℤ)` are *one theory described twice*, so
the exact content must be invariant under it. `validate_full_duality.py` proves the group
acts and preserves the tadpole **symbolically**. What has never been tested is whether the
library's own superpotential and moduli actually realise that action on a real, sampled
vacuum.

**The transformation used.** The S-generator acts on the flux pair as

    (F, H) -> (-H, F)

and preserves the tadpole exactly: `N' = (-H)ᵀJ F = -HᵀJ F = FᵀJ H = N`, because `J` is
antisymmetric. It acts on the axio-dilaton as `τ -> -1/τ`. So for a genuine vacuum the
transformed pair must be a vacuum of the transformed theory at the transformed coupling.

**What is measured, and what would falsify it.** For each committed vacuum with content
`d = 1` we evaluate `W` at `(flux, τ)` and at `(-H, F)` with `τ' = -1/τ`, at the *same*
moduli, and report:

  * `|W'| / |W|` — the transformation law. If S-duality is realised, this is a clean
    function of τ across every vacuum; if it scatters, the library's W does not transform
    as the duality requires and the mechanism is unverified at degree 0.
  * the ratio against `|τ|` — the power `a` in `|W'| = |W| · |τ|^a`, fitted in log-log, with
    the residual. A good fit is evidence of a well-defined law; a bad fit is the falsifier.

**Honest status reporting.** Any row that fails (non-finite W, division by zero, library
error) is printed as a failure, never skipped, and the script exits non-zero if fewer than
half the rows could be evaluated.

Run on a node with jaxvacua:
    /home/rob/cytools-venv/bin/python scripts/validate_s_duality_vacua.py [max_rows]
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
    """SUSY vacua with primitive flux — the cleanest sample of genuine vacua."""
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


def main(argv):
    limit = int(argv[1]) if len(argv) > 1 else 60
    rows = load_susy_primitive(limit)
    print("=" * 84)
    print("S-duality on real vacua — (F,H) -> (-H,F),  tau -> -1/tau, at fixed moduli")
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

            W = complex(model.superpotential_gauge_invariant(moduli, tau, jnp.array(f, dtype=float)))
            f_s = [-x for x in H] + [x for x in F]
            tau_s = -1.0 / tau
            W_s = complex(model.superpotential_gauge_invariant(
                moduli, tau_s, jnp.array(f_s, dtype=float)))

            if not (np.isfinite(abs(W)) and np.isfinite(abs(W_s))) or abs(W) == 0:
                failures += 1
                print(f"  FAIL {fn.split('/')[-1]} h12={h12}: non-finite or zero W")
                continue
            ratio = abs(W_s) / abs(W)
            pts.append((abs(tau), ratio, fn.split("/")[-1], h12))
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"  FAIL {fn.split('/')[-1]} h12={h12}: {type(e).__name__}: {e}")

    print(f"\nevaluated {len(pts)}   failed {failures}")
    if len(pts) < max(1, len(rows) // 2):
        print("INSUFFICIENT: fewer than half the rows evaluated — do not interpret")
        return 1

    print(f"\n{'|tau|':>10} {'|W_S|/|W|':>12}  source")
    for at, ratio, fn, h12 in pts[:20]:
        print(f"{at:>10.3e} {ratio:>12.4e}  {fn} h12={h12}")
    if len(pts) > 20:
        print(f"... {len(pts) - 20} more")

    # the transformation law: fit log|W_S|/|W| = a log|tau| + b
    x = np.log(np.array([p[0] for p in pts]))
    y = np.log(np.array([p[1] for p in pts]))
    if len(x) >= 3 and np.ptp(x) > 0:
        a, b = np.polyfit(x, y, 1)
        resid = y - (a * x + b)
        print(f"\ntransformation law fit: |W_S|/|W| = exp({b:.4f}) * |tau|^{a:.4f}")
        print(f"  residual rms in log: {resid.std():.4f}   (near 0 = a law; large = no law)")
        verdict = "LAW" if resid.std() < 0.10 else "SCATTER"
        print(f"  verdict: {verdict}")
    else:
        print("\nnot enough spread in |tau| to fit a law")
        verdict = "NO-FIT"
    print("\nNOTE: this measures the realised transformation law. It does not assume the")
    print("textbook one, so a scatter result is a finding about the library, not a bug here.")
    print(f"\n===VERDICT=== {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
