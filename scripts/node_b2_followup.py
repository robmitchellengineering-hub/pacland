"""B2 follow-up — the falsifier fired at h12=10 and not at h12=25, so settle two things before believing it.

Run 1 measured ONE generic moduli point per h12 and found:
    h12= 2   move 0.00%   geometry
    h12= 5   move 0.00%   geometry
    h12=10   move 27.75%  TRUNCATION   <-- falsifier fired
    h12=25   move  0.47%  geometry

Two reasons not to believe that yet, and this script addresses both:

1 **the point may be the finding.** One point per h12 cannot separate a degree effect from where in
   moduli space the point landed. This runs 5 points per h12 and reports the spread per point and the
   worst one.
2 **jaxvacua warned that mirror worldsheet instanton corrections were DISABLED while GV charges were
   provided.** If the instanton corrections are off, the degree ladder is not measuring the series it
   claims to. This prints the constructor signature and the warning's own source, and retries with any
   instanton-related flag it can find.

FALSIFIER, unchanged and stated before the run: a move >10% between degrees 1/2/3 means truncation.
"""
import inspect
import json
import signal
import sys
import time
import warnings

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np  # noqa: E402
import jaxvacua as jvc  # noqa: E402

DEGREES = (1, 2, 3)
THRESHOLD = 0.10
POINTS = 5


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def introspect():
    out = {"signature": str(inspect.signature(jvc.FluxVacuaFinder.__init__))}
    try:
        import jaxvacua.periods as per
        src = inspect.getsource(per)
        lines = src.splitlines()
        hit = [i for i, l in enumerate(lines) if "Mirror worldsheet instanton corrections are disabled" in l]
        if hit:
            i = hit[0]
            out["warning_context"] = "\n".join(lines[max(0, i - 14):i + 3])
    except Exception as e:  # noqa: BLE001
        out["source_error"] = f"{type(e).__name__}: {e}"
    try:
        params = list(inspect.signature(jvc.FluxVacuaFinder.__init__).parameters)
        out["instanton_like_params"] = [p for p in params if "instant" in p.lower() or "mirror" in p.lower()]
    except Exception:  # noqa: BLE001
        pass
    return out


def cond_at(h12, degree, z, timeout=900, extra=None):
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(timeout)
    t0 = time.time()
    try:
        kwargs = {"h12": h12, "model_ID": 1, "model_type": "KS", "maximum_degree": degree}
        if extra:
            kwargs.update(extra)
        model = jvc.FluxVacuaFinder(**kwargs)
        M = np.asarray(model.ISD_matrix(z, np.conjugate(z)))
        evals = np.linalg.eigvalsh(M[0])
        idx = np.argsort(np.abs(evals))
        cond = float(abs(evals[idx[-1]]) / max(abs(evals[idx[0]]), 1e-300))
        return {"ok": True, "cond": cond, "seconds": round(time.time() - t0, 1)}
    except Timeout:
        return {"ok": False, "error": f"timeout {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}
    finally:
        signal.alarm(0)


def ladder(h12, seeds, extra=None, label=""):
    rows = []
    for k in range(seeds):
        rng = np.random.default_rng(1000 + 37 * k + h12)
        z = (rng.uniform(-1.0, 1.0, (1, h12)) + 1j * rng.uniform(0.5, 3.0, (1, h12)))
        vals = {}
        for d in DEGREES:
            r = cond_at(h12, d, z, extra=extra)
            vals[d] = r
        if all(v["ok"] for v in vals.values()):
            cs = [vals[d]["cond"] for d in DEGREES]
            spread = (max(cs) - min(cs)) / min(cs)
        else:
            spread = None
        rows.append({"point": k, "spread": spread,
                     "conds": {d: vals[d].get("cond") for d in DEGREES},
                     "errors": {d: vals[d].get("error") for d in DEGREES if not vals[d]["ok"]}})
        print(f"   h12={h12:>2}{label} point {k}: " +
              " ".join(f"d{d}={vals[d]['cond']:.4e}" if vals[d]["ok"] else f"d{d}=FAIL"
                       for d in DEGREES) +
              (f"  move {spread:.2%}" if spread is not None else ""))
    good = [r["spread"] for r in rows if r["spread"] is not None]
    return {"h12": h12, "label": label, "points": rows,
            "max_spread": max(good) if good else None,
            "median_spread": float(np.median(good)) if good else None,
            "verdict": ("TRUNCATION" if good and max(good) > THRESHOLD else
                        ("geometry" if good else "not measurable"))}


def main(argv):
    h12s = [int(x) for x in (argv[1].split(",") if len(argv) > 1 else ["2", "5", "10", "25"])]
    seeds = int(argv[2]) if len(argv) > 2 else POINTS
    out = {"falsifier": f"a move >{THRESHOLD:.0%} between degrees 1/2/3 means truncation",
           "threshold": THRESHOLD, "introspection": introspect(), "runs": []}
    print("=" * 100)
    print("B2 follow-up · 5 points per h12, and the instanton warning investigated")
    print(f"falsifier, stated before the run: a move >{THRESHOLD:.0%} means truncation, not geometry")
    print("=" * 100)
    print("\nintrospection:")
    print(json.dumps(out["introspection"], indent=2)[:2000])

    extra = {}
    for key in ("mirror_instanton", "use_mirror_instanton", "include_instantons"):
        try:
            jvc.FluxVacuaFinder(h12=2, model_ID=1, model_type="KS", maximum_degree=1, **{key: True})
            extra[key] = True
            print(f"\naccepted flag: {key}=True")
            break
        except Exception:  # noqa: BLE001
            continue
    if not extra:
        print("\nno instanton flag accepted by the constructor — the ladder runs as before")

    for h12 in h12s:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            res = ladder(h12, seeds, extra=extra)
            msgs = sorted({str(w.message)[:160] for w in caught})
        res["warnings"] = msgs
        out["runs"].append(res)
        print(f"  -> h12={h12}: max move {res['max_spread']:.2%}, median {res['median_spread']:.2%} "
              f"=> {res['verdict']}\n" if res["max_spread"] is not None
              else f"  -> h12={h12}: not measurable\n")

    print(json.dumps({r["h12"]: r["verdict"] for r in out["runs"]}, indent=2))
    with open("b2_followup.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote b2_followup.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
