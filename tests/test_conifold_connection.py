"""F2 M2c — the connection closes, and the log normalisation is load-bearing.

The gate: the exponent-2 conifold branch must be a **constant** linear combination of the four z = 0
branches. Fitted at 0.3–0.6 z_c, tested at points not used, the residual is at the rounding level. If the
binomial weight in the log normalisation is dropped, it is not — and that mutation is the test.
"""
import unittest

import mpmath as mp

from pacland.periods import connection as C
from pacland.periods import quintic as Q


class TestConnection(unittest.TestCase):
    def test_it_closes(self):
        r = C.connect()
        self.assertTrue(r["closes"], f"worst residual {mp.nstr(r['worst'], 3)}")
        self.assertLess(float(r["worst"]), 1e-14)

    def test_the_fit_is_well_conditioned(self):
        r = C.connect()
        self.assertLess(float(r["cond"]), 1e9)

    def test_the_coefficients_are_stable(self):
        a = C.connect()["coefficients"]
        b = C.connect(n_max=200)["coefficients"]
        for i in range(4):
            self.assertLess(abs(a[i] - b[i]) / max(abs(a[i]), 1), 1e-14)

    def test_the_far_points_are_truncation_limited_not_wrong(self):
        # at 0.9 / 0.95 the conifold series' own truncation dominates; the residual there is a
        # statement about term count and is reported separately, never inside the verdict
        r = C.connect()
        far = [row for row in r["rows"] if not row["in_verdict"]]
        self.assertTrue(far)
        for row in far:
            self.assertLess(float(row["relative"]), 1e-3)


class TestTheWeightIsLoadBearing(unittest.TestCase):
    """Dropping the binomial weight leaves omega_2 and omega_3 outside the solution space."""

    def _lcs_without_binomial(self, z, k, n_max=140):
        mp.mp.dps = 50
        z = mp.mpf(z)
        parts = Q.as_log_parts(k, n_max, dps=50)
        # as_log_parts now carries the binomial weight k!/(k-j)!; divide it back out to reproduce the bug
        weights = [mp.factorial(k) / mp.factorial(k - j) for j in range(k + 1)]
        return sum(mp.log(z) ** j / mp.factorial(j) *
                   (sum(f[n] * z ** n for n in range(n_max + 1)) / weights[j])
                   for j, f in enumerate(parts) if j <= k)

    def test_without_the_weight_the_connection_does_not_close(self):
        mp.mp.dps = 50
        c = C.conifold_series(160)
        M = mp.matrix(4, 4)
        b = mp.matrix(4, 1)
        for i, frac in enumerate(C.FIT_POINTS):
            z = C.ZC * mp.mpf(frac)
            b[i] = C.conifold_value(z, c)
            for k in range(4):
                M[i, k] = self._lcs_without_binomial(z, k)
        a = mp.lu_solve(M, b)
        z = C.ZC * mp.mpf("0.7")
        pred = sum(a[k] * self._lcs_without_binomial(z, k) for k in range(4))
        exact = C.conifold_value(z, c)
        # the corrected version gives ~1e-25 here; the unweighted one must be far worse
        self.assertGreater(float(abs(pred - exact) / abs(exact)), 1e-6)


if __name__ == "__main__":
    unittest.main()
