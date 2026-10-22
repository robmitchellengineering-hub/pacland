"""The transformation table — piece 3 of the unification description.

**Why this replaces "coordinates on the orbit space".** Completeness proves `Sp(b3, R)` is
transitive on each tadpole level set, so over R there is **one orbit per tadpole**: the orbit
space is a point, and observables cannot be *coordinates* on it. What can be true — and what
makes the programme solid — is that the physical data are **covariant functions on the orbit**:
each transforms under the duality group by a definite law, and only the tadpole `N` is
invariant. So the dictionary is a **transformation table**, not a coordinate chart.

**The generators measured here** (both preserve `N = FᵀJH` because `J` is antisymmetric):

    S:  (F, H) -> (-H, F)        tau -> -1/tau
    T:  (F, H) -> (F, H + F)     tau -> tau + 1

**What is tabulated, per vacuum.** The complex ratio `W_gen/W` (not just its modulus, so a
phase change is visible), and `g_s' = 1/Im(tau')` against `g_s` — the coupling's transformation
is the one with an obvious physics reading (`g_s -> 1/g_s` under S would be the celebrated
statement).

**Falsifier, stated before the run.** If a generator leaves `|W|` invariant but moves it in
*phase* by something that is not a fixed function of `tau`, then `W` is not covariant and the
table has no law in it — that is a finding about the library, and it blocks the third piece.

Run on a node with jaxvacua:
    /home/rob/cytools-venv/bin/python scripts/diag_transformation_laws.py [max_rows]
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


def load(limit):
    rows = []
    for fn in sorted(glob.glob("data/h12_*_stats.json")):
        doc = json.load(open(fn))
        for r in doc.get("vacua", []):
            if not r.get("is_susy") or not r.get("flux"):
                continue
            if content(r["flux"]) != 1 or abs(r["tau"][1]) == 0:
                continue
            rows.append((doc.get("h12"), doc.get("model_ID"), r))
            if len(rows) >= limit:
                return rows
    return rows


def generators(f):
    half = len(f) // 2
    F, H = f[:half], f[half:]
    return {
        "S": ([-x for x in H] + list(F), "tau_minus_inv"),
        "T": (list(F) + [a + b for a, b in zip(H, F)], "tau_plus_one"),
    }


def main(argv):
    limit = int(argv[1]) if len(argv) > 1 else 30
    rows = load(limit)
    print("=" * 88)
    print("transformation table — how W and g_s move under the duality generators")
    print("=" * 88)
    if not rows:
        print("CANNOT-CHECK no primitive SUSY vacuum in data/")
        return 2

    table = {"S": [], "T": []}
    failures = 0
    for h12, mid, r in rows:
        try:
            model = jvc.FluxVacuaFinder(h12=h12, model_ID=mid, model_type="KS",
                                        maximum_degree=0)
            moduli = jnp.array([complex(a, b) for a, b in r["moduli"]])
            tau = complex(r["tau"][0], r["tau"][1])
            f = [int(round(x)) for x in r["flux"]]

            W = complex(model.superpotential_gauge_invariant(moduli, tau, jnp.array(f, dtype=float)))
            if abs(W) == 0 or not np.isfinite(abs(W)):
                failures += 1
                continue
            for name, (f2, tau_rule) in generators(f).items():
                tau2 = (-1.0 / tau) if tau_rule == "tau_minus_inv" else (tau + 1.0)
                W2 = complex(model.superpotential_gauge_invariant(
                    moduli, tau2, jnp.array(f2, dtype=float)))
                if not np.isfinite(abs(W2)):
                    failures += 1
                    continue
                table[name].append({
                    "tau": abs(tau), "tau2": abs(tau2),
                    "gs": 1.0 / abs(tau.imag), "gs2": 1.0 / abs(tau2.imag),
                    "ratio": W2 / W,
                    "abs_ratio": abs(W2) / abs(W),
                })
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"  FAIL h12={h12}: {type(e).__name__}: {e}")

    print(f"\nevaluated rows: {len(rows)}   failures: {failures}")
    for name in ("S", "T"):
        pts = table[name]
        if not pts:
            print(f"\n{name}: NO DATA — do not interpret")
            continue
        ar = np.array([p["abs_ratio"] for p in pts])
        ph = np.array([np.angle(p["ratio"]) for p in pts])
        print(f"\n{name} generator — n={len(pts)}")
        print(f"  |W'|/|W|   : mean {ar.mean():.6f}  min {ar.min():.6f}  max {ar.max():.6f}  std {ar.std():.3e}")
        print(f"  arg(W'/W)  : mean {ph.mean():+.6f} rad  std {ph.std():.3e}")
        gs_pairs = np.array([[p["gs"], p["gs2"]] for p in pts])
        print(f"  g_s        : {gs_pairs[:,0].mean():.4f} -> {gs_pairs[:,1].mean():.4f} "
              f"(per-vacuum g_s'/g_s mean {(gs_pairs[:,1]/gs_pairs[:,0]).mean():.4f})")
        verdict = ("LAW" if ar.std() < 1e-6 and ph.std() < 1e-6
                   else "LAW-IN-MODULUS" if ar.std() < 1e-6
                   else "SCATTER")
        print(f"  verdict    : {verdict}")

    print("\nNOTE: a LAWS table here is piece 3 of the description; a SCATTER is a finding.")
    print("===DONE===")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
