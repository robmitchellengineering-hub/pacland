"""The landscape count — the gauge symmetry barely bites, and the content scales with b3."""
import unittest

from pacland.exactness import landscape_count as L


class TestTheCounts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v = L.verdict()

    def test_the_recorded_numbers_reproduce(self):
        rows = {r["b3"]: r for r in self.v["rows"]}
        self.assertEqual(rows[2]["flux_pairs"], 81)
        self.assertEqual(rows[2]["orbits"], 80)
        self.assertEqual(rows[4]["orbits"], 6560)
        self.assertEqual(rows[6]["orbits"], 531440)
        self.assertEqual(rows[6]["up_to_1"], 107100)

    def test_the_gauge_quotient_is_negligible(self):
        self.assertTrue(self.v["gauge_quotient_negligible"])
        rows = {r["b3"]: r for r in self.v["rows"]}
        self.assertGreater(rows[6]["quotient_ratio"], 0.9999)   # one pair removed out of 531,441

    def test_the_content_scales_with_the_window_at_fixed_L(self):
        # the falsifier: if this holds, the content is NOT a function of the tadpole bound alone
        self.assertTrue(self.v["content_scales_with_b3"])
        ups = [r["up_to_1"] for r in self.v["rows"]]
        self.assertGreater(ups[2], 50 * ups[0])

    def test_the_verdict_is_refuted_and_says_why(self):
        self.assertIn("REFUTED", self.v["verdict"])
        self.assertIn("negligible", self.v["verdict"])

    def test_the_window_is_stated(self):
        self.assertIn("|component| <= 1", self.v["window"])
        self.assertIn("6", self.v["window"])


class TestTheCountingIsExact(unittest.TestCase):
    def test_per_tadpole_classes_sum_to_the_orbit_count(self):
        for row in L.ladder():
            self.assertEqual(sum(row["per_tadpole"].values()), row["orbits"])

    def test_the_zero_tadpole_class_half_fills_the_window(self):
        # the null cone is large: N = 0 is ~24% of the window at b3 = 6
        row = {r["b3"]: r for r in L.ladder()}[6]
        self.assertGreater(row["per_tadpole"][0] / row["orbits"], 0.20)


if __name__ == "__main__":
    unittest.main()
