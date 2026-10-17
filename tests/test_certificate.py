import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest
from math import log, sqrt

from pacland.certificate import (
    Certificate,
    empirical_exceedance,
    finite_d_certificate,
    hoeffding_radius,
    two_level_certificate,
)


class TestHoeffding(unittest.TestCase):
    def test_value_matches_definition(self):
        n, delta = 1000, 0.05
        self.assertAlmostEqual(
            hoeffding_radius(n, delta), sqrt(log(1.0 / delta) / (2.0 * n)), places=12
        )

    def test_monotonic_in_n(self):
        self.assertGreater(
            hoeffding_radius(100, 0.05), hoeffding_radius(10000, 0.05)
        )

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            hoeffding_radius(0, 0.05)
        with self.assertRaises(ValueError):
            hoeffding_radius(100, 0.0)
        with self.assertRaises(ValueError):
            hoeffding_radius(100, 1.0)


class TestTwoLevelCertificate(unittest.TestCase):
    def test_bound_and_confidence(self):
        cert = two_level_certificate(
            p_hat_g=0.10, n=1000, p_hat_e=0.05, m=100, delta_s=0.05, delta_e=0.05
        )
        r_s = sqrt(log(1.0 / 0.05) / (2.0 * 1000))
        r_e = sqrt(log(1.0 / 0.05) / (2.0 * 100))
        self.assertAlmostEqual(cert.bound, 0.10 + 0.05 + r_s + r_e, places=12)
        self.assertAlmostEqual(cert.confidence, 0.90, places=12)
        self.assertFalse(cert.exact)
        self.assertEqual(cert.n, 1000)
        self.assertEqual(cert.m, 100)

    def test_invalid_rates(self):
        with self.assertRaises(ValueError):
            two_level_certificate(1.5, 100, 0.0, 100, 0.05, 0.05)
        with self.assertRaises(ValueError):
            two_level_certificate(0.1, 100, -0.1, 100, 0.05, 0.05)


class TestFiniteDCertificate(unittest.TestCase):
    def test_sampling_term_vanishes(self):
        cert = finite_d_certificate(p_g_exact=0.2, p_hat_e=0.0, m=100, delta_e=0.05)
        self.assertTrue(cert.exact)
        self.assertIsNone(cert.n)
        self.assertEqual(cert.radius_s, 0.0)
        self.assertAlmostEqual(cert.confidence, 0.95, places=12)
        r_e = sqrt(log(1.0 / 0.05) / (2.0 * 100))
        self.assertAlmostEqual(cert.bound, 0.2 + 0.0 + r_e, places=12)


class TestEmpiricalExceedance(unittest.TestCase):
    def test_rate(self):
        self.assertAlmostEqual(
            empirical_exceedance([1, 2, 3, 4], 2.5), 0.5, places=12
        )

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            empirical_exceedance([], 1.0)


if __name__ == "__main__":
    unittest.main()
