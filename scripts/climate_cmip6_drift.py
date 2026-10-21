#!/usr/bin/env python3
"""Run the CMIP6 conservation-drift guard on real data and print the result as JSON.

Mesh-runnable entry point: reads ``data/climate/cmip6_drift.json`` (Irving et al.
2021), runs ``guard_energy_budget`` per model, and prints one JSON result.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.climate.cmip6_drift import summary, verdict_table  # noqa: E402


def main() -> int:
    print(json.dumps({"summary": summary(), "per_model": verdict_table()}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
