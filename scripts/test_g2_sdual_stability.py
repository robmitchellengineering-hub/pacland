"""G2 of the programme — is the S-dual of a stable vacuum itself stable?

**Why this is the next rung.** Law II showed `|W|` is invariant under S. That is necessary but
not sufficient for **well-definedness**: a duality must map a *vacuum* to a *vacuum*, not merely
a superpotential to an equal superpotential. G2 tests exactly that:

    take a vacuum (F, H, z, tau) with |DW| ~ 0
    apply S:  (F, H) -> (-H, F),  tau -> -1/tau,  z unchanged
    evaluate |DW| for the transformed flux at the transformed coupling, same moduli

If the transformed configuration also has `|DW| ~ 0`, duality maps vacua to vacua and C3's
well-definedness holds at degree 0. If it does not, the "one orbit" picture does not act on the
vacuum set at all, which is a major negative result.

**The control that makes this honest.** The same evaluation path is run on the *original* flux
first, and compared against the `|DW|` the corpus already stores for that row. If the probe
cannot reproduce the stored value, the probe is wrong and the G2 result is not reported — a
measurement that cannot reproduce a known answer is not a measurement.

**F-terms without guessing.** The library's exact F-term entry point is not documented in this
repo, so the script probes a short list of candidate attributes and, failing that, reports
`CANNOT-CHECK` with the attribute names it saw. It never invents a residual function.

Run on a node with jaxvacua:
    /home/rob/cytools-venv/bin/python scripts/test_g2_sdual_stability.py
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

DW_CANDIDATES = ("DW", "dW", "F_terms", "f_terms", "DW_norm", "residual", "grad_W",
                 "superpotential_gradients", "f_terms_moduli")


def content(flux):
    return reduce(gcd, [int(round(abs(x))) for x in flux], 0)


def pick_row():
    for fn in sorted(glob.glob("data/h12_*_stats.json")):
        doc = json.load(open(fn))
        for r in doc.get("vacua", []):
            if not r.get("is_susy") or not r.get("flux") or abs(r.get("tau", [0, 0])[1]) == 0:
                continue
            if content(r["flux"]) != 1:
                continue
            dw = r.get("|DW|")
            if dw is not None and float(dw) < 1e-6:  # a genuinely converged vacuum
                return fn, doc.get("h12"), doc.get("model_ID"), r
    return None, None, None, None


def find_dw(model):
    for name in DW_CANDIDATES:
        fn = getattr(model, name, None)
        if callable(fn):
            return name, fn
    return None, None


def main():
    fn, h12, mid, row = pick_row()
    if row is None:
        print("CANNOT-CHECK no converged primitive SUSY vacuum in data/")
        return 2
    model = jvc.FluxVacuaFinder(h12=h12, model_ID=mid, model_type="KS", maximum_degree=0)
    name, dw_fn = find_dw(model)
    print("=" * 80)
    print("G2 — S-duality must map a vacuum to a vacuum")
    print("=" * 80)
    print(f"row: {fn.split('/')[-1]}  h12={h12} model_ID={mid}  stored |DW| = {row.get('|DW|')}")

    if dw_fn is None:
        near = [a for a in dir(model) if any(k in a.lower() for k in
                                             ("dw", "resid", "kahler", "potential", "term"))]
        print(f"CANNOT-CHECK no F-term entry point among {DW_CANDIDATES}")
        print(f"  candidate attributes present: {near[:20]}")
        print("  -> G2 is NOT evaluated; reporting it as a pass would be a fabrication.")
        return 2

    moduli = jnp.array([complex(a, b) for a, b in row["moduli"]])
    tau = complex(row["tau"][0], row["tau"][1])
    f = [int(round(x)) for x in row["flux"]]
    half = len(f) // 2
    F, H = f[:half], f[half:]
    f_s = [-x for x in H] + list(F)
    tau_s = -1.0 / tau

    def dw_norm(flux, tau_v):
        try:
            val = dw_fn(moduli, tau_v, jnp.array(flux, dtype=float))
        except TypeError:
            val = dw_fn(jnp.array(flux, dtype=float), moduli, tau_v)
        arr = np.asarray(val)
        return float(np.linalg.norm(arr)), arr.shape

    print(f"using F-term entry point: {name}")
    orig, shape = dw_norm(f, tau)
    print(f"  control  |DW|(original)  = {orig:.6e}   (shape {shape})")
    stored = float(row.get("|DW|") or 0.0)
    if stored > 0 and not (orig <= 100 * max(stored, 1e-30) or abs(orig - stored) < 1e-6):
        print(f"  CONTROL FAILED: stored |DW| = {stored:.6e}, probe gives {orig:.6e}")
        print("  -> the probe does not reproduce a known value; G2 not reported.")
        return 2

    dual, _ = dw_norm(f_s, tau_s)
    print(f"  S-dual   |DW|(-H, F; -1/tau) = {dual:.6e}")
    print()
    tol = 1e-6
    if dual <= tol:
        print(f"  VERDICT: STABLE — |DW| = {dual:.3e} <= {tol:g}. Duality maps this vacuum to a")
        print("  vacuum: C3's well-definedness holds at degree 0 on this row.")
        return 0
    print(f"  VERDICT: NOT-STABLE — |DW| = {dual:.3e} > {tol:g}. The transformed pair is not a")
    print("  vacuum at the transformed coupling, so the orbit picture does not act on the")
    print("  vacuum set as claimed. This is a negative result and must be written up as one.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
