"""max |N| = b3 is a theorem: bounded by counting brackets, attained by construction."""
import unittest

from pacland.exactness import tadpole_bound as T


class TestTheProof(unittest.TestCase):
    def test_the_bounding_argument(self):
        # each of the n = b3/2 brackets lies in [-2, 2], so |N| <= 2n = b3
        for b3 in (2, 4, 6, 8, 12):
            self.assertEqual(T.bound(b3), 2 * (b3 // 2))

    def test_the_attaining_pair_gives_exactly_the_bound(self):
        for b3 in (2, 4, 6, 8, 12):
            F, H = T.attain(b3)
            self.assertEqual(T.tadpole(F, H), b3)


class TestTheMeasurement(unittest.TestCase):
    def test_four_rungs_agree_with_the_theorem(self):
        for b3 in (2, 4, 6, 8):
            self.assertEqual(T.measured(b3), b3)

    def test_the_bound_is_not_beaten(self):
        # exhaustive at these sizes: nothing in the window exceeds b3
        for b3 in (2, 4, 6):
            self.assertLessEqual(T.measured(b3), b3)


class TestWhatItMeans(unittest.TestCase):
    def test_the_tadpole_grows_linearly_with_b3_at_the_cap(self):
        # the cap is linear in the dimension, which is why 10^500-style counts overestimate reachable flux
        self.assertEqual(T.bound(200) / T.bound(100), 2.0)


if __name__ == "__main__":
    unittest.main()
