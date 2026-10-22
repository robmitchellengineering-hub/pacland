"""G3 — the truncation scan: how conditioning of the ISD matrix behaves with h12.

**The question this answers.** `docs/h12-25-sampling-wall.md` says the wall is the ISD matrix's
conditioning, growing from `1.8e2` at `h12=2` to `4.8e6` at `h12=25`. That claim decides whether
the h12 frontier is a landscape fact or a proposal artefact, and it has never been reproducible
from the repo.

**The stage error this fixes.** A first attempt measured `cond(M)` on *converged* corpus vacua and
got `~1e135`. That was my error, not the doc's: at a SUSY vacuum `⋆G = iG`, so the ISD matrix is
**singular by construction** and its condition number there is meaningless. The doc's number is a
**proposal-stage** quantity. `FluxVacuaFinder` exposes `ISD_matrix(moduli, moduli_conj)` but the
proposal's moduli come from a sampler class it does not expose, so this script does the
stage-free version instead:

    draw moduli points from a STATED box, and report cond(M) over the box per h12.

**What is honest here and what is not.**
- Honest: the box is printed, every h12 is measured the same way, and the trend across h12 is a
  real property of `M` over that box.
- Not claimed: that these points lie in the Kähler cone (cone membership is not enforced — no
  sampler is available), and therefore not claimed to be the doc's exact numbers. It is the
  *trend* that carries the physics, and the trend is what the wall hypothesis needs.
- Several scales are measured, so a conclusion that only holds at one scale is visible as such.

Run on the powerhouse node:
    /home/rob/cytools-venv/bin/python scripts/scan_isd_conditioning.py
"""
import sys

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
import jaxvacua as jvc  # noqa: E402

H12 = [2, 3, 4, 5, 10, 15, 20, 25]
SCALES = [1.0, 10.0, 100.0]
N_POINTS = 6
SEED = 20261022


def measure(h12, scale, rng):
    try:
        model = jvc.FluxVacuaFinder(h12=h12, model_ID=1, model_type="KS", maximum_degree=0)
    except Exception as e:  # noqa: BLE001
        return {"h12": h12, "scale": scale, "status": f"model-build-failed: {type(e).__name__}"}

    conds, boundary = [], []
    for _ in range(N_POINTS):
        try:
            z = scale * (rng.uniform(-1, 1, h12) + 1j * rng.uniform(0.5, 3.0, h12))
            M = np.asarray(model.ISD_matrix(jnp.asarray(z), jnp.asarray(z.conj())))
            ev, vecs = np.linalg.eigh(M)
            a = np.abs(ev)
            if a.min() <= 0:
                continue
            conds.append(a.max() / a.min())
            v = np.abs(vecs[:, int(np.argmin(a))]) ** 2
            tot = v.sum()
            boundary.append(float(v[max(len(v) - 2, 0):].sum() / tot) if tot > 0 else float("nan"))
        except Exception:  # noqa: BLE001
            continue
    if not conds:
        return {"h12": h12, "scale": scale, "status": "all points failed"}
    return {
        "h12": h12, "scale": scale, "status": "ok",
        "n": len(conds),
        "cond_median": float(np.median(conds)),
        "cond_min": float(np.min(conds)),
        "cond_max": float(np.max(conds)),
        "boundary_median": float(np.nanmedian(boundary)),
    }


def main():
    rng = np.random.default_rng(SEED)
    rows = [measure(h, s, rng) for h in H12 for s in SCALES]

    print("=" * 96)
    print("G3 — cond(M) over a stated moduli box, by h12 and scale")
    print(f"box: Re z in [-s, s], Im z in [0.5s, 3.0s], s in {SCALES}; {N_POINTS} points each; seed {SEED}")
    print("NOTE: cone membership NOT enforced (no sampler exposed by FluxVacuaFinder) —")
    print("      this is the trend of cond(M) over the box, not the wall doc's exact numbers.")
    print("=" * 96)
    print(f"{'h12':>4} {'scale':>6} {'n':>3} {'cond med':>12} {'cond min':>12} {'cond max':>12} {'bnd med':>8}  status")
    for r in rows:
        if r.get("status") != "ok":
            print(f"{r['h12']:>4} {r['scale']:>6} {'-':>3} {'-':>12} {'-':>12} {'-':>12} {'-':>8}  {r['status']}")
            continue
        print(f"{r['h12']:>4} {r['scale']:>6} {r['n']:>3} {r['cond_median']:>12.3e} "
              f"{r['cond_min']:>12.3e} {r['cond_max']:>12.3e} {r['boundary_median']:>8.3f}  {r['status']}")

    print()
    for s in SCALES:
        ok = [r for r in rows if r.get("status") == "ok" and r["scale"] == s]
        if len(ok) < 2:
            continue
        lo, hi = ok[0], ok[-1]
        growth = hi["cond_median"] / lo["cond_median"] if lo["cond_median"] > 0 else float("inf")
        print(f"scale {s:>5g}: cond median {lo['cond_median']:.3e} (h12={lo['h12']}) -> "
              f"{hi['cond_median']:.3e} (h12={hi['h12']})  = {growth:.1f}x")
    print("\nIf the growth is comparable at every scale, conditioning is intrinsic to h12.")
    print("If it only appears at one scale, the earlier wall numbers may be a patch artefact.")
    print("===DONE===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
