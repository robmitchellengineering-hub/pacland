"""B3 retried — de Sitter requires a positive term beyond the F-term potential."""
import mpmath as mp
import unittest

from pacland.oracle import ds_needs_uplift as D


class TestTheProvedHalf(unittest.TestCase):
    """At a SUSY point the F-term potential is negative, for a Kahler modulus too."""

    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 30
        cls.s = D.susy_point()

    def test_a_susy_point_is_found(self):
        self.assertAlmostEqual(float(self.s["T"]), 43.58, places=1)

    def test_dw_is_zero_at_the_root(self):
        self.assertLess(abs(self.s["DW"]), mp.mpf("1e-25"))

    def test_the_identity_holds(self):
        self.assertLess(self.s["identity_residual"], mp.mpf("1e-25"))

    def test_the_potential_is_negative(self):
        self.assertTrue(self.s["is_ads"])
        self.assertLess(self.s["V"], 0)


class TestTheExhibitedHalf(unittest.TestCase):
    """An uplift above D_crit lifts the same minimum to de Sitter."""

    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 30
        cls.s = D.susy_point()
        cls.u = D.uplift_scan(cls.s)

    def test_d_critical_gives_exactly_minkowski(self):
        self.assertTrue(self.u["minkowski_at_critical"])

    def test_below_the_threshold_is_still_ads(self):
        self.assertTrue(self.u["below_is_ads"])

    def test_above_the_threshold_is_ds(self):
        self.assertTrue(self.u["above_is_ds"])

    def test_the_threshold_is_computed_not_searched(self):
        # D_crit = 3 |W|^2 / (2T) — a formula, so a reader can check it by hand
        T = self.s["T"]
        W = mp.mpf("-0.05") + mp.exp(mp.mpf("-0.1") * T)
        self.assertLess(abs(self.u["D_crit"] - 3 * W ** 2 / (2 * T)) / self.u["D_crit"], mp.mpf("1e-30"))


class TestTheEngineRefusesABadBracket(unittest.TestCase):
    def test_no_sign_change_raises_rather_than_returning_a_point(self):
        # W0 = -A kills the small-T divergence and leaves no root: the code must say so
        with self.assertRaises(ArithmeticError):
            D.susy_point(W0=mp.mpf("-1"), A=1, a=mp.mpf("0.1"))


if __name__ == "__main__":
    unittest.main()
