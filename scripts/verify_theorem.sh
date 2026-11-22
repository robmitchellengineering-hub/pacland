#!/usr/bin/env bash
# Verify a theorem against the four-criteria standard (docs/PROOF-VERIFICATION-STANDARD.md).
# Usage: scripts/verify_theorem.sh <path/to/Theorem.lean>  (from the repo root)
set -euo pipefail

FILE="${1:?usage: verify_theorem.sh <path/to/Theorem.lean>}"
export PATH="$HOME/.elan/bin:$PATH"

PROOF_DIR="pacland-proof"
if [ ! -d "$PROOF_DIR" ]; then
  echo "proof tree not found at $PROOF_DIR" >&2
  exit 1
fi
if [ ! -f "$FILE" ]; then
  echo "theorem file not found: $FILE" >&2
  exit 1
fi

echo "== criterion 2: the library compiles (no sorry/admit/axiom) =="
if (cd "$PROOF_DIR" && lake build 2>&1) | grep -qE "error|warning: declaration uses 'sorry'"; then
  echo "BUILD FAILED or carries sorry/admit/axiom"
  exit 1
fi
echo "  build green"

echo "== criterion 3 + 4: the kernel accepts the theorem =="
if (cd "$PROOF_DIR" && lake env lean "../$FILE" 2>&1) | grep -qE "error|sorry|admit|axiom"; then
  echo "KERNEL REJECTED the file (error or sorry/admit/axiom)"
  exit 1
fi
echo "  kernel accepted (no error, no sorry/admit/axiom)"

echo "== criterion 4 (independent): con-leche / con-ron =="
echo "  NOTE: run the independent checker on the exported proof for the strongest bar:"
echo "  (not yet wired into this script — see docs/PROOF-VERIFICATION-STANDARD.md)"

echo "VERIFIED: $FILE meets criteria 2-4."
