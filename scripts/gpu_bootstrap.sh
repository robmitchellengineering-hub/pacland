#!/usr/bin/env bash
# Bootstrap a rented cloud GPU (Ubuntu 22.04/24.04 + NVIDIA CUDA 12 image) into a
# working PACLAND flux-vacua sampler: JAX (CUDA 12) + JAXVacua + CYTools, then verify
# the GPU is seen by JAX and the quintic known-answer returns (1, 101).
#
# Run ONCE on the rented instance (as a sudo user). Easiest: paste as a single line.
#
#   curl -sSL https://raw.githubusercontent.com/robmitchellengineering-hub/pacland/main/scripts/gpu_bootstrap.sh | bash
#
# Then sample (e.g. 30 vacua at h12=25):
#   cd pacland && source .venv/bin/activate
#   python scripts/sample_h12_25.py 30 h12_25_vacua.json
set -euo pipefail

echo "== [1/5] system deps (GMP for CYTools) =="
sudo apt-get update -y
sudo apt-get install -y libgmp-dev libgmpxx4ldbl git python3-venv python3-pip

echo "== [2/5] clone pacland =="
test -d pacland || git clone https://github.com/robmitchellengineering-hub/pacland.git
cd pacland

echo "== [3/5] venv + JAX(CUDA12) + JAXVacua + CYTools =="
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
# NOTE: use `jax[cuda12]` on a CUDA 12 image; on a CUDA 11 image use `jax[cuda11]`.
.venv/bin/pip install "jax[cuda12]" jaxvacua cytools

echo "== [4/5] GPU + JAX check =="
.venv/bin/python - <<'PY'
import jax
print("JAX devices:", jax.devices())
assert any("gpu" in str(d).lower() for d in jax.devices()), "NO GPU DETECTED BY JAX"
print("GPU OK")
PY

echo "== [5/5] CYTools quintic known-answer (h11=1, h21=101) =="
.venv/bin/python - <<'PY'
from cytools import Polytope
p = Polytope([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [-1, -1, -1, -1]])
cy = p.triangulate().get_cy()
print("h11 =", cy.h11(), " h21 =", cy.h21())
assert (cy.h11(), cy.h21()) == (1, 101), "unexpected Hodge numbers"
print("CYTools OK")
PY

echo "== bootstrap complete =="
echo "Sample now:  source .venv/bin/activate && python scripts/sample_h12_25.py 30 h12_25_vacua.json"
