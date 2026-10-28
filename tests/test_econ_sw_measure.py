"""SW's observables: extracted from the model, mapped to the data, units reconciled."""
import unittest

from pacland.economics import sw_measure as M


class TestMeasurement(unittest.TestCase):
    def test_all_six_observables_are_extracted(self):
        rows = M.measurement()["observables"]
        self.assertEqual(sorted(rows), ["dc", "dinve", "dw", "dy", "pinfobs", "robs"])

    def test_growth_carries_ctrend(self):
        rows = M.measurement()["observables"]
        for obs in ("dy", "dc", "dinve", "dw"):
            self.assertAlmostEqual(rows[obs]["constant"], 0.43, places=9)

    def test_inflation_and_rate_carry_their_own_constants(self):
        rows = M.measurement()["observables"]
        self.assertAlmostEqual(rows["pinfobs"]["constant"], 0.78, places=9)
        self.assertAlmostEqual(rows["robs"]["constant"], 1.540722, places=5)


class TestMapping(unittest.TestCase):
    def test_the_data_maps_to_five_observables(self):
        import json
        data = json.loads(M.VINTAGES.read_text())
        obs = M.observations(data["current"], data.get("rates"))
        self.assertEqual(sorted(obs), ["dc", "dinve", "dy", "pinfobs", "robs"])

    def test_wages_are_named_as_missing(self):
        self.assertEqual(list(M.MISSING), ["dw"])
        self.assertFalse(M.unit_check()["dw_available"])

    def test_quarter_keys_are_idempotent(self):
        self.assertEqual(M._qkey("1985-04-01"), "1985-Q2")
        self.assertEqual(M._qkey("1985-Q2"), "1985-Q2")
        self.assertEqual(M._qkey("1985-12"), "1985-Q4")


class TestUnits(unittest.TestCase):
    def test_the_model_matches_sample_inflation_closely(self):
        rows = M.unit_check()["rows"]
        self.assertLess(abs(rows["pinfobs"]["gap"]), 0.2)

    def test_the_growth_gap_is_reported_not_hidden(self):
        rows = M.unit_check()["rows"]
        self.assertGreater(rows["dy"]["gap"], 0.1)

    def test_the_rate_is_annualised_before_comparison(self):
        rows = M.unit_check()["rows"]
        self.assertEqual(rows["robs"]["clock"], 4.0)
        self.assertLess(abs(rows["robs"]["gap"]), 2.0)

    def test_the_audit_is_green(self):
        self.assertTrue(M.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
