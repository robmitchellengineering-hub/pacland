"""Route C exact sub-item — the conifold coefficients are rationals, not measurements."""
import unittest
from fractions import Fraction

from pacland.periods import exact_series as E


class TestTheExactCoefficients(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = E.against_numeric(10)

    def test_every_coefficient_is_rational(self):
        self.assertTrue(self.r["all_rational"])
        for c in self.r["exact"]:
            self.assertIsInstance(c, Fraction)

    def test_the_leading_coefficient_is_one(self):
        self.assertEqual(self.r["exact"][0], Fraction(1))

    def test_the_exact_series_reproduces_the_numeric_one(self):
        # two independent evaluations of the same recursion must agree to machine precision and beyond
        self.assertLess(self.r["worst_relative"], 1e-30)

    def test_the_known_first_coefficients(self):
        c = self.r["exact"]
        self.assertEqual(c[1], Fraction(37, 30))
        self.assertEqual(c[2], Fraction(2309, 1800))
        self.assertEqual(c[3], Fraction(286471, 225000))


class TestTheFormStatement(unittest.TestCase):
    def test_it_says_where_the_transcendental_structure_lives(self):
        f = E.form()
        self.assertIn("rational", f["statement"])
        self.assertIn("LCS basis", f["statement"])

    def test_it_does_not_claim_the_connection_exactly(self):
        f = E.form()
        self.assertIn("NOT derived exactly", f["connection_matrix"])
        self.assertIn("measured", f["connection_matrix"])


class TestTheRecursionCanFail(unittest.TestCase):
    def test_a_resonant_index_raises_rather_than_returning_a_number(self):
        with self.assertRaises(ArithmeticError):
            # s0 = 1 sits on the resonance the module guards against
            E.conifold_coefficients(n_max=6, s0=1)


if __name__ == "__main__":
    unittest.main()
