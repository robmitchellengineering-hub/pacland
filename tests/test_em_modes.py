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
        self.assertEqual(tuple(idx), (0, 1, 1), f"lowest mode was {idx}")
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


class TestPolarisation(unittest.TestCase):
    def test_mode_fields_are_vectors_with_the_right_support(self):
        # TE modes have no Ez component; TM modes have one
        te = E.mode_field((1, 1, 1), "TE", 0.3, 0.4, 0.5, 3.0, 4.0, 2.5)
        tm = E.mode_field((1, 1, 1), "TM", 0.3, 0.4, 0.5, 3.0, 4.0, 2.5)
        self.assertEqual(te[2], 0.0)
        self.assertNotEqual(tm[2], 0.0)

    def test_polarisation_changes_the_rank(self):
        import random
        rng = random.Random(3)
        n = 4
        tx = [(0.6, 3.2, 1.5), (1.2, 2.4, 1.8), (1.8, 1.6, 2.0), (2.4, 0.8, 2.2)]
        rx = [((3.0 - x) * 0.8 + 0.3, (4.0 - y) * 0.8 + 0.4, z) for (x, y, z) in tx]
        scalar = E.streams(E.channel_matrix(3.0, 4.0, 2.5, 5.18e9, tx, rx), 20.0)
        pol = E.streams(E.channel_matrix_polarised(
            3.0, 4.0, 2.5, 5.18e9, tx, rx,
            [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)],
            [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]), 20.0)
        self.assertLessEqual(pol, scalar)


if __name__ == "__main__":
    unittest.main()
