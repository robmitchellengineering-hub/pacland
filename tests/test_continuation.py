"""Route C — a period computed outside the large-complex-structure radius."""
import mpmath as mp
import unittest

from pacland.periods import continuation as C


class TestTheTransfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = C.truncation_study()

    def test_the_point_is_outside_the_lcs_radius(self):
        self.assertEqual(self.s["z_over_zc"], mp.mpf("1.5"))
        self.assertGreater(self.s["z_over_zc"], 1)

    def test_the_point_is_inside_the_conifold_chart(self):
        self.assertLess(abs(self.s["u"]), 1)

    def test_the_pass_mark_is_met(self):
        # the plan's pass mark: value moves < 1e-10 between orders N and N+40
        self.assertTrue(self.s["pass_mark_1e-10"], self.s["moves"])

    def test_the_series_converges_with_order(self):
        moves = self.s["moves"]
        self.assertLess(moves[120], moves[80])
        self.assertLess(moves[80], moves[40])

    def test_the_two_charts_are_described(self):
        w = C.where_both_converge()
        self.assertIn("z_c < z < 2 z_c", w["outside_lcs_inside_conifold"])

    def test_the_second_pass_mark_is_not_claimed(self):
        self.assertIn("not yet wired", self.s["note"])


class TestTheEngineCanFail(unittest.TestCase):
    def test_outside_the_conifold_chart_the_series_does_not_converge(self):
        # u = -1.2 is past the chart; the truncation study must report failure, not a number
        s = C.truncation_study(u=mp.mpf("-1.2"), orders=(40, 160))
        self.assertFalse(s["pass_mark_1e-10"])


if __name__ == "__main__":
    unittest.main()
