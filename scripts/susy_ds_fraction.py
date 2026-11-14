#!/usr/bin/env python3
"""The corrected SUSY fraction, computed on the data_sampler corpus (0 runaway).

Replaces the retracted "27.9% -> 19.7% -> 1.1%" (a sampler artefact — the old corpus was 91%
runaway at b3=10). Loads data/h12_*_ds.json, classifies each vacuum's moduli against the
sampler's declared domain (1.0, 5.0), and reports the in-domain SUSY fraction per b3 with a
Wilson interval.

Run: python3 scripts/susy_ds_fraction.py
"""
import glob
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scale(row):
    vals = [abs(complex(x[0], x[1])) for x in row["moduli"]]
    vals.append(abs(complex(row["tau"][0], row["tau"][1])))
    return max(vals)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5
    return ((c - r) / d, (c + r) / d)


def main():
    print("Corrected SUSY fraction — data_sampler corpus (0 runaway)")
    print(f"{'b3':>3} {'h12':>4} {'SUSY':>6} {'in-domain':>10} {'fraction':>10} {'95% CI':>18}")
    rows_by_b3 = {}
    for f in sorted(glob.glob(str(ROOT / "data" / "h12_*_ds.json"))):
        d = json.load(open(f))
        h12 = d["h12"]
        b3 = 2 * h12 + 2
        rows = d["vacua"]
        indom = sum(1 for r in rows if 1.0 <= scale(r) <= 5.0)
        rows_by_b3[b3] = (h12, len(rows), indom)
    for b3 in sorted(rows_by_b3):
        h12, n, indom = rows_by_b3[b3]
        lo, hi = wilson(indom, n)
        print(f"{b3:>3} {h12:>4} {n:>6} {indom:>10} {indom / n:>9.1%}  [{lo:.1%}, {hi:.1%}]")
    fracs = [rows_by_b3[b][2] / rows_by_b3[b][1] for b in sorted(rows_by_b3)]
    print(f"\nflatness: fractions span {min(fracs):.1%}..{max(fracs):.1%}")
    print("(the retracted 'collapse' was 27.9% -> 1.1% — a sampler artefact)")


if __name__ == "__main__":
    main()
