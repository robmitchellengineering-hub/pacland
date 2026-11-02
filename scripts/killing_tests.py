#!/usr/bin/env python3
"""H-E: are the survivors the ones a test could have killed?

    python3 scripts/killing_tests.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import killing_tests as K  # noqa: E402


def main() -> int:
    a = K.audit()
    print("H-E: are the survivors the ones a test could have killed?\n")
    print(f"  {'record':<44}{'falsifier?':>11}{'status':>11}")
    for name, kind, stated, status, test in K.REGISTER:
        print(f"  {name[:43]:<44}{('yes' if stated else 'NO'):>11}{status:>11}")
    print(f"\n  {a['verdict']}")
    print(f"\n  demoted without a stated falsifier : {a['demoted']}")
    print(f"  survivors with one                : {a['survived']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
