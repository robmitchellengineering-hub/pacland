"""The instanton-corrected mass gap: positive, and a measurement of the free parameter W0."""
import unittest

from pacland.oracle.kklt_mass import mass_gap, stabilize, potential


class TestKKLTMass(unittest.TestCase):
    def test_susu_minimum_solves_DTW_0(self):
        s, resid = stabilize(-1e-3)
        self.assertLess(resid, 1e-12)

    def test_mass_is_positive(self):
        for W0 in (-1e-2, -1e-3, -1e-4):
            self.assertGreater(mass_gap(W0)["m2"], 0.0)

    def test_ads_before_uplift(self):
        for W0 in (-1e-2, -1e-3, -1e-4):
            self.assertLess(mass_gap(W0)["V"], 0.0)

    def test_mass_scales_with_W0(self):
        # the mass gap tracks the free parameter W0 (a value, not a fixed relation)
        m_hi = mass_gap(-1e-2)["mass"]
        m_lo = mass_gap(-1e-4)["mass"]
        self.assertGreater(m_hi, m_lo)


if __name__ == "__main__":
    unittest.main()
