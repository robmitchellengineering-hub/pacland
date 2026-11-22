"""The three mass-gap routes are mutually consistent (m = 1/ξ = 3.2·√σ, RG exponent matches)."""
import unittest

from pacland import route_consistency as rc


class TestRouteConsistency(unittest.TestCase):
    def test_three_routes_agree(self):
        self.assertTrue(rc.check_consistency()["consistent"])

    def test_correlation_length_is_the_inverse(self):
        self.assertAlmostEqual(rc.correlation_length_from_m(3.0), 1.0 / rc.referee(3.0), places=10)

    def test_string_tension_is_the_square(self):
        self.assertAlmostEqual(rc.string_tension_from_m(3.0), (rc.referee(3.0) / 3.2) ** 2, places=10)

    def test_exponents_are_consistent(self):
        e = rc.consistent_exponents()
        self.assertEqual(e["correlation_length_exponent"], +1.182)
        self.assertEqual(e["string_tension_exponent"], -2 * 1.182)


if __name__ == "__main__":
    unittest.main()
