"""F2 M2d — the recursion matrix, and the two branches at the double root.

The matrix is checked against the two computations that already existed (the indicial polynomial from
M2a and the numeric series from M2c), and every branch is held to the same gate: a constant combination
of the LCS basis, tested away from the points it was fitted at.
"""
import unittest

import mpmath as mp
import sympy as sp

from pacland.periods import conifold_recursion as R
from pacland.periods import connection as C


class TestMatrix(unittest.TestCase):
    def test_the_indicial_coefficient_is_the_m2a_polynomial(self):
        r = R.consistency(10)
        self.assertTrue(r["indicial_matches"], str(r["indicial_from_matrix"]))

    def test_the_resonance_pattern_matches_m2b(self):
        # vanishes at s0=0 for n=-2 and n=-1, at s0=1 only for n=-2, never at s0=2
        r = R.consistency(10)
        self.assertTrue(r["pattern_matches"], r["resonance_pattern"])

_CACHE = {}


def all_branches():
    """The three reachable branches, computed once for the whole module (the matrix is expensive)."""
    if "r" not in _CACHE:
        _CACHE["r"] = R.all_branches(80)
        _CACHE["d"] = R.double_root(80)
    return _CACHE["r"]


class TestDoubleRoot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = _CACHE.get("d") or R.double_root(80)
        _CACHE["d"] = cls.d

    def test_the_two_branches_are_finite(self):
        for n in range(6):
            self.assertTrue(mp.isfinite(self.d["d0"][n]))
            self.assertTrue(mp.isfinite(self.d["d1"][n]))

    def test_the_series_branch_connects(self):
        r = all_branches()["exponent_1_series"]
        self.assertLess(float(r["worst"]), 1e-9, f"worst {mp.nstr(r['worst'], 3)}")

    def test_the_log_branch_connects(self):
        r = all_branches()["exponent_1_log"]
        self.assertLess(float(r["worst"]), 1e-9, f"worst {mp.nstr(r['worst'], 3)}")

    def test_the_branches_are_different(self):
        # if the log branch were secretly the series branch, both would have the same coefficients
        a = all_branches()["exponent_1_series"]["coefficients"]
        b = all_branches()["exponent_1_log"]["coefficients"]
        self.assertGreater(abs(a[0] - b[0]) / max(abs(a[0]), abs(b[0])), 1e-3)


class TestAllBranches(unittest.TestCase):
    def test_three_of_four_branches_close(self):
        r = all_branches()
        self.assertEqual(len(r), 3)
        for name, v in r.items():
            # 1e-9 rather than 1e-10: at 60-80 terms the *conifold* series truncation at u = 0.75 is
            # ~1e-10, so the residual is a statement about term count, not about the connection
            self.assertLess(float(v["worst"]), 1e-9, f"{name}: worst {mp.nstr(v['worst'], 3)}")

    def test_the_exponent_2_column_agrees_with_m2c(self):
        r = all_branches()["exponent_2"]["coefficients"]
        m2c = C.connect()["coefficients"]
        for i in range(4):
            self.assertLess(abs(r[i] - m2c[i]) / max(abs(m2c[i]), 1), 1e-10)


if __name__ == "__main__":
    unittest.main()
