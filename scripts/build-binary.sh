#!/bin/bash
# Build the double-clickable SEXTANT binaries with PyInstaller (macOS/Linux).
# Produces dist/sextant-node (the GUI) and dist/sextant-mcp (the MCP server).
set -euo pipefail
cd "$(dirname "$0")/.."

command -v pyinstaller >/dev/null 2>&1 || {
  echo "pyinstaller not found — install it:  pip3 install pyinstaller"
  exit 1
}

echo "↓ Building sextant-node (the GUI) …"
pyinstaller --noconfirm --onefile --name sextant-node \
  --add-data "web:web" \
  --hidden-import pacland.sextant_node \
  src/pacland/sextant_node.py

echo "↓ Building sextant-mcp (the MCP server) …"
pyinstaller --noconfirm --onefile --name sextant-mcp \
  --hidden-import pacland.mcp_server \
  src/pacland/mcp_server.py

echo
echo "Built:"
echo "  dist/sextant-node   (double-click to open the SEXTANT GUI)"
echo "  dist/sextant-mcp    (the MCP server for Claude Code / Cursor)"
echo
echo "The .dmg/.exe packaging (signing + bundling Python/Node) is the next step; these binaries"
echo "are the unsigned first cut."
