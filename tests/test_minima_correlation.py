"""Pre-registered: if no lattice invariant correlates with is_minimum, the 0.8 law is model-specific."""
import unittest

from pacland.exactness import minima_correlation as M


class TestThePreRegisteredTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = M.correlations()

    def test_no_lattice_invariant_predicts_a_minimum(self):
        for k in ("b3", "N", "support", "max_comp"):
            v = self.r["correlations"][k]
            if v is None:
                continue
            self.assertLess(abs(v), 0.2, f"{k}: {v}")

    def test_the_only_real_predictor_is_dynamical(self):
        # log|DW| is the SUSY order parameter, not a lattice invariant
        self.assertLess(abs(self.r["correlations"]["log|DW|"]), 0.6)
        self.assertGreater(abs(self.r["correlations"]["log|DW|"]), 0.2)

    def test_primitivity_is_constant_so_it_carries_no_information(self):
        self.assertIsNone(self.r["correlations"]["primitive"])

    def test_the_rate_reproduces_the_gated_figure(self):
        self.assertAlmostEqual(self.r["minima_rate"], 0.805, places=2)


if __name__ == "__main__":
    unittest.main()
