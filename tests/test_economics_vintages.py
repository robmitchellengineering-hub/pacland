"""Real-time vintage tests — parsing, the guards, the models, and the committed run."""
import math
import unittest

from pacland.economics import meese_rogoff as mr, vintages as V


class TestFixture(unittest.TestCase):
    def setUp(self):
        self.data = V.load()

    def test_fixture_has_the_four_series(self):
        self.assertEqual(sorted(self.data["series"]), ["CPIAUCSL", "GDPC1", "GPDIC1", "PCECC96"])

    def test_fixture_has_the_expected_vintages(self):
        self.assertEqual(len(V.vintages(self.data)), 10)

    def test_every_vintage_is_look_ahead_free(self):
        for v in V.vintages(self.data):
            ok, msg = V.guard_no_lookahead(v)
            self.assertTrue(ok, msg)

    def test_current_vintage_is_revised_and_longer(self):
        cur = V.current(self.data)
        self.assertGreaterEqual(len(cur["GDPC1"]), 85)
        first = V.vintages(self.data)[0]
        self.assertLess(len(first.observations("GDPC1")), len(cur["GDPC1"]))


class TestParsing(unittest.TestCase):
    def test_parse_csv_skips_missing_values(self):
        text = "observation_date,GDPC1_20200101\n2020-01-01,100.5\n2020-04-01,.\n2020-07-01,101.5\n"
        out = V.parse_csv(text)
        self.assertEqual(out, {"2020-01-01": 100.5, "2020-07-01": 101.5})

    def test_parse_csv_ignores_a_ragged_row(self):
        text = "observation_date,X\n2020-01-01,1.0\nbroken\n"
        self.assertEqual(V.parse_csv(text), {"2020-01-01": 1.0})


class TestGuards(unittest.TestCase):
    def test_look_ahead_is_caught(self):
        v = V.Vintage(as_of="2000-01-01", series={"GDPC1": {"1999-10-01": 1.0, "2000-04-01": 2.0}})
        ok, msg = V.guard_no_lookahead(v)
        self.assertFalse(ok)
        self.assertIn("LOOK-AHEAD", msg)

    def test_target_leak_is_caught(self):
        hist = [("2000-01-01", 1.0), ("2000-04-01", 1.1)]
        self.assertFalse(V.guard_truth_is_not_input(hist, "2000-04-01")[0])
        self.assertTrue(V.guard_truth_is_not_input(hist, "2000-07-01")[0])

    def test_missing_benchmark_is_refused(self):
        ok, msg = V.guard_benchmark_present({"AR(1)": {1: 0.1}})
        self.assertFalse(ok)
        self.assertIn("benchmark", msg)
        self.assertTrue(V.guard_benchmark_present({"no-change": {1: 0.1}})[0])

    def test_level_scale_errors_are_refused(self):
        # the seeded fault: comparing levels across vintages measures a rebasing
        fake = {m: {1: 0.5, 2: 0.6, 4: 0.7} for m in mr.MODELS}
        ok, msg = mr.guard_growth_not_levels(fake)
        self.assertFalse(ok)
        self.assertIn("LEVELS", msg)


class TestModels(unittest.TestCase):
    def test_ols_recovers_an_exact_linear_relation(self):
        x = [[1.0, float(i)] for i in range(10)]
        y = [2.0 + 3.0 * i for i in range(10)]
        c, m = mr._ols(x, y)
        self.assertAlmostEqual(c, 2.0, places=9)
        self.assertAlmostEqual(m, 3.0, places=9)

    def test_no_change_is_the_last_value(self):
        self.assertEqual(mr.no_change([1.0, 2.0, 3.0], 4), 3.0)

    def test_ar1_recovers_rho(self):
        # y_t = 1 + 0.8 y_{t-1} exactly -> rho must come back
        y = [10.0]
        for _ in range(60):
            y.append(1.0 + 0.8 * y[-1])
        f1 = mr.ar1(y, 1)
        self.assertAlmostEqual(f1, 1.0 + 0.8 * y[-1], places=6)

    def test_var1_recovers_known_coefficients(self):
        # two-variable VAR(1), no noise: the one-step forecast must be exact
        a = [[0.5, 0.0, 0.3], [0.1, 1.0, 0.2]]      # rows: [const, y1, y2]
        y1, y2 = [10.0], [5.0]
        for _ in range(40):
            n1 = a[0][0] + a[0][1] * y1[-1] + a[0][2] * y2[-1]
            n2 = a[1][0] + a[1][1] * y1[-1] + a[1][2] * y2[-1]
            y1.append(n1)
            y2.append(n2)
        f = mr.var1([y1, y2], 1)
        self.assertAlmostEqual(f[0], a[0][0] + a[0][1] * y1[-1] + a[0][2] * y2[-1], places=6)
        self.assertAlmostEqual(f[1], a[1][0] + a[1][1] * y1[-1] + a[1][2] * y2[-1], places=6)

    def test_next_quarter_rolls_over_the_year(self):
        self.assertEqual(mr.next_quarter("1999-10-01", 1), "2000-01-01")
        self.assertEqual(mr.next_quarter("2000-01-01", 4), "2001-01-01")

    def test_balanced_panel_needs_history(self):
        v = V.Vintage(as_of="2000-01-01", series={
            "GDPC1": {"1999-01-01": 1.0}, "PCECC96": {"1999-01-01": 1.0},
            "GPDIC1": {"1999-01-01": 1.0}})
        self.assertIsNone(mr._balanced(v))


class TestTheRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = mr.evaluate()

    def test_the_null_is_the_unit(self):
        for h in (1, 2, 4):
            self.assertAlmostEqual(self.res["no-change"][h] / self.res["no-change"][h], 1.0)

    def test_both_statistical_models_beat_the_null_at_every_horizon(self):
        base = self.res["no-change"]
        for m in ("AR(1)", "VAR(1)"):
            for h in (1, 2, 4):
                self.assertLess(self.res[m][h], base[h], f"{m} at h={h}")

    def test_the_var_beats_the_null_more_often_than_not(self):
        wins = self.res["VAR(1)"]["wins"]
        for h in (1, 2, 4):
            self.assertGreater(wins[h], self.res["VAR(1)"]["n"][h] / 2, f"h={h}")

    def test_the_sample_size_is_reported(self):
        self.assertGreaterEqual(self.res["_meta"]["forecasts"], 20)
        self.assertEqual(self.res["_meta"]["unit"], "log-growth RMSE")

    def test_summary_names_the_benchmark(self):
        self.assertIn("no-change", mr.summary())


if __name__ == "__main__":
    unittest.main()
