#!/usr/bin/env python3
"""Run the energy-budget guard on real cited data and print the result as JSON.

This is the mesh-runnable entry point: it reads ``data/climate/energy_budget.json``,
runs ``guard_energy_budget`` twice (0-2000 m ocean only, then the full budget),
and prints one JSON result for the record.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.climate.energy_budget import closure  # noqa: E402


def main() -> int:
    print(json.dumps(closure(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
