"""Climate's null tests — the hindcast, the three guards, and the result."""
import copy
import unittest

from pacland.climate import baseline as B


class TestFixture(unittest.TestCase):
    def setUp(self):
        self.data = B.load()

    def test_series_cover_the_window(self):
        self.assertIn(1980, self.data["gmst"])
        self.assertIn(2025, self.data["gmst"])
        self.assertGreater(len(self.data["co2"]), 40)

    def test_units_are_degrees_c(self):
        ok, msg = B.guard_units(self.data)
        self.assertTrue(ok, msg)


class TestNulls(unittest.TestCase):
    def setUp(self):
        self.data = B.load()

    def test_persistence_is_the_level(self):
        self.assertEqual(B.persistence_null(self.data["gmst"], 2000, 10), self.data["gmst"][2000])

    def test_trend_continues_the_fit(self):
        v = B.trend_null(self.data["gmst"], 2000, 10)
        self.assertGreater(v, self.data["gmst"][2000])   # warming continued

    def test_co2_is_extrapolated_not_observed(self):
        path = B.co2_path(self.data["co2"], 2000, 10)
        for year, ppm in path.items():
            if year > 2000:
                # not the observed value: a linear extrapolation of data ≤ 2000
                self.assertNotEqual(ppm, self.data["co2"].get(year))

    def test_emulator_starts_from_the_observed_anomaly(self):
        v = B.emulator(3.0, 3.7, self.data, 2000, 0)
        self.assertAlmostEqual(v, self.data["gmst"][2000], places=12)


class TestGuards(unittest.TestCase):
    def setUp(self):
        self.data = B.load()

    def test_no_lookahead(self):
        ok, msg = B.guard_no_lookahead(self.data, 2000, 20)
        self.assertTrue(ok, msg)

    def test_truth_outside_window(self):
        self.assertTrue(B.guard_truth_is_outside_the_window(self.data, 2000, 20)[0])


class TestHindcast(unittest.TestCase):
    def setUp(self):
        self.data = B.load()

    def test_it_produces_every_method(self):
        models = {"X": (3.0, 3.7)}
        r = B.hindcast(self.data, models, 2000, 10)
        for key in ("persistence", "trend", "emulator:X", "truth"):
            self.assertIn(key, r)

    def test_a_missing_target_is_refused(self):
        with self.assertRaises(ValueError):
            B.hindcast(self.data, {}, 2020, 20)


class TestTheResult(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = B.evaluate()

    def test_seven_hindcasts(self):
        self.assertEqual(self.r["n"], 7)

    def test_the_trend_null_is_the_strongest(self):
        m = self.r["methods"]
        emulators = [k for k in m if k.startswith("emulator:")]
        for e in emulators:
            self.assertGreater(m[e]["mae"], m["trend"]["mae"] - 1e-12, e)

    def test_emulators_beat_persistence(self):
        m = self.r["methods"]
        for e in [k for k in m if k.startswith("emulator:")]:
            self.assertLess(m[e]["mae"], m["persistence"]["mae"])

    def test_summary_says_what_the_emulators_are_not(self):
        s = B.summary()
        self.assertIn("NOT the CMIP6 runs", s)


if __name__ == "__main__":
    unittest.main()
