"""The rate wall — the measured loss, and the honest boundary of the claim."""
import unittest

from pacland.exactness import rate_wall as W


class TestTheRates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = W.the_wall()

    def test_every_rate_carries_its_budget(self):
        for r in self.w["rows"]:
            self.assertGreater(r["tries"], 0)
            self.assertIn("where", r)

    def test_the_loss_is_at_convergence_not_proposal(self):
        # validity barely moves; points-per-valid collapses
        self.assertLess(self.w["validity_loss"], 0.10)
        self.assertGreater(self.w["convergence_ratio"], 50)

    def test_the_ratio_is_quoted_with_its_direction(self):
        self.assertIn("collapses", self.w["statement"])

    def test_the_hypothesis_is_labelled_a_hypothesis(self):
        self.assertIn("solve dimension doubles", self.w["hypothesis"])
        self.assertIn("alternative", self.w["hypothesis"])

    def test_the_blocker_is_named(self):
        self.assertIn("does not expose per-trial residuals", self.w["test_that_would_settle_it"])

    def test_degree_is_excluded_as_the_cause(self):
        self.assertIn("degree 1 and 2", self.w["degree_is_not_the_cause"])


class TestTheNumbersReproduce(unittest.TestCase):
    def test_points_per_valid_is_computed_not_quoted(self):
        rows = W.rates()
        h2 = [r for r in rows if r["h12"] == 2][0]
        self.assertAlmostEqual(h2["points_per_valid"], 53 / 384, places=9)

    def test_the_two_h12_five_runs_are_both_included(self):
        rows = [r for r in W.rates() if r["h12"] == 5]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["points"] == 2 for r in rows))


if __name__ == "__main__":
    unittest.main()


class TestTheArrivalExperiment(unittest.TestCase):
    """Twenty calls: uniformly rare, or clustered?"""

    @classmethod
    def setUpClass(cls):
        cls.a = W.arrivals()

    def test_the_counts_are_the_measured_ones(self):
        self.assertEqual(len(W.ARRIVALS_20), 20)
        self.assertEqual(sum(W.ARRIVALS_20), 11)

    def test_the_verdict_is_uniformly_rare(self):
        self.assertIn("uniformly rare", self.a["verdict"])
        self.assertLess(self.a["variance_over_mean"], 1.5)

    def test_no_call_produced_two_points(self):
        self.assertEqual(self.a["max"], 1)
        self.assertEqual(self.a["observed_calls_with_two_or_more"], 0)

    def test_poisson_would_have_expected_some(self):
        # the discriminating number: if arrivals were free-Poisson we would have seen >= 2 per call twice
        self.assertGreater(self.a["expected_calls_with_two_or_more"], 1.0)

    def test_the_rate_matches_the_five_call_runs(self):
        # 11/20 calls = 0.55 points per call, against 2/5 = 0.40 in the wrapper run
        self.assertAlmostEqual(self.a["mean"], 0.55, places=6)
        self.assertGreater(self.a["rate_per_try"], 0.0)

    def test_the_cap_hypothesis_is_flagged_not_asserted(self):
        self.assertIn("suggests", self.a["note"])
        self.assertIn("lower bound", self.a["note"])


class TestTheArrivalEngineCanFail(unittest.TestCase):
    def test_clustered_counts_are_detected(self):
        clustered = (0, 0, 0, 5, 0, 0, 6, 0, 0, 0)
        a = W.arrivals(clustered)
        self.assertIn("clustered", a["verdict"])

    def test_uniform_counts_read_as_uniform(self):
        uniform = tuple([1, 0] * 10)
        a = W.arrivals(uniform)
        self.assertIn("uniformly rare", a["verdict"])
