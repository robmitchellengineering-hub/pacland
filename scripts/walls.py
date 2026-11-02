#!/usr/bin/env python3
"""Regenerate or verify the wall register.

    python3 scripts/walls.py            # write docs/walls.md
    python3 scripts/walls.py --check    # exit 1 on drift
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import walls as W  # noqa: E402

TARGET = ROOT / "docs" / "walls.md"


def main(argv) -> int:
    text = W.render()
    if "--check" in argv:
        current = TARGET.read_text(encoding="utf-8") if TARGET.is_file() else ""
        if current != text:
            print(f"drift: {TARGET.relative_to(ROOT)} does not match the register", file=sys.stderr)
            return 1
        print("wall register is up to date")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    c = W.counts()
    print(f"wrote {TARGET.relative_to(ROOT)}: {c['total']} walls ({c['provable']} provable, {c['dissolves']} "
          f"dissolve, {c['bounded']} bounded, {c['infrastructure']} infrastructure)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
