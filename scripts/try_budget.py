#!/usr/bin/env python3
"""The try-budget wrapper — a budget in the units the API actually exposes.

    python3 scripts/try_budget.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import try_budget as T  # noqa: E402


def main() -> int:
    print("The try-budget wrapper — what a budget can honestly count\n")
    r = T.run_to_budget(T.dry_sampler([[], [], [1], []]), calls=4)
    print(f"  calls ............. {r.calls}")
    print(f"  points ............ {len(r.points)}  (per call: {r.per_call})")
    print(f"  seconds ........... {r.seconds:.3f}")
    print(f"  yield ............. {r.yield_per_call:.2f} per call")
    print(f"  tries ............. {r.tries}")
    print(f"  stopped because ... {r.stopped_because}")
    print("\nThe sampler caps its own search per call and does not expose the try count, so a budget in")
    print("'tries' is not available from outside. This wrapper spends calls and seconds — the units the API")
    print("has — and reports tries as UNKNOWN rather than inferring them. That is the fix for T1's silent")
    print("'1200-try' run, which did 400.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
