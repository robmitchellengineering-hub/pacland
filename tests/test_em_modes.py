"""The electromagnetic twin of the room engine: exact counting, Weyl, degeneracy."""
import math
import unittest

from pacland.spectral import em_modes as E


class TestExactModes(unittest.TestCase):
    def test_te101_frequency_of_a_cube(self):
        # TE101 in a cube of side a: f = c/(2a) * sqrt(2)
        a = 0.5
        modes = E.cavity_modes(a, a, a, 1e9)
        f101, pol, idx = modes[0]
        self.assertEqual(pol, "TE")
        self.assertAlmostEqual(idx, (0, 1, 1), msg=f"lowest mode was {idx}")
        self.assertAlmostEqual(f101, E.C_LIGHT / (2 * a) * math.sqrt(2), places=0)

    def test_count_grows_with_bandwidth(self):
        self.assertLess(E.exact_count(0.5, 0.5, 0.5, 1e9), E.exact_count(0.5, 0.5, 0.5, 3e9))

    def test_every_mode_is_te_or_tm_and_positive(self):
        for f, pol, idx in E.cavity_modes(0.5, 0.4, 0.3, 2e9):
            self.assertIn(pol, ("TE", "TM"))
            self.assertGreater(f, 0)
            self.assertNotEqual(idx, (0, 0, 0))


class TestWeyl(unittest.TestCase):
    def test_the_fitted_law_reproduces_the_exact_count_within_a_percent(self):
        a, b, d, f_max = 3.0, 4.0, 2.5, 3e9
        n = E.exact_count(a, b, d, f_max)
        coef = E.fit_surface_coefficient(a, b, d, f_max)["surface_coefficient"]
        weyl = E.weyl_count(f_max, a * b * d, 2 * (a * b + b * d + a * d), surface_coefficient=coef)
        self.assertLess(abs(weyl - n) / n, 0.01, f"weyl {weyl}, exact {n}")


class TestDegeneracy(unittest.TestCase):
    def test_a_cube_is_heavily_degenerate(self):
        r = E.degeneracy(0.5, 0.5, 0.5, 3e9)
        self.assertGreater(r["fraction"], 0.5, r)

    def test_distinct_never_exceeds_modes(self):
        r = E.degeneracy(3.0, 4.0, 2.5, 1e9)
        self.assertLessEqual(r["distinct"], r["modes"])


if __name__ == "__main__":
    unittest.main()
