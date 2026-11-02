"""The two b3 scales — one is a clean exponential, the other is not, and the product survives both."""
import unittest

from pacland.exactness import b3_scaling as S


class TestTheContentScale(unittest.TestCase):
    def test_the_content_factor_is_about_8_55_per_unit_b3(self):
        self.assertAlmostEqual(S.per_unit_factor(S.CONTENT)["factor"], 8.554, places=2)

    def test_the_content_intervals_agree(self):
        # 8.602 then 8.507 -- a clean exponential, which is what makes A quotable
        r = S.per_unit_factor(S.CONTENT)
        self.assertTrue(r["consistent_exponential"])
        fs = [f for _, _, f in r["intervals"]]
        self.assertLess((max(fs) - min(fs)) / (sum(fs) / len(fs)), 0.02)


class TestTheAccessibilityScale(unittest.TestCase):
    def test_it_falls_but_not_exponentially(self):
        # per-interval 0.575 then 0.308: the rate steepens, so a single B would hide that
        r = S.per_unit_factor(S.ACCESSIBILITY)
        self.assertLess(r["factor"], 1.0)
        self.assertFalse(r["consistent_exponential"])

    def test_the_steepening_is_visible(self):
        fs = [f for _, _, f in S.per_unit_factor(S.ACCESSIBILITY)["intervals"]]
        self.assertLess(fs[1], fs[0])


class TestTheProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = S.scales()

    def test_the_product_exceeds_one_on_every_interval(self):
        self.assertGreater(self.s["product_range"][0], 1.0)

    def test_the_verdict_says_grows(self):
        self.assertIn("GROWS", self.s["verdict"])

    def test_the_caveat_names_the_window_problem(self):
        self.assertIn("windows scale together", self.s["caveat"])
        self.assertIn("heuristic", self.s["caveat"])

    def test_the_falsifier_is_stated(self):
        self.assertIn("fourth b3", self.s["falsifier"])


if __name__ == "__main__":
    unittest.main()
