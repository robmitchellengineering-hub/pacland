"""Best-prediction ECS — guards the trust-gated estimate so it cannot drift.

Known answers (computed from data/climate/cmip6_ecs.json x cmip6_drift.json):
- naive (all 19)              mean ~4.084 K
- conservation-gated (5 clean) mean ~3.864 K
- trust-gated (2 GISS)         mean 2.710 K
- the gates pull ECS DOWN (naive > gated > trust), landing inside the IPCC
  likely range 2.5-4.0 K at the assessed best estimate ~3.0 K.
"""
import unittest

from pacland.climate.ecs_model import best_prediction, ecs_estimates


class TestEcsEstimates(unittest.TestCase):
    def test_naive_is_all_19(self):
        n = ecs_estimates()["naive"]
        self.assertEqual(n["n"], 19)
        self.assertAlmostEqual(n["mean_K"], 4.084, places=3)

    def test_conservation_gated_is_five_clean(self):
        g = ecs_estimates()["conservation_gated"]
        self.assertEqual(g["n"], 5)
        self.assertAlmostEqual(g["mean_K"], 3.864, places=3)

    def test_trust_gated_is_two_giss(self):
        t = ecs_estimates()["trust_gated"]
        self.assertEqual(t["n"], 2)
        self.assertAlmostEqual(t["mean_K"], 2.710, places=3)
        self.assertEqual(sorted(t["models"]), ["GISS-E2-1-G", "GISS-E2-1-G-CC"])

    def test_gates_pull_ecs_down(self):
        e = ecs_estimates()
        self.assertGreater(e["naive"]["mean_K"], e["conservation_gated"]["mean_K"])
        self.assertGreater(e["conservation_gated"]["mean_K"], e["trust_gated"]["mean_K"])

    def test_trust_gated_lands_inside_ipcc_range(self):
        b = best_prediction()
        self.assertTrue(b["inside_ipcc_likely"])
        lo, hi = b["ipcc_likely_range_K"]
        self.assertTrue(lo <= b["best_estimate_K"] <= hi)

    def test_survivor_is_one_family(self):
        # The honest caveat, made into a check: the trust gate collapses to a
        # single model family (GISS), so the "spread" is degenerate by design.
        b = best_prediction()
        self.assertEqual(b["survivor_families"], ["GISS"])
        self.assertEqual(b["trust_gated"]["min_K"], b["trust_gated"]["max_K"])

    def test_shift_removes_hot_model_bias(self):
        b = best_prediction()
        self.assertAlmostEqual(b["shift_K"], 4.084 - 2.710, places=2)
        self.assertGreater(b["shift_K"], 1.0)


if __name__ == "__main__":
    unittest.main()
