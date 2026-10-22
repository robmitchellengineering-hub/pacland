"""Numeric control for the flux-scaling lemma, on real committed vacua.

The lemma (`scripts/validate_flux_scaling_lemma.py`) is exact algebra: `W` is linear in the
flux, so `W(d·flux) = d·W(flux)` and `DW` zeros are preserved. This script checks the same
identity **against the library** at a real vacuum's own moduli — the one place a nonlinearity
could hide (if `superpotential_gauge_invariant` is not flux-linear, this fails and that is a
finding about the library, not about the lemma).

Takes a SUSY row with content d = gcd(F,H) = 1 from the committed corpus, evaluates `|W|` at
the stored moduli/tau for the flux and for `2·flux`, and asserts the ratio is exactly 2.

Run on a node with jaxvacua (the Mac has none):
    python3 scripts/verify_flux_scaling_numeric.py
"""
import glob
import json
import sys
from functools import reduce
from math import gcd

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import jaxvacua as jvc  # noqa: E402

TOL = 1e-10


def content(flux):
    return reduce(gcd, [int(round(abs(x))) for x in flux], 0)


def find_case():
    """First SUSY row with primitive content (d=1) — scaling it by 2 gives content 2."""
    for fn in sorted(glob.glob("data/h12_*_stats.json")):
        doc = json.load(open(fn))
        for r in doc.get("vacua", []):
            if not r.get("is_susy") or not r.get("flux"):
                continue
            if content(r["flux"]) != 1:
                continue
            if abs(r["tau"][1]) == 0:
                continue
            return fn, doc.get("h12"), doc.get("model_ID"), r
    return None, None, None, None


def main():
    fn, h12, model_id, row = find_case()
    if row is None:
        print("CANNOT-CHECK no primitive SUSY vacuum found in data/ — nothing to test")
        return 2

    model = jvc.FluxVacuaFinder(h12=h12, model_ID=model_id, model_type="KS", maximum_degree=0)
    moduli = jnp.array([[m[0], m[1]] for m in row["moduli"]], dtype=complex)
    tau = complex(row["tau"][0], row["tau"][1])
    flux = [int(round(x)) for x in row["flux"]]

    def W_of(f):
        return complex(model.superpotential_gauge_invariant(
            moduli, tau, jnp.array(f, dtype=float)))

    W1 = W_of(flux)
    W2 = W_of([2 * x for x in flux])

    print("=" * 72)
    print("numeric control — flux scaling against the library, at a real vacuum")
    print("=" * 72)
    print(f"source          : {fn.split('/')[-1]}  h12={h12} model_ID={model_id}")
    print(f"content d       : {content(flux)} -> scaled content {content([2 * x for x in flux])}")
    print(f"tadpole Nflux   : {row.get('Nflux')} (scaled tadpole would be 4x by bilinearity)")
    print(f"|W(F)|          : {abs(W1):.12e}")
    print(f"|W(2F)|         : {abs(W2):.12e}")
    ratio = abs(W2) / abs(W1) if W1 != 0 else float("inf")
    print(f"ratio |W(2F)|/|W(F)| = {ratio!r}   (lemma requires exactly 2)")

    ok = abs(ratio - 2.0) <= TOL
    print(f"[{'PASS' if ok else 'FAIL'}] ratio == 2 within {TOL:g}")
    if not ok:
        print("  The library's superpotential is NOT flux-linear at this point. That contradicts")
        print("  the lemma's premise, so report it as a finding about the library, not the lemma.")
        return 1
    print()
    print("Confirmed: scaling the flux by 2 doubles W at identical moduli. The lemma's premise")
    print("holds in the library, so the content d adds nothing beyond d·W and d²·N.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
