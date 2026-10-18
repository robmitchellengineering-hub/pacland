"""Validate the flux oracle's tadpole: N_flux is EXACTLY the symplectic pairing.

Self-asserting (mesh discipline). The D3 tadpole is a topological charge with a
closed form: N_flux = F^T J H, where J is the symplectic intersection form on the
6-dimensional flux space (F = first 6 flux quanta, H = last 6). This script fits
the bilinear form F_i * H_j -> tadpole by exact least squares on the real
vacua_observables.json data and asserts:

  1. the fit is exact (r = 1.0, residual ~ machine epsilon), and
  2. the recovered 6x6 matrix J is the standard symplectic form
     [ 0  I ; -I  0 ]  (with signs fixed by the model's orientation).

Exits 0 iff both hold. Pure stdlib.
"""
import json
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from pacland.structure import _gauss_solve, _pearson  # noqa: E402

DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "vacua_observables.json",
)


def _feats(f):
    return [f[i] * f[j + 6] for i in range(6) for j in range(6)]


def main() -> int:
    with open(DATA) as fp:
        data = json.load(fp)
    records = [r for d in data.values() for r in d]
    fluxes = [r["flux"] for r in records]
    tads = [r["tadpole"] for r in records]

    X = [_feats(f) for f in fluxes]
    d = 36
    XtX = [[0.0] * d for _ in range(d)]
    Xty = [0.0] * d
    for xi, yi in zip(X, tads):
        for a in range(d):
            Xty[a] += xi[a] * yi
            for b in range(d):
                XtX[a][b] += xi[a] * xi[b]
    beta = _gauss_solve(XtX, Xty)
    pred = [sum(beta[k] * xi[k] for k in range(d)) for xi in X]
    r = _pearson(pred, tads)
    maxres = max(abs(p - t) for p, t in zip(pred, tads))

    J = [[round(beta[i * 6 + j]) for j in range(6)] for i in range(6)]
    symplectic = [[0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 1],
                  [-1, 0, 0, 0, 0, 0],
                  [0, -1, 0, 0, 0, 0],
                  [0, 0, -1, 0, 0, 0]]
    exact = r == 1.0 and maxres < 1e-8
    symp = J == symplectic
    out = {
        "guard": "tadpole_symplectic_pairing",
        "r": r,
        "max_residual": maxres,
        "matrix_J": J,
        "expected_symplectic": symplectic,
        "exact": exact,
        "is_standard_symplectic": symp,
        "passed": exact and symp,
    }
    print(json.dumps(out))
    return 0 if out["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
