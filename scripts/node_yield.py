"""Does the sampler actually FIND vacua at a real budget?

B2-applied (#214) ran a deliberately tiny budget (n_target=5, max_batches=40) and found 0 SUSY at h12=5 and
10. That answered "does degree 2 fix the yield" with "not at that budget" — it did not answer "does the
sampler find vacua at all".

FALSIFIER, stated before the run: if a budget 50x larger still returns zero critical points at h12=5, the
sampler's proposal step is the limit, not the budget and not the truncation. If it finds points but none SUSY,
the solve is the limit. If it finds SUSY vacua, B2 applies after all and the wall was truncation + budget.

Stays at h12 <= 5 for the first pass: h12=25 OOM'd at 143 GB elsewhere and the rog has 31 GB.

Run on pacland-rog:
    /home/rob/cytools-venv/bin/python scripts/node_yield.py [h12_csv] [degree_csv] [n_target] [max_batches]
"""
import json
import signal
import sys
import time

import jax
jax.config.update("jax_enable_x64", True)

import jaxvacua as jvc  # noqa: E402


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def run(h12: int, degree: int, n_target: int, max_batches: int, limit_s: int = 2700):
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(limit_s)
    t0 = time.time()
    try:
        model = jvc.FluxVacuaFinder(h12=h12, model_ID=1, model_type="KS", maximum_degree=degree,
                                    mirror_instanton=True)
        vacua = list(model.sample_critical_points(Q=None, n_target=n_target, n_batch=25,
                                                  max_batches=max_batches, isd_mode="ISD-",
                                                  solver="scipy", verbose=False))
        susy = sum(1 for r in vacua if bool(getattr(r, "get", lambda *_: False)("is_susy")))
        return {"ok": True, "critical_points": len(vacua), "susy": susy,
                "seconds": round(time.time() - t0, 1), "hit_target": len(vacua) >= n_target}
    except Timeout:
        return {"ok": False, "error": f"timeout after {limit_s}s", "seconds": round(time.time() - t0, 1)}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "seconds": round(time.time() - t0, 1)}
    finally:
        signal.alarm(0)


def main(argv):
    h12s = [int(x) for x in (argv[1].split(",") if len(argv) > 1 else ["5"])]
    degrees = [int(x) for x in (argv[2].split(",") if len(argv) > 2 else ["0"])]
    n_target = int(argv[3]) if len(argv) > 3 else 20
    max_batches = int(argv[4]) if len(argv) > 4 else 2000
    out = {"falsifier": "zero critical points at 50x the budget means the proposal step is the limit",
           "n_target": n_target, "max_batches": max_batches, "budget": n_target * max_batches, "runs": []}
    print("=" * 90)
    print(f"YIELD · budget {n_target} x {max_batches} = {n_target * max_batches} candidate batches")
    print("falsifier: zero critical points at this budget means the proposal step is the limit")
    print("=" * 90)
    for h12 in h12s:
        for d in degrees:
            r = run(h12, d, n_target, max_batches)
            r.update({"h12": h12, "degree": d})
            out["runs"].append(r)
            print(f"  h12={h12:>2} deg={d}: " + (f"{r['critical_points']} points, {r['susy']} SUSY, "
                  f"{r['seconds']}s" if r["ok"] else f"FAIL {r['error']}"), flush=True)
            with open("yield_result.json", "w") as f:
                json.dump(out, f, indent=2)
    print("\nwrote yield_result.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
