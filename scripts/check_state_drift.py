#!/usr/bin/env python3
"""Regenerate the live-state files and fail (exit 1) if the committed copy drifted.

The live-state files (web/delivery-status.json, web/research-frontier.json) are generated from the
code. This script regenerates them and diffs against the committed copy — if a code change made the
state stale and no one regenerated, CI fails here. The generators are deterministic (no timestamps),
so a clean run produces no diff.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GENERATORS = [
    ("scripts/build_delivery_status.py", "web/delivery-status.json"),
    ("scripts/build_frontier_view.py", "web/frontier-view.json"),
]


def main() -> int:
    for script, _out in GENERATORS:
        subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)
    r = subprocess.run(["git", "diff", "--exit-code", "--",
                        "web/delivery-status.json", "web/frontier-view.json"],
                       cwd=ROOT)
    if r.returncode != 0:
        print("STATE DRIFT: the committed live-state files are stale. "
              "Run scripts/build_delivery_status.py and scripts/build_frontier_view.py, then commit.")
        return 1
    print("live-state files match the code (no drift)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
