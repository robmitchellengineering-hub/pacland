#!/usr/bin/env python3
"""Minima-only reporting: the numbers that are about the landscape, with the runaway share beside them.

"27.9%" and "43.3% at a 37.9% runaway share" are different claims, and only the second is about the theory.

    python3 scripts/minima_report.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import counterexample as C   # noqa: E402
from pacland.exactness import ingest_gate as G      # noqa: E402


def main() -> int:
    rows = [c["row"] for c in C.load_corpus()]
    per = G.report(rows)

    print("Minima-only reporting — gated at the sampler's own bounds\n")
    print(f"  {'b3':>3} {'rows':>6} {'in-domain':>10} {'runaway':>8} {'SUSY all':>9} {'SUSY gated':>11} "
          f"{'minima all':>11} {'minima gated':>13}")
    for b3, d in sorted(per.items()):
        print(f"  {b3:>3} {d['rows']:>6} {d['in_domain']:>10} {d['runaway_share']:>7.1%} "
              f"{d['susy_rate_all']:>8.1%} {d['susy_rate_in_domain']:>10.1%} "
              f"{d['minima_rate_all']:>10.1%} {d['minima_rate_in_domain']:>12.1%}")

    print(f"\n  with 95% Wilson intervals on the gated minima rate:")
    for b3, d in sorted(per.items()):
        lo, hi = d["minima_ci"]
        print(f"    b3={b3}: {d['minima_rate_in_domain']:.3f}  [{lo:.3f}, {hi:.3f}]  n={d['in_domain']}"
              + ("   <-- under 200 rows" if d["in_domain"] < 200 else ""))
    iv = G.interval_verdict(per)
    print(f"\n  {iv['statement']}")

    tot = sum(d["rows"] for d in per.values())
    run = sum(d["runaway"] for d in per.values())
    print(f"\n  corpus: {tot} rows, {run} outside the declared bounds ({run/tot:.1%})")
    print("  a figure quoted without the gated column is a figure about the corpus, not the theory.")

    # does the N/b3 collapse survive the gate?
    gated = [r for r in rows if G.classify(r) == "in_domain"
             and r.get("Nflux") is not None and float(r.get("Nflux")) > 0]
    print(f"\n  N/b3 collapse over IN-DOMAIN rows only ({len(gated)} rows):")
    for b3 in sorted({len(r["flux"]) // 2 for r in gated}):
        sel = sorted((float(r["Nflux"]), bool(r.get("is_susy"))) for r in gated if len(r["flux"]) // 2 == b3)
        if len(sel) < 8:
            print(f"    b3={b3}: too few rows ({len(sel)}) to bin")
            continue
        k = len(sel) // 4
        frs = []
        for q in range(4):
            chunk = sel[q * k:(q + 1) * k] if q < 3 else sel[3 * k:]
            frs.append(sum(1 for _, s in chunk if s) / len(chunk))
        climb = frs[-1] > frs[0]
        print(f"    b3={b3}: quartiles {['%.3f' % f for f in frs]}  climbs with N = {climb}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
