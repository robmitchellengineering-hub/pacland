#!/usr/bin/env python3
"""Generate the committed live status snapshot (web/delivery-status.json).

The status table in docs/TOOL-SEXTANT-DELIVERY.md points at this file; the live truth is
src/pacland/delivery_status.live_status(), and tests/test_delivery_status.py fails if the doc's
hand-asserted status drifts from it.

Usage: python3 scripts/build_delivery_status.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.delivery_status import live_status  # noqa: E402


def main() -> int:
    out = Path(__file__).resolve().parents[1] / "web" / "delivery-status.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(live_status(), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
