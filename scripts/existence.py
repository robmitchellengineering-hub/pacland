#!/usr/bin/env python3
"""The existence engine — exhibit the object, or say none is in the window.

    python3 scripts/existence.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import existence as E  # noqa: E402


def main() -> int:
    print("The existence engine — the other side of the falsifier\n")
    for x in E.run_all():
        mark = "FOUND " if x.found is not None else "NONE  "
        print(f"{mark} {x.question}")
        print(f"        {x.states}")
        print(f"        why it matters: {x.why}")
        print()
    found = sum(1 for x in E.run_all() if x.found is not None)
    print(f"{found} of {len(E.run_all())} questions exhibit an object, and every verdict names its window.")
    print("An exhibited object is a resource: a concrete flux pair any other computation can be handed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
