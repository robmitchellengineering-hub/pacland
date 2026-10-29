"""B2 APPLIED — does degree 2 actually find vacua that degree 0/1 could not?

#208 measured that cond(M) at h12=25 moves up to 88% between degree 1 and degree 2 and that degree 2 is
converged (d2 = d3 at every point). That is a statement about the series. This asks the question the
series is FOR: does the fix change what the sampler finds?

FALSIFIER (stated before the run): if degree 0 and degree 2 find the same number of SUSY vacua from the
same budget, the truncation was not what limited the sampler and #208's fix buys nothing at these h12.

Memory note: this stays at h12 <= 10. The h12=25 sampler OOM'd at 143 GB elsewhere and the rog has 31.

Run on pacland-rog:
    /home/rob/cytools-venv/bin/python scripts/node_b2_applied.py
"""
import json
import sys
import time

import jax
jax.config.update("jax_enable_x64", True)

import jaxvacua as jvc  # noqa: E402


def run(h12: int, degree: int, n_target: int = 5, max_batches: int = 40):
    t0 = time.time()
    try:
        model = jvc.FluxVacuaFinder(h12=h12, model_ID=1, model_type="KS", maximum_degree=degree,
                                    mirror_instanton=True)
        vacua = model.sample_critical_points(Q=None, n_target=n_target, n_batch=10,
                                            max_batches=max_batches, isd_mode="ISD-",
                                            solver="scipy", verbose=False)
        rows = list(vacua)
        n_susy = sum(1 for r in rows if bool(getattr(r, "get", lambda *_: False)("is_susy")))
        return {"ok": True, "n": len(rows), "n_susy": n_susy,
                "seconds": round(time.time() - t0, 1)}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "seconds": round(time.time() - t0, 1)}


def main():
    out = {"falsifier": "degree 0 and degree 2 finding the same SUSY count means truncation was not "
                        "what limited the sampler", "runs": []}
    print("=" * 88)
    print("B2 APPLIED · does degree 2 find vacua that degree 0/1 could not?")
    print("falsifier: the same SUSY count at degree 0 and 2 means the fix buys nothing")
    print("=" * 88)
    for h12 in (5, 10):
        for degree in (0, 2):
            r = run(h12, degree)
            r.update({"h12": h12, "degree": degree})
            out["runs"].append(r)
            if r["ok"]:
                print(f"  h12={h12:>2} degree={degree}: {r['n']} critical points, "
                      f"{r['n_susy']} SUSY  ({r['seconds']}s)")
            else:
                print(f"  h12={h12:>2} degree={degree}: FAIL {r['error']}  ({r['seconds']}s)")
    print("\n" + json.dumps(out["runs"], indent=2))
    with open("b2_applied.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote b2_applied.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
