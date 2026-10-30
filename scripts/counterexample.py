#!/usr/bin/env python3
"""The counterexample engine — exhaustive window search with known-answer controls.

    python3 scripts/counterexample.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import counterexample as C  # noqa: E402


def main() -> int:
    print("The counterexample engine — D17's second instrument\n")
    verdicts = C.run_all()
    for v in verdicts:
        mark = "BROKEN " if v.counterexample is not None else "CLEAN  "
        print(f"{mark} {v.conjecture:<28} in {v.window}")
        print(f"         {v.proves}")
        print()
    broken = sum(1 for v in verdicts if v.counterexample is not None)
    print(f"{broken} of {len(verdicts)} broken, {len(verdicts) - broken} clean.")
    print("\nA clean verdict is a statement about THE WINDOW, never a proof. Two of these searches are")
    print("known-answer controls: they must find a counterexample, and if they ever stop finding one the")
    print("engine is blind rather than the conjecture being true. That is the check on the checker.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
