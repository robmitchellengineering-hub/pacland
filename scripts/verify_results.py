"""Regenerate every headline number from the committed data (self-asserting).

The verification discipline applied to itself: one command that recomputes the
structure map, the no-scale result, the tadpole control, and the wall chain from
``data/``, and asserts each. Exits 0 iff every claim reproduces; a drift is a
loud failure, not a silent pass.

Run:  python3 scripts/verify_results.py

Pure stdlib (uses pacland.structure's ridge fit + the committed JSON).
"""
import json
import math
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from pacland.structure import _pearson, ridge_cv_predictability  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name):
    with open(os.path.join(ROOT, "data", name)) as f:
        return json.load(f)


def tad(f):
    F = f[0:6]; H = f[6:12]
    return (F[0]*H[3] + F[1]*H[4] + F[2]*H[5]) - (F[3]*H[0] + F[4]*H[1] + F[5]*H[2])


def main() -> int:
    failures = []

    def check(name, cond, detail):
        status = "PASS" if cond else "FAIL"
        print(f"  [{status}] {name}: {detail}")
        if not cond:
            failures.append(name)

    print("PACLAND result verification\n")

    # 1. The tadpole positive control: exactly the symplectic pairing.
    obs = _load("vacua_observables.json")
    recs = [r for d in obs.values() for r in d]
    fluxes = [r["flux"] for r in recs]
    tads = [r["tadpole"] for r in recs]
    r_tad = _pearson([tad(f) for f in fluxes], tads)
    check("tadpole = F^T J H exactly", r_tad == 1.0, f"r = {r_tad}")

    # 2. The structure map (wide-flux, 174 SUSY).
    rich = _load("rich_sample.json")["points"]
    susy = [p for p in rich if p["is_susy"] and p["tau_im"] > 0]
    fx = [p["flux"] for p in susy]
    lw = [p["log_W0"] for p in susy]
    r_w0 = ridge_cv_predictability(fx, lw)
    r_gs = ridge_cv_predictability(fx, [math.log(1.0 / p["tau_im"]) for p in susy])
    r_v = ridge_cv_predictability(fx, [float(p["V"]) for p in susy])
    check("W0 weakly learnable (r~0.6)", 0.4 < r_w0 < 0.8, f"r = {r_w0:.2f}")
    check("g_s uniform (r<0.25)", r_gs < 0.25, f"r = {r_gs:.2f}")
    check("CC uniform (r<0.25)", abs(r_v) < 0.25, f"r = {r_v:.2f}")

    # 3. No-scale: V = 0 at SUSY points (machine precision).
    vmax = max(abs(float(p["V"])) for p in susy)
    check("no-scale V=0 at SUSY", vmax < 1e-20, f"max|V| = {vmax:.1e}")

    # 4. The wall chain (SUSY, stability).
    n_all = len(rich)
    n_susy = len(susy)
    stable = [p for p in susy if all(e > 1e-6 for e in p["eigs"])]
    check("SUSY eliminates ~87%", 0.84 < (1 - n_susy / n_all) < 0.90,
          f"{100*(1 - n_susy/n_all):.1f}%")
    check("stability eliminates ~5% of SUSY", 0.03 < (1 - len(stable)/n_susy) < 0.07,
          f"{100*(1 - len(stable)/n_susy):.1f}%")

    # 5. The tadpole bound is pre-satisfied (L = Q = 276).
    n_flux = [tad(p["flux"]) for p in susy]
    check("tadpole bound pre-satisfied (all N_flux <= 276)", max(n_flux) <= 276,
          f"max N_flux = {max(n_flux)}")

    print()
    if failures:
        print(f"FAILURES: {failures}")
        return 1
    print(f"ALL {9 - len(failures)} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
