"""Diagnose the ISD conditioning wall — the measurement behind `docs/h12-25-sampling-wall.md`.

**Why this exists.** The wall document reports cond(M) = 1.8e2 at h12=2 rising to 4.8e6 at
h12=25 (up to 2.7e10 across polytopes), and that number is the entire case for "the wall is
at the ISD proposal". But there was no script in the repo that produced it, so the result
could not be reproduced or attacked. This is that script.

**What it measures, per h12.** The ISD Hodge-⋆ matrix `M` is the model's own
`ISD_matrix(moduli, moduli_conj)` (`jaxvacua/css.py`, also `periods.py`). We report
`eigvalsh(M)` and its condition number **at a moduli point**, plus the composition of the
eigenvector belonging to the smallest-magnitude eigenvalue — the object the fix would
project out.

**The distinction that matters.** The wall doc says the near-null direction may be either
a truncation artefact or a real hierarchy; it never tests which. The **composition** of that
eigenvector is the discriminator, so it is printed as a plain number: the fraction of the
eigenvector's weight sitting on the last coordinate(s) (the axio-dilaton / boundary block)
versus the moduli block. A direction concentrated on the boundary is a truncation signature;
one spread through the moduli is a physical hierarchy.

**Manifest honesty.** The moduli point is the weak link, so it is reported with its source:
`committed-vacuum` (a row from `data/`, trustworthy), `isd-initial-guess`, or `unavailable`
— and an `unavailable` row is printed as such, never silently skipped.

Run on a node with jaxvacua (the Mac has none):
    /home/rob/cytools-venv/bin/python scripts/diagnose_isd_conditioning.py [h12 ...]
"""
import glob
import json
import sys

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
import jaxvacua as jvc  # noqa: E402

DEFAULT_H12 = [2, 3, 4, 5, 10, 15, 20, 25]


def committed_moduli(h12):
    """A real, in-cone moduli point from the committed corpus, if this h12 has one."""
    for fn in sorted(glob.glob(f"data/h12_{h12}_m*_stats.json")):
        doc = json.load(open(fn))
        for r in doc.get("vacua", []):
            m = r.get("moduli")
            if m and len(m) == h12:
                return np.array([complex(a, b) for a, b in m]), fn.split("/")[-1]
    return None, None


def isd_initial_guess(model, n=2):
    """The sampler's own ISD initial guess — the point the proposal actually starts from."""
    for args in ((n,), (n, None), ()):
        try:
            out = model.initial_guesses_ISD(*args)
            arr = np.asarray(out)
            # accept a single moduli vector of length h12, or the first row of a batch
            if arr.ndim == 1 and arr.shape[0] == model.h12:
                return arr.astype(complex), "isd-initial-guess"
            if arr.ndim == 2 and arr.shape[1] == model.h12 and arr.shape[0] > 0:
                return arr[0].astype(complex), "isd-initial-guess"
        except Exception:
            continue
    return None, None


def diagnose(h12):
    try:
        model = jvc.FluxVacuaFinder(h12=h12, model_ID=1, model_type="KS", maximum_degree=0)
    except Exception as e:  # noqa: BLE001
        return {"h12": h12, "status": f"model-build-failed: {type(e).__name__}: {e}"}

    moduli, source = committed_moduli(h12)
    if moduli is None:
        moduli, source = isd_initial_guess(model)
    if moduli is None:
        return {"h12": h12, "status": "unavailable: no committed vacuum and no ISD initial guess"}

    try:
        M = np.asarray(model.ISD_matrix(jnp.asarray(moduli), jnp.asarray(moduli.conj())))
        ev, vecs = np.linalg.eigh(M)
        ev_abs = np.abs(ev)
        cond = float(ev_abs.max() / ev_abs.min()) if ev_abs.min() > 0 else float("inf")
        k = int(np.argmin(ev_abs))
        v = vecs[:, k]
        dim = len(v)
        # the last two components are the axio-dilaton; the rest are the complex-structure moduli
        weight = np.abs(v) ** 2
        total = weight.sum()
        boundary_frac = float(weight[max(dim - 2, 0):].sum() / total) if total > 0 else float("nan")
        return {
            "h12": h12,
            "status": "ok",
            "moduli_source": source,
            "dim_M": dim,
            "eig_min": float(ev_abs.min()),
            "eig_max": float(ev_abs.max()),
            "cond_M": cond,
            "near_null_eig_index": k,
            "near_null_boundary_weight": boundary_frac,
            "near_null_top_components": [
                int(i) for i in np.argsort(weight)[::-1][:3]
            ],
        }
    except Exception as e:  # noqa: BLE001
        return {"h12": h12, "status": f"measure-failed: {type(e).__name__}: {e}", "moduli_source": source}


def main(argv):
    hs = [int(a) for a in argv[1:]] or DEFAULT_H12
    rows = [diagnose(h) for h in hs]

    print("=" * 84)
    print("ISD conditioning diagnostic — is the wall the truncation or a real hierarchy?")
    print("=" * 84)
    print(f"{'h12':>4} {'dim':>4} {'eig_min':>11} {'eig_max':>11} {'cond(M)':>12} "
          f"{'boundary w':>11}  source / status")
    for r in rows:
        if r.get("status") != "ok":
            print(f"{r['h12']:>4} {'-':>4} {'-':>11} {'-':>11} {'-':>12} {'-':>11}  {r['status']}")
            continue
        print(f"{r['h12']:>4} {r['dim_M']:>4} {r['eig_min']:>11.3e} {r['eig_max']:>11.3e} "
              f"{r['cond_M']:>12.3e} {r['near_null_boundary_weight']:>11.3f}  {r['moduli_source']}")

    ok = [r for r in rows if r.get("status") == "ok"]
    print()
    if len(ok) >= 2:
        lo, hi = ok[0], ok[-1]
        print(f"cond(M) {lo['h12']} -> {hi['h12']}: {lo['cond_M']:.3e} -> {hi['cond_M']:.3e} "
              f"({hi['cond_M'] / lo['cond_M']:.1f}x)")
        fracs = [r["near_null_boundary_weight"] for r in ok]
        print(f"near-null boundary weight: min {min(fracs):.3f} max {max(fracs):.3f} "
              f"(->1.0 = truncation signature, widely spread = physical hierarchy)")
    print()
    print("INTERPRETATION IS NOT AUTOMATIC: this prints the numbers the decision needs. The")
    print("call on truncation-vs-hierarchy is made from the trend in `boundary w`, not here.")

    print("\n===JSON===")
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
