#!/usr/bin/env python3
"""The energy floor of verification, and the crossover against re-execution.

    python3 scripts/energy_verify_joules.py [--data PATH]

REGISTERED, NOT RUN. Claim (docs/energy-conjectures.md): verification has an energy floor of 1-3 uJ per
check — process overhead, not the hash — and a crossover at 10^4-10^6 operations per item: above it,
checking a witness beats re-executing the work; below it, it loses.

This is a measurement, not arithmetic. It needs one machine, a power meter with millisecond resolution,
and a batched SHA-256d sweep (10^6 hashes, k = 8...28) to separate per-check overhead from per-byte cost.
Until that runs, this script refuses and says exactly what it would need.

Falsifier: a measured floor outside 0.3-10 uJ per check, or a crossover outside 10^3-10^7 ops per item.
"""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data" / "compute" / "verify_energy.json"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Verification energy floor (registered).")
    ap.add_argument("--data", default=str(DEFAULT))
    args = ap.parse_args(argv[1:])
    path = pathlib.Path(args.data)

    if not path.is_file():
        print("REFUSED: no measurement exists, so no floor can be stated.")
        print(f"  looked for: {path}")
        print()
        print("The measurement, as registered:")
        print("  sweep     : 10^6 batched SHA-256d, k = 8...28, 5 repeats, 1 ms power sampling")
        print("  extract   : E(k) = a + b*k  ->  floor a (uJ per check), marginal b (uJ per byte)")
        print("  crossover : a / (cost of re-executing one operation) in ops per item")
        print()
        print("  prediction: a = 1-3 uJ; crossover at 10^4-10^6 ops per item")
        print("  falsifier : a outside 0.3-10 uJ, or crossover outside 10^3-10^7 ops")
        print()
        print("  why it matters: 1 W buys 10^6 checks/s at 1 uJ — the real cap on fraud-proof designs,")
        print("  and the energy price of this estate's own product.")
        return 2
    print("REFUSED: data present but the extraction is not implemented in this change.")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
