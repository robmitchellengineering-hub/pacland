"""GDPNow tests — the real-time record, the four guards, and the deficit ceiling."""
import copy
import unittest

from pacland.economics import gdpnow as G


class TestFixture(unittest.TestCase):
    def setUp(self):
        self.data = G.load()

    def test_record_size_and_span(self):
        recs = G.records(self.data)
        self.assertEqual(len(recs), 37)
        self.assertEqual(recs[0]["quarter"], "2016Q2")
        self.assertEqual(recs[-1]["quarter"], "2025Q4")

    def test_every_record_carries_its_vintages(self):
        for r in G.records(self.data):
            for key in ("nowcast", "nowcast_vintage", "benchmark_growth",
                        "benchmark_vintage", "advance", "advance_vintage"):
                self.assertIn(key, r, r["quarter"])

    def test_targets_are_growth_not_levels(self):
        for r in G.records(self.data):
            self.assertLess(abs(r["advance"]), 60.0, r["quarter"])


class TestGuards(unittest.TestCase):
    def test_all_four_are_green(self):
        for guard in (G.guard_nowcast_predates_release, G.guard_benchmark_shares_the_vintage,
                      G.guard_target_is_the_first_publication, G.guard_units_are_growth):
            ok, msg = guard()
            self.assertTrue(ok, msg)

    def test_a_nowcast_from_after_the_release_is_caught(self):
        data = copy.deepcopy(G.load())
        data["quarters"][0]["nowcast_vintage"] = data["quarters"][0]["advance_vintage"]
        ok, msg = G.guard_nowcast_predates_release(data)
        self.assertFalse(ok)
        self.assertIn("NOT BEFORE", msg)

    def test_a_benchmark_from_another_vintage_is_caught(self):
        data = copy.deepcopy(G.load())
        data["quarters"][0]["benchmark_vintage"] = "1999-01-01"
        ok, msg = G.guard_benchmark_shares_the_vintage(data)
        self.assertFalse(ok)
        self.assertIn("MISMATCH", msg)

    def test_level_units_are_caught(self):
        data = copy.deepcopy(G.load())
        data["quarters"][0]["advance"] = 23526.085
        ok, msg = G.guard_units_are_growth(data)
        self.assertFalse(ok)
        self.assertIn("level would be thousands", msg)


class TestEvaluation(unittest.TestCase):
    def test_the_nowcast_beats_the_null(self):
        r = G.evaluate()
        self.assertEqual(r["n"], 37)
        self.assertLess(r["ratio"]["mae"], 0.5)
        self.assertLess(r["ratio"]["rmse"], 0.5)

    def test_it_wins_more_paired_comparisons_than_it_loses(self):
        r = G.evaluate()
        self.assertGreater(r["wins"], r["n"] / 2)

    def test_excluding_2020_the_edge_survives(self):
        # the honest robustness check: COVID dominates the null's RMSE
        r = G.evaluate(exclude_2020=True)
        self.assertEqual(r["n"], 33)
        self.assertLess(r["ratio"]["mae"], 1.0)
        self.assertGreater(r["wins"], r["n"] / 2)

    def test_the_deficit_ceiling_is_one_observable(self):
        d = G.deficit()
        self.assertEqual(d.n_validation, 1)
        self.assertAlmostEqual(d.radius, 1.359, places=2)


class TestSummary(unittest.TestCase):
    def test_it_states_the_narrow_claim(self):
        s = G.summary()
        self.assertIn("ADVANCE estimate", s)
        self.assertIn("final revised value", s)


if __name__ == "__main__":
    unittest.main()
