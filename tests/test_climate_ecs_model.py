"""Best-prediction ECS — guards both views (widened and strict) against drift.

Known answers:
  widened naive (53)          mean ~3.777 K
  sens+forc gated (15)        mean ~3.081 K, ~13 families, range 2.56-3.87
  strict naive (19)           mean ~4.084 K
  conservation-gated (5)      mean ~3.864 K
  trust-gated (2 GISS)        mean ~2.710 K, one family

The honest caveat is encoded as a check: the widened gate is a multi-family
ensemble, the strict three-axis gate collapses to a single family.
"""
import unittest

from pacland.climate.ecs_model import best_prediction, ecs_estimates


class TestWidenedView(unittest.TestCase):
    def test_widened_naive_is_53(self):
        wn = ecs_estimates()["widened_naive"]
        self.assertEqual(wn["n"], 53)
        self.assertAlmostEqual(wn["mean_K"], 3.7768, places=3)

    def test_sens_forc_gated_is_15(self):
        sf = ecs_estimates()["sens_forc_gated"]
        self.assertEqual(sf["n"], 15)
        self.assertAlmostEqual(sf["mean_K"], 3.0807, places=3)
        self.assertAlmostEqual(sf["min_K"], 2.56, places=2)
        self.assertAlmostEqual(sf["max_K"], 3.87, places=2)

    def test_widened_gate_is_multi_family(self):
        e = ecs_estimates()
        self.assertGreaterEqual(e["sens_forc_families"], 10)

    def test_widened_gate_pulls_ecs_down(self):
        e = ecs_estimates()
        self.assertGreater(e["widened_naive"]["mean_K"], e["sens_forc_gated"]["mean_K"])


class TestStrictView(unittest.TestCase):
    def test_strict_naive_is_19(self):
        sn = ecs_estimates()["strict_naive"]
        self.assertEqual(sn["n"], 19)
        self.assertAlmostEqual(sn["mean_K"], 4.084, places=3)

    def test_conservation_gated_is_five(self):
        cg = ecs_estimates()["conservation_gated"]
        self.assertEqual(cg["n"], 5)
        self.assertAlmostEqual(cg["mean_K"], 3.864, places=3)

    def test_trust_gated_is_two_giss(self):
        tg = ecs_estimates()["trust_gated"]
        self.assertEqual(tg["n"], 2)
        self.assertAlmostEqual(tg["mean_K"], 2.710, places=3)
        self.assertEqual(tg["models"], ["GISS-E2-1-G", "GISS-E2-1-G-CC"])

    def test_strict_gates_pull_ecs_down(self):
        e = ecs_estimates()
        self.assertGreater(e["strict_naive"]["mean_K"], e["conservation_gated"]["mean_K"])
        self.assertGreater(e["conservation_gated"]["mean_K"], e["trust_gated"]["mean_K"])

    def test_trust_gate_is_one_family(self):
        # the honest caveat, made a check
        e = ecs_estimates()
        self.assertEqual(e["trust_families"], 1)


class TestBestPrediction(unittest.TestCase):
    def test_both_views_inside_ipcc(self):
        b = best_prediction()
        self.assertTrue(b["inside_ipcc_likely"])
        lo, hi = b["ipcc_likely_range_K"]
        self.assertTrue(lo <= b["best_estimate_K"] <= hi)
        self.assertTrue(lo <= b["strict_estimate_K"] <= hi)

    def test_bracket_order(self):
        b = best_prediction()
        self.assertLess(b["bracket_K"][0], b["bracket_K"][1])

    def test_bracket_spans_ipcc_best_estimate(self):
        b = best_prediction()
        lo, hi = b["bracket_K"]
        self.assertTrue(lo <= b["ipcc_best_estimate_K"] <= hi)


if __name__ == "__main__":
    unittest.main()
