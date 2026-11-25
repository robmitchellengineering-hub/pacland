#!/usr/bin/env python3
"""Register the SEXTANT MCP server with Claude Code and Cursor.

Writes the SEXTANT + VVS MCP server entry into the harness configs, merging with whatever is
already there. After this, Claude Code / Cursor can call `sextant_verify`, `sextant_graph`,
`valiant_status`, etc.

Usage:  python3 scripts/register-harness.py
"""
import json
import sys
from pathlib import Path

PACLAND = Path(__file__).resolve().parents[1]


def server_config() -> dict:
    return {
        "command": "python3",
        "args": ["-m", "pacland.mcp_server"],
        "env": {"PYTHONPATH": str(PACLAND / "src")},
    }


def register(path: Path, config: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data: dict = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    servers = data.setdefault("mcpServers", {})
    servers["sextant"] = config
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"registered  {path}")


def main() -> int:
    home = Path.home()
    cfg = server_config()
    register(home / ".claude.json", cfg)
    register(home / ".cursor" / "mcp.json", cfg)
    print("done — restart Claude Code / Cursor to load the SEXTANT tools")
    return 0


if __name__ == "__main__":
    sys.exit(main())
