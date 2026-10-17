#!/usr/bin/env bash
# Install CYTools + its C++ prerequisites, then verify against the quintic.
# Usage: bash scripts/install_cytools.sh
# See docs/toolchain.md for the reasoning and the macOS alternative.
set -euo pipefail

if command -v apt-get >/dev/null 2>&1; then
  echo "== Linux: installing GMP via apt =="
  sudo apt-get update
  sudo apt-get install -y libgmp-dev libgmpxx4ldbl
else
  echo "== non-Linux: assuming GMP is already installed (brew/conda) =="
fi

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install cytools

echo "== verifying (quintic -> h11=1, h21=101) =="
.venv/bin/python - <<'PY'
from cytools import Polytope
p = Polytope([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [-1, -1, -1, -1]])
cy = p.triangulate().get_cy()
print("h11 =", cy.h11(), " h21 =", cy.h21())
assert (cy.h11(), cy.h21()) == (1, 101), "unexpected Hodge numbers"
print("CYTools OK")
PY
