"""The correlation-length bound: the exact definition, the quantified statement, and the
referee-independent check (no fitted mass gap imported)."""
import unittest

from pacland import correlation_length_bound as clb


class TestCorrelationLengthBound(unittest.TestCase):
    def test_connected_correlation_subtracts_the_vacuum(self):
        # G(x) = <P(0)P(x)> - <P(0)><P(x)>
        self.assertAlmostEqual(clb.connected_correlation(5.0, 2.0, 3.0), 5.0 - 6.0)

    def test_correlation_length_is_inverse_decay_rate(self):
        self.assertAlmostEqual(clb.correlation_length(0.5), 2.0)

    def test_derived_exponent_is_12pi2_over_11(self):
        self.assertAlmostEqual(clb.asymptotic_freedom_exponent(2.0), 12 * 3.141592653589793 ** 2 / 11, places=9)

    def test_bound_survives_only_with_the_derived_exponent(self):
        c = clb.asymptotic_freedom_exponent(2.0)
        self.assertTrue(clb.check_bound_independent(2.0, c, 1.0)["survives"])
        # a fitted exponent (1.182) is REJECTED — the fitted result is not an assumption
        self.assertFalse(clb.check_bound_independent(2.0, 1.182, 1.0)["survives"])

    def test_non_finite_prefactor_is_rejected(self):
        c = clb.asymptotic_freedom_exponent(2.0)
        self.assertFalse(clb.check_bound_independent(2.0, c, 0.0)["survives"])


if __name__ == "__main__":
    unittest.main()
