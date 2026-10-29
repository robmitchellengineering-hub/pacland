"""B1 fixed — the GV basis convention, and why integrality alone is not the check."""
import unittest
from fractions import Fraction

from pacland.periods import gv_basis as G


class TestConvention(unittest.TestCase):
    def test_the_round_trip_recovers_the_classical_integers(self):
        r = G.report()
        self.assertTrue(r["round_trip"])
        self.assertEqual(r["rows"][0]["correct"], Fraction(2875))
        self.assertEqual(r["rows"][1]["correct"], Fraction(609250))
        self.assertEqual(r["rows"][2]["correct"], Fraction(317206375))

    def test_the_coefficients_are_not_integers(self):
        # c_m carries 1/m^3 x the multi-cover sum -- if these were integers the relation would be trivial
        c = G.report()["coefficients"]
        self.assertEqual(c[1].denominator, 8)
        self.assertEqual(c[2].denominator, 27)

    def test_a_naive_readoff_returns_integers_and_the_wrong_ones(self):
        # THIS is the finding: integrality is not a sufficient check. The naive m^3 c_m is integral at
        # a composite degree and wrong by a factor that grows with m.
        r = G.report()
        self.assertTrue(r["naive_all_integer"])
        self.assertTrue(r["naive_any_wrong"])
        naive = G.naive_readoff(r["coefficients"])
        self.assertEqual(naive[1], Fraction(4876875))       # integer, and NOT 609250
        self.assertNotEqual(naive[1], Fraction(609250))

    def test_degree_one_is_the_same_either_way(self):
        # the defect only appears at composite degrees -- which is exactly where #209's check fired
        r = G.report()
        self.assertEqual(r["rows"][0]["naive"], r["rows"][0]["correct"])
        self.assertTrue(all(row["naive_is_wrong"] for row in r["rows"][1:]))


if __name__ == "__main__":
    unittest.main()
