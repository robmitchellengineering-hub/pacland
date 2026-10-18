"""Reality Guard tests — falsification semantics plus seeded-fault mutations.

Each guard must rule out a candidate that is computable AND outside tolerance,
while a non-computable observable rules nothing out (prediction zone).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.reality_guards import (
    RealityGuard,
    STANDARD_REALITY_GUARDS,
    falsify,
    falsify_all,
    ruled_out,
)


class TestFalsify(unittest.TestCase):
    def test_within_tolerance_not_ruled_out(self):
        g = RealityGuard("alpha_s_MZ", -2.14, 0.01)
        self.assertFalse(falsify(g, -2.15).ruled_out)

    def test_outside_tolerance_ruled_out(self):
        # seeded fault: a candidate far from the measured value
        g = RealityGuard("alpha_s_MZ", -2.14, 0.01)
        v = falsify(g, -1.0)
        self.assertTrue(v.ruled_out)
        self.assertAlmostEqual(v.delta, 1.14, places=2)

    def test_not_computable_rules_nothing_out(self):
        # Lambda is not computable today -> prediction zone, not falsified
        g = RealityGuard("Lambda_MPl4", -280.9, 0.01)
        v = falsify(g, None)
        self.assertFalse(v.ruled_out)
        self.assertTrue(v.in_prediction_zone)

    def test_exact_match_delta_zero(self):
        g = RealityGuard("m_t_over_m_Z", 0.64, 0.01)
        v = falsify(g, 0.64)
        self.assertFalse(v.ruled_out)
        self.assertEqual(v.delta, 0.0)


class TestSuite(unittest.TestCase):
    def test_standard_suite_has_ten(self):
        self.assertEqual(len(STANDARD_REALITY_GUARDS), 10)

    def test_falsify_all_maps_ruled_out(self):
        # a candidate that matches everywhere except alpha_s
        predicted = {g.name: g.target_log for g in STANDARD_REALITY_GUARDS}
        predicted["alpha_s_MZ"] = -1.0  # wrong
        predicted["Lambda_MPl4"] = None  # not computable
        verdicts = falsify_all(STANDARD_REALITY_GUARDS, predicted)
        self.assertEqual(ruled_out(verdicts), ["alpha_s_MZ"])


if __name__ == "__main__":
    unittest.main()
