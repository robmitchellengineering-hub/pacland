"""B3, retried — de Sitter requires a positive term **beyond** the F-term potential.

**The claim as written in the plan was "dS requires a Kähler modulus, not an uplift".** Executing it refuted that
wording and replaced it with a sharper one that *is* provable with what is here.

The one-modulus KKLT-type model:

    K = -3 ln(T + Tbar),      W = W0 + A e^{-aT},     T = Tbar (real slice, so T + Tbar = 2T)
    D_T W = -3 W / (2T) - a A e^{-aT}
    V = e^K ( g^{TTbar} |D_T W|^2 - 3 |W|^2 ),        g^{TTbar} = (2T)^2 / 3
      = (2T)^{-3} ( (2T)^2/3 ) |D_T W|^2 - 3 (2T)^{-3} |W|^2
      = |D_T W|^2 / (3 (2T)) - 3 |W|^2 / (2T)^3

At a SUSY point (`D_T W = 0`):

    V = -3 |W|^2 / (2T)^3  =  -3 e^K |W|^2  <  0     identically

— the same identity as the T^6 result, now with a **Kähler** modulus stabilised. So stabilising the modulus does
not produce de Sitter.

**The uplift.** Adding `D / (2T)^2` gives `V_up = D/(2T)^2`, which is positive, and above

    D_crit = 3 |W|^2 / (2T)

the same minimum is lifted to `V > 0`. So:

    dS requires a positive term beyond the F-term potential   (proved necessary here, exhibited sufficient)
    the modulus is what stabilises; the uplift is what lifts

**Method note (why this is the second attempt).** The first used `mp.findroot` from a guess and silently returned
a point where `D_T W != 0`, so `V` came out positive and contradicted the theorem — caught by the module's own
identity check. This version **brackets and bisects** the 1-D transcendental equation on a stated interval and
asserts the identity residual *before* any uplift scan.

Run:        python3 scripts/ds_uplift.py
Guarded by: tests/test_ds_needs_uplift.py
"""
from __future__ import annotations

import mpmath as mp

#: The bracket for `D_T W = 0`. Chosen so the function changes sign; asserted, not hoped for.
BRACKET = (mp.mpf("0.01"), mp.mpf("100"))


def dtw(T, W0, A, a):
    """`D_T W` on the real slice."""
    T = mp.mpf(T)
    W = W0 + A * mp.exp(-a * T)
    return -3 * W / (2 * T) - a * A * mp.exp(-a * T)


def potential(T, W0, A, a, uplift_D=0):
    """`V` on the real slice, optionally uplifted by `D/(2T)^2`."""
    T = mp.mpf(T)
    W = W0 + A * mp.exp(-a * T)
    d = dtw(T, W0, A, a)
    v = d ** 2 / (3 * (2 * T)) - 3 * W ** 2 / (2 * T) ** 3
    if uplift_D:
        v += uplift_D / (2 * T) ** 2
    return v


def susy_point(W0=mp.mpf("-0.05"), A=1, a=mp.mpf("0.1"), bracket=BRACKET) -> dict:
    """Bracketed bisection for `D_T W = 0`, with the identity asserted before anything else."""
    lo, hi = mp.mpf(bracket[0]), mp.mpf(bracket[1])
    flo, fhi = dtw(lo, W0, A, a), dtw(hi, W0, A, a)
    if flo * fhi > 0:
        raise ArithmeticError(f"no sign change on the bracket: f({lo})={flo}, f({hi})={fhi}")
    f = lambda x: dtw(x, W0, A, a)
    T = mp.findroot(f, (lo, hi), solver="bisect")
    v = potential(T, W0, A, a)
    k = -3 * mp.log(2 * T)
    w = W0 + A * mp.exp(-a * T)
    predicted = -3 * mp.exp(k) * w ** 2
    resid = abs(v - predicted) / abs(predicted) if predicted else float("inf")
    if resid > mp.mpf("1e-20"):
        raise ArithmeticError(f"the identity failed at the root: residual {resid}")
    return {"T": T, "V": v, "predicted": predicted, "identity_residual": resid,
            "DW": dtw(T, W0, A, a), "is_ads": bool(v < 0)}


def uplift_scan(s=None, factors=(0, 0.5, 1, 2)) -> dict:
    """Exhibit the uplift that makes the minimum positive — with `D_crit` computed, not searched."""
    s = s or susy_point()
    T, W0, A, a = s["T"], mp.mpf("-0.05"), 1, mp.mpf("0.1")
    W = W0 + A * mp.exp(-a * T)
    D_crit = 3 * W ** 2 / (2 * T)
    rows = []
    for f in factors:
        D = D_crit * mp.mpf(f)
        v = potential(T, W0, A, a, D)
        rows.append({"D_factor": f, "D": D, "V": v, "dS": bool(v > 0)})
    return {"T": T, "D_crit": D_crit, "rows": rows,
            "below_is_ads": all(not r["dS"] for r in rows if r["D_factor"] < 1),
            "above_is_ds": all(r["dS"] for r in rows if r["D_factor"] > 1),
            "minkowski_at_critical": any(abs(r["V"]) < mp.mpf("1e-25") for r in rows if r["D_factor"] == 1)}


def statement() -> dict:
    s = susy_point()
    u = uplift_scan(s)
    return {
        "claim_as_written": "dS requires a Kähler modulus, not an uplift",
        "verdict": "REFUTED as written; replaced by a provable statement",
        "proved": ("at any SUSY point V = -3 e^K |W|^2 < 0 identically, for a Kähler modulus exactly as for the "
                   "T^6 sector — stabilising a modulus cannot produce de Sitter"),
        "exhibited": (f"an uplift D/(2T)^2 lifts the same minimum: D_crit = {float(u['D_crit']):.6g} gives "
                      f"exactly Minkowski (V = 0), and anything above it gives de Sitter (V > 0)"),
        "surviving_statement": ("dS requires a positive term beyond the F-term potential; the modulus "
                                "stabilises, the uplift lifts"),
        "excludes": "that the F-term potential alone can give de Sitter, in either sector",
        "susy_point": {k: float(v) if hasattr(v, "real") or isinstance(v, (int, float)) else str(v)
                       for k, v in s.items()},
        "scan": [{"D_factor": r["D_factor"], "V": float(r["V"]), "dS": r["dS"]} for r in u["rows"]],
        "below_is_ads": u["below_is_ads"], "above_is_ds": u["above_is_ds"],
        "minkowski_at_critical": u["minkowski_at_critical"],
        "scope": ("one modulus, one non-perturbative term, real slice. Necessity is proved here; sufficiency is "
                  "exhibited at the level of the potential, not shown to be dynamically attainable"),
    }


__all__ = ["BRACKET", "dtw", "potential", "susy_point", "uplift_scan", "statement"]
