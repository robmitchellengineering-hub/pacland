#!/usr/bin/env python3
"""Cross-validate the widened drift: does the raw recomputation reproduce Irving?

Recomputes the piControl net-TOA drift for the Irving models that are in the
pangeo-cmip6 catalog (r1i1p1f1), and compares to Irving et al. 2021. If the raw
method reproduces Irving's values, the widened (raw) drift is a valid second
source, not a biased estimate.

Requires xarray/zarr (the widening environment). Run on the Mac.

    python3 scripts/climate_drift_crosscheck.py
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "scripts")

from climate_drift_widen import catalog_paths, drift_of  # noqa: E402

SEC = 3.15576e7
AREA = 5.101e14


def main() -> None:
    d = json.load(open("data/climate/cmip6_drift.json"))
    irving = {m["model"]: m["netTOA_J_per_yr"] / (SEC * AREA) for m in d["models"]}
    paths = catalog_paths()
    print(f"catalog: {len(paths)} (model,var) rows", file=sys.stderr)
    out = []
    for model, iv in irving.items():
        res, err = drift_of(model, paths)
        if err:
            out.append({"model": model, "status": "skipped", "reason": err})
            print(f"{model:18s} SKIP {err}", flush=True)
            continue
        raw = res["mean_Wm2"]
        delta = raw - iv
        out.append({"model": model, "raw_Wm2": round(raw, 3), "irving_Wm2": round(iv, 3),
                    "delta_Wm2": round(delta, 3),
                    "match": abs(delta) < 0.25})
        print(f"{model:18s} raw {raw:+.3f} vs Irving {iv:+.3f}  "
              f"{'MATCH' if abs(delta) < 0.25 else 'MISMATCH'} (delta {delta:+.3f})", flush=True)
    n = len([o for o in out if o.get("match")])
    print(json.dumps({"n_compared": n, "n_total": len(irving),
                      "max_delta_Wm2": max((abs(o.get('delta_Wm2', 0)) for o in out), default=0),
                      "models": out}, indent=2))


if __name__ == "__main__":
    main()
