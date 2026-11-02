#!/usr/bin/env python3
"""Regenerate or verify the measure-invariance register.

    python3 scripts/measure_audit.py            # write docs/measure-invariance.md
    python3 scripts/measure_audit.py --check    # exit 1 if the file has drifted
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import measure_invariance as M  # noqa: E402

TARGET = ROOT / "docs" / "measure-invariance.md"


def main(argv) -> int:
    text = M.render()
    if "--check" in argv:
        current = TARGET.read_text(encoding="utf-8") if TARGET.is_file() else ""
        if current != text:
            print(f"drift: {TARGET.relative_to(ROOT)} does not match the register", file=sys.stderr)
            return 1
        print("measure-invariance register is up to date")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    c = M.counts()
    print(f"wrote {TARGET.relative_to(ROOT)}: {c['invariant']} invariant, {c['dependent']} dependent")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
