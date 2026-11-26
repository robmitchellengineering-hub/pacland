#!/usr/bin/env python3
"""Generate web/proof-graph.mmd — the mermaid proof dependency graph, from the frontier data.

Thin wrapper around pacland.proof_graph.build(); the diagram source is derived from
web/research-frontier.json so the sextant page's flow chart cannot drift from the accounting.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.proof_graph import build  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "web" / "proof-graph.mmd"


def main() -> int:
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
