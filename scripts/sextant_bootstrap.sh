#!/usr/bin/env bash
# SEXTANT mesh bootstrap — put a SEXTANT instance on a node and prove it runs.
#
# A node that runs this and prints "catalog OK" has a working yes/no engine: the full claim
# registry, the live falsifiers (numpy/stim, quimb optional), and the CHSH control (2√2) all run.
# This is the "instance" that gets SEXTANT onto every mesh node for parallel formalization.
set -uo pipefail

REPO="https://github.com/robmitchellengineering-hub/pacland.git"
WORK="${PACLAND_DIR:-$HOME/pacland}"

echo "== SEXTANT bootstrap on $(hostname) =="

# 1. clone or pull
if [ -d "$WORK/.git" ]; then
  git -C "$WORK" pull --ff-only 2>&1 | tail -1 || { echo "FAIL: pull"; exit 1; }
else
  git clone --depth 1 "$REPO" "$WORK" 2>&1 | tail -1 || { echo "FAIL: clone"; exit 1; }
fi

# 2. python deps — numpy + stim are required, quimb is optional
cd "$WORK"
python3 -m venv .venv 2>/dev/null || true
# shellcheck disable=SC1091
. .venv/bin/activate 2>/dev/null || true
pip install -q --disable-pip-version-check numpy stim 2>&1 | tail -1 || { echo "FAIL: pip"; exit 1; }
pip install -q --disable-pip-version-check quimb 2>/dev/null || echo "note: quimb skipped (optional)"

# 3. run the SEXTANT guard — the falsifier suite + the exact CHSH control
GUARD_LOG="$WORK/sextant-guard.txt"
python3 scripts/validate_sextant.py 2>&1 | tee "$GUARD_LOG"

# 4. verdict: pass requires the guard to report the catalog-OK line
if grep -q "catalog OK" "$GUARD_LOG"; then
  echo "RESULT: SEXTANT instance is LIVE on $(hostname)"
  exit 0
else
  echo "RESULT: guard did not report OK"
  exit 1
fi
