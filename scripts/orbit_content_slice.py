"""The orbit-content slice — does the integer content d = gcd(F,H) carry physics?

**Why this measurement.** Mitchell's Completeness Theorem says the tadpole `N = FᵀJH` is
the unique *exact* duality invariant, and that over ℤ there are **finitely many orbits
per tadpole — one per divisor `d | √N` of the content** `d = gcd(F, H)` with `d² | N`.
So the tadpole cannot distinguish those orbits. The dictionary question is whether the
low-energy physics can: if two vacua with the *same* N and *different* d behave
differently, the content is physical content; if they do not, it is a lattice label.

**The smallest slice.** A second class needs `d ≥ 2` and `d² | N`, so the smallest
tadpole carrying two classes is **N = 4**, with `d ∈ {1, 2}`. This script measures the
committed corpus at that slice and reports what it can and cannot conclude.

Two honesty notes that govern the output:

1. **`d² | N` is arithmetic, not evidence.** `N = FᵀJH` is bilinear, so `d | F, d | H`
   forces `d² | N`. A corpus where it fails has corrupt fields; a corpus where it holds
   proves only that `flux` and `Nflux` agree. Do not report it as confirming the theorem.
2. **A missing comparison is not a negative result.** If the corpus contains one point
   in the `d = 2` class, the slice cannot be tested at all — and that is reported as
   `verdict: insufficient`, never as "the content carries no physics".

Usage (on a mesh node, from the repo root):
    python3 scripts/orbit_content_slice.py [--json data/orbit_content_slice.json]
"""
import argparse
import glob
import json
import statistics as st
from functools import reduce
from math import gcd


def content(flux):
    """d = gcd of every integer flux component (F and H together)."""
    return reduce(gcd, [int(round(abs(x))) for x in flux], 0)


def load_rows(pattern="data/h12_*_stats.json"):
    rows = []
    for fn in sorted(glob.glob(pattern)):
        doc = json.load(open(fn))
        for r in doc.get("vacua", []):
            r["_file"] = fn.split("/")[-1]
            r["_h12"] = doc.get("h12")
            r["_model"] = doc.get("model_ID")
            rows.append(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    rows = load_rows()
    if not rows:
        print("INSUFFICIENT no data/h12_*_stats.json found — run from the repo root")
        return 1

    # --- the label holds on every row (data integrity, NOT evidence: see docstring) ---
    labelled = 0
    d_ok = 0
    groups = {}
    for r in rows:
        nf, fl = r.get("Nflux"), r.get("flux")
        if nf is None or not fl:
            continue
        nf = int(round(nf))
        d = content(fl)
        if d < 1:
            continue
        labelled += 1
        if nf % (d * d) == 0:
            d_ok += 1
        groups.setdefault((r["_file"], r["_h12"], r["_model"], nf), set()).add(d)

    multi = {k: sorted(v) for k, v in groups.items() if len(v) > 1}

    print("=" * 78)
    print("orbit-content slice — does d = gcd(F,H) carry physics?")
    print("=" * 78)
    print(f"rows with flux+Nflux : {labelled}")
    print(f"d^2 | N              : {d_ok}/{labelled}  "
          f"(ARITHMETIC — bilinearity forces it; this is a field-consistency check)")
    print(f"distinct (file,h12,model,N) groups : {len(groups)}")
    print(f"groups with more than one content class : {len(multi)}")

    # --- how much data each candidate slice actually has -----------------------------
    print("\n-- candidate slices (fixed tadpole, more than one content class) --")
    if not multi:
        print("none — no tadpole in the corpus carries two content classes")
    for (fn, h12, model, nf), ds in sorted(multi.items(), key=lambda kv: kv[0][3])[:10]:
        per = {}
        for r in rows:
            if (r["_file"], r["_h12"], r["_model"],
                    int(round(r["Nflux"]))) != (fn, h12, model, nf):
                continue
            d = content(r["flux"])
            per.setdefault(d, []).append(r)
        parts = []
        for d, rs in sorted(per.items()):
            sus = sum(1 for r in rs if r.get("is_susy"))
            gs = [1.0 / abs(r["tau"][1]) for r in rs if abs(r["tau"][1]) > 0]
            med = st.median(gs) if gs else float("nan")
            parts.append(f"d={d}: n={len(rs)} susy={sus} g_s_med={med:.4g}")
        print(f"  {fn} h12={h12} m{model} N={nf}  ->  " + " | ".join(parts))

    # --- verdict: can this corpus answer the question at all? ------------------------
    thin = {d: n for (fn, h12, model, nf), ds in multi.items()
            for d, n in [(d, sum(1 for r in rows
                                if (r["_file"], r["_h12"], r["_model"],
                                    int(round(r["Nflux"]))) == (fn, h12, model, nf)
                                and content(r["flux"]) == d)) for d in ds] if d >= 2}
    verdict = "insufficient" if (not multi or any(n < 5 for n in thin.values())) else "testable"
    print(f"\nverdict: {verdict}")
    if verdict == "insufficient":
        print("  A d>=2 class is populated by fewer than 5 points, so no comparison is")
        print("  possible. Random flux sampling essentially never draws an all-even flux")
        print("  (d>=2 requires d to divide EVERY component), so this class must be")
        print("  CONSTRUCTED (scale a primitive pair by d) rather than drawn. Reporting")
        print("  this as 'the content carries no physics' would be a false negative.")

    if args.json:
        json.dump({"rows": labelled, "d2_divides_N": d_ok,
                   "groups": len(groups), "multi_class_groups": len(multi),
                   "verdict": verdict}, open(args.json, "w"), indent=2)
        print(f"\nwrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
