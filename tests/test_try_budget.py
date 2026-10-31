"""The try-budget wrapper — and the honesty about what a budget can count."""
import time
import unittest

from pacland.exactness import try_budget as T


class TestTheBudget(unittest.TestCase):
    def test_it_spends_exactly_the_call_budget(self):
        r = T.run_to_budget(T.dry_sampler([[1], [2], [3]]), calls=3)
        self.assertEqual(r.calls, 3)
        self.assertEqual(r.points, [1, 2, 3])
        self.assertIn("call budget", r.stopped_because)

    def test_it_stops_early_when_a_point_is_found(self):
        r = T.run_to_budget(T.dry_sampler([[], [], [7], [8]]), calls=5, stop_when_found=1)
        self.assertEqual(r.calls, 3)
        self.assertEqual(r.points, [7])
        self.assertIn("found 1 point", r.stopped_because)

    def test_it_reports_a_wall_clock_budget(self):
        slow = T.dry_sampler([[], [], [], [], []])
        def ticking():
            time.sleep(0.01)
            return slow()
        r = T.run_to_budget(ticking, calls=100, seconds=0.05)
        self.assertLess(r.calls, 100)
        self.assertIn("wall-clock", r.stopped_because)

    def test_the_yield_is_per_call_and_per_second(self):
        r = T.run_to_budget(T.dry_sampler([[1], [1]]), calls=2)
        self.assertAlmostEqual(r.yield_per_call, 1.0)
        self.assertGreater(r.yield_per_second, 0.0)

    def test_the_try_count_is_reported_as_unknown(self):
        r = T.run_to_budget(T.dry_sampler([[1]]), calls=1)
        self.assertIn("unknown", r.tries)


class TestTheBudgetCanFail(unittest.TestCase):
    def test_zero_calls_does_nothing_rather_than_crashing(self):
        r = T.run_to_budget(T.dry_sampler([[1]]), calls=0)
        self.assertEqual(r.calls, 0)
        self.assertEqual(r.points, [])
        self.assertEqual(r.yield_per_call, 0.0)

    def test_a_sampler_returning_nothing_reports_zero_yield(self):
        r = T.run_to_budget(T.dry_sampler([[], [], []]), calls=3)
        self.assertEqual(r.points, [])
        self.assertEqual(r.yield_per_call, 0.0)
        self.assertEqual(r.per_call, [0, 0, 0])


if __name__ == "__main__":
    unittest.main()
