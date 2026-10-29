"""B2 — the truncation ladder: does cond(M) move when the instanton series is carried further?

FALSIFIER, stated before the run (docs/plan-exact-terms.md §4 B2): if cond(M) moves by more than
10% between maximum_degree 1, 2 and 3, then the h12 >= 5 wall is SERIES TRUNCATION and the degree is
the fix. If it moves by less, truncation is excluded at these moduli and the wall is geometry.

Method: at ONE fixed generic moduli point per h12 (the point must not move, or the comparison is of
two different measurements), build the LCS tree at maximum_degree = 1, 2, 3 and take the condition
number of the ISD matrix. Degree 0 is included as the sampler's own setting.

Run on pacland-rog (only node with jax/jaxvacua/cytools):
    /home/rob/cytools-venv/bin/python scripts/node_b2_truncation.py 2,5,10,25 1
"""
import json
import signal
import sys
import time

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np  # noqa: E402
import jaxvacua as jvc  # noqa: E402

DEGREES = (0, 1, 2, 3)
MOVES_THRESHOLD = 0.10


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def cond_at(h12: int, degree: int, z: np.ndarray, timeout: int = 600):
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(timeout)
    t0 = time.time()
    try:
        model = jvc.FluxVacuaFinder(h12=h12, model_ID=1, model_type="KS", maximum_degree=degree)
        M = np.asarray(model.ISD_matrix(z, np.conjugate(z)))
        Mk = M[0]
        evals, evecs = np.linalg.eigh(Mk)
        idx = np.argsort(np.abs(evals))
        cond = float(abs(evals[idx[-1]]) / max(abs(evals[idx[0]]), 1e-300))
        v = np.abs(evecs[:, idx[0]]) ** 2
        w = v / v.sum()
        h = h12
        bands = {"dilaton": float(w[0] + w[2 * h + 1]),
                 "interior": float(w[1:h].sum() + w[h + 1:2 * h].sum()),
                 "boundary": float(w[h] + w[2 * h])}
        return {"ok": True, "cond": cond, "dim": int(Mk.shape[0]), "bands": bands,
                "seconds": round(time.time() - t0, 1)}
    except Timeout:
        return {"ok": False, "error": f"timeout after {timeout}s", "seconds": round(time.time() - t0, 1)}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "seconds": round(time.time() - t0, 1)}
    finally:
        signal.alarm(0)


def main(argv):
    h12s = [int(x) for x in (argv[1].split(",") if len(argv) > 1 else ["2", "5", "10", "25"])]
    seed = int(argv[2]) if len(argv) > 2 else 1
    out = {"falsifier": "cond(M) moving >10% between maximum_degree 1/2/3 means truncation",
           "threshold": MOVES_THRESHOLD, "cells": [], "verdicts": []}
    print("=" * 96)
    print("B2 · truncation ladder — cond(M) at a FIXED generic moduli point, per h12")
    print(f"falsifier (stated before the run): a move >{MOVES_THRESHOLD:.0%} means truncation, not geometry")
    print("=" * 96)
    for h12 in h12s:
        rng = np.random.default_rng(seed + h12)          # the SAME z for every degree at this h12
        z = (rng.uniform(-1.0, 1.0, (1, h12)) + 1j * rng.uniform(0.5, 3.0, (1, h12)))
        row = {"h12": h12, "cells": {}}
        for d in DEGREES:
            r = cond_at(h12, d, z)
            row["cells"][str(d)] = r
            out["cells"].append({"h12": h12, "degree": d, **r})
            if r["ok"]:
                print(f"  h12={h12:>2} degree={d}  cond={r['cond']:.6e}  dim={r['dim']}  "
                      f"boundary={r['bands']['boundary']:.3f}  ({r['seconds']}s)")
            else:
                print(f"  h12={h12:>2} degree={d}  FAIL {r['error']}  ({r['seconds']}s)")
        ok = {d: row["cells"][str(d)] for d in (1, 2, 3) if row["cells"][str(d)]["ok"]}
        if len(ok) >= 2:
            vals = [ok[d]["cond"] for d in sorted(ok)]
            spread = (max(vals) - min(vals)) / min(vals)
            verdict = ("TRUNCATION" if spread > MOVES_THRESHOLD else "geometry")
            row.update({"spread": spread, "verdict": verdict, "degrees_compared": sorted(ok)})
            out["verdicts"].append({"h12": h12, "spread": spread, "verdict": verdict,
                                    "degrees_compared": sorted(ok)})
            print(f"  -> h12={h12}: cond moves {spread:.2%} across degrees {sorted(ok)} => {verdict}\n")
        else:
            row.update({"spread": None, "verdict": "not measurable"})
            out["verdicts"].append({"h12": h12, "spread": None, "verdict": "not measurable",
                                    "degrees_compared": sorted(ok)})
            print(f"  -> h12={h12}: fewer than two degrees measured => not measurable\n")
        out.setdefault("rows", []).append(row)
    print(json.dumps({k: out[k] for k in ("falsifier", "threshold", "verdicts")}, indent=2))
    with open("b2_result.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote b2_result.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
