"""The observability engine — a proportion is a claim, and the claim has three parts."""
import unittest

from pacland.exactness import observability as O


class TestTheVerdicts(unittest.TestCase):
    def test_a_narrow_stable_proportion_is_measured(self):
        r = O.proportion("k/n", 500, 1000)
        self.assertEqual(r.verdict, "measured")
        self.assertLess(r.ci_high - r.ci_low, 0.1)

    def test_a_threshold_dominated_proportion_is_parameter_limited(self):
        # the estimate is 0.40 and a stated parameter moves it by 0.20 -- that is the threshold talking
        r = O.proportion("k/n", 400, 1000, parameter_spread=0.25)
        self.assertEqual(r.verdict, "parameter-limited")
        self.assertIn("measuring the threshold", r.why)

    def test_a_tiny_sample_is_sample_limited(self):
        r = O.proportion("k/n", 5, 10, coverage=2.4e-5)
        self.assertEqual(r.verdict, "sample-limited")
        self.assertIn("not the space", r.why)

    def test_the_statistical_error_is_reported_even_when_the_verdict_is_not_measured(self):
        r = O.proportion("k/n", 400, 1000, parameter_spread=0.25)
        self.assertGreater(r.ci_high, r.ci_low)
        self.assertEqual(r.n_used, 1000)

    def test_zero_denominator_does_not_explode(self):
        r = O.proportion("k/n", 0, 0)
        self.assertEqual(r.estimate, 0.0)
        self.assertIsNotNone(r.verdict)


class TestTheCorpusReadings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {r.quantity: r for r in O.corpus_readings()}

    def test_the_susy_fraction_survives_scrutiny(self):
        r = self.rows["SUSY fraction (primitive rows)"]
        self.assertEqual(r.verdict, "measured")
        from pacland.exactness import counterexample as C
        prim = [c for c in C.load_corpus() if C.scaling_gcd(c["row"]["flux"]) <= 1]
        susy_prim = sum(1 for c in prim if c["row"].get("is_susy"))
        self.assertAlmostEqual(r.estimate, susy_prim / len(prim), places=9)

    def test_the_minima_fraction_does_not(self):
        r = self.rows["minima fraction (primitive rows)"]
        self.assertEqual(r.verdict, "parameter-limited")
        self.assertIsNotNone(r.parameter_spread)

    def test_it_uses_primitive_rows_not_all_rows(self):
        r = self.rows["primitive fraction"]
        self.assertEqual(r.n_used, 5965)
        self.assertLess(r.estimate, 1.0)


class TestTheEngineCanSayNo(unittest.TestCase):
    def test_a_ratio_that_moves_more_than_its_error_is_downgraded(self):
        # the same numerator, judged twice: stable vs threshold-dominated
        stable = O.proportion("x", 200, 1000)
        moved = O.proportion("x", 200, 1000, parameter_spread=0.15)
        self.assertEqual(stable.verdict, "measured")
        self.assertEqual(moved.verdict, "parameter-limited")
        self.assertEqual(stable.estimate, moved.estimate)


if __name__ == "__main__":
    unittest.main()
