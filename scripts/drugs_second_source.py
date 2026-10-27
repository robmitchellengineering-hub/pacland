#!/usr/bin/env python3
"""Class 5 for drug discovery: the same potency, from two independent databases.

    python3 scripts/drugs_second_source.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.drugs import second_source as ss  # noqa: E402


def main() -> int:
    report = ss.audit()
    r = ss.cross_source()
    data = ss.load()
    print(f"PACLAND · drug discovery — class 5 on {data['compound']} "
          f"({data['chembl_id']} / CID {data['pubchem_cid']})\n")
    for name in ("chembl", "pubchem"):
        p = r[name]
        print(f"{name:8} n={p['n']:>5}  median {p['median_nm']:>9.0f} nM   "
              f"10-90pct {p['p10_nm']:.1f} - {p['p90_nm']:.0f} nM   "
              f"fold {p['fold_range_10_90']:.0f}x")
    print(f"\ncross-source agreement on the median: {r['median_ratio']:.2f}x")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:24} {check['detail']}")
    print(f"\n{r['verdict']}.")
    print("so the CENTRE is reproducible and a SINGLE value is not — which is what a")
    print("certificate has to say out loud.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
