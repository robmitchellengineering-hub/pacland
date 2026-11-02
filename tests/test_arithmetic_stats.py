"""Arithmetic statistics — the control validates the statistic; the arithmetic spectra deviate."""
import unittest

from pacland.spectral import arithmetic_stats as A


class TestTheStatistic(unittest.TestCase):
    def test_a_lattice_gives_ratio_one(self):
        # uniform spacing -> every adjacent pair has ratio 1.000; far from Poisson and GOE
        self.assertAlmostEqual(A.ratio([3 * k for k in range(200)]), 1.0, places=12)

    def test_the_nearest_reference_is_reported_with_its_gap(self):
        self.assertEqual(A.nearest_reference(0.386)[0], "Poisson")
        self.assertEqual(A.nearest_reference(0.531)[0], "GOE")


class TestTheThreeSpectra(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v = A.verdict()

    def test_the_control_lands_on_poisson(self):
        # this is what validates the instrument: no structure -> Poisson
        self.assertEqual(self.v["control_sits_at"], "Poisson")
        self.assertAlmostEqual(self.v["control_ratio"], A.RATIO_POISSON, delta=0.02)

    def test_the_zeta_zeros_sit_above_goe(self):
        z = next(r for r in self.v["rows"] if "zeta" in r["spectrum"])
        self.assertGreater(z["ratio"], A.RATIO_GOE)      # arithmetic rigidity, not noise

    def test_both_arithmetic_spectra_deviate_from_the_control(self):
        self.assertEqual(len(self.v["arithmetic_deviating"]), 2)

    def test_the_claim_names_the_consequence(self):
        self.assertIn("BGS", self.v["claim"])
        self.assertIn("measured correction", self.v["claim"])


class TestTheSpectraAreBuiltCorrectly(unittest.TestCase):
    def test_sums_of_two_squares_start_as_expected(self):
        self.assertEqual(A.sums_of_two_squares(25)[:5], [0, 1, 2, 4, 5])

    def test_the_control_is_deterministic(self):
        self.assertEqual(A.uniform_control(10, seed=3), A.uniform_control(10, seed=3))

    def test_zeta_zeros_begin_with_the_known_value(self):
        z = A.zeta_zeros(3)
        self.assertAlmostEqual(z[0], 14.1347, places=3)
        self.assertLess(z[0], z[1])


if __name__ == "__main__":
    unittest.main()
