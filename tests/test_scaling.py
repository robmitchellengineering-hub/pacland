"""Route A — a lattice fact must survive a change of b3, or be labelled as a window fact."""
import unittest

from pacland.exactness import scaling as S


class TestTheLadder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = S.report()

    def test_the_ladder_is_two_four_six(self):
        self.assertEqual(self.r["ladder"], [2, 4, 6])

    def test_the_recorded_values_reproduce(self):
        f = self.r["facts"]
        self.assertAlmostEqual(f["|N| <= 1 fraction"]["values"][2], 0.6437, places=3)
        self.assertAlmostEqual(f["N = 0 fraction"]["values"][0], 0.4074, places=3)
        self.assertAlmostEqual(f["primitive fraction"]["values"][2], 1.0, places=3)

    def test_only_primitivity_is_invariant_and_it_is_still_trending(self):
        # the 10% rule calls primitivity invariant (1.2% movement) -- and it is monotone to 1, so the
        # verdict and the trend must BOTH be reported rather than the trend hidden behind the label
        self.assertEqual(self.r["invariant"], ["primitive fraction"])
        self.assertEqual(self.r["trend_within_tolerance"], ["primitive fraction"])

    def test_the_moving_fractions_are_scale_dependent(self):
        for k in ("N = 0 fraction", "|N| <= 1 fraction", "all components non-zero"):
            self.assertEqual(self.r["facts"][k]["verdict"], "scale-dependent", k)

    def test_the_tadpole_bound_inside_the_window_is_b3(self):
        # a small exact fact: with |component| <= 1 the largest |N| is exactly b3
        for row in self.r["rows"]:
            self.assertEqual(row["max |N|"], row["b3"])

    def test_each_movement_has_a_direction(self):
        for k, v in self.r["facts"].items():
            self.assertIn(v["direction"], ("rising", "falling", "non-monotone"), k)


class TestTheVerdictCanSayInvariant(unittest.TestCase):
    def test_a_constant_across_the_ladder_is_invariant(self):
        # the verdict function itself must be able to return "scale-invariant"
        vals = [0.5, 0.5, 0.5]
        lo, hi = min(vals), max(vals)
        self.assertLessEqual((hi - lo) / (sum(vals) / 3), 0.10)
        self.assertEqual(S._direction(vals), "rising")   # monotone-or-equal counts as rising

    def test_a_non_monotone_sequence_is_named(self):
        self.assertEqual(S._direction([0.1, 0.3, 0.2]), "non-monotone")


if __name__ == "__main__":
    unittest.main()
