"""Padgett's intuition, made testable — and the instrument's own limits."""
import math
import unittest

from pacland.spectral import prime_interference as PI


class TestTheDefinitions(unittest.TestCase):
    def test_the_seven_sets_are_built(self):
        d = PI.definitions(1000)
        self.assertEqual(len(d), 7)
        self.assertIn("ALL ODD NUMBERS (control)", d)
        self.assertTrue(all(d[k] for k in d))

    def test_the_concrete_sets_are_right(self):
        d = PI.definitions(30)
        self.assertEqual(d["all primes"], [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
        self.assertTrue(all(p % 4 == 1 for p in d["primes = 1 mod 4"]))


class TestTheWalkRatio(unittest.TestCase):
    def test_a_random_set_sits_at_order_one(self):
        import random
        random.seed(7)
        vals = [random.uniform(0, 2 * math.pi) for _ in range(5000)]
        r = PI.walk_ratio(vals, theta=1.0, at=(1600,))
        self.assertTrue(0.2 < r[0][1] < 5.0, r)

    def test_the_odd_numbers_cancel_hard(self):
        # the control's amplitude collapses: at theta=1 a uniformly spaced odd set is a geometric series
        r = PI.walk_ratio([k for k in range(3, 20001, 2)], at=(400, 6400))
        self.assertLess(r[-1][1], r[0][1])

    def test_primes_do_not_resist_cancellation(self):
        # the claim would need |S|/sqrt(k) to GROW; it does not
        r = PI.walk_ratio(PI.primes_upto(20000), at=(400, 6400))
        self.assertLess(r[-1][1], 5.0)


class TestTheRatioStatisticIsNotUniversal(unittest.TestCase):
    def test_a_lattice_gives_one_not_poisson(self):
        # a uniform set has constant gaps, so r = 1 -- far from Poisson(0.386) and GOE(0.531).
        # This is why the raw-gap ratio is NOT a valid spectrum test for an arithmetic set, and the module
        # says so rather than quoting Poisson.
        self.assertAlmostEqual(PI.ratio_statistic([2 * k for k in range(100)]), 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
