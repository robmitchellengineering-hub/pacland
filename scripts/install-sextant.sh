#!/usr/bin/env bash
# SEXTANT installer — the headless simulated quantum computer, one command.
#
#   curl -fsSL https://raw.githubusercontent.com/robmitchellengineering-hub/pacland/main/scripts/install-sextant.sh | bash
#
# Installs into ~/sextant (a venv) and puts `sextant` + `sextant-node` on PATH via ~/.local/bin.
#
# Platform behaviour:
#   x86_64 (Linux/macOS)   — stim is a pre-built wheel, instant.
#   aarch64 (Raspberry Pi) — stim compiles from source on first install (~10-30 min native);
#                            every other dependency is a pre-built wheel.
set -euo pipefail

DEST="${SEXTANT_HOME:-$HOME/sextant}"
BIN="$HOME/.local/bin"
PY="${PYTHON:-python3}"

echo "== SEXTANT installer =="
echo "   dest: $DEST"
mkdir -p "$DEST" "$BIN"

# 1. clone pacland (the full SEXTANT: sextant.py + phantom.py + sextant_node.py)
if [ -d "$DEST/pacland/.git" ]; then
  (cd "$DEST/pacland" && git pull -q --ff-only) || true
else
  git clone -q https://github.com/robmitchellengineering-hub/pacland.git "$DEST/pacland"
fi

# 2. venv + the deps (stim wheel on x86_64; native compile on aarch64)
if [ ! -x "$DEST/venv/bin/python" ]; then
  "$PY" -m venv "$DEST/venv"
fi
"$DEST/venv/bin/pip" install -q --upgrade pip
echo "   installing pacland + stim/quimb/numpy (this is the long step on a Pi)…"
"$DEST/venv/bin/pip" install -q -e "$DEST/pacland" stim quimb numpy

# 3. put the commands on PATH
ln -sf "$DEST/venv/bin/sextant"      "$BIN/sextant"
ln -sf "$DEST/venv/bin/sextant-node" "$BIN/sextant-node"

echo ""
echo "Installed. Run the whole engine:"
echo "  sextant --verify        # 28/28 claims survive their falsifier"
echo "  sextant verify chsh     # one claim"
echo "  sextant-node            # headless node at http://127.0.0.1:8090"
echo ""
if ! echo "$PATH" | tr ':' '\n' | grep -qxF "$BIN"; then
  echo "Add ~/.local/bin to your PATH:"
  echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi
