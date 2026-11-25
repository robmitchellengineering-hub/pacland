#!/bin/bash
# SEXTANT + VVS SDK — double-click installer (macOS).
# Double-click this file in Finder; it opens Terminal and installs both tools.
set -euo pipefail

echo "=============================================="
echo "  SEXTANT + Valiant Verification SDK  installer"
echo "=============================================="
echo

fail() { echo; echo "❌ $1"; echo "Press Return to close."; read -r; exit 1; }

# 1 — prerequisites
command -v python3 >/dev/null 2>&1 || fail "Python 3 not found. Install it from https://www.python.org/downloads/ first."
command -v node >/dev/null 2>&1 || fail "Node.js not found. Install Node 18+ from https://nodejs.org first."
command -v git >/dev/null 2>&1 || fail "git not found. Install it from https://git-scm.com first."
echo "✓ Python $(python3 --version 2>&1 | awk '{print $2}') · Node $(node --version) · git $(git --version | awk '{print $3}')"

# 2 — install SEXTANT (the discovery/verification engine) into ~/sextant
SEXTANT_DIR="$HOME/sextant"
if [ -d "$SEXTANT_DIR/.git" ]; then
  echo "✓ SEXTANT already present — updating"
  git -C "$SEXTANT_DIR" pull --quiet
else
  echo "↓ Downloading SEXTANT …"
  git clone --quiet --depth 1 https://github.com/robmitchellengineering-hub/pacland.git "$SEXTANT_DIR"
fi

# 3 — install the VVS SDK (the code-verification discipline)
VVS_TARBALL="https://api.morpheus.nz/api/functions/getPackage?name=valiant-verification-sdk&version=0.2.0"
echo "↓ Installing the Valiant Verification SDK …"
if command -v valiant >/dev/null 2>&1; then
  echo "✓ valiant already installed"
else
  npm install -g "$VVS_TARBALL" || echo "⚠ valiant install skipped (registry unreachable?) — install it later with: npm install -g '$VVS_TARBALL'"
fi

# 4 — the launch command (no Python typing required)
cat > "$SEXTANT_DIR/SEXTANT-node.command" <<'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 -m pacland.sextant_node
EOF
chmod +x "$SEXTANT_DIR/SEXTANT-node.command"

# 5 — register the MCP server with Claude Code / Cursor (so they can call SEXTANT + VVS)
echo "↓ Registering with Claude Code / Cursor …"
python3 "$SEXTANT_DIR/scripts/register-harness.py" 2>/dev/null \
  || echo "⚠ harness registration skipped (run it later: python3 $SEXTANT_DIR/scripts/register-harness.py)"

echo
echo "=============================================="
echo "  Done."
echo "  SEXTANT:  $SEXTANT_DIR"
echo "  Open it:  double-click SEXTANT-node.command (in $SEXTANT_DIR)"
echo "  VVS:      run 'valiant status' in a terminal"
echo "  Claude/Cursor: restart them to load the SEXTANT tools"
echo "=============================================="
echo "Press Return to close."
read -r
