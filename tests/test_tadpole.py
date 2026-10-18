import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.structure import _gauss_solve, _pearson

DATA = Path(__file__).resolve().parents[1] / "data" / "vacua_observables.json"

SYMPLECTIC = [[0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 1],
              [-1, 0, 0, 0, 0, 0],
              [0, -1, 0, 0, 0, 0],
              [0, 0, -1, 0, 0, 0]]


def _feats(f):
    return [f[i] * f[j + 6] for i in range(6) for j in range(6)]


class TestTadpoleSymplectic(unittest.TestCase):
    def test_tadpole_is_exact_symplectic_pairing(self):
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
        self.assertEqual(r, 1.0)
        self.assertLess(maxres, 1e-8)
        J = [[round(beta[i * 6 + j]) for j in range(6)] for i in range(6)]
        self.assertEqual(J, SYMPLECTIC)


if __name__ == "__main__":
    unittest.main()
